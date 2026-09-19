#!/usr/bin/env python3
"""The small overworld objects still drawn as vanilla's (T-167, batch A; vision.md 9.4).

    python3 tools/genmisc.py            # preview to /tmp/misc_ow.png (ours, then vanilla's under it)
    python3 tools/genmisc.py --write    # the ten sheets in place

T-164 measured the sprite server against the overworld and found it hit or miss at 16x16, so these are drawn
here as genprops.py draws its props: EVERY PIXEL AUTHORED, vanilla used only as measurement (size, frame count,
palette slot), never traced -- CLAUDE.md's promise, and genprops.py's first draft is the warning.

WHAT EACH OBJECT IS, in OUR lexicon -- the thing the game calls it is the thing drawn:

    fossil.png        16x16  npc_white  HELIX CORE / DRUM CORE    a platter wound in a spiral groove -- a core, and a helix
    old_amber.png     16x16  npc_blue   OLD CORE                  a gold block with something dark kept inside it
    ruby.png          16x16  npc_blue   PUBLIC KEY                a key, red, that anyone may hold
    sapphire.png      16x16  npc_blue   PRIVATE KEY               the same key in purple, cut differently
    town_map.png      32x16  npc_blue   SITEMAP                   a wall board: one box, and the boxes it branches into
    clipboard.png     16x16  npc_white  a clipboard               the lab's, and the Index's
    lapras_doll.png   32x32  npc_pink   FERRY's doll              the sea turtle of batch 12, stitched and soft
    sign.png          16x16  npc_white  a metal signboard         HEARSAY's icon for a place
    wooden_sign.png   16x16  npc_white  TRAINER TIPS              planks on a post
    gym_sign.png      16x32  npc_white  a BENCHMARK marker        a stone plinth with a plaque -- HEARSAY's icon for a leader

PALETTES ARE FIXED AND SHARED (engine.md trap 17): each object draws from the NPC slot vanilla put it in, and no
colour it lacks may be added -- chosen by ROLE, never by nearest RGB (genprops.py: nearest-RGB turned a pale leaf
into skin). The engine draws shadows. Every sheet is one frame; single-frame 16x16 misc sheets carry no conversion
rule, and the larger ones keep the rule they already have (the sizes are asserted unchanged).
"""
import os, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from genfolk import read_pal, GBA, WHITE
from genleaders import BLUE, PINK

PREVIEW = "/tmp/misc_ow.png"
WRITE = "--write" in sys.argv
MISC = os.path.join(GBA, "graphics/object_events/pics/misc")


def m16(half):
    """a symmetric 16-wide row from its left 8"""
    return half.ljust(8)[:8] + half.ljust(8)[:8][::-1]


# ================================================================ npc_white
# a peach  s S skin  e dark red-brown  T sand  t olive  u dark olive  R orange-red  r red-brown  E darkest brown
# w pale grey  g grey  G dark grey  W white  K black

SIGN = [m16(h) for h in [
    "", " KKKKKKK", " KWWWWWW", " KWgggGW", " KWWWWWW", " KWggWWW", " KWWWWWW", " KWgggGW", " KwwwwwW",
    " KKKKKKK", "   KgK", "   KgK", "   KgK", "   KgK", "   KGK", "    K"]]
SIGN = [r[:15] + ("K" if r[1] == "K" and r[14] != " " else r[15]) for r in SIGN]      # right edge closed

WOODEN = [
    "                ",
    " KKKKKKKKKKKKKK ",
    " KTTTTTTTTTTTeK ",
    " KTEEEETTTTTTeK ",
    " KTTTTTTTTTTTeK ",
    " KrrrrrrrrrrrrK ",
    " KTTTTTTTTTTTeK ",
    " KTTTEEEEEETTeK ",
    " KTTTTTTTTTTTeK ",
    " KeeeeeeeeeeeeK ",
    " KKKKKKKKKKKKKK ",
    "      KrEK      ",
    "      KrEK      ",
    "      KrEK      ",
    "      KrEK      ",
    "      KKKK      ",
]

CLIPBOARD = [
    "                ",
    "      KKKK      ",
    "   KKKKggKKKK   ",
    "  KeKgGGGGgKeK  ",
    "  KeKKKKKKKKeK  ",
    "  KeKWWWWWWKeK  ",
    "  KeKWggggWKeK  ",
    "  KeKWWWWWWKeK  ",
    "  KeKWgggWWKeK  ",
    "  KeKWWWWWWKeK  ",
    "  KeKWggggWKeK  ",
    "  KeKWWWWWWKeK  ",
    "  KeKKKKKKKKeK  ",
    "  KeeeeeeeeeeK  ",
    "   KKKKKKKKKK   ",
    "                ",
]

# HELIX CORE: a platter, wound -- the groove runs inward in a spiral to a dark hub, lit from the upper left.
CORE = [
    "                ",
    "     KKKKKK     ",
    "   KKwwwwwgKK   ",
    "  KwwgggggggGK  ",
    " KwwgwwwwwwggGK ",
    " KwgwggggggwgGK ",
    "KwwgwgwwwwgwgGGK",
    "KwgwgwgKKgwgwGGK",
    "KwgwgwgKKgwgwGGK",
    "KwgwgwwgggwgwGGK",
    " KgwggggggggwGK ",
    " KgwwwwwwwwwwGK ",
    "  KggggggggGGK  ",
    "   KKGGGGGGKK   ",
    "     KKKKKK     ",
    "                ",
]

# A BENCHMARK marker, 16x32: a stone plinth with a plaque, standing on a stepped base.
PLINTH = ["                "] * 3 + [m16(h) for h in [
    "     KKK", "    KwwW", "   KwwwW", "   KwwgW", "   KKKKK", "   KwwgG", "   KwggG", "   KWWWW",
    "   KWggg", "   KWWWW", "   KWggg", "   KWWWW", "   KKKKK", "   KwggG", "   KwggG", "   KwggG",
    "   KwggG", "   KwggG", "   KwggG", "  KKKKKK", "  KwwwgG", " KKKKKKK", " KwwwggG", "KKKKKKKK",
    "KgggGGGG", "KKKKKKKK"]]
PLINTH = (PLINTH + ["                "] * 32)[:32]

# ================================================================ npc_blue
# a peach  s S skin  e red-brown  y yellow  o gold  Y dark gold  v light purple  V purple  D dark purple-grey
# O orange  r red  d dark brown  W white  K black

OLD_CORE = [
    "                ",
    "                ",
    "     KKKKKK     ",
    "   KKyyyyooKK   ",
    "  KyWyyyyyooYK  ",
    "  KyyyyyyoooYK  ",
    " KyyyyddddoooYK ",
    " KyyydKKKdoooYK ",
    " KyyydKKKdooYYK ",
    " KoyyyddddoYYYK ",
    " KooooooooYYYYK ",
    "  KoooooYYYYYK  ",
    "  KKYYYYYYYYKK  ",
    "    KKKKKKKK    ",
    "                ",
    "                ",
]


def key(lit, body, deep, teeth):
    """a key: a ring bow on the left, a shaft, and the cut -- `teeth` is the pattern along the bottom edge"""
    rows = [
        "                ",
        "                ",
        "                ",
        "  KKKK          ",
        " K{L}{L}{B}K         ",
        "K{L}WKK{B}K         ",
        "K{L}K  K{B}KKKKKKKKK",
        "K{B}K  K{B}{B}{B}{B}{B}{B}{B}{B}{D}K",
        "K{B}{B}KK{B}{D}KKKKKKKKK",
        " K{B}{D}{D}{D}K{T}",
        "  KKKK {U}",
        "                ",
        "                ",
        "                ",
        "                ",
        "                ",
    ]
    t = "".join("KK" if c == "1" else "  " for c in teeth)[:9]
    u = "".join("K " if c == "1" else "  " for c in teeth)[:9]
    out = []
    for r in rows:
        r = r.replace("{L}", lit).replace("{B}", body).replace("{D}", deep).replace("{T}", t).replace("{U}", u)
        out.append(r.ljust(16)[:16])
    return out

PUBLIC_KEY = key("O", "r", "d", "10110")      # red, the one handed out
PRIVATE_KEY = key("v", "V", "D", "11011")     # purple, the one kept -- a different cut


# SITEMAP, 32x16: a board on the wall. One box at the top, the lines it branches into, and the boxes below.
SITEMAP = [
    "                                ",
    " KKKKKKKKKKKKKKKKKKKKKKKKKKKKKK ",
    " KDDDDDDDDDDDDDDDDDDDDDDDDDDDDK ",
    " KDWWWWWWWWWWWWWWWWWWWWWWWWWWDK ",
    " KDWWWWWWWWWWKKKKKWWWWWWWWWWWDK ",
    " KDWWWWWWWWWWKVVVKWWWWWWWWWWWDK ",
    " KDWWWWWWWWWWKKKKKWWWWWWWWWWWDK ",
    " KDWWWWWWWWWWWWDWWWWWWWWWWWWWDK ",
    " KDWWWWDDDDDDDDDDDDDDDDDDWWWWDK ",
    " KDWWWWDWWWWWWWDWWWWWWWWWDWWWDK ",
    " KDWWKKKKKWWKKKKKWWWWKKKKKWWWDK ",
    " KDWWKvvvKWWKvvvKWWWWKvvvKWWWDK ",
    " KDWWKKKKKWWKKKKKWWWWKKKKKWWWDK ",
    " KDDDDDDDDDDDDDDDDDDDDDDDDDDDDK ",
    " KKKKKKKKKKKKKKKKKKKKKKKKKKKKKK ",
    "                                ",
]

# ================================================================ npc_pink
# a peach  s S skin  e red-brown  p pink  P rose  m dark rose  c light blue  B blue  n dark navy
# w pale grey  g grey  G dark grey  W white  K black

# FERRY's doll, 32x32: the sea turtle, sewn -- a domed shell in blue with its plates stitched on, a light-blue head
# and flippers, one button eye, a pink cheek because it is a toy. Sitting, so it reads as a doll and not the daemon.
FERRY_DOLL = [
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "            KKKKKKKK            ",
    "          KKBBBBBBBBKK          ",
    "         KBBcBBBBBBcBBK         ",
    "        KBcBBnBBBBnBBcBK        ",
    "       KBBBBnBBBBBBnBBBBK       ",
    "      KBBBnnnnBBBBnnnnBBBK      ",
    "  KKK KBBnBBBBnBBnBBBBnBBK      ",
    " KcccKKBnBBBBBBnnBBBBBBnBK      ",
    "KcWKccKBBnBBBBnBBnBBBBnBBK KKK  ",
    "KcKKccKBBBnnnnBBBBnnnnBBBKKcccK ",
    "KcccpcKnnnnnnnnnnnnnnnnnnKccccK ",
    " KcccKKwwwwwwwwwwwwwwwwwwKKcccK ",
    "  KKKcKwgwgwgwgwgwgwgwgwwKcKKK  ",
    "     KcKwwwwwwwwwwwwwwwwKcK     ",
    "    KccKKwwwwwwwwwwwwwwKKccK    ",
    "   KcccK KKwwwwwwwwwwKK KcccK   ",
    "   KccK    KKKKKKKKKK    KccK   ",
    "    KK                    KK    ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
    "                                ",
]


FERRY_DOLL = ["                                "] * 6 + FERRY_DOLL[:26]      # sits on the cell's floor, as objects stand

SHEETS = [   # name, file, the one frame, letter index, palette
    ("the HELIX CORE",  "fossil.png",      CORE,        WHITE, "npc_white.pal"),
    ("the OLD CORE",    "old_amber.png",   OLD_CORE,    BLUE,  "npc_blue.pal"),
    ("the PUBLIC KEY",  "ruby.png",        PUBLIC_KEY,  BLUE,  "npc_blue.pal"),
    ("the PRIVATE KEY", "sapphire.png",    PRIVATE_KEY, BLUE,  "npc_blue.pal"),
    ("the SITEMAP",     "town_map.png",    SITEMAP,     BLUE,  "npc_blue.pal"),
    ("the clipboard",   "clipboard.png",   CLIPBOARD,   WHITE, "npc_white.pal"),
    ("FERRY's doll",    "lapras_doll.png", FERRY_DOLL,  PINK,  "npc_pink.pal"),
    ("the signboard",   "sign.png",        SIGN,        WHITE, "npc_white.pal"),
    ("TRAINER TIPS",    "wooden_sign.png", WOODEN,      WHITE, "npc_white.pal"),
    ("the BENCHMARK marker", "gym_sign.png", PLINTH,    WHITE, "npc_white.pal"),
]


def check(name, rows, index, w, h):
    assert len(rows) == h, "%s is %d rows, the sheet is %d" % (name, len(rows), h)
    for r, line in enumerate(rows):
        assert len(line) == w, "%s row %d is %d wide, want %d: %r" % (name, r, len(line), w, line)
        bad = set(line) - set(index)
        assert not bad, "%s row %d has %r" % (name, r, bad)


def build(rows, index, pal):
    img = Image.new("P", (len(rows[0]), len(rows)))
    flat = [c for rgb in pal for c in rgb]
    img.putpalette(flat + [0] * (768 - len(flat)))
    px = img.load()
    for y, line in enumerate(rows):
        for x, ch in enumerate(line):
            px[x, y] = index[ch]
    return img


def main():
    tiles, built = [], []
    for name, filename, rows, index, palname in SHEETS:
        old = Image.open(os.path.join(MISC, filename))
        check(name, rows, index, old.width, old.height)            # one frame: the sheet IS the frame
        img = build(rows, index, read_pal(palname))
        assert img.size == old.size
        built.append((filename, img))
        tiles.append((img, old))
    S = 6
    W = sum(max(a.width, b.width) * S + 12 for a, b in tiles)
    H = max(a.height for a, _ in tiles) * S * 2 + 12
    out = Image.new("RGB", (W, H), (60, 60, 60)); x = 0
    for img, old in tiles:
        for k, im in enumerate((img, old)):
            bg = Image.new("RGB", im.size, (150, 150, 150))
            bg.paste(im.convert("RGB"), (0, 0), Image.frombytes("L", im.size, bytes(255 if i else 0 for i in im.getdata())))
            out.paste(bg.resize((im.width * S, im.height * S), Image.NEAREST), (x, k * (H // 2)))
        x += max(img.width, old.width) * S + 12
    out.save(PREVIEW)
    print("  %d sheets -> preview %s (ours above, vanilla's below)" % (len(built), PREVIEW))
    if WRITE:
        for filename, img in built:
            img.save(os.path.join(MISC, filename), bits=4)
        print("  written %d sheets in place: %s" % (len(built), ", ".join(f for f, _ in built)))


if __name__ == "__main__":
    main()
