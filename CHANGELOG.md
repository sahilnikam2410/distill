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
- `CONTRIBUTING.md`, issue and pull request templates, `.editorconfig`.

### Fixed
- `benchmark/tasks/evals.json` named the skill `lean` instead of `distill`.
- `distill.skill` shipped `SKILL.md` with CRLF line endings.

## [1.0.0] - 2026-09-28

### Added
- First release: the distill skill (levels `lite`, `pro`, `max`, `auto` and
  three wenyan levels), `token_meter.py`, the Claude Code plugin and
  marketplace manifests, and a 3-task benchmark against caveman and no skill.
