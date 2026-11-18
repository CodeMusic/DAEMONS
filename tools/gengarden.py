#!/usr/bin/env python3
"""T-585 THE GARDEN OF ECHOES: the three animals at ROUTE 24's grove fir, and what lies beside them.

    python3 tools/gengarden.py            # report: what would change (previews in the scratch folder)
    python3 tools/gengarden.py --write    # the five sheets in engineGba/graphics/object_events/pics/people/

The scene is docs/garden-of-echoes-draft.md, A (the user, 2026-11-17, by multiple choice; vision 3.4). Its scripts and
words are engineGba's data/scripts/garden_of_echoes.inc; the grove's objects and its arrival hook are written by
tools/gbagrove.py (GARDEN), so this tool only draws.

FIVE SHEETS, each 48x16, three 16x16 frames in the order the standard animations read them (south, north, west; east
is west flipped), all in npc_white (PALSLOT_NPC_4), the palette the LARK at the fir already loads there, so nothing on
the map is repainted (engine.md trap 17):

  garden_hare.png    the hare: tan, a white scut, pink in the ears. Its walk frames are its standing ones; it hops
                     (jump_*), so the arc carries the motion.
  garden_magpie.png  the magpie: black and white, the wing slate blue.
  garden_mole.png    the mole, half out of its hole: velvet grey, a pink snout and hands, earth heaped round it.
  garden_sheaf.png   the mole's pages, by the frame: a few (south), a pile (north), a heap (west). The grove sets the
                     sheaf's facing on arrival from VAR_GARDEN_VISITS, so one graphics id is all three.
  garden_stones.png  the cairn with the pale stone on top (south), and the hare's tracks, leading down (north, and
                     west the same). The tracks are this sheet's second frame, placed facing north.

Every pixel is DRAFT, drawn here from nothing.
"""
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PEOPLE = os.path.join(GBA, "graphics/object_events/pics/people")
WHITE_PAL = os.path.join(GBA, "graphics/object_events/palettes/npc_white.pal")
SCRATCH = os.environ.get("DAEMONS_SCRATCH", "/tmp/gengarden")
WRITE = "--write" in sys.argv

# npc_white, by index: 1 peach light, 2 peach, 4 red-brown, 5 tan, 6 olive brown, 7 dark olive, 10 dark brown,
# 11 light grey, 12 grey, 13 slate, 14 white, 15 black.
KEY = {".": 0, "P": 1, "p": 2, "r": 4, "t": 5, "s": 6, "o": 7, "B": 10, "g": 11, "G": 12, "d": 13, "w": 14, "k": 15}

HARE = [
    [   # south: facing the player, both ears up
        "................",
        "....oo....oo....",
        "...otpo..opto...",
        "...otpo..opto...",
        "...otpo..opto...",
        "....otooooto....",
        "....otttttto....",
        "...otkttttkto...",
        "...otttwwttto...",
        "....ottpptto....",
        "...ootttttttoo..",
        "..ottwwwwwwttto.",
        "..otwwwwwwwwtso.",
        "..ostwwwwwwtsso.",
        "...osPPsosPPso..",
        "....oooo.oooo...",
    ],
    [   # north: from behind, the scut showing
        "................",
        "....oo....oo....",
        "...otto..otto...",
        "...otto..otto...",
        "...otto..otto...",
        "....otoooooto...",
        "....otttttto....",
        "...otttttttto...",
        "...otttttttto...",
        "....ostttsto....",
        "...ootttttttoo..",
        "..otttttttttto..",
        "..ottttwwttttso.",
        "..osttwwwwttsso.",
        "...ossswwsssso..",
        "....oooo.oooo...",
    ],
    [   # west: in profile, facing left, the ears laid back
        "................",
        "......ooo.......",
        ".....otppoo.....",
        "......ootppo....",
        "........ootto...",
        "...oooo...oto...",
        "..otttto.oto....",
        ".okttttttto.....",
        "otttttttttsooo..",
        ".oottttttttttso.",
        "...otttttttttswo",
        "...ottttttttswwo",
        "...ostttttsssswo",
        "...ossoossssooo.",
        "..oPPo..osPPo...",
        "..oooo..ooooo...",
    ],
]

MAGPIE = [
    [   # south: round, the beak down, the white flanks
        "................",
        "................",
        "................",
        "......kkkk......",
        ".....kkkkkk.....",
        ".....kGkkGk.....",
        ".....kkddkk.....",
        "......kddk......",
        "....kkkkkkkk....",
        "...kwwkkkkwwk...",
        "...kwwwkkwwwk...",
        "...kdwwkkwwdk...",
        "....kdwwwwdk....",
        ".....kkkkkk.....",
        "......k..k......",
        ".....kk..kk.....",
    ],
    [   # north: the back, white shoulders, the long tail down
        "................",
        "................",
        "................",
        "......kkkk......",
        ".....kkkkkk.....",
        ".....kkkkkk.....",
        "......kkkk......",
        ".....kkkkkk.....",
        "....wkkkkkkw....",
        "....wdkkkkdw....",
        "....ddkkkkdd....",
        ".....dkkkkd.....",
        "......kkkk......",
        "......kddk......",
        "......kddk......",
        ".......kk.......",
    ],
    [   # west: facing left, the tail out behind
        "................",
        "................",
        "................",
        "....kkk.........",
        "..kkkGkk........",
        "....kkkkk.......",
        "....kkkwwk......",
        "....kwwwwdk.....",
        "....kwwwwddkk...",
        "....kwwwwdddkkk.",
        ".....kwwwddkkddk",
        "......kkkkk...kk",
        ".......k.k......",
        ".......k.k......",
        "......kk.kk.....",
        "................",
    ],
]

MOLE = [
    [   # south: half out of the hole, hands on the rim
        "................",
        "................",
        "................",
        "................",
        "................",
        "......kkkk......",
        ".....kGGGGk.....",
        "....kGddddGk....",
        "....kGkddkGk....",
        "....kddddddk....",
        "..PP.kdppdk.PP..",
        ".pPPkddppddkPPp.",
        ".rrsskdddddkssr.",
        "rssBBBBBBBBBBssr",
        "rsssssssssssssr.",
        ".rrrrrrrrrrrrrr.",
    ],
    [   # north: the back of it, no snout
        "................",
        "................",
        "................",
        "................",
        "................",
        "......kkkk......",
        ".....kGGGGk.....",
        "....kGGGGGGk....",
        "....kGddddGk....",
        "....kddddddk....",
        "....kddddddk....",
        "....kddddddk....",
        ".rrsskddddkssr..",
        "rssBBBBBBBBBBssr",
        "rsssssssssssssr.",
        ".rrrrrrrrrrrrrr.",
    ],
    [   # west: the snout to the left
        "................",
        "................",
        "................",
        "................",
        "................",
        ".......kkkk.....",
        "......kGGGGk....",
        "....kkGdddGGk...",
        "..pppkkddddGk...",
        "...pkddddddGk...",
        "..PP.kddddddk...",
        ".PPPkddddddddk..",
        ".rrsskdddddkssr.",
        "rssBBBBBBBBBBssr",
        "rsssssssssssssr.",
        ".rrrrrrrrrrrrrr.",
    ],
]

SHEAF = [
    [   # south: a few pages
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "...GGGGGGGG.....",
        "..GwwwwwwwwG....",
        "..GwGGGwGGwGGG..",
        "...GwwwwwwwwwwG.",
        "....GwGGwGGGwG..",
        ".....GGGGGGGG...",
    ],
    [   # north: a pile
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "....GGGGGGGG....",
        "...GwwwwwwwwG...",
        "...GwGGwGGGwG...",
        "..GGwwwwwwwwGG..",
        "..GwwGGwGGwwwG..",
        "..GgwwwwwwwwgG..",
        "..GwGGGwGGwGwG..",
        "..GgwwwwwwwwgG..",
        "...GGGGGGGGGG...",
    ],
    [   # west: a heap, pages sliding off it
        "................",
        "................",
        "................",
        ".....GGGGGG.....",
        "....GwwwwwwG....",
        "....GwGGwGwGG...",
        "...GGwwwwwwwwG..",
        "...GwGGwGGwGwG..",
        "..GGwwwwwwwwwGG.",
        "..GwwGGwGGGwwwG.",
        ".GgwwwwwwwwwwwgG",
        ".GwGGwGGGwGGwwwG",
        ".GgwwwwwwwwwwwgG",
        "GwwGwGGwGGwGwGwG",
        "GgwwwwwwwwwwwwwG",
        ".GGGGGGGGGGGGGG.",
    ],
]

STONES = [
    [   # south: the cairn, the pale stone on top
        "................",
        "................",
        "................",
        "................",
        "......dddd......",
        ".....dwwwwd.....",
        ".....dwwwgd.....",
        "......dddd......",
        ".....dGGGGd.....",
        "....dGgGGGGd....",
        "....dGGGGGdd....",
        "...ddddddddd....",
        "..dGGgGddGGGd...",
        "..dGGGGddGGGGd..",
        "..ddGGGddGGGdd..",
        "...ddddddddddd..",
    ],
    [   # north: the hare's tracks, leading down and out
        "................",
        "...s.s..........",
        "...s.s..........",
        "....s...........",
        "......ss.ss.....",
        "......ss.ss.....",
        "......ss.ss.....",
        "........s.......",
        "...ss.ss........",
        "...ss.ss........",
        "...ss.ss........",
        ".....s..........",
        "........ss.ss...",
        "........ss.ss...",
        "........ss.ss...",
        "..........s.....",
    ],
]
STONES.append(STONES[1])   # west: the tracks again (the north frame is the one placed)

SHEETS = {
    "garden_hare.png": HARE,
    "garden_magpie.png": MAGPIE,
    "garden_mole.png": MOLE,
    "garden_sheaf.png": SHEAF,
    "garden_stones.png": STONES,
}


def read_pal(path):
    lines = open(path).read().split()
    n = int(lines[2])
    vals = [int(v) for v in lines[3:3 + 3 * n]]
    return vals + [0] * (768 - len(vals))


def draw(frames):
    pal = read_pal(WHITE_PAL)
    im = Image.new("P", (16 * len(frames), 16), 0)
    im.putpalette(pal)
    for f, rows in enumerate(frames):
        assert len(rows) == 16, "a frame is 16 rows"
        for y, row in enumerate(rows):
            #  a stray space or a lookalike letter is read as transparent: the grids are typed by hand
            row = row.replace(" ", ".").replace("о", "o")
            row = (row + "." * 16)[:16]
            for x, ch in enumerate(row):
                im.putpixel((f * 16 + x, y), KEY.get(ch, 0))
    return im


def same(path, im):
    if not os.path.exists(path):
        return False
    old = Image.open(path)
    return old.size == im.size and list(old.getdata()) == list(im.getdata()) and \
        old.getpalette()[:48] == im.getpalette()[:48]


def main():
    os.makedirs(SCRATCH, exist_ok=True)
    changed = 0
    for name, frames in SHEETS.items():
        im = draw(frames)
        im.save(os.path.join(SCRATCH, name))
        path = os.path.join(PEOPLE, name)
        if same(path, im):
            print("  %-18s unchanged" % name)
            continue
        changed += 1
        if WRITE:
            im.save(path)
            print("  %-18s written" % name)
        else:
            print("  %-18s would change" % name)
    if not WRITE:
        print("  report only; pass --write (previews in %s)" % SCRATCH)
    return 0


if __name__ == "__main__":
    sys.exit(main())
