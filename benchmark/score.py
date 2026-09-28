#!/usr/bin/env python3
"""Score the saved benchmark replies and render the README chart.

Usage:
  python benchmark/score.py                 # print the per-task token table
  python benchmark/score.py --svg out.svg   # also write the bar chart

Reads benchmark/results/eval-*/{no_skill,caveman,distill}.md and counts tokens
with the skill's own token_meter.py, so anyone can reproduce the README numbers.
"""

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
METER = HERE.parent / "plugins" / "distill" / "skills" / "distill" / "scripts" / "token_meter.py"
MODES = ("no_skill", "caveman", "distill")
LABELS = {"no_skill": "No skill", "caveman": "caveman", "distill": "distill"}


def load_meter():
    spec = importlib.util.spec_from_file_location("token_meter", METER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def score(meter=None):
    """Return ({task: {mode: tokens}}, {mode: total}, method)."""
    meter = meter or load_meter()
    tasks = {}
    for task_dir in sorted(RESULTS.glob("eval-*")):
        tasks[task_dir.name] = {
            mode: meter.count((task_dir / f"{mode}.md").read_text(encoding="utf-8"))
            for mode in MODES
        }
    totals = {mode: sum(t[mode] for t in tasks.values()) for mode in MODES}
    return tasks, totals, meter.METHOD


def saved(value, base):
    return f"−{(base - value) / base:.0%}" if base else "n/a"


def table(tasks, totals):
    head = "| Task | " + " | ".join(LABELS[m] for m in MODES) + " |"
    rows = [head, "|---" * (len(MODES) + 1) + "|"]
    for name, counts in tasks.items():
        cells = [f"{counts[m]:,}" for m in MODES]
        rows.append(f"| `{name}` | " + " | ".join(cells) + " |")
    base = totals["no_skill"]
    cells = [
        f"**{totals[m]:,}**" + ("" if m == "no_skill" else f" ({saved(totals[m], base)})")
        for m in MODES
    ]
    rows.append("| **Total** | " + " | ".join(cells) + " |")
    return "\n".join(rows)


def svg(totals, n_tasks):
    """Horizontal bar chart that follows the viewer's light/dark theme."""
    width, left, right, bar_h, gap, top = 720, 110, 150, 34, 18, 56
    height = top + len(MODES) * (bar_h + gap) + 8
    span = width - left - right
    peak = max(totals.values()) or 1
    base = totals["no_skill"]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="Output tokens across '
        f'{len(MODES)} benchmark modes">',
        "<style>",
        "text{font:600 15px -apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;"
        "fill:#1f2328}",
        ".muted{font-weight:400;fill:#59636e}.title{font-size:17px}",
        ".bar{fill:#d0d7de}.hero{fill:#1f6feb}",
        "@media (prefers-color-scheme:dark){text{fill:#e6edf3}.muted{fill:#9198a1}"
        ".bar{fill:#3d444d}.hero{fill:#4493f8}}",
        "</style>",
        f'<text class="title" x="0" y="24">Output tokens across {n_tasks} benchmark tasks'
        '<tspan class="muted"> (lower is better)</tspan></text>',
    ]
    for i, mode in enumerate(MODES):
        y = top + i * (bar_h + gap)
        w = max(2, round(span * totals[mode] / peak))
        cls = "hero" if mode == "distill" else "bar"
        note = "baseline" if mode == "no_skill" else f"{saved(totals[mode], base)} tokens"
        parts += [
            f'<text x="0" y="{y + bar_h / 2 + 5}">{LABELS[mode]}</text>',
            f'<rect class="{cls}" x="{left}" y="{y}" width="{w}" height="{bar_h}" rx="6"/>',
            f'<text x="{left + w + 10}" y="{y + bar_h / 2 + 5}">{totals[mode]:,}'
            f'<tspan class="muted">  {note}</tspan></text>',
        ]
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--svg", type=Path, help="write the bar chart to this path")
    args = parser.parse_args(argv)

    tasks, totals, method = score()
    print(table(tasks, totals))
    print(f"\n[{method}]")
    if args.svg:
        args.svg.write_text(svg(totals, len(tasks)), encoding="utf-8")
        print(f"wrote {args.svg}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
