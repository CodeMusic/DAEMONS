"""T-452 round two, part A: batch 1's notes (the user, 2026-10-25, on the built art), drafted into gfx/drafts/t452/r.

    round2.py gen       the drafts that need the sprite server (LOCUS's back; RELAY's and BUFFER's backs re-gridded)
    round2.py build     everything else, and the reductions: r/clean/*, r/reduced/*, r/fixes.json

ROVERCUB  the pilot's front stood on a pale ground ellipse the clean kept (b/clean/rovercub_front.png). The ellipse
          is taken off the CLEAN grid, not redrawn: a flood from the transparent ground through pale cells (value
          >= 110, grey) in the lower third of the figure. The feet are sealed by their outline, so the fill stops at
          them; the gap between the legs is ellipse too, and goes.
LOCUS     its back was a pink bean (today's old back repainted). Redrawn as the new front from behind: four
          text-to-image rear views naming the key shape (the tail curled into a loop) -- SEED+1..4 -- and two by
          image-to-image from the new front MIRRORED, at 0.7 and 0.8, rear-view prompt (SEED+11, +12).
RELAY,    their backs were drawn small in the frame (RELAY's 42px tall against a 51px front). The chosen draft is
BUFFER    cropped to its subject and scaled so the subject's longer side is 58 of the 64 cells, feet on the same
          ground line, then re-gridded by image-to-image at 0.3 and 0.4 (SEED+21, +22) -- a plain resize of an 8px
          grid by 1.4 leaves cells of two sizes. CHOSEN, though: the plain zoom (r/src/*_back_zoom.png) -- both
          i2i passes tinted the grey body blue and the reduction kept it as violet fringes; uneven cells don't show.
MANIFOLD  (part B, drafted in e/ and m/) preclean() below takes the grey card some drafts come on.
ICONS     ROVERSEER, INDEXER, INJECTOR, CRAWLER: icon3.py (its docstring says why they were muddy) from the same
          drawn busts; CRAWLER's drafts were four to a frame, so one quarter of seed 4841 is the source.
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from subjects import S
import icon3
R = "/Users/christopherhicks/Projects/DAEMONS"; T = R + "/gfx/drafts/t452"; D = T + "/r"; REL = "gfx/drafts/t452/r"
PY = os.path.expanduser("~/.pyenv/versions/3.12.2/bin/python3"); SEED = 5000
os.chdir(R)
for d in ("src", "clean", "reduced"): os.makedirs(f"{D}/{d}", exist_ok=True)
D1 = json.load(open(T + "/d/picks.json")); B2 = json.load(open(T + "/b/picks2.json"))

HEAD = "pure white background, pixel art game sprite of a single cute creature, "
GB = ("full body, chibi proportions, big round head seen from behind, soft shading, mostly greyscale, "
      "medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, "
      "centered, large in the frame, no shadow, no text")
GBC = "rear view, seen from behind, facing away from the viewer, " + GB
N = ("photorealistic, 3d render, colorful, rainbow, colored background, grey background, dark background, scenery, "
     "floor, ground, text, letters, watermark, multiple creatures, two creatures, duplicate, human, person, cropped, "
     "blurry, drop shadow, border, white body, pale body")
NB = "face, eyes, nose, mouth, beak tip, whiskers, front view, facing the viewer, side view, profile, " + N

def run(a):
    out = a[a.index("--out") + 1]
    if os.path.exists(out + ".png"): return
    t = subprocess.run([PY, "tools/spriteforge.py"] + a, capture_output=True, text=True)
    print(out, t.stdout.strip()[-60:], t.stderr.strip()[-300:], flush=True)

LOCUS_KEY = "a long thick tail curled up behind it into a big round loop"
LOCUS_BACK = ("a cute little round grey critter seen from behind, the back of its round head with two small pointed ears, "
              "a round grey back, two stubby feet, its long thick tail curled up into a big round loop")

def bgmask(a):
    b = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]]); bg = np.median(b, 0)
    return np.abs(a - bg).max(2) > 28, bg

def zoom(n, src, target=58):
    a = np.asarray(Image.open(src).convert("RGB")).astype(int); m, bg = bgmask(a)
    ys, xs = np.where(m); y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    crop = Image.fromarray(a[y0:y1, x0:x1].astype(np.uint8))
    sc = target * 8 / max(crop.size); w, h = round(crop.width * sc), round(crop.height * sc)
    big = Image.new("RGB", (512, 512), tuple(int(v) for v in bg))
    big.paste(crop.resize((w, h), Image.LANCZOS), ((512 - w) // 2, 512 - 24 - h))
    out = f"{D}/src/{n}_back_zoom.png"; big.save(out); return out

def gen():
    s = S["locus"]; bneg = "girl, long hair, hair, snake, worm, food, bagel, pink, " + NB
    for k in range(4):
        run(["t2i", "--size", "512x512", "--seed", str(SEED + 1 + k), "--out", f"{REL}/locus_back_{SEED + 1 + k}",
             "--prompt", HEAD + LOCUS_KEY + ", " + LOCUS_BACK + ", " + GBC, "--negative", bneg])
    fr = Image.open(f"{T}/d/{D1['locus']['front']}").convert("RGB").transpose(Image.FLIP_LEFT_RIGHT)
    src = f"{D}/src/locus_newfront_mirror_512.png"; fr.save(src)
    for k, dn in enumerate((0.7, 0.8)):
        run(["i2i", "--seed", str(SEED + 11 + k), "--denoise", str(dn), "--image", src,
             "--out", f"{REL}/locus_back_fromfront_{SEED + 11 + k}", "--prompt", HEAD + LOCUS_KEY + ", " + LOCUS_BACK + ", " + GBC,
             "--negative", bneg])
    for n in ("relay", "buffer"):
        z = zoom(n, f"{T}/d/{D1[n]['back']}")
        bp = HEAD + S[n]["back"] + ", " + GBC
        for k, dn in enumerate((0.3, 0.4)):
            run(["i2i", "--seed", str(SEED + 21 + k), "--denoise", str(dn), "--image", z,
                 "--out", f"{REL}/{n}_back_zoom_i2i_{SEED + 21 + k}", "--prompt", bp, "--negative", S[n]["neg"] + ", " + NB])

def unground(src, out):
    """ROVERCUB's ellipse off the clean grid"""
    a = np.array(Image.open(src).convert("RGBA")).astype(int)
    L = (a[..., 0] * 299 + a[..., 1] * 587 + a[..., 2] * 114) // 1000; sat = a[..., :3].max(2) - a[..., :3].min(2)
    op = a[..., 3] > 127; ys = np.where(op.any(1))[0]; y0, y1 = ys.min(), ys.max()
    lo = y0 + int((y1 - y0) * 0.66)
    pale = op & (L >= 110) & (sat < 40); pale[:lo] = False
    seen = np.zeros(op.shape, bool); st = []
    for y, x in zip(*np.where(pale)):
        if any(0 <= y + dy < 64 and 0 <= x + dx < 64 and not op[y + dy, x + dx] for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            seen[y, x] = True; st.append((y, x))
    while st:
        y, x = st.pop()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p, q = y + dy, x + dx
            if 0 <= p < 64 and 0 <= q < 64 and pale[p, q] and not seen[p, q]: seen[p, q] = True; st.append((p, q))
    #  a foot whose sole was the ellipse is left open at the bottom: a removed cell under a pale cell of the
    #  figure becomes outline, the figure's own darkest ink
    ink = a[op & (L < 60)][:, :4]; ink = ink[np.argmin(ink[:, :3].sum(1))] if len(ink) else np.array([30, 30, 34, 255])
    sole = seen & np.roll(op & ~seen & (L >= 60), 1, 0)
    a[seen, 3] = 0; a[seen, :3] = 0
    a[sole] = ink
    Image.fromarray(a.astype(np.uint8), "RGBA").save(out)
    return int(seen.sum())

def reduce(n, front, back, typ):
    r = subprocess.run([PY, f"{HERE}/reduce2.py", n, typ, front, "--back=" + back, "--dir=r"], capture_output=True, text=True)
    if r.returncode: raise SystemExit(n + ": " + r.stdout + r.stderr)
    return json.loads(r.stdout.strip().splitlines()[-1])

def build():
    ch = json.load(open(D + "/choose.json"))
    rep = {}
    #  ROVERCUB: the built clean front, ungrounded; its reduction re-placed in GRASS beside the built back
    import gbs
    gone = unground(f"{T}/b/clean/rovercub_front.png", f"{D}/clean/rovercub_front.png")
    g, p = gbs.place_rich(f"{D}/clean/rovercub_front.png", gbs.TYPE_COLOR["GRASS"])
    gbs.write_png4(f"{D}/reduced/rovercub_front.png", g, p)
    gb, _ = gbs.place_rich(f"{T}/b/clean/rovercub_back.png", gbs.TYPE_COLOR["GRASS"], shared=p)
    gbs.write_png4(f"{D}/reduced/rovercub_back.png", gb, p)
    rep["rovercub"] = {"ground_cells_removed": gone, "note": "the pale ground ellipse under the feet and between the legs, off the built front"}
    #  the backs: the built front's draft with the chosen new back, re-reduced together (one palette)
    for n in ("locus", "relay", "buffer"):
        m = reduce(n, "../d/" + D1[n]["front"], ch[n]["back"], D1[n]["type"])
        rep[n] = {"back": ch[n]["back"], "note": ch[n].get("note", ""), "back_accent_pct": m["back_accent_pct"],
                  "front_accent_pct": m["front_accent_pct"]}
    #  the icons
    for n, src in (("roverseer", f"{T}/d/clean/roverseer_icon.png"), ("indexer", f"{T}/d/clean/indexer_icon.png"),
                   ("injector", f"{T}/d/clean/injector_icon.png"), ("crawler", f"{D}/clean/crawler_icon_src.png")):
        if n == "crawler" and not os.path.exists(src):
            Image.open(f"{T}/d/crawler_icon_4841.png").convert("RGB").crop((0, 0, 256, 256)).resize((512, 512), Image.NEAREST).save(f"{D}/src/crawler_icon_quad_4841.png")
            subprocess.run([PY, f"{R}/tools/cleandraft.py", f"{D}/src/crawler_icon_quad_4841.png", src], check=True, capture_output=True)
        rep.setdefault(n, {})["icon"] = icon3.make(n, D1[n]["type"], src, f"{D}/reduced/{n}_icon.png")
    json.dump(rep, open(D + "/fixes.json", "w"), indent=1)
    print(json.dumps(rep, indent=1))

if __name__ == "__main__":
    {"gen": gen, "build": build}[sys.argv[1]]()

def preclean(src, out):
    """a draft on a grey card with a lighter rim and a cast shadow (MANIFOLD 4903, 4951): cleandraft's fill starts
    from the rim colour and stops at the card. Flood from the border through every pale grey (value >= 120,
    spread < 25) and stop at the outline (value < 90), then paint what was reached white. The creature is sealed by
    its outline, so its own pale greys are never reached."""
    from collections import deque
    a = np.asarray(Image.open(src).convert("RGB")).astype(int); h, w = a.shape[:2]
    L = (a[..., 0] * 299 + a[..., 1] * 587 + a[..., 2] * 114) // 1000; ok = (L >= 120) & (a.max(2) - a.min(2) < 25)
    seen = np.zeros((h, w), bool); q = deque()
    for y in range(h):
        for x in (0, w - 1):
            if ok[y, x] and not seen[y, x]: seen[y, x] = True; q.append((y, x))
    for x in range(w):
        for y in (0, h - 1):
            if ok[y, x] and not seen[y, x]: seen[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p, r = y + dy, x + dx
            if 0 <= p < h and 0 <= r < w and ok[p, r] and not seen[p, r]: seen[p, r] = True; q.append((p, r))
    a[seen] = 255
    Image.fromarray(a.astype(np.uint8)).save(out); return out

def cardoff(src, out, tol=40):
    """an icon drawn on a card (a flat grey or dark ground, SURGE 4941, PARTITION 4941, THREAD 4941, PREDICTOR 4942):
    flood from the border through everything within TOL of the border's median colour and paint it white --
    cleandraft then takes the white. A card is flat but shaded, so TOL is 40 and nothing else: with preclean()'s pale flood after
    it, the fill went through the outline's gaps into every white body (SUSPEND, FLICKER, THREAD lost half of
    themselves). A draft already on white is copied as it is."""
    from collections import deque
    a = np.asarray(Image.open(src).convert("RGB")).astype(int); h, w = a.shape[:2]
    bd = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]]); bg = np.median(bd, 0)
    if bg.min() > 235:
        Image.fromarray(a.astype(np.uint8)).save(out); return out
    ok = np.abs(a - bg).max(2) <= tol
    seen = np.zeros((h, w), bool); q = deque()
    for y in range(h):
        for x in range(w):
            if (y in (0, h - 1) or x in (0, w - 1)) and ok[y, x]: seen[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p, r = y + dy, x + dx
            if 0 <= p < h and 0 <= r < w and ok[p, r] and not seen[p, r]: seen[p, r] = True; q.append((p, r))
    a[seen] = (0, 200, 0)          # a key ground, not white: cleandraft's own fill would go on into a white body
    Image.fromarray(a.astype(np.uint8)).save(out)
    return out

def icon_from_draft(d, n, draft, typ):
    """card off, cleaned, icon3: the drawn icon as round two files it"""
    src = f"{T}/{d}/src/{n}_icon_card.png"; cl = f"{T}/{d}/clean/{n}_icon.png"
    #  batch.py's unframe() painted outside a drawn box white and left the card inside it: start from the draft itself
    draft = draft.replace("src/", "").replace("_unframed", "")
    cardoff(f"{T}/{d}/{draft}", src)
    subprocess.run([PY, f"{R}/tools/cleandraft.py", src, cl], check=True, capture_output=True)
    return icon3.make(n, typ, cl, f"{T}/{d}/reduced/{n}_icon.png")
