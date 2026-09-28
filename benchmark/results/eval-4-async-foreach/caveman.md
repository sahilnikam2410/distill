`forEach` doesn't wait for async callbacks. It starts every callback, ignores the promises they return, and exits right away. The `return sum` line runs while `sum` is still 0. Each `await price(id)` finishes later and adds to `sum`, but by then the function has already returned 0.

Fix, running the calls in parallel:

```js
async function total(ids) {
  const prices = await Promise.all(ids.map(id => price(id)));
  return prices.reduce((a, b) => a + b, 0);
}
```

Fix, running them one at a time:

```js
async function total(ids) {
  let sum = 0;
  for (const id of ids) {
    sum += await price(id);
  }
  return sum;
}
```

The parallel version is faster. Use the loop if the calls must run in order or you need to limit load.

Rule: never pass an async callback to `forEach`. Use `for...of` or `Promise.all` with `map`.
