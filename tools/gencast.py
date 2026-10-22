#!/usr/bin/env python3
"""The T-439 cast: the eleven sprites no map placed, drawn as new people (vision.md 9.4, the fable rule).

    python3 tools/gencast.py                  # report: who each one is, its frames, its palette, does it fit
    python3 tools/gencast.py --draft [DIR]    # the sheets and palettes as PNG/.pal in DIR (gfx/drafts/t439/)
    python3 tools/gencast.py --sheets DIR     # the contact sheets: vanilla beside ours at 4x, and each over its map at 2x
                                              #   (--before OLD adds t439_draw_fix.png: the moth and secretary bird
                                              #   against an earlier draft's sheets in OLD)
    python3 tools/gencast.py --write          # into the engine -- NOT YET: the cast is a draft until the user has
                                              #   seen the sheets (then --write --approved)

WHO, AND WHY THAT ANIMAL (the user's choices, T-439, 2026-10-22; docs/private/plan-cast-2026-10-22.md):

    cameraman                 a KINGFISHER photographer   HALFTONE -- the bluest bird, in the town that shows no blue
    unused_woman              a PEPPERED MOTH             HALFTONE -- coloured by her surroundings, and back again
    rich_boy                  a young ERMINE              RESORT SUBLIME -- the fur of kings; a coat the season changes
    sitting_boy               a SLOTH, seated             DOLDRUM's water -- the animal that is still on purpose
    teachy_tv_host            a MYNAH                     CALLOW's centre -- repeats every STREAM it has heard
    unused_male_receptionist  a SECRETARY BIRD            UMBRA, the REVIEW BOARD's door -- takes everything down
    unused_man                a PTARMIGAN whitewasher     BLANCHE -- white for winter and back again
    deoxys_a                  PROTEUS, all edges          THE ANNEX, CONTENT -- hood thrown back, blades out
    deoxys_d                  PROTEUS, a shell            THE ANNEX, CONTEXT -- hood drawn shut, curled like a cocoon
    red_surf                  a MUSKRAT in a reed boat    DOLDRUM's water, becalmed (both editions)
    green_surf                a GREAT CRESTED GREBE       SEAFADE, with her chick riding on her back (both editions)

HOW THEY ARE DRAWN. Exactly as gentowns.py / gennamed.py / genfolk.py draw everyone else: a head (gentowns'
parametric MAMMAL or BIRD head, or one drawn by hand where the species needs it) on the shared torso, species
carried by marks, overlays for tails, crests and tools, and genfolk.figure()'s walk -- the figure drops a row,
swings its arms against its legs and lifts a foot. FRAME COUNTS ARE VANILLA'S: each sheet holds as many 16x32
frames as the vanilla sheet it replaces (nine where it walks, three where it stands), in vanilla's order --
S, N, W, then S-walk x2, N-walk x2, W-walk x2; east is the west frames flipped by the engine.

  sitting_boy is the SEATED layout: three frames, and its pic table reads them S=0, N=2, W=1. Vanilla's frame 2 was
  a copy of frame 0; ours is the sloth's back, because he sits facing the water.

  red_surf / green_surf are 32x32, nine frames in vanilla's layout: S, S, N, N, W, W (each pair a bob) and then
  three more, S N W. Vanilla's last three were the rider alone; ours are the rider AT REST -- no wake, the muskrat
  becalmed and the grebe's chick asleep -- so a script can show him going nowhere before the mark and drifting after.

  deoxys_a / deoxys_d are 32x32, two frames, drawn in the PSYCHIC type palette's indices (daemon_type_psychic.pal,
  which deoxys_n already uses; gbaowslots.py patches it at spawn, T-133), from our hooded PROTEUS (T-176):
  ATTACK throws the hood back and puts the blades out; DEFENSE draws the hood shut and curls into a shell.

PALETTES (engine.md trap 17: a sheet keeps one tag per slot). Most draw from a palette a slot already has, so no
colour changes anywhere: the KINGFISHER and the MOTH from npc_pink, the MYNAH from npc_blue, the SECRETARY BIRD and
the GREBE from npc_white, the SLOTH and the MUSKRAT from DOLDRUM's own (npc_town_doldrum, the tag DOLDRUM's locals
already hold in PALSLOT_NPC_SPECIAL, so they contend with nothing there). The ERMINE and the PTARMIGAN each carry a
palette of their own -- a SUMMER and a WINTER .pal over the same sheet, the coat on letters nothing else uses -- and
need a new tag in a slot their map leaves free.

  SEASONS DO NOT REACH SPRITES TODAY. src/data/season_palettes.h (tools/gbaseasons.py) recolours gTileset_General's
  BG palette only; no object palette follows DaemonsSeason(). So the winter coat needs one engine step: either two
  graphics ids (summer, winter) picked at map load through VAR_OBJ_GFX_ID_x, or a patch at spawn in the manner of
  TryPatchDaemonTypePalette choosing the winter .pal when DaemonsSeason() == SEASON_WINTER. The drawing is ready
  for either: only the .pal changes.

Every in-game word this cast says is DRAFT and lives in the proposal, not here: this tool draws.
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daemonslib
from genfolk import overlay, figure, check, sheet, read_pal, mirror, WHITE, PEOPLE, GBA
from genleaders import H, S, BLUE, PINK
from gentowns import mammal, bird, fig, put, pad, TAIL, CANE_X, LETTERS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POKEMON = os.path.join(GBA, "graphics/object_events/pics/pokemon")
PALDIR = os.path.join(GBA, "graphics/object_events/palettes")
DRAFT_DEFAULT = os.path.join(ROOT, "gfx/drafts/t439")
PREVIEW = daemonslib.preview("cast_ow.png")      # /tmp/cast_ow.png

ARGS = sys.argv[1:]
WRITE = "--write" in ARGS


def argval(flag):
    if flag in ARGS:
        i = ARGS.index(flag)
        if i + 1 < len(ARGS) and not ARGS[i + 1].startswith("--"):
            return ARGS[i + 1]
        return ""
    return None


DRAFT = argval("--draft")
if DRAFT == "":
    DRAFT = DRAFT_DEFAULT
SHEETS = argval("--sheets")

DOLDRUM = dict(LETTERS)      # npc_town_doldrum: a pale blue  b blue  c navy  d grey  e orange  f brown  g dark brown
                             #   h tan  i cream  j sand  k red  l lilac  m dark lilac  W RUST (AL's, not white)  K black
PSY = {" ": 0, **{str(i): i for i in range(1, 10)}}   # daemon_type_psychic: 1..4 the ramp light to dark, 5 the line,
                                                       #   6 white, 7..9 greys


def grid(rows, w):
    """'.' is clear; every row padded to w"""
    return [r.replace(".", " ").ljust(w)[:w] for r in rows]


def halves(rows):
    """a left half drawn to sixteen, mirrored to thirty-two; a row that stops on a colour carries it to the middle"""
    return mirror([(r + (r[-1] if r[-1] not in ". " else ".") * 16)[:16] for r in rows])


# ============================================================ the KINGFISHER photographer (cameraman.png, npc_pink)
# npc_pink: a s S peach  e dark brown  p pink  P rose  m dark rose  c light blue  B blue  n navy  w g G greys  W  K
# The bluest bird there is -- crown and wings in the slot's two blues, the rufous cheek and breast in its peach, a
# white throat, a long dark bill; a photographer's grey vest open over the breast and a camera on a strap.
_h = bird("B", "S", "n", "S")
_h = (put(put(put(put(_h[0], 2, 5, "c"), 3, 4, "c"), 3, 6, "c"), 7, 6, "W"),    # the crown's pale flecks; a white chin
      put(put(put(put(put(_h[1], 2, 5, "c"), 3, 4, "c"), 4, 6, "c"), 7, 5, "B"), 7, 6, "B"),
      put(put(put(_h[2], 2, 6, "c"), 3, 7, "c"), 5, 4, "W"))
_f, _b, _s = fig(_h, "B", "ggSS", "n", "P", "m")
_s = overlay(_s, 4, ["Knnn", " Knn"], 0)                           # the dagger bill, in profile
_b = overlay(_b, 7, ["     BBBB", "      BB"], 0)                      # blue down the back of the neck
_b = overlay(_b, 9, ["    gggggggg"], 0)
_b = overlay(_b, 10, ["    gggggggg", "    gggggggg", "    gggggggg"], 0)   # the vest's back
_f = overlay(_f, 9, [" K    K", "  KKKK", "  KGGK", "  KwGK", "  KKKK"], 4)   # the strap, and the camera at the chest
_s = overlay(_s, 10, ["KKK", "wGK", "KKK"], 3)
_b = overlay(_b, 9, ["    KK"], 5)                                   # the strap over the shoulders
KINGFISHER = (_f, _b, _s)

# ============================================================ the PEPPERED MOTH (unused_woman.png, npc_pink)
# Speckled wings worn as a shawl, a pale furred face, big black eyes, two feathered antennae. She reads grey in
# HALFTONE by design: so does her story.
# T-439 (the user, 2026-10-22): unmistakably a moth FROM THE FRONT -- the antennae feathered and spread wide, the
# pepper dark and clear on pale, and the wings standing out behind her shoulders, so the head is drawn by hand.
_ant = ["KGK     ", " KGK    ", "  KGK KK"]                             # feathered, spread wide, meeting the crown
_mf = _ant + ["   KwWWW", "  KwKKWW", "  KwKKww", "  Kwwwww", "   KwwWW", "    KKWW"]   # big black eyes, a fluffy collar
_mb = _ant + ["   Kwwww", "  Kwwwww", "  Kwwwww", "  Kwwwww", "   Kwwww", "    KKww"]
_ms = ["   KGK", "    KGK", "     KGKK", "     KwwwK", "    KwwwwwK", "   KwKKwwwK", "  KwwKKwwwK",
       "   KwwWWwK", "     KKWK"]
_f, _b, _s = fig((_mf, _mb, _ms), "W", "WWWW", "G", "g", "K")
_wings = mirror(["KKWWKWWW", "KWKWWWKW", "KWWWKWWW", "KKWWWWKW", " KWKWWGG", "  KKKGGG"])   # the shawl, wing-wide
_f = overlay(_f, 9, _wings, 0)
_f = put(put(put(_f, 10, 9, "G"), 12, 5, "G"), 11, 11, "K")          # and the pepper, never quite even
_b = overlay(_b, 9, ["KKWWWWWWWWWWWWKK", "KWGWWKWWWWGWWKWK", "KWWKWWWGWWWWKWWK", "KKWWGWWWWKWWGWKK",
                     " KWWWWKWWWGWWWK ", "  KKKWWWWWWKKK  ", "     KKKKKK     "], 0)   # the wings, folded down her back
_s = overlay(_s, 9, ["  KKWWK", " KWKWWGWK", " KWWWKWWWK", "  KWGWWWGWK", "   KWWKWWK", "    KKKKK"], 2)
MOTH = (_f, _b, _s)

# ============================================================ the young ERMINE (rich_boy.png, a palette of his own)
# a fur  b fur shade  -- the two letters the WINTER .pal turns white; nothing else draws from them
ERMINE_SUMMER = [(176, 120, 64), (120, 76, 40), (248, 240, 216), (40, 32, 32), (120, 56, 136), (80, 32, 96),
                 (232, 192, 72), (248, 248, 248), (216, 208, 184), (160, 148, 120), (232, 136, 144), (96, 56, 32),
                 (64, 48, 48)]
ERMINE_WINTER = [(248, 248, 244), (208, 212, 224)] + ERMINE_SUMMER[2:]
# c cream  d the tail's black tip  e royal purple  f deep purple  g gold  h white  i cream twill  j its shade
# k pink nose  l brown shoe  m dark brown
_h = mammal("a", "b", "c")
_h = (put(put(_h[0], 6, 7, "k"), 5, 3, "c"), _h[1], put(_h[2], 6, 1, "k"))   # the cream runs up his cheek
_f, _b, _s = fig(_h, "e", "eegh", "f", "a", "l")
_b = [r.replace("g", "e").replace("h", "e") if 9 <= i <= 12 else r for i, r in enumerate(_b)]   # the jacket's back
_f = overlay(_f, 9, ["KffK"], 6)                                     # a bow tie
_f = put(put(_f, 11, 6, "g"), 12, 9, "g")                            # brass buttons, off true like a boy's
_b = overlay(_b, TAIL + 1, ["KaK", "KbaK", " KaK", " KdK", " KdK", "  K"], 11)   # the long tail, black at the end
_s = overlay(_s, TAIL, ["KaK", "KbaK", " KddK", "  KK"], 10)
ERMINE = (_f, _b, _s)

# ============================================================ the SECRETARY BIRD (unused_male_receptionist.png, npc_white)
# npc_white: a s S peach  e red-brown  T sand-gold  t olive  u dark olive  R orange-red  r red-brown  E darkest brown
#            w pale grey  g grey  G dark grey  W white  K black
# Pale grey, the bare orange face, a hooked bill, the quills behind the head he is named for, black thighs as
# trousers and the long legs; a grey waistcoat and a black tie at the desk.
# T-439 (the user, 2026-10-22): the crest must read as QUILLS, not ears -- separate dark strokes raked back and out
# behind both cheeks -- with the bare orange face and the hooked bill. The head is drawn by hand for it.
_sf = ["K       ",
       " G      ",
       "K G  KKK",      # three quills a side, each its own stroke, raked out from behind the crown
       " G  Kwww",
       "K GKwwww",
       " GKRKRww",      # the bare orange face round the eye
       "  KRRRGG",      # the bill, broad at the base
       "   KwwwG",
       "    KKwK"]      # and its hook, dropping at the middle
_sb = ["K       ", " G      ", "K G  KKK", " G  Kwww", "K GKwwww", " GKwwwww", "  Kwwwww", "   Kwwww", "    KKww"]
_ss = ["          K K", "         G G", "     KKKKG  K", "    KwwwwKGG", "   KwRKwwwK", " KGRRRwwwwK", "  KGKwwwwK",
       "     KwwwK", "     KwwK"]
_f, _b, _s = fig((_sf, _sb, _ss), "G", "gWWW", "K", "w", "G")
_f = overlay(_f, 9, ["KK"], 7)                                       # the tie
_f = overlay(_f, 10, ["KK"], 7)
_b = [r.replace("W", "g") if 9 <= i <= 12 else r for i, r in enumerate(_b)]   # the waistcoat's back
SECRETARY = (_f, _b, _s)

# ============================================================ the PTARMIGAN whitewasher (unused_man.png, a palette of his own)
# a plumage  b its shade  c its light  -- the three the WINTER .pal turns white
PTARMIGAN_SUMMER = [(168, 120, 72), (104, 72, 44), (216, 184, 136), (248, 248, 240), (216, 56, 48), (88, 124, 184),
                    (56, 80, 128), (176, 128, 72), (240, 240, 228), (152, 152, 160), (96, 96, 104), (56, 48, 40),
                    (32, 32, 36)]
PTARMIGAN_WINTER = [(248, 248, 244), (212, 216, 228), (248, 248, 244)] + PTARMIGAN_SUMMER[3:]
# d white (wings, feathered feet)  e the red comb  f denim  g its shade  h the brush's handle  i whitewash
# j k bucket greys  l bill  m the black tail he keeps all year
_h = bird("a", "c", "l", "c")
_h = (put(_h[0], 3, 4, "e"), put(_h[1], 3, 3, "e"), put(_h[2], 3, 5, "e"))   # the red comb over each eye
_h = (put(put(_h[0], 2, 5, "b"), 6, 4, "b"), put(put(put(_h[1], 3, 5, "b"), 5, 4, "b"), 6, 6, "b"),
      put(_h[2], 5, 6, "b"))                                         # summer's mottle
_f, _b, _s = fig(_h, "d", "ffff", "f", "d", "d")
_cap = ["     KKKKKK     ", "    KiiiiiiK    ", "   KiiiiiiiiK   "]
_f = overlay(_f, 0, _cap, 0)                                         # a painter's paper cap
_b = overlay(_b, 0, _cap, 0)
_s = overlay(_s, 0, ["      KKKK", "     KiiiiK", "    KiiiiiiK"], 0)
_f = overlay(_f, 9, ["   c      c"], 2)                               # the bib's straps over a pale breast
_f = overlay(_f, 9, ["cc"], 7)
_f = put(put(put(_f, 13, 5, "i"), 15, 9, "i"), 11, 10, "i")          # whitewash, everywhere but the fence
_f = overlay(_f, 6, ["KKK", "KiK", "KiK", "KhK", " hK", " hK", " hK", " hK", " hK", " hK", " hK", " KK"], 13)
_b = overlay(_b, TAIL, ["KmmK", " KK "], 6)
_s = overlay(_s, TAIL, ["KmK", " K"], 10)
PTARMIGAN = (_f, _b, _s)

# ============================================================ the MYNAH (teachy_tv_host.png, npc_blue)
# npc_blue: a s S peach  e brown-red  y yellow  o gold  Y dark gold  v light purple  V purple  D dark purple-grey
#           O orange  r red  d dark brown  W  K
# Glossy dark, the yellow wattle behind the eye, an orange bill, the white wing flash; a STREAM fan's tee.
_h = bird("D", "y", "O")
_h = (put(put(_h[0], 4, 3, "y"), 6, 3, "y"), _h[1], put(put(_h[2], 3, 7, "y"), 4, 6, "y"))
_f, _b, _s = fig(_h, "D", "vvvv", "d", "y", "o")
_f = overlay(_f, 10, ["KWWK", "KrWK", "KKKK"], 6)                    # the STREAM's little screen, on his chest
_f = put(put(_f, 11, 2, "W"), 11, 13, "W")                           # the white flash in each wing
_b = put(put(_b, 11, 2, "W"), 11, 13, "W")
_b = overlay(_b, 10, ["KvvK"], 6)
_s = put(_s, 10, 5, "W")
MYNAH = (_f, _b, _s)

# ============================================================ the SLOTH, seated (sitting_boy.png, DOLDRUM's palette)
# Shaggy brown, the pale face and the dark band through the eyes, long arms round his knees and the claws laced
# over them; a striped swim tee and navy shorts. Sitting is the whole of what he does.
SLOTH_S = mirror([
    "        ", "        ", "        ", "        ", "        ", "        ", "        ", "        ", "        ", "        ",
    "        ",
    "     KKK",
    "    Kfff",
    "   Kffhh",
    "   Kfgii",
    "   KgKgi",    # the eye in its dark band
    "   Kfgii",
    "    Kfig",    # the nose
    "    KKii",
    "   Kfbab",    # long arms round a striped tee
    "  Kffaba",
    "  KfKbab",
    "  KfKccc",
    "  KjjKcc",    # the claws, laced over the knees
    "  KKjjKf",
    "   Kfffh",
    "   Kffhh",
    "   KjjKK",    # and the feet's claws
    "    KK  ",
    "        ", "        ", "        ",
])
SLOTH_N = mirror([
    "        ", "        ", "        ", "        ", "        ", "        ", "        ", "        ", "        ", "        ",
    "        ",
    "     KKK",
    "    Kfff",
    "   Kffff",
    "   Kfgfg",
    "   Kgfgf",
    "   Kgfgg",
    "    Kfff",
    "    KKff",
    "   Kfbab",
    "  Kffbab",
    "  Kffbab",
    "  KffKba",
    "  KjfKcc",
    "  KKKccc",
    "   KKKcc",
    "    KKKK",
    "        ", "        ", "        ", "        ", "        ",
])
SLOTH_W = [s.ljust(16) for s in [
    "", "", "", "", "", "", "", "", "", "", "",
    "      KKKK",
    "     KffffK",
    "    KhhfffffK",
    "   KiigffffK",
    "   KgKgfffK",
    "  KiiigfffK",
    "  KgiiffffK",
    "   KKiifffK",
    "     KKbabK",
    "    KfffabaK",
    "   KjjfKbabK",
    "   KjjKcccccK",
    "   KffffcccK",
    "  KjffffhKKK",
    "  KjjKKKhK",
    "   KK  KK",
    "", "", "", "", "",
]]
SLOTH = [grid(SLOTH_S, 16), grid(SLOTH_W, 16), grid(SLOTH_N, 16)]      # FILE order: pic 0 S, pic 1 W, pic 2 N


# ============================================================ the riders, 32x32 (red_surf / green_surf)
def canvas(n=32):
    return [" " * n for _ in range(n)]


def stamp(rows, part, top, left):
    """paste a sprite part: its spaces are clear"""
    rows = list(rows)
    for i, line in enumerate(part):
        y = top + i
        if not 0 <= y < len(rows) or not line.strip():
            continue
        r = list(rows[y])
        for j, ch in enumerate(line):
            if ch != " " and 0 <= left + j < len(r):
                r[left + j] = ch
        rows[y] = "".join(r)
    return rows


def ellipse(rows, cx, cy, rx, ry, fill, stripe=None, every=2):
    """a filled ellipse with its own black line; `stripe` every other row (bundled reeds)"""
    rows = [list(r) for r in rows]
    inside = lambda x, y: ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1.0
    for y in range(len(rows)):
        for x in range(len(rows[0])):
            if inside(x, y):
                edge = any(not inside(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                rows[y][x] = "K" if edge else (stripe if stripe and (y - int(cy)) % every == 0 else fill)
    return ["".join(r) for r in rows]


def shift(rows, dy=0, dx=0):
    n = len(rows)
    out = [" " * len(rows[0])] * n
    out = [rows[y - dy] if 0 <= y - dy < n else " " * len(rows[0]) for y in range(n)]
    if dx:
        out = [(" " * dx + r[:-dx]) if dx > 0 else (r[-dx:] + " " * -dx) for r in out]
    return out


def upper(head, arm, shirt, side=False):
    """a head and the top four rows of the shared torso: what shows of a rider above the boat"""
    f, b, s = fig(head, arm, shirt, shirt, arm, arm)
    return f[:13], b[:13], s[:13]


# --- the MUSKRAT in a reed boat (DOLDRUM's palette): brown, small round ears, a tan muzzle, a straw hat, a blue
#     waistcoat; the boat bundled reeds in sand and tan, bound in brown, both ends curling up. Becalmed.
_mh = mammal("f", "g", "h")
_mh = (put(_mh[0], 6, 7, "g"), _mh[1], put(_mh[2], 6, 1, "g"))
_mf, _mb, _ms = upper(_mh, "f", "bbab")
_hat = ["    KKKKKKKK    ", "   KjjjjjjjjK   ", " KKjjggggggjjKK ", "KjjjjjjjjjjjjjjK", " KKKKKKKKKKKKKK "]
_hat_s = ["     KKKKKK", "    KjjjjjjK", "   KjgggggjK", " KjjjjjjjjjjjK", "  KKKKKKKKKKK"]
_mf, _mb = overlay(_mf, 0, _hat, 0), overlay(_mb, 0, _hat, 0)
_ms = overlay(_ms, 0, _hat_s, 0)


def reed_boat(view):
    c = canvas()
    if view == "side":
        c = ellipse(c, 16, 23, 13.5, 3.6, "j", "h")
        c = stamp(c, ["KK", "KjK", "KjjK", " KjjK", " KjhK", "  KjK"], 16, 1)          # the prow, curling up
        c = stamp(c, ["   KK", "  KjK", " KjjK", "KjhK", "KjK"], 17, 26)               # the stern
        for x in (9, 16, 23):                                                           # the bindings
            c = stamp(c, ["g", "g", "g"], 22, x)
    else:
        c = ellipse(c, 16, 23, 11, 4.2, "j", "h")
        for x in (8, 23):
            c = stamp(c, ["g", "g", "g", "g"], 21, x)
    return c


def end_curl(view):
    """the near end of the boat, drawn over the rider: the prow from the front, the stern from behind"""
    if view == "front":
        return ["  KK  ", " KjjK ", " KjhK ", "KjjjjK", "KhjjhK", " KKKK "]
    return ["  KK  ", " KjjK ", "KjhjjK", " KKKK "]


def wake(c, view, phase):
    """ripples off the hull while it moves; nothing at rest"""
    if view == "side":
        ripple = [(26, 0, "aab"), (27, 3, "bb"), (26, 28, "baa"), (27, 26, "bb")]
    else:
        ripple = [(26, 3, "aab"), (27, 6, "bb"), (26, 26, "baa"), (27, 24, "bb")]
    for y, x, s in ripple:
        c = stamp(c, [s], y + phase, x - phase if x < 16 else x + phase)
    return c


def muskrat(view, phase, rest=False):
    c = reed_boat("side" if view == "side" else "front")
    body = {"front": _mf, "back": _mb, "side": _ms}[view]
    lift = 0 if rest else phase
    c = stamp(c, body, 8 + lift, 8)                         # he sits in it: the gunwale hides him from the waist
    c = stamp(c, reed_boat("side" if view == "side" else "front")[21:], 21, 0)
    if view == "front":
        c = stamp(c, end_curl("front"), 21, 13)
    elif view == "back":
        c = stamp(c, end_curl("back"), 22, 13)
        c = stamp(c, ["KffK", " KgK", "  K"], 21, 22)      # his flat tail over the side
    else:
        c = stamp(c, ["KffK", "KfggK", " KKgK"], 20, 21)   # the tail, trailing over the stern
    if not rest:
        c = wake(c, view, phase)
    return c


# --- the GREAT CRESTED GREBE with her chick (npc_white). Grey-brown back, a white face and front, the black
#     double crest, the chestnut ruff edged dark, a red eye; a sand-gold shawl. Her chick rides between her wings,
#     humbug-striped, as grebe chicks do. She is the boat.
def grebe_head(view):
    if view == "front":
        return ["   KK      KK   ",
                "  KGKK    KKGK  ",
                "   KGGKKKKGGK   ",
                "   KGGGGGGGGK   ",
                "  KWWKWWWWKWWK  ",
                " KRWWRWWWWRWWRK ",
                " KRRWWWGGWWWRRK ",
                " KrRRWWGGWWRRrK ",
                "  KrRRWWWWRRrK  ",
                "   KKKWWWWKKK   ",
                "      KWWK      ",
                "      KWWK      "]
    if view == "back":
        return ["   KK      KK   ",
                "  KGKK    KKGK  ",
                "   KGGKKKKGGK   ",
                "   KGGGGGGGGK   ",
                "  KGGGGGGGGGGK  ",
                " KRGGGGGGGGGGRK ",
                " KRRGGGGGGGGRRK ",
                " KrRRGGGGGGRRrK ",
                "  KrRRGGGGRRrK  ",
                "   KKKGGGGKKK   ",
                "      KGGK      ",
                "      KGGK      "]
    return ["      KK  KK    ",
            "     KGGKKGGK   ",
            "     KGGGGGGK   ",
            "  KKKWWGGGGK    ",
            "KGGGWRKWGGGK    ",       # the long bill and the red eye
            " KKKWWWWRRGK    ",
            "    KWWWRRRrK   ",
            "    KWWWRRrK    ",
            "     KWWWKK     ",
            "     KWWWK      ",
            "     KWWWK      ",
            "     KWWWK      "]


def chick(asleep, view):
    eye = "K" if not asleep else "W"
    if view == "side":
        return [" KK ", "KWKWK", "R" + eye + "WKK", "KKWK"]
    return [" KKK ", "KWKWK", "K" + eye + "W" + eye + "K", " KRK "]


def grebe(view, phase, rest=False):
    c = canvas()
    lift = 0 if rest else phase
    if view == "side":
        c = ellipse(c, 17, 23, 11.5, 4.2, "g", None)
        c = stamp(c, ["   GGGGGG", "  GGgggGGG", " GgggggggGG"], 20, 15)          # the folded wings
        c = stamp(c, grebe_head("side"), 9 + lift, 4)
        c = stamp(c, ["KTTTTK", "KTTTTTK"], 19 + lift, 9)                         # the shawl
        c = stamp(c, chick(rest, "side"), 15 + (2 if rest else 0) + lift, 19)
        c = stamp(c, ["KKK", "WWWK", "WWK"], 22, 6)                               # the white breast at the water
    else:
        c = ellipse(c, 16, 23, 10.5, 4.6, "G" if view == "back" else "g", None)
        if view == "front":
            c = stamp(c, ["  WWWWWW  ", " WWWWWWWW ", "WWWWWWWWWW", " WWWWWWWW "], 20, 11)   # the white breast
            c = stamp(c, [" GG            GG ", "GGG            GGG"], 21, 7)                 # the wings' dark edge
        else:
            c = stamp(c, ["gggGGGGGGGGGGGgggg", "  gGGGGGGGGGGGg"], 21, 7)
        c = stamp(c, grebe_head(view), 7 + lift, 8)
        c = stamp(c, ["KTTTTTTK", "KTTTTTTTTK"], 18 + lift, 11 - (1 if True else 0))
        if view == "front":
            c = stamp(c, chick(rest, "front"), 15 + (2 if rest else 0) + lift, 20)   # peeping past her shoulder
        else:
            c = stamp(c, chick(rest, "back"), 15 + (2 if rest else 0) + lift, 14)    # on her back, nearest you
    # the water's edge along the body: white foam, and a wake while she moves
    c = stamp(c, ["w" * 22], 27, 5)
    if not rest:
        c = stamp(c, ["ww", " w"], 25 + phase, 2 - phase)
        c = stamp(c, ["ww", "w "], 25 + phase, 28 + phase)
    return c


def rider_frames(draw):
    """vanilla's surf layout: S S N N W W, then S N W -- here at rest"""
    return [draw("front", 0), draw("front", 1), draw("back", 0), draw("back", 1), draw("side", 0), draw("side", 1),
            draw("front", 0, True), draw("back", 0, True), draw("side", 0, True)]


# ============================================================ PROTEUS, two shapes (deoxys_a / deoxys_d, PSYCHIC)
# 1 2 3 4 the ramp, light to dark  5 the line  6 white  7 8 9 greys -- as daemon_type_psychic.pal lays them out
PROTEUS_ATTACK = grid(halves([
    "................",
    "................",
    ".5..............",
    ".55..........555",
    ".515........5111",
    ".515.......51111",
    "..515......51244",    # the bare head, a dark band where the face was
    "..515......51114",
    "..515.......5111",
    "..515.....555511",
    "..5115..55333355",    # the hood, fallen back about the shoulders
    "...5115533222233",
    "...532253225111",     # and the blades, up and out from both arms
    "....5552225111",
    ".......5225111",
    "........5111116",     # the crystal at the breast
    ".........5111111",
    ".........5111111",
    "..........511111",
    "..........522222",
    "..........522222",
    "..........532222",
    "..........532222",
    ".........5332222",
    ".........5333222",
    "........53333322",
    ".......533333333",
    "......5444444443",
    "......5555555555",
    "................",
    "................",
    "................",
]), 32)
PROTEUS_DEFENSE = grid(halves([
    "................",
    "................",
    "...............5",
    "..............51",    # the hood drawn to a point
    ".............511",
    "............5111",
    "...........51112",
    "..........511125",
    ".........5111254",    # the seam where it closes
    "........51112546",    # and the light through it
    "........51122546",
    ".......511222544",
    ".......512222254",
    "......5112333325",
    "......5122444432",    # the arms, wrapped round
    "......5123555543",
    ".....51123333334",
    ".....51222222223",
    ".....51222222222",
    ".....51223333332",
    ".....51234444443",
    ".....51235555554",
    "......5123333333",
    "......5122222222",
    "......5122222222",
    ".......512222222",
    ".......512233333",
    "........51234444",
    ".........5555555",
    "................",
    "................",
    "................",
]), 32)


def shade_right(rows):
    """the light comes from the upper left: the right half one step darker, as the battle front is lit"""
    step = {"1": "2", "2": "3", "3": "4"}
    return [r[:16] + "".join(step.get(ch, ch) for ch in r[16:]) for r in rows]


PROTEUS_DEFENSE = shade_right(PROTEUS_DEFENSE)
PROTEUS_ATTACK = shade_right(PROTEUS_ATTACK)


def proteus_frames(base, kind):
    if kind == "attack":                        # the blades flex: the outer ends come in a pixel
        f2 = shift(base, 1)
        f2 = [r[:1].replace("5", " ") + r[1:31] + r[31:].replace("5", " ") for r in f2]
    else:                                       # the shell breathes: down a row, the light through the seam brighter
        f2 = [r.replace("4546", "4566").replace("6454", "6654") for r in shift(base, 1)]
    return [base, f2]


# ============================================================ the cast
def walk_sheet(art, still=False):
    return figure(art[0], art[1], art[2], still=still)


CAST = [
    # key, vanilla file, who, frames, size, letters, palette name or colours, winter colours, where (map, x, y), note
    dict(key="kingfisher", file="people/cameraman.png", who="a KINGFISHER photographer",
         frames=walk_sheet(KINGFISHER), size=16, index=PINK, pal="npc_pink.pal",
         place=("LavenderTown", 16, 8), slot="NPC_2 (pink), its own tag kept; new gfx id (none today)"),
    dict(key="moth", file="people/unused_woman.png", who="a PEPPERED MOTH",
         frames=walk_sheet(MOTH), size=16, index=PINK, pal="npc_pink.pal",
         place=("LavenderTown", 7, 10), slot="NPC_2 (pink) as its graphics info has it"),
    dict(key="ermine", file="people/rich_boy.png", who="a young ERMINE",
         frames=walk_sheet(ERMINE), size=16, index=LETTERS, colours=ERMINE_SUMMER, winter=ERMINE_WINTER,
         place=("FiveIsland_ResortGorgeous", 35, 11), slot="a NEW tag (cast_ermine) in a slot RESORT SUBLIME leaves free"),
    dict(key="sloth", file="people/sitting_boy.png", who="a SLOTH, seated",
         frames=SLOTH, size=16, index=DOLDRUM, pal="npc_town_doldrum.pal",
         place=("CeruleanCity", 22, 3), slot="PALSLOT_NPC_SPECIAL on DOLDRUM's own tag (its locals' palette)"),
    dict(key="mynah", file="people/teachy_tv_host.png", who="a MYNAH, the STREAM's superfan",
         frames=walk_sheet(MYNAH), size=16, index=BLUE, pal="npc_blue.pal",
         place=("ViridianCity_PokemonCenter_1F", 10, 6), slot="NPC_1 (blue): its info names NPC_WHITE today -- repoint"),
    dict(key="secretary", file="people/unused_male_receptionist.png", who="a SECRETARY BIRD",
         frames=walk_sheet(SECRETARY, still=True), size=16, index=WHITE, pal="npc_white.pal",
         place=("IndigoPlateau_PokemonCenter_1F", 7, 3), slot="NPC_4 (white) as its graphics info has it"),
    dict(key="ptarmigan", file="people/unused_man.png", who="a PTARMIGAN whitewasher",
         frames=walk_sheet(PTARMIGAN, still=True), size=16, index=LETTERS, colours=PTARMIGAN_SUMMER,
         winter=PTARMIGAN_WINTER, place=("PalletTown", 9, 12),
         slot="a NEW tag (cast_ptarmigan) in a slot BLANCHE leaves free (blue or pink); new gfx id (none today)"),
    dict(key="proteus_attack", file="pokemon/deoxys_a.png", who="PROTEUS, all edges (CONTENT)",
         frames=proteus_frames(PROTEUS_ATTACK, "attack"), size=32, index=PSY, pal="daemon_type_psychic.pal",
         place=("BirthIsland_Exterior", 15, 3), slot="the PSYCHIC type tag, patched at spawn (gbaowslots.py)"),
    dict(key="proteus_defense", file="pokemon/deoxys_d.png", who="PROTEUS, a shell (CONTEXT)",
         frames=proteus_frames(PROTEUS_DEFENSE, "defense"), size=32, index=PSY, pal="daemon_type_psychic.pal",
         place=("BirthIsland_Exterior", 15, 3), slot="the PSYCHIC type tag, patched at spawn (gbaowslots.py)"),
    dict(key="muskrat", file="people/red_surf.png", who="a MUSKRAT in a reed boat",
         frames=rider_frames(muskrat), size=32, index=DOLDRUM, pal="npc_town_doldrum.pal",
         place=("CeruleanCity", 9, 12), slot="DOLDRUM's tag (never PLAYER_RED); on a route, a free slot with it"),
    dict(key="grebe", file="people/green_surf.png", who="a GREAT CRESTED GREBE and her chick",
         frames=rider_frames(grebe), size=32, index=WHITE, pal="npc_white.pal",
         place=("Route20", 27, 10), slot="NPC_4 (white), its own tag (never PLAYER_GREEN)"),
]


def colours(c):
    if "colours" in c:
        return [(115, 197, 164)] + c["colours"] + [(255, 255, 255), (0, 0, 0)]
    return read_pal(c["pal"]) if c["pal"].startswith("npc_") else daemonslib.read_pal(os.path.join(PALDIR, c["pal"]))


def checked(c):
    n = c["size"]
    for k, f in enumerate(c["frames"]):
        assert len(f) == 32, "%s frame %d is %d rows" % (c["key"], k, len(f))
        for r, line in enumerate(f):
            assert len(line) == n, "%s frame %d row %d is %d wide: %r" % (c["key"], k, r, len(line), line)
            bad = set(line) - set(c["index"])
            assert not bad, "%s frame %d row %d has %r" % (c["key"], k, r, bad)
    old = Image.open(os.path.join(GBA, "graphics/object_events/pics", c["file"]))
    assert old.size == (n * len(c["frames"]), 32), "%s: %d frames of %d drawn, %s is %s" % (
        c["key"], len(c["frames"]), n, c["file"], old.size)
    return old


def build(c, pal=None):
    n = c["size"]
    img = Image.new("P", (n * len(c["frames"]), 32))
    flat = [v for rgb in (pal or colours(c)) for v in rgb]
    img.putpalette(flat + [0] * (768 - len(flat)))
    px = img.load()
    for k, f in enumerate(c["frames"]):
        for y, line in enumerate(f):
            for x, ch in enumerate(line):
                px[k * n + x, y] = c["index"][ch]
    return img


# ============================================================ the contact sheets
BG = (150, 150, 150)
try:
    FONT = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 14)
    SMALL = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 11)
except OSError:
    FONT = SMALL = ImageFont.load_default()


def frame_rgba(img, k, n, pal=None):
    """frame k of a P sheet, index 0 clear"""
    f = img.crop((k * n, 0, k * n + n, 32))
    p = pal or [tuple(img.getpalette()[3 * i:3 * i + 3]) for i in range(16)]
    out = Image.new("RGBA", (n, 32), (0, 0, 0, 0))
    src, dst = f.load(), out.load()
    for y in range(32):
        for x in range(n):
            v = src[x, y]
            if v:
                dst[x, y] = tuple(p[v]) + (255,)
    return out


def groups(c):
    """which frames to lay out under DOWN / UP / LEFT / RIGHT (right = left flipped, as the engine draws it)"""
    m = len(c["frames"])
    if c["key"] == "sloth":
        return [("down", [0]), ("up", [2]), ("left", [1]), ("right", [-1])]
    if m == 2:
        return [("idle", [0, 1])]
    if m == 3:
        return [("down", [0]), ("up", [1]), ("left", [2]), ("right", [-2])]
    if c["size"] == 32:
        return [("down", [0, 1, 6]), ("up", [2, 3, 7]), ("left", [4, 5, 8]), ("right", [-4, -5, -8])]
    return [("down", [0, 3, 4]), ("up", [1, 5, 6]), ("left", [2, 7, 8]), ("right", [-2, -7, -8])]


def strip(img, c, z, pal=None):
    """one sheet laid out by direction at zoom z; a negative frame is that frame mirrored"""
    n = c["size"]
    gs = groups(c)
    cell, gap, tall = n * z, 3 * z, 32 * z
    w = sum(len(fr) * (cell + 2) + gap for _, fr in gs)
    out = Image.new("RGB", (w, tall + 16), BG)
    d = ImageDraw.Draw(out)
    x = 0
    for name, fr in gs:
        d.text((x + 2, 1), name, fill=(40, 40, 40), font=SMALL)
        for k in fr:
            f = frame_rgba(img, abs(k) if k != -0 else 0, n, pal)
            if k < 0:
                f = f.transpose(Image.FLIP_LEFT_RIGHT)
            big = f.resize((cell, tall), Image.NEAREST)
            out.paste(big, (x, 16), big)
            x += cell + 2
        x += gap
    return out


def people_sheet(path, members, z=4):
    rows = []
    for c in members:
        old = Image.open(os.path.join(GBA, "graphics/object_events/pics", c["file"]))
        oldp = [tuple(old.getpalette()[3 * i:3 * i + 3]) for i in range(16)]
        new = build(c)
        parts = [("vanilla " + os.path.basename(c["file"]), strip(old.convert("P") if old.mode == "P" else old, c, z, oldp)),
                 ("ours: " + c["who"] + ("  (summer)" if "winter" in c else ""), strip(new, c, z))]
        if "winter" in c:
            parts.append(("ours: winter coat (the same sheet, the winter .pal)",
                          strip(new, c, z, [(0, 0, 0)] + c["winter"] + [(255, 255, 255), (0, 0, 0)])))
        rows.append(parts)
    w = max(p.width for parts in rows for _, p in parts) + 20
    h = sum(sum(p.height + 22 for _, p in parts) + 18 for parts in rows) + 40
    out = Image.new("RGB", (w, h), (60, 60, 64))
    d = ImageDraw.Draw(out)
    d.text((10, 8), "T-439 the cast -- DRAFT, not in the engine. Vanilla above, ours below, at %dx." % z,
           fill=(240, 240, 240), font=FONT)
    y = 36
    for parts in rows:
        for label, p in parts:
            d.text((10, y), label, fill=(230, 230, 200), font=FONT)
            out.paste(p, (10, y + 18))
            y += p.height + 22
        y += 18
    out.save(path)
    return path


def map_sheet(path, z=2, span=(12, 8)):
    """each placed over a crop of its map, at 2x: the map drawn by reviewsheet.py from what the ROM is built from"""
    import importlib.util
    saved = sys.argv
    spec = importlib.util.spec_from_file_location("reviewsheet", os.path.join(ROOT, "tools/reviewsheet.py"))
    rs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rs)
    sys.argv = saved
    import json
    cells, cache = [], {}
    for c in CAST:
        m, px, py = c["place"]
        if m not in cache:
            cache[m] = rs.render(rs.layout_of(m))
        full = cache[m].copy()
        W, H_ = full.width // 16, full.height // 16
        x0 = max(0, min(W - span[0], px - span[0] // 2))
        y0 = max(0, min(H_ - span[1], py - span[1] // 2))
        # the neighbours already standing there, for scale: frame 0 of each one's own sheet
        objs = json.load(open(os.path.join(GBA, "data/maps/%s/map.json" % m))).get("object_events", [])
        for o in objs:
            g = str(o.get("graphics_id", "")).replace("OBJ_EVENT_GFX_", "").lower()
            p = os.path.join(PEOPLE, g + ".png")
            if not os.path.exists(p) or not (x0 <= o["x"] < x0 + span[0] and y0 <= o["y"] < y0 + span[1]):
                continue
            im = Image.open(p)
            if im.height != 32 or im.mode != "P":
                continue
            f = frame_rgba(im, 0, 16)
            full.paste(f, (o["x"] * 16, o["y"] * 16 - 16), f)
        img = build(c)
        n = c["size"]
        f = frame_rgba(img, 0, n)
        ox = px * 16 - (n - 16) // 2
        full.paste(f, (ox, py * 16 + 16 - 32), f)
        crop = full.crop((x0 * 16, y0 * 16, (x0 + span[0]) * 16, (y0 + span[1]) * 16))
        cells.append(("%s -- %s (%d,%d)" % (c["key"], m, px, py), crop.resize((crop.width * z, crop.height * z), Image.NEAREST)))
    cw = max(cl.width for _, cl in cells)
    ch = max(cl.height for _, cl in cells) + 22
    cols = 2
    rowsn = (len(cells) + cols - 1) // cols
    out = Image.new("RGB", (cols * (cw + 16) + 16, rowsn * (ch + 12) + 44), (60, 60, 64))
    d = ImageDraw.Draw(out)
    d.text((16, 10), "T-439 the cast on their maps, at 2x -- DRAFT. Neighbours already there drawn for scale.",
           fill=(240, 240, 240), font=FONT)
    for i, (label, cl) in enumerate(cells):
        x, y = 16 + (i % cols) * (cw + 16), 40 + (i // cols) * (ch + 12)
        d.text((x, y), label, fill=(230, 230, 200), font=SMALL)
        out.paste(cl, (x, y + 18))
    out.save(path)
    return path


def fix_sheet(path, before, keys=("moth", "secretary"), z=6):
    """before and after, front and side, for the ones redrawn: `before` holds the earlier draft's sheets by filename"""
    cells = []
    for c in CAST:
        if c["key"] not in keys:
            continue
        old = Image.open(os.path.join(before, os.path.basename(c["file"])))
        for label, img in (("before", old), ("after", build(c))):
            for k, view in ((0, "front"), (2, "side")):
                f = frame_rgba(img, k, 16)
                bg = Image.new("RGB", (16, 32), BG)
                bg.paste(f, (0, 0), f)
                cells.append(("%s %s %s" % (c["key"], label, view), bg.resize((16 * z, 32 * z), Image.NEAREST)))
    cw, chh = 16 * z + 84, 32 * z + 22
    out = Image.new("RGB", (max(4 * cw + 16, 720), 2 * chh + 44), (60, 60, 64))
    d = ImageDraw.Draw(out)
    d.text((10, 8), "T-439 the moth and the secretary bird, before and after -- DRAFT, at %dx." % z, fill=(240, 240, 240), font=FONT)
    for i, (label, cl) in enumerate(cells):
        x, y = 10 + (i % 4) * cw, 36 + (i // 4) * chh
        d.text((x, y), label, fill=(230, 230, 200), font=SMALL)
        out.paste(cl, (x, y + 16))
    out.save(path)
    return path


# ============================================================ main
def main():
    if WRITE and "--approved" not in ARGS:
        print("  --write refused: T-439's cast is a draft until the user has approved the sheets.")
        print("  (When they have: --write --approved writes each sheet over its vanilla file in")
        print("   graphics/object_events/pics/ and the ermine's and ptarmigan's palettes into graphics/object_events/palettes/;")
        print("   the graphics ids, tags, slots and placements are the engine's own edit, by hand.)")
        return 0
    print("  T-439, the cast: %d sheets" % len(CAST))
    built = []
    for c in CAST:
        old = checked(c)
        img = build(c)
        built.append((c, img))
        print("  %-16s %-34s %d x %dpx  %-26s %s" % (c["key"], c["file"], len(c["frames"]), c["size"],
              c.get("pal") or "own (summer + winter)", c["who"]))
        print("  %16s at %s %s; %s" % ("", c["place"][0], c["place"][1:], c["slot"]))
    # a preview, outside the tree
    strips = [strip(img, c, 3) for c, img in built]
    pv = Image.new("RGB", (max(s.width for s in strips), sum(s.height for s in strips)), BG)
    y = 0
    for s in strips:
        pv.paste(s, (0, y)); y += s.height
    pv.save(PREVIEW)
    print("  preview -> %s" % PREVIEW)

    if DRAFT is not None:
        os.makedirs(DRAFT, exist_ok=True)
        for c, img in built:
            base = os.path.basename(c["file"])[:-4]
            img.save(os.path.join(DRAFT, base + ".png"), bits=4 if len(colours(c)) <= 16 else 8)
            if "colours" in c:
                daemonslib.write_pal(os.path.join(DRAFT, "cast_%s_summer.pal" % c["key"]), colours(c), pad=True)
                wint = [(115, 197, 164)] + c["winter"] + [(255, 255, 255), (0, 0, 0)]
                daemonslib.write_pal(os.path.join(DRAFT, "cast_%s_winter.pal" % c["key"]), wint, pad=True)
                build(c, wint).save(os.path.join(DRAFT, base + "_winter_preview.png"))
        people_sheet(os.path.join(DRAFT, "contact_people.png"), [c for c in CAST if c["size"] == 16])
        people_sheet(os.path.join(DRAFT, "contact_riders_proteus.png"), [c for c in CAST if c["size"] == 32])
        print("  draft -> %s" % os.path.relpath(DRAFT, ROOT))
    if SHEETS:
        os.makedirs(SHEETS, exist_ok=True)
        for p in (people_sheet(os.path.join(SHEETS, "t439_draw_people.png"), [c for c in CAST if c["size"] == 16]),
                  people_sheet(os.path.join(SHEETS, "t439_draw_riders_proteus.png"), [c for c in CAST if c["size"] == 32]),
                  map_sheet(os.path.join(SHEETS, "t439_draw_maps.png"))):
            print("  sheet -> %s" % p)
        if argval("--before"):
            print("  sheet -> %s" % fix_sheet(os.path.join(SHEETS, "t439_draw_fix.png"), argval("--before")))

    if WRITE:
        for c, img in built:
            img.save(os.path.join(GBA, "graphics/object_events/pics", c["file"]), bits=4)
            if "colours" in c:
                daemonslib.write_pal(os.path.join(PALDIR, "cast_%s.pal" % c["key"]), colours(c), pad=True)
                daemonslib.write_pal(os.path.join(PALDIR, "cast_%s_winter.pal" % c["key"]),
                                     [(115, 197, 164)] + c["winter"] + [(255, 255, 255), (0, 0, 0)], pad=True)
            print("  written %s" % c["file"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
