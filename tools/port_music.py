#!/usr/bin/env python3
"""Carry our music into the GBA build by writing MIDI.

    python3 tools/port_music.py [--write]

The two engines could not be less alike. The Game Boy build IS the sequencer --
`note C_, 8` writes a frequency into a hardware channel. The GBA has a software
mixer, and pokefirered builds its music from .mid files through mid2agb. So
nothing can be copied; the notes have to be re-emitted in another format.

Which is fine, because the notes are the part worth keeping.

Each track REPLACES the MIDI of a slot that already exists rather than claiming
a new one. Adding a song means a new constant, a new song_table row and every
index after it moving; replacing means none of that. The slots were chosen so
the map that plays them is the map the track was written for:

    titletheme -> mus_title      the front door
    slatecity  -> mus_pewter     Pewter IS Slate City
    thebleed   -> mus_route1     Routes 1 and 2

CONVERSIONS, all of them assumptions worth writing down:
  * eight GB ticks is one quarter note -- our own tracks are built in bars of
    32 ticks as four notes of eight, so this is what we wrote them to mean
  * GB octave N becomes MIDI octave N, so `octave 4 / note C_` is middle C and
    a bass line at `octave 2` lands where a bass line belongs
  * the GB `tempo` value is used as BPM directly
The first two are structural. The third is a guess and the most likely thing to
want tuning by ear.
"""
import os, re, struct, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GB, GBA = os.path.join(ROOT, "engine"), os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv
TPQ, TICKS_PER_QUARTER = 480, 8          # MIDI resolution, GB ticks per quarter

TRACKS = [("titletheme", "mus_title"), ("slatecity", "mus_pewter"),
          ("thebleed", "mus_route1")]
# brazen.asm has nowhere to go yet. FireRed ships no mus_saffron -- Saffron
# shares a theme with other cities -- so giving Brazen a slot means either
# taking one that belongs to a city we have also renamed, or adding a song and
# moving every index after it. That is a decision, not a lookup, and it is not
# made here.

SEMI = {"C_": 0, "C#": 1, "D_": 2, "D#": 3, "E_": 4, "F_": 5,
        "F#": 6, "G_": 7, "G#": 8, "A_": 9, "A#": 10, "B_": 11}

def parse(path):
    """-> (tempo, [channel, ...]) where a channel is [(midi_note|None, ticks)]."""
    text = open(path).read()
    tempo = int(re.search(r'tempo (\d+)', text).group(1))
    chans = []
    for body in re.split(r'^Music_\w+_Ch\d+::', text, flags=re.M)[1:]:
        octave, events = 4, []
        for line in body.splitlines():
            line = line.split(";")[0].strip()
            m = re.match(r'octave (\d+)', line)
            if m:
                octave = int(m.group(1)); continue
            m = re.match(r'note (\w[_#]), (\d+)', line)
            if m:
                events.append(((octave + 1) * 12 + SEMI[m.group(1)], int(m.group(2)))); continue
            m = re.match(r'rest (\d+)', line)
            if m:
                events.append((None, int(m.group(1))))
        if events:
            chans.append(events)
    return tempo, chans

def vlq(n):
    out = bytearray([n & 0x7F]); n >>= 7
    while n:
        out.insert(0, (n & 0x7F) | 0x80); n >>= 7
    return bytes(out)

def track(events, chan, repeats=2):
    data = bytearray()
    data += b"\x00" + bytes([0xC0 | chan, 0])          # program change
    for _ in range(repeats):
        rest = 0
        for note, ticks in events:
            dur = ticks * TPQ // TICKS_PER_QUARTER
            if note is None:
                rest += dur; continue
            data += vlq(rest) + bytes([0x90 | chan, note, 100])
            data += vlq(max(1, dur - 6)) + bytes([0x80 | chan, note, 0])
            rest = 6
    data += b"\x00\xFF\x2F\x00"
    return b"MTrk" + struct.pack(">I", len(data)) + bytes(data)

def midi(tempo, chans):
    head = bytearray(b"\x00\xFF\x51\x03") + struct.pack(">I", 60000000 // tempo)[1:]
    head += b"\x00\xFF\x2F\x00"
    out = b"MThd" + struct.pack(">IHHH", 6, 1, len(chans) + 1, TPQ)
    out += b"MTrk" + struct.pack(">I", len(head)) + bytes(head)
    for i, ev in enumerate(chans):
        out += track(ev, i)
    return out

rc = 0
for name, slot in TRACKS:
    src = os.path.join(GB, "audio/music/%s.asm" % name)
    dst = os.path.join(GBA, "sound/songs/midi/%s.mid" % slot)
    if not os.path.exists(src):
        print("  !! no %s" % src); rc = 1; continue
    if not os.path.exists(dst):
        print("  !! no slot %s.mid to replace" % slot); rc = 1; continue
    tempo, chans = parse(src)
    notes = sum(1 for c in chans for n, _ in c if n is not None)
    print("  %-11s -> %-14s %d channels, %d notes, tempo %d"
          % (name, slot, len(chans), notes, tempo))
    if not chans:
        print("  !! parsed no channels"); rc = 1; continue
    if WRITE:
        open(dst, "wb").write(midi(tempo, chans))
if WRITE and rc == 0:
    print("  written")
sys.exit(rc)
