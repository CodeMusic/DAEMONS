#!/usr/bin/env python3
"""T-432: a shiny palette for every daemon, kept inside its type (invariant 5).

    python3 tools/genshiny.py                  # report: each type's shiny anchor, how many daemons change, questions
    python3 tools/genshiny.py --sheet OUT.png  # also draw the review sheets: OUT_1.png, OUT_2.png ... and OUT_overview.png
    python3 tools/genshiny.py --write          # write engineGba/graphics/pokemon/<name>/shiny.pal
    python3 tools/genshiny.py bulbasaur pikachu   # only these folders

WHY A TOOL. tools/gbasprite.py writes each redrawn daemon's shiny.pal as a COPY of its normal.pal, so a shiny looked
like any other daemon everywhere -- only UNOWN and the eight NEXUS daemons, which never went through it, differ.
gbafollowerpal.py's shiny set (T-18 P3) reads shiny.pal, so a palette written here reaches the follower on its next run.

THE RULE IT KEEPS. 9.4: a daemon is coloured by what it IS, and the body ramp (palette 1..5) is the type. A shiny that
took any colour would be a daemon of some other type, so the shift is bounded by the chart itself:

  1. THE BODY RAMP MOVES PER TYPE, NOT PER DAEMON. Each type gets ONE shiny anchor -- its mid tone moved in CIE LCh
     (hue rotated, chroma scaled, lightness held within LSHIFT) -- and the ramp is rebuilt from it by gbasprite's own
     ramp5(), so highlight / light / mid / dark keep their spacing and the sprite reads the same. Every shiny of a type
     shares the anchor, so "a shiny SIGNAL" is one recognisable thing, as the type itself is.
  2. THE ANCHOR MUST STILL BE ITS OWN TYPE. A candidate counts only if it stays NEARER ITS OWN TYPE THAN ANY OTHER
     by at least MARGIN (CIE76 on the mid tone, 9.4's own measure) and turns no more than MAXTURN degrees of hue; of
     those, the one taken lands nearest TARGET from the normal mid -- far enough to see, under the floor of 20 that
     separates two types. Ties go to the smaller turn, then the smaller chroma change. An optimiser that MAXIMISED the
     distance was tried first and gave bone a pink shiny and OPAQUE a maroon one: 9.4's lesson again, distance is
     a constraint here, not the design.
  3. THE ACCENTS TAKE THE SHINY. An eye, a beak, a marking (palette 6..10) rotate by ACCENT_TURN degrees of hue,
     keeping their saturation and value; an accent that lands within 40 degrees of the shiny type hue is pushed to
     the far side (gbasprite's shift_off rule), and one that lands within 20 CIE76 of the ramp tries the next turn.
     Near-grey accents (whites, greys, blacks) are left alone: they carry no hue to turn.
  4. LEFT ALONE: index 0 (transparent), the outline INK at 5, the four streak slots 11..14 (the engine fills them
     from the moves at runtime) and 15, and any pure black or white anywhere.

Deterministic: no randomness, no state; the same normal.pal gives the same shiny.pal.

It finds a daemon's type from its PALETTE (palette 3 is the type's mid tone, exactly), not from species_info.h, because
the palette is what the player sees; a daemon whose mid tone matches no type is skipped and named. Its secondary type
does not move the shiny -- the body is the primary, as 9.4 drew it -- and the report lists the dual types so the user
can say whether a shiny should lean toward the second one instead.

  5. THE PALE TYPES TINT THE LIGHT END TOO (the user, 2026-10-21): see PALE_NAMED below.

WHO OWNS shiny.pal: this tool, for every daemon whose normal.pal is a type ramp; a daemon without one (UNOWN, the
eight NEXUS daemons) keeps the shiny it has. tools/gbasprite.py, which writes normal.pal, calls make_shiny() here for
shiny.pal rather than copying normal.pal into it -- so a whole-tree gbasprite --write keeps the shinies.
"""
import ast, colorsys, math, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daemonslib   # T-421: read_pal / write_pal, CRLF as the engine keeps them

GBA = os.path.join(ROOT, "engineGba")
MON = os.path.join(GBA, "graphics", "pokemon")
WRITE = "--write" in sys.argv

LSHIFT = 3.0       # how far the anchor's L* may move: the ramp's lightness, and so the drawing, stays as it is
MARGIN = 8.0       # the shiny mid must be this much nearer its own type than the nearest other one (CIE76)
MAXSHIFT = 30.0    # and no further than this from the normal mid -- "family", not a new colour
TARGET = 16.0      # the shift aimed for: plainly visible, and still under the floor of 20 that separates two types
MAXTURN = 30       # degrees of LCh hue: further, and a low-chroma type reads as a neighbour though CIE76 says not
GREY_C = 15.0      # a type with less chroma than this may also gain a little (it has no hue to turn otherwise)
ACCENT_TURNS = (180, 120, 240, 90, 270)   # tried in order; the first that clears both floors is taken
ACCENT_MIN_SAT = 0.25                      # HSV saturation below this is a grey: left alone
FLOOR = 20.0                               # 9.4's separability floor, CIE76
#  THE PALE TYPES' STRONGER TELL (the user, 2026-10-21). A type whose body can move only a little inside its bounds,
#  on a daemon with no accent to turn, is a shiny nobody sees. So these also TINT THE LIGHT END: highlight and light
#  keep their lightness and take the anchor's hue, with chroma enough to move them about TINT_TARGET -- and never more
#  chroma than the anchor's own (_tint says why the anchor's distance rule cannot be used at the light end).
PALE_NAMED = ("ROCK", "ICE", "DARK", "BUG", "STEEL")   # LEGACY FROZEN OPAQUE SWARM HARDENED, named by the user
PALE_BELOW = 15.5                                       # and any other type whose anchor moves less than this
TINT_TARGET = 14.0


# ------------------------------------------------------------------------------------------- read gbasprite's table
def _gbasprite():
    """TYPE_COLOR, ramp5's constants, INK and STREAK_BLANK, read out of tools/gbasprite.py rather than copied --
    importing it would run it (it is a script), and a copy would drift the day a hue moves again."""
    src = open(os.path.join(ROOT, "tools", "gbasprite.py"), encoding="utf-8").read()
    tree = ast.parse(src)
    vals = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name in ("TYPE_COLOR", "INK", "STREAK_BLANK", "BG", "STREAK_FIRST"):
                vals[name] = ast.literal_eval(node.value)
    ours = dict(re.findall(r'"(\w+)":\s*\(\s*\d+,\s*\d+,\s*\d+\),\s*#\s*([A-Z]+)', src))
    return vals, ours


_G, OURS = _gbasprite()
TYPE_COLOR, INK, STREAK_BLANK, STREAK_FIRST = _G["TYPE_COLOR"], _G["INK"], _G["STREAK_BLANK"], _G["STREAK_FIRST"]


def ramp5(r, g, b):
    """gbasprite.ramp5, the four tones it derives from the mid (the fifth is INK, left alone)."""
    up = lambda t: tuple(min(255, int(c + (255 - c) * t)) for c in (r, g, b))
    dn = lambda t: tuple(max(0, int(c * t)) for c in (r, g, b))
    return [up(0.70), up(0.38), (r, g, b), dn(0.52)]


# ------------------------------------------------------------------------------------------------- colour science
def _lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _gam(c):
    c = 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
    return c * 255.0


def lab(rgb):
    r, g, b = (_lin(v) for v in rgb)
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    f = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    fx, fy, fz = f(x), f(y), f(z)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def rgb_from_lab(L, a, b):
    """None when the colour is outside sRGB: a shiny is never a clipped colour."""
    fy = (L + 16) / 116
    fx, fz = fy + a / 500, fy - b / 200
    inv = lambda t: t ** 3 if t ** 3 > 0.008856 else (t - 16 / 116) / 7.787
    x, y, z = inv(fx) * 0.95047, inv(fy), inv(fz) * 1.08883
    r = 3.2406 * x - 1.5372 * y - 0.4986 * z
    g = -0.9689 * x + 1.8758 * y + 0.0415 * z
    bb = 0.0557 * x - 0.2040 * y + 1.0570 * z
    out = []
    for v in (r, g, bb):
        if v < -0.0005 or v > 1.0005:
            return None
        out.append(int(round(min(255, max(0, _gam(min(1, max(0, v))))))))
    return tuple(out)


def de(c1, c2):
    a, b = lab(c1), lab(c2)
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def hsv(c):
    return colorsys.rgb_to_hsv(*[v / 255 for v in c])


def hue_gap(h1, h2):
    d = abs(h1 - h2) % 1.0
    return min(d, 1 - d)


# --------------------------------------------------------------------------------------------- the type anchors
def shiny_anchor(t):
    """The one shiny mid tone for type T: about TARGET from its normal mid, still reading as T (rule 2)."""
    mid = TYPE_COLOR[t]
    L, A, B = lab(mid)
    C, H = math.hypot(A, B), math.atan2(B, A)
    others = [lab(TYPE_COLOR[o]) for o in TYPE_COLOR if o != t]
    dist = lambda p, q: math.sqrt(sum((x - y) ** 2 for x, y in zip(p, q)))
    best, best_score = (0.0, 0, mid), None
    adds = (0, 4, 8) if C < GREY_C else (0,)         # a near-grey type (OPAQUE, LEGACY, CONTENT) has little to scale
    for dh in range(-MAXTURN, MAXTURN + 1, 2):        # degrees of hue in LCh
        h2 = H + math.radians(dh)
        for cs in [x / 20 for x in range(16, 33)]:   # chroma x0.80 .. x1.60
            for add in adds:
                for dl in (-LSHIFT, 0.0, LSHIFT):
                    c2 = C * cs + add
                    p = (L + dl, c2 * math.cos(h2), c2 * math.sin(h2))
                    shift = dist(p, (L, A, B))
                    if shift > MAXSHIFT:
                        continue
                    #  rule 2: still nearer its own type (whose mid it moved from) than any other, by MARGIN
                    if min(dist(p, o) for o in others) - shift < MARGIN:
                        continue
                    cand = rgb_from_lab(*p)
                    if cand is None:
                        continue
                    #  measured again after rounding to 8 bits, so the report states what is written
                    s8 = de(cand, mid)
                    if min(dist(lab(cand), o) for o in others) - s8 < MARGIN:
                        continue
                    #  as near TARGET as the chart allows; then the smaller turn, the smaller chroma change, darker
                    score = (round(abs(s8 - TARGET), 1), abs(dh), abs(cs - 1), add, dl)
                    if best_score is None or score < best_score:
                        best, best_score = (s8, dh, cand), score
    return (de(best[2], mid), best[1], best[2])   # (distance from the normal mid, hue turn, the shiny mid)


_ANCHORS = {}


def anchor(t):
    if t not in _ANCHORS:
        _ANCHORS[t] = shiny_anchor(t)
    return _ANCHORS[t]


def nearest_other(t, rgb):
    o = min((x for x in TYPE_COLOR if x != t), key=lambda x: de(rgb, TYPE_COLOR[x]))
    return o, de(rgb, TYPE_COLOR[o])


# ---------------------------------------------------------------------------------------------- one daemon's shiny
def is_fixed(c):
    return c in ((0, 0, 0), (255, 255, 255), INK, STREAK_BLANK)


def turn_accent(c, shiny_ramp, type_hue):
    h, s, v = hsv(c)
    if is_fixed(c) or s < ACCENT_MIN_SAT or max(c) - min(c) < 30:
        return c
    for deg in ACCENT_TURNS:
        h2 = (h + deg / 360) % 1.0
        if hue_gap(h2, type_hue) < 40 / 360:
            h2 = (type_hue + 0.5) % 1.0                 # gbasprite.shift_off: off the type, to the far side
        n = tuple(int(round(x * 255)) for x in colorsys.hsv_to_rgb(h2, s, v))
        if all(de(n, r) >= FLOOR for r in shiny_ramp[:3]):
            return n
    return tuple(int(round(x * 255)) for x in colorsys.hsv_to_rgb((h + ACCENT_TURNS[0] / 360) % 1.0, s, v))


def type_of(pal):
    for t, c in TYPE_COLOR.items():
        if tuple(pal[3]) == c and [tuple(x) for x in pal[1:5]] == ramp5(*c):
            return t
    return None


def pale(t):
    return t in PALE_NAMED or anchor(t)[0] < PALE_BELOW


def _tint(t, i, smid):
    """Step I (0 highlight, 1 light) of type T's ramp, at its own lightness, in the ANCHOR'S hue, tinted toward
    TINT_TARGET but never more coloured than the shiny mid itself.

    WHY NOT THE ANCHOR'S RULE. The light ends of all the ramps sit within 5-8 CIE76 of each other (LEGACY's highlight
    is 5.1 from LOGIC's, SWARM's 5.1 from GROWTH's) -- near white is near white -- so "nearer its own type's step
    than any other's by MARGIN" admits no tint at all. The bound is carried instead by the two things already proven
    inside the type: the HUE is the anchor's, which passed rule 2 on the mid tone, and the CHROMA is capped at the
    anchor's own, so a highlight is never more of a colour than the body it lights."""
    n = ramp5(*TYPE_COLOR[t])[i]
    Ln = lab(n)
    L, A, B = lab(smid)
    hue, cmax = math.atan2(B, A), math.hypot(A, B)
    best, best_score = n, None
    for dl in (0.0, -1.5, 1.5):
        #  from the step's own chroma up: a tint adds colour, it never drains it (SWARM's light step went grey without this)
        for c10 in range(int(math.hypot(Ln[1], Ln[2]) * 10), int(cmax * 10) + 1, 2):
            c = c10 / 10
            cand = rgb_from_lab(Ln[0] + dl, c * math.cos(hue), c * math.sin(hue))
            if cand is None:
                continue
            score = (round(abs(de(cand, n) - TINT_TARGET), 1), abs(dl), c)
            if best_score is None or score < best_score:
                best, best_score = cand, score
    return best


_RAMPS = {}


def shiny_ramp(t, tell=True):
    """Type T's four shiny tones: ramp5 of the anchor, and for a pale type the light end tinted (above)."""
    key = (t, tell)
    if key not in _RAMPS:
        smid = anchor(t)[2]
        r = ramp5(*smid)
        if tell and pale(t):
            r[0], r[1] = _tint(t, 0, smid), _tint(t, 1, smid)
        _RAMPS[key] = r
    return _RAMPS[key]


def make_shiny(pal, tell=True):
    """(type, the shiny palette) -- or (None, None) when palette 1..4 is no type's ramp: then the daemon's shiny is
    not this tool's (UNOWN, the NEXUS daemons) and is left as it is."""
    t = type_of(pal)
    if t is None:
        return None, None
    _, _, smid = anchor(t)
    sramp = shiny_ramp(t, tell)
    out = list(pal)
    out[1:5] = sramp
    th = hsv(smid)[0]
    for i in range(6, min(STREAK_FIRST, len(pal))):
        out[i] = turn_accent(tuple(pal[i]), sramp, th)
    return t, out


# ---------------------------------------------------------------------------------------------------- the census
def species_info():
    """{folder: (SPECIES_X, name the player reads, (type1, type2))} from the engine's own tables."""
    info = open(os.path.join(GBA, "src", "data", "pokemon", "species_info.h"), encoding="utf-8").read()
    types = dict((k, (a, b)) for k, a, b in
                 re.findall(r"\[SPECIES_(\w+)\]\s*=.*?\.types = \{TYPE_(\w+),\s*TYPE_(\w+)\}", info, re.S))
    names = dict(re.findall(r'\[SPECIES_(\w+)\]\s*= _\("(.*?)"\)',
                            open(os.path.join(GBA, "src", "data", "text", "species_names.h"), encoding="utf-8").read()))
    return types, names


def census(only):
    types, names = species_info()
    rows, skipped = [], []
    for d in sorted(os.listdir(MON)):
        p = os.path.join(MON, d)
        if only and d not in only:
            continue
        if not (os.path.isfile(os.path.join(p, "normal.pal")) and os.path.isfile(os.path.join(p, "shiny.pal"))):
            continue
        normal = daemonslib.read_pal(os.path.join(p, "normal.pal"))
        shiny = daemonslib.read_pal(os.path.join(p, "shiny.pal"))
        #  OWNERSHIP: genshiny owns every shiny.pal whose normal.pal is a type ramp, and no other. A daemon without one
        #  (UNOWN, the eight NEXUS daemons) keeps the shiny it has -- the user, 2026-10-21.
        t, new = make_shiny(normal)
        if t is None:
            skipped.append((d, "not a type ramp: keeps its own shiny.pal"))
            continue
        sp = d.upper()
        rows.append(dict(dir=d, name=names.get(sp, d.upper()), type=t, types=types.get(sp),
                         normal=normal, shiny=new, current=shiny, plain=make_shiny(normal, tell=False)[1]))
    return rows, skipped


# ------------------------------------------------------------------------------------------------------ the sheets
def _font(size):
    from PIL import ImageFont
    for f in ("/System/Library/Fonts/Menlo.ttc", "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"):
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


PAPER, TEXT, RULE = (238, 236, 228), (30, 30, 34), (180, 178, 170)


def sprite(d, pal, scale):
    """The front sprite, decoded through PAL (its own pixel indices, nothing re-quantised), index 0 transparent."""
    from PIL import Image
    im = Image.open(os.path.join(MON, d, "front.png"))
    w, h = im.size
    idx = list(im.getdata())
    rgba = Image.new("RGBA", (w, h))
    rgba.putdata([(0, 0, 0, 0) if i == 0 else tuple(pal[i % 16]) + (255,) for i in idx])
    return rgba.resize((w * scale, h * scale), Image.NEAREST)


def swatches(draw, x, y, cols, s=14):
    for i, c in enumerate(cols):
        draw.rectangle([x + i * s, y, x + i * s + s - 1, y + s - 1], fill=tuple(c), outline=RULE)


def type_label(t):
    return "%s (%s)" % (OURS.get(t, t), t)


ORDER = list(TYPE_COLOR)


def draw_sheets(rows, out, per=40, cols=4, scale=2):
    from PIL import Image, ImageDraw
    groups = {}
    for r in rows:
        groups.setdefault(r["type"], []).append(r)
    for g in groups.values():
        g.sort(key=lambda r: r["name"])
    #  pack whole types onto pages, splitting a type only when it alone is longer than a page
    pages, cur = [], []
    for t in ORDER:
        g = groups.get(t, [])
        while g:
            room = per - sum(len(x[1]) for x in cur)
            if room <= 0 or (len(g) > room and room < 12 and cur):
                pages.append(cur); cur = []; continue
            cur.append((t, g[:room])); g = g[room:]
    if cur:
        pages.append(cur)
    f_big, f_small, f_name = _font(26), _font(15), _font(17)
    cell_w, cell_h = 64 * scale * 2 + 24, 64 * scale + 30
    W = cols * cell_w + 40
    base, ext = os.path.splitext(out)
    paths = []
    for n, page in enumerate(pages, 1):
        H = 70
        for t, g in page:
            H += 54 + ((len(g) + cols - 1) // cols) * cell_h + 10
        im = Image.new("RGB", (W, H), PAPER)
        dr = ImageDraw.Draw(im)
        dr.text((20, 18), "T-432 shiny palettes -- sheet %d of %d  (left normal, right shiny)" % (n, len(pages)),
                font=f_big, fill=TEXT)
        y = 70
        for t, g in page:
            sh, dh, smid = anchor(t)
            dr.line([20, y, W - 20, y], fill=RULE, width=2)
            dr.text((20, y + 10), type_label(t), font=f_big, fill=TEXT)
            sx = 20 + int(dr.textlength(type_label(t), font=f_big)) + 24
            swatches(dr, sx, y + 14, ramp5(*TYPE_COLOR[t]), 18)
            dr.text((sx + 80, y + 12), "->", font=f_name, fill=TEXT)
            swatches(dr, sx + 108, y + 14, shiny_ramp(t), 18)
            dr.text((sx + 196, y + 15), "hue %+d deg, dE %.0f%s" % (dh, sh, ", light end tinted" if pale(t) else ""),
                    font=f_small, fill=TEXT)
            y += 54
            for i, r in enumerate(g):
                cx, cy = 20 + (i % cols) * cell_w, y + (i // cols) * cell_h
                im.paste(sprite(r["dir"], r["normal"], scale), (cx, cy), sprite(r["dir"], r["normal"], scale))
                s = sprite(r["dir"], r["shiny"], scale)
                im.paste(s, (cx + 64 * scale + 4, cy), s)
                label = r["name"]
                if r["types"] and r["types"][1] != r["types"][0]:
                    label += " /" + OURS.get(r["types"][1], r["types"][1])
                dr.text((cx + 4, cy + 64 * scale + 4), label, font=f_name, fill=TEXT)
            y += ((len(g) + cols - 1) // cols) * cell_h + 10
        p = "%s_%d%s" % (base, n, ext or ".png")
        im.save(p)
        paths.append(p)
    return paths


def draw_overview(rows, out, scale=2):
    """One daemon per type, its ramp and its shiny ramp: the whole rule on one page."""
    from PIL import Image, ImageDraw
    pick = {}
    for r in sorted(rows, key=lambda r: (r["types"] is not None and r["types"][0] != r["types"][1], r["name"])):
        pick.setdefault(r["type"], r)
    ts = [t for t in ORDER if t in pick]
    cols = 3
    cw, ch = 64 * scale * 2 + 60, 64 * scale + 92
    W, H = cols * cw + 40, 80 + ((len(ts) + cols - 1) // cols) * ch
    im = Image.new("RGB", (W, H), PAPER)
    dr = ImageDraw.Draw(im)
    f_big, f_name, f_small = _font(26), _font(18), _font(14)
    dr.text((20, 20), "T-432 shiny -- one per type (left normal, right shiny)", font=f_big, fill=TEXT)
    for i, t in enumerate(ts):
        r = pick[t]
        cx, cy = 20 + (i % cols) * cw, 80 + (i // cols) * ch
        sh, dh, smid = anchor(t)
        dr.text((cx, cy), "%s  %s" % (OURS.get(t, t), r["name"]), font=f_name, fill=TEXT)
        swatches(dr, cx, cy + 26, ramp5(*TYPE_COLOR[t]), 14)
        swatches(dr, cx + 64 * scale + 4, cy + 26, shiny_ramp(t), 14)
        dr.text((cx + 64 * scale + 64, cy + 26), "%+d deg dE %.0f%s" % (dh, sh, " +tint" if pale(t) else ""),
                font=f_small, fill=TEXT)
        a = sprite(r["dir"], r["normal"], scale)
        b = sprite(r["dir"], r["shiny"], scale)
        im.paste(a, (cx, cy + 46), a)
        im.paste(b, (cx + 64 * scale + 4, cy + 46), b)
    im.save(out)
    return out


def draw_pale(rows, out, per_type=4, scale=2):
    """The pale types before and after the stronger tell: normal, the shiny without it, the shiny with it. Daemons with
    no accent to turn come first -- they are the ones the tell is for."""
    from PIL import Image, ImageDraw
    ts = [t for t in ORDER if pale(t)]
    cw, ch = 64 * scale * 3 + 40, 64 * scale + 34
    W = 2 * cw + 40
    picks = {}
    for t in ts:
        g = sorted((r for r in rows if r["type"] == t),
                   key=lambda r: (r["shiny"][6:STREAK_FIRST] != r["normal"][6:STREAK_FIRST], r["name"]))
        picks[t] = g[:per_type]
    H = 80 + sum(60 + ((len(picks[t]) + 1) // 2) * ch for t in ts)
    im = Image.new("RGB", (W, H), PAPER)
    dr = ImageDraw.Draw(im)
    f_big, f_name, f_small = _font(26), _font(17), _font(15)
    dr.text((20, 20), "T-432 pale types: normal | before | with tint", font=f_big, fill=TEXT)
    y = 80
    for t in ts:
        dr.line([20, y, W - 20, y], fill=RULE, width=2)
        dr.text((20, y + 10), type_label(t), font=f_big, fill=TEXT)
        sx = 20 + int(dr.textlength(type_label(t), font=f_big)) + 24
        swatches(dr, sx, y + 14, ramp5(*TYPE_COLOR[t]), 18)
        swatches(dr, sx + 90, y + 14, shiny_ramp(t, tell=False), 18)
        swatches(dr, sx + 180, y + 14, shiny_ramp(t), 18)
        y += 60
        for i, r in enumerate(picks[t]):
            cx, cy = 20 + (i % 2) * cw, y + (i // 2) * ch
            for k, pal in enumerate((r["normal"], r["plain"], r["shiny"])):
                sp = sprite(r["dir"], pal, scale)
                im.paste(sp, (cx + k * (64 * scale + 6), cy), sp)
            dr.text((cx + 4, cy + 64 * scale + 4), r["name"], font=f_name, fill=TEXT)
        y += ((len(picks[t]) + 1) // 2) * ch
    im.save(out)
    return out


# ---------------------------------------------------------------------------------------------------------- report
def main():
    args = sys.argv[1:]
    sheet = None
    if "--sheet" in args:
        sheet = args[args.index("--sheet") + 1]
    only = {a for i, a in enumerate(args) if not a.startswith("--") and (i == 0 or args[i - 1] != "--sheet")}
    rows, skipped = census(only)

    print("  THE SHINY ANCHORS -- one per type; the mid tone moved, the ramp rebuilt from it")
    print("  %-22s %-15s %-15s %6s %6s  %s" % ("type", "normal mid", "shiny mid", "turn", "dE", "nearest other (dE)"))
    for t in ORDER:
        sh, dh, smid = anchor(t)
        o, od = nearest_other(t, smid)
        o0, od0 = nearest_other(t, TYPE_COLOR[t])
        print("  %-22s %-15s %-15s %+5dd %6.1f  %s %.1f (was %s %.1f)"
              % (type_label(t), "%d,%d,%d" % TYPE_COLOR[t], "%d,%d,%d" % smid, dh, sh,
                 OURS.get(o, o), od, OURS.get(o0, o0), od0))
        dl = max(abs(lab(a)[0] - lab(b)[0]) for a, b in zip(ramp5(*TYPE_COLOR[t]), ramp5(*smid)))
        if dl > 6:
            print("      !! the ramp's lightness moves %.1f L* at one step" % dl)

    print("\n  THE PALE TYPES' TELL -- the light end tinted (highlight, light: normal -> shiny, dE)")
    for t in ORDER:
        if pale(t):
            n, sr = ramp5(*TYPE_COLOR[t]), shiny_ramp(t)
            print("  %-22s %s" % (type_label(t), "   ".join("%d,%d,%d -> %d,%d,%d (%.1f)" % (n[i] + sr[i] + (de(n[i], sr[i]),))
                                                              for i in (0, 1))))
    change = [r for r in rows if r["shiny"] != r["current"]]
    print("\n  %d daemons, %d of them would change; %d skipped" % (len(rows), len(change), len(skipped)))
    for d, why in skipped:
        print("     skip %-18s %s" % (d, why))
    weak = [t for t in ORDER if anchor(t)[0] < 10]
    if weak:
        print("  a shiny under dE 10 from its normal (the chart leaves it little room): %s"
              % ", ".join(OURS.get(t, t) for t in weak))
    mism = [r for r in rows if r["types"] and r["types"][0] != r["type"]]
    if mism:
        print("  %d daemons are coloured by a type that is not their first type in species_info.h:" % len(mism))
        for r in mism:
            print("     %-14s body %-9s species_info %s/%s" % (r["name"], OURS.get(r["type"], r["type"]),
                                                             OURS.get(r["types"][0]), OURS.get(r["types"][1])))
    dual = [r for r in rows if r["types"] and r["types"][1] != r["types"][0]]
    print("  %d dual-typed daemons take their body's (first) type's shiny; the second does not move it" % len(dual))
    noacc = [r for r in rows if r["shiny"][6:STREAK_FIRST] == r["normal"][6:STREAK_FIRST]]
    print("  %d have no accent that turns (all grey, or none): their shiny is the ramp alone" % len(noacc))

    if sheet:
        paths = draw_sheets(rows, sheet)
        ov = draw_overview(rows, os.path.splitext(sheet)[0] + "_overview.png")
        pl = draw_pale(rows, os.path.splitext(sheet)[0] + "_pale.png")
        print("  sheets: %s" % ", ".join(paths + [ov, pl]))

    if WRITE:
        for r in change:
            daemonslib.write_pal(os.path.join(MON, r["dir"], "shiny.pal"), r["shiny"], pad=True)
        print("  wrote %d shiny.pal (make rebuilds the .gbapal; then tools/gbafollowerpal.py --write)" % len(change))
    elif change:
        print("  %d shiny.pal would change -- --write to write them" % len(change))
    return 0


if __name__ == "__main__":
    sys.exit(main())
