# Ever wanted to access Native/GUI apps in your browser?

Github: https://lnkd.in/gb-DNv3T

I had a Python Tkinter app running in a K8s pod and needed to serve it in a browser with keyboard, mouse, and audio support. Xpra made it surprisingly straightforward.

Xpra is basically tmux for X11. It starts a virtual display, attaches your app to it, and serves a built-in HTML5 client over WebSocket. It does not stream a raw
framebuffer like VNC. Instead it tracks which parts of the window changed and only sends those rectangles, compressed as JPEG or PNG.

The whole thing starts with one command:

```
xpra start :100 \
 --bind-tcp=0.0.0.0:10000 \
 --html=on \
 --no-daemon \
 --exit-with-children \
 --start-child="python3 /app/wordle.py"
```

Audio works too. Xpra forwards PulseAudio over the same WebSocket connection using Opus. The HTML5 client renders onto a canvas element so you can embed it in an iframe or import xpra.js directly into your own page.

One nginx gotcha: you need the WebSocket upgrade headers in your ingress annotations. Without them the connection silently fails and you get no error.

Tech stack: Kubernetes, Xpra, Nginx, Python, Tkinter
