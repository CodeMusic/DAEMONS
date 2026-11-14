#!/usr/bin/env python3
"""T-547 THE BLANK TABLET's two sprites: the stone in BLANCHE, and the old toad who says the player's lean.

    python3 tools/genblanktablet.py            # report: what would change (previews in the scratch folder)
    python3 tools/genblanktablet.py --write    # blank_tablet.png, old_toad.png and src/data/blank_tablet_words.h

THE WORDS come from docs/blank-tablet-draft.md, the one place they are written: its four tables become
src/data/blank_tablet_words.h, every page broken into at most two lines of 208px by the engine's own font (port_dialogue's
textwidth), and the tool fails rather than write a page that needs a third. Edit the draft, never the header.

THE STONE (blank_tablet.png, 16x32, one frame, npc_white) is drawn here from nothing: a standing tablet with a rounded
head, light on its upper left, a little weather on its right side, and nothing on its face -- "a stone with nothing on
it". It is one frame because a stone does not turn; which face is read is the side the player stands on (the script).

THE OLD TOAD (old_toad.png, 48x32, three frames S N W, npc_green) is drawn from TILT's toad (koga.png), the only toad
the field already has, so she is plainly kin and keeps his palette: his green hat band becomes a purple shawl over her
head and down her shoulders, his purple shirt a long dark-green dress, and she leans on a stick. Every colour is one
npc_green already holds, so she repaints no one (engine.md trap 17).

Every pixel is DRAFT (the user, 2026-11-12, by multiple choice: "An old toad").
"""
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PEOPLE = os.path.join(GBA, "graphics/object_events/pics/people")
WHITE_PAL = os.path.join(GBA, "graphics/object_events/palettes/npc_white.pal")
TOAD_SRC = os.path.join(PEOPLE, "koga.png")
STONE = os.path.join(PEOPLE, "blank_tablet.png")
WORDS = os.path.join(GBA, "src/data/blank_tablet_words.h")
DRAFT = os.path.join(ROOT, "docs/blank-tablet-draft.md")
LINE_PX = 208
# The sayings' rows, in the order the spells are cast from the book (daemons_spellbook.h; THE PULL writes no line).
SPELLS = ["AWAKENING", "CONTRAST", "ROOM", "MIRROR", "PATTERN", "RETURN", "SMALL HAND", "GREAT HAND", "PROCESS",
          "SEAM", "LENS", "FIELD"]
ENUMS = {n: "SPELL_" + n.replace(" ", "_") for n in SPELLS}
POLES = ["REASON", "INTUITION", "CONTENT", "CONTEXT"]
TOAD = os.path.join(PEOPLE, "old_toad.png")
SCRATCH = os.environ.get("DAEMONS_SCRATCH", "/tmp/genblanktablet")
WRITE = "--write" in sys.argv

# npc_white: 11 light grey, 12 mid grey, 13 dark grey, 14 white, 15 black.
S_FACE, S_SIDE, S_DARK, S_LIGHT, S_INK = 11, 12, 13, 14, 15
# npc_green: 4 brown, 9/10 dark greens, 11-13 the purples (light, mid, dark), 15 black.
T_STICK, T_DRESS, T_DRESS_DARK, T_SHAWL_LIGHT, T_SHAWL, T_SHAWL_DARK, T_INK = 4, 9, 10, 11, 12, 13, 15


def read_pal(path):
    lines = open(path).read().split()
    n = int(lines[2])
    vals = [int(v) for v in lines[3:3 + 3 * n]]
    return vals + [0] * (768 - len(vals))


def draw_stone():
    """A standing tablet, columns 2-13, its head an arc from row 6, its foot on row 29."""
    w, h = 16, 32
    cx, top, foot, half = 7.5, 6, 29, 6
    inside = set()
    for y in range(top, foot + 1):
        for x in range(w):
            dx = abs(x - cx)
            if dx > half:
                continue
            if y < top + half:                      # the rounded head
                dy = (top + half) - y - 0.5
                if dx * dx + dy * dy > half * half + 1:
                    continue
            inside.add((x, y))
    im = Image.new("P", (w, h), 0)
    im.putpalette(read_pal(WHITE_PAL))
    for (x, y) in inside:
        edge = any((x + a, y + b) not in inside for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        if edge:
            c = S_INK
        elif x >= 11:
            c = S_DARK if x == 12 else S_SIDE       # the shaded side
        elif y == foot - 1:
            c = S_SIDE                              # where it meets the ground
        else:
            c = S_FACE
        im.putpixel((x, y), c)
    # Light on the upper left, just inside the outline.
    for (x, y) in inside:
        if im.getpixel((x, y)) != S_FACE:
            continue
        lit = ((x - 1, y) in inside and im.getpixel((x - 1, y)) == S_INK) or \
              ((x, y - 1) in inside and im.getpixel((x, y - 1)) == S_INK)
        if lit and x <= 8 and y <= 18:
            im.putpixel((x, y), S_LIGHT)
    # A little weather, never a mark that could be read: two pits on the shaded side, one low on the face.
    for (x, y) in ((11, 14), (12, 21), (5, 25)):
        if (x, y) in inside:
            im.putpixel((x, y), S_SIDE if x < 11 else S_DARK)
    return im


def draw_toad():
    src = Image.open(TOAD_SRC)
    im = src.copy()
    w, h = im.size
    px = im.load()
    for f in range(w // 16):
        x0 = f * 16
        side = f == 2
        # The shirt becomes a long dress (first: the shawl takes the purples after).
        for y in range(h):
            for x in range(x0, x0 + 16):
                if px[x, y] == 12:
                    px[x, y] = T_DRESS
                elif px[x, y] == 13:
                    px[x, y] = T_DRESS_DARK
        # The hat band (rows 10-12) becomes a hood: a row higher, its crown lit, the band itself the shawl.
        band = [x for x in range(x0, x0 + 16) if px[x, 10] == T_INK]
        if band:
            for x in range(band[0] + 1, band[-1]):
                px[x, 9] = T_INK
                px[x, 10] = T_SHAWL_LIGHT
        for y in (11, 12):
            for x in range(x0, x0 + 16):
                if px[x, y] in (8, 9):
                    px[x, y] = T_SHAWL
        # ... and hangs down beside her face to the shoulders: two pixels in from each edge, rows 13-18 (one edge,
        # the back of her head, from the side).
        for y in range(13, 19):
            row = [x for x in range(x0, x0 + 16) if px[x, y] not in (0, T_INK)]
            if not row:
                continue
            ends = row[-2:] if side else row[:2] + row[-2:]
            for x in ends:
                px[x, y] = T_SHAWL_DARK if y >= 17 else T_SHAWL
        # The stick: on her right in front (column 14), held before her from the side (column 1).
        if f == 0:
            col = x0 + 14
        elif side:
            col = x0 + 1
        else:
            col = None                               # from behind, her body hides it
        if col is not None:
            for y in range(18, 31):
                if px[col, y] == 0:
                    px[col, y] = T_STICK
    return im


def tables():
    """docs/blank-tablet-draft.md's tables, by the heading above each: {heading: [row cells...]}."""
    out, head = {}, None
    for line in open(DRAFT).read().split("\n"):
        if line.startswith("## "):
            head = line[3:].strip()
        elif line.startswith("|") and not line.startswith("|---") and head:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            out.setdefault(head, []).append(cells)
    return {h: rows[1:] for h, rows in out.items()}     # the header row off


def page(text):
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    from port_dialogue import textwidth
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if textwidth(t) <= LINE_PX:
            cur = t
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    if len(lines) > 2:
        raise SystemExit("genblanktablet: a page needs %d lines (two at most): %s" % (len(lines), text))
    return "\\n".join(l.replace('"', '\\"') for l in lines)


def two(first, second):
    """Two lines the draft keeps apart (the stone's blanks): each must fit one line."""
    for t in (first, second):
        if t and "\\n" in page(t):
            raise SystemExit("genblanktablet: a stone line needs two lines: %s" % t)
    return page(first) + ("\\n" + page(second) if second else "")


def words():
    t = tables()
    say = {r[0]: r[1:5] for r in t["The twelve sayings"]}
    if sorted(say) != sorted(SPELLS):
        raise SystemExit("genblanktablet: the sayings' rows are not the twelve spells: %s" % sorted(say))
    thirteen = {r[0]: r[1:3] for r in t["The thirteenth line"]}
    stone = [r[1:3] for r in t["The stone with nothing to read"]]
    toad = {r[0]: r[1:3] for r in t["The old toad in BLANCHE"]}
    decl = []

    def lit(text):
        name = "sBT_%d" % len(decl)
        decl.append('static const u8 %s[] = _("%s");' % (name, text))
        return name

    tab = ["", "// [spell][face: 0 front, the night half; 1 back, the dawn half][voice: 0 reason, 1 intuition]",
           "static const u8 *const sBlankSayings[BLANK_SAYINGS][2][2] = {"]
    for n in SPELLS:
        fr, fi, br, bi = (lit(page(x)) for x in say[n])
        tab.append("    [BLANK_%s] = {{ %s, %s }, { %s, %s }}," % (n.replace(" ", "_"), fr, fi, br, bi))
    tab += ["};", "", "// The thirteenth line's saying, [pole: LEDGER_*][face]",
            "static const u8 *const sBlankThirteenth[LEDGER_COUNT][2] = {"]
    for p in POLES:
        f, b = (lit(page(x)) for x in thirteen[p])
        tab.append("    [LEDGER_%s] = { %s, %s }," % (p, f, b))
    tab += ["};", "", "// The stone with nothing to read: nothing held (or neither face yours), your face with nothing cast",
            "// yet, the night half from behind, the dawn half from in front.", "static const u8 *const sBlankStone[4] = {"]
    for a, b in stone:
        tab.append("    %s," % lit(two(a, b)))
    tab += ["};", "", "// The old toad: [0 nothing yet, 1 + LEDGER_*][0 night and day, 1 dawn]",
            "static const u8 *const sOldToad[1 + LEDGER_COUNT][2] = {"]
    for k in ["NOTHING YET"] + POLES:
        n, d = (lit(page(x)) for x in toad[k])
        tab.append("    { %s, %s },   // %s" % (n, d, k))
    tab += ["};", ""]
    head = ["// T-547 THE BLANK TABLET's words, from DAEMONS docs/blank-tablet-draft.md by tools/genblanktablet.py --write.",
            "// Edit the draft and run the tool; never this file. Every word DRAFT (the user, 2026-11-12: \"Keep as drafted\").",
            ""]
    return "\n".join(head + decl + tab)


def same(path, im):
    if not os.path.exists(path):
        return False
    old = Image.open(path)
    return old.size == im.size and list(old.getdata()) == list(im.getdata()) and \
        old.getpalette()[:48] == im.getpalette()[:48]


def main():
    os.makedirs(SCRATCH, exist_ok=True)
    out = {STONE: draw_stone(), TOAD: draw_toad()}
    changed = 0
    for path, im in out.items():
        name = os.path.basename(path)
        im.save(os.path.join(SCRATCH, name))
        if same(path, im):
            print("  %-16s unchanged" % name)
            continue
        changed += 1
        if WRITE:
            im.save(path)
            print("  %-16s written" % name)
        else:
            print("  %-16s would change" % name)
    text = words()
    if os.path.exists(WORDS) and open(WORDS).read() == text:
        print("  %-16s unchanged" % "blank_tablet_words.h")
    elif WRITE:
        open(WORDS, "w").write(text)
        print("  %-16s written" % "blank_tablet_words.h")
    else:
        print("  %-16s would change" % "blank_tablet_words.h")
    if not WRITE:
        print("  report only; pass --write (previews in %s)" % SCRATCH)
    return 0


if __name__ == "__main__":
    sys.exit(main())
