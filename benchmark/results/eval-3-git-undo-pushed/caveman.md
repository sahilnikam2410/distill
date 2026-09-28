Already pushed to shared `main`, so use revert. Revert makes new commits that undo old ones. No history rewrite, and teammates stay unbroken.

```bash
git revert --no-edit HEAD~3..HEAD
git push origin main
```

This makes 3 revert commits, newest first. If you want one commit instead:

```bash
git revert --no-commit HEAD~3..HEAD
git commit -m "Revert last 3 commits"
git push origin main
```

Check first with `git log --oneline -5` that the last 3 are the right ones. Merge commit in range makes revert fail, so revert that one with `git revert -m 1 <sha>`.

**Other way: rewrite history (only if you're the only one on the repo).**

> **Warning:** This deletes the 3 commits from `main` on the remote. Anyone who already pulled them gets diverged history. Any commits pushed by others after yours get wiped. Branch protection may also block force push.
> ```bash
> git reset --hard HEAD~3
> git push --force-with-lease origin main
> ```
> `--hard` also throws away uncommitted local changes. If you want to keep the changes as unstaged edits, use `--soft` or `--mixed`.

Mistake after reset? `git reflog` finds the old SHA. `git reset --hard <sha>` gets it back.
