Mutable default arg. `tags=[]` evaluated once, at `def` time, not per call. Every call without `tags` share same list object. First call append `'a'`, second call get same list, append `'b'` → `['a', 'b']`.

Fix: default to `None`, make new list inside:

```python
def add_tag(tag, tags=None):
    if tags is None:
        tags = []
    tags.append(tag)
    return tags

print(add_tag('a'))  # ['a']
print(add_tag('b'))  # ['b']
```

Same trap for `{}`, `set()`, any mutable default. Proof: `add_tag.__defaults__` show list growing.
