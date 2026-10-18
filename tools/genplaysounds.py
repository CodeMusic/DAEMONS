#!/usr/bin/env python3
"""PLAY's note sounds (T-417 P0): the HARP's and the FLUTE's eight naturals, as sound effects.

    python3 tools/genplaysounds.py            # report
    python3 tools/genplaysounds.py --write    # the sixteen .mid files and their four lines each

docs/private/draft-play-2026-10-17.md sec. 5. The timbres are OUR OWN (T-425, the user 2026-10-18 by ear): the HARP and
FLUTE of audio/instruments/, which tools/geninstruments.py also writes into the engine as voicegroup193 -- nothing
here is a sample:
  HARP   voice 0 of voicegroup193 (DirectSoundWaveData_daemons_harp) -- plucked: the sample rings out by itself
         and does not loop, so a press is a pluck.
  FLUTE  voice 1 of voicegroup193 (DirectSoundWaveData_daemons_flute) -- its sample loops and its envelope sustains,
         so the note is one long held note (TIE) and src/play.c fades it out and stops it when the button is let go:
         a breath.
(Until T-425 these were retail's sc88pro_harp, voice 46 of voicegroup128, and sc88pro_flute, voice 73 of
voicegroup132; both samples stay in the ROM, other songs play them.)

Eight naturals per instrument, C to the C above (SE_HARP_C .. SE_HARP_C_HIGH, SE_FLUTE_C .. SE_FLUTE_C_HIGH), on the
SE2 player as the toy piano's are; a sharp is its natural bent a semitone up and an octave is a bend of twelve
(m4aMPlayPitchControl, 256 to the semitone) -- which for a DirectSound voice is the same resampling a different MIDI
key would be, so the bend costs nothing a note of its own would not. The HARP's middle C is C4 (MIDI 60), the
FLUTE's C5 (MIDI 72), each instrument's comfortable middle; L and R take either an octave down or up.

Appended after MUS_NEXUS (350): 351-358 the HARP, 359-366 the FLUTE. A new song is FOUR lines (engine.md trap 25):
include/constants/songs.h, sound/song_table.inc, sound/songs/midi/midi.cfg and ld_script.ld -- the last is the one
whose absence the linker reports as a discarded section. This tool writes all four, and only adds what is missing.
"""
import os, re, struct, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
MIDI_DIR = os.path.join(GBA, "sound", "songs", "midi")
SONGS_H = os.path.join(GBA, "include", "constants", "songs.h")
TABLE = os.path.join(GBA, "sound", "song_table.inc")
CFG = os.path.join(MIDI_DIR, "midi.cfg")
LD = os.path.join(GBA, "ld_script.ld")

FIRST = 351                      # after MUS_NEXUS
NATURALS = [("C", 0), ("D", 2), ("E", 4), ("F", 5), ("G", 7), ("A", 9), ("B", 11), ("C_HIGH", 12)]
TPQ = 24
#  name, program, middle C, velocity, ticks held, midi.cfg flags
INSTRUMENTS = [
    ("HARP",  0, 60, 112, 4 * TPQ,  "-E -R50 -G193 -V110 -P4"),
    ("FLUTE", 1, 72, 100, 32 * TPQ, "-E -R50 -G193 -V100 -P4"),
]
TEMPO = 120


def var(n):
    out = [n & 0x7F]; n >>= 7
    while n:
        out.insert(0, (n & 0x7F) | 0x80); n >>= 7
    return bytes(out)


def chunk(tag, data):
    return tag + struct.pack(">I", len(data)) + data


def midi(program, pitch, vel, ticks):
    ev = bytearray(b"\x00\xFF\x51\x03") + struct.pack(">I", 60000000 // TEMPO)[1:]
    ev += b"\x00" + bytes((0xC0, program))
    ev += b"\x00" + bytes((0x90, pitch, vel))
    ev += var(ticks) + bytes((0x80, pitch, 0))
    ev += b"\x00\xFF\x2F\x00"
    return chunk(b"MThd", struct.pack(">HHH", 0, 1, TPQ)) + chunk(b"MTrk", bytes(ev))


def sounds():
    out, n = [], FIRST
    for name, program, c, vel, ticks, flags in INSTRUMENTS:
        for note, semis in NATURALS:
            label = "se_%s_%s" % (name.lower(), note.lower())
            out.append((n, "SE_%s_%s" % (name, note), label, midi(program, c + semis, vel, ticks), flags))
            n += 1
    return out


def ensure_lines(text, anchor_re, lines, what):
    """Add each line not already present, after the last line matching anchor_re (then after each added line)."""
    missing = [l for l in lines if l not in text]
    if not missing:
        return text, []
    rows = text.split("\n")
    at = max(i for i, r in enumerate(rows) if re.search(anchor_re, r))
    for l in missing:
        at += 1
        rows.insert(at, l)
    return "\n".join(rows), ["%s: + %s" % (what, l.strip()) for l in missing]


def main():
    write = "--write" in sys.argv
    changes = []
    snd = sounds()
    for n, const, label, data, flags in snd:
        p = os.path.join(MIDI_DIR, label + ".mid")
        old = open(p, "rb").read() if os.path.exists(p) else None
        if old != data:
            changes.append("%s.mid" % label)
            if write:
                open(p, "wb").write(data)

    h = open(SONGS_H, encoding="utf-8").read()
    want = [("#define %-25s %d" % (const, n)) + ("   // T-417: PLAY's notes (tools/genplaysounds.py)" if i == 0 else "")
            for i, (n, const, label, data, flags) in enumerate(snd)]
    have = {m.group(1): int(m.group(2)) for m in re.finditer(r"#define\s+(SE_(?:HARP|FLUTE)_\w+)\s+(\d+)", h)}
    if have != {const: n for n, const, *_ in snd}:
        h2 = re.sub(r"\n#define\s+SE_(?:HARP|FLUTE)_\w+[^\n]*", "", h)
        h2, c = ensure_lines(h2, r"#define\s+MUS_NEXUS\b", want, "songs.h")
        changes += c or ["songs.h: renumbered"]
        if write:
            open(SONGS_H, "w", encoding="utf-8").write(h2)

    for path, anchor, fmt, what in [
        (TABLE, r"song mus_nexus,", "\tsong %s, 2, 2", "song_table.inc"),
        (LD, r"sound/songs/midi/mus_nexus\.o", "        sound/songs/midi/%s.o(.rodata);", "ld_script.ld"),
    ]:
        t = open(path, encoding="utf-8").read()
        t2, c = ensure_lines(t, anchor, [fmt % label for _, _, label, _, _ in snd], what)
        changes += c
        if write and c:
            open(path, "w", encoding="utf-8").write(t2)

    t = open(CFG, encoding="utf-8").read()
    want = ["%-31s%s" % (label + ".mid:", flags) for _, _, label, _, flags in snd]
    stale = [l for l in re.findall(r"^se_(?:harp|flute)_\w+\.mid:.*$", t, flags=re.M) if l not in want]
    if stale:                                        # a line whose flags moved: take it out, ensure_lines puts it back
        t = re.sub(r"^(?:%s)\n" % "|".join(re.escape(l) for l in stale), "", t, flags=re.M)
    t2, c = ensure_lines(t, r"^mus_nexus\.mid:", ["%-31s%s" % (label + ".mid:", flags) for _, _, label, _, flags in snd],
                         "midi.cfg")
    changes += c + ["midi.cfg: - %s" % l for l in stale]
    if write and c:
        open(CFG, "w", encoding="utf-8").write(t2)

    print("  %d sounds, %d-%d: %s" % (len(snd), FIRST, FIRST + len(snd) - 1,
          "unchanged" if not changes else ("written" if write else "would write")))
    for c in changes:
        print("    " + c)


if __name__ == "__main__":
    main()
