Fixed. The bug was in `total()` in `cart.py`: it taxed the full subtotal before subtracting the coupon discount (`sub * 1.08 - disc`). The docstring and tests both say tax applies to the discounted amount, so any order with a coupon came out too high. For example, $100 with SAVE25 gave $108.00 - $25.00 = $83.00 instead of $81.00.

I changed it to discount first, then add tax:

```python
return money((sub - disc) * (1 + TAX_RATE))
```

Before the fix, 2 of the 3 tests failed (both coupon cases). Now all 3 pass (`python -m unittest discover -s tests`). Carts without a coupon give the same totals as before.
