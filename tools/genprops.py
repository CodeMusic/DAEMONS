#!/usr/bin/env python3
"""The obstacles the field moves clear: the tree, the rock and the boulder (T-124; vision.md 9.4, 9.22).

    python3 tools/genprops.py            # preview to /tmp/props_ow.png (ours, then vanilla's under it)
    python3 tools/genprops.py --write    # the three sheets in place

THREE SHEETS, 210 OBJECTS, and they are not miscellaneous -- they are the three things a field move
removes, and the bible already named all three moves:

    cut_tree.png          4 x 16x16   55 objects   CUT -> PRUNE      "the obstacle is literally a tree"
    rock_smash_rock.png   4 x 16x16   97 objects   ROCK SMASH -> CRACK  "you crack a rock and a problem"
    strength_boulder.png  1 x 16x16   58 objects   STRENGTH -> DISPLACE  push it aside

THE BOULDER IS REACHED BY ANOTHER NAME. There is no OBJ_EVENT_GFX_STRENGTH_BOULDER: the maps place
OBJ_EVENT_GFX_PUSHABLE_BOULDER and graphics_info_pointers.h:291 points it at
gObjectEventGraphicsInfo_StrengthBoulder, which INCBINs strength_boulder.4bpp. Counting the file's own
name found ZERO objects and the sheet looked dead. Twice more in the same hour: sPicTable_RedSurf draws
every frame from gObjectEventPic_RedSurfRun, so red_surf.png is the unused one; and a grep for SURF_RUN
that excluded the pointer tables returned nothing while the answer sat in the excluded file. THE RULE:
a name that finds nothing has not told you the sheet is unused -- follow the pointer table.

WHY THE TREE HAD TO CHANGE. gbatrees.py (T-61) replaced vanilla's conifer across the General tileset
with a round broadleaf, and it is shipped -- 204 of that tileset's 640 tiles differ from vanilla.
Route 2 loads gTileset_General and carries five cut-trees, so our broadleaves and vanilla's dark bush
are on screen together. That is the contradiction this sheet closes.

AND OUR TREE IS THE LIGHT ONE, WHICH IS THE OPPOSITE OF WHAT I FIRST WROTE HERE. Measured off
broadleaf(): LIT 38.5%, LEAF 36.8%, DARK 13.4%, DEEP 11.3% -- three quarters of the crown is in the
two light bands. Vanilla's cut_tree is the reverse, N 52% of its ink. npc_green has no LIT, so both
light roles collapse onto 'l' and IT BECOMES THE BODY COLOUR, not a highlight; 'J' is the underside,
and 'N' is rim only. Luminance confirms the ramp lines up: l 178 / J 111 / N 54 against LEAF 169 /
DARK 110 / DEEP 71.

THE ART HERE IS DRAWN, NOT TRACED, AND THE FIRST ATTEMPT WAS NOT. A draft that "authored vanilla's
structure" came out 97% identical to vanilla -- 248 of 256 cells, twelve of sixteen rows byte for
byte. That is not a conversion, and it would have put Nintendo-derived pixels into THIS repo as source
literals, which is the one thing CLAUDE.md promises not to do. gbatrees.py and gbaground.py do derive
from vanilla pixel by pixel, but they READ it out of engineGba at runtime and transform it; genfolk.py
authors its figures outright. gbacopyright.py lifts vanilla's font pixel-for-pixel and SAYS SO, with a
reason -- the two editions of that screen should be the same object. A tree has no such reason: its
whole job is to stop matching vanilla. So vanilla is used here only as MEASUREMENT -- what the cell
must achieve -- and every pixel below was drawn.

WHAT THE MEASUREMENT SAID, and all of it is obeyed:

  * ONE CONNECTED COMPONENT. Vanilla's tree is a single 161px mass; its crown alone is 95px spanning
    the full width. Four readings of this sprite were wrong before a connected-component pass settled
    it in one line -- a footprint, a dome profile, lobes, then two clumps, each inferred from a
    PROJECTION (per-row widths, a per-colour mask, min/max spans) rather than tested. The "gap" at
    row 2 is a notch in one mass, and it closes at row 3.
  * THE CELL'S THREE BANDS. Crown rows 0-8, trunk 9-12, root flare 13-15, foliage carried down around
    the trunk at row 9 rather than leaving a bare stem.
  * THE ENGINE DRAWS THE SHADOW (.shadowSize = SHADOW_SIZE_S), so no sheet draws one.
  * FRAME 0 IS THE OBSTACLE; 1-3 CLEAR IT. sAnimTable_CutTree and _RockSmashRock hold exactly
    [ANIM_STAY_STILL] and [ANIM_REMOVE_OBSTACLE], running frames 0,1,2,3 -- 6 ticks each for the tree,
    8 for the rock. The boulder's table is sAnim_Inanimate: one frame, pushed rather than destroyed.

THE STONE IS DRAWN AS THIS PROJECT DRAWS A PROP. item_ball.png -- ours, 16x16, in this same palette
slot -- spends four colours and no dither: a hard K outline over flat w / g / G bands. Vanilla's rock
is an olive-and-sand dither (u, t, T) that reads as mossy earth. Grey stone is also SLATE's own
vocabulary, the town whose argument is stone as a writing surface. THE ROCK IS ANGULAR AND FISSURED
and THE BOULDER IS SMOOTH AND ROUND, so the two read apart at a glance -- one is broken open, the
other is shoved aside. A judgment call, nothing in the bible rules on it: revert this file's ROCK and
BOULDER art and rerun to undo.

WHY THE BREAK FRAMES ARE CHUNKY. Vanilla's rock frame 1 is still one dense mass with K fissures driven
through it; only frames 2 and 3 separate, into 10 and 11 components whose largest are 44, 19, 18, 16px
-- shards that keep a lit interior inside their rim. A first draft used 0- and 1-radius blobs, so
every pixel became outline and they read as black asterisks. A shard is at least three across.

PALETTES ARE FIXED AND SHARED. cut_tree draws from npc_green in PALSLOT_NPC_3; the rock and boulder
from npc_white in PALSLOT_NPC_4. Nothing here may use a colour those sixteen do not hold, and
NEAREST-RGB IS THE WRONG WAY TO PICK ONE: asked for the world tree's pale highlight, nearest-distance
in npc_green returns 's', a peach skin tone, because the palette has no pale green and distance
crosses hue freely. Colours are chosen by ROLE. That is the failure that made a moth read as a cow.

CONVERSION RULES. cut_tree and rock_smash_rock already carry `-mwidth 2 -mheight 2` in
spritesheet_rules.mk; they are 64x16 strips and engine.md trap 15 applies to them. strength_boulder
has NO rule and MUST NOT BE GIVEN ONE: every single-frame 16x16 misc sheet goes without (clipboard,
fossil, item_ball, pokedex, ruby, sign, wooden_sign), because one frame in raster order is already
correct, and its .4bpp decodes clean today.

NOTHING IS IMPORTED THAT WRITES. gbatrees.py ends in a bare main() with no __main__ guard -- 21 tools
here do -- so `import gbatrees` RUNS IT, and under `genprops.py --write` its own WRITE flag reads True
off the shared sys.argv and it rewrites the General tileset. An earlier draft imported it to sample
broadleaf(); this one does not import it at all, which is why the numbers above are quoted rather than
computed. See engine.md trap 16.

NO TOOL OWNS pics/misc/. gbabox.py writes item_ball.png because the ball is the BOX's icon and
gbaplayer.py writes surf_blob.png because you ride it; both are side-effects of their own subject.
These three are their own subject and belong here.
"""
import os, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from genfolk import read_pal, GBA, GREEN, WHITE
from genodd import check, build          # guarded by __main__; importing it runs nothing

PREVIEW = "/tmp/props_ow.png"
WRITE = "--write" in sys.argv
MISC = os.path.join(GBA, "graphics/object_events/pics/misc")


# ================================================================ THE TREE (npc_green)
# l = the body, our broadleaf's two light bands collapsed; J = the underside; N = the rim, one pixel.
# e / Y / o = bark. A round crown, lit from above, foliage carried down around the trunk into a flare.
TREE = [
    "     NNNNNN     ",
    "   NllllllllN   ",
    "  NllllllllllN  ",
    " NllllllJlllllN ",
    "NlllllllllJllllN",
    "NllJlllllllllllN",
    "NlllJllllllJlllN",
    " NJllllllllllJN ",
    "  NJJJJJJJJJJN  ",
    "   NJJNeYNJJN   ",
    "      NeYN      ",
    "      NeYN      ",
    "      NeYN      ",
    "    NNeoYoNN    ",
    "   NeooYYooeN   ",
    "    NNNNNNNN    ",
]

# PRUNE lands: a white cut driven down through the crown from the upper right, the tree still whole.
TREE_CUT = [
    "     NNNNNN   l ",
    " l NllllllllN   ",
    "  NllllllllllN  ",
    " NllllllJlWWllN ",
    "NlllllllWWJllllN",
    "NllJllWWlllllllN",
    "NlllJllllllJlllN",
    " NJllllllllllJN ",
    "  NJJJJJJJJJJN  ",
    "   NJJNeYNJJN   ",
    "      NeYN      ",
    "      NeYN      ",
    "      NeYN      ",
    "    NNeoYoNN    ",
    "   NeooYYooeN   ",
    "    NNNNNNNN    ",
]

# The crown comes apart and lifts away; the trunk still stands.
TREE_FALL = [
    " ll       JJ    ",
    " lJ       Jl    ",
    "  l         lJ  ",
    "    JllJ    ll  ",
    "    lllJ        ",
    "  Jl JlJ        ",
    "  lJ  JJ    l   ",
    "      JJ        ",
    "      JJ        ",
    "      NJYN      ",
    "      NeYN      ",
    "      NeYN      ",
    "      NeYN      ",
    "    NNeoYoNN    ",
    "   NeooYYooeN   ",
    "    NNNNNNNN    ",
]

# The last leaves in the air, and the cut stump -- PRUNE leaves a stump, it does not erase a tree.
TREE_STUMP = [
    "                ",
    "  ll            ",
    "  lJ        JJ  ",
    "            Jl  ",
    "                ",
    " J           l  ",
    "                ",
    "      ll        ",
    "      lJ        ",
    "                ",
    "                ",
    "                ",
    "      NNNN      ",
    "    NNeoYoNN    ",
    "   NeooYYooeN   ",
    "    NNNNNNNN    ",
]


# ================================================================ THE ROCK (npc_white)
# Angular and already fissured -- a thing that will be cracked open. K rim, w lit face, g body, G shade.
ROCK = [
    "                ",
    "     KKKKKK     ",
    "   KKwwwKggK    ",
    "  KwwwwKgggK    ",
    " KwwwwwKggggK   ",
    " KwwwwKKgggggK  ",
    "KwwwgKKgggggGK  ",
    "KwwggKgggggGGK  ",
    "KwgggKggggGGGK  ",
    "KgggKKgggGGGGK  ",
    "KgggKgggGGGGGK  ",
    " KggKggGGGGGKK  ",
    " KKKKgGGGGGKK   ",
    "   KKKGGGKKK    ",
    "     KKKKK      ",
    "                ",
]

# CRACK lands: still one mass, but the fissures open right through it.
ROCK_CRACK = [
    "                ",
    "     KKKKKK     ",
    "   KKwwKKggK    ",
    "  KwwwKKgggK    ",
    " KwwwKKKggggK   ",
    " KwwKKKKgggggK  ",
    "KwwgKKKgggggGK  ",
    "KwgKKKgggggGGK  ",
    "KwgKKKgggGGGGK  ",
    "KggKKKggGGGGGK  ",
    "KggKKgggGGGGGK  ",
    " KgKKggGGGGGKK  ",
    " KKKKgGGGGGKK   ",
    "   KKKGGGKKK    ",
    "     KKKKK      ",
    "                ",
]

# It separates into shards -- each at least three across, so each keeps a lit interior.
ROCK_SHARDS = [
    "                ",
    "           KKK  ",
    "          KwggK ",
    "  KKKK     KGGK ",
    " KwwwgK     KK  ",
    " KwgggGK        ",
    " KggGGGK   KKK  ",
    "  KGGGK   KwgK  ",
    "   KKK    KgGK  ",
    "           KK   ",
    "  KKKK          ",
    " KwwggK    KKK  ",
    " KggGGK   KwggK ",
    "  KKKK    KgGGK ",
    "           KKK  ",
    "                ",
]

# The pieces thrown clear, on their way out.
ROCK_GONE = [
    "                ",
    "  KKK           ",
    " KwgK      KK   ",
    " KgGK     KwgK  ",
    "  KK      KgGK  ",
    "           KK   ",
    "     KKKK       ",
    "    KwwggK      ",
    "    KgggGK   KK ",
    "    KggGGK  KwK ",
    "     KKKK    KK ",
    "                ",
    "   KK      KKK  ",
    "  KwK     KwgK  ",
    "   KK     KgGK  ",
    "           KKK  ",
]


# ================================================================ THE BOULDER (npc_white)
# Smooth and whole, because DISPLACE pushes it aside rather than breaking it. Round where the rock is
# angular, so the two never read as the same object.
BOULDER = [
    "                ",
    "     KKKKKK     ",
    "   KKwwwwggKK   ",
    "  KwwwwwgggggK  ",
    " KwwwwwgggggggK ",
    " KwwwwggggggggK ",
    "KwwwwgggggggGGK ",
    "KwwwggggggggGGK ",
    "KwwggggggggGGGK ",
    "KwgggggggggGGGK ",
    "KgggggggggGGGGK ",
    " KgggggggGGGGGK ",
    " KKgggggGGGGGKK ",
    "  KKgggGGGGGKK  ",
    "   KKKGGGGKKK   ",
    "     KKKKKK     ",
]


SHEETS = [   # name, file, frames, letter index, palette
    ("the tree",    "cut_tree.png",         [TREE, TREE_CUT, TREE_FALL, TREE_STUMP], GREEN, "npc_green.pal"),
    ("the rock",    "rock_smash_rock.png",  [ROCK, ROCK_CRACK, ROCK_SHARDS, ROCK_GONE], WHITE, "npc_white.pal"),
    ("the boulder", "strength_boulder.png", [BOULDER], WHITE, "npc_white.pal"),
]


def main():
    rows, built = [], []
    for name, filename, frames, index, palname in SHEETS:
        check(name, frames, index, 16)
        old = Image.open(os.path.join(MISC, filename))
        assert len(frames) == old.width // 16, "%s: %d frames, %s holds %d" % (
            name, len(frames), filename, old.width // 16)
        img = build(frames, index, read_pal(palname), 16)
        assert img.size == old.size, "%s: %s would change size %s -> %s" % (
            name, filename, old.size, img.size)
        built.append((filename, img))
        bg = Image.new("RGB", img.size, (150, 150, 150))
        bg.paste(img.convert("RGB"), (0, 0),
                 Image.frombytes("L", img.size, bytes(255 if i else 0 for i in img.getdata())))
        rows.append(bg)
        rows.append(old.convert("RGB"))
    w = max(r.width for r in rows) * 6
    h = sum(r.height * 6 + 12 for r in rows)
    out = Image.new("RGB", (w, h), (60, 60, 60))
    y = 0
    for r in rows:
        out.paste(r.resize((r.width * 6, r.height * 6), Image.NEAREST), (0, y))
        y += r.height * 6 + 12
    out.save(PREVIEW)
    print("  %d sheets -> preview %s (each: ours, then vanilla's under it)" % (len(built), PREVIEW))
    if WRITE:
        for filename, img in built:
            img.save(os.path.join(MISC, filename), bits=4)
        print("  written %d sheets in place: %s" % (len(built), ", ".join(f for f, _ in built)))
        print("  NOTE strength_boulder keeps NO conversion rule, as every single-frame 16x16 misc sheet does")


if __name__ == "__main__":
    main()
