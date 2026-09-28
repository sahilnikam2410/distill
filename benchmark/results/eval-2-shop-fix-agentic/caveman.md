Bug in `cart.py` `total()`. Tax got applied to full subtotal, then discount subtracted untaxed. Docstring + tests want tax on discounted amount.

Before:
```python
taxed = sub * (1 + TAX_RATE)
return money(taxed - disc)
```

After:
```python
return money((sub - disc) * (1 + TAX_RATE))
```

Example: $100 + SAVE25 → was 108 − 25 = 83.00, now 75 × 1.08 = 81.00.

Tests: `python -m unittest discover -s tests` → 3/3 pass.
