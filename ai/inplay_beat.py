#!/usr/bin/env python3
# BRAIN: none -- a presence beat to the hub: the run's save and screen when changed; exits when the hub says end
"""C-496: an AI run-through, reported to the companion's hub as a game in play (companion C-478's API).

Every BEAT seconds: a heartbeat to the hub with the run's save when it has changed, and the emulator's screen when it
has changed (the bridge rewrites it at every turn of the agent). When the hub answers {"end": true} -- END THIS
RUN-THROUGH, pressed in THE ENGINE ROOM's IN PLAY -- it says goodbye and exits 3, and ai/airun.sh stops the run.
Standard library only: it runs on any Python the machine has.

    python3 ai/inplay_beat.py --hub http://daemons-hearth:4730 --key KEY --id ai-... --save FILE.sav --frame FILE.png
"""
import argparse, base64, hashlib, json, os, signal, sys, time, urllib.request, urllib.error

BEAT = 5


def post(hub, key, path, body, ctype="application/json"):
    data = json.dumps(body).encode() if ctype == "application/json" else body
    req = urllib.request.Request(hub + path, data=data, method="POST", headers={"content-type": ctype})
    if key:
        req.add_header("authorization", f"Bearer {key}")
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read() or b"{}")


def sha(path):
    try:
        with open(path, "rb") as f:
            b = f.read()
        return hashlib.sha1(b).hexdigest(), b
    except OSError:
        return None, None


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--hub", required=True); a.add_argument("--key", default="")
    a.add_argument("--id", required=True); a.add_argument("--save"); a.add_argument("--frame")
    a.add_argument("--device", default="this Mac"); a.add_argument("--user", default="the AI")
    a.add_argument("--edition", default="CONTENT")
    o = a.parse_args()
    hub = o.hub.rstrip("/")
    last_save = last_frame = None

    def bye(*_):
        try:
            post(hub, o.key, f"/api/games/{o.id}/over", {})
        except Exception:
            pass
        sys.exit(0)
    signal.signal(signal.SIGTERM, bye)
    signal.signal(signal.SIGINT, bye)

    print(f"in play as {o.id} at {hub}", flush=True)
    while True:
        try:
            body = {"id": o.id, "source": "ai", "device": o.device, "user": o.user, "edition": o.edition}
            h, b = sha(o.save) if o.save else (None, None)
            if b and len(b) >= 0x10000 and h != last_save:
                body["save"] = base64.b64encode(b).decode()
            r = post(hub, o.key, "/api/games/beat", body)
            if "save" in body:
                last_save = h
            fh, fb = sha(o.frame) if o.frame else (None, None)
            if fb and fh != last_frame and len(fb) <= 400 * 1024:
                ctype = "image/png" if o.frame.lower().endswith(".png") else "image/jpeg"
                post(hub, o.key, f"/api/games/{o.id}/frame", fb, ctype)
                last_frame = fh
            if r.get("end"):
                print("the hub asked this run-through to end", flush=True)
                try:
                    post(hub, o.key, f"/api/games/{o.id}/over", {})
                except Exception:
                    pass
                sys.exit(3)
        except urllib.error.HTTPError as e:
            print(f"the hub said {e.code}: {e.read()[:200]!r}", flush=True)
            if e.code in (401, 403):
                sys.exit(2)
        except Exception as e:   # the hub restarting: keep beating
            print(f"no answer from the hub ({e}); trying again", flush=True)
        time.sleep(BEAT)


if __name__ == "__main__":
    main()
