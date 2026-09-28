Bug is `'127.0.0.1'`. Inside container, loopback mean container only. Docker port forward come in on container's eth0 interface, not loopback → nobody listening there → connection refused/reset.

Fix: bind all interfaces.

```js
app.listen(3000, '0.0.0.0');
// or just
app.listen(3000);
```

Better: make configurable.

```js
const HOST = process.env.HOST || '0.0.0.0';
const PORT = process.env.PORT || 3000;
app.listen(PORT, HOST);
```

Then rebuild + rerun:

```bash
docker build -t myapp .
docker run -p 3000:3000 myapp
```

Your `-p 3000:3000` fine. Keep it.

Check if still broken:
- `docker ps` → PORTS column should show `0.0.0.0:3000->3000/tcp`
- `docker logs <id>` → app started, no crash
- `curl localhost:3000` from host

Security note: `0.0.0.0` inside container is safe. Only ports you publish with `-p` get exposed. To keep it reachable only from your own machine, publish like this: `-p 127.0.0.1:3000:3000`.
