Cause: `127.0.0.1` inside the container is the container's own loopback. Traffic forwarded by `-p 3000:3000` comes in on the container's network interface, not loopback, so nothing is listening to receive it.

Fix: bind to all interfaces.
```js
app.listen(3000, '0.0.0.0')
```
You can also leave the host out (`app.listen(3000)`). Then rebuild and run it again:
```bash
docker build -t myapp . && docker run -p 3000:3000 myapp
```

Verify: `curl localhost:3000` from the host.

If you don't want other machines to reach the app, restrict the host side instead: `-p 127.0.0.1:3000:3000`.
