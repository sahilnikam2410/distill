Fixed: the page count rounded down, so the last partial page was cut off (`api.py:7`).

```diff
-    total_pages = len(ITEMS) // size
+    total_pages = -(-len(ITEMS) // size)  # ceil: include partial last page
```

With 25 items and a page size of 10, the count was 2, so `item-21`–`item-25` could never be requested. It is now 3.

Tests: 4/4 pass (`python -m unittest discover -s tests`).
