#!/usr/bin/env python3
"""Transcribe audio to MIDI with signal processing, not with a language model.

    python3 tools/mp3midi.py track.mp3                 # report only
    python3 tools/mp3midi.py track.mp3 --write mus_title

4.9 records what happens when a model that cannot hear is asked to transcribe:
it hands back an earlier answer and admits, in its own DOUBT field, that the
transcription was a guess. The NO AUDIO gate exists to catch that, and when it
fires the answer is not a better prompt -- it is to stop asking.

So this does the work. librosa gives a beat grid, a chroma profile and two
pitch tracks; Krumhansl-Schmuckler gives the key by correlating the chroma
against twenty-four profiles. Nothing here is an opinion.

THREE VOICES ARE HEARD. The melody is pyin over everything above 250Hz, the
bass is pyin under 300Hz, and the middle voice is the strongest chord tone per
beat that is neither of them -- which is what an arpeggio is.

FIVE TRACKS ARE WRITTEN, and the other two are derived from those three. Three
was the Game Boy's limit and I carried it into a machine that does not have it:
vanilla's mus_vs_trainer runs ten.

EVERY TRACK OPENS WITH A GENERAL MIDI PROGRAM CHANGE. Without one mid2agb emits
no VOICE byte and the track plays on slot 0 of its bank -- which in the bank the
title used to point at is a square wave, so a transcription with the right notes,
the right tempo and the right key came back sounding like a Game Boy. The
programs below address voicegroup191 (see tools/gbavoices.py); they are ordinary
GM numbers because Gen 3's banks are GM-mapped.

QUANTISING IS THE LOSSY STEP AND IT IS DELIBERATE. Every cell of the beat grid
takes the median pitch of its voiced frames, and cells that are mostly unvoiced
become rests. A performance becomes a sequence, which is the thing the Game Boy
could store and the thing 7.14 was written in.
"""
import os, struct, sys, warnings
warnings.filterwarnings("ignore")
import numpy as np
import librosa
from scipy.signal import butter, filtfilt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
MAJOR = np.array([6.35,2.23,3.48,2.33,4.38,4.09,2.52,5.19,2.39,3.66,2.29,2.88])
MINOR = np.array([6.33,2.68,3.52,5.38,2.60,3.53,2.54,4.75,3.98,2.69,3.34,3.17])
HOP, DIV = 512, 2                 # DIV grid cells per beat -- eighth notes
CELLS_PER_BAR = DIV * 4           # assumed 4/4, which every theme here is

#  The arrangement. GM programs into voicegroup191; see tools/gbavoices.py.
TRUMPET, GLOCKENSPIEL, STRINGS, BASS, TIMPANI = 56, 9, 48, 33, 47

def key_of(chroma):
    prof = chroma.mean(axis=1)
    out = []
    for i in range(12):
        r = np.roll(prof, -i)
        out.append((np.corrcoef(r, MAJOR)[0, 1], NAMES[i], "major"))
        out.append((np.corrcoef(r, MINOR)[0, 1], NAMES[i], "minor"))
    out.sort(reverse=True)
    return out[0], out[1]

def track(sig, sr, lo, hi, kind):
    b, a = butter(4, (250 if kind == "high" else 300) / (sr / 2), kind)
    f0, _, _ = librosa.pyin(filtfilt(b, a, sig), sr=sr, hop_length=HOP,
                            fmin=librosa.note_to_hz(lo), fmax=librosa.note_to_hz(hi))
    return librosa.hz_to_midi(f0)

def cells_of(midi_track, grid):
    """One pitch per grid cell, or None where the cell is mostly unvoiced."""
    cells = []
    for i in range(len(grid) - 1):
        raw = midi_track[grid[i]:grid[i + 1]]
        seg = raw[~np.isnan(raw)]
        cells.append(int(round(np.median(seg))) if len(seg) > len(raw) * 0.4 else None)
    return cells

def merge(cells):
    """Repeats become held notes. Merging AFTER the per-cell pass, because the
    middle voice needs to know what the other two are doing in each cell and a
    merged list no longer lines up with the grid."""
    notes, i = [], 0
    while i < len(cells):
        j = i
        while j + 1 < len(cells) and cells[j + 1] == cells[i]:
            j += 1
        notes.append((cells[i], j - i + 1))
        i = j + 1
    return notes

def midi_bytes(tempo, parts):
    """parts is (program, velocity, notes). The program change is not optional:
    mid2agb emits a VOICE byte only where the MIDI carries one."""
    TPQ = 48
    def var(n):
        out = [n & 0x7F]; n >>= 7
        while n:
            out.insert(0, (n & 0x7F) | 0x80); n >>= 7
        return bytes(out)
    def chunk(tag, data):
        return tag + struct.pack(">I", len(data)) + data
    head = bytearray(b"\x00\xFF\x51\x03") + struct.pack(">I", 60000000 // int(tempo))[1:]
    head += b"\x00\xFF\x2F\x00"
    out = chunk(b"MThd", struct.pack(">HHH", 1, len(parts) + 1, TPQ))
    out += chunk(b"MTrk", bytes(head))
    for ch, (program, vel, notes) in enumerate(parts):
        ev, rest = bytearray(b"\x00" + bytes((0xC0 | ch, program))), 0
        for pitch, cells in notes:
            ticks = cells * (TPQ // DIV)
            if pitch is None:
                rest += ticks; continue
            pitch = max(0, min(127, pitch))
            ev += var(rest) + bytes((0x90 | ch, pitch, vel))
            ev += var(ticks) + bytes((0x80 | ch, pitch, 0))
            rest = 0
        ev += var(rest) + b"\xFF\x2F\x00"
        out += chunk(b"MTrk", bytes(ev))
    return out

def octave_up(cells):
    """A glockenspiel doubling the trumpet. Notes already near the top of the
    sample's useful range stay where they are rather than turning to whistle."""
    return [None if n is None else (n + 12 if n + 12 <= 96 else n) for n in cells]

def downbeats(cells):
    """One timpani stroke a bar, on the bass note that bar actually lands on.
    This is the part that makes it sound like a theme rather than a melody."""
    out = []
    for start in range(0, len(cells), CELLS_PER_BAR):
        bar = cells[start:start + CELLS_PER_BAR]
        hit = next((n for n in bar if n is not None), None)
        while hit is not None and hit < 36:      # timpani, not a floor rumble
            hit += 12
        out.append((hit, 2))
        out.append((None, len(bar) - 2))
    return out

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = sys.argv[1]
    y, sr = librosa.load(src, sr=22050, mono=True)
    h = librosa.effects.harmonic(y)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    tempo = float(tempo)
    chroma = librosa.feature.chroma_cqt(y=h, sr=sr, hop_length=HOP)
    (k1, n1, m1), (k2, n2, m2) = key_of(chroma)
    print("  %s" % os.path.basename(src))
    print("  duration   %.1f s" % (len(y) / sr))
    print("  tempo      %.1f BPM" % tempo)
    print("  key        %s %s   (runner-up %s %s, correlation %.2f vs %.2f)"
          % (n1, m1, n2, m2, k1, k2))

    grid = []
    for i in range(len(beats) - 1):
        for d in range(DIV):
            grid.append(int(beats[i] + (beats[i + 1] - beats[i]) * d / DIV))
    grid.append(int(beats[-1]))

    mel_cells = cells_of(track(h, sr, 'C3', 'C7', "high"), grid)
    bass_cells = cells_of(track(h, sr, 'C1', 'C4', "low"), grid)

    # the middle voice: the strongest chord tone per beat that is neither
    mid = []
    for i in range(len(grid) - 1):
        col = chroma[:, grid[i]:grid[i + 1]].mean(axis=1) if grid[i + 1] > grid[i] else None
        if col is None or np.isnan(col).all():
            mid.append((None, 1)); continue
        order = np.argsort(-col)
        taken = {(mel_cells[i] or -1) % 12, (bass_cells[i] or -1) % 12}
        pc = next((int(p) for p in order if int(p) not in taken), int(order[0]))
        mid.append((pc + 60, 1))

    # pyin slips -- an octave here, a semitone there -- and a slip is audible in
    # a three-channel arrangement in a way it is not in a mix. The chroma is far
    # more confident about the key (0.88) than the pitch track is about any
    # single note, so notes outside the scale are moved to the nearest degree
    # and the count is reported. If that count is large, the key was wrong.
    root = NAMES.index(n1)
    degrees = [0, 2, 4, 5, 7, 9, 11] if m1 == "major" else [0, 2, 3, 5, 7, 8, 10]
    scale = {(root + d) % 12 for d in degrees}

    def snap(cells):
        moved = 0
        out = []
        for n in cells:
            if n is None:
                out.append(None); continue
            if n % 12 in scale:
                out.append(n); continue
            best = min((abs(c), n + c) for c in (-1, 1, -2, 2) if (n + c) % 12 in scale)
            moved += 1
            out.append(best[1])
        return out, moved

    mel_cells, m_moved = snap(mel_cells)
    bass_cells, b_moved = snap(bass_cells)
    voiced = sum(1 for n in mel_cells if n is not None)
    print("  snapped    %d melody and %d bass notes to the %s %s scale (%d%% of melody)"
          % (m_moved, b_moved, n1, m1, 100 * m_moved // max(1, voiced)))

    mel, bass = merge(mel_cells), merge(bass_cells)
    sounded = [n for n, _ in mel if n is not None]
    ups = sum(1 for a, b in zip(sounded, sounded[1:]) if b > a)
    downs = sum(1 for a, b in zip(sounded, sounded[1:]) if b < a)
    print("  melody     %d notes, %s..%s" % (len(sounded),
          librosa.midi_to_note(min(sounded)), librosa.midi_to_note(max(sounded))))
    print("  motion     %d up, %d down" % (ups, downs))
    hook = [librosa.midi_to_note(n) for n in sounded[:16]]
    print("  first 16   %s" % " ".join(hook))

    if "--write" in sys.argv:
        slot = sys.argv[sys.argv.index("--write") + 1]
        dst = os.path.join(GBA, "sound/songs/midi/%s.mid" % slot)
        if not os.path.isfile(dst):
            sys.exit("  !! no slot called %s" % slot)
        parts = [(TRUMPET,      100, mel),
                 (GLOCKENSPIEL,  52, merge(octave_up(mel_cells))),
                 (STRINGS,        70, mid),
                 (BASS,           96, bass),
                 (TIMPANI,        88, downbeats(bass_cells))]
        open(dst, "wb").write(midi_bytes(tempo, parts))
        print("  written    sound/songs/midi/%s.mid" % slot)
        for program, vel, notes in parts:
            print("             VOICE %-3d  %d events, velocity %d"
                  % (program, sum(1 for n, _ in notes if n is not None), vel))

main()
