"""T-452 roll-out (the user, 2026-10-24): every daemon in batches of about 20, a sheet each, by round two's method.

    batch.py STAGE --dir=c --seed=4700 --prefix=t452c [NAME ...]      or  --next=20 in place of the names

STAGE  gen      a front by image-to-image from today's front at 0.6 and 0.66, a back the same from today's back,
                two drawn icons (busts). Every draft keeps spriteforge's seed record beside it.
       lo       two more fronts nearer today's (i2i 0.5 and 0.55), where 0.6 lost the props
       icon2    two more icons from subjects.py's icon2 wording (the whole shape), where the bust became a face
       t2i      two text-to-image fronts, for one whose props i2i lost (only kept where the props survive)
       contact  one candidates sheet per daemon in the scratchpad, to choose from
       reduce   reduce2.py on the chosen drafts (DIR/choose.json overrides the defaults), into DIR/picks.json
       sheets   the overview (today | new, 1x and 2x, accent %), the icons, two battle mocks, the failures
       all      gen, reduce, sheets
       charm    batch 1 redone for charm (the user, 2026-10-25: "more charm, accept drift"; --dir=d --seed=4800):
                two text-to-image chibi fronts (SEED+1, +2; the pilot's recipe, the ONE key prop from subjects.CHARM
                named first), two fronts by image-to-image from today's at 0.8 and 0.85 (SEED+21, +22), two backs
                from today's back at 0.66 and 0.75 (SEED+31, +32), two chibi icons (SEED+41, +42)
       charmlo  for one whose key prop the charm stage lost: two fronts from today's at 0.72 and 0.76 (SEED+23, +24),
                nearer today's than charm's 0.8, still well past batch 1's 0.6; and, where subjects.CHARM has front2,
                two text-to-image fronts from that second wording (SEED+3, +4)
       charmback  two more backs, image-to-image from the CHOSEN new front (choose.json) at 0.75 and 0.85, rear-view
                prompt (SEED+51, +52): the model turning the new chibi rather than repainting today's back

--next=N takes the first N daemons in INDEX order that no earlier round or batch has drawn (b/picks2.json and every
*/picks.json beside DIR), skipping the HANDSHAKE line (261-263, drawn by T-450). Writes only under
gfx/drafts/t452/DIR and the scratchpad; never the engine.

Defaults, before choose.json: front = i2i 0.6, back = i2i 0.6, icon = the first seed. choose.json is
    {"name": {"front": FILE, "back": FILE, "icon": FILE | "derived", "note": "...", "failed": "why, if it did",
              "key": true (clean the front on a key ground), "key-back": true, "box-front": "x0,y0,x1,y1", "box-back": ...}}"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from subjects import S, CHARM, CHARM2
R = "/Users/christopherhicks/Projects/DAEMONS"
#  T452_ROOT: work outside the tree (a release once needed it clean for half an hour); copy the files in afterwards
T = os.environ.get("T452_ROOT", R + "/gfx/drafts/t452")
PY = os.path.expanduser("~/.pyenv/versions/3.12.2/bin/python3")
SP = "/private/tmp/claude-502/-Users-christopherhicks-Projects-DAEMONS/d99297fc-c29c-48ac-bea7-477ee8d1422e/scratchpad/"
os.chdir(R)
opt = {a.split("=", 1)[0][2:]: a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--") and "=" in a}
args = [a for a in sys.argv[1:] if not a.startswith("--")]
stage, names = args[0], args[1:]
DIRN = opt.get("dir", "c"); D = f"{T}/{DIRN}"; REL = f"gfx/drafts/t452/{DIRN}" if "T452_ROOT" not in os.environ else D
SEED = int(opt.get("seed", 4700)); PREFIX = opt.get("prefix", "t452" + DIRN); LABEL = opt.get("label", DIRN.upper())
os.makedirs(D + "/src", exist_ok=True)
SPEC = json.load(open(R + "/companion/server/data/species.json"))
BYNAME = {v["name"].lower(): v for v in SPEC.values()}

def drawn_already():
    done = set(json.load(open(T + "/b/picks2.json"))) - {"_battles"}
    for d in os.listdir(T):
        p = f"{T}/{d}/picks.json"
        if d != DIRN and os.path.exists(p): done |= set(json.load(open(p))) - {"_battles"}
    return done
if "next" in opt:
    done = drawn_already(); names = []
    for k, v in SPEC.items():
        if int(k) in (261, 262, 263) or v["name"].lower() in done: continue
        names.append(v["name"].lower())
        if len(names) == int(opt["next"]): break
missing = [n for n in names if n not in S]
if missing and stage in ("gen", "t2i", "all"): raise SystemExit("no subject in subjects.py for: " + ", ".join(missing))

#  round two's prompt pieces (gen2.py), unchanged
HEAD = "pure white background, pixel art game sprite of a single cute creature, "
G = ("full body, chibi proportions, big round head, large expressive eyes, soft shading, mostly greyscale, "
     "medium grey body with light grey highlights and dark grey shading, only small touches of colour, "
     "clean black outline, isolated on white, centered, large in the frame, no shadow, no text")
GB = ("full body, chibi proportions, big round head seen from behind, soft shading, mostly greyscale, "
      "medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, "
      "centered, large in the frame, no shadow, no text")
N = ("photorealistic, 3d render, colorful, rainbow, colored background, grey background, dark background, scenery, "
     "floor, ground, text, letters, watermark, multiple creatures, two creatures, duplicate, human, person, cropped, "
     "blurry, drop shadow, border, white body, pale body")
NB = "face, eyes, nose, mouth, beak tip, whiskers, front view, facing the viewer, side view, profile, " + N
GI = ("bust portrait, head and shoulders only, big round head filling the frame, very simple, large shapes, few details, "
      "thick black outline, flat shading, mostly greyscale, medium grey with light grey highlights, isolated on white, "
      "centered, no text")

def idle():
    """the sprite server is SHARED (batch 5, 2026-10-27): wait for its queue to empty before submitting, politely"""
    import urllib.request, time, random
    for _ in range(240):
        try:
            q = json.loads(urllib.request.urlopen("http://roverbyteseer:8008/queue", timeout=15).read())
            if len(q["queue_pending"]) + len(q["queue_running"]) == 0: return   # batch 9: an idle queue before each job (chain8's rule)
        except Exception as e:
            print("queue?", e, flush=True)
        time.sleep(8 + random.random() * 6)

def run(a):
    out = a[a.index("--out") + 1]
    for k in range(30):   # batch 11: the network may drop for a while (laptop moving, hub updating) -- retry every 60 s for up to 30 min
        if os.path.exists(out + ".png"): return
        idle()
        t = subprocess.run([PY, "tools/spriteforge.py"] + a, capture_output=True, text=True)
        print(out, t.stdout.strip()[-60:], t.stderr.strip()[-300:], flush=True)
        if not os.path.exists(out + ".png"):
            import time; time.sleep(60)

def src512(n, kind):
    dst = f"{D}/src/{n}_{kind}_512.png"
    im = Image.open(f"{R}/{BYNAME[n]['art'][kind]}").convert("RGBA")
    if im.width != 64: im = im.resize((64, 64), Image.LANCZOS)
    a = np.array(im)
    if (a[..., 3] < 128).mean() < 0.01:   # batch 13: THE NEXUS's painted art is opaque on black -- flood the black ground from the edges to transparent
        from collections import deque
        dk = a[..., :3].max(-1) < 40; seen = np.zeros(dk.shape, bool); q = deque()
        for y in range(64):
            for x in range(64):
                if (y in (0, 63) or x in (0, 63)) and dk[y, x]: seen[y, x] = True; q.append((y, x))
        while q:
            y, x = q.popleft()
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                p_, r_ = y + dy, x + dx
                if 0 <= p_ < 64 and 0 <= r_ < 64 and dk[p_, r_] and not seen[p_, r_]: seen[p_, r_] = True; q.append((p_, r_))
        a[seen, 3] = 0; im = Image.fromarray(a)
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255)); bg.alpha_composite(im)
    bg.convert("RGB").resize((512, 512), Image.NEAREST).save(dst)
    return dst

def gen(n):
    s = S[n]
    fneg = "rear view, " + s["neg"] + ", " + N; bneg = s["neg"] + ", " + NB
    for k, (dn) in enumerate((0.6, 0.66)):
        run(["i2i", "--seed", str(SEED + 11 + k), "--denoise", str(dn), "--image", src512(n, "front"),
             "--out", f"{REL}/{n}_front_i2i_{SEED + 11 + k}", "--prompt", HEAD + s["front"] + ", " + G, "--negative", fneg])
    for k, dn in enumerate((0.6, 0.66)):
        run(["i2i", "--seed", str(SEED + 11 + k), "--denoise", str(dn), "--image", src512(n, "back"),
             "--out", f"{REL}/{n}_back_i2i_{SEED + 11 + k}", "--prompt", HEAD + s["back"] + ", " + GB, "--negative", bneg])
    for k in range(2):
        run(["t2i", "--size", "512x512", "--seed", str(SEED + 41 + k), "--out", f"{REL}/{n}_icon_{SEED + 41 + k}",
             "--prompt", HEAD + s["icon"] + ", " + GI, "--negative", "full body, legs, feet, " + s["neg"] + ", " + N])

#  the charm recipe: the pilot's (round one, *_4521) and T-450's -- the key prop first, then a chibi subject
GC = "facing left three-quarter view, " + G
GIC = ("chibi, big round head, large expressive eyes, the whole creature filling the frame, very simple, large shapes, "
       "few details, thick black outline, soft shading, mostly greyscale, medium grey with light grey highlights, "
       "isolated on white, centered, no text, no frame, no border")
GBC = "rear view, seen from behind, facing away from the viewer, " + GB

def charm(n, lean=False):
    s, c = S[n], CHARM2.get(n, CHARM[n])
    fp = HEAD + c["key"] + ", " + c["front"] + ", " + GC; fneg = "rear view, " + s["neg"] + ", " + N
    for k in range(2):
        run(["t2i", "--size", "512x512", "--seed", str(SEED + 1 + k), "--out", f"{REL}/{n}_front_{SEED + 1 + k}",
             "--prompt", fp, "--negative", fneg])
    for k, dn in enumerate((0.8, 0.85)):
        run(["i2i", "--seed", str(SEED + 21 + k), "--denoise", str(dn), "--image", src512(n, "front"),
             "--out", f"{REL}/{n}_front_i2i_{SEED + 21 + k}", "--prompt", fp, "--negative", fneg])
    bp = HEAD + c["key"] + ", " + s["back"] + ", " + GBC; bneg = "girl, long hair, hair, " + s["neg"] + ", " + NB
    for k, dn in enumerate((0.66,) if lean else (0.66, 0.75)):
        run(["i2i", "--seed", str(SEED + 31 + k), "--denoise", str(dn), "--image", src512(n, "back"),
             "--out", f"{REL}/{n}_back_i2i_{SEED + 31 + k}", "--prompt", bp, "--negative", bneg])
    for k in range(1 if lean else 2):
        run(["t2i", "--size", "512x512", "--seed", str(SEED + 41 + k), "--out", f"{REL}/{n}_icon_{SEED + 41 + k}",
             "--prompt", HEAD + c["key"] + ", " + c["icon"] + ", " + GIC,
             "--negative", "sprite sheet, grid of icons, tiled pattern, repeated, many copies, four creatures, human, girl, "
             "boy, person, frame, border, " + s["neg"] + ", " + N])

def charmlo(n):
    s, c = S[n], CHARM2.get(n, CHARM[n]); fneg = "rear view, " + s["neg"] + ", " + N
    fp = HEAD + c["key"] + ", " + c["front"] + ", " + GC
    for k, dn in enumerate((0.72, 0.76)):
        run(["i2i", "--seed", str(SEED + 23 + k), "--denoise", str(dn), "--image", src512(n, "front"),
             "--out", f"{REL}/{n}_front_i2i_{SEED + 23 + k}", "--prompt", fp, "--negative", fneg])
    if "front2" in c:
        for k in range(2):
            run(["t2i", "--size", "512x512", "--seed", str(SEED + 3 + k), "--out", f"{REL}/{n}_front_{SEED + 3 + k}",
                 "--prompt", HEAD + c["front2"] + ", " + GC, "--negative", fneg + ", " + c.get("neg2", "")])

def charmback(n):
    """the chosen new front, turned: image-to-image from it with the rear-view prompt, at 0.75 and 0.85"""
    s, c = S[n], CHARM2.get(n, CHARM[n])
    fr = choose().get(n, {}).get("front")
    if not fr: print(n, "charmback: no front chosen in choose.json"); return
    a = Image.open(f"{D}/{fr}").convert("RGB"); src = f"{D}/src/{n}_newfront_512.png"; a.save(src)
    bp = HEAD + c["key"] + ", " + s["back"] + ", " + GBC; bneg = "girl, long hair, hair, " + s["neg"] + ", " + NB
    for k, dn in enumerate((0.75, 0.85)):
        run(["i2i", "--seed", str(SEED + 51 + k), "--denoise", str(dn), "--image", src,
             "--out", f"{REL}/{n}_back_fromfront_{SEED + 51 + k}", "--prompt", bp, "--negative", bneg])

def lo(n):
    """nearer today's front, for one whose props 0.6 lost: 0.5 and 0.55"""
    s = S[n]
    for k, dn in enumerate((0.5, 0.55)):
        run(["i2i", "--seed", str(SEED + 13 + k), "--denoise", str(dn), "--image", src512(n, "front"),
             "--out", f"{REL}/{n}_front_i2i_{SEED + 13 + k}", "--prompt", HEAD + s["front"] + ", " + G,
             "--negative", "rear view, " + s["neg"] + ", " + N])

def t2i(n):
    s = S[n]
    for k in range(2):
        run(["t2i", "--size", "512x512", "--seed", str(SEED + 1 + k), "--out", f"{REL}/{n}_front_{SEED + 1 + k}",
             "--prompt", HEAD + s["front"] + ", " + G, "--negative", "rear view, " + s["neg"] + ", " + N])

GI2 = ("game icon, the whole creature filling the frame, very simple, large shapes, few details, thick black outline, "
       "flat shading, mostly greyscale, medium grey with light grey highlights, isolated on white, centered, no text, "
       "no frame, no border")

def icon2(n):
    s = S[n]
    if "icon2" not in s: return
    for k in range(2):
        run(["t2i", "--size", "512x512", "--seed", str(SEED + 43 + k), "--out", f"{REL}/{n}_icon_{SEED + 43 + k}",
             "--prompt", HEAD + s["icon2"] + ", " + GI2,
             "--negative", "human, girl, boy, person, big face, frame, border, " + s["neg"] + ", " + N])

def cands(n):
    return sorted(f for f in os.listdir(D) if f.startswith(n + "_") and f.endswith(".png"))

try:
    F = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 16); FS = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 12)
except Exception:
    F = FS = ImageFont.load_default()
PAPER = (236, 234, 226); INKC = (30, 30, 34); GAMEBG = (205, 205, 172); PARTY = (98, 156, 131); RED = (170, 40, 40)

def today(n, k="front"):
    im = Image.open(f"{R}/{BYNAME[n]['art'][k]}").convert("RGBA")
    return im if im.width == 64 else im.resize((64, 64), Image.LANCZOS)
def sprite(path, pal_from=None):
    im = Image.open(path)
    if pal_from: im.putpalette(Image.open(pal_from).getpalette())
    a = im.convert("RGBA"); px = np.array(im); al = np.array(a); al[px == 0, 3] = 0
    return Image.fromarray(al)
def on(im, bg, scale=1):
    b = Image.new("RGBA", im.size, bg + (255,)); b.alpha_composite(im)
    return b.convert("RGB").resize((im.width * scale, im.height * scale), Image.NEAREST)

def contact(n):
    fs = cands(n); W = 20 + len(fs) * 212 + 2 * 212
    s = Image.new("RGB", (W, 270), PAPER); d = ImageDraw.Draw(s)
    d.text((20, 6), f"{n.upper()} -- {S[n]['props']}", fill=INKC, font=FS)
    s.paste(on(today(n), GAMEBG, 3), (20, 30)); s.paste(on(today(n, "back"), GAMEBG, 3), (232, 30))
    for i, f in enumerate(fs):
        x = 20 + (i + 2) * 212
        s.paste(Image.open(f"{D}/{f}").convert("RGB").resize((192, 192)), (x, 30))
        d.text((x, 228), f.replace(n + "_", "")[:-4], fill=INKC, font=FS)
    os.makedirs(T + "/cand", exist_ok=True); s.save(T + f"/cand/{PREFIX}_cand_{n}.png")

def choose():
    p = f"{D}/choose.json"
    return json.load(open(p)) if os.path.exists(p) else {}

def keyed(f):
    """the draft on a chroma-key ground: cleandraft wears away a dark mass that touches no light body, which took
    CRAWLER's dark segments and left only its head; on a key ground (bg spread >= 80) that step is skipped.
    The white ground is flooded from the edges, so white inside the creature stays."""
    from collections import deque
    a = np.array(Image.open(f"{D}/{f}").convert("RGB")).astype(int); h, w = a.shape[:2]
    white = (a.min(2) > 225) & (a.max(2) - a.min(2) < 20)
    seen = np.zeros((h, w), bool); q = deque()
    for y in range(h):
        for x in (0, w - 1):
            if white[y, x]: seen[y, x] = True; q.append((y, x))
    for x in range(w):
        for y in (0, h - 1):
            if white[y, x] and not seen[y, x]: seen[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p, r = y + dy, x + dx
            if 0 <= p < h and 0 <= r < w and white[p, r] and not seen[p, r]: seen[p, r] = True; q.append((p, r))
    a[seen] = (0, 200, 0)
    out = "src/" + os.path.basename(f)[:-4] + "_key.png"
    Image.fromarray(a.astype(np.uint8)).save(f"{D}/{out}")
    return out

def unframe(f):
    """a drawn icon the model put in a rounded box (seed 4742 did it nine times in batch 1): the box is a dark line
    running most of the way across, near the edge; everything from it outward is painted white, in place on the
    8px grid (no resize). Returns f itself when there is no box."""
    a = np.array(Image.open(f"{D}/{f}").convert("RGB")).astype(int); h, w = a.shape[:2]
    dark = (a[..., 0] * 299 + a[..., 1] * 587 + a[..., 2] * 114) // 1000 < 150
    rows, cols = dark.mean(1), dark.mean(0); M = 96
    top = max([y for y in range(M) if rows[y] > 0.5], default=None)
    bot = min([y for y in range(h - M, h) if rows[y] > 0.5], default=None)
    lef = max([x for x in range(M) if cols[x] > 0.5], default=None)
    rig = min([x for x in range(w - M, w) if cols[x] > 0.5], default=None)
    if sum(v is not None for v in (top, bot, lef, rig)) < 3: return f
    y0 = (top if top is not None else -1) + 12; y1 = (bot if bot is not None else h) - 12
    x0 = (lef if lef is not None else -1) + 12; x1 = (rig if rig is not None else w) - 12
    m = np.ones((h, w), bool); m[max(0, y0):y1, max(0, x0):x1] = False
    a[m] = 255
    out = "src/" + f[:-4] + "_unframed.png"
    Image.fromarray(a.astype(np.uint8)).save(f"{D}/{out}")
    return out

def reduce(n):
    c = choose().get(n, {})
    fr = c.get("front", f"{n}_front_i2i_{SEED + 11}.png"); bk = c.get("back", f"{n}_back_i2i_{SEED + 11}.png")
    ic = c.get("icon", f"{n}_icon_{SEED + 41}.png")
    if c.get("key"): fr = keyed(fr)
    if c.get("key-back"): bk = keyed(bk)
    if ic != "derived": ic = unframe(ic)
    v = BYNAME[n]
    import gbs
    typ = gbs.primary_type(v["constant"].lower())
    #  "icon": "derived" -- no drawn bust kept the shape; the icon derived from the new front stands in
    cmd = [PY, f"{HERE}/reduce2.py", n, typ, fr, "--back=" + bk, "--dir=" + DIRN] + ([] if ic == "derived" else ["--icon=" + ic])
    for k in ("box-front", "box-back"):
        if k in c: cmd.append(f"--{k}={c[k]}")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: raise SystemExit(n + ": " + r.stdout + r.stderr)
    m = json.loads(r.stdout.strip().splitlines()[-1])
    if ic == "derived":
        import shutil; shutil.copy(f"{D}/reduced/{n}_icon_derived.png", f"{D}/reduced/{n}_icon.png")
    for k in ("name", "type", "front"): m.pop(k, None)
    rec = {"name": v["name"], "national": v["national"], "slot": v["constant"].lower(), "gametype": v["types"][0],
           "type": typ, "props": S[n]["props"], "note": c.get("note", ""), "failed": c.get("failed", ""),
           "front": fr, "back": bk, "icon": ic, "measured": m}
    print(n, typ, "front %.1f%% back %.1f%%" % (m["front_accent_pct"], m["back_accent_pct"]), m["front_streaks"]["painted"], flush=True)
    return rec

def sheets(P):
    items = sorted(((n, p) for n, p in P.items() if not n.startswith("_")), key=lambda t: t[1]["national"])
    #  overview: today 1x 2x | (--prev=DIR: that batch's 1x 2x |) new 1x 2x; four to a row, three with --prev
    PREV = opt.get("prev"); PD = f"{T}/{PREV}" if PREV else None
    pair = 64 + 8 + 128 + 24; ncol = 3 if PREV else 2; cw = ncol * pair + 16; per = 3 if PREV else 4
    rows = (len(items) + per - 1) // per
    s = Image.new("RGB", (24 + per * cw, 60 + rows * 200), PAPER); d = ImageDraw.Draw(s)
    d.text((24, 12), f"T-452 roll-out batch {LABEL}, DRAFT: today | " + (opt.get("prevlabel", f"batch {PREV.upper()}") + " | " if PREV else "") +
           "new, each 1x and 2x on the battle ground, coloured by type; accent % of the new front's pixels (cap 15)",
           fill=INKC, font=F)
    for i, (n, p) in enumerate(items):
        x = 24 + (i % per) * cw; y = 50 + (i // per) * 200
        m = p["measured"]
        d.text((x, y), "%d %s  %s/%s" % (p["national"], p["name"], p["gametype"], p["type"]), fill=INKC, font=FS)
        d.text((x, y + 16), "accents %.1f%% (back %.1f%%)%s" % (m["front_accent_pct"], m["back_accent_pct"],
               "  FAILED: see list" if p["failed"] else ""), fill=RED if p["failed"] else INKC, font=FS)
        cols = [today(n)] + ([sprite(f"{PD}/reduced/{n}_front.png")] if PREV else []) + [sprite(f"{D}/reduced/{n}_front.png")]
        for j, im in enumerate(cols):
            xx = x + j * pair
            s.paste(on(im, GAMEBG, 1), (xx, y + 40)); s.paste(on(im, GAMEBG, 2), (xx + 72, y + 40))
    s.save(SP + f"{PREFIX}_overview.png")
    #  backs, the same way (not asked for by name; the backs are half the work)
    s = Image.new("RGB", (24 + per * cw, 60 + rows * 200), PAPER); d = ImageDraw.Draw(s)
    d.text((24, 12), f"T-452 batch {LABEL} backs, DRAFT: today (left) | new (right), 1x and 2x", fill=INKC, font=F)
    for i, (n, p) in enumerate(items):
        x = 24 + (i % per) * cw; y = 50 + (i // per) * 200
        d.text((x, y), "%s" % p["name"], fill=INKC, font=FS)
        t = today(n, "back"); nw = sprite(f"{D}/reduced/{n}_back.png", f"{D}/reduced/{n}_front.png")
        s.paste(on(t, GAMEBG, 1), (x, y + 40)); s.paste(on(t, GAMEBG, 2), (x + 72, y + 40))
        xx = x + 64 + 8 + 128 + 24
        s.paste(on(nw, GAMEBG, 1), (xx, y + 40)); s.paste(on(nw, GAMEBG, 2), (xx + 72, y + 40))
    s.save(SP + f"{PREFIX}_backs.png")
    #  icons: today's slot icon | derived from the new front | drawn; 1x and 3x on the party green
    cols = ["today", "derived", "drawn"]; Sc = 3; cw2 = 32 + 8 + 32 * Sc + 24; per2 = 2
    rows2 = (len(items) + per2 - 1) // per2; bw = 150 + len(cols) * cw2
    s = Image.new("RGB", (24 + per2 * bw, 70 + rows2 * (32 * Sc + 16)), PAPER); d = ImageDraw.Draw(s)
    d.text((24, 10), f"T-452 batch {LABEL} party icons, DRAFT: today | derived from the new front | drawn as a bust; "
           "1x and 3x. Shared icon palettes, so colour is the silhouette's job.", fill=INKC, font=FS)
    for i, (n, p) in enumerate(items):
        bx = 24 + (i % per2) * bw; y = 40 + (i // per2) * (32 * Sc + 16)
        d.text((bx, y + 40), p["name"], fill=INKC, font=FS)
        srcs = [f"{R}/engineGba/graphics/pokemon/{p['slot']}/icon.png", f"{D}/reduced/{n}_icon_derived.png", f"{D}/reduced/{n}_icon.png"]
        for j, f in enumerate(srcs):
            x = bx + 120 + j * cw2
            if not os.path.exists(f): d.text((x, y + 40), "(none)", fill=INKC, font=FS); continue
            ic = sprite(f).crop((0, 0, 32, 32))
            s.paste(on(ic, PARTY, 1), (x, y + 32)); s.paste(on(ic, PARTY, Sc), (x + 40, y))
    s.save(SP + f"{PREFIX}_icons.png")
    #  two battle mocks at 1x (and 3x beside, to read)
    for foe, plr in P.get("_battles", []):
        bg = Image.open(SP + "battle_bg_clean.png").convert("RGBA")
        f = sprite(f"{D}/reduced/{foe}_front.png"); b = sprite(f"{D}/reduced/{plr}_back.png", f"{D}/reduced/{plr}_front.png")
        bg.alpha_composite(f, (144, 8)); bg.alpha_composite(b, (40, 48)); one = bg.convert("RGB")
        s = Image.new("RGB", (240 + 720 + 72, 520), PAPER); d = ImageDraw.Draw(s)
        s.paste(one, (24, 60)); s.paste(one.resize((720, 480), Image.NEAREST), (288, 30))
        d.text((24, 8), "MOCK, T-452 batch %s DRAFT: %s front vs %s back, 1x (left) and 3x" % (LABEL, foe.upper(), plr.upper()), fill=INKC, font=FS)
        d.text((24, 236), "boxes and names from\nan earlier theatre shot;\nonly the two sprites\nare new", fill=INKC, font=FS)
        s.save(SP + f"{PREFIX}_battle_{foe}_vs_{plr}.png")
    #  failures: what was lost, beside today's and the draft
    fails = [(n, p) for n, p in items if p["failed"]]
    s = Image.new("RGB", (1100, 70 + max(1, len(fails)) * 220), PAPER); d = ImageDraw.Draw(s)
    d.text((24, 12), f"T-452 batch {LABEL}: what failed, and why (today's front and back | the chosen drafts | reduced)", fill=INKC, font=F)
    if not fails: d.text((24, 60), "nothing failed", fill=INKC, font=F)
    for i, (n, p) in enumerate(fails):
        y = 50 + i * 220
        import textwrap
        d.text((24, y - 6), "\n".join(textwrap.wrap(p["name"] + ": " + p["failed"], 150)), fill=RED, font=FS)
        y += 10
        s.paste(on(today(n), GAMEBG, 2), (24, y + 24)); s.paste(on(today(n, "back"), GAMEBG, 2), (160, y + 24))
        s.paste(Image.open(f"{D}/{p['front']}").convert("RGB").resize((160, 160)), (310, y + 24))
        s.paste(Image.open(f"{D}/{p['back']}").convert("RGB").resize((160, 160)), (480, y + 24))
        s.paste(on(sprite(f"{D}/reduced/{n}_front.png"), GAMEBG, 2), (660, y + 24))
        s.paste(on(sprite(f"{D}/reduced/{n}_back.png", f"{D}/reduced/{n}_front.png"), GAMEBG, 2), (800, y + 24))
    s.save(SP + f"{PREFIX}_failures.png")
    print("sheets:", PREFIX + "_{overview,backs,icons,failures,battle_*}.png in the scratchpad")

if stage in ("gen", "all"):
    for n in names: gen(n)
if stage == "t2i":
    for n in names: t2i(n)
if stage == "charm":
    for n in names: charm(n)
if stage == "charm8":   # batch 8 (shared server, four batches at once): one back from today's, one icon
    for n in names: charm(n, lean=True)
if stage == "charmlo":
    for n in names: charmlo(n)
if stage == "charmback":
    for n in names: charmback(n)
if stage == "lo":
    for n in names: lo(n)
if stage == "icon2":
    for n in names: icon2(n)
if stage == "contact":
    for n in names: contact(n)
if stage in ("reduce", "all"):
    P = {n: reduce(n) for n in names}
    old = json.load(open(D + "/picks.json")) if os.path.exists(D + "/picks.json") else {}
    old.update(P)
    bt = opt.get("battles")
    if bt: old["_battles"] = [b.split(":") for b in bt.split(",")]
    json.dump(old, open(D + "/picks.json", "w"), indent=1)
if stage in ("sheets", "all"):
    sheets(json.load(open(D + "/picks.json")))
