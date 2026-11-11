#!/usr/bin/env python3
"""THE COMPANION's pictures: the companion's site photographed, screen by screen, for the book (C-321; the user,
2026-11-10: "built in a way as we evolve the app the manual can easily be update and rebuilt").

    python3 tools/companion_shots.py                 say which pictures the book asks for and which are missing
    python3 tools/companion_shots.py --write         take every one again (and the site exported again if the app changed)
    python3 tools/companion_shots.py --write --only today,talk     take only those
    python3 tools/companion_shots.py --write --keep-site           use the site already exported, even if older

Then `python3 tools/manual.py --book companion --write` prints the book with them.

WHAT IT DOES
  1. Exports the companion's site (companion/app, `expo export -p web`) into .theatre/companion-site/, when the app's
     sources are newer than the last export.
  2. Starts a THROWAWAY hub: the companion's server on a free port of its own, a database in a temporary folder, and a
     COPY of a theatre save (.theatre/rom/theatre_debug.sav, the DEBUG build's, never anyone's own) with its trainer
     renamed ROVER. No AI, no save watching. docs/manual-companion/shots.json may "seed" it first ({"post": path,
     "body": {...}}), so a page that shows the player's own things has something to show.
  3. Opens the site in headless Google Chrome (Playwright) with ?server= naming that hub, and for each shot in
     shots.json runs its steps -- {"tab": "LIBRARY"}, {"click": "exact text"}, {"wait": ms} -- scrolls its "scroll"
     text to the top if it has one, and takes "height" pixels of a 400-wide phone at 2x. Every request the page makes
     anywhere but the throwaway hub is refused: the pictures can never show, or touch, a real hub.
  4. Files each as docs/manual-companion/pictures/<name>.png and lists it in frames.json's "pictures", where
     tools/manual.py's {{pictures NAME}} finds it.

Needs: Node 24 (Homebrew's node@24), the companion's node_modules, Playwright for Python, and Google Chrome.
"""
import datetime, json, os, shutil, socket, struct, subprocess, sys, tempfile, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMPANION = os.path.join(ROOT, "companion")
BOOK = os.path.join(ROOT, "docs", "manual-companion")
SHOTS = os.path.join(BOOK, "shots.json")
FRAMES = os.path.join(BOOK, "frames.json")
PICS = os.path.join(BOOK, "pictures")
SITE = os.path.join(ROOT, ".theatre", "companion-site")
SAVE = os.path.join(ROOT, ".theatre", "rom", "theatre_debug.sav")
NODE = "/opt/homebrew/opt/node@24/bin"
NAME, RIVAL = "ROVER", "KIT"                     # the trainer and rival the pictures show


def newest(folder, exts=(".ts", ".tsx", ".json", ".png", ".ttf")):
    t = 0.0
    for d, dirs, fs in os.walk(folder):
        dirs[:] = [x for x in dirs if x not in ("node_modules", "ios", "android", "dist", ".expo")]
        for f in fs:
            if f.endswith(exts):
                t = max(t, os.path.getmtime(os.path.join(d, f)))
    return t


def export_site(keep):
    index = os.path.join(SITE, "index.html")
    if os.path.exists(index) and (keep or os.path.getmtime(index) >= newest(os.path.join(COMPANION, "app"))):
        print("  the site: .theatre/companion-site/ is current")
        return
    print("  the site: exporting it again (a minute or two)")
    shutil.rmtree(SITE, ignore_errors=True)
    env = dict(os.environ, PATH=NODE + ":" + os.environ["PATH"], EXPO_PUBLIC_DAEMONS_SERVER="origin")
    r = subprocess.run(["npx", "expo", "export", "-p", "web", "--output-dir", SITE], cwd=os.path.join(COMPANION, "app"),
                       env=env, capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(index):
        sys.stderr.write(r.stdout[-2000:] + r.stderr[-2000:])
        raise SystemExit("companion_shots: the site did not export")


def sizes():
    """Each section's checksummed length, as the companion reads the save (its data/save_layout.json)."""
    l = json.load(open(os.path.join(COMPANION, "server", "data", "save_layout.json"), encoding="utf-8"))
    d = l["sector_data_size"]
    return {0: l["saveblock2_size"], **{i: min(d, l["saveblock1_size"] - (i - 1) * d) for i in range(1, 5)}}


def renamed(src, dest, name, rival):
    """A copy of a FireRed-layout save, its trainer and rival renamed: the trainer in section 0's first 8 bytes, the
    rival in SaveBlock1's rivalName (profile_layout.json; in section 4), each section's checksum redone."""
    SIZES = sizes()
    l = json.load(open(os.path.join(COMPANION, "server", "data", "save_layout.json"), encoding="utf-8"))
    SECTOR = l["sector_data_size"]
    RIVAL_AT = json.load(open(os.path.join(COMPANION, "server", "data", "profile_layout.json"), encoding="utf-8"))["sb1"]["rival_name"]
    assert 3 * SECTOR <= RIVAL_AT < 4 * SECTOR, "the rival's name is not in section 4"
    b = bytearray(open(src, "rb").read())
    enc = lambda n: bytes(0xBB + ord(c) - 65 for c in n.upper()) + b"\xff" * (8 - len(n))
    for sec in range(len(b) // 0x1000):
        o = sec * 0x1000
        sid = struct.unpack_from("<H", b, o + 0xFF4)[0]
        if struct.unpack_from("<I", b, o + 0xFF8)[0] != 0x08012025 or sid not in (0, 4):
            continue
        if sid == 0:
            b[o:o + 8] = enc(name)
        else:
            at = RIVAL_AT - 3 * SECTOR
            b[o + at:o + at + 7] = enc(rival)[:7]
        s = sum(struct.unpack_from("<%dI" % (SIZES[sid] // 4), b, o)) & 0xFFFFFFFF
        struct.pack_into("<H", b, o + 0xFF6, ((s >> 16) + s) & 0xFFFF)
    open(dest, "wb").write(b)


def free_port():
    for port in range(4790, 4800):
        with socket.socket() as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise SystemExit("companion_shots: no free port between 4790 and 4799")


def start_hub(tmp):
    port = free_port()
    save = os.path.join(tmp, "demo.sav")
    renamed(SAVE, save, NAME, RIVAL)
    cfg = {"port": port, "host": "127.0.0.1", "database": os.path.join(tmp, "demo.sqlite"), "edition": "CONTENT",
           "savePath": save, "siteDir": SITE, "ai": {"enabled": False}, "talk": {"url": None}, "watchSave": False}
    path = os.path.join(tmp, "config.json")
    json.dump(cfg, open(path, "w"))
    env = dict(os.environ, PATH=NODE + ":" + os.environ["PATH"], COMPANION_CONFIG=path)
    log = open(os.path.join(tmp, "server.log"), "w")
    proc = subprocess.Popen(["npx", "tsx", "src/main.ts"], cwd=os.path.join(COMPANION, "server"), env=env,
                            stdout=log, stderr=subprocess.STDOUT, start_new_session=True)   # its own group: npx's node goes with it
    url = "http://127.0.0.1:%d" % port
    for _ in range(60):
        try:
            urllib.request.urlopen(url + "/api/profile", timeout=2).read()
            return proc, url
        except Exception:
            if proc.poll() is not None:
                break
            time.sleep(0.5)
    stop(proc)
    raise SystemExit("companion_shots: the throwaway hub did not start (%s)" % os.path.join(tmp, "server.log"))


def stop(proc):
    import signal
    try:
        os.killpg(proc.pid, signal.SIGTERM)
        proc.wait(10)
    except (ProcessLookupError, subprocess.TimeoutExpired):
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass


def seed(url, steps):
    for s in steps:
        req = urllib.request.Request(url + s["post"], data=json.dumps(s.get("body", {})).encode(),
                                     headers={"content-type": "application/json"}, method="POST")
        try:
            urllib.request.urlopen(req, timeout=10).read()
        except Exception as e:
            print("  !! seed %s: %s" % (s["post"], e))


def take(url, shots, view, only):
    from playwright.sync_api import sync_playwright
    host = url.split("//")[1]
    taken = {}
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True)
        for name, sh in shots.items():
            if only and name not in only:
                continue
            w, h = sh.get("viewport", view)
            pg = b.new_page(viewport={"width": w, "height": max(h, sh.get("height", h))}, device_scale_factor=2)
            pg.route("**/*", lambda r: r.continue_() if r.request.url.split("/")[2] == host
                     or r.request.url.startswith("data:") else r.abort())
            pg.goto(url + "/?server=" + url, wait_until="networkidle")
            pg.wait_for_timeout(1200)
            try:
                for st in sh.get("steps", []):
                    if "tab" in st:
                        pg.get_by_text(st["tab"], exact=True).first.click()
                        pg.wait_for_timeout(1500)
                    elif "click" in st:
                        pg.get_by_text(st["click"], exact=True).first.click(timeout=5000)
                        pg.wait_for_timeout(900)
                    elif "wait" in st:
                        pg.wait_for_timeout(st["wait"])
                top = 0
                if sh.get("scroll"):
                    el = pg.get_by_text(sh["scroll"], exact=True).first
                    el.scroll_into_view_if_needed()
                    top = max(0, el.bounding_box()["y"] - 16)
                pg.wait_for_timeout(800)
                out = os.path.join(PICS, name + ".png")
                height = sh.get("height", h)
                page = pg.evaluate("document.documentElement.scrollHeight")
                top = max(0, min(top, page - height))     # a picture near the foot of the page ends at the foot
                pg.screenshot(path=out, clip={"x": 0, "y": top, "width": w, "height": height}, full_page=True)
                taken[name] = sh.get("about", "")
                print("  took %s" % name)
            except Exception as e:
                print("  !! %s: %s" % (name, str(e).splitlines()[0][:160]))
            pg.close()
        b.close()
    return taken


def main():
    args = sys.argv[1:]
    write = "--write" in args
    only = set(args[args.index("--only") + 1].split(",")) if "--only" in args else None
    if not os.path.exists(SHOTS):
        print("  no docs/manual-companion/shots.json: no pictures asked for")
        return 0
    spec = json.load(open(SHOTS, encoding="utf-8"))
    shots, view = spec["shots"], spec.get("viewport", [400, 860])
    missing = [n for n in shots if not os.path.exists(os.path.join(PICS, n + ".png"))]
    print("  %d pictures asked for; %d not yet taken%s" % (len(shots), len(missing),
                                                         (": " + ", ".join(missing)) if missing else ""))
    if not write:
        return 0
    os.makedirs(PICS, exist_ok=True)
    export_site("--keep-site" in args)
    with tempfile.TemporaryDirectory(prefix="daemons-shots-") as tmp:
        proc, url = start_hub(tmp)
        try:
            seed(url, spec.get("seed", []))
            taken = take(url, shots, view, only)
        finally:
            stop(proc)
    frames = json.load(open(FRAMES, encoding="utf-8"))
    pics = frames.setdefault("pictures", {})
    today = datetime.date.today().isoformat()
    for name, about in taken.items():
        pics[name] = {"from": "docs/manual-companion/pictures/%s.png" % name, "taken": today, "shows": about}
    for name in list(pics):                      # a shot no longer asked for is no longer listed
        if name not in shots:
            del pics[name]
    tmpf = FRAMES + ".tmp"
    open(tmpf, "w", encoding="utf-8").write(json.dumps(frames, indent=1, ensure_ascii=False) + "\n")
    os.replace(tmpf, FRAMES)
    print("  %d taken; frames.json lists %d" % (len(taken), len(pics)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
