# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- CI: lint (ruff), tests on Python 3.9 and 3.13, a tiktoken smoke test, and a
  check that `distill.skill` matches the plugin source.
- Release workflow: pushing a `vX.Y.Z` tag publishes a GitHub release with
  `distill.skill` attached.
- `scripts/build_skill.py` to rebuild `distill.skill` deterministically.
- Tests for `token_meter.py` and for manifest/skill consistency.
- `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, issue and pull request
  templates, Dependabot for GitHub Actions, `.editorconfig`.
- `benchmark/score.py` recomputes the benchmark table and chart from the saved
  replies; tests fail if the README drifts from the results.
- Theme-aware SVG benchmark chart (replaces `benchmark/benchmark.png`) and a
  social preview image (`.github/social-preview.png`).

### Changed
- README rewritten: before/after examples, per-task benchmark table, FAQ.

### Fixed
- `benchmark/tasks/evals.json` named the skill `lean` instead of `distill`.
- `distill.skill` shipped `SKILL.md` with CRLF line endings.

## [1.0.0] - 2026-09-28

### Added
- First release: the distill skill (levels `lite`, `pro`, `max`, `auto` and
  three wenyan levels), `token_meter.py`, the Claude Code plugin and
  marketplace manifests, and a 3-task benchmark against caveman and no skill.
