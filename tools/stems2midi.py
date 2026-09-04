#!/usr/bin/env python3
"""Build the title theme from a separated stem set.

    ./bpvenv/bin/python tools/bpextract.py "<dir>/1 Bass.mp3" notes/bass.json 30 400
    python3 tools/stems2midi.py <dir> --notes notes --write mus_title

The first step needs its own interpreter; see tools/bpextract.py. The second
runs on the machine's own Python, so nothing here is pinned to basic-pitch.

WHY THIS REPLACES mp3midi.py FOR THIS JOB. That tool had to guess which notes
belonged to which voice, because a mix is one signal: it split the melody from
the bass with a filter at 250Hz and INFERRED the middle voice from a chroma
profile, because a monophonic pitch tracker cannot hear two notes at once.
Both of those are approximations of an instrument list we now simply have.

Two things changed. Suno exports STEMS, so each instrument arrives on its own,
and Basic Pitch is POLYPHONIC, so chords come back as chords. Nothing here is
inferred: every note in the output was heard in a file that contained one
instrument.

WHAT IS STILL LOSSY, AND DELIBERATELY. The GBA plays one note per track, so a
chord is reduced to a single voice -- the highest, except in the bass where it
is the lowest, which is what a musician reading a lead sheet would do. And
timing is quantised to a sixteenth-note grid taken from the mix's own beats.
7.14g's arrangement survives that; a performance does not.

STEMS ARE TIME-ALIGNED AT ZERO. They are shorter than the mix and each other
because the export trims where an instrument stops, not because they are
offset: five of seven stems' loudness contours correlate best against the mix
at exactly lag zero, and a separator emits aligned stems by construction.
"""
import importlib.util, json, os, sys, warnings
warnings.filterwarnings("ignore")
import numpy as np
import librosa

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GBA = os.path.join(ROOT, "engineGba")
NOTES = "notes"        # overridden by --notes

spec = importlib.util.spec_from_file_location("mp3midi", os.path.join(HERE, "mp3midi.py"))
mm = importlib.util.module_from_spec(spec); spec.loader.exec_module(mm)

DIV = 4                    # sixteenths -- Basic Pitch's timing earns the resolution
mm.DIV = DIV               # midi_bytes does its tick maths off this; keep them equal

#  GM programs into voicegroup191 -- see tools/gbavoices.py.
PIANO, HARP, BASS, TIMPANI, STRINGS, TRUMPET = 0, 46, 33, 47, 48, 56

#  stem file -> (label, program, velocity, which voice of a chord to keep)
STEMS = [
    ("7 Brass",    "brass",   TRUMPET, 100, "high"),
    #  the synth stem is the busiest line in the track -- 233 of 400 cells --
    #  which is an arpeggio, and an arpeggio is what a harp is for. A
    #  glockenspiel across that many cells at 152 BPM is a smoke alarm.
    ("5 Synth",    "synth",   HARP,     64, "high"),
    ("4 Strings",  "strings", STRINGS,  78, "high"),
    ("2 Keyboard", "keys",    PIANO,    58, "high"),
    ("1 Bass",     "bass",    BASS,     96, "low"),
]

def register(notes):
    """The band a stem actually plays in. Basic Pitch reports upper partials as
    real notes -- the brass came back reaching G#6 and the keyboard F7 -- and a
    sparse high tail is exactly what a percentile window removes. It is measured
    per stem rather than assumed, because these are five different instruments."""
    p = sorted(n[2] for n in notes)
    lo = p[int(len(p) * 0.03)]
    hi = p[int(len(p) * 0.90)]
    return lo, hi

def cells_from(notes, grid, times, keep):
    """One pitch per grid cell -- the GBA plays one note per track, so a chord
    has to become a line. A note occupies every cell it sounds through, so a
    held note repeats and merge() joins it back up.

    TAKING THE TOP NOTE IS WRONG and it was what this did first: the top note
    of a cell is as often a harmonic as a melody, so the line leapt an octave
    and back. It picks the LOUDEST note now, and where two are within a hair of
    each other it takes the one NEAREST WHAT IT WAS ALREADY PLAYING -- which is
    the assumption a musician transcribing by ear makes without noticing."""
    lo, hi = register(notes)
    out = [None] * (len(grid) - 1)
    prev, quiet = None, 0
    for i in range(len(out)):
        t0, t1 = times[i], times[i + 1]
        live = [n for n in notes if n[0] < t1 and n[1] > t0 and lo <= n[2] <= hi]
        if not live:
            quiet += 1
            if quiet > DIV * 2:        # after half a bar of rest, no line to follow
                prev = None
            continue
        quiet = 0
        if keep == "low":
            pick = min(live, key=lambda n: (n[2], -n[3]))
        else:
            top = max(n[3] for n in live)
            near = [n for n in live if n[3] >= top - 0.08]
            pick = (min(near, key=lambda n: abs(n[2] - prev)) if prev is not None
                    else max(near, key=lambda n: n[3]))
        out[i] = prev = pick[2]
    return out

def snap(cells, scale):
    moved = 0
    out = []
    for n in cells:
        if n is None or n % 12 in scale:
            out.append(n); continue
        out.append(min((abs(c), n + c) for c in (-1, 1, -2, 2)
                       if (n + c) % 12 in scale)[1])
        moved += 1
    return out, moved

def timpani(drums, sr, times, bass_cells):
    """One stroke a bar, on the loudest onset in it, pitched from the bass.
    This is the part that makes it a theme rather than a melody."""
    env = librosa.onset.onset_strength(y=drums, sr=sr, hop_length=512)
    frames = librosa.frames_to_time(np.arange(len(env)), sr=sr, hop_length=512)
    per_bar = DIV * 4
    out = []
    for start in range(0, len(bass_cells), per_bar):
        bar = range(start, min(start + per_bar, len(bass_cells)))
        seg = [(env[j], t) for j, t in enumerate(frames)
               if times[bar[0]] <= t < times[min(bar[-1] + 1, len(times) - 1)]]
        pitch = next((bass_cells[i] for i in bar if bass_cells[i] is not None), None)
        while pitch is not None and pitch < 36:
            pitch += 12
        hit = pitch if seg and max(s for s, _ in seg) > np.mean(env) else None
        out.append((hit, 2))
        out.append((None, len(bar) - 2))
    return out

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    d = os.path.expanduser(sys.argv[1])
    global NOTES
    if "--notes" in sys.argv:
        NOTES = os.path.expanduser(sys.argv[sys.argv.index("--notes") + 1])
    mix_path = os.path.join(os.path.dirname(d.rstrip("/")), "Star Key Ascend.mp3")

    y, sr = librosa.load(mix_path, sr=22050, mono=True)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    tempo = float(tempo)
    chroma = librosa.feature.chroma_cqt(y=librosa.effects.harmonic(y), sr=sr, hop_length=512)
    (k1, n1, m1), (k2, n2, m2) = mm.key_of(chroma)
    print("  mix        %.1f s, %.1f BPM, %s %s (runner-up %s %s, %.2f vs %.2f)"
          % (len(y) / sr, tempo, n1, m1, n2, m2, k1, k2))

    grid = []
    for i in range(len(beats) - 1):
        for j in range(DIV):
            grid.append(int(beats[i] + (beats[i + 1] - beats[i]) * j / DIV))
    grid.append(int(beats[-1]))
    times = librosa.frames_to_time(np.array(grid), sr=sr, hop_length=512)
    print("  grid       %d cells of a %d-per-beat grid" % (len(grid) - 1, DIV))

    root = mm.NAMES.index(n1)
    degrees = [0, 2, 4, 5, 7, 9, 11] if m1 == "major" else [0, 2, 3, 5, 7, 8, 10]
    scale = {(root + x) % 12 for x in degrees}

    parts, bass_cells = [], None
    for fname, label, program, vel, keep in STEMS:
        jf = os.path.join(NOTES, fname + ".json")
        if not os.path.isfile(jf):
            print("  %-10s -- no notes file, skipped" % label); continue
        raw = json.load(open(jf))
        cells = cells_from(raw, grid, times, keep)
        cells, moved = snap(cells, scale)
        if label == "bass":
            bass_cells = cells
        sounded = [n for n in cells if n is not None]
        print("  %-10s %4d heard, %4d cells, %s..%s, %d snapped"
              % (label, len(raw), len(sounded),
                 librosa.midi_to_note(min(sounded)), librosa.midi_to_note(max(sounded)),
                 moved))
        parts.append((program, vel, mm.merge(cells)))

    drums, _ = librosa.load(os.path.join(d, "0 Drums.mp3"), sr=sr, mono=True)
    if bass_cells:
        t = timpani(drums, sr, times, bass_cells)
        parts.append((TIMPANI, 88, t))
        print("  timpani    %d strokes" % sum(1 for n, _ in t if n is not None))

    if "--write" in sys.argv:
        slot = sys.argv[sys.argv.index("--write") + 1]
        dst = os.path.join(GBA, "sound/songs/midi/%s.mid" % slot)
        if not os.path.isfile(dst):
            sys.exit("  !! no slot called %s" % slot)
        open(dst, "wb").write(mm.midi_bytes(tempo, parts))
        print("  written    sound/songs/midi/%s.mid, %d tracks" % (slot, len(parts)))
    else:
        print("\n  (report only; pass --write <slot>)")

main()
