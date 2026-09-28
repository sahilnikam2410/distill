#!/usr/bin/env python3
"""Build distill.skill (the claude.ai upload bundle) from the plugin source.

Usage:
  python scripts/build_skill.py           # rebuild distill.skill
  python scripts/build_skill.py --check   # exit 1 if distill.skill is out of date

The archive is deterministic (sorted entries, fixed timestamps, LF endings), so
rebuilding an unchanged source produces an identical file.
"""

import argparse
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "plugins" / "distill" / "skills" / "distill"
BUNDLE = ROOT / "distill.skill"
PREFIX = "distill"
EPOCH = (1980, 1, 1, 0, 0, 0)
IGNORED = {"__pycache__", ".DS_Store"}


def source_files():
    """Map archive name -> file bytes for every file in the skill directory."""
    files = {}
    for path in sorted(SKILL_DIR.rglob("*")):
        if path.is_dir() or IGNORED.intersection(path.parts) or path.suffix == ".pyc":
            continue
        name = f"{PREFIX}/{path.relative_to(SKILL_DIR).as_posix()}"
        files[name] = path.read_bytes().replace(b"\r\n", b"\n")
    return files


def bundle_files(bundle):
    with zipfile.ZipFile(bundle) as zf:
        return {
            info.filename: zf.read(info).replace(b"\r\n", b"\n")
            for info in zf.infolist()
            if not info.is_dir()
        }


def build(files, bundle):
    with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, data in files.items():
            info = zipfile.ZipInfo(name, date_time=EPOCH)
            info.compress_type = zipfile.ZIP_DEFLATED
            mode = 0o755 if name.endswith(".py") else 0o644
            info.external_attr = (0o100000 | mode) << 16
            zf.writestr(info, data)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="verify instead of writing")
    args = parser.parse_args(argv)

    files = source_files()
    if args.check:
        if not BUNDLE.exists():
            print(f"{BUNDLE.name} is missing; run: python scripts/build_skill.py")
            return 1
        current = bundle_files(BUNDLE)
        if current != files:
            changed = sorted(
                set(current) ^ set(files)
                | {n for n in set(current) & set(files) if current[n] != files[n]}
            )
            print(f"{BUNDLE.name} is out of date: {', '.join(changed)}")
            print("Run: python scripts/build_skill.py")
            return 1
        print(f"{BUNDLE.name} is up to date ({len(files)} files)")
        return 0

    build(files, BUNDLE)
    print(f"wrote {BUNDLE.relative_to(ROOT)} ({len(files)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
