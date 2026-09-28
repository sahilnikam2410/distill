Cause: `<StrictMode>` in `main.jsx`. In dev only, React 18 mounts → unmounts → remounts every component to expose effects that lack cleanup. Production builds run the effect once.

Fix: don't stop it. Give the effect a cleanup, so the second run is harmless:

```jsx
useEffect(() => {
  const controller = new AbortController();
  fetch('/api/data', { signal: controller.signal })
    .then(r => r.json())
    .then(setData)
    .catch(e => { if (e.name !== 'AbortError') throw e; });
  return () => controller.abort();
}, []);
```

Same pattern for subscriptions, timers and listeners: `return () => unsubscribe()` / `clearInterval(id)` / `removeEventListener(...)`.

Removing `<StrictMode>` from `main.jsx` also stops the double run. Not recommended: it hides the bugs StrictMode is meant to catch. A `useRef` "already ran" guard has the same problem.

Verify: `npm run build && npm run preview` → effect runs once.
