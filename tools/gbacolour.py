#!/usr/bin/env python3
"""Convert a full-colour illustration into a GBA sprite.

    python3 tools/gbacolour.py art.png CODEMUSAI front
    python3 tools/gbacolour.py art.png CODEMUSAI back

The companion to tools/gbasprite.py. That one lays a type palette over our
four-tone Game Boy art and spends four of the sixteen colours; this one takes
art that was drawn in colour and spends the rest.

Index 0 is the background and Gen 3 treats it as transparent, so the subject
gets fifteen. They are chosen by median cut over the pixels that are actually
in the sprite -- quantising the white surround as well would waste a slot on a
colour nothing draws.

The outline is protected. Generated art puts a lot of nearly-black pixels on an
edge, and a median cut will happily merge them into the darkest body colour and
leave the creature with no outline at all. Anything below OUTLINE luminance is
forced to index 1, pure black, before the cut runs on everything else.
"""
import os, re, subprocess, sys, zlib, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GB, GBA = os.path.join(ROOT, "engine"), os.path.join(ROOT, "engineGba")
SIZE, NCOLOURS, OUTLINE, BG_CUT = 64, 15, 60, 232

def read_rgb(path):
    if not path.lower().endswith(".png"):
        tmp = "/tmp/_gbacolour.png"
        subprocess.run(["sips", "-s", "format", "png", path, "--out", tmp],
                       capture_output=True)
        path = tmp
    d = open(path, "rb").read(); i = 8; idat = b""; hdr = None; plte = None
    while i < len(d):
        ln = struct.unpack(">I", d[i:i+4])[0]; t = d[i+4:i+8]; c = d[i+8:i+8+ln]
        if t == b"IHDR": hdr = struct.unpack(">IIBBBBB", c)
        elif t == b"PLTE": plte = [tuple(c[k:k+3]) for k in range(0, len(c), 3)]
        elif t == b"IDAT": idat += c
        i += 12 + ln
    w, h, bd, ct = hdr[0], hdr[1], hdr[2], hdr[3]
    nch = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[ct]
    stride = (w * nch * bd + 7) // 8
    raw = zlib.decompress(idat); bpp = max(1, nch * bd // 8)
    out = bytearray(); prev = bytearray(stride); o = 0
    for _ in range(h):
        f = raw[o]; o += 1; line = bytearray(raw[o:o+stride]); o += stride
        for x in range(stride):
            a = line[x-bpp] if x >= bpp else 0
            b = prev[x]; c2 = prev[x-bpp] if x >= bpp else 0
            if f == 1: line[x] = (line[x] + a) & 255
            elif f == 2: line[x] = (line[x] + b) & 255
            elif f == 3: line[x] = (line[x] + (a + b) // 2) & 255
            elif f == 4:
                p = a + b - c2; pa, pb, pc = abs(p-a), abs(p-b), abs(p-c2)
                line[x] = (line[x] + (a if pa <= pb and pa <= pc else b if pb <= pc else c2)) & 255
        out += line; prev = line
    px = []
    for y in range(h):
        row = []
        for x in range(w):
            if ct == 3: row.append(plte[out[y*stride + x]])
            elif ct == 2: k = y*stride + x*3; row.append(tuple(out[k:k+3]))
            elif ct == 6: k = y*stride + x*4; row.append(tuple(out[k:k+3]))
            else: v = out[y*stride + x]; row.append((v, v, v))
        px.append(row)
    return w, h, px

def lum(c): return (c[0]*299 + c[1]*587 + c[2]*114) // 1000

def median_cut(pixels, n):
    boxes = [pixels]
    while len(boxes) < n:
        boxes.sort(key=lambda b: max(max(p[i] for p in b) - min(p[i] for p in b)
                                     for i in range(3)) if len(b) > 1 else -1)
        big = boxes.pop()
        if len(big) < 2: boxes.append(big); break
        ch = max(range(3), key=lambda i: max(p[i] for p in big) - min(p[i] for p in big))
        big.sort(key=lambda p: p[ch]); m = len(big) // 2
        boxes += [big[:m], big[m:]]
    return [tuple(sum(p[i] for p in b) // len(b) for i in range(3)) for b in boxes if b]

def main():
    if len(sys.argv) < 4: sys.exit(__doc__)
    src, daemon, kind = sys.argv[1], sys.argv[2].upper(), sys.argv[3]
    van = subprocess.run(["git", "-C", GB, "show", "upstream/master:data/pokemon/names.asm"],
                         capture_output=True, text=True).stdout
    pat = r'dname\s+"([^"]*)"'
    pairs = {o: v for v, o in zip(re.findall(pat, van),
             re.findall(pat, open(os.path.join(GB, "data/pokemon/names.asm")).read())) if v != o}
    if daemon not in pairs: sys.exit("no daemon called %s" % daemon)
    FIX = {"NIDORAN♀": "nidoran_f", "NIDORAN♂": "nidoran_m",
           "FARFETCH'D": "farfetchd", "MR.MIME": "mr_mime"}
    d = FIX.get(pairs[daemon], pairs[daemon].lower().replace(" ", "_").replace(".", ""))
    outdir = os.path.join(GBA, "graphics/pokemon", d)
    if not os.path.isdir(outdir): sys.exit("no %s" % outdir)

    w, h, px = read_rgb(src)
    xs = [x for y in range(h) for x in range(w) if lum(px[y][x]) < BG_CUT]
    ys = [y for y in range(h) for x in range(w) if lum(px[y][x]) < BG_CUT]
    if not xs: sys.exit("no subject found -- is the background white?")
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    side = int(max(x1-x0+1, y1-y0+1) * 1.04)
    sx, sy = (x0+x1)//2 - side//2, (y0+y1)//2 - side//2
    step = side / SIZE

    grid, body = [[0]*SIZE for _ in range(SIZE)], []
    samples = []
    for gy in range(SIZE):
        row = []
        for gx in range(SIZE):
            ax, ay = sx + int((gx+0.5)*step), sy + int((gy+0.5)*step)
            c = px[ay][ax] if 0 <= ax < w and 0 <= ay < h else (255, 255, 255)
            row.append(c)
            if lum(c) >= BG_CUT: pass
            elif lum(c) < OUTLINE: pass
            else: samples.append(c)
        body.append(row)
    # Gen 3 gives a species ONE palette, shared by front and back. So the back
    # must not compute its own -- doing that would recolour the front sprite
    # that is already in the ROM. The front defines the palette; the back maps
    # into it.
    palfile = os.path.join(outdir, "normal.pal")
    reuse = kind == "back" and os.path.exists(os.path.join(outdir, "front.png"))
    if reuse:
        rows = open(palfile, "rb").read().decode().splitlines()[3:]
        palette = [tuple(int(v) for v in r.split()) for r in rows if r.strip()][:16]
        print("  reusing the front's palette (Gen 3 shares one per species)")
    else:
        palette = ([(205, 205, 172), (0, 0, 0)]
                   + median_cut(samples or [(128, 128, 128)], NCOLOURS - 1))[:16]

    for gy in range(SIZE):
        for gx in range(SIZE):
            c = body[gy][gx]
            if lum(c) >= BG_CUT: grid[gy][gx] = 0
            elif lum(c) < OUTLINE: grid[gy][gx] = 1
            else:
                grid[gy][gx] = min(range(2, len(palette)),
                    key=lambda i: sum((palette[i][k]-c[k])**2 for k in range(3)))

    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "gs", os.path.join(os.path.dirname(os.path.abspath(__file__)), "gbasprite.py"))
    # gbasprite runs work at import, so the writers are re-declared here instead.
    def write_png4(path, g, pal):
        plte = b"".join(bytes(c) for c in pal) + b"\x00\x00\x00" * (16 - len(pal))
        raw = b""
        for row in g:
            packed = bytearray()
            for i in range(0, len(row), 2): packed.append((row[i] << 4) | row[i+1])
            raw += b"\x00" + bytes(packed)
        def ch(t, dta):
            c = t + dta; return struct.pack(">I", len(dta)) + c + struct.pack(">I", zlib.crc32(c))
        open(path, "wb").write(b"\x89PNG\r\n\x1a\n"
            + ch(b"IHDR", struct.pack(">IIBBBBB", SIZE, SIZE, 4, 3, 0, 0, 0))
            + ch(b"PLTE", plte) + ch(b"IDAT", zlib.compress(raw)) + ch(b"IEND", b""))
    def write_pal(path, pal):
        full = list(pal) + [(0, 0, 0)] * (16 - len(pal))
        body = ["JASC-PAL", "0100", "16"] + ["%d %d %d" % c for c in full]
        open(path, "wb").write(("\r\n".join(body) + "\r\n").encode())

    write_png4(os.path.join(outdir, "%s.png" % kind), grid, palette)
    if not reuse:
        write_pal(palfile, palette)
        write_pal(os.path.join(outdir, "shiny.pal"), palette)
    used = len(set(v for r in grid for v in r))
    print("  %s %s -> graphics/pokemon/%s/%s.png  %d of 16 colours used"
          % (daemon, kind, d, kind, used))

main()
