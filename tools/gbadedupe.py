#!/usr/bin/env python3
"""Free the General tileset's duplicate tiles (T-85).

    python3 tools/gbadedupe.py                              # report
    python3 tools/gbadedupe.py --write                      # repoint every block, blank the freed slots
    python3 tools/gbadedupe.py --secondary gTileset_X ...   # the same inside town tilesets (T-85)

The General tileset's 640 tile slots are full, and the buildings of 9.23 need
more than the slots only they use. But vanilla stores the same 8x8 tile more
than once -- sometimes as an exact copy, sometimes as a mirror image that a
block could have drawn with a flip bit. Every such copy is a slot.

So each tile is keyed by the smallest of itself and its three flips; the lowest
slot with that key is kept, and every metatile entry that draws a later copy is
pointed at the keeper with the flip that reproduces it. That is done in the
General tileset's own blocks and in every secondary tileset that is ever loaded
with General (a secondary paired with the Building tileset numbers its low tiles
in a different sheet and is not touched). The freed slots are blanked, so
gbacivic.py finds them unreferenced.

Never merged: a slot drawn by a secondary tileset that is also loaded with
another primary (Seafoam Islands), since its entries cannot be repointed; the
animated tiles (water 416..481, flowers 508..511), which
TilesetAnim_General writes over by slot number, and slot 0.
"""
import json, os, re, struct, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
PD = os.path.join(GBA, "data/tilesets/primary/general")
WRITE = "--write" in sys.argv
ANIM = set(range(416, 482)) | set(range(508, 512))


def tdir(symbol):
    want = re.sub(r"[^a-z0-9]", "", symbol.replace("gTileset_", "").lower())
    for d in os.listdir(os.path.join(GBA, "data/tilesets/secondary")):
        if re.sub(r"[^a-z0-9]", "", d.lower()) == want:
            return os.path.join(GBA, "data/tilesets/secondary", d)


def main():
    layouts = json.load(open(os.path.join(GBA, "data/layouts/layouts.json")))["layouts"]
    pairs = {}
    for l in layouts:
        if l.get("secondary_tileset"):
            pairs.setdefault(l["secondary_tileset"], set()).add(l["primary_tileset"])
    # a secondary loaded with General AND another primary cannot be repointed (its low ids mean two sheets),
    # so any General slot it draws stays where it is
    mixed = sorted(s for s, p in pairs.items() if "gTileset_General" in p and len(p) > 1)
    secondaries = sorted(s for s, p in pairs.items() if p == {"gTileset_General"})
    pinned = set()
    for s in mixed:
        b = open(os.path.join(tdir(s), "metatiles.bin"), "rb").read()
        pinned |= {struct.unpack_from("<H", b, n * 2)[0] & 0x3FF for n in range(len(b) // 2)} - {0}
    print("  not repointed, loaded with two primaries: %s (%d General slots stay put)" % (mixed, len(pinned)))

    img = Image.open(os.path.join(PD, "tiles.png")); px = img.load()
    tile = lambda i: tuple(px[(i % 16) * 8 + k % 8, (i // 16) * 8 + k // 8] for k in range(64))
    hf = lambda t: tuple(t[(k // 8) * 8 + 7 - k % 8] for k in range(64))
    vf = lambda t: tuple(t[(7 - k // 8) * 8 + k % 8] for k in range(64))
    keeper, remap = {}, {}                                    # remap: slot -> (keeper, flip bits that turn keeper into slot)
    for i in range(1, 640):
        if i in ANIM:
            continue
        t = tile(i)
        if not any(t):
            continue
        variants = {0: t, 0x400: hf(t), 0x800: vf(t), 0xC00: hf(vf(t))}
        key = min(variants.values())
        if key not in keeper:
            keeper[key] = (i, next(f for f, v in variants.items() if v == key))
            continue
        k, kf = keeper[key]
        if i in pinned:
            continue
        # keeper drawn with kf gives key; slot i drawn with f gives key; so slot i = keeper drawn with kf then f undone
        f = next(f for f, v in variants.items() if v == key)
        remap[i] = (k, kf ^ f)
    print("  %d duplicate tiles, across General and %d secondary tilesets" % (len(remap), len(secondaries)))

    files = [os.path.join(PD, "metatiles.bin")] + [os.path.join(tdir(s), "metatiles.bin") for s in secondaries]
    changed = 0
    out = {}
    for f in files:
        b = bytearray(open(f, "rb").read())
        for n in range(len(b) // 2):
            v = struct.unpack_from("<H", b, n * 2)[0]
            i = v & 0x3FF
            if i in remap:
                k, flip = remap[i]
                struct.pack_into("<H", b, n * 2, (v & ~0x0FFF) | k | ((v & 0x0C00) ^ flip)); changed += 1
        out[f] = b
    # check: every repointed entry draws exactly what it drew
    for f, b in out.items():
        old = open(f, "rb").read()
        for n in range(len(b) // 2):
            a, c = struct.unpack_from("<H", old, n * 2)[0], struct.unpack_from("<H", b, n * 2)[0]
            if a != c:
                def draw(v):
                    t = tile(v & 0x3FF)
                    if v & 0x400: t = hf(t)
                    if v & 0x800: t = vf(t)
                    return t
                assert draw(a) == draw(c) and (a >> 12) == (c >> 12), "entry %d of %s would change" % (n, f)
    print("  %d entries repointed; every one draws the same pixels" % changed)
    if WRITE:
        for f, b in out.items():
            open(f, "wb").write(b)
        new = img.copy(); np_ = new.load()
        for i in remap:
            for k in range(64):
                np_[(i % 16) * 8 + k % 8, (i // 16) * 8 + k // 8] = 0
        new.save(os.path.join(PD, "tiles.png"))
        print("  written: %d metatile files; %d slots blanked" % (len(out), len(remap)))


def secondary(symbols):
    """A town tileset's own tiles are drawn only by its own blocks, so its duplicates can be merged
    the same way without touching any other file -- except the slots its tileset animation writes."""
    anim_src = open(os.path.join(GBA, "src/tileset_anims.c")).read()
    for symbol in symbols:
        d = tdir(symbol)
        name = symbol.replace("gTileset_", "")
        stem = re.sub(r"(City|Town|Island)$", "", name)            # the animation functions say Celadon, not CeladonCity
        body = "".join(re.findall(r"static void \w*%s\w*\([^)]*\)\s*\{.*?\n\}" % stem, anim_src, re.S))
        anim = set()
        for start in re.findall(r"TILE_OFFSET_4BPP\((\d+)\)", body):
            anim |= set(range(int(start) - 640, int(start) - 640 + 32))
        img = Image.open(os.path.join(d, "tiles.png")); px = img.load()
        n = img.height // 8 * 16
        tile = lambda i: tuple(px[(i % 16) * 8 + k % 8, (i // 16) * 8 + k // 8] for k in range(64))
        hf = lambda t: tuple(t[(k // 8) * 8 + 7 - k % 8] for k in range(64))
        vf = lambda t: tuple(t[(7 - k // 8) * 8 + k % 8] for k in range(64))
        meta = bytearray(open(os.path.join(d, "metatiles.bin"), "rb").read())
        keeper, remap = {}, {}
        for i in range(n):
            if i in anim:
                continue
            t = tile(i)
            if not any(t):
                continue
            variants = {0: t, 0x400: hf(t), 0x800: vf(t), 0xC00: hf(vf(t))}
            key = min(variants.values())
            f = next(fl for fl, v in variants.items() if v == key)
            if key not in keeper:
                keeper[key] = (i, f); continue
            remap[i] = (keeper[key][0], keeper[key][1] ^ f)
        old = bytes(meta); changed = 0
        for k in range(len(meta) // 2):
            v = struct.unpack_from("<H", meta, k * 2)[0]; i = (v & 0x3FF) - 640
            if 0 <= i and i in remap:
                kk, flip = remap[i]
                struct.pack_into("<H", meta, k * 2, (v & ~0x0FFF) | (640 + kk) | ((v & 0x0C00) ^ flip)); changed += 1
        def draw(v):
            t = tile((v & 0x3FF) - 640)
            if v & 0x400: t = hf(t)
            if v & 0x800: t = vf(t)
            return t
        for k in range(len(meta) // 2):
            a, c = struct.unpack_from("<H", old, k * 2)[0], struct.unpack_from("<H", meta, k * 2)[0]
            if a != c:
                assert draw(a) == draw(c) and a >> 12 == c >> 12, "%s entry %d would change" % (symbol, k)
        print("  %s: %d duplicate tiles, %d entries repointed, each drawing the same pixels; animation slots kept: %d" % (symbol, len(remap), changed, len(anim)))
        if WRITE:
            open(os.path.join(d, "metatiles.bin"), "wb").write(meta)
            new = img.copy(); np_ = new.load()
            for i in remap:
                for k in range(64):
                    np_[(i % 16) * 8 + k % 8, (i // 16) * 8 + k // 8] = 0
            new.save(os.path.join(d, "tiles.png"))


if __name__ == "__main__":
    if "--secondary" in sys.argv:
        secondary([a for a in sys.argv[sys.argv.index("--secondary") + 1:] if a.startswith("gTileset_")])
    else:
        main()
