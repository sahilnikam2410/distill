Cause: `forEach` doesn't wait for async callbacks. It starts each one and returns straight away, so `return sum` runs before any `await price(id)` finishes. At that point `sum` is still `0`. The additions happen later, after the value has already been returned.

Fix (parallel):
```js
async function total(ids) {
  const prices = await Promise.all(ids.map(price));
  return prices.reduce((a, b) => a + b, 0);
}
```

For sequential calls (e.g. to respect rate limits), use `for (const id of ids) sum += await price(id);` instead.
