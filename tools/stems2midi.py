#!/usr/bin/env python3
"""Build the title theme from a separated stem set.

    ./bpvenv/bin/python tools/bpextract.py "<dir>/1 Bass.mp3" notes/bass.json 30 400
    python3 tools/stems2midi.py <dir> --notes notes --write mus_title
    python3 tools/stems2midi.py <dir> --notes notes --split other --write mus_intro

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
import importlib.util, json, os, re, sys, warnings
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
GLOCK = 9        # the intro theme's lead, once it is split out of "other"

#  the word in a stem's filename -> (label, program, velocity, chord voice)
#
#  KEYED ON THE WORD, NOT THE NUMBER. Suno numbers stems by track order and
#  that order differs per song: the title theme's synth arrived as "5 Synth"
#  and the intro's as "2 Synth". A table of literal filenames matched the one
#  song it was written for and silently skipped every stem of the next.
ROLES = {
    "brass":      ("brass",   TRUMPET, 100, "high"),
    #  the synth stem was the busiest line in the title theme -- 233 of 400
    #  cells -- which is an arpeggio, and an arpeggio is what a harp is for. A
    #  glockenspiel across that many cells at 152 BPM is a smoke alarm.
    "synth":      ("synth",   HARP,     64, "high"),
    "strings":    ("strings", STRINGS,  78, "high"),
    "keyboard":   ("keys",    PIANO,    58, "high"),
    "piano":      ("keys",    PIANO,    58, "high"),
    "bass":       ("bass",    BASS,     96, "low"),
    #  "Other" is the separator's remainder, not an instrument. It is taken as
    #  a keyboard part because that is the safest thing an unknown mid-register
    #  line can be -- but see the warning main() prints when it dominates.
    "other":      ("other",   PIANO,    70, "high"),
    "drums":      None,        # percussion comes from the voicegroup, not here
    "percussion": None,
    "vocals":     None,        # nothing in this game sings
}

#  loudest first: which line survives when the GBA runs out of tracks
ORDER = ["brass", "synth", "strings", "keys", "other", "bass"]

def stems_in(d):
    """Discover the stem set from the directory. Returns the STEMS list the
    rest of this tool expects, ordered as ORDER, with unknown words reported
    rather than dropped -- a stem this table has never seen is a thing to look
    at, not a thing to skip quietly."""
    found, unknown = {}, []
    for f in sorted(os.listdir(d)):
        stem, ext = os.path.splitext(f)
        if ext.lower() not in (".mp3", ".wav", ".flac") or f.startswith("."):
            continue
        word = re.sub(r"^[\d\s_-]+", "", stem).strip().lower()
        if word not in ROLES:
            unknown.append(stem); continue
        if ROLES[word] is None:
            continue
        found[stem] = ROLES[word]
    for u in unknown:
        print("  %-12s -- unrecognised stem, skipped (add it to ROLES)" % u[:12])
    return [(f,) + found[f] for f in
            sorted(found, key=lambda f: ORDER.index(found[f][0]))]

def valley(notes, lo=60, hi=80):
    """Where two voices sharing a stem part company, measured rather than set.

    ONLY FOR A STEM THAT HOLDS TWO INSTRUMENTS. The separator gave the intro
    theme three stems -- drums, bass, and everything else -- so the
    glockenspiel and the electric piano arrived in one file, and one file is
    one line as far as cells_from is concerned.

    Splitting a mix by pitch is exactly the guess this tool was written to
    stop making, so it is not done quietly and it is not done on faith: the
    histogram has to actually show two modes. The cut is the emptiest bin
    between them, and if that bin is not meaningfully emptier than the peaks
    on either side there are no two voices to separate and this returns None.
    Anything it does split is INFERRED, and main() says so in its output."""
    p = np.array([n[2] for n in notes])
    h = np.array([((p >= x) & (p < x + 3)).sum() for x in range(lo, hi, 3)])
    if len(h) < 3:
        return None
    i = int(np.argmin(h[1:-1])) + 1
    left, right = h[:i].max(), h[i + 1:].max()
    if h[i] > 0.75 * min(left, right):        # a dip, not a valley
        return None
    return lo + i * 3 + 1, h[i], min(left, right)


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
    #  Suno names the folder after the song and adds " Stems", so the mix sits
    #  beside it under the bare name. Hardcoding one song's title here was the
    #  same mistake as hardcoding its stem filenames.
    if "--mix" in sys.argv:
        mix_path = os.path.expanduser(sys.argv[sys.argv.index("--mix") + 1])
    else:
        base = os.path.basename(d.rstrip("/"))
        mix_path = os.path.join(os.path.dirname(d.rstrip("/")),
                                re.sub(r"\s*Stems$", "", base) + ".mp3")
    #  NO MIX IS RECOVERABLE, because the mix was only ever two measurements.
    #  Summing the stems reconstructs it well enough for both: a separator's
    #  output adds back up, which is what makes it a separation. Beat tracking
    #  actually prefers this -- it reads a bare percussion stem more cleanly
    #  than a full mix -- while key detection is slightly worse off, so the
    #  tool says which one it used and prints its runner-up either way.
    if not os.path.isfile(mix_path):
        srcs = [os.path.join(d, f) for f in sorted(os.listdir(d))
                if os.path.splitext(f)[1].lower() in (".mp3", ".wav", ".flac")
                and not f.startswith(".")]
        if not srcs:
            sys.exit("no mix at %s and no stems to rebuild one from" % mix_path)
        print("  no mix at %s\n  rebuilding it from %d stems"
              % (os.path.basename(mix_path), len(srcs)))
        acc = None
        for f in srcs:
            y1, sr = librosa.load(f, sr=22050, mono=True)
            acc = y1 if acc is None else (
                np.pad(acc, (0, max(0, len(y1) - len(acc))))
                + np.pad(y1, (0, max(0, len(acc) - len(y1)))))
        mix_path = os.path.join(NOTES, "_rebuilt_mix.wav")
        os.makedirs(NOTES, exist_ok=True)
        import soundfile as sf
        sf.write(mix_path, acc / max(1e-9, np.abs(acc).max()), sr)

    split_words = set()
    if "--split" in sys.argv:
        split_words = {w.strip().lower()
                       for w in sys.argv[sys.argv.index("--split") + 1].split(",")}

    STEMS = stems_in(d)
    if not STEMS:
        sys.exit("no recognised stems in %s" % d)

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

    parts, bass_cells, span = [], None, {}
    for fname, label, program, vel, keep in STEMS:
        #  bpextract is run by hand and gets named either way round: the title
        #  theme's notes landed as "1 Bass.json", the intro's as "bass.json".
        jf = next((c for c in (os.path.join(NOTES, fname + ".json"),
                               os.path.join(NOTES, label + ".json"))
                   if os.path.isfile(c)), None)
        if jf is None:
            print("  %-10s -- no notes file, skipped" % label); continue
        raw = json.load(open(jf))
        if label in split_words:
            v = valley(raw)
            if v is None:
                print("  %-10s -- asked to split, but its histogram shows one\n"
                      "               voice, not two. Left whole." % label)
            else:
                cut, floor, peak = v
                print("  %-10s split at MIDI %d (%d notes there against %d at\n"
                      "               the modes) -- the upper line is INFERRED,\n"
                      "               not heard on its own." % (label, cut, floor, peak))
                lead = [n for n in raw if n[2] >= cut]
                raw = [n for n in raw if n[2] < cut]
                lc = cells_from(lead, grid, times, "high")
                lc, lm = snap(lc, scale)
                sl = [n for n in lc if n is not None]
                print("  %-10s %4d heard, %4d cells, %s..%s, %d snapped"
                      % (label + "-lead", len(lead), len(sl),
                         librosa.midi_to_note(min(sl)), librosa.midi_to_note(max(sl)), lm))
                parts.append((GLOCK, 82, mm.merge(lc)))
                span[label + "-lead"] = (np.percentile(sl, 3), np.percentile(sl, 90), len(sl))
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
        #  the SAME band cells_from works in. Measured with min/max first,
        #  which reported 21 semitones of overlap on an arrangement whose
        #  working registers overlap by 10 -- one stray harmonic at either
        #  end is enough to make two separate parts look like one.
        span[label] = (np.percentile(sounded, 3), np.percentile(sounded, 90),
                       len(sounded))

    #  DOES THIS ARRANGEMENT HAVE PARTS, OR ONE TEXTURE? Asked here because the
    #  intro theme's first take did not, and nothing upstream of this noticed:
    #  its synth stem exported as digital silence and the whole arrangement
    #  collapsed into "other", whose notes spanned MIDI 29..65 -- straight
    #  through the bass's own 28..57. Three lines sharing a register are one
    #  line, and every transcription below this point was wasted on it.
    #  Cheap to check, and it is the difference between a fixable prompt and a
    #  day of tuning extraction thresholds against a track that has no parts.
    if len(span) > 1:
        worst = max(((a, b) for a in span for b in span if a < b),
                    key=lambda ab: min(span[ab[0]][1], span[ab[1]][1])
                                 - max(span[ab[0]][0], span[ab[1]][0]))
        a, b = worst
        overlap = min(span[a][1], span[b][1]) - max(span[a][0], span[b][0])
        if overlap > 12:
            print("  !! %s and %s overlap by %d semitones -- these are not\n"
                  "     separate registers, and the mix will read as one voice."
                  % (a, b, overlap))
    if span:
        big, total = max(span, key=lambda k: span[k][2]), sum(v[2] for v in span.values())
        if span[big][2] > total * 0.6:
            print("  !! %s carries %d%% of all sounded cells -- the separation\n"
                  "     did not work, or the arrangement has only one part."
                  % (big, round(100 * span[big][2] / total)))

    perc = next((f for f in sorted(os.listdir(d))
                 if re.sub(r"^[\d\s_-]+", "", os.path.splitext(f)[0]).strip().lower()
                 in ("drums", "percussion")), None)
    drums = np.zeros(1) if perc is None else librosa.load(
        os.path.join(d, perc), sr=sr, mono=True)[0]
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

if __name__ == "__main__":
    main()
