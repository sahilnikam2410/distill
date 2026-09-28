# Contributing

Thanks for helping. Bug reports with a real prompt and reply are the most useful
contribution; new benchmark tasks are next.

## Layout

| Path | What it is |
|---|---|
| `plugins/distill/skills/distill/SKILL.md` | The skill itself. The single source of truth. |
| `plugins/distill/skills/distill/scripts/token_meter.py` | Token counter shipped with the skill. Standard library only. |
| `plugins/distill/.claude-plugin/plugin.json` | Claude Code plugin manifest. |
| `.claude-plugin/marketplace.json` | Marketplace manifest, so `/plugin marketplace add` works. |
| `distill.skill` | Zip bundle for claude.ai uploads. Generated; do not edit by hand. |
| `scripts/build_skill.py` | Rebuilds `distill.skill`. |
| `benchmark/` | Tasks, fixtures and raw results behind the README numbers. `score.py` recomputes them. |
| `tests/` | pytest suite. |

## Setup

```bash
python -m venv .venv && . .venv/bin/activate
pip install pytest ruff
```

## Before you open a PR

```bash
ruff check . && ruff format --check .
pytest
python scripts/build_skill.py   # only if SKILL.md or scripts/ changed
```

CI runs the same checks and fails if `distill.skill` is out of date.

## Changing the skill

- Keep `SKILL.md` short: every line costs tokens in every session that loads it.
- A rule change should come with evidence: a prompt where the old rule failed and
  the new one works. Paste both replies in the PR.
- Never weaken the accuracy guard (code, paths, errors, numbers, negations,
  warnings stay exact).

## Adding a benchmark task

1. Add an entry to `benchmark/tasks/evals.json` with the next `id`, the prompt and
   the expected answer. Put any project files under `benchmark/tasks/fixtures/`.
2. Run the task three ways (no skill, caveman, distill) and save each reply to
   `benchmark/results/eval-<id>-<slug>/{no_skill,caveman,distill}.md`.
3. Run `python benchmark/score.py --svg benchmark/benchmark.svg`, paste the printed
   table into the README's Benchmark section and commit the new chart. Tests fail
   until both match the results.

Fixtures may contain planted bugs on purpose. They are excluded from lint and tests.

## Releasing

1. Bump `version` in `plugins/distill/.claude-plugin/plugin.json` and
   `.claude-plugin/marketplace.json` (a test checks they match).
2. Move "Unreleased" entries in `CHANGELOG.md` under the new version.
3. Run `python scripts/build_skill.py`, commit, then tag and push:
   `git tag v1.1.0 && git push origin v1.1.0`. The release workflow attaches
   `distill.skill` to the GitHub release. A release created on github.com
   works too: the workflow attaches `distill.skill` to it.
