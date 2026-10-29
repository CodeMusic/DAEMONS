#!/usr/bin/env python3
"""OSRIC HATTER, the Hatter of QUICKSILVER: a stoat in a top hat (T-485; bible 4.39, the user 2026-10-29).

    python3 tools/genhatter.py            # report: is the sheet, its palette and its registration current
    python3 tools/genhatter.py --write    # osric_hatter.png + npc_osric_hatter.pal, its spritesheet rule, and the
                                          #   graphics id OBJ_EVENT_GFX_OSRIC_HATTER with its own palette tag

THE AUTHOR OF THE HERMETIC LAYER. He made hats on QUICKSILVER until the quicksilver in the felt began to talk to him;
every person is an animal (fable-actors-animals), and he is a STOAT -- the hatter's mustelid, in his own top hat with
a band in THE SUBTLE LAYER's purple. Drawn exactly as the user's sheet drew him (gfx/drafts/t485/draw_t485.py,
5ac9524d): nine 16x32 frames in vanilla's order (S, N, W, then each walking twice), east the west frames flipped.

HIS OWN PALETTE (the user's answer Q4 A): QUICKSILVER's people's sixteen (npc_town_quicksilver.pal) with the light
blue and the blue turned to the band's purple and its dark -- only his band and bow use those two -- under a tag of
his own in PALSLOT_NPC_SPECIAL. He stands only in his house, where nobody else holds the special slot, so the T-365
repaint cannot happen there (engine.md trap 17; check_reach reads every map's special slot). His reflection uses his
own palette, as every special-slot person's does since T-484 (field_effect_helpers.c).
"""
import os, re, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daemonslib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PALDIR = os.path.join(GBA, "graphics/object_events/palettes")
SHEET = os.path.join(GBA, "graphics/object_events/pics/people/osric_hatter.png")
PAL = os.path.join(PALDIR, "npc_osric_hatter.pal")
RULES = os.path.join(GBA, "spritesheet_rules.mk")
WRITE = "--write" in sys.argv

CONST, CNAME, FNAME = "OBJ_EVENT_GFX_OSRIC_HATTER", "OsricHatter", "osric_hatter"
TAG, TAG_VALUE = "OBJ_EVENT_PAL_TAG_NPC_OSRIC_HATTER", 0x112E


def own_pal():
    """npc_town_quicksilver with slot 5 (light blue) and 6 (blue) turned to the band's purple and its dark"""
    p = daemonslib.read_pal(os.path.join(PALDIR, "npc_town_quicksilver.pal"))
    p[5] = (176, 86, 158)
    p[6] = (112, 50, 104)
    return p


# K outline 13 . F felt 4 . f felt lit 3 . B band 5 . b band dark 6 . C card 7 . R fur 10 . T fur lit 9
# W cream 8 . E eye/nose 15 . V waistcoat 12 . O bow 11 . G grey shoe 13
KEY = {".": 0, "K": 13, "F": 4, "f": 3, "B": 5, "b": 6, "C": 7, "R": 10, "T": 9, "W": 8, "E": 15, "V": 12,
       "O": 11, "N": 15, "G": 13}

FRONT = [
    "................", "................", "................", "................", "................",
    "................", "...KKKKKKKK.....", "..KfFFFFFFFK....", "..KfFFFFFFFK....", "...KfFFFFFFK....",
    "...KfFFFFFCK....", "...KBBBBBBCK....", "...KbBBBBBbK....", ".KKKKKKKKKKKKK..", "..KRRKKKKKKRRK..",
    "..KRRRRRRRRRRK..", "..KRERRRRRRERK..", "..KTWWWWWWWWTK..", "..KWWWWWNWWWWK..", "...KWWWWWWWWK...",
    "....KKWWWWKK....", "...KVVOOOOVVK...", "..KRVVWWWWVVRK..", "..KRVVWWWWVVRK..", "..KTVVWWWWVVTK..",
    "...KVVWWWWVVK...", "...KRRRRRRRRK...", "...KRRRKKRRRK...", "...KRRK..KRRK...", "...KGGK..KGGK...",
    "...KKKK..KKKK...", "................",
]
BACK = [
    "................", "................", "................", "................", "................",
    "................", ".....KKKKKKKK...", "....KfFFFFFFFK..", "....KfFFFFFFFK..", "....KfFFFFFFK...",
    "....KfFFFFFFK...", "....KBBBBBBBK...", "....KbBBBBBbK...", "..KKKKKKKKKKKKK.", "..KRRKKKKKKRRK..",
    "..KRRRRRRRRRRK..", "..KRRRRRRRRRRK..", "..KTRRRRRRRRTK..", "..KRRRRRRRRRRK..", "...KRRRRRRRRK...",
    "....KKRRRRKK....", "...KVVVVVVVVK...", "..KRVVVVVVVVRK..", "..KRVVVVVVVVRK..", "..KTVVVVVVVVTK..",
    "...KVVVVVVVVKKK.", "...KRRRRRRRRKRRK", "...KRRRKKRRRKGGK", "...KRRK..KRRKKK.", "...KGGK..KGGK...",
    "...KKKK..KKKK...", "................",
]
SIDE = [  # facing left (west); the engine mirrors it for east
    "................", "................", "................", "................", "................",
    "................", "....KKKKKKK.....", "...KfFFFFFFK....", "...KfFFFFFFK....", "....KfFFFFFK....",
    "....KCFFFFFK....", "....KCBBBBBK....", "....KbBBBBbK....", "..KKKKKKKKKKKK..", "....KRRRRRKRRK..",
    "...KRRRRRRRRRK..", "..KKERRRRRRRRK..", ".KNWWWRRRRRRK...", "..KWWWWWRRRRK...", "...KKWWWRRRK....",
    ".....KWWWKK.....", ".....KOVVVK.....", ".....KVVRRK.....", ".....KVVRRK.....", ".....KVVTTK..KK.",
    ".....KVVVVK.KGGK", ".....KRRRRKKRRK.", ".....KRRRRRRRK..", ".....KRRKRRKK...", ".....KGGKGGK....",
    ".....KKKKKKK....", "................",
]


def walk(frame, step):
    """a walk frame: one foot lifted a pixel, the other planted (vanilla's two-step)"""
    old = [list(r) for r in frame]
    f = [list(r) for r in frame]
    for x in (range(0, 8) if step == 0 else range(8, 16)):
        for y in (28, 29, 30):
            f[y - 1][x] = old[y][x]
        f[30][x] = "."
    return ["".join(r) for r in f]


def sheet():
    frames = [FRONT, BACK, SIDE, walk(FRONT, 0), walk(FRONT, 1), walk(BACK, 0), walk(BACK, 1),
              walk(SIDE, 0), walk(SIDE, 1)]
    img = Image.new("P", (16 * len(frames), 32), 0)
    img.putpalette([v for c in own_pal() for v in c] + [0] * (768 - 48))
    px = img.load()
    for n, f in enumerate(frames):
        assert len(f) == 32 and all(len(r) == 16 for r in f)
        for y, row in enumerate(f):
            for x, ch in enumerate(row):
                px[n * 16 + x, y] = KEY[ch]
    return img


def ensure_rule():
    target = "$(OBJEVENTGFXDIR)/people/%s.4bpp" % FNAME
    s = open(RULES).read()
    if target + ":" in s:
        return False
    open(RULES, "w").write(s.rstrip("\n") + "\n\n%s: %%.4bpp: %%.png\n\t$(GFX) $< $@ -mwidth 2 -mheight 4\n" % target)
    return True


def gentowns():
    """gentowns.register_one, imported without arming anything (engine.md trap 16): it writes nothing at import"""
    argv, sys.argv = sys.argv, ["gentowns"]
    try:
        import gentowns as g
    finally:
        sys.argv = argv
    return g


def register():
    """the tag, the palette, the graphics id: each step once (a second run changes nothing)"""
    def edit(path, fn):
        p = os.path.join(GBA, path); s = open(p).read(); s2 = fn(s)
        if s2 != s:
            open(p, "w").write(s2)

    def movement(s):
        if TAG in s:
            return s
        anchor = "#define OBJ_EVENT_PAL_TAG_CAST_PTARMIGAN              0x112D\n"
        assert s.count(anchor) == 1 and ("0x%04X" % TAG_VALUE) not in s
        s = s.replace(anchor, anchor + "//  T-485: OSRIC HATTER, in his own palette in PALSLOT_NPC_SPECIAL; he stands only in his house.\n"
                      "#define %-45s 0x%04X\n" % (TAG, TAG_VALUE))
        entry = "    {gObjectEventPal_CastPtarmigan,            OBJ_EVENT_PAL_TAG_CAST_PTARMIGAN},\n"
        assert s.count(entry) == 1
        return s.replace(entry, entry + "    {gObjectEventPal_NpcOsricHatter,           %s},   // T-485\n" % TAG)
    edit("src/event_object_movement.c", movement)

    def graphics_pal(s):
        if "gObjectEventPal_NpcOsricHatter[]" in s:
            return s
        anchor = 'const u16 gObjectEventPal_NpcTownCallow[] = INCBIN_U16("graphics/object_events/palettes/npc_town_callow.gbapal");\n'
        assert s.count(anchor) == 1
        return s.replace(anchor, anchor + '//  T-485: OSRIC HATTER\'s own sixteen (DAEMONS tools/genhatter.py).\n'
                         'const u16 gObjectEventPal_NpcOsricHatter[] = INCBIN_U16("graphics/object_events/palettes/npc_osric_hatter.gbapal");\n')
    edit("src/data/object_events/object_event_graphics.h", graphics_pal)

    gentowns().register_one(edit, CONST, CNAME, FNAME, TAG,
                            "T-485: OSRIC HATTER, the Hatter of QUICKSILVER -- a stoat in a top hat, his own palette")


def current():
    """(sheet current, palette current, rule present, registered)"""
    img = sheet()
    old = Image.open(SHEET) if os.path.exists(SHEET) else None
    same = old is not None and old.size == img.size and list(old.getdata()) == list(img.getdata())
    pal = os.path.exists(PAL) and daemonslib.read_pal(PAL) == own_pal()
    rule = ("people/%s.4bpp:" % FNAME) in open(RULES).read()
    info = open(os.path.join(GBA, "src/data/object_events/object_event_graphics_info.h")).read()
    mov = open(os.path.join(GBA, "src/event_object_movement.c")).read()
    reg = ("gObjectEventGraphicsInfo_%s =" % CNAME) in info and TAG in mov
    return img, same, pal, rule, reg


def main():
    img, same, pal, rule, reg = current()
    print("  OSRIC HATTER: 9 frames (3 drawn), his own palette (QUICKSILVER's, the blues turned purple), tag 0x%04X"
          % TAG_VALUE)
    print("  sheet %s, palette %s, rule %s, registered %s" % (
        "current" if same else "STALE", "current" if pal else "STALE", "present" if rule else "MISSING",
        "yes" if reg else "NO"))
    if same and pal and rule and reg:
        return
    if not WRITE:
        print("  report only; pass --write")
        return
    img.save(SHEET, bits=4)
    daemonslib.write_pal(PAL, own_pal())
    ensure_rule()
    register()
    print("  written: %s, %s, the rule, %s" % (os.path.relpath(SHEET, GBA), os.path.relpath(PAL, GBA), CONST))


if __name__ == "__main__":
    main()
