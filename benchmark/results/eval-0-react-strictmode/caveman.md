Cause: `<React.StrictMode>` in `main.jsx`. React 18 dev mode mount → unmount → remount every component on purpose. Effect run, cleanup run, effect run again. Test that effect survive remount. Dev only. Production build (`vite build`) run once.

Not bug. Usually not need stop. Fix effect instead: add cleanup.

```jsx
useEffect(() => {
  const controller = new AbortController();

  fetch('/api/data', { signal: controller.signal })
    .then(res => res.json())
    .then(setData)
    .catch(err => {
      if (err.name !== 'AbortError') throw err;
    });

  return () => controller.abort(); // cleanup kill first run
}, []);
```

Same idea for other side effects:
- Subscription / event listener → unsubscribe / `removeEventListener` in cleanup.
- `setInterval` / `setTimeout` → `clearInterval` / `clearTimeout` in cleanup.
- Socket → `close()` in cleanup.

Double run harmless after cleanup. Correct cleanup also fix real bugs (fast navigation, unmount mid-fetch).

**Want truly once?** (analytics ping, one-time init) Use ref guard:

```jsx
const didRun = useRef(false);

useEffect(() => {
  if (didRun.current) return;
  didRun.current = true;
  sendAnalytics();
}, []);
```

Or move code outside component (module top level) — run once per app load.

**Nuke option:** remove StrictMode in `src/main.jsx`:

```jsx
// before
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// after
ReactDOM.createRoot(document.getElementById('root')).render(<App />);
```

Works, but lose StrictMode warnings (missing cleanup, deprecated APIs). Not recommended — fix cleanup instead.

For data fetching, TanStack Query / SWR handle dedupe + cancel for you.
