#!/usr/bin/env python3
"""THE NEXUS's own theme, MUS_NEXUS (T-409, DRAFT): O CHRISTMAS TREE's feel, built on the singing fir's notes.

    python3 tools/gennexustheme.py            # report
    python3 tools/gennexustheme.py --write    # engineGba/sound/songs/midi/mus_nexus.mid

The user, 2026-10-16: the NEXUS gets music "with an o-christmas-tree feel built on the fir's notes". The fir sings
the carol's first phrase in B-flat, the painting's key (src/field_specials.c, sFirTune; the user, 2026-10-16). The
notes below are written in A-flat and sounded a whole tone up (KEY), so the tree's song and the room's are one piece. Sixteen bars and a loop:

  A (1-8)   harp arpeggios under a held string chord; the glockenspiel -- the tree's sparkle -- answers with the
            phrase's first two gestures only (E-flat to the three A-flats; B-flat to the three Cs), never the whole
            tune, so the room hints at the song the tree will sing.
  B (9-16)  the strings take the fir's whole phrase at half speed, the harp keeps moving, and the glockenspiel lights
            one high note each bar.

Bank voicegroup191 (the title's, real instruments): 46 harp, 48 string ensemble, 9 glockenspiel, 33 bass.
"""
import os, struct, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "engineGba", "sound", "songs", "midi", "mus_nexus.mid")
TPQ, CELL = 48, 12          # a cell is a sixteenth; a 3/4 bar is twelve
BAR = 12
TEMPO = 84
KEY = 2                     # written in A-flat, sounded in B-flat

#  A-flat major. MIDI numbers.
Ab3, Bb3, C4, Db4, Eb4, F4, G4, Ab4, Bb4, C5, Db5, Eb5 = 56, 58, 60, 61, 63, 65, 67, 68, 70, 72, 73, 75
CHORD = {  # root, third, fifth, around A-flat 3
    "Ab": (56, 60, 63), "Db": (49, 53, 56), "Eb": (51, 55, 58), "Fm": (53, 56, 60), "Eb7": (51, 55, 61),
}
BARS = ["Ab", "Ab", "Db", "Eb", "Eb", "Ab", "Db", "Eb",      # A
        "Ab", "Ab", "Fm", "Ab", "Eb", "Eb7", "Eb", "Ab"]     # B

def harp():
    out = []
    for c in BARS:
        r, t, f = CHORD[c]
        out += [(n, 2) for n in (r, f, r + 12, t + 12, r + 12, f)]
    return out

def bass():
    return [(CHORD[c][0] - 12, BAR) for c in BARS]

def strings():
    #  A: the chord held, softly; bar 8 gives way to the phrase's pick-up. B: the fir's phrase, doubled in length.
    a = [(CHORD[c], BAR) for c in BARS[:7]] + [(None, 4), (Eb4, 8)]
    b = [(Ab4, 6), (Ab4, 2), (Ab4, 12), (Bb4, 4),
         (C5, 6), (C5, 2), (C5, 12), (C5, 4),
         (Bb4, 4), (C5, 4), (Db5, 8), (G4, 8),
         (Bb4, 8), (Ab4, 16)]
    return a + b

def glock():
    up = 12
    a = [(None, 8), (Eb4 + 2 * up, 4), (Ab4 + up, 3), (Ab4 + up, 1), (Ab4 + up, 8), (None, 2 * BAR),
         (None, 8), (Bb4 + up, 4), (C5 + up, 3), (C5 + up, 1), (C5 + up, 8), (None, 2 * BAR)]
    b = []
    for c in BARS[8:]:
        b += [(None, 8), (CHORD[c][2] + 2 * up, 4)]
    return a + b

PARTS = [(48, 70, strings()), (46, 96, harp()), (9, 84, glock()), (33, 90, bass())]

def var(n):
    out = [n & 0x7F]; n >>= 7
    while n:
        out.insert(0, (n & 0x7F) | 0x80); n >>= 7
    return bytes(out)

def chunk(tag, data):
    return tag + struct.pack(">I", len(data)) + data

def midi():
    end = BAR * len(BARS) * CELL
    for _, _, notes in PARTS:
        assert sum(c for _, c in notes) == BAR * len(BARS), [sum(c for _, c in n) for _, _, n in PARTS]
    head = bytearray(b"\x00\xFF\x51\x03") + struct.pack(">I", 60000000 // TEMPO)[1:]
    head += b"\x00\xFF\x58\x04\x03\x02\x18\x08"                       # 3/4
    #  The loop markers go on the tempo track: mid2agb reads text events from the first track only (mp3midi.py).
    head += b"\x00\xFF\x01\x01[" + var(end) + b"\xFF\x01\x01]" + b"\x00\xFF\x2F\x00"
    out = chunk(b"MThd", struct.pack(">HHH", 1, len(PARTS) + 1, TPQ)) + chunk(b"MTrk", bytes(head))
    for ch, (program, vel, notes) in enumerate(PARTS):
        ev, rest = bytearray(b"\x00" + bytes((0xC0 | ch, program))), 0
        for pitch, cells in notes:
            ticks = cells * CELL
            if pitch is None:
                rest += ticks; continue
            ps = tuple(x + KEY for x in ((pitch,) if isinstance(pitch, int) else pitch))
            ev += var(rest) + bytes((0x90 | ch, ps[0], vel))
            for x in ps[1:]:
                ev += b"\x00" + bytes((0x90 | ch, x, vel))
            ev += var(ticks) + bytes((0x80 | ch, ps[0], 0))
            for x in ps[1:]:
                ev += b"\x00" + bytes((0x80 | ch, x, 0))
            rest = 0
        ev += var(rest) + b"\xFF\x2F\x00"
        out += chunk(b"MTrk", bytes(ev))
    return out

def main():
    data = midi()
    old = open(OUT, "rb").read() if os.path.exists(OUT) else None
    print("  mus_nexus.mid: %d bars of 3/4 at %d, %d tracks, %s" % (len(BARS), TEMPO, len(PARTS),
          "unchanged" if old == data else ("would write" if "--write" not in sys.argv else "written")))
    if "--write" in sys.argv and old != data:
        open(OUT, "wb").write(data)

if __name__ == "__main__":
    main()
