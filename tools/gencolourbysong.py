#!/usr/bin/env python3
"""T-597: COLOUR BY SONG -- a daemon's colours come in with the notes of its song it learns. A PROTOTYPE, DRAFT: it
changes nothing in the engine and writes nothing but the pictures it is asked for.

    python3 tools/gencolourbysong.py                          # report: the rule, the census, what would need drawing
    python3 tools/gencolourbysong.py NAME... [--share N]      # each form's slots, their notes, and its palette at a
                                                              # share of its own part (0..255, default every quarter)
    python3 tools/gencolourbysong.py --sheet DIR NAME...      # a contact sheet per line: every form, every approach,
                                                              # at 0, 25, 50, 75 and 100% of its own part, beside today

THE USER'S WORDS (2026-11-18): "those colour levels of the daemon were most representative of how the daemons' own song
part completion"; "the colours in the first form would carry through and already be coloured in the next form, but as
they train and discover that next part of their song those new colours populate"; "it is okay if we do have to redraw
some"; and (the lane note) "for a daemon of a given type, the colours of its representative musical key should be
leaned into as the predominant colours in the daemon's sprite (but not limited to)".

WHAT A PALETTE IS HERE (tools/gbasprite.py): 0 transparent; 1-4 the BODY, one ramp of the type's colour (9.4); 5 the
INK, true black (T-184); 6-10 the ACCENTS, the drawing's own markings; 11-14 the STREAKS, one grey in the file and
filled from the daemon's moves at runtime (T-132); 15 unused.

THE TIE (every approach): a slot is tied to the notes of the song it comes in with.
    the body      the type is the KEY (gensongs.KEYS), and a key is the whole part, not one note: the ramp comes in
                  with every note of the part (tied to the tonic alone it waited for the last note in half the lines)
    an accent     the note of its own part nearest its hue on SYNESTHESIA's wheel (C red ... B violet, a black key
                  between its neighbours); an accent too grey to have a hue is the key's, as the body is
    the ink       never: an outline is not a colour (T-184)
    the streaks   the part as a whole (they are the moves', T-132; the file holds only their grey)
A slot's FILL is the share of its notes learned (at the engine's own learn points, gensongs.engine_rows), each note's
colour closing on it over the WINDOW its static closes over (SONG_WINDOW), so it comes in a note at a time and is whole
at 100%.

EVOLUTION: a colour the earlier forms already had -- or the nearest to one -- is CARRIED: whole from the first frame of
the new form, never grey again. Only a colour new to the form waits, and it waits for the NEW part's notes.

THE THREE APPROACHES (the user picks; vision 8.6's daemons row, T-424's hook):
    A  GREY UNTIL SUNG      an unlearned colour is its own grey (T-424's Desaturate, its 12% floor kept), so the
                            drawing reads at 0% and its colours arrive note by note.
    B  THE KEY FIRST        an unlearned colour is a wash of the KEY's colour (the tonic's) at its own value, so a
                            daemon at 0% is a monochrome in its key, and each note turns its colour to its own.
    C  THE KEY'S PALETTE    an art pass (the lane note) and then A: every accent's hue moved onto the nearest note of
                            the key that its part sings, so the key's colours are the drawing's; the body stays the type
                            (invariant 5 -- six pairs of types share a tonic). Forms with nothing new to fill are listed
                            for redrawing.
"""
import colorsys, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import gensongs as gsg

GBA = os.path.join(ROOT, "engineGba")
GFX = os.path.join(GBA, "graphics", "pokemon")

BODY, INK, ACCENTS, STREAKS = range(1, 5), 5, range(6, 11), range(11, 15)
KEEP_LOW = 31                     # T-424's floor (daemon_saturation.c): a hint of the hue at nothing learned
NEUTRAL = 0.16                    # an accent less saturated than this has no hue to tie: it is the key's (the tonic)
CARRY_NEAR = 40                   # RGB distance: a colour this near an earlier form's is the same colour
CARRY_FAR = 80                    # ... and an earlier colour carries its nearest new colour if it is within this
TINT = 0.45                       # B: how much of the key's colour an unlearned colour wears
SHARES = [0, 64, 128, 191, 255]   # 0, 25, 50, 75, 100% of a part, as the engine counts it
LETTER = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
SCALE = {False: gsg.MAJOR, True: gsg.MINOR}


# ------------------------------------------------------------------------------------------------- colour helpers
def rgb_hex(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def hsv(c):
    return colorsys.rgb_to_hsv(*[x / 255 for x in c])


def pc_rgb(pc):
    """A pitch's colour: a white key's own, a black key the blend of its neighbours (SYNESTHESIA)."""
    cs = [rgb_hex(x) for x in gsg.pc_colours(pc)]
    return tuple(sum(c[i] for c in cs) // len(cs) for i in range(3))


def _circ_mean(a, b):
    d = (b - a + 0.5) % 1.0 - 0.5
    return (a + d / 2) % 1.0


PC_HUE = {}
for _pc in range(12):
    _cs = gsg.pc_colours(_pc)
    _h = [hsv(rgb_hex(x))[0] for x in _cs]
    PC_HUE[_pc] = _h[0] if len(_h) == 1 else _circ_mean(*_h)


def name(pc):
    return "key" if pc is None else LETTER[pc]


def hue_gap(a, b):
    d = abs(a - b) % 1.0
    return min(d, 1 - d)


def to5(c):
    """The GBA keeps five bits a channel."""
    return tuple(x >> 3 for x in c)


def to8(c5):
    return tuple((x << 3) | (x >> 2) for x in c5)


def desaturate(c, keep):
    """daemon_saturation.c's Desaturate, in the GBA's own five bits: each channel toward the colour's grey."""
    r, g, b = to5(c)
    grey = (r * 77 + g * 150 + b * 29 + 128) >> 8
    f = lambda x: grey + int((x - grey) * keep / 256)   # C's division truncates toward zero, as int() does
    return to8((f(r), f(g), f(b)))


def lum(c):
    return (c[0] * 77 + c[1] * 150 + c[2] * 29) / 256


def key_wash(c, tonic_rgb, amount):
    """B: the colour's own grey, washed with the key's colour (its chroma, not its value)."""
    g = lum(c)
    tl = lum(tonic_rgb)
    return tuple(max(0, min(255, int(round(g + (tonic_rgb[i] - tl) * amount)))) for i in range(3))


def mix(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def dist(a, b):
    return sum((a[i] - b[i]) ** 2 for i in range(3)) ** 0.5


# ------------------------------------------------------------------------------------------------- the data
def read_pal(path):
    rows = open(path).read().split("\n")[3:19]
    return [tuple(int(x) for x in r.split()) for r in rows if r.strip()]


class World:
    def __init__(self):
        self.sp, self.paths, _ = gsg.build()
        self.rows = {str(r["id"]): r for r in gsg.engine_rows(self.sp)}
        self.by_name = {v["name"]: k for k, v in self.sp.items()}

    def folder(self, k):
        return os.path.join(GFX, self.sp[k]["constant"].lower())

    def has_art(self, k):
        return os.path.exists(os.path.join(self.folder(k), "front.png"))

    def palette(self, k):
        return read_pal(os.path.join(self.folder(k), "normal.pal"))

    def used(self, k):
        from PIL import Image
        return set(Image.open(os.path.join(self.folder(k), "front.png")).getdata())

    def line(self, k):
        """The whole line through k: its path, and every form after it (the first branch where it branches)."""
        path = list(self.paths[k])
        while True:
            nxt = [e for e in (self.sp[path[-1]].get("evolutions") or []) if str(e["target"]) in self.sp]
            if not nxt or len(path) >= 3:
                return path
            path.append(str(nxt[0]["target"]))


# ------------------------------------------------------------------------------------------------- the rule
def slot_kind(i, pal, used):
    if i == 0 or i == 15:
        return None
    if i == INK:
        return "ink"
    if i in BODY:
        return "body"
    if i in STREAKS:
        return "streak" if i in used else None
    if i in ACCENTS and i in used and pal[i] != (0, 0, 0):
        return "accent"
    return None


def snap_to_key(c, tonic, minor, sung):
    """C: an accent's hue moved onto the nearest note of the key its part sings; its own value kept, and its
    saturation half way to the note's. A grey accent stays grey."""
    h, s, v = hsv(c)
    if s < NEUTRAL:
        return c
    inkey = [pc for pc in sung if (pc - tonic) % 12 in SCALE[minor]] or sorted(sung)
    pc = min(inkey, key=lambda p: hue_gap(h, PC_HUE[p]))
    ns = hsv(pc_rgb(pc))[1]
    out = colorsys.hsv_to_rgb(PC_HUE[pc], s + (ns - s) * 0.5, v)
    return tuple(int(round(x * 255)) for x in out)


def form_palette(w, k, approach):
    """The palette the form is drawn from: as built, or (C) moved onto its key."""
    pal = w.palette(k)
    if approach != "C" or k not in w.rows:
        return pal
    r = w.rows[k]
    sung = {n[0] % 12 for n in r["notes"]}
    used = w.used(k)
    return [snap_to_key(c, r["tonic"], r["minor"], sung) if slot_kind(i, pal, used) == "accent" else c
            for i, c in enumerate(pal)]


def ties(w, k, approach):
    """Each slot: (kind, the pitch class it waits for or None, carried, the learn points of its notes)."""
    pal = form_palette(w, k, approach)
    used = w.used(k)
    row = w.rows.get(k)
    notes = row["notes"] if row else []
    tonic = row["tonic"] if row else 0
    sung = sorted({n[0] % 12 for n in notes}) or [tonic]
    earlier = []
    for e in w.paths[k][:-1]:
        if w.has_art(e):
            ep, eu = form_palette(w, e, approach), w.used(e)
            earlier += [ep[i] for i in range(1, 11) if slot_kind(i, ep, eu) in ("body", "accent")]
    kinds = {i: slot_kind(i, pal, used) for i in range(16)}
    colours = [i for i in range(16) if kinds[i] in ("body", "accent")]
    carried = {i for i in colours if earlier and min(dist(pal[i], e) for e in earlier) <= CARRY_NEAR}
    for e in earlier:                                           # "or the nearest to one"
        if any(dist(pal[i], e) <= CARRY_NEAR for i in colours):
            continue
        near = min(colours, key=lambda i: dist(pal[i], e))
        if dist(pal[near], e) <= CARRY_FAR:
            carried.add(near)
    out = {}
    for i in range(16):
        kind = kinds[i]
        if kind in ("body", "accent"):
            h, s, _ = hsv(pal[i])
            pc = None if (kind == "body" or s < NEUTRAL) else min(sung, key=lambda p: hue_gap(h, PC_HUE[p]))
            pts = [n[2] for n in notes if pc is None or n[0] % 12 == pc]
            out[i] = (kind, pc, i in carried, pts)
        elif kind == "streak":
            out[i] = (kind, None, False, [n[2] for n in notes])
        else:
            out[i] = (kind, None, False, [])
    return pal, out


WINDOW = round(gsg.WINDOW * 255)   # a note's colour closes on it over the same stretch its static does (SONG_WINDOW)


def note_in(p, share):
    """How much of one note's colour is in: none until WINDOW before its point, all of it at its point."""
    if share >= p:
        return 1.0
    return max(0.0, 1 - (p - share) / WINDOW)


def fill(tie, share):
    kind, pc, carried, pts = tie
    if kind not in ("body", "accent", "streak") or carried or not pts:
        return 1.0
    return sum(note_in(p, share) for p in pts) / len(pts)


def shown(w, k, approach, share):
    """The palette the form shows at this share of its own part (0..255)."""
    pal, t = ties(w, k, approach)
    row = w.rows.get(k)
    tonic_rgb = pc_rgb(row["tonic"]) if row else (128, 128, 128)
    out = list(pal)
    for i in range(1, 16):
        f = fill(t[i], share)
        if f >= 1.0:
            continue
        if approach == "B":
            out[i] = mix(key_wash(pal[i], tonic_rgb, TINT), pal[i], f)
        else:
            out[i] = desaturate(pal[i], KEEP_LOW + int((256 - KEEP_LOW) * f))
    return out


def needs_drawing(w, k):
    """Why a form has too little to fill: no accent at all, or (a later form) no colour new to its part."""
    _, t = ties(w, k, "A")
    accents = [i for i, x in t.items() if x[0] == "accent"]
    new = [i for i, x in t.items() if x[0] in ("body", "accent") and not x[2]]
    why = []
    if len(w.paths[k]) > 1 and not new:
        why.append("nothing new to learn: every colour carried from the form before")
    if not accents:
        why.append("no accent: only the body ramp, one colour, can come in")
    elif all(t[i][1] is None for i in accents):
        why.append("grey accents only: nothing comes in in a note's own colour")
    return why


def waiting_area(w, k):
    """The share of the drawing's pixels whose colour waits on its own part (not carried, not ink, not a streak)."""
    from PIL import Image
    _, t = ties(w, k, "A")
    idx = [v for v in Image.open(os.path.join(w.folder(k), "front.png")).getdata() if v]
    wait = [v for v in idx if t[v][0] in ("body", "accent") and not t[v][2]]
    return len(wait) / max(1, len(idx))


# ------------------------------------------------------------------------------------------------- report
def describe(w, k, approach="A"):
    pal, t = ties(w, k, approach)
    r = w.rows.get(k, {})
    lines = ["%s (%s, %s, Lv %s-%s, %d notes)" % (w.sp[k]["name"], "/".join(w.sp[k]["types"]), r.get("key", "?"),
                                                  r.get("from", "?"), r.get("to", "?"), len(r.get("notes", [])))]
    for i in range(1, 16):
        kind, pc, carried, pts = t[i]
        if kind in ("body", "accent"):
            lines.append("   %2d %-6s %-15s -> %-3s %s" % (i, kind, "%d,%d,%d" % pal[i], name(pc),
                         "CARRIED" if carried else "at " + " ".join("%d%%" % round(p * 100 / 255) for p in pts)))
        elif kind == "streak":
            lines.append("   %2d streak  (the moves')      -> the part as a whole" % i)
    return "\n".join(lines)


def report(names, share):
    w = World()
    if names:
        for n in names:
            k = w.by_name.get(n.upper())
            if not k:
                print("gencolourbysong: no daemon %s" % n)
                continue
            for f in w.line(k):
                if not w.has_art(f):
                    continue
                print(describe(w, f))
                for s in ([share] if share is not None else SHARES):
                    print("   at %3d%%: %s" % (round(s * 100 / 255), " ".join("%02X%02X%02X" % c for c in shown(w, f, "A", s)[1:15])))
        return 0
    forms = [k for k in w.sp if w.has_art(k) and k in w.rows]
    draw = {k: needs_drawing(w, k) for k in forms}
    by_why = {}
    for k, why in draw.items():
        for y in why:
            by_why.setdefault(y, []).append(w.sp[k]["name"])
    print("gencolourbysong: %d forms with art and a song (T-597 prototype, DRAFT)" % len(forms))
    steps = []
    for k in forms:
        _, t = ties(w, k, "A")
        steps.append(len({p for x in t.values() if x[0] in ("body", "accent") and not x[2] for p in x[3]}))
    steps.sort()
    print("  the distinct moments a form's colour changes as its part is learned: median %d, fewest %d, most %d"
          % (steps[len(steps) // 2], steps[0], steps[-1]))
    for y, ns in sorted(by_why.items(), key=lambda kv: -len(kv[1])):
        print("  %3d %s: %s%s" % (len(ns), y, ", ".join(ns[:14]), " ..." if len(ns) > 14 else ""))
    later = [k for k in forms if len(w.paths[k]) > 1]
    area = sorted(waiting_area(w, k) for k in later)
    small = [w.sp[k]["name"] for k in later if waiting_area(w, k) < 0.10]
    print("  a later form's drawing that waits on its own part (the rest carried): median %d%% of its pixels; %d of %d "
          "under 10%%, so its part would barely show: %s ..." % (round(100 * area[len(area) // 2]), len(small),
                                                                len(later), ", ".join(small[:12])))
    redraw = sorted({n for ns in by_why.values() for n in ns} | set(small))
    print("  candidates for drawing (any of the above): %d forms" % len(redraw))
    print("  the type's colour against its key's tonic (hue apart, degrees):")
    seen = {}
    for k in forms:
        ty = w.sp[k]["types"][0]
        if ty in seen:
            continue
        body = w.palette(k)[3]
        tonic = w.rows[k]["tonic"]
        seen[ty] = (round(hue_gap(hsv(body)[0], PC_HUE[tonic]) * 360), LETTER[tonic], round(hsv(body)[1] * 100))
    for ty, (d, l, s) in sorted(seen.items(), key=lambda kv: kv[1][0]):
        print("     %-9s %-3s %3d%s" % (ty, l, d, "   (the type has little hue: %d%% saturated)" % s if s < 25 else ""))
    return 0


# ------------------------------------------------------------------------------------------------- the sheet
def sheet(outdir, names):
    from PIL import Image, ImageDraw, ImageFont
    w = World()
    os.makedirs(outdir, exist_ok=True)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 13)
        small = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 11)
        big = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 18)
    except OSError:
        font = small = big = ImageFont.load_default()
    SC, CELL, STRIP = 2, 136, 10
    LABEL = 210
    cols = [("TODAY", None), ("TODAY, f70", "f70")] + [("%d%%" % round(s * 100 / 255), s) for s in SHARES]
    BG = (236, 236, 230)
    written = []
    for n in names:
        k0 = w.by_name.get(n.upper())
        if not k0:
            print("gencolourbysong: no daemon %s" % n)
            continue
        forms = [f for f in w.line(k0) if w.has_art(f)]
        rows = [(f, a) for f in forms for a in ("A", "B", "C")]
        head = 64
        tie_h = 0
        tie_txt = {}
        for f in forms:
            pal, t = ties(w, f, "A")
            parts = []
            for i in range(1, 15):
                kind, pc, carried, pts = t[i]
                if kind == "body" and i != 3:
                    continue
                if kind in ("body", "accent"):
                    parts.append("%s %d->%s%s" % ("body" if kind == "body" else "acc", i, name(pc),
                                 " carried" if carried else " x%d" % len(pts)))
            tie_txt[f] = parts
        H = head + len(forms) * (24 + 3 * (CELL + STRIP + 14)) + 40
        W = LABEL + len(cols) * (CELL + 8) + 20
        im = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(im)
        line_names = " > ".join(w.sp[f]["name"] for f in forms)
        d.text((12, 10), "T-597 COLOUR BY SONG (DRAFT)  %s" % line_names, fill=(20, 20, 24), font=big)
        d.text((12, 36), "A grey until sung   B the key first   C the key's palette, then A.   "
               "% = share of the form's OWN part learned (the earlier parts whole).", fill=(60, 60, 60), font=small)
        y = head
        for f in forms:
            r = w.rows[f]
            d.text((12, y + 4), "%s  %s  %s  Lv %d-%d  %d notes   ties: %s" % (
                w.sp[f]["name"], "/".join(w.sp[f]["types"]), r["key"], r["from"], r["to"], len(r["notes"]),
                ", ".join(tie_txt[f])), fill=(20, 20, 24), font=font)
            y += 24
            for a in ("A", "B", "C"):
                d.text((12, y + 40), {"A": "A grey until sung", "B": "B the key first", "C": "C key's palette"}[a],
                       fill=(30, 30, 30), font=font)
                if a == "C":
                    sp = form_palette(w, f, "C")
                    d.text((12, y + 60), "(accents on the key)", fill=(90, 90, 90), font=small)
                for ci, (title, s) in enumerate(cols):
                    x = LABEL + ci * (CELL + 8)
                    if title.startswith("TODAY") and a != "A":
                        continue
                    if s is None:
                        pal = w.palette(f)
                    elif s == "f70":
                        pal = [w.palette(f)[0]] + [desaturate(c, 31 + 225 * (65025 - 185 * 185) // 65025)
                                                    for c in w.palette(f)[1:]]
                    else:
                        pal = shown(w, f, a, s)
                    idx = list(Image.open(os.path.join(w.folder(f), "front.png")).getdata())
                    rgba = Image.new("RGB", (64, 64))
                    rgba.putdata([pal[v] if v < len(pal) else (0, 0, 0) for v in idx])
                    mask = Image.new("L", (64, 64))
                    mask.putdata([255 if v else 0 for v in idx])
                    rgba = rgba.resize((64 * SC, 64 * SC), Image.NEAREST)
                    mask = mask.resize((64 * SC, 64 * SC), Image.NEAREST)
                    im.paste(rgba, (x + 4, y + 2), mask)
                    d.rectangle([x, y, x + CELL, y + CELL], outline=(200, 200, 194))
                    for j in range(1, 15):
                        d.rectangle([x + (j - 1) * 9 + 4, y + CELL + 2, x + (j - 1) * 9 + 12, y + CELL + STRIP],
                                    fill=pal[j])
                    if y == head + 24 and f == forms[0]:
                        pass
                    if a == "A" or not title.startswith("TODAY"):
                        d.text((x + 4, y + CELL - 14), title, fill=(70, 70, 70), font=small)
                y += CELL + STRIP + 14
        d.text((12, H - 26), "Strip under each picture: palette slots 1-14 (1-4 body, 5 ink, 6-10 accents, 11-14 the "
               "streaks' grey, filled from moves at runtime).", fill=(80, 80, 80), font=small)
        path = os.path.join(outdir, "t597_%s.png" % w.sp[forms[0]]["name"].lower().replace(" ", "_"))
        im.save(path)
        written.append(path)
        print("gencolourbysong: wrote %s" % path)
    return 0


def main():
    a = sys.argv[1:]
    share = None
    if "--share" in a:
        i = a.index("--share")
        share = max(0, min(255, int(a[i + 1])))
        del a[i:i + 2]
    if "--sheet" in a:
        i = a.index("--sheet")
        return sheet(a[i + 1], a[i + 2:] or ["ROVERCUB"])
    return report(a, share)


if __name__ == "__main__":
    sys.exit(main())
