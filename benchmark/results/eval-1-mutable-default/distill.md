Cause: Python evaluates default args once, when the `def` line runs, not on each call. Every call without `tags` gets the same list, so appends carry over.

Fix: default to `None` and make a new list inside the function.

```python
def add_tag(tag, tags=None):
    if tags is None:
        tags = []
    tags.append(tag)
    return tags
```

Now `add_tag('b')` returns `['b']`. Any mutable default (`{}`, `set()`) has the same problem.
