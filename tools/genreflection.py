#!/usr/bin/env python3
"""A palette we redrew still reflected in vanilla's colours (T-129).

    python3 tools/genreflection.py            # report, and a swatch preview to /tmp/reflection.png
    python3 tools/genreflection.py --write    # rewrite every stale <name>_reflection.pal

A sprite standing on a reflective tile draws its REFLECTION from a SECOND palette -- `<name>_reflection.pal`,
patched into PALSLOT_PLAYER_REFLECTION for the player -- and nothing ties that palette to the first. So
redrawing `player.pal` left the figure under the player's feet in the old figure's colours, and no build,
check or census noticed: T-52 wrote it down as "still open" on 2026-09-14 and it sat there until a sweep
of closed tickets read the sentence.

WHICH REFLECTIONS ARE STALE IS MEASURED: a base palette that differs from upstream/master with a reflection
that does not. Today that is `player.pal` alone -- every NPC palette and its reflection are still vanilla's,
because every sheet drawn since was drawn INSIDE its slot's sixteen.

HOW A REFLECTION IS MADE IS LEARNED FROM VANILLA, NOT GUESSED. Vanilla's reflections are hand-tuned --
each colour lifted a long way toward white and pushed a little toward blue -- so the rule is fitted from
vanilla's own five pairs (the player's and the four NPC palettes, 70 colours). Three models were scored
two ways: leaving each vanilla colour out and predicting it, and how far each moves OUR colours in hue:

                                  held-out error    hue drift on our palette
    the 3 nearest vanilla colours     11.5             mean 32.1, worst 136.7
    one line per channel              15.6             mean  6.1, worst  16.7
    one mix toward one tint           15.4             mean  6.6, worst  16.7

THE MODEL WITH THE BEST SCORE WAS THE WRONG ONE, and the swatches showed it before the numbers did: the
near-black turned brown, the tan mint, the cream icy cyan. Its error was measured on VANILLA's colours,
which are saturated, and this figure is greys and browns -- the nearest saturated neighbours of a grey
lend it their hue. The score measured the wrong palette. So the rule is the MIX: every colour moved the
same fraction of the way toward one pale, bluish point, which is what a reflection in water is, and which
cannot turn a grey into a colour. Index 0 is the transparent key and 15 the outline, and both keep the
values vanilla's reflection gives them.

Every value is snapped to the GBA's five bits per channel, which is what the converter will do anyway.
"""
import os, statistics, subprocess, sys
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
DIR = "graphics/object_events/palettes"
WRITE = "--write" in sys.argv
PREVIEW = "/tmp/reflection.png"
TRAIN = ("player", "npc_blue", "npc_pink", "npc_green", "npc_white")


def read(text):
    return [tuple(map(int, l.split())) for l in text.replace("\r", "").split("\n")[3:19]]


def upstream(path):
    r = subprocess.run(["git", "-C", GBA, "show", "upstream/master:" + path], capture_output=True, text=True)
    return read(r.stdout) if r.returncode == 0 else None


def on_disk(path):
    return read(open(os.path.join(GBA, path)).read())


def snap(v):
    return round(round(max(0, min(255, v)) * 31 / 255) * 255 / 31)


def model():
    pairs = []
    for base in TRAIN:
        a, b = upstream("%s/%s.pal" % (DIR, base)), upstream("%s/%s_reflection.pal" % (DIR, base))
        pairs += [(x, y) for i, (x, y) in enumerate(zip(a, b)) if i not in (0, 15)]
    # out = in + s * (W - in), one s for every channel: search s, and W is then the mean it implies
    best = None
    for s in [i / 100 for i in range(20, 90)]:
        W = [statistics.mean((y[ch] - (1 - s) * x[ch]) / s for x, y in pairs) for ch in range(3)]
        err = statistics.mean(abs(max(0, min(255, (1 - s) * x[ch] + s * W[ch])) - y[ch]) for x, y in pairs for ch in range(3))
        if not best or err < best[0]:
            best = (err, s, W)
    err, s, W = best

    def reflect(c):
        return tuple(snap((1 - s) * c[ch] + s * W[ch]) for ch in range(3))
    # the tint point itself lies past white -- only the part of the way travelled lands in range -- so it
    # is reported as what it does to a colour: kept at (1 - s) of itself, and lifted by s * W
    reflect.describe = "each colour kept at %.0f%% and lifted by (%d, %d, %d); mean error %.1f of 255" % (
        (1 - s) * 100, *[round(s * w) for w in W], err)
    return reflect, len(pairs)


def stale():
    out = []
    for name in sorted(os.listdir(os.path.join(GBA, DIR))):
        if not name.endswith("_reflection.pal"):
            continue
        base = name[:-len("_reflection.pal")] + ".pal"
        bp, rp = "%s/%s" % (DIR, base), "%s/%s" % (DIR, name)
        if not os.path.exists(os.path.join(GBA, bp)):
            continue
        if on_disk(bp) != upstream(bp) and on_disk(rp) == upstream(rp):
            out.append((bp, rp))
    return out


def main():
    reflect, n = model()
    todo = stale()
    print("  learned from %d vanilla colour pairs: %s" % (n, reflect.describe))
    print("  %d reflection(s) out of step with a redrawn base" % len(todo))
    rows = []
    for bp, rp in todo:
        base, old = on_disk(bp), on_disk(rp)
        new = [old[0]] + [reflect(c) for c in base[1:15]] + [old[15]]
        rows.append((bp, base, old, new))
        print("  %s -> %s" % (os.path.basename(bp), os.path.basename(rp)))
        for i in range(16):
            print("     %2d %-16s  was %-16s  now %s" % (i, base[i], old[i], new[i]))
        if WRITE:
            with open(os.path.join(GBA, rp), "w") as fh:
                fh.write("JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % c for c in new))
    if rows:
        S = 28
        img = Image.new("RGB", (16 * S + 150, len(rows) * 3 * S + 10), (40, 40, 46))
        d = ImageDraw.Draw(img)
        for k, (bp, base, old, new) in enumerate(rows):
            for j, (label, colours) in enumerate((("base", base), ("was", old), ("now", new))):
                y = k * 3 * S + j * S
                d.text((4, y + 8), "%s %s" % (os.path.basename(bp)[:-4], label), fill=(230, 230, 230))
                for i, c in enumerate(colours):
                    d.rectangle([150 + i * S, y, 150 + i * S + S - 2, y + S - 2], fill=c)
        img.save(PREVIEW)
        print("  swatches -> %s" % PREVIEW)
    if WRITE:
        print("  written %d reflection palette(s)" % len(rows))


if __name__ == "__main__":
    main()
