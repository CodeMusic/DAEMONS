#!/usr/bin/env python3
"""THE NEXUS: the place between the groves, made entirely of paint (T-395; docs/nexus.md).

    python3 tools/gbanexusmap.py            # report what would change, and a preview of the map in the scratch dir
    python3 tools/gbanexusmap.py --write    # the tileset, the map, its scripts and words, its residents

WHAT IT IS (the user, 2026-10-09, from THE PAINTED MIRROR). With the band's sheet, any singing fir -- the S.S.
ANNE's, or the one now standing in every grove -- is a door, and through it is THE NEXUS: night, a meadow of paint,
and the light coming from the creatures and the music. Its trees are doors to the groves: a grove the player has been
in is an ordinary painted tree, and through it the player arrives in that grove beside its fir; a grove not yet found
is a grey tree, and the harder the player tries it, the less real it becomes -- smudged, then only dots and lines
(redrawn in place, and whole again on the next visit). One Christmas tree stands among them, the way home to the
S.S. ANNE's pier. Leaving by any door, the GUARDIAN OF THE NEXUS speaks, a voice and never seen, a different line at
each. THE (NOT A) HUNTER stands in the meadow, a bear in red plaid (tools/genhunter.py). PHOENIX waits once in the
paint; the eight residents (tools/gbanexus.py) and PENGUIN live in the meadow.

THE ART. Every surface is drawn on spriteforge (roverbyteseer by name) and cleaned here; ART names the drafts, each
with its seed and prompt beside it in gfx/drafts/nexus/env/. Textures are cropped, scaled so a brushstroke survives
at sixteen pixels a cell, made seamless (the offset-and-blend trick), and quantised to fifteen colours; the trees are
cut-outs, fitted to their cells and laid on the painted ground on the middle layer. The grey door's three states are
the ordinary tree's own pixels, greyed, smudged and reduced to lines, so the four read as one tree.

THE TILESET. gTileset_Nexus, a secondary over gTileset_General (whose metatiles the map never uses). Six palettes,
7..12: ground, meadow, the wall of trees, the tree, the grey tree's three states, the Christmas tree. Every metatile is
COVERED (both layers beneath the sprites), so a tree never draws over the player's head. The meadow carries
TILE_ENCOUNTER_LAND with an ordinary behaviour: encounters, and no grass-rustle sprite drawn in another tileset's
green. MAP_TYPE_UNDERGROUND, so the day's light never tints a place that is always night.

THE WORDS: the GUARDIAN's fifteen lines (the source's, cut to the box) and the bear's (close to it, his precious ones
DAEMONS) were APPROVED by the user, 2026-10-10 -- and then the rest: the fir's remark, the door and tree prompts, the
music, PHOENIX's level and the meadow's residents. Nothing in THE NEXUS is a draft now.
"""
import importlib.util, json, os, re, struct, sys
from PIL import Image, ImageFilter, ImageOps, ImageEnhance

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv
SCRATCH = os.environ.get("DAEMONS_SCRATCH", os.path.join(ROOT, ".theatre"))
DRAFTS = os.path.join(ROOT, "gfx/drafts/nexus/env")
SAVED = os.path.join(ROOT, "gfx/nexus/env")              # the cleaned pieces, as the game draws them
NAME, MAPC, LAYOUT = "Nexus", "MAP_NEXUS", "LAYOUT_NEXUS"
TILESET, TSDIR = "gTileset_Nexus", "nexus"


def _load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, "tools", name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


grove = _load("gbagrove")
_src = open(os.path.join(ROOT, "tools/port_vocab.py"), encoding="utf-8").read()
_ns = {"__name__": "port_vocab_font", "__file__": os.path.join(ROOT, "tools/port_vocab.py")}
exec(compile(_src.split("# ------------------------------------------------------- names, derived")[0], "port_vocab.py", "exec"), _ns)
textwidth = _ns["textwidth"]

# ---------------------------------------------------------------------------------------------------------- the art
#  (draft, crop box as fractions of the draft, the size it is scaled to before the seamless blend)
ART = {
    "ground": ("calm_12001.png", (0.22, 0.28, 0.66, 0.72), 64),
    "meadow": ("meadow_11003.png", (0.20, 0.20, 0.80, 0.80), 64),
    "wall":   ("wall_11001.png",   (0.25, 0.25, 0.75, 0.75), 48),
    #  The trees: no cut-out model can lift a tree out of a whole painted scene, so each is CROPPED from its draft
    #  and given a drawn silhouette (masked() below): the paint is the draft's, the edge is ours.
    "tree":   ("tree_11004.png", (0.18, 0.10, 0.82, 0.66), "round"),
    "xmas":   ("xmas_11002.png", (0.27, 0.06, 0.73, 0.86), "fir"),
}
PAL = {"ground": 7, "meadow": 8, "wall": 9, "tree": 10, "grey": 11, "xmas": 12}
COVERED = 1 << 29
LAND = 1 << 24
COLLIDE = 0x0C00
ELEV = 0x3000

# ----------------------------------------------------------------------------------------------------------- the map
W, H = 26, 23
CHRISTMAS = (12, 2)                                       # 2 wide, 3 tall
ARRIVE = (12, 5)                                          # in front of it, from any fir
MEADOW = [(10, 8, 15, 12), (10, 16, 15, 19)]
#  The wall of trees comes in here and there, so the clearing is not a box -- never on a door, its foot or the way in.
BUMPS = [(2, 2), (2, 6), (2, 7), (2, 11), (2, 12), (2, 16), (2, 17), (2, 20), (3, 20),
         (23, 2), (23, 6), (23, 7), (23, 11), (23, 12), (23, 16), (23, 17), (23, 20), (22, 20),
         (5, 2), (6, 2), (9, 2), (16, 2), (19, 2), (20, 2), (8, 20), (9, 20), (15, 20), (16, 20)]
WALL_LIGHT = 0.72                                         # the leaves, darkened for a place that is always night
#  The doors: the mainland's seven on the left, the islands' on the right (each world hides the other half), a 2x2
#  tree whose foot answers A from the cell below. Rows of gbagrove.GROVES by name, and where each tree stands.
DOORS = [
    ("Route1_Grove", (3, 3)), ("ViridianForest_Grove", (7, 5)), ("Route24_Grove", (3, 8)), ("Route25_Grove", (7, 10)),
    ("Route11_Grove", (3, 13)), ("Route8_Grove", (7, 15)), ("Route13_Grove", (4, 18)),
    ("OneIsland_Grove", (21, 3)), ("TwoIsland_Grove", (17, 5)), ("ThreeIsland_BerryForest_Grove", (21, 8)),
    ("FourIsland_Grove", (17, 10)), ("FiveIsland_Meadow_Grove", (21, 13)), ("SixIsland_WaterPath_Grove", (17, 15)),
    ("SevenIsland_Grove", (20, 18)),
]
#  T-408 (the user, 2026-10-16, from The Painted Mirror, where each NEXUS door was its own universe): every grove is a
#  universe, and a sign stands beside its door -- readable before you have been, its words a hint to where the door is.
#  Names and words approved by the user, 2026-10-16. The sign is the game's own sign object: no tile is spent (the
#  tileset is at 1006 of 1024), one shared picture. It stands on the clearing's side of the door, a row below its crown.
UNIVERSES = {
    "ViridianForest_Grove": ("THE BACKDROPVERSE", "Where everyone walks past first,\none tree is not part of the forest."),
    "Route1_Grove": ("THE PULSEVERSE", "Before you knew the way, your feet\nknew the first road out of town."),
    "Route24_Grove": ("THE INWARDVERSE", "Past the bridge everyone dares,\nthe one who stops to look inside."),
    "Route25_Grove": ("THE EMPATHVERSE", "On the long road to the far cottage,\na bush stands where no one asked it."),
    "Route11_Grove": ("THE DRIFTVERSE", "East of the harbour, a tree is\nresting where the road forgot it."),
    "Route8_Grove": ("THE HAZEVERSE", "Between two towns, a little before\nthe tower, something is fading."),
    "Route13_Grove": ("THE HUSHVERSE", "In the copse by the fences, one\ncorner tree has not said a word."),
    "OneIsland_Grove": ("THE SEEDVERSE", "On the first island, one bush is\nholding a value nobody can see."),
    "TwoIsland_Grove": ("THE WEATHERVERSE", "On the second island, a tree is\nwaiting to see what the sky does."),
    "ThreeIsland_BerryForest_Grove": ("THE HUNGERVERSE", "In the third island's berries,\nsomething has eaten all the paths."),
    "FourIsland_Grove": ("THE HUSKVERSE", "On the cold fourth island, a tree\nhas left its old shell behind."),
    "FiveIsland_Meadow_Grove": ("THE MECHAVERSE", "In the fifth island's meadow, four\nminds are learning to be one."),
    "SixIsland_WaterPath_Grove": ("THE COMPASSVERSE", "Along the sixth island's water,\na rock points the same way always."),
    "SevenIsland_Grove": ("THE CLAYVERSE", "At the end of the seventh island,\na bush hides a figure of clay."),
}


def sign_at(x, y):
    """Beside a door's 2x2 crown at (x, y): right of it on the mainland's (left) side, left of it on the islands'."""
    return (x + 2, y + 1) if x < W // 2 else (x - 1, y + 1)


HUNTER = (12, 14)
PHOENIX = (12, 10)
PIER = ("MAP_SSANNE_EXTERIOR", 57, 27)                    # beside the pier's fir, on the strip north of it
MUSIC = "MUS_NEXUS"         # T-409 (DRAFT): its own, on the fir's notes (tools/gennexustheme.py); was MUS_SLOW_PALLET

# ------------------------------------------------------------------------- the words (approved by the user, 2026-10-10)
#  The GUARDIAN OF THE NEXUS, a voice, never seen: the source's own lines, one at each door, cut to the box. APPROVED by
#  the user, 2026-10-10, as were the bear's words below.
VOICE = "A voice carries across the paint."
GUARDIAN_HOME = "“Those notes were never flat.\nThey were only misunderstood.\\pYou may return home.”"
GUARDIAN = [
    "“Remember what you have learned!”",
    "“The door was always there.\nYou just could not see it.”",
    "“Just because you cannot see it\ndoes not mean you can't believe it.”",
    "“You have passed more tests\nthan you realize.”",
    "“Perhaps now is the time to gaze\nbeyond your reflection.”",
    "“What you hold is more than a mirror.\nIt is also a window.”",
    "“You still have more work\nin front of you.”",
    "“This world belongs to everyone.\nShow you care, and do not run.”",
    "“Every universe has a mirror.\\pYour heart alongside your head\nwill be your compass.”",
    "“Enter from a place of love,\notherwise you will not arrive\\lwhere you expect.”",
    "“Everything exists in a duality.”",
    "“You were never lost…”",
    "“Believe in yourself,\nand use your senses.”",
    "“Shed those fears, and ask them now.\nI promise it will mean a ton.”",
]
TEXT = {
    #  the fir, everywhere
    "Text_SingingFir_Hums": "The fir's branches stir.\nIt hums an old tune.",
    "Text_SingingFir_Off": "Close to right, all the way\nthrough. Something is missing.\\p"
                           "And the fir looks faded, like\na painting left in the sun.",
    "Text_SingingFir_HoldUpSheet": "{PLAYER} held up the band's sheet.\\pThe fir hums the tune again.",
    "Text_SingingFir_Right": "The same notes.\nThis time, every one is home.",
    "Text_SingingFir_Door": "The branches part, like a door.\nGo through?",
    "Text_SingingFir_FirstTime": "On the other side, everything\nis made of paint.",
    #  the NEXUS
    "Nexus_Text_Voice": VOICE,
    "Nexus_Text_DoorOpen": "This tree stands open, like a door.\nGo through?",
    "Nexus_Text_Locked1": "The door won't open.\\pThe harder {PLAYER} tries,\nthe less real it becomes…",
    "Nexus_Text_Locked2": "…until it is only\ndots and lines.",
    "Nexus_Text_Locked3": "Only a drawing of a tree.",
    "Nexus_Text_Christmas": "The tree glows a different colour\nwith every note.\\pGo home?",
    "Nexus_Text_GuardianHome": GUARDIAN_HOME,
    "Nexus_Text_HunterFirst": "Red plaid, in the dark.\nA hunter?\\p"
                              "Hunter? I'm no hunter…\nnot anymore.\\p"
                              "And frankly, I never was\nto begin with.\\p"
                              "How could anyone hurt these\nDAEMONS? They are precious.\\p"
                              "…Now why would you turn back?\nWhy would my tone make you buckle?\\p"
                              "Charm must be balanced with\nfirmness, or you are only\\lspeaking in mirages.\\p"
                              "And keep faith. Don't let walls\nbe placed where doors should be.",
    "Nexus_Text_Hunter": "These DAEMONS are precious.\nMind how you walk among them.",
    "Nexus_Text_HunterAll": "Every door here is open to you now.\nThey always were.",
    "Nexus_Text_Phoenix": "Its cry rings out, and the shadows\nin the paint come clear!",
}
TEXT.update({"Nexus_Text_Guardian%d" % k: g for k, g in enumerate(GUARDIAN)})
TEXT.update({"Nexus_Text_Sign%d" % k: "%s\\p%s" % UNIVERSES[name] for k, (name, _) in enumerate(DOORS)})   # T-408
BOX = 208


def check_words():
    """Every line of every box within the box's 208px ({PLAYER} counted at seven wide letters)."""
    bad = []
    for label, t in TEXT.items():
        for line in re.split(r"\n|\\p|\\l", t):
            if textwidth(line) > BOX:
                bad.append("%s: %r is %dpx" % (label, line, textwidth(line)))
    return bad


def gba_string(t):
    """A text as .string lines: a newline is the engine's \\n; \\p and \\l stay as written."""
    out, cur = [], ""
    for p in re.split(r"(\n|\\p|\\l)", t):
        cur += "\\n" if p == "\n" else p
        if p in ("\n", "\\p", "\\l"):
            out.append(cur)
            cur = ""
    out.append(cur + "$")
    return "".join('    .string "%s"\n' % x for x in out if x)


# ------------------------------------------------------------------------------------------------ the art, cleaned
def seamless(img):
    """The offset-and-blend: edges from the half-rolled copy (continuous across the wrap), the middle from itself."""
    w, h = img.size
    rolled = Image.new("RGB", (w, h))
    rolled.paste(img.crop((w // 2, h // 2, w, h)), (0, 0))
    rolled.paste(img.crop((0, h // 2, w // 2, h)), (w - w // 2, 0))
    rolled.paste(img.crop((w // 2, 0, w, h // 2)), (0, h - h // 2))
    rolled.paste(img.crop((0, 0, w // 2, h // 2)), (w - w // 2, h - h // 2))
    mask = Image.new("L", (w, h))
    mp = mask.load()
    for y in range(h):
        for x in range(w):
            d = min(x, y, w - 1 - x, h - 1 - y) / (w / 4.0)
            mp[x, y] = int(255 * max(0.0, min(1.0, d)))
    return Image.composite(img, rolled, mask)


def texture(key):
    f, (a, b, c, d), size = ART[key]
    im = Image.open(os.path.join(DRAFTS, f)).convert("RGB")
    W0, H0 = im.size
    im = im.crop((int(a * W0), int(b * H0), int(c * W0), int(d * H0))).resize((size, size), Image.LANCZOS)
    return seamless(im)


def cutout(name, w, h):
    """A cut-out (RGBA), fitted into w x h with its foot on the bottom row; alpha is all or nothing."""
    im = Image.open(os.path.join(DRAFTS, name)).convert("RGBA")
    box = im.getchannel("A").point(lambda v: 255 if v > 96 else 0).getbbox()
    im = im.crop(box)
    s = min(w / im.width, h / im.height)
    im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    out = Image.new("RGBA", (w, h))
    out.paste(im, ((w - im.width) // 2, h - im.height), im)
    a = out.getchannel("A").point(lambda v: 255 if v > 128 else 0)
    out.putalpha(a)
    return out


def silhouette(shape, w, h):
    """The drawn edge: a round canopy on a short trunk, or a tiered fir with its star. A little ragged, as paint is."""
    import math, random
    rnd = random.Random(395)
    m = Image.new("L", (w, h))
    mp = m.load()
    if shape == "round":
        cx, cy, rx, ry = w / 2 - 0.5, h * 0.42, w * 0.47, h * 0.40
        wob = [1 + 0.07 * math.sin(k * 1.7) + rnd.uniform(-0.05, 0.05) for k in range(24)]
        for y in range(h):
            for x in range(w):
                a = (math.atan2(y - cy, x - cx) + math.pi) / (2 * math.pi) * 24
                r = wob[int(a) % 24]
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= r * r:
                    mp[x, y] = 255
        for y in range(int(h * 0.74), h):
            for x in range(w // 2 - 2, w // 2 + 2):
                mp[x, y] = 128                           # the trunk: drawn, not the draft's
    else:
        tiers = [(5, 16, 1, 6), (13, 28, 3, 10), (24, h - 6, 5, 15)]   # (top, bottom, half-width at top, at bottom)
        for top, bot, w0, w1 in tiers:
            for y in range(top, bot + 1):
                half = w0 + (w1 - w0) * (y - top) / max(1, bot - top) + rnd.uniform(-0.6, 0.6)
                for x in range(w):
                    if abs(x - (w / 2 - 0.5)) <= half:
                        mp[x, y] = 255
        for y in range(0, 6):                            # the star
            for x in range(w):
                if abs(x - (w / 2 - 0.5)) <= (2.5 - abs(y - 2.5) * 0.6):
                    mp[x, y] = 255
        for y in range(h - 6, h):
            for x in range(w // 2 - 2, w // 2 + 2):
                mp[x, y] = 128
    return m


def masked(key, w, h):
    """A tree for the game: the draft's paint, cropped and scaled, inside its silhouette; the trunk a painted brown."""
    f, (a, b, c, d), shape = ART[key]
    im = Image.open(os.path.join(DRAFTS, f)).convert("RGB")
    W0, H0 = im.size
    im = im.crop((int(a * W0), int(b * H0), int(c * W0), int(d * H0))).resize((w, h), Image.LANCZOS)
    m = silhouette(shape, w, h)
    out = Image.new("RGBA", (w, h))
    ip, op, mp = im.load(), out.load(), m.load()
    for y in range(h):
        for x in range(w):
            if mp[x, y] == 255:
                op[x, y] = ip[x, y] + (255,)
            elif mp[x, y] == 128:
                op[x, y] = (92, 58, 40, 255) if x % 2 else (66, 40, 30, 255)
    return out


def grey_states(tree):
    """The door not yet found: the tree greyed; smudged; then only dots and lines."""
    a = tree.getchannel("A")
    rgb = tree.convert("RGB")
    grey = ImageEnhance.Contrast(ImageEnhance.Color(rgb).enhance(0.12)).enhance(0.7)
    grey = ImageEnhance.Brightness(grey).enhance(0.85)
    g1 = grey.copy()
    g1.putalpha(a)
    smear = grey.filter(ImageFilter.GaussianBlur(1.3))
    sa = a.filter(ImageFilter.GaussianBlur(1.0)).point(lambda v: 255 if v > 150 else 0)
    g2 = smear.copy()
    g2.putalpha(sa)
    edges = ImageOps.grayscale(rgb).filter(ImageFilter.FIND_EDGES)
    outline = a.filter(ImageFilter.FIND_EDGES)
    lines = Image.new("RGBA", tree.size)
    lp, ep, op, ap = lines.load(), edges.load(), outline.load(), a.load()
    for y in range(tree.height):
        for x in range(tree.width):
            if ap[x, y] and (op[x, y] > 60 or (ep[x, y] > 70 and (x + y) % 2 == 0)):
                lp[x, y] = (176, 176, 190, 255)            # pale, like pencil on the dark
    return g1, g2, lines


def quantise(images, colours=15):
    """Fifteen colours shared by IMAGES (RGB or RGBA), index 0 kept for transparency. Returns (palette, [P images])."""
    strip = Image.new("RGB", (sum(i.width for i in images), max(i.height for i in images)))
    x = 0
    for i in images:
        rgb = i.convert("RGB")
        if i.mode == "RGBA":                        # transparent pixels must not pull the palette
            bg = Image.new("RGB", i.size, rgb.getpixel((0, 0)))
            src = [p for p, al in zip(rgb.getdata(), i.getchannel("A").getdata()) if al]
            if src:
                bg = Image.new("RGB", i.size, src[0])
            rgb = Image.composite(rgb, bg, i.getchannel("A"))
        strip.paste(rgb, (x, 0))
        x += i.width
    q = strip.quantize(colors=colours, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    pal = q.getpalette()[:colours * 3]
    pal = [tuple(c >> 3 << 3 for c in pal[k * 3:k * 3 + 3]) for k in range(colours)]
    out = []
    for i in images:
        rgb = i.convert("RGB")
        p = Image.new("P", i.size)
        pp = p.load()
        rp = rgb.load()
        ap = i.getchannel("A").load() if i.mode == "RGBA" else None
        for y in range(i.height):
            for xx in range(i.width):
                if ap is not None and not ap[xx, y]:
                    pp[xx, y] = 0
                    continue
                r, g, b = rp[xx, y]
                pp[xx, y] = 1 + min(range(colours), key=lambda k: (pal[k][0] - r) ** 2 + (pal[k][1] - g) ** 2 + (pal[k][2] - b) ** 2)
        out.append(p)
    return [(0, 0, 0)] + pal, out


# ---------------------------------------------------------------------------------------- the landscape, painted whole
#  (the user, 2026-10-10: "review how the landscape looks so it doesn't look jagged"). Cell by cell, the clearing was a
#  box with square notches and the meadows two rectangles. Now it is ONE PICTURE at the game's own size -- the paint
#  textures laid down under soft masks: a clearing whose edge wanders like a brushstroke, a shadow pooled inside it,
#  meadows with ragged edges, a shadow under every door, light around the Christmas tree -- and the picture is cut into
#  tiles afterwards. The tiles share ten painted palettes, and a tile that matches another (flipped or not) is drawn
#  once. That needs more than one secondary tileset holds, so THE NEXUS has its own primary too (gTileset_NexusPaint,
#  as interiors have gTileset_Building): 1024 tiles and 13 palettes between the two.
import numpy as np
from scipy.cluster.vq import kmeans2

PRIMARY, PDIR = "gTileset_NexusPaint", "nexus_paint"
CLEAR = (1.55, 1.30, W - 1.55, H - 1.30)                # the clearing's box, in cells, before its edge wanders
CORNER = 4.6                                              # its corners' radius, in cells
WOBBLE, BRUSH = 7.0, 2.4                                  # how far the edge wanders, and its brushstroke ragged
SHADOW, SHADOW_W = 0.42, 18.0                             # the shade pooled inside the edge, and how far in it reaches
MEADOWS = [(13.0, 10.4, 3.9, 2.9), (13.0, 17.8, 3.8, 2.3)]   # centre and radii, in cells
GLOW = (13.0, 3.6, 3.0, None, 0.16)                      # the Christmas tree's light: centre, radius, -, strength
GROUND_WHOLE = (40, 60, 1000, 900)                        # the floor: this much of its draft, over the whole map
DITHER = 14.0                                             # its strength, in 8-bit steps
LAND_PALS = 10                                            # palettes 0..9 for the landscape; 10..12 the trees
TREE_PAL = {"tree": 10, "grey": 11, "xmas": 12}


def smooth_noise(h, w, cell, seed):
    """Smooth value noise in -0.5..0.5, its features about CELL pixels across."""
    rng = np.random.default_rng(seed)
    gh, gw = h // cell + 3, w // cell + 3
    g = Image.fromarray((rng.random((gh, gw)) * 255).astype(np.uint8))
    return np.asarray(g.resize((gw * cell, gh * cell), Image.BICUBIC), float)[:h, :w] / 255.0 - 0.5


def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def landscape():
    """(RGB float image, wall alpha, meadow alpha) for the whole map, W*16 x H*16."""
    ph, pw = H * 16, W * 16
    yy, xx = np.mgrid[0:ph, 0:pw].astype(float)
    tex = {k: np.asarray(texture(k), float) for k in ("ground", "meadow", "wall")}
    tex["wall"] = tex["wall"] * WALL_LIGHT
    tile = lambda t: np.tile(t, (ph // t.shape[0] + 1, pw // t.shape[1] + 1, 1))[:ph, :pw]
    #  The floor is one painting laid over the whole clearing, never repeated -- a repeat drew a grid of its streaks.
    f, (a, b, c, d), _ = ART["ground"]
    gimg = Image.open(os.path.join(DRAFTS, f)).convert("RGB")
    G = np.asarray(gimg.crop(GROUND_WHOLE).resize((pw, ph), Image.LANCZOS), float)
    M, L = tile(tex["meadow"]), tile(tex["wall"])
    x0, y0, x1, y1 = (v * 16 for v in CLEAR)
    r = CORNER * 16
    qx = np.abs(xx - (x0 + x1) / 2) - ((x1 - x0) / 2 - r)
    qy = np.abs(yy - (y0 + y1) / 2) - ((y1 - y0) / 2 - r)
    inside = -(np.hypot(np.maximum(qx, 0), np.maximum(qy, 0)) + np.minimum(np.maximum(qx, qy), 0) - r)
    inside = inside + WOBBLE * 2 * smooth_noise(ph, pw, 44, 1) + BRUSH * 2 * smooth_noise(ph, pw, 5, 2)
    wall = 1 - smoothstep(-2.5, 2.5, inside)
    shade = 1 - SHADOW * np.clip(1 - inside / SHADOW_W, 0, 1)
    img = G * shade[..., None]
    meadow = np.zeros((ph, pw))
    for k, (cx, cy, rx, ry) in enumerate(MEADOWS):
        e = np.sqrt(((xx - cx * 16) / (rx * 16)) ** 2 + ((yy - cy * 16) / (ry * 16)) ** 2)
        sd = (1 - e) * min(rx, ry) * 16 + 9 * smooth_noise(ph, pw, 14, 10 + k) + 5 * smooth_noise(ph, pw, 4, 20 + k)
        meadow = np.maximum(meadow, smoothstep(-3, 3, sd))
    img = img * (1 - meadow[..., None]) + M * meadow[..., None]
    for _, (x, y) in DOORS:                                   # a shadow under every door
        e = np.sqrt(((xx - (x + 1) * 16) / 19.0) ** 2 + ((yy - (y + 1.8) * 16) / 7.5) ** 2)
        img = img * (1 - 0.45 * np.clip(1 - e, 0, 1) ** 0.8)[..., None]
    gx, gy, gr, gc, gs = GLOW                               # light, not paint: the floor lifted toward white, its hue kept
    d = np.hypot(xx - gx * 16, yy - gy * 16) / (gr * 16)
    img = img + (255 - img) * (gs * np.clip(1 - d, 0, 1) ** 2)[..., None]
    img = img * (1 - wall[..., None]) + L * wall[..., None]
    return np.clip(img, 0, 255), wall, meadow * (1 - wall)


class Sheet:
    """Every tile and metatile of both tilesets, numbered as the engine numbers them (0..1023)."""
    def __init__(self):
        self.tiles = [np.zeros(64, np.uint8)]                 # tile 0: empty, for an empty layer
        self.index = {bytes(64): (0, 0)}
        self.metas = [((0,) * 4, (0,) * 4, COVERED)]           # metatile 0: nothing, never placed
        self.meta_index = {self.metas[0]: 0}
        self.pals = [[(0, 0, 0)] * 16 for _ in range(16)]

    def tile(self, idx, flips=True):
        """The entry (tile number and flip bits) for an 8x8 block of palette indices."""
        a = np.asarray(idx, np.uint8).reshape(8, 8)
        key = bytes(a)
        if key in self.index:
            t, f = self.index[key]
            return t | f
        if flips:
            for f, b in ((0x400, a[:, ::-1]), (0x800, a[::-1, :]), (0xC00, a[::-1, ::-1])):
                k2 = bytes(np.ascontiguousarray(b))
                if k2 in self.index:
                    t, f0 = self.index[k2]
                    return t | (f0 ^ f)
        n = len(self.tiles)
        self.tiles.append(a.reshape(64))
        self.index[key] = (n, 0)
        return n

    def meta(self, bottom, middle, attr):
        key = (tuple(bottom), tuple(middle), attr)
        if key not in self.meta_index:
            self.meta_index[key] = len(self.metas)
            self.metas.append(key)
        return self.meta_index[key]


def landscape_palettes(img):
    """Ten palettes for the picture's tiles, and each tile's palette and indices."""
    th, tw = H * 2, W * 2
    T = img.reshape(th, 8, tw, 8, 3).transpose(0, 2, 1, 3, 4).reshape(th * tw, 64, 3)
    feat = np.concatenate([T.mean(1), T.std(1) * 0.6], 1)
    _, lab = kmeans2(feat, LAND_PALS, seed=395, minit="++")
    pals = []
    for it in range(4):
        pals = []
        for g in range(LAND_PALS):
            pix = T[lab == g].reshape(-1, 3)
            if len(pix) == 0:
                pix = T.reshape(-1, 3)
            rng = np.random.default_rng(395 + g)
            pix = pix[rng.choice(len(pix), min(len(pix), 24000), replace=False)]
            c, _ = kmeans2(pix, 15, seed=395 + g, minit="++")
            pals.append(np.clip(np.round(c / 8) * 8, 0, 248))
        err = np.stack([((T[:, :, None, :] - p[None, None]) ** 2).sum(-1).min(-1).sum(-1) for p in pals], 1)
        lab = err.argmin(1)
    #  A light ordered dither as each pixel takes its colour: where neighbouring tiles took different palettes, the
    #  seam is broken up rather than drawn as a square.
    bayer = (np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]], float) / 16 - 0.47) * DITHER
    dith = np.tile(bayer, (2, 2)).reshape(64, 1)
    idx = np.stack([((T[n][:, None, :] + dith[:, :, None] - pals[lab[n]][None]) ** 2).sum(-1).argmin(-1) + 1
                    for n in range(len(T))])
    return pals, lab.reshape(th, tw), idx.reshape(th, tw, 64)


def merge_tiles(pals, lab, idx, budget):
    """Fewer tiles, if the picture needs more than the tilesets hold: the tiles are clustered by how they look, and every
    tile in a cluster is drawn as the real tile nearest its middle. Painted texture hides it; a flat edge would not."""
    th, tw = lab.shape
    keys, first, who = {}, [], np.zeros(th * tw, int)
    for n in range(th * tw):
        k = (int(lab.flat[n]), bytes(idx.reshape(-1, 64)[n].astype(np.uint8)))
        if k not in keys:
            keys[k] = len(first)
            first.append(n)
        who[n] = keys[k]
    if len(first) <= budget:
        return lab, idx, len(first)
    rgb = np.stack([pals[lab.flat[n]][idx.reshape(-1, 64)[n] - 1].reshape(-1) for n in first]).astype(float)
    #  Agglomerative (Ward): the closest pairs merge first, so no tile stands in for one that looks nothing like it.
    from scipy.cluster.hierarchy import linkage, fcluster
    cl = fcluster(linkage(rgb, "ward"), budget, criterion="maxclust")
    rep = {}
    for c in set(cl):
        members = np.where(cl == c)[0]
        cent = rgb[members].mean(0)
        rep[c] = members[((rgb[members] - cent) ** 2).sum(1).argmin()]
    lab2, idx2 = lab.copy().reshape(-1), idx.copy().reshape(-1, 64)
    for n in range(th * tw):
        m = first[rep[cl[who[n]]]]
        lab2[n], idx2[n] = lab.flat[m], idx.reshape(-1, 64)[m]
    return lab2.reshape(th, tw), idx2.reshape(th, tw, 64), len(set(cl))


def build_art():
    tree = masked("tree", 32, 32)
    xmas = masked("xmas", 32, 48)
    g1, g2, g3 = grey_states(tree)
    pals, P = {}, {}
    pals["tree"], (P["tree"],) = quantise([tree])
    pals["grey"], (P["grey1"], P["grey2"], P["grey3"]) = quantise([g1, g2, g3])
    pals["xmas"], (P["xmas"],) = quantise([xmas])
    return pals, P


def build(pals, P):
    img, wall, meadow = landscape()
    lpals, lab, idx = landscape_palettes(img)
    tree_tiles = 1 + 4 * 16 + 6 * 4                              # the four door trees and the Christmas tree, at most
    lab, idx, n = merge_tiles(lpals, lab, idx, 1024 - tree_tiles - 8)
    sh = Sheet()
    for g, p in enumerate(lpals):
        sh.pals[g] = [(0, 0, 0)] + [tuple(int(v) for v in c) for c in p]
    for k, v in TREE_PAL.items():
        sh.pals[v] = list(pals[k])
    land = [[sh.tile(idx[ty, tx]) | (int(lab[ty, tx]) << 12) for tx in range(W * 2)] for ty in range(H * 2)]
    bottom = lambda x, y: [land[2 * y][2 * x], land[2 * y][2 * x + 1], land[2 * y + 1][2 * x], land[2 * y + 1][2 * x + 1]]
    raw = [[0] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            cw = wall[y * 16:(y + 1) * 16, x * 16:(x + 1) * 16].mean()
            cm = meadow[y * 16:(y + 1) * 16, x * 16:(x + 1) * 16].mean()
            attr = COVERED | (LAND if cm > 0.5 and cw <= 0.5 else 0)
            raw[y][x] = sh.meta(bottom(x, y), [0] * 4, attr) | (COLLIDE if cw > 0.5 else 0) | ELEV

    def over(im, pal, dx, dy):
        out = []
        for k in range(4):
            px = np.asarray(im.crop((dx * 16 + (k % 2) * 8, dy * 16 + (k // 2) * 8,
                                     dx * 16 + (k % 2) * 8 + 8, dy * 16 + (k // 2) * 8 + 8)), np.uint8)
            t = sh.tile(px, flips=False) if px.any() else 0
            out.append(t | (pal << 12) if t else 0)
        return out

    def overlay(im, pal, x0, y0, w, h, store):
        for dy in range(h):
            for dx in range(w):
                x, y = x0 + dx, y0 + dy
                m = sh.meta(bottom(x, y), over(im, pal, dx, dy), COVERED)
                store[(dx, dy)] = m
                raw[y][x] = m | COLLIDE | ELEV

    overlay(P["xmas"], TREE_PAL["xmas"], CHRISTMAS[0], CHRISTMAS[1], 2, 3, {})
    states = {}
    for name, (x, y) in DOORS:
        st = {}
        for key, im, pal in (("tree", P["tree"], "tree"), ("grey3", P["grey3"], "grey"),
                             ("grey2", P["grey2"], "grey"), ("grey1", P["grey1"], "grey")):
            st[key] = {}
            overlay(im, TREE_PAL[pal], x, y, 2, 2, st[key])     # the last drawn stays: grey, as the map is drawn
        states[name] = st
    for (x, y) in (ARRIVE, HUNTER, PHOENIX) + tuple((x + dx, y + 2) for _, (x, y) in DOORS for dx in (0, 1)) + \
            ((CHRISTMAS[0], CHRISTMAS[1] + 3), (CHRISTMAS[0] + 1, CHRISTMAS[1] + 3)):
        assert not (raw[y][x] >> 10) & 3, "(%d,%d) must be open ground" % (x, y)
    assert len(sh.tiles) <= 1024 and len(sh.metas) <= 1023, (len(sh.tiles), len(sh.metas))
    return sh, raw, states


# ------------------------------------------------------------------------------------------------- the engine files
def gpath(p):
    return os.path.join(GBA, p)


def read(p):
    return open(gpath(p)).read()


def jasc(pal):
    return "JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % c for c in (list(pal) + [(0, 0, 0)] * 16)[:16])


def tileset_files(sh):
    """{(dir, path): data} for the primary half (tiles and metatiles 0..639, palettes 0..6) and the secondary."""
    files = {}
    for part, d, t0, t1, m0, m1, pals in (("primary", PDIR, 0, 640, 0, 640, range(0, 7)),
                                          ("secondary", TSDIR, 640, 1024, 640, 1024, range(7, 13))):
        tiles = sh.tiles[t0:t1]
        n = 640 if part == "primary" else max(1, len(tiles))
        img = Image.new("P", (128, ((n + 15) // 16) * 8))
        img.putpalette(sum(([v * 17] * 3 for v in range(16)), []) + [0] * 720)
        ip = img.load()
        for k, t in enumerate(tiles):
            for i, v in enumerate(t):
                ip[(k % 16) * 8 + i % 8, (k // 16) * 8 + i // 8] = int(v)
        files[(part, d, "tiles.png")] = img
        meta, attr = bytearray(), bytearray()
        for b, m, a in sh.metas[m0:m1]:
            meta += struct.pack("<8H", *(list(b) + list(m)))
            attr += struct.pack("<I", a)
        files[(part, d, "metatiles.bin")] = bytes(meta) or bytes(16)
        files[(part, d, "metatile_attributes.bin")] = bytes(attr) or bytes(4)
        for r in range(16):
            files[(part, d, "palettes/%02d.pal" % r)] = jasc(sh.pals[r] if r in pals else [(0, 0, 0)] * 16)
    return files


def scripts(states, ts):
    rows = {g["name"]: g for g in grove.GROVES}
    out = ["@ T-395: THE NEXUS (docs/nexus.md) -- tools/gbanexusmap.py writes this file. Every word approved by the user, 2026-10-10.",
           "",
           "%s_MapScripts::" % NAME,
           "\tmap_script MAP_SCRIPT_ON_LOAD, %s_OnLoad" % NAME,
           "\tmap_script MAP_SCRIPT_ON_TRANSITION, %s_OnTransition" % NAME,
           "\t.byte 0",
           "",
           "%s_OnTransition::" % NAME,
           "\tsetflag FLAG_NEXUS_VISITED",
           "\tend",
           "",
           "@ The map is drawn with every door grey; a grove once arrived in is an ordinary tree again.",
           "%s_OnLoad::" % NAME]
    for k, (name, (x, y)) in enumerate(DOORS):
        out.append("\tcall_if_set %s, %s_EventScript_Found%d" % (grove.found_flag(grove.map_const(rows[name])), NAME, k))
    out += ["\tend", ""]
    for k, (name, (x, y)) in enumerate(DOORS):
        out.append("%s_EventScript_Found%d::" % (NAME, k))
        for (dx, dy), m in sorted(states[name]["tree"].items(), key=lambda kv: (kv[0][1], kv[0][0])):
            out.append("\tsetmetatile %d, %d, 0x%X, TRUE" % (x + dx, y + dy, m))
        out += ["\treturn", ""]
    for k, (name, (x, y)) in enumerate(DOORS):
        g = rows[name]
        fx, fy = grove.fir_of(g)
        var = "VAR_TEMP_%X" % (k + 1)
        out += ["@ %s" % name,
                "%s_EventScript_Door%d::" % (NAME, k),
                "\tlockall",
                "\tgoto_if_unset %s, %s_EventScript_Locked%d" % (grove.found_flag(grove.map_const(g)), NAME, k),
                "\tmsgbox %s_Text_DoorOpen, MSGBOX_YESNO" % NAME,
                "\tgoto_if_eq VAR_RESULT, NO, %s_EventScript_Stay" % NAME,
                "\tmsgbox %s_Text_Voice" % NAME,
                "\tmsgbox %s_Text_Guardian%d" % (NAME, k),
                "\tplayse SE_WARP_IN",
                "\twarp %s, %d, %d" % (grove.map_const(g), fx, fy + 1),
                "\twaitstate",
                "\treleaseall",
                "\tend",
                "",
                "%s_EventScript_Locked%d::" % (NAME, k),
                "\tswitch %s" % var,
                "\tcase 0, %s_EventScript_Smudge%d" % (NAME, k),
                "\tcase 1, %s_EventScript_Lines%d" % (NAME, k),
                "\tmsgbox %s_Text_Locked3" % NAME,
                "\treleaseall",
                "\tend",
                "",
                "%s_EventScript_Smudge%d::" % (NAME, k)]
        for (dx, dy), m in sorted(states[name]["grey2"].items(), key=lambda kv: (kv[0][1], kv[0][0])):
            out.append("\tsetmetatile %d, %d, 0x%X, TRUE" % (x + dx, y + dy, m))
        out += ["\tspecial DrawWholeMapView", "\tsetvar %s, 1" % var, "\tmsgbox %s_Text_Locked1" % NAME,
                "\treleaseall", "\tend", "", "%s_EventScript_Lines%d::" % (NAME, k)]
        for (dx, dy), m in sorted(states[name]["grey3"].items(), key=lambda kv: (kv[0][1], kv[0][0])):
            out.append("\tsetmetatile %d, %d, 0x%X, TRUE" % (x + dx, y + dy, m))
        out += ["\tspecial DrawWholeMapView", "\tsetvar %s, 2" % var, "\tmsgbox %s_Text_Locked2" % NAME,
                "\treleaseall", "\tend", ""]
    found = [grove.found_flag(grove.map_const(rows[n])) for n, _ in DOORS]
    out += ["%s_EventScript_Stay::" % NAME, "\treleaseall", "\tend", "",
            "@ The one Christmas tree: the way home, to the S.S. ANNE's pier.",
            "%s_EventScript_ChristmasTree::" % NAME,
            "\tlockall",
            "\tsetvar VAR_0x8004, TRUE",
            "\tspecial SingingFir_Sing",
            "\twaitstate",
            "\tmsgbox %s_Text_Christmas, MSGBOX_YESNO" % NAME,
            "\tgoto_if_eq VAR_RESULT, NO, %s_EventScript_Stay" % NAME,
            "\tmsgbox %s_Text_Voice" % NAME,
            "\tmsgbox %s_Text_GuardianHome" % NAME,
            "\tplayse SE_WARP_IN",
            "\twarp %s, %d, %d" % PIER,
            "\twaitstate",
            "\treleaseall",
            "\tend",
            "",
            "@ THE (NOT A) HUNTER, a bear in red plaid.",
            "%s_EventScript_Hunter::" % NAME,
            "\tlock",
            "\tfaceplayer",
            "\tgoto_if_set FLAG_NEXUS_HUNTER_MET, %s_EventScript_HunterAgain" % NAME,
            "\tsetflag FLAG_NEXUS_HUNTER_MET",
            "\tmsgbox %s_Text_HunterFirst" % NAME,
            "\trelease",
            "\tend",
            "",
            "%s_EventScript_HunterAgain::" % NAME]
    out += ["\tgoto_if_unset %s, %s_EventScript_HunterNotAll" % (f, NAME) for f in found]
    out += ["\tmsgbox %s_Text_HunterAll" % NAME, "\trelease", "\tend", "",
            "%s_EventScript_HunterNotAll::" % NAME, "\tmsgbox %s_Text_Hunter" % NAME, "\trelease", "\tend", "",
            "@ PHOENIX, once, waiting in the paint.",
            "%s_EventScript_Phoenix::" % NAME,
            "\tgoto_if_questlog EventScript_ReleaseEnd",
            "\tspecial QuestLog_CutRecording",
            "\tlock",
            "\tfaceplayer",
            "\tsetwildbattle SPECIES_HO_OH, 35",
            "\twaitse",
            "\tplaymoncry SPECIES_HO_OH, CRY_MODE_ENCOUNTER",
            "\tmessage %s_Text_Phoenix" % NAME,
            "\twaitmessage",
            "\twaitmoncry",
            "\tdelay 10",
            "\tplaybgm MUS_ENCOUNTER_GYM_LEADER, 0",
            "\twaitbuttonpress",
            "\tsetflag FLAG_SYS_SPECIAL_WILD_BATTLE",
            "\tspecial StartLegendaryBattle",
            "\twaitstate",
            "\tclearflag FLAG_SYS_SPECIAL_WILD_BATTLE",
            "\tspecialvar VAR_RESULT, GetBattleOutcome",
            "\tgoto_if_eq VAR_RESULT, B_OUTCOME_WON, %s_EventScript_PhoenixGone" % NAME,
            "\tgoto_if_eq VAR_RESULT, B_OUTCOME_RAN, %s_EventScript_PhoenixFlew" % NAME,
            "\tgoto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, %s_EventScript_PhoenixFlew" % NAME,
            "\trelease",
            "\tend",
            "",
            "%s_EventScript_PhoenixGone::" % NAME,
            "\tgoto EventScript_RemoveStaticMon",
            "\tend",
            "",
            "%s_EventScript_PhoenixFlew::" % NAME,
            "\tsetvar VAR_0x8004, SPECIES_HO_OH",
            "\tgoto EventScript_MonFlewAway",
            "\tend",
            "",
            "@ ------------------------------------------------------------------------------------------------",
            "@ THE SINGING FIR, everywhere it stands: every grove (tools/gbagrove.py) and the S.S. ANNE's pier. Flat",
            "@ until the band's sheet gives it its key; then a door into THE NEXUS. The fir before the key and the fir",
            "@ after it are two objects on one tile, the bright one the next local id: swapped here, the first time.",
            "EventScript_SingingFir::",
            "\tlock",
            "\tgoto_if_set FLAG_FIR_IN_KEY, EventScript_SingingFir_InKey",
            "\tmsgbox Text_SingingFir_Hums",
            "\tsetvar VAR_0x8004, FALSE",
            "\tspecial SingingFir_Sing",
            "\twaitstate",
            "\tgoto_if_set FLAG_NOTEBOOK_LOOSE_KEY, EventScript_SingingFir_GivenKey",
            "\tmsgbox Text_SingingFir_Off",
            "\trelease",
            "\tend",
            "",
            "EventScript_SingingFir_GivenKey::",
            "\tmsgbox Text_SingingFir_HoldUpSheet",
            "\tsetvar VAR_0x8004, TRUE",
            "\tspecial SingingFir_Sing",
            "\twaitstate",
            "\tsetflag FLAG_FIR_IN_KEY",
            "\tclearflag FLAG_HIDE_FIR_UNKEYED",
            "\tcopyvar VAR_0x8005, VAR_LAST_TALKED",
            "\tremoveobject VAR_0x8005",
            "\taddvar VAR_0x8005, 1",
            "\taddobject VAR_0x8005",
            "\tmsgbox Text_SingingFir_Right",
            "\tgoto EventScript_SingingFir_Door",
            "",
            "EventScript_SingingFir_InKey::",
            "\tmsgbox Text_SingingFir_Hums",
            "\tsetvar VAR_0x8004, TRUE",
            "\tspecial SingingFir_Sing",
            "\twaitstate",
            "EventScript_SingingFir_Door::",
            "\tmsgbox Text_SingingFir_Door, MSGBOX_YESNO",
            "\tgoto_if_eq VAR_RESULT, NO, EventScript_SingingFir_Stay",
            "\tcall_if_unset FLAG_NEXUS_VISITED, EventScript_SingingFir_FirstTime",
            "\tplayse SE_WARP_IN",
            "\twarp %s, %d, %d" % ((MAPC,) + ARRIVE),
            "\twaitstate",
            "\trelease",
            "\tend",
            "",
            "EventScript_SingingFir_FirstTime::",
            "\tmsgbox Text_SingingFir_FirstTime",
            "\treturn",
            "",
            "EventScript_SingingFir_Stay::",
            "\trelease",
            "\tend",
            "",
            "@ On every arrival where a fir stands: the bright one stays hidden until the key.",
            "EventScript_FirKeyFlags::",
            "\tgoto_if_set FLAG_FIR_IN_KEY, EventScript_FirKeyFlags_Keyed",
            "\tsetflag FLAG_HIDE_FIR_UNKEYED",
            "\treturn",
            "",
            "EventScript_FirKeyFlags_Keyed::",
            "\tclearflag FLAG_HIDE_FIR_UNKEYED",
            "\treturn",
            ""]
    #  T-408: the universes' signs, one beside every door, read whether or not the grove has been found
    for k, (name, _) in enumerate(DOORS):
        out += ["%s_EventScript_Sign%d::" % (NAME, k), "\tmsgbox %s_Text_Sign%d, MSGBOX_SIGN" % (NAME, k), "\tend", ""]
    return "\n".join(out)


def text_inc():
    out = ["@ T-395: THE NEXUS's words, and the singing fir's (tools/gbanexusmap.py). Every word approved by the user, 2026-10-10.", ""]
    for label, t in TEXT.items():
        out.append("%s::\n%s" % (label, gba_string(t)))
    return "\n".join(out)


def map_json():
    rows = {g["name"]: g for g in grove.GROVES}
    bg = [{"type": "sign", "x": CHRISTMAS[0] + dx, "y": CHRISTMAS[1] + 2, "elevation": 0,
           "player_facing_dir": "BG_EVENT_PLAYER_FACING_NORTH", "script": "%s_EventScript_ChristmasTree" % NAME} for dx in (0, 1)]
    for k, (name, (x, y)) in enumerate(DOORS):
        bg += [{"type": "sign", "x": x + dx, "y": y + 1, "elevation": 0, "player_facing_dir": "BG_EVENT_PLAYER_FACING_NORTH",
                "script": "%s_EventScript_Door%d" % (NAME, k)} for dx in (0, 1)]
    obj = lambda gfx, xy, mv, script, flag: {
        "type": "object", "graphics_id": gfx, "x": xy[0], "y": xy[1], "elevation": 3, "movement_type": mv,
        "movement_range_x": 1, "movement_range_y": 1, "trainer_type": "TRAINER_TYPE_NONE",
        "trainer_sight_or_berry_tree_id": "0", "script": script, "flag": flag}
    return {
        "id": MAPC, "name": NAME, "layout": LAYOUT, "music": MUSIC, "region_map_section": "MAPSEC_S_S_ANNE",
        "requires_flash": False, "weather": "WEATHER_NONE", "map_type": "MAP_TYPE_UNDERGROUND",
        "allow_cycling": False, "allow_escaping": False, "allow_running": True, "show_map_name": False,
        "floor_number": 0, "battle_scene": "MAP_BATTLE_SCENE_NORMAL", "connections": None,
        "object_events": [obj("OBJ_EVENT_GFX_NEXUS_HUNTER", HUNTER, "MOVEMENT_TYPE_LOOK_AROUND",
                              "%s_EventScript_Hunter" % NAME, "0"),
                          obj("OBJ_EVENT_GFX_HO_OH", PHOENIX, "MOVEMENT_TYPE_FACE_DOWN",
                              "%s_EventScript_Phoenix" % NAME, "FLAG_NEXUS_PHOENIX_GONE")] +
                         [obj("OBJ_EVENT_GFX_SIGN", sign_at(x, y), "MOVEMENT_TYPE_FACE_DOWN",       # T-408
                              "%s_EventScript_Sign%d" % (NAME, k), "0") for k, (_, (x, y)) in enumerate(DOORS)],
        "warp_events": [], "coord_events": [], "bg_events": bg}


#  The residents (tools/gbanexus.py): twelve slots of the land table, 20 20 10 10 10 10 5 5 4 4 1 1. The tiger and
#  the lioness pass close only once in a long while; the grown forms come by growing.
RESIDENTS = [("REFLECTION", 22, 26), ("LYNX", 22, 26), ("MULTIMAL", 22, 26), ("SPHEAL", 22, 26),
             ("REFLECTION", 24, 28), ("LYNX", 24, 28), ("LODESTAR", 25, 28), ("MULTIMAL", 25, 28),
             ("SPHEAL", 25, 28), ("LODESTAR", 27, 30), ("PERIHELION", 30, 30), ("LYUBOV", 30, 30)]


def encounters():
    mons = [{"min_level": lo, "max_level": hi, "species": "SPECIES_" + s} for s, lo, hi in RESIDENTS]
    return [{"map": MAPC, "base_label": "s%s_%s" % (NAME, ed), "land_mons": {"encounter_rate": 20, "mons": mons}}
            for ed in ("FireRed", "LeafGreen")]


def preview(sh, raw):
    """The map as the game will draw it, at 2x, for a contact sheet."""
    img = np.zeros((H * 16, W * 16, 3), np.uint8)
    def draw(e, x, y, transparent):
        t = sh.tiles[e & 0x3FF].reshape(8, 8)
        if e & 0x400:
            t = t[:, ::-1]
        if e & 0x800:
            t = t[::-1, :]
        pal = np.array(sh.pals[e >> 12], np.uint8)
        block = pal[t]
        if transparent:
            m = t != 0
            img[y:y + 8, x:x + 8][m] = block[m]
        else:
            img[y:y + 8, x:x + 8] = block
    for my in range(H):
        for mx in range(W):
            b, m, _ = sh.metas[raw[my][mx] & 0x3FF]
            for layer, entries in ((False, b), (True, m)):
                for k, e in enumerate(entries):
                    if e or not layer:
                        draw(e, mx * 16 + (k % 2) * 8, my * 16 + (k // 2) * 8, layer)
    return Image.fromarray(img).resize((W * 32, H * 32), Image.NEAREST)


def main():
    bad = check_words()
    if bad:
        sys.exit("  words too wide for the box:\n    " + "\n    ".join(bad))
    pals, P = build_art()
    ts, raw, states = build(pals, P)
    print("  the tilesets: %d tiles, %d metatiles (of 1024 between the primary and the secondary)" % (len(ts.tiles), len(ts.metas)))
    os.makedirs(SCRATCH, exist_ok=True)
    pv = preview(ts, raw)
    pv.save(os.path.join(SCRATCH, "nexus_map_preview.png"))
    print("  preview: %s" % os.path.join(SCRATCH, "nexus_map_preview.png"))

    todo = {}
    for (part, d, rel), v in tileset_files(ts).items():
        p = gpath(os.path.join("data/tilesets", part, d, rel))
        if isinstance(v, Image.Image):
            same = os.path.exists(p) and list(Image.open(p).getdata()) == list(v.getdata()) and Image.open(p).size == v.size
        else:
            data = v.encode() if isinstance(v, str) else v
            same = os.path.exists(p) and open(p, "rb").read() == data
        if not same:
            todo[p] = v
    mbin = b"".join(struct.pack("<H", raw[y][x]) for y in range(H) for x in range(W))
    wall = raw[0][0]
    border = struct.pack("<4H", wall, wall, wall, wall)
    for rel, data in (("data/layouts/%s/map.bin" % NAME, mbin), ("data/layouts/%s/border.bin" % NAME, border)):
        if not os.path.exists(gpath(rel)) or open(gpath(rel), "rb").read() != data:
            todo[gpath(rel)] = data
    for rel, s in (("data/maps/%s/scripts.inc" % NAME, scripts(states, ts)), ("data/maps/%s/text.inc" % NAME, text_inc()),
                   ("data/maps/%s/map.json" % NAME, json.dumps(map_json(), indent=2) + "\n")):
        if not os.path.exists(gpath(rel)) or read(rel) != s:
            todo[gpath(rel)] = s

    #  the registrations: layout, map group, includes, tileset headers and rule, encounters
    layouts = json.loads(read("data/layouts/layouts.json"))
    entry = {"id": LAYOUT, "name": NAME + "_Layout", "width": W, "height": H, "border_width": 2, "border_height": 2,
             "primary_tileset": PRIMARY, "secondary_tileset": TILESET,
             "border_filepath": "data/layouts/%s/border.bin" % NAME, "blockdata_filepath": "data/layouts/%s/map.bin" % NAME}
    have = [l for l in layouts["layouts"] if l.get("id") == LAYOUT]
    if have != [entry]:
        layouts["layouts"] = [l for l in layouts["layouts"] if l.get("id") != LAYOUT] + [entry]
        todo[gpath("data/layouts/layouts.json")] = json.dumps(layouts, indent=2) + "\n"
    groups = json.loads(read("data/maps/map_groups.json"))
    grp = next(k for k in groups["group_order"] if "SSAnne_Exterior" in groups[k])
    if NAME not in groups[grp]:
        groups[grp].append(NAME)
        todo[gpath("data/maps/map_groups.json")] = json.dumps(groups, indent=2) + "\n"
    ev = read("data/event_scripts.s")
    inc_s = '\t.include "data/maps/%s/scripts.inc"\n' % NAME
    if inc_s not in ev:
        ev = ev.replace('\t.include "data/maps/SSAnne_Exterior/scripts.inc"\n',
                        '\t.include "data/maps/SSAnne_Exterior/scripts.inc"\n' + inc_s, 1)
        assert inc_s in ev, "event_scripts.s: no SSAnne_Exterior include to follow"
    inc_t = '\t.include "data/maps/%s/text.inc"\n' % NAME
    if inc_t not in ev:                          # the pier has no text.inc of its own: follow the groves' first
        anchor = '\t.include "data/maps/Route1_Grove/text.inc"\n'
        assert anchor in ev, "event_scripts.s: no grove text include to follow"
        ev = ev.replace(anchor, anchor + inc_t, 1)
    if ev != read("data/event_scripts.s"):
        todo[gpath("data/event_scripts.s")] = ev
    stem = TILESET[len("gTileset_"):]
    regs = [("src/data/tilesets/graphics.h", "gTilesetTiles_%s[]" % stem,
             "// T-395: THE NEXUS, made entirely of paint (tools/gbanexusmap.py, the DAEMONS repo).\n"
             "const u32 gTilesetTiles_%s[] = INCBIN_U32(\"data/tilesets/secondary/%s/tiles.4bpp.lz\");\n\n"
             "const u16 gTilesetPalettes_%s[][16] =\n{\n%s};\n" % (stem, TSDIR, stem,
             "".join("\tINCBIN_U16(\"data/tilesets/secondary/%s/palettes/%02d.gbapal\"),\n" % (TSDIR, k) for k in range(16)))),
            ("src/data/tilesets/metatiles.h", "gMetatiles_%s[]" % stem,
             "const u16 gMetatiles_%s[] = INCBIN_U16(\"data/tilesets/secondary/%s/metatiles.bin\");\n"
             "const u32 gMetatileAttributes_%s[] = INCBIN_U32(\"data/tilesets/secondary/%s/metatile_attributes.bin\");\n"
             % (stem, TSDIR, stem, TSDIR)),
            ("src/data/tilesets/headers.h", "gTileset_%s =" % stem,
             "// T-395: THE NEXUS (tools/gbanexusmap.py).\nconst struct Tileset gTileset_%s =\n{\n    .isCompressed = TRUE,\n"
             "    .isSecondary = TRUE,\n    .tiles = gTilesetTiles_%s,\n    .palettes = gTilesetPalettes_%s,\n"
             "    .metatiles = gMetatiles_%s,\n    .metatileAttributes = gMetatileAttributes_%s,\n    .callback = NULL,\n};\n"
             % (stem, stem, stem, stem, stem))]
    ps = PRIMARY[len("gTileset_"):]
    regs += [("src/data/tilesets/graphics.h", "gTilesetTiles_%s[]" % ps,
              "// T-395: THE NEXUS's primary half -- the landscape painted whole (tools/gbanexusmap.py).\n"
              "const u32 gTilesetTiles_%s[] = INCBIN_U32(\"data/tilesets/primary/%s/tiles.4bpp.lz\");\n\n"
              "const u16 gTilesetPalettes_%s[][16] =\n{\n%s};\n" % (ps, PDIR, ps,
              "".join("\tINCBIN_U16(\"data/tilesets/primary/%s/palettes/%02d.gbapal\"),\n" % (PDIR, k) for k in range(16)))),
             ("src/data/tilesets/metatiles.h", "gMetatiles_%s[]" % ps,
              "const u16 gMetatiles_%s[] = INCBIN_U16(\"data/tilesets/primary/%s/metatiles.bin\");\n"
              "const u32 gMetatileAttributes_%s[] = INCBIN_U32(\"data/tilesets/primary/%s/metatile_attributes.bin\");\n"
              % (ps, PDIR, ps, PDIR)),
             ("src/data/tilesets/headers.h", "gTileset_%s =" % ps,
              "// T-395: THE NEXUS's primary half (tools/gbanexusmap.py), as interiors have gTileset_Building.\n"
              "const struct Tileset gTileset_%s =\n{\n    .isCompressed = TRUE,\n"
              "    .isSecondary = FALSE,\n    .tiles = gTilesetTiles_%s,\n    .palettes = gTilesetPalettes_%s,\n"
              "    .metatiles = gMetatiles_%s,\n    .metatileAttributes = gMetatileAttributes_%s,\n    .callback = NULL,\n};\n"
              % (ps, ps, ps, ps, ps))]
    for rel, marker, block in regs:
        s = read(rel)
        if marker not in s:
            todo[gpath(rel)] = s + ("" if s.endswith("\n") else "\n") + block
    rules0 = rules = read("tileset_rules.mk")
    for part, d, n in (("primary", PDIR, 640), ("secondary", TSDIR, max(1, len(ts.tiles) - 640))):
        key = "$(TILESETGFXDIR)/%s/%s/tiles.4bpp: %%.4bpp: %%.png\n\t$(GFX) $< $@ -num_tiles " % (part, d)
        want = key + "%d -Wnum_tiles\n" % n
        if want not in rules:
            rules = re.sub(r"\n*" + re.escape(key) + r"\d+ -Wnum_tiles\n", "\n", rules)
            rules = rules.rstrip("\n") + "\n\n" + want
    if rules != rules0:
        todo[gpath("tileset_rules.mk")] = rules
    wild = json.loads(read("src/data/wild_encounters.json"))
    wg = next(x for x in wild["wild_encounter_groups"] if x.get("label") == "gWildMonHeaders")
    mine = encounters()
    if [e for e in wg["encounters"] if e["map"] == MAPC] != mine:
        wg["encounters"] = [e for e in wg["encounters"] if e["map"] != MAPC] + mine
        todo[gpath("src/data/wild_encounters.json")] = json.dumps(wild, indent=2) + "\n"
    fl = read("include/constants/flags.h")
    if "FLAG_NEXUS_PHOENIX_GONE" not in fl:
        todo[gpath("include/constants/flags.h")] = fl.replace(
            "#define FLAG_NEXUS_HUNTER_MET         (DAEMONS_FLAGS_START + 0x102)\n",
            "#define FLAG_NEXUS_HUNTER_MET         (DAEMONS_FLAGS_START + 0x102)\n"
            "#define FLAG_NEXUS_PHOENIX_GONE       (DAEMONS_FLAGS_START + 0x103)\n", 1)

    for p in sorted(todo):
        print("  %s %s" % ("wrote" if WRITE else "would write", os.path.relpath(p, GBA)))
    if not todo:
        print("  THE NEXUS is built, nothing to do")
    if WRITE:
        for p, v in todo.items():
            os.makedirs(os.path.dirname(p), exist_ok=True)
            if isinstance(v, Image.Image):
                v.save(p)
            elif isinstance(v, str):
                open(p, "w", newline="" if p.endswith(".pal") else None).write(v)
            else:
                open(p, "wb").write(v)
    return 0


if __name__ == "__main__":
    sys.exit(main())
