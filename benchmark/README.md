# Benchmark

Each task in [`tasks/evals.json`](tasks/evals.json) was run three ways: with no
skill, with the caveman skill, and with distill. The saved replies are in
[`results/`](results), one folder per task.

## How the runs were made

- Every run was a fresh Claude Code session with no shared context.
- All three modes got the same wrapper: the user's message, plus "your final
  message is shown to that user verbatim". Skill modes were also told to load
  their `SKILL.md` at its default level. Nothing else differed.
- Agentic tasks (`eval-2`, `eval-7`) ran in a private copy of the fixture under
  [`tasks/fixtures/`](tasks/fixtures), which contains a planted bug.
- Tasks 0–2 were run for v1.0.0; tasks 3–7 were added in v1.1.0 with the
  same method.

## Grading

A reply is correct if it contains everything in the task's `expected_output`.
For agentic tasks the fixture's tests must also pass after the fix. All 24
replies (8 tasks × 3 modes) were correct.

## Counting

`python benchmark/score.py` counts tokens in every saved reply with the skill's
own [`token_meter.py`](../plugins/distill/skills/distill/scripts/token_meter.py)
and prints the table used in the main README. Counts are estimates. Tool calls
exclude loading the skill file and are listed in the main README.

## Limits

One run per mode, eight tasks, one grader. Treat the numbers as indicative,
not precise. New tasks are welcome; see [CONTRIBUTING.md](../CONTRIBUTING.md).
