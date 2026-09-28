This is Python's "mutable default argument" gotcha.

Python evaluates default values **once, when the function is defined**, not each time it's called. So `tags=[]` creates a single list object, and every call that doesn't pass `tags` uses that same list. The first call adds `'a'` to it and the second call adds `'b'` to the same list, which is why you get `['a', 'b']`.

You can see the shared list here:

```python
print(add_tag.__defaults__)  # (['a', 'b'],) after your two calls
```

**Fix:** use `None` as the default and create a new list inside the function:

```python
def add_tag(tag, tags=None):
    if tags is None:
        tags = []
    tags.append(tag)
    return tags

print(add_tag('a'))  # ['a']
print(add_tag('b'))  # ['b']
```

The same applies to any mutable default, such as `{}`, `set()`, or a custom object. Immutable defaults like `None`, numbers, strings, and tuples are safe.
