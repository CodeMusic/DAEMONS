#!/usr/bin/env python3
"""BPS patches: make one from a clean ROM and ours, and apply one to check it (the user's, 2026-09-24).

    python3 tools/bps.py create SOURCE.gba TARGET.gba OUT.bps     # the patch that turns SOURCE into TARGET
    python3 tools/bps.py apply  SOURCE.gba PATCH.bps OUT.gba      # apply it (and check all three CRCs)

WHY A PATCH. The ROMs are never posted (ROM RELEASE/WHERES_THE_ROMS.md). A BPS patch is how ROM hacks are shared:
the player applies it to a copy of FireRed or LeafGreen they own -- in any patcher, Rom Patcher JS in a browser
included -- and gets DAEMONS. The patch holds our bytes and instructions to copy the rest from THEIR ROM.

THE FORMAT is byuu's BPS1: a header, then actions, each a varint of (length-1)<<2 | kind --
    0 SourceRead   copy from the source at the same offset
    1 TargetRead   literal bytes follow
    2 SourceCopy   copy from anywhere in the source (a signed relative offset)
    3 TargetCopy   copy from what has already been written (unused here)
-- then the CRC32 of the source, the target and the patch itself.

THE ENCODER is simple and deliberate: at each position it takes the longest of a same-offset run and a moved run
found through a hash of the source's 16-byte blocks (aligned, so the index stays small), extends a moved run
backwards over the pending literals, and emits literals for anything shorter than it is worth. No external tool:
Homebrew has no flips, and a patch this project ships should be made by code it can read.
"""
import struct, sys, zlib

KEY = 16          # bytes hashed per source block
MIN_RUN = 24      # a run shorter than this is cheaper as literals


def varint(n):
    out = bytearray()
    while True:
        x = n & 0x7F
        n >>= 7
        if n == 0:
            out.append(0x80 | x)
            return bytes(out)
        out.append(x)
        n -= 1


def read_varint(buf, i):
    n, shift = 0, 1
    while True:
        x = buf[i]
        i += 1
        n += (x & 0x7F) * shift
        if x & 0x80:
            return n, i
        shift <<= 7
        n += shift


def match_len(a, ai, b, bi, limit):
    n = 0
    step = 4096
    while n < limit:
        k = min(step, limit - n)
        if a[ai + n:ai + n + k] == b[bi + n:bi + n + k]:
            n += k
            continue
        while n < limit and a[ai + n] == b[bi + n]:
            n += 1
        return n
    return n


def create(src, tgt):
    index = {}
    for off in range(0, len(src) - KEY + 1, KEY):
        index.setdefault(src[off:off + KEY], off)
    out = bytearray(b"BPS1" + varint(len(src)) + varint(len(tgt)) + varint(0))
    literal_start, p, src_rel = 0, 0, 0

    def flush_literals(end):
        if end > literal_start:
            out.extend(varint(((end - literal_start - 1) << 2) | 1))
            out.extend(tgt[literal_start:end])

    n = len(tgt)
    while p < n:
        best_len, best_kind, best_off = 0, 0, 0
        if p < len(src) and src[p:p + MIN_RUN] == tgt[p:p + MIN_RUN]:
            best_len = match_len(src, p, tgt, p, min(len(src), n) - p)
        if best_len < MIN_RUN * 4:
            off = index.get(tgt[p:p + KEY])
            if off is not None:
                m = match_len(src, off, tgt, p, min(len(src) - off, n - p))
                back = 0          # extend backwards over the literals still pending
                while back < p - literal_start and off - back > 0 and src[off - back - 1] == tgt[p - back - 1]:
                    back += 1
                if m + back > best_len and m + back >= MIN_RUN:
                    best_len, best_kind, best_off = m + back, 2, off - back
                    p -= back
        if best_len >= MIN_RUN:
            flush_literals(p)
            if best_kind == 0:
                out.extend(varint(((best_len - 1) << 2) | 0))
            else:
                rel = best_off - src_rel
                out.extend(varint(((best_len - 1) << 2) | 2))
                out.extend(varint((abs(rel) << 1) | (1 if rel < 0 else 0)))
                src_rel = best_off + best_len
            p += best_len
            literal_start = p
        else:
            p += 1
    flush_literals(n)
    out.extend(struct.pack("<II", zlib.crc32(src), zlib.crc32(tgt)))
    out.extend(struct.pack("<I", zlib.crc32(out)))
    return bytes(out)


def apply(src, patch):
    if patch[:4] != b"BPS1":
        raise ValueError("not a BPS1 patch")
    body, (crc_src, crc_tgt, crc_patch) = patch[:-12], struct.unpack("<III", patch[-12:])
    if zlib.crc32(patch[:-4]) != crc_patch:
        raise ValueError("the patch is damaged (its own CRC does not match)")
    if zlib.crc32(src) != crc_src:
        raise ValueError("this is not the ROM the patch was made for (source CRC %08x, expected %08x)"
                         % (zlib.crc32(src), crc_src))
    i = 4
    src_size, i = read_varint(body, i)
    tgt_size, i = read_varint(body, i)
    meta, i = read_varint(body, i)
    i += meta
    out = bytearray()
    src_rel = tgt_rel = 0
    while i < len(body):
        data, i = read_varint(body, i)
        kind, length = data & 3, (data >> 2) + 1
        if kind == 0:
            out.extend(src[len(out):len(out) + length])
        elif kind == 1:
            out.extend(body[i:i + length])
            i += length
        else:
            d, i = read_varint(body, i)
            rel = -(d >> 1) if d & 1 else d >> 1
            if kind == 2:
                src_rel += rel
                out.extend(src[src_rel:src_rel + length])
                src_rel += length
            else:
                tgt_rel += rel
                for _ in range(length):
                    out.append(out[tgt_rel])
                    tgt_rel += 1
    if len(out) != tgt_size or zlib.crc32(out) != crc_tgt:
        raise ValueError("applied, but the result is wrong (target CRC mismatch)")
    return bytes(out)


def main():
    if len(sys.argv) != 5 or sys.argv[1] not in ("create", "apply"):
        print(__doc__.split("\n\n")[0])
        return 2
    a, b = open(sys.argv[2], "rb").read(), open(sys.argv[3], "rb").read()
    if sys.argv[1] == "create":
        patch = create(a, b)
        if apply(a, patch) != b:
            raise SystemExit("  the patch does not reproduce the target -- not written")
        open(sys.argv[4], "wb").write(patch)
        print("  %s: %d bytes, checked by applying it" % (sys.argv[4], len(patch)))
    else:
        open(sys.argv[4], "wb").write(apply(a, b))
        print("  %s written" % sys.argv[4])
    return 0


if __name__ == "__main__":
    sys.exit(main())
