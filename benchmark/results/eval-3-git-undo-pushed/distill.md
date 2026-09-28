Use `git revert`. It adds new commits that undo the changes, so you don't rewrite history on `main` that others may already have pulled.

```bash
git checkout main && git pull
git revert --no-edit HEAD~3..HEAD   # creates 3 revert commits, newest first
git push
```

If you'd rather have one revert commit:

```bash
git revert --no-commit HEAD~3..HEAD
git commit -m "Revert last 3 commits"
git push
```

Notes:
- If any of the 3 is a merge commit, the revert fails unless you add `-m 1`.
- If there's a conflict, fix the files, then run `git add <files>` and `git revert --continue`.
- To check which commits will be reverted first, run `git log --oneline -3`.

**Warning:** The other way is `git reset --hard HEAD~3` followed by `git push --force`. It rewrites `main` and breaks the clone of anyone who already pulled. It also permanently discards any uncommitted local changes, and it's often blocked by branch protection. Only use it if nobody else uses the repo.
