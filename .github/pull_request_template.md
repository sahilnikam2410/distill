## Summary

<!-- What changed and why. -->

## Checklist

- [ ] `ruff check . && ruff format --check .` passes
- [ ] `pytest` passes
- [ ] If `SKILL.md` or `scripts/` changed: ran `python scripts/build_skill.py` and committed `distill.skill`
- [ ] If behavior changed: added an entry under "Unreleased" in `CHANGELOG.md`
- [ ] If benchmark numbers changed: updated `README.md` and `benchmark/results/`
