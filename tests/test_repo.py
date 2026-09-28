"""Consistency checks across manifests, skill metadata and the release bundle."""

import json
import re

from conftest import ROOT, SKILL_DIR

MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
PLUGIN = ROOT / "plugins" / "distill" / ".claude-plugin" / "plugin.json"
SKILL_MD = SKILL_DIR / "SKILL.md"
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def frontmatter():
    text = SKILL_MD.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert match, "SKILL.md must start with a --- frontmatter block"
    fields = {}
    for line in match.group(1).splitlines():
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


def test_manifests_agree():
    market, plugin = load(MARKETPLACE), load(PLUGIN)
    entry = next(p for p in market["plugins"] if p["name"] == plugin["name"])

    assert SEMVER.match(plugin["version"])
    assert market["metadata"]["version"] == plugin["version"]
    assert entry["description"] == plugin["description"]
    assert (ROOT / entry["source"] / ".claude-plugin" / "plugin.json").resolve() == PLUGIN


def test_skill_frontmatter():
    fields = frontmatter()
    assert fields["name"] == "distill"
    assert re.fullmatch(r"[a-z0-9-]{1,64}", fields["name"])
    assert 0 < len(fields["description"]) <= 1024


def test_skill_references_existing_files():
    text = SKILL_MD.read_text(encoding="utf-8")
    for rel in set(re.findall(r"`(scripts/[\w./-]+)`", text)):
        assert (SKILL_DIR / rel).is_file(), f"SKILL.md references missing {rel}"


def test_evals_file():
    evals = load(ROOT / "benchmark" / "tasks" / "evals.json")
    assert evals["skill_name"] == "distill"
    ids = [e["id"] for e in evals["evals"]]
    assert ids == sorted(set(ids))
    for e in evals["evals"]:
        for rel in e["files"]:
            assert (ROOT / "benchmark" / "tasks" / rel).exists()


def test_bundle_is_up_to_date(build_skill):
    assert build_skill.main(["--check"]) == 0
