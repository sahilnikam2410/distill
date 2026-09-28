Fixed. Tests pass now: 4/4, run with `python -m unittest discover -s tests`. They failed before on `ValueError: page 3 out of range (1-2)`.

Bug in `api.py` `list_items`. It counted pages with floor division, `len(ITEMS) // size`. 25 items at size 10 → 2 pages. So page 3 (`item-21`..`item-25`) raised out-of-range, and users never saw last partial page.

Fix, `/tmp/claude-0/-home-user-distill/64c5fe7a-bd69-5582-a3a3-6991449170e0/scratchpad/runs/paging-caveman/api.py` line 7:
```python
total_pages = -(-len(ITEMS) // size)  # ceil: keep partial last page
```
Rounds up now → 3 pages. Exact multiples still right (25/5 → 5). `paginate.py` slicing already correct, not touched.

Two edge cases left alone, not in scope:
- Empty `ITEMS` → 0 pages, so `page=1` raises.
- `size <= 0` → `ZeroDivisionError` or negative page count, since size never validated.
