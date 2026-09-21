#!/usr/bin/env python3
"""Which trainer portraits a player actually FACES, and which of those are still vanilla's (T-120, T-117).

    python3 tools/gbafaced.py            # the report
    python3 tools/gbafaced.py --all      # and name every faced portrait, ours included

WHY THIS AND NOT THE CENSUS. tools/gbaspritecensus.py counts all 146 portraits vanilla shipped, which is the right
number for "how far from vanilla" and the wrong one for "what does a player see". Some of those pictures belong to
classes no map places, and a portrait nobody meets is not worth a draft.

THE WALK IS checkfable.py's, because it is already proven: every map.json object event -> its script -> the
trainerbattle line -> TRAINER_x -> .trainerPic -> the front pic file. A portrait is FACED if any map places a
trainer who uses it.

And "still vanilla" is the census's own test: the file's pixels, against pret's upstream/master.
"""
import glob, io, json, os, re, subprocess, sys
from collections import defaultdict
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = os.path.join(ROOT, "engineGba")
ALL = "--all" in sys.argv


def git(*a, binary=False):
    r = subprocess.run(["git", "-C", E] + list(a), capture_output=True)
    return r.stdout if binary else r.stdout.decode()


def faced():
    tr = open(os.path.join(E, "src/data/trainers.h")).read()
    pic = dict(re.findall(r"\[(TRAINER_\w+)\]\s*=\s*\{.*?\.trainerPic = (TRAINER_PIC_\w+)", tr, re.S))
    g2f = dict(re.findall(r'(gTrainerFrontPic_\w+)\[\]\s*=\s*INCBIN_U32\("graphics/trainers/front_pics/(\w+)_front_pic\.4bpp',
                          open(os.path.join(E, "src/data/graphics/trainers.h")).read()))
    c2g = dict(re.findall(r"TRAINER_SPRITE\((\w+),\s*(gTrainerFrontPic_\w+)",
                          open(os.path.join(E, "src/data/trainer_graphics/front_pic_tables.h")).read()))
    text = "".join(open(f).read() + "\n" for f in
                   glob.glob(os.path.join(E, "data/scripts/*.inc")) + glob.glob(os.path.join(E, "data/maps/*/scripts.inc")))
    labels = {m.group(1): m.group(2) for m in re.finditer(r"^(\w+)::\n(.*?)(?=^\w+::|\Z)", text, re.S | re.M)}
    out = defaultdict(set)
    for mj in glob.glob(os.path.join(E, "data/maps/*/map.json")):
        town = mj.split(os.sep)[-2]
        for o in json.load(open(mj)).get("object_events", []):
            body = labels.get(o.get("script", ""), "")
            for t in re.findall(r"trainerbattle\w*\s+(?:\w+,\s*)?(TRAINER_\w+)", body):
                if t in pic:
                    f = g2f.get(c2g.get(pic[t][len("TRAINER_PIC_"):], ""), None)
                    if f:
                        out[f].add(town)
    return out


def is_vanilla(name):
    rel = "graphics/trainers/front_pics/%s_front_pic.png" % name
    raw = git("show", "upstream/master:" + rel, binary=True)
    if not raw:
        return False                       # a picture vanilla never had is ours by definition
    ours = Image.open(os.path.join(E, rel))
    theirs = Image.open(io.BytesIO(raw))
    return ours.size == theirs.size and ours.tobytes() == theirs.tobytes()


def main():
    seen = faced()
    stale = sorted((len(m), n) for n, m in seen.items() if is_vanilla(n))
    print("  %d portraits are FACED on a map (of 146 vanilla shipped)" % len(seen))
    print("  %d of those are still vanilla's\n" % len(stale))
    for n, name in sorted(stale, reverse=True):
        print("     %-26s faced on %2d map(s)" % (name, n))
    if ALL:
        print("\n  every faced portrait:")
        for name in sorted(seen):
            print("     %-26s %s%s" % (name, "VANILLA " if is_vanilla(name) else "ours    ", len(seen[name])))


if __name__ == "__main__":
    main()
