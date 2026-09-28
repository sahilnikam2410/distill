Rebase. Merge only if branch shared.

**Rebase when branch is yours alone** (most feature branches):
- History stays linear. No "Merge branch 'main' into feature" noise in PR.
- PR diff cleaner for reviewers.
- Cost: rewrites commits, so needs force push.

```bash
git fetch origin
git rebase origin/main
# fix conflicts, then: git add <file> && git rebase --continue
git push --force-with-lease
```

Use `--force-with-lease`, not `--force`. It refuses to push if someone else pushed to branch since your last fetch.

**Merge when someone else also commits to same branch:**
- Rebase rewrites their base. Their next pull breaks.
- Merge safe, no force push.

```bash
git fetch origin
git merge origin/main
git push
```

**Team of 4 on GitHub:**
1. Agree on one rule: "own branch → rebase, shared branch → merge."
2. Set repo to **Squash and merge** (Settings → General → Pull Requests). Each PR lands on main as one commit, so your branch history matters less. Messy merge commits disappear on squash.
3. Optional: enable "Require branches to be up to date before merging". GitHub "Update branch" button then offers merge or rebase.

**Rebase gotchas:**
- Long branch plus many conflicts means rebase replays each commit and you may fix same conflict many times. Turn on `git config --global rerere.enabled true` so git remembers resolutions, or merge instead.
- Force push mid-review can make GitHub review comments show as "outdated". Minor, but tell reviewers.

TL;DR: solo branch → `git rebase origin/main` + `--force-with-lease`. Shared branch → `git merge origin/main`. Squash-merge PRs.
