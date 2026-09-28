The problem is `app.listen(3000, '127.0.0.1')`.

Inside a container, `127.0.0.1` means the container's own loopback interface, not your computer's. When you run `-p 3000:3000`, Docker forwards traffic from your machine to the container's network interface (something like `172.17.0.x`). Because your app only listens on the container's loopback, that forwarded traffic never reaches it. The connection gets refused or reset even though the app is running.

**Fix:** have the app listen on all interfaces:

```js
app.listen(3000, '0.0.0.0');
// or just leave out the host. Node listens on all interfaces by default:
app.listen(3000);
```

If you want to keep `127.0.0.1` for local runs, make it configurable:

```js
const HOST = process.env.HOST || '127.0.0.1';
app.listen(3000, HOST);
```

Then pass `HOST=0.0.0.0` to the container, either with `ENV HOST=0.0.0.0` in the Dockerfile or `docker run -e HOST=0.0.0.0 -p 3000:3000 myapp`.

**After the change:**
1. Rebuild the image: `docker build -t myapp .`. Editing the source alone does nothing until you rebuild.
2. Run it: `docker run -p 3000:3000 myapp`
3. Open `http://localhost:3000`, or run `curl -v http://localhost:3000`.

**If it still doesn't work:**
- Run `docker ps`. The PORTS column should show `0.0.0.0:3000->3000/tcp`.
- Run `docker logs <container>` to confirm the app started and didn't crash.
- The container port (the second 3000 in `-p`) has to match the port the app listens on. Check whether something like `process.env.PORT` sets a different port.

Binding to `0.0.0.0` inside the container is safe. The only way in from outside is the port you publish with `-p`. To keep it reachable only from your own machine, publish it with `-p 127.0.0.1:3000:3000`.
