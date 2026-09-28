Fixed: tax was applied to the full subtotal instead of the discounted amount (`cart.py:20-21`).

```diff
-    taxed = sub * (1 + TAX_RATE)
-    return money(taxed - disc)
+    taxed = (sub - disc) * (1 + TAX_RATE)
+    return money(taxed)
```

Tests: 3/3 pass (`python -m unittest discover -s tests`).
