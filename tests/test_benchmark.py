"""The README's benchmark numbers and chart must match the saved replies."""

from conftest import ROOT


def test_readme_table_matches_results(bench):
    tasks, totals, _ = bench.score()
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert bench.table(tasks, totals) in readme


def test_chart_matches_results(bench):
    tasks, totals, _ = bench.score()
    chart = (ROOT / "benchmark" / "benchmark.svg").read_text(encoding="utf-8")
    hint = "run: python benchmark/score.py --svg benchmark/benchmark.svg"
    assert chart == bench.svg(totals, len(tasks)), hint


def test_every_task_has_all_modes():
    for task_dir in sorted((ROOT / "benchmark" / "results").glob("eval-*")):
        for mode in ("no_skill", "caveman", "distill"):
            assert (task_dir / f"{mode}.md").is_file(), f"{task_dir.name} is missing {mode}.md"
