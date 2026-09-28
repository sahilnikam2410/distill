`forEach` doesn't wait for async callbacks. It calls each one, gets back a Promise, throws that Promise away, and moves on. So `return sum` runs right after the loop starts. At that point no `await price(id)` has finished, and `sum` is still `0`. The additions do happen later, after `total` has already returned.

**Fix 1: run the calls in parallel (usually what you want)**
```js
async function total(ids) {
  const prices = await Promise.all(ids.map(price));
  return prices.reduce((sum, p) => sum + p, 0);
}
```

**Fix 2: run the calls one at a time (if they must not overlap, e.g. rate limits)**
```js
async function total(ids) {
  let sum = 0;
  for (const id of ids) {
    sum += await price(id);
  }
  return sum;
}
```

`for...of` pauses at each `await`. `forEach`, `filter` and `reduce` never wait for a callback's Promise. `map` doesn't wait either, but it returns the Promises, so you can wrap it in `Promise.all` as in Fix 1.

Your version has a second problem too. `sum += await price(id)` reads `sum` before the `await` and writes it after. If several callbacks overlap, they can overwrite each other's additions. Both fixes above avoid this.
