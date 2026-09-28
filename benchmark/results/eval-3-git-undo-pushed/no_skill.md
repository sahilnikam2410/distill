Because the commits are already on `main`, the safest way to undo them is `git revert`. It adds new commits that cancel out the old ones, so history isn't rewritten and anyone who already pulled won't have problems.

**Option 1: Revert (recommended for a shared branch)**

```bash
git checkout main
git pull                      # make sure you're up to date
git log --oneline -5          # check that the top 3 are the ones you want to undo

git revert --no-edit HEAD~3..HEAD   # creates 3 revert commits, newest first
git push origin main
```

If you'd rather have one revert commit instead of three:

```bash
git revert --no-commit HEAD~3..HEAD
git commit -m "Revert last 3 commits"
git push origin main
```

If any of the three is a merge commit, revert that one on its own with `git revert -m 1 <sha>`.

**Option 2: Reset and force-push (rewrites history)**

Only do this if nobody else uses `main` or has pulled those commits, and branch protection allows force-pushes:

```bash
git reset --hard HEAD~3               # careful: this also discards any uncommitted changes
git push --force-with-lease origin main
```

If someone else has already pulled the commits, this leaves their history out of sync with `main`. `--force-with-lease` at least stops you from overwriting commits someone else pushed in the meantime.

**Want to keep the changes locally?** Use `git reset --soft HEAD~3` instead of `--hard` in Option 2. It removes the commits but leaves their changes staged.

When the branch is shared, stick with Option 1.
