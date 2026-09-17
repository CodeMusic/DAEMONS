#!/usr/bin/env python3
"""The CUE BALL rides, and the rhinoceros rides with him (T-127; vision.md 9.4).

    python3 tools/genrhino.py            # preview to /tmp/rhino.png, and what would be repointed
    python3 tools/genrhino.py --write    # the sheet, its registration, and the eight map objects

THE LAST DISAGREEMENT `spritejoin.py` REPORTS, and the only one whose stand-in is not 16x32: eight
objects on Routes 16, 17 and 18 stand on `biker.png` -- 32x32, ten frames, PINK slot 2 -- and battle
as CUE_BALL, whose picture is a rhinoceros. The sheet under them is the boar.

VANILLA SETTLES THE QUESTION THE TICKET LEFT OPEN. Those three routes ARE Cycling Road; every
trainer on them is a rider, and the class is the gang's muscle. Taking the bike away to give the
rhino a 16x32 sheet would fix the species by breaking the scene, so the rhino rides.

AND THE MACHINE IS NOT REDRAWN, BECAUSE IT IS ALREADY OURS AND IT COST SIX DRAFTS. engine.md records
what those drafts learned -- handlebars standing clear of the body read as outstretched arms, the
head-on wheel as a licence plate, and every draft was wider than the sprite it replaced until one
was measured against vanilla's own front frame. None of that is worth risking to change a rider. So
this reads OUR `biker.png` and replaces THE HEAD ONLY: the jacket, the frame, the wheels and the
tail lights come through untouched, and the tool asserts it.

WHICH FRAMES SHARE A HEAD IS DERIVED, NOT TYPED. The ten frames hold three heads between them --
front, back and side -- each appearing once standing and twice more shifted a row up or down for the
walk. That is measured by comparing every frame's head band against the three standing ones at each
offset, so a sheet redrawn later cannot quietly fall out of step with a table written here.

A 32x32 SHEET IS CUT 4x4 AND CHECKED 4x4. `spritesheet_rules.mk` needs `-mwidth 4 -mheight 4`, the
pic table takes `overworld_frame(pic, 4, 4, k)`, and the info carries .size 512 with the 32x32 oam
and subsprite tables -- a 32x32 sheet cut 2x4 is trap 15 with more tiles, and decoding one 2x4 to
check it once reported five of the player's own sprites as scrambled when nothing was wrong.
"""
import glob, json, os, re, sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from genfolk import ensure_rule, PEOPLE, GBA
from gentowns import register_one, GEOM_32x32

PREVIEW = "/tmp/rhino.png"
WRITE = "--write" in sys.argv
SRC, DST = "biker.png", "cue_ball.png"
CONST, CNAME = "OBJ_EVENT_GFX_CUE_BALL", "CueBall"

# The species declaration `spritejoin.py` reads, in the shape the gen* tools all use. Without it
# the join matches this sheet to its portrait BY NAME ALONE and reports "?" for the animal --
# which passes, and would go on passing if the sheet were later redrawn as something else.
SPECIES = [("rhinoceros", "cue_ball.png")]

# npc_pink, by index: 11 pale grey  12 grey  13 dark grey  14 white  15 black
LET = {".": None, "w": 11, "g": 12, "G": 13, "W": 14, "K": 15}

# The head is drawn in the grey the slot already has, and the HORN is the read: at the front it is a
# pale wedge standing up off the muzzle, in profile it is the thing out in front of the face. Small
# ears set wide, because a rhino's are, and because two tall ones on a broad skull would be horns of
# the wrong kind -- the failure this project has now had four times.
FRONT = [                      # sixteen columns, mirrored to the frame's own 32
    "................",
    "............KGGK",
    "............KGGK",
    "........KggggggW",
    "........KggggggW",
    "........KgKggggW",
    "........KgggggWW",
    "........KgggggWW",
    ".........KGGGgWW",
    ".........KGGGGWW",
]
BACK = [
    "................",
    "............KGGK",
    "............KGGK",
    "........Kggggggg",
    "........Kggggggg",
    "........Kggggggg",
    "........Kggggggg",
    "........Kggggggg",
    ".........KGGGGGG",
    ".........KGGGGGG",
]
SIDE = [                       # a profile is not symmetrical, so it is drawn the frame's full width
    "..........KgggggK...............",
    ".........KgggggggK..............",
    "........KgKggggggK..............",
    "......KWWggggggggK..............",
    ".....KWWWgggggggK...............",
    "......KWGGGGGGGK................",
    "........KGGGGGK.................",
    ".........KGGGK..................",
]
# where each head sits in a standing frame, and how many rows of the frame it is allowed to touch
HEADS = {0: dict(art=FRONT, top=6, band=(4, 15)),
         1: dict(art=BACK, top=6, band=(4, 15)),
         2: dict(art=SIDE, top=6, band=(4, 13))}


def frames_of(img):
    px = img.load()
    return [[[px[f * 32 + x, y] for x in range(32)] for y in range(32)] for f in range(img.width // 32)]


def kinds(fs):
    """which standing head each frame wears, and the row offset it wears it at -- measured"""
    def band(f, dy):
        return tuple(tuple(fs[f][y][x] if 0 <= y < 32 else 0 for x in range(32)) for y in range(4 + dy, 17 + dy))
    out = {}
    for f in range(len(fs)):
        for n in HEADS:
            for dy in (-2, -1, 0, 1, 2):
                if band(f, dy) == band(n, 0):
                    out[f] = (n, dy)
                    break
            if f in out:
                break
        assert f in out, "frame %d wears a head none of the three standing frames has" % f
    return out


def mirrored(rows):
    for r in rows:
        assert len(r) in (16, 32), "a head row is %d columns, not 16 (a half) or 32" % len(r)
    return [r if len(r) == 32 else r + r[::-1] for r in rows]


def draw(fs, plan):
    for f, (n, dy) in plan.items():
        head = HEADS[n]
        lo, hi = head["band"][0] + dy, head["band"][1] + dy
        for y in range(lo, hi + 1):
            for x in range(32):
                fs[f][y][x] = 0
        for r, row in enumerate(mirrored(head["art"])):
            for c, ch in enumerate(row):
                v = LET[ch]
                if v is not None:
                    y = head["top"] + dy + r
                    assert lo <= y <= hi, "frame %d: the head draws outside the band it cleared (row %d)" % (f, y)
                    fs[f][y][c] = v


def plan_maps():
    pics = {}
    for m in re.finditer(r"\[(TRAINER_[A-Z0-9_]+)\]\s*=\s*\{(.*?)\n    \}",
                         open(os.path.join(GBA, "src/data/trainers.h")).read(), re.S):
        p = re.search(r"\.trainerPic\s*=\s*TRAINER_PIC_([A-Z0-9_]+)", m.group(2))
        if p:
            pics[m.group(1)] = p.group(1)
    labels = {}
    for f in glob.glob(os.path.join(GBA, "data/**/*.inc"), recursive=True):
        for m in re.finditer(r"^(\w+)::\s*\n(.*?)(?=^\w+::|\Z)", open(f, errors="ignore").read(), re.S | re.M):
            t = re.search(r"trainerbattle\w*\s+(TRAINER_[A-Z0-9_]+)", m.group(2))
            if t:
                labels[m.group(1)] = t.group(1)
    todo = []
    for mp in sorted(glob.glob(os.path.join(GBA, "data/maps/*/map.json"))):
        for i, o in enumerate(json.load(open(mp)).get("object_events", [])):
            if pics.get(labels.get(o.get("script"))) == "CUE_BALL" and o.get("graphics_id") != CONST:
                todo.append((mp, i, o.get("graphics_id", "")))
    return todo


def main():
    src = Image.open(os.path.join(PEOPLE, SRC))
    assert src.size == (320, 32) and src.mode == "P", "%s is %s %s" % (SRC, src.mode, src.size)
    before = frames_of(src)
    fs = frames_of(src)
    plan = kinds(fs)
    print("  %s on the boar's own bike -- %d frames wearing %d heads: %s" % (
          SPECIES[0][0], len(fs), len({n for n, _ in plan.values()}),
          ", ".join("%d=%s%+d" % (f, "fbs"[n], dy) for f, (n, dy) in sorted(plan.items()))))
    draw(fs, plan)
    for f, (n, dy) in plan.items():
        lo, hi = HEADS[n]["band"][0] + dy, HEADS[n]["band"][1] + dy
        for y in range(32):
            if not (lo <= y <= hi):
                assert fs[f][y] == before[f][y], "frame %d row %d changed and it is not head" % (f, y)
    out = Image.new("P", src.size)
    out.putpalette(src.getpalette())
    op = out.load()
    for f, frame in enumerate(fs):
        for y in range(32):
            for x in range(32):
                op[f * 32 + x, y] = frame[y][x]

    rows = []
    for img in (src, out):
        rgb = img.convert("RGB")
        bg = Image.new("RGB", img.size, (150, 150, 150))
        bg.paste(rgb, (0, 0), Image.frombytes("L", img.size, bytes(255 if i else 0 for i in img.getdata())))
        rows.append(bg)
    prev = Image.new("RGB", (320 * 3, 32 * 3 * 2 + 8), (48, 48, 52))
    for i, r in enumerate(rows):
        prev.paste(r.resize((960, 96), Image.NEAREST), (0, i * 104))
    prev.save(PREVIEW)
    print("  -> preview %s (the boar above, the rhinoceros below; everything from the jacket down is the same bike)" % PREVIEW)

    todo = plan_maps()
    for mp, i, was in todo:
        print("  repoint %-28s object %-2d %s -> CUE_BALL" % (os.path.basename(os.path.dirname(mp)), i,
              was.replace("OBJ_EVENT_GFX_", "")))
    if not todo:
        print("  every object that battles as a CUE_BALL already points at its own sheet")

    if WRITE:
        out.save(os.path.join(PEOPLE, DST), bits=4)
        made = ensure_rule(DST, mwidth=4, mheight=4)     # 32x32 is cut 4x4, not 2x4

        def edit(path, fn):
            p = os.path.join(GBA, path); s = open(p).read(); s2 = fn(s)
            if s2 != s:
                open(p, "w").write(s2)
        register_one(edit, CONST, CNAME, DST[:-4], "OBJ_EVENT_PAL_TAG_NPC_PINK",
                     "the cue ball (T-127): a rhinoceros on the boar's own bike -- the head is redrawn and the "
                     "machine is not, on pink's palette and slot, where it used to borrow biker",
                     frames=len(fs), slot="PALSLOT_NPC_2", geom=GEOM_32x32)
        ev = open(os.path.join(GBA, "include/constants/event_objects.h")).read()
        n = int(re.search(r"#define %s (\d+)" % CONST, ev).group(1))
        if n % 2 == 0:
            def colours(s):
                start = s.index("static const u8 sTextColorTable[] =")
                end = s.index("};", start)
                body = s[start:end]
                if ("[%s / 2]" % CONST) not in body:
                    body += "    [%s / 2] = COLORS(NPC_TEXT_COLOR_NEUTRAL, NPC_TEXT_COLOR_NEUTRAL),\n" % CONST
                return s[:start] + body + s[end:]
            edit("src/dynamic_placeholder_text_util.c", colours)
        changed = {}
        for mp, i, _was in todo:
            if mp not in changed:
                raw = open(mp).read()
                changed[mp] = (json.loads(raw), raw.endswith("\n"))
            changed[mp][0]["object_events"][i]["graphics_id"] = CONST
        for mp, (m, nl) in changed.items():
            open(mp, "w").write(json.dumps(m, indent=2) + ("\n" if nl else ""))
        print("  written %s (%s), registered 32x32/10 frames, %d objects repointed across %d maps"
              % (DST, "new conversion rule" if made else "rule already present", len(todo), len(changed)))


if __name__ == "__main__":
    main()
