For a team of 4 opening PRs on GitHub, I'd rebase your feature branch onto main as long as you're the only one pushing to it. If other people commit to the same branch, merge main into it instead.

**Why rebase is usually better here**
- Your PR shows only your commits, with no "Merge branch 'main' into feature" noise, so it's easier to review.
- History stays linear, which makes `git log` and `git bisect` simpler.
- You fix conflicts one commit at a time, against the commit that caused them.

**Workflow:**
```bash
git fetch origin
git rebase origin/main
# fix conflicts: edit, git add <file>, git rebase --continue
git push --force-with-lease
```
Use `--force-with-lease`, not `--force`. It refuses to push if someone else pushed to the branch since you last fetched, so you can't silently wipe out their work.

**When to merge instead** (`git merge origin/main`)
- Someone else has commits on your branch or has it checked out. Rebasing rewrites commit hashes and breaks their copy.
- A long branch with many commits hits the same conflicts over and over during a rebase. Either merge, or squash your commits first (`git rebase -i`) and then rebase.
- Reviewers are partway through a review and you don't want to reset GitHub's "changes since last review" view. A force-push can make incremental review harder.

**Two things that matter more than this choice**
1. **How PRs land on main.** If you enable "Squash and merge" in the repo settings, each PR becomes one commit on main. Main stays clean whichever way you update feature branches, so the choice only affects how the branch looks during review. Many small teams pick this and stop worrying about it.
2. **Agreeing as a team.** Choose one approach, write it in your CONTRIBUTING file or README, and optionally turn on "Require branches to be up to date before merging" in branch protection. The "Update branch" button on the PR page can then do either a merge or a rebase for you.

**Tip:** run `git config --global rerere.enabled true` so Git remembers how you resolved a conflict and reuses that fix when the same conflict comes up again. This helps a lot if you rebase often.

**In short:** rebase your own branches with `--force-with-lease`, merge when a branch is shared, and consider squash-merging PRs into main.
