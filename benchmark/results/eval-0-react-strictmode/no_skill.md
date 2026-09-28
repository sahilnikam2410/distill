This is expected, and it's caused by **React 18's `<StrictMode>`**, not by Vite or a bug in your code.

## Why it happens

Open `src/main.jsx` (or `main.tsx`). The Vite React template wraps your app like this:

```jsx
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
```

In **development only**, React 18's StrictMode deliberately mounts each component, unmounts it, and mounts it again:

1. mount → effect runs
2. simulated unmount → cleanup runs
3. mount again → effect runs again

React does this to catch effects that don't clean up after themselves (leaked subscriptions, duplicate listeners, timers that keep running, and so on). Later React features like Fast Refresh, `<Activity>`/offscreen and back-navigation can unmount and remount components for real, so your effects need to survive that.

**Production builds (`vite build`) don't do this.** There your effect runs once.

## How to "stop" it

### Option 1 (recommended): write a cleanup so running twice doesn't matter

If you get the same result whether the effect runs once or twice, you're done. Some common cases:

**Event listeners / subscriptions**
```jsx
useEffect(() => {
  const onResize = () => setWidth(window.innerWidth);
  window.addEventListener('resize', onResize);
  return () => window.removeEventListener('resize', onResize);
}, []);
```

**Timers**
```jsx
useEffect(() => {
  const id = setInterval(tick, 1000);
  return () => clearInterval(id);
}, []);
```

**Data fetching**: cancel the stale request or ignore its result
```jsx
useEffect(() => {
  const controller = new AbortController();

  fetch('/api/data', { signal: controller.signal })
    .then(res => res.json())
    .then(setData)
    .catch(err => {
      if (err.name !== 'AbortError') console.error(err);
    });

  return () => controller.abort();
}, []);
```

You'll still see two requests in the Network tab in dev (the first one shows as cancelled). That's fine.

**Connections (WebSocket, chat, etc.)**
```jsx
useEffect(() => {
  const ws = new WebSocket(url);
  return () => ws.close();
}, [url]);
```

### Option 2: move the logic out of the effect

- **Something that should run once per app load** (analytics init, reading a token, etc.): put it at module level, outside the component, or guard it:
  ```jsx
  let didInit = false;

  function App() {
    useEffect(() => {
      if (didInit) return;
      didInit = true;
      initAnalytics();
    }, []);
  }
  ```
- **Something caused by a user action** (like a POST when a button is clicked): do it in the event handler, not in an effect.
- **Data fetching in general**: a library like TanStack Query or SWR handles deduplication and caching for you.

### Option 3: remove StrictMode (not recommended)

```jsx
ReactDOM.createRoot(document.getElementById('root')).render(<App />)
```

This stops the double run, but you also lose the dev-time checks that find real bugs. Hiding the symptom usually means the missing-cleanup bug appears later, for example as duplicate listeners after a route change.

### What doesn't work: a `useRef` guard

```jsx
const ran = useRef(false);
useEffect(() => {
  if (ran.current) return;
  ran.current = true;
  // ...
}, []);
```

People often suggest this, but it only hides the problem. It also skips your cleanup logic, so it can break when a real remount happens.

## TL;DR

The double run is StrictMode testing your effect, and it only happens in dev. Don't try to prevent it. Return a cleanup function from the effect so running it twice is harmless. In production it runs once.
