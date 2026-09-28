Use `git rebase` if only you push to the feature branch. Use `git merge` if teammates also push to it.

Rebase keeps the PR history linear and easier to review. Merge doesn't rewrite commits that other people already have.

```
git fetch origin
git rebase origin/main
git push --force-with-lease
```

**Warning:** Rebasing rewrites your commits, so you have to force-push afterward. Use `--force-with-lease`: it refuses the push if someone else has pushed to the branch since your last fetch. A plain `--force` would silently overwrite their work.

If you squash-merge PRs on GitHub, the choice matters less, because the branch's commit history (merge commits included) becomes a single commit on main.
