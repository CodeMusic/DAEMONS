#!/usr/bin/env python3
"""The groves' music (T-408 part 3): fourteen loops from the user's own recordings, each on its universe's own band --
and CALLOW's theme (T-05), a fifteenth loop made the same way, on a town's band.

    python3 tools/gengrovemusic.py                     # report: transcribe all fourteen, sizes, voices, slots
    python3 tools/gengrovemusic.py --out DIR           # also write the fourteen MIDIs to DIR (mus_grove_<x>.mid)
    python3 tools/gengrovemusic.py --out DIR --render  # and render each to audio, plus "Grove arrangements.mp3"
    python3 tools/gengrovemusic.py --write             # into engineGba: the MIDIs, four slot lines each, the maps
    python3 tools/gengrovemusic.py BACKDROP HUSH ...   # just those universes (or CALLOW)

DECIDED BY THE USER, 2026-10-17 (docs/TODO.md T-408; the mapping and its reasons are in the private draft
docs/private/draft-grove-music-2026-10-17.md, the sources in docs/private/audio/ -- neither is in git, so on a fresh
clone this tool reports that and writes nothing):

  * six new songs, two groves each; HUNGER borrows 9 / Forgiveness Offered (79.25-101.84) and CLAY Harmony in
    Balance (49.95-70.89), both from sections with no PLAY motif;
  * each loop exactly the window drafted (GROVES below), transcribed with mp3midi's own functions: melody (pyin over
    250 Hz), bass (pyin under 300 Hz), and a chord per half bar (the diatonic triad whose template best fits the
    chroma), everything snapped to the window's key;
  * each universe its own band of real instruments on voicegroup191 -- no new samples -- so two groves sharing a song
    sound different;
  * a new MUS_GROVE_<X> slot each (engine.md trap 25: the parents' slots are shared, never written over);
  * written at half speed where the song reads double time (BPM below over 130), so the grid holds eighths, not
    sixteenths, and the song stays small. The loop is a whole number of bars and the MIDI's tempo is set so that it
    lasts as long as the window, to the nearest even BPM (mid2agb stores TEMPO as BPM/2 in a byte): the game's
    loop is the recording's bars, a fraction of a percent faster or slower.

THE HARDWARE'S LIMIT IS FIVE. src/m4a.c starts the mixer with 5 DirectSound channels (SOUND_MODE_MAXCHN), and every
voice in voicegroup191 is DirectSound. A sixth simultaneous note steals one, so every band below is written to sound
at most five notes at once (the report counts it; --render models the stealing).

voicegroup191, read from sound/voice_groups.inc (gbavoices.py made it General MIDI; every other slot is the piano):
  0 piano  9 glockenspiel  13 xylophone  14 tubular bell  24 nylon guitar  33 fingered bass  38 synth bass
  45 pizzicato  46 harp  47 timpani  48 strings  52 choir  56 trumpet  58 tuba  60 french horn  68 oboe  73 flute
  78 whistle

THE BANDS, and why (the user's draft table, T-408 section 5, made playable in five channels):

  BACKDROP  strings (3-note pad), harp arpeggio, nylon guitar lead. The painted set behind everything: the song has
            almost no lead line (13% above the accompaniment), so the strings hold the picture and the harp moves
            inside it; the guitar takes what melody there is, softly, like something seen at the edge.
  PULSE     xylophone lead, pizzicato off-beat stabs (2), fingered bass, timpani on every beat. The first road: the
            beat is the point, so the drum is on all four and the strings bounce between.
  INWARD    flute lead, harp arpeggio, fingered bass, a soft string dyad. Looking in: one breath (the flute) over
            a slow inner turning (the harp).
  EMPATH    oboe lead, choir (3-note pad), fingered bass. The emotional universe, the most colour: human voices
            are the colour, and the oboe is the most vocal of the reeds.
  DRIFT     strings (3-note pad, one chord a BAR), harp carrying the melody, fingered bass held. Resting: the
            harmony moves half as often as BACKDROP's from the same song, and nothing strikes.
  HAZE      piano lead, low choir dyad, fingered bass, a tubular bell every second bar. Fading: the only piano in the
            groves (an ordinary sound, half there) under a far bell.
  HUSH      flute lead (soft), harp arpeggio, a very soft string dyad. NO BASS: before the sound comes, nothing
            is underneath.
  SEED      glockenspiel lead, pizzicato arpeggio, pizzicato bass on the beat, a soft string dyad. Something
            starting: small bright points, the same song as PULSE with the drum taken away.
  WEATHER   french horn lead, strings (3-note pad), timpani rolls into every fourth bar. The sky breaking: the
            loudest section of its song, scored like weather.
  HUNGER    oboe lead, pizzicato arpeggio, tuba bass, a string dyad. Appetite: the tuba is the stomach of the
            band, the pizzicato its picking.
  HUSK      nylon guitar lead, guitar arpeggio, fingered bass, a whistle holding the first note of every bar.
            The cold island and the shell left behind: the whistle is the wind through it.
  MECHA     xylophone lead, glockenspiel answering an octave up, synth bass in eighths, pizzicato ostinato.
            Metal and silicon: everything struck, nothing sustained, four parts locked to one clock.
  COMPASS   french horn lead, harp arpeggio, fingered bass, a tubular bell on every downbeat. One direction: the
            bell is the north it keeps returning to. (Shares the horn with WEATHER and nothing else.)
  CLAY      nylon guitar lead, guitar strummed dyads on 1 and 3, tuba bass, timpani on every downbeat. Earth:
            plucked, low and heavy, balanced on one point.

CALLOW (T-05, chosen by the user's ear 2026-10-19 from three candidate loops): The Christmas Cloak of Self,
68.68-96.92 s, 12 bars at 102 BPM, D major (pinned in KEYS: D major, B minor and G major hear alike, 0.83), with no
PLAY motif in it. Its band, SCHOOLBELL, is no grove's: piano lead, glockenspiel answering an octave up, a string dyad,
fingered bass -- a schoolroom's instruments for the town of the school. It is written into MUS_CALLOW (349), the slot
CALLOW already had (the town, its house and every floor of the school play it -- tools/port_music.py's MAP_MUSIC),
over the placeholder transcription of Desperate Shadows; THE BLEED is mus_route1 and is not touched. MUS_CALLOW is
CALLOW's own slot, not a parent's, so trap 25 does not stand in the way.

WHAT IT DOES NOT DO. It cannot hear. The transcription is signal processing (mp3midi.py's docstring says why that
and not a model), so a window whose key is ambiguous (HUSH, COMPASS: E major and E minor read equally) or whose lead
is buried (BACKDROP) comes out weaker, and the report says which. --render is for the user's ear, not a proof.
"""
import json, os, re, shutil, struct, subprocess, sys, tempfile, warnings
warnings.filterwarnings("ignore")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
AUDIO = os.path.join(ROOT, "docs", "private", "audio")
CACHE = os.path.join(os.path.expanduser("~"), ".cache", "daemons", "gengrovemusic")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

WRITE = "--write" in sys.argv
RENDER = "--render" in sys.argv
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None

TPQ, DIV = 48, 2                 # MIDI ticks per quarter; grid cells per beat (eighths)
CELL = TPQ // DIV
MAXCHN = 5                       # src/m4a.c: 5 DirectSound channels
CFG = "-E -R50 -G191 -V080"      # midi.cfg, as MUS_NEXUS

#  The songs: file in docs/private/audio/, and the whole song's BPM as measured for the draft (librosa's beat
#  tracker). Over 130 is read as double time and written at half.
SONGS = {
    "MIRROR":   ("2. The Painted Mirror - Through the Painted Mirror.mp3", 136),
    "MAGIC":    ("4. Christmas Magic.mp3", 161),
    "CLOAK":    ("3. The Painted Mirror - The Christmas Cloak of Self.mp3", 103),
    "ENTANGLE": ("3. Entangled Worlds.mp3", 144),
    "BETWEEN":  ("1. The Painted Mirror - Between the Worlds (Painted Reflection).mp3", 161),
    "SOUNDS":   ("4. The Painted Mirror - Where Sounds Come to Light.mp3", 144),
    "NINE":     ("9 - 9’s Love, 9’s Hope, Forgiveness Offered.mp3", 172),
    "HARMONY":  ("6. The Painted Mirror - Harmony in Balance.mp3", 92),
}

#  universe -> (grove map, song, loop start, loop end). The windows are the draft's, to the hundredth.
GROVES = {
    "BACKDROP": ("ViridianForest_Grove",          "MIRROR",    66.99,  95.27),
    "PULSE":    ("Route1_Grove",                  "MAGIC",    108.72, 132.70),
    "INWARD":   ("Route24_Grove",                 "CLOAK",     41.03,  59.86),
    "EMPATH":   ("Route25_Grove",                 "ENTANGLE",  12.65,  33.23),
    "DRIFT":    ("Route11_Grove",                 "MIRROR",    14.40,  35.50),
    "HAZE":     ("Route8_Grove",                  "BETWEEN",   15.39,  33.41),
    "HUSH":     ("Route13_Grove",                 "SOUNDS",    17.41,  44.09),
    "SEED":     ("OneIsland_Grove",               "MAGIC",     20.20,  38.20),
    "WEATHER":  ("TwoIsland_Grove",               "BETWEEN",   79.92, 103.91),
    "HUNGER":   ("ThreeIsland_BerryForest_Grove", "NINE",      79.25, 101.84),
    "HUSK":     ("FourIsland_Grove",              "CLOAK",    151.05, 169.85),
    "MECHA":    ("FiveIsland_Meadow_Grove",       "ENTANGLE",  60.65,  88.10),
    "COMPASS":  ("SixIsland_WaterPath_Grove",     "SOUNDS",   115.77, 135.77),
    "CLAY":     ("SevenIsland_Grove",             "HARMONY",   49.95,  70.89),
}

#  The towns (T-05): name -> (slot, song, loop start, loop end). Their maps are port_music.py's MAP_MUSIC.
TOWNS = {
    "CALLOW":   ("mus_callow",                    "CLOAK",     68.68,  96.92),
}
WINDOWS = dict(list(GROVES.items()) + list(TOWNS.items()))

#  voicegroup191's real instruments (General MIDI numbers, zero-based)
PIANO, GLOCK, XYLO, BELL, GUITAR, BASS, SYNBASS, PIZZ, HARP, TIMP, STRINGS, CHOIR, TRUMPET, TUBA, HORN, OBOE, FLUTE, \
    WHISTLE = 0, 9, 13, 14, 24, 33, 38, 45, 46, 47, 48, 52, 56, 58, 60, 68, 73, 78
REAL = {PIANO, GLOCK, XYLO, BELL, GUITAR, BASS, SYNBASS, PIZZ, HARP, TIMP, STRINGS, CHOIR, TRUMPET, TUBA, HORN, OBOE,
        FLUTE, WHISTLE}

#  A part is (role, program, velocity, (low, high), options). Roles are written by part() below.
BANDS = {
    "BACKDROP": [("pad",   STRINGS, 64, (50, 74), {"n": 3}),
                 ("arp",   HARP,    84, (50, 79), {}),
                 ("lead",  GUITAR,  88, (52, 79), {})],
    "PULSE":    [("lead",  XYLO,    92, (65, 91), {}),
                 ("stabs", PIZZ,    76, (55, 76), {"n": 2}),
                 ("bass",  BASS,    96, (31, 52), {}),
                 ("beats", TIMP,    70, (41, 55), {})],
    "INWARD":   [("lead",  FLUTE,   92, (62, 91), {}),
                 ("arp",   HARP,    80, (50, 79), {}),
                 ("bass",  BASS,    80, (31, 52), {}),
                 ("pad",   STRINGS, 48, (55, 74), {"n": 2})],
    "EMPATH":   [("lead",  OBOE,    96, (60, 86), {}),
                 ("pad",   CHOIR,   70, (52, 76), {"n": 3}),
                 ("bass",  BASS,    88, (31, 52), {})],
    "DRIFT":    [("pad",   STRINGS, 66, (48, 72), {"n": 3, "bar": True}),
                 ("lead",  HARP,    90, (55, 84), {}),
                 ("roots", BASS,    80, (31, 50), {"bar": True})],
    "HAZE":     [("lead",  PIANO,   84, (57, 84), {}),
                 ("pad",   CHOIR,   62, (48, 67), {"n": 2}),
                 ("bass",  BASS,    80, (31, 50), {}),
                 ("bell",  BELL,    60, (60, 76), {"every": 2})],
    "HUSH":     [("lead",  FLUTE,   74, (62, 91), {}),
                 ("arp",   HARP,    70, (50, 79), {}),
                 ("pad",   STRINGS, 40, (55, 74), {"n": 2})],
    "SEED":     [("lead",  GLOCK,   84, (72, 96), {}),
                 ("arp",   PIZZ,    80, (55, 79), {}),
                 ("roots", PIZZ,    86, (36, 52), {}),
                 ("pad",   STRINGS, 44, (55, 74), {"n": 2})],
    "WEATHER":  [("lead",  HORN,    96, (53, 79), {}),
                 ("pad",   STRINGS, 70, (50, 76), {"n": 3}),
                 ("roll",  TIMP,    80, (41, 55), {})],
    "HUNGER":   [("lead",  OBOE,    92, (60, 86), {}),
                 ("arp",   PIZZ,    78, (55, 79), {}),
                 ("bass",  TUBA,    92, (33, 55), {}),
                 ("pad",   STRINGS, 50, (55, 74), {"n": 2})],
    "HUSK":     [("lead",  GUITAR,  92, (52, 79), {}),
                 ("arp",   GUITAR,  66, (45, 69), {}),
                 ("bass",  BASS,    80, (31, 50), {}),
                 ("held",  WHISTLE, 46, (72, 91), {})],
    "MECHA":    [("lead",  XYLO,    94, (65, 91), {}),
                 ("answer", GLOCK,  66, (72, 96), {}),
                 ("eighths", SYNBASS, 88, (31, 50), {}),
                 ("ostinato", PIZZ, 76, (48, 72), {})],
    "COMPASS":  [("lead",  HORN,    92, (53, 79), {}),
                 ("arp",   HARP,    78, (50, 79), {}),
                 ("bass",  BASS,    84, (31, 52), {}),
                 ("bell",  BELL,    62, (60, 76), {"every": 1})],
    "CLAY":     [("lead",  GUITAR,  92, (52, 79), {}),
                 ("strum", GUITAR,  70, (48, 67), {"n": 2}),
                 ("bass",  TUBA,    92, (33, 55), {}),
                 ("down",  TIMP,    78, (41, 55), {})],
    #  SCHOOLBELL, CALLOW's (T-05): the schoolroom's piano, the bell answering it, strings and a walking bass
    "CALLOW":   [("lead",  PIANO,   88, (60, 84), {}),
                 ("answer", GLOCK,  60, (72, 96), {}),
                 ("pad",   STRINGS, 52, (55, 74), {"n": 2}),
                 ("bass",  BASS,    86, (31, 52), {})],
}

NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


# ---------------------------------------------------------------- the transcription (mp3midi's functions)

def grid_of(song, t0, t1):
    """(beats, bpm, half): a whole number of bars that lasts exactly t1 - t0."""
    bpm = SONGS[song][1]
    half = bpm > 130
    if half:
        bpm /= 2.0
    beats = max(4, int(round((t1 - t0) * bpm / 60.0 / 4.0)) * 4)
    #  mid2agb writes TEMPO as bpm/2 in a byte, so the game plays only even tempos: write the one it will play
    return beats, 2 * round(beats * 60.0 / (t1 - t0) / 2), half


def chords_of(segs, root, mode):
    """One diatonic triad per segment (segs: a 12-bin chroma mean each): the template that best fits.
    Returns (root pc, "M" or "m") per segment."""
    import numpy as np
    if mode == "major":
        cands = [(0, "M"), (2, "m"), (4, "m"), (5, "M"), (7, "M"), (9, "m")]
    else:
        cands = [(0, "m"), (3, "M"), (5, "m"), (7, "m"), (7, "M"), (8, "M"), (10, "M")]
    temps = []
    for deg, q in cands:
        r = (root + deg) % 12
        t = np.full(12, -0.15)
        t[r] = 1.0; t[(r + (4 if q == "M" else 3)) % 12] = 0.75; t[(r + 7) % 12] = 0.75
        temps.append(((r, q), t))
    out, prev = [], None
    for col in segs:
        col = np.array(col)
        col = col / (col.max() or 1)
        scores = sorted(((float(col @ t), c) for c, t in temps), reverse=True)
        best = scores[0][1]
        #  hysteresis: keep the chord already sounding unless the new one is clearly better
        if prev is not None:
            sp = next(s for s, c in scores if c == prev)
            if scores[0][0] - sp < 0.08:
                best = prev
        out.append(best); prev = best
    return out


def analyse(universe):
    """Listen to one window: the beat grid, the two pitch tracks per cell, the chroma per half bar and per bar, and
    the key candidates. Cached on disk, outside both repos (~/.cache/daemons/gengrovemusic), by source and window,
    so the report stays inside check_generators' time limit."""
    import numpy as np, librosa, mp3midi
    grove, song, t0, t1 = WINDOWS[universe]
    src = os.path.join(AUDIO, SONGS[song][0])
    key = "v6|%s|%s|%.2f|%.2f|%d" % (os.path.basename(src), os.path.getmtime(src), t0, t1, os.path.getsize(src))
    cpath = os.path.join(CACHE, "%s.json" % universe)
    if os.path.exists(cpath):
        c = json.load(open(cpath))
        if c.get("key") == key:
            return c
    beats, bpm, half = grid_of(song, t0, t1)
    sr = 22050
    y, _ = librosa.load(src, sr=sr, mono=True, offset=t0, duration=t1 - t0)
    h = librosa.effects.harmonic(y)
    chroma = librosa.feature.chroma_cqt(y=h, sr=sr, hop_length=mp3midi.HOP)
    prof = chroma.mean(axis=1)
    cands = []
    for i in range(12):
        r = np.roll(prof, -i)
        cands.append((float(np.corrcoef(r, mp3midi.MAJOR)[0, 1]), NAMES[i], "major"))
        cands.append((float(np.corrcoef(r, mp3midi.MINOR)[0, 1]), NAMES[i], "minor"))
    cands.sort(reverse=True)
    n_frames = chroma.shape[1]
    ncell = beats * DIV
    grid = [int(round(i * n_frames / ncell)) for i in range(ncell + 1)]
    seg = lambda step: [chroma[:, grid[i]:max(grid[i + step], grid[i] + 1)].mean(axis=1).tolist()
                        for i in range(0, ncell, step)]
    c = {"key": key, "universe": universe, "beats": beats, "bpm": bpm, "half": half, "cands": cands[:3],
         "mel_raw": mp3midi.cells_of(mp3midi.track(h, sr, 'C3', 'C7', "high"), grid),
         "bass_raw": mp3midi.cells_of(mp3midi.track(h, sr, 'C1', 'C4', "low"), grid),
         "seg2": seg(DIV * 2), "seg4": seg(DIV * 4)}
    os.makedirs(CACHE, exist_ok=True)
    json.dump(c, open(cpath, "w"))
    return c


def in_key(a, tonic, mode):
    """The window heard in one key: both lines snapped to its scale (mp3midi's rule: the nearest degree, a
    semitone before a tone), and the chords chosen from its triads."""
    root = NAMES.index(tonic)
    degrees = [0, 2, 4, 5, 7, 9, 11] if mode == "major" else [0, 2, 3, 5, 7, 8, 10]
    scale = {(root + d) % 12 for d in degrees}

    def snap(cells):
        moved, out = 0, []
        for n in cells:
            if n is None or n % 12 in scale:
                out.append(n); continue
            moved += 1
            out.append(min((abs(c), n + c) for c in (-1, 1, -2, 2) if (n + c) % 12 in scale)[1])
        return out, moved
    t = dict(a)
    t["mel"], t["m_moved"] = snap(a["mel_raw"])
    t["bass"], t["b_moved"] = snap(a["bass_raw"])
    t["chords2"], t["chords4"] = chords_of(a["seg2"], root, mode), chords_of(a["seg4"], root, mode)
    t["tonic"], t["mode"] = tonic, mode
    t["kcorr"] = next((k for k, n, m in a["cands"] if (n, m) == (tonic, mode)), float("nan"))
    return t


#  The user's ear overrides the arithmetic: universe -> (tonic, mode). Empty until the user has listened.
KEYS = {"CALLOW": ("D", "major")}       # the user chose candidate 1 in D major (2026-10-19)


# ---------------------------------------------------------------- the arrangement

def clean(cells):
    """A pitch track is noisier than a line. Single-cell blips between two equal notes take their neighbours' pitch;
    a single voiced cell between rests is dropped; an octave slip (a leap over a ninth that comes straight back)
    is folded back."""
    c = list(cells)
    for i in range(1, len(c) - 1):
        a, x, b = c[i - 1], c[i], c[i + 1]
        if x is not None and a is not None and a == b and x != a:
            c[i] = a
        elif x is not None and a is None and b is None:
            c[i] = None
    prev = None
    for i, x in enumerate(c):
        if x is None:
            continue
        if prev is not None:
            while x - prev > 9:
                x -= 12
            while prev - x > 9:
                x += 12
        c[i] = x; prev = x
    return c


def fit(notes, lo, hi):
    """Shift a line by whole octaves so its middle sits in the instrument's range, then fold what still falls out."""
    sounded = sorted(n for n in notes if n is not None)
    if not sounded:
        return notes
    mid = sounded[len(sounded) // 2]
    shift = 12 * round(((lo + hi) / 2 - mid) / 12)
    out = []
    for n in notes:
        if n is None:
            out.append(None); continue
        n += shift
        while n < lo:
            n += 12
        while n > hi:
            n -= 12
        out.append(n)
    return out


def triad(chord, lo, hi, n):
    """The chord's tones in close position from the lowest root at or above lo; n of them (1-3)."""
    r, q = chord
    base = lo + ((r - lo) % 12)
    tones = [base, base + (4 if q == "M" else 3), base + 7]
    if tones[-1] > hi:
        tones = [t - 12 for t in tones]
    if n == 2:
        tones = tones[1:]                    # third and fifth: the root is the bass's
    return tones[:n] if n < 3 else tones


def root_in(chord, lo, hi):
    n = lo + ((chord[0] - lo) % 12)
    return n if n <= hi else n - 12


def part(role, rng, opts, a):
    """Events (start cell, length in cells, [notes]) for one role, over the whole loop."""
    lo, hi = rng
    ncell = a["beats"] * DIV
    bar, hb = DIV * 4, DIV * 2
    ch2 = [tuple(c) for c in a["chords2"]]
    ch4 = [tuple(c) for c in a["chords4"]]
    chord_at = lambda cell: ch2[min(cell // hb, len(ch2) - 1)]
    ev = []
    if role in ("lead", "answer"):
        mel = fit(clean(a["mel"]), lo, hi)
        if role == "answer":                 # an octave up, only where the lead has just moved, on the off-beats
            mel = [n if (n is not None and i % 2 == 1 and i and mel[i - 1] != n) else None for i, n in enumerate(mel)]
        i = 0
        while i < ncell:
            n = mel[i]
            j = i + 1
            while j < ncell and mel[j] == n and n is not None and (j - i) < bar:
                j += 1
            if n is not None:
                ev.append((i, j - i, [n]))
            i = j
    elif role == "held":                     # the lead's first note of each bar, held the bar
        mel = fit(clean(a["mel"]), lo, hi)
        for s in range(0, ncell, bar):
            n = next((x for x in mel[s:s + bar] if x is not None), None)
            if n is not None:
                ev.append((s, bar, [n]))
    elif role == "pad":
        n = opts.get("n", 3)
        if opts.get("bar"):
            for k, c in enumerate(ch4):
                ev.append((k * bar, bar, triad(c, lo, hi, n)))
        else:
            k = 0
            while k < len(ch2):
                j = k
                while j + 1 < len(ch2) and ch2[j + 1] == ch2[k] and (j + 1 - k) < 4:
                    j += 1
                ev.append((k * hb, (j - k + 1) * hb, triad(ch2[k], lo, hi, n)))
                k = j + 1
    elif role == "arp":                      # up and back down the chord, an eighth each
        for s in range(0, ncell, hb):
            t = triad(chord_at(s), lo, hi, 3)
            pat = [t[0], t[1], t[2], t[0] + 12]
            for k in range(hb):
                ev.append((s + k, 1, [pat[k % 4]]))
    elif role == "stabs":                    # the off-beats
        for s in range(0, ncell, DIV):
            ev.append((s + 1, 1, triad(chord_at(s), lo, hi, opts.get("n", 2))))
    elif role == "strum":                    # beats 1 and 3, a half bar ringing
        for s in range(0, ncell, hb):
            ev.append((s, hb, triad(chord_at(s), lo, hi, opts.get("n", 2))))
    elif role == "bass":                     # the bass line heard, its gaps filled with the chord's root
        b = a["bass"]
        cells = []
        for i in range(ncell):
            n = b[i] if i < len(b) else None
            cells.append(n if n is not None else (root_in(chord_at(i), lo, hi) + 24))
        cells = fit(clean(cells), lo, hi)
        i = 0
        while i < ncell:
            j = i + 1
            while j < ncell and cells[j] == cells[i] and (j - i) < hb:
                j += 1
            ev.append((i, j - i, [cells[i]]))
            i = j
    elif role == "roots":                    # the chord's root on every beat (or held a bar)
        if opts.get("bar"):
            for k, c in enumerate(ch4):
                ev.append((k * bar, bar, [root_in(c, lo, hi)]))
        else:
            for s in range(0, ncell, DIV):
                ev.append((s, 1, [root_in(chord_at(s), lo, hi)]))
    elif role == "eighths":                  # root on every eighth, the octave on the off-beats
        for s in range(ncell):
            r = root_in(chord_at(s), lo, hi)
            ev.append((s, 1, [r + 12 if s % 2 and r + 12 <= hi + 12 else r]))
    elif role == "ostinato":                 # root, fifth, octave, fifth
        for s in range(ncell):
            r = root_in(chord_at(s), lo, hi)
            ev.append((s, 1, [(r, r + 7, r + 12, r + 7)[s % 4]]))
    elif role in ("beats", "down", "roll"):
        step = DIV if role == "beats" else bar
        for s in range(0, ncell, step):
            ev.append((s, 1, [root_in(chord_at(s), lo, hi)]))
        if role == "roll":                   # into every fourth bar: the last beat in eighths, rising to the fifth
            for b0 in range(bar * 4 - DIV * 2, ncell, bar * 4):
                r = root_in(chord_at(b0), lo, hi)
                for k in range(DIV * 2):
                    ev.append((b0 + k, 1, [r if k < DIV * 2 - 1 else min(hi, r + 7)]))
    elif role == "bell":
        every = opts.get("every", 2)
        for s in range(0, ncell, bar * every):
            ev.append((s, bar * every, [root_in(chord_at(s), lo, hi)]))
    else:
        raise ValueError(role)
    #  one note at a time per pitch: drop exact duplicates and clip anything past the loop's end
    seen, out = set(), []
    for s, l, ns in sorted(ev, key=lambda e: e[0]):
        if s >= ncell or (s, tuple(ns)) in seen:
            continue
        seen.add((s, tuple(ns)))
        out.append((s, min(l, ncell - s), [max(0, min(127, x)) for x in ns]))
    return out


def arrange(universe, a):
    tracks = []
    for role, program, vel, rng, opts in BANDS[universe]:
        assert program in REAL, (universe, program)
        tracks.append((program, vel, part(role, rng, opts, a), role))
    return tracks


def polyphony(tracks, ncell):
    load = [0] * ncell
    for _, _, ev, _ in tracks:
        for s, l, ns in ev:
            for c in range(s, s + l):
                load[c] += len(ns)
    return max(load)


# ---------------------------------------------------------------- MIDI

def var(n):
    out = [n & 0x7F]; n >>= 7
    while n:
        out.insert(0, (n & 0x7F) | 0x80); n >>= 7
    return bytes(out)


def chunk(tag, data):
    return tag + struct.pack(">I", len(data)) + data


def midi(tracks, bpm, ncell):
    """Format 1. The tempo track carries the tempo, 4/4 and the loop markers -- mid2agb reads text events from the
    first track only (mp3midi.py) -- and every note track opens with its program change (no square-wave slot 0)."""
    end = ncell * CELL
    head = bytearray(b"\x00\xFF\x51\x03") + struct.pack(">I", int(round(60000000 / bpm)))[1:]
    head += b"\x00\xFF\x58\x04\x04\x02\x18\x08"
    head += b"\x00\xFF\x01\x01[" + var(end) + b"\xFF\x01\x01]" + b"\x00\xFF\x2F\x00"
    out = chunk(b"MThd", struct.pack(">HHH", 1, len(tracks) + 1, TPQ)) + chunk(b"MTrk", bytes(head))
    for ch, (program, vel, ev, _) in enumerate(tracks):
        msgs = []
        for s, l, ns in ev:
            for n in ns:
                msgs.append((s * CELL, 1, n))
                msgs.append(((s + l) * CELL, 0, n))
        msgs.sort(key=lambda m: (m[0], m[1], m[2]))     # offs before ons at the same tick
        data, t = bytearray(b"\x00" + bytes((0xC0 | ch, program))), 0
        for tick, on, n in msgs:
            data += var(tick - t) + bytes(((0x90 if on else 0x80) | ch, n, vel if on else 0))
            t = tick
        data += var(max(0, end - t)) + b"\xFF\x2F\x00"
        out += chunk(b"MTrk", bytes(data))
    return out


def parse_midi(data):
    """The reverse, for --render: (bpm, loop end tick, [(on, off, program, note, vel)]) from what midi() wrote."""
    def rv(p):
        n = 0
        while True:
            b = data[p]; p += 1
            n = (n << 7) | (b & 0x7F)
            if not b & 0x80:
                return n, p
    ntrk, tpq = struct.unpack(">H", data[10:12])[0], struct.unpack(">H", data[12:14])[0]
    p, bpm, loop_end, notes = 14, 120.0, None, []
    for _ in range(ntrk):
        assert data[p:p + 4] == b"MTrk"
        ln = struct.unpack(">I", data[p + 4:p + 8])[0]
        q, e, t, prog, held = p + 8, p + 8 + ln, 0, 0, {}
        while q < e:
            d, q = rv(q); t += d
            st = data[q]
            if st == 0xFF:
                typ = data[q + 1]; ml, q2 = rv(q + 2)
                body = data[q2:q2 + ml]
                if typ == 0x51:
                    bpm = 60000000 / int.from_bytes(body, "big")
                elif typ == 0x01 and body == b"]":
                    loop_end = t
                q = q2 + ml
            elif st & 0xF0 == 0xC0:
                prog = data[q + 1]; q += 2
            elif st & 0xF0 in (0x80, 0x90):
                n, v = data[q + 1], data[q + 2]; q += 3
                if st & 0xF0 == 0x90 and v:
                    held[n] = (t, v)
                elif n in held:
                    on, vv = held.pop(n)
                    notes.append((on * TPQ // tpq, t * TPQ // tpq, prog, n, vv))
            else:
                raise ValueError("unexpected MIDI status %02x" % st)
        p = e
    return bpm, loop_end, notes


def agb_bytes(mid_path):
    """What the song costs in the ROM: mid2agb's output, counted (.byte operands, .word as 4). Run into a temp dir
    from the engine's own built mid2agb; nothing in the engine is written."""
    tool = os.path.join(GBA, "tools", "mid2agb", "mid2agb")
    if not os.path.exists(tool):
        return None
    with tempfile.TemporaryDirectory() as d:
        s = os.path.join(d, os.path.basename(mid_path)[:-4] + ".s")
        r = subprocess.run([tool, mid_path, s] + CFG.split(), capture_output=True, text=True)
        if r.returncode or not os.path.exists(s):
            return None
        n = 0
        for line in open(s):
            line = line.split("@")[0].strip()
            if line.startswith(".byte"):
                n += len([x for x in line[5:].split(",") if x.strip()])
            elif line.startswith(".word"):
                n += 4 * len([x for x in line[5:].split(",") if x.strip()])
        return n


# ---------------------------------------------------------------- --render: the game's own samples, mixed as m4a does

def voicegroup191():
    """program -> (sample path, attack, decay, sustain, release), read from the engine (read only)."""
    vg = open(os.path.join(GBA, "sound", "voice_groups.inc")).read()
    body = vg.split("voicegroup191::", 1)[1].split("voicegroup192::", 1)[0]
    dsd = open(os.path.join(GBA, "sound", "direct_sound_data.inc")).read()
    out = {}
    for prog, line in enumerate(l.strip() for l in body.splitlines() if l.strip().startswith("voice_")):
        m = re.match(r"voice_directsound\s+\d+,\s*\d+,\s*(\w+),\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)", line)
        if not m:
            continue
        bin_ = re.search(r"^%s::\s*\n\s*\.incbin \"([^\"]+)\"" % re.escape(m.group(1)), dsd, re.M)
        out[prog] = (os.path.join(GBA, bin_.group(1)),) + tuple(int(m.group(k)) for k in range(2, 6))
    return out


def load_sample(path):
    import numpy as np
    raw = open(path, "rb").read()
    flags, freq, ls, size = struct.unpack_from("<HIII", raw, 2)
    pcm = np.frombuffer(raw[16:16 + size + 1], dtype=np.int8).astype(np.float32) / 128.0
    return pcm, freq / 1024.0, (ls if flags & 0x4000 else None), size


RATE, FRAME = 13379, 13379 / 59.7275


def render(mid_data, loops=2, voices=None, samples=None):
    """Mix at 13379 Hz, as FireRed's m4aSoundInit sets it: each note's sample resampled by 2^((key-60)/12) from
    its rate at C4 (the header's freq/1024), looped at its loop point, under m4a's per-frame envelope (attack
    added, decay and release multiplied by n/256, sustain a level), at most MAXCHN notes at once -- a new note
    takes a free channel, then one already releasing, then the oldest."""
    import numpy as np
    bpm, loop_end, notes = parse_midi(mid_data)
    sec = 60.0 / bpm / TPQ
    allnotes = []
    for k in range(loops):
        for on, off, prog, n, v in notes:
            allnotes.append(((on + k * loop_end) * sec, (off + k * loop_end) * sec, prog, n, v))
    allnotes.sort()
    total = loops * loop_end * sec + 2.0
    out = np.zeros(int(total * RATE) + 1, dtype=np.float32)
    chans, steals = [], 0                       # [natural end, note-off time, start, index]
    plan = []

    def env_curve(a, d, s, r, hold, cut):
        """Per-frame envelope from note-on: attack/decay/sustain while held, release after; zero after `cut`."""
        e, vals, f, phase = 0, [], 0, "a"
        nhold = int(round(hold * 59.7275))
        while True:
            if f >= nhold and phase != "r":
                phase = "r"
            if phase == "a":
                e += a
                if e >= 255:
                    e = 255; phase = "d"
            elif phase == "d":
                e = (e * d) >> 8
                if e <= s:
                    e = s; phase = "s"
            elif phase == "r":
                e = (e * r) >> 8
            vals.append(e)
            f += 1
            if (phase == "r" and e == 0) or f > nhold + 600 or f / 59.7275 >= cut:
                break
        return np.array(vals, dtype=np.float32) / 255.0

    for idx, (t_on, t_off, prog, n, v) in enumerate(allnotes):
        free = [c for c in chans if c[0] <= t_on]
        for c in free:
            chans.remove(c)
        if len(chans) >= MAXCHN:
            rel = [c for c in chans if c[1] <= t_on]
            victim = min(rel, key=lambda c: c[1]) if rel else min(chans, key=lambda c: c[2])
            chans.remove(victim)
            plan[victim[3]][1] = min(plan[victim[3]][1], t_on)
            steals += victim[1] > t_on          # a note cut while still held; a release tail taken is not counted
        a, d, s, r = voices[prog][1:]
        tail = 0.0 if r == 0 else min(3.0, np.log(1 / 255.0) / np.log(max(r, 1) / 256.0) / 59.7275)
        chans.append([t_off + tail, t_off, t_on, len(plan)])
        plan.append([t_on, t_off + tail, t_off, prog, n, v])
    for t_on, t_cut, t_off, prog, n, v in plan:
        pcm, fr, ls, size = samples[prog]
        a, d, s, r = voices[prog][1:]
        dur = max(0.0, t_cut - t_on)
        env = env_curve(a, d, s, r, t_off - t_on, dur)
        nsamp = min(int(len(env) * FRAME), int(dur * RATE) + 1)
        if nsamp <= 0:
            continue
        step = fr * 2 ** ((n - 60) / 12.0) / RATE
        pos = np.arange(nsamp, dtype=np.float64) * step
        if ls is not None:
            span = size - ls
            pos = np.where(pos >= size, ls + np.mod(pos - ls, span), pos)
        else:
            nsamp = min(nsamp, int(size / step))
            pos = pos[:nsamp]
        if nsamp <= 0:
            continue
        i0 = pos.astype(np.int64); fr_ = (pos - i0).astype(np.float32)
        i1 = np.minimum(i0 + 1, len(pcm) - 1)
        w = pcm[i0] * (1 - fr_) + pcm[i1] * fr_
        e = env[np.minimum((np.arange(nsamp) / FRAME).astype(np.int64), len(env) - 1)]
        st = int(t_on * RATE)
        seg = w * e * (v / 127.0) * (80 / 127.0)
        out[st:st + len(seg)] += seg[:len(out) - st]
    return out, steals


_HEARD = {}


def likeness(u, mix, data):
    """How like the recording the arrangement is, as a number: the mean cosine between the two chromagrams, frame by
    frame, over one loop (1.0 is the same pitch classes at the same moments). It hears harmony, not tone."""
    import numpy as np, librosa
    if u not in _HEARD:
        _, song, t0, t1 = WINDOWS[u]
        y, sr = librosa.load(os.path.join(AUDIO, SONGS[song][0]), sr=22050, mono=True, offset=t0, duration=t1 - t0)
        _HEARD[u] = librosa.feature.chroma_cqt(y=librosa.effects.harmonic(y), sr=22050, hop_length=2048)
    a = _HEARD[u]
    bpm, loop_end, _ = parse_midi(data)
    r = librosa.resample(mix[:int(loop_end * 60.0 / bpm / TPQ * RATE)], orig_sr=RATE, target_sr=22050)
    b = librosa.feature.chroma_cqt(y=r, sr=22050, hop_length=2048)
    n = min(a.shape[1], b.shape[1])
    a, b = a[:, :n], b[:, :n]
    cos = (a * b).sum(0) / (np.linalg.norm(a, axis=0) * np.linalg.norm(b, axis=0) + 1e-9)
    return float(cos.mean())


def say(text, path):
    subprocess.run(["say", "-o", path, "--data-format=LEI16@22050", text], check=True)


def render_all(midis, outdir, voices, samples):
    import numpy as np, soundfile as sf, librosa
    sr = 44100
    sil = lambda s: np.zeros(int(s * sr), dtype=np.float32)
    whole, notes = [sil(0.5)], []
    loopdir = os.path.join(outdir, "loops")
    os.makedirs(loopdir, exist_ok=True)
    for u, data in midis:
        mix, steals = render(data, loops=2, voices=voices, samples=samples)
        peak = float(np.abs(mix).max()) or 1.0
        mix = librosa.resample(mix / peak * 0.85, orig_sr=RATE, target_sr=sr)
        sf.write(os.path.join(loopdir, "%s.wav" % u), mix, sr)
        with tempfile.TemporaryDirectory() as d:
            wav = os.path.join(d, "name.wav")
            say(("%s." if u in TOWNS else "The %sverse.") % u.capitalize(), wav)
            voice, vsr = sf.read(wav, dtype="float32")
            voice = librosa.resample(voice, orig_sr=vsr, target_sr=sr) * 0.8
        whole += [voice, sil(0.6), mix, sil(1.2)]
        notes.append((u, steals))
    wav = os.path.join(outdir, "Grove arrangements.wav")
    sf.write(wav, np.concatenate(whole), sr)
    mp3 = os.path.join(outdir, "Grove arrangements.mp3")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-codec:a", "libmp3lame", "-q:a", "3", mp3],
                   check=True)
    os.remove(wav)
    return mp3, notes


# ---------------------------------------------------------------- --write: the engine

def slot(u):
    return TOWNS[u][0] if u in TOWNS else "mus_grove_%s" % u.lower()


def write_engine(midis):
    """The MIDIs and, per trap 25, the four lines each -- appended, never inserted -- and each grove's music."""
    songs_h = os.path.join(GBA, "include/constants/songs.h")
    table = os.path.join(GBA, "sound/song_table.inc")
    cfg = os.path.join(GBA, "sound/songs/midi/midi.cfg")
    ld = os.path.join(GBA, "ld_script.ld")
    h, t, c, l = (open(p).read() for p in (songs_h, table, cfg, ld))
    defs = [(m.group(1), int(m.group(2))) for m in re.finditer(r"^#define\s+((?:MUS|SE)_\w+)\s+(\d+)\b", h, re.M)]
    last = max(n for _, n in defs)
    rows = re.findall(r"^\tsong \w+, \d+, \d+$", t, re.M)
    if len(rows) != last + 1:
        sys.exit("  !! song_table.inc has %d rows and songs.h ends at %d: the table is positional, so stop" %
                 (len(rows), last))
    changed = []
    for u, data in midis:
        s, const = slot(u), slot(u).upper()
        open(os.path.join(GBA, "sound/songs/midi/%s.mid" % s), "wb").write(data)
        if not re.search(r"^#define\s+%s\b" % const, h, re.M):
            last += 1
            line = "#define %-25s %d" % (const, last) + ("   // T-408: the groves' music (tools/gengrovemusic.py)"
                                                          if u == list(GROVES)[0] else "")
            m = list(re.finditer(r"^#define\s+(?:MUS|SE)_\w+\s+\d+\b.*$", h, re.M))[-1]
            h = h[:m.end()] + "\n" + line + h[m.end():]
            m = list(re.finditer(r"^\tsong \w+, \d+, \d+$", t, re.M))[-1]
            t = t[:m.end()] + "\n\tsong %s, 0, 0" % s + t[m.end():]
            changed.append(const)
        if re.search(r"^%s\.mid:" % s, c, re.M):        # a town's slot already exists: its bank becomes ours
            c = re.sub(r"^(%s\.mid:\s*).*$" % s, lambda m: m.group(1) + CFG, c, count=1, flags=re.M)
        else:
            m = list(re.finditer(r"^(?:mus_nexus|mus_grove_\w+)\.mid:.*$", c, re.M))[-1]
            c = c[:m.end()] + "\n%-31s%s" % (s + ".mid:", CFG) + c[m.end():]
        if "sound/songs/midi/%s.o(.rodata);" % s not in l:
            m = list(re.finditer(r"^(\s*)sound/songs/midi/\w+\.o\(\.rodata\);$", l, re.M))[-1]
            l = l[:m.end()] + "\n%ssound/songs/midi/%s.o(.rodata);" % (m.group(1), s) + l[m.end():]
        if u in TOWNS:                       # a town's maps are port_music.py's
            continue
        mj = os.path.join(GBA, "data/maps/%s/map.json" % GROVES[u][0])
        raw = open(mj).read()
        new = re.sub(r'"music": "[A-Z0-9_]+"', '"music": "%s"' % const, raw, count=1)
        if new != raw:
            open(mj, "w").write(new)
            changed.append("%s music" % GROVES[u][0])
    for p, s in ((songs_h, h), (table, t), (cfg, c), (ld, l)):
        if open(p).read() != s:
            open(p, "w").write(s)
    return changed


# ---------------------------------------------------------------- main

def main():
    only = [a.upper() for a in sys.argv[1:] if a.upper() in WINDOWS]
    if OUT:
        only = [a for a in only if a != os.path.basename(OUT).upper()]
    todo = only or list(WINDOWS)
    missing = sorted({SONGS[WINDOWS[u][1]][0] for u in todo if not os.path.exists(os.path.join(AUDIO, SONGS[WINDOWS[u][1]][0]))})
    if missing:
        print("  the sources are private (docs/private/audio/) and %d are not here: %s" % (len(missing), "; ".join(missing)))
        print("  nothing transcribed; nothing written")
        return 0
    if OUT:
        os.makedirs(OUT, exist_ok=True)
    print("  %-9s %-9s %6s %5s %-9s %5s %5s %5s %5s %6s %6s %4s  %s" % ("universe", "song", "secs", "bpm", "key",
          "kcorr", "like", "snap%", "mel%", "MIDI", "agb", "poly", "band"))
    midis, total_mid, total_agb, likes = [], 0, 0, {}
    voices = voicegroup191()
    samples = {p: load_sample(v[0]) for p, v in voices.items()}
    for u in todo:
        raw = analyse(u)
        ncell = raw["beats"] * DIV
        #  THE KEY IS CHOSEN BY LISTENING BACK, not by the profile alone: the three best-correlated keys are each
        #  arranged, rendered and compared with the recording (likeness()), and the closest kept -- unless the
        #  user's ear has said (KEYS). A window that reads two keys equally (HUSH, COMPASS) is where this matters.
        tried = []
        for tonic, mode in ([KEYS[u]] if u in KEYS else [(n, m) for _, n, m in raw["cands"]]):
            a = in_key(raw, tonic, mode)
            tracks = arrange(u, a)
            data = midi(tracks, a["bpm"], ncell)
            mix, _ = render(data, loops=1, voices=voices, samples=samples)
            tried.append((likeness(u, mix, data), a, tracks, data))
        #  relative keys share a scale and often tie: within 0.01 of the best, the key the profile favours wins
        top = max(t[0] for t in tried)
        like, a, tracks, data = max((t for t in tried if t[0] >= top - 0.01), key=lambda x: x[1]["kcorr"])
        likes[u] = (like, ["%s %s %.2f" % (t[1]["tonic"], t[1]["mode"][:3], t[0]) for t in tried])
        midis.append((u, data))
        voiced = sum(1 for n in a["mel"] if n is not None)
        poly = polyphony(tracks, ncell)
        assert poly <= MAXCHN, "%s sounds %d notes at once; the mixer has %d" % (u, poly, MAXCHN)
        agb = None
        if OUT:
            path = os.path.join(OUT, "%s.mid" % slot(u))
            open(path, "wb").write(data)
            agb = agb_bytes(path)
        else:
            with tempfile.TemporaryDirectory() as d:
                path = os.path.join(d, "%s.mid" % slot(u))
                open(path, "wb").write(data)
                agb = agb_bytes(path)
        total_mid += len(data); total_agb += agb or 0
        _, song, t0, t1 = WINDOWS[u]
        band = ", ".join("%s %s" % (r, p) for r, p, _, _, _ in BANDS[u])
        print("  %-9s %-9s %6.2f %5.1f %-9s %5.2f %5.2f %5d %5d %6d %6s %4d  %s%s" % (
            u, song, t1 - t0, a["bpm"], "%s %s" % (a["tonic"], a["mode"][:3]), a["kcorr"], likes[u][0],
            100 * a["m_moved"] // max(1, voiced), 100 * voiced // max(1, len(a["mel"])), len(data),
            agb if agb is not None else "?", poly, band, " (half)" if a["half"] else ""))
    print("  total: %d bytes of MIDI, about %d bytes in the ROM (mid2agb's output, counted)" % (total_mid, total_agb))
    print("  like: chroma likeness to the recording, 1.0 the same; two unrelated windows score 0.47-0.70 (0.70 when")
    print("  both are in D), so under about 0.75 the transcription is little nearer the song than chance. Keys tried:")
    for u in todo:
        print("    %-9s %s" % (u, "; ".join(likes[u][1])))
    if RENDER:
        if not OUT:
            sys.exit("  !! --render needs --out DIR")
        mp3, notes = render_all(midis, OUT, voices, samples)
        print("  rendered: %s" % mp3)
        cut = ", ".join("%s %d" % (u, n) for u, n in notes if n)
        print("  held notes cut by the 5-channel limit: %s" % (cut or "none"))
    if WRITE:
        ch = write_engine(midis)
        print("  written: %d MIDIs; %s" % (len(midis), "; ".join(ch) if ch else "every slot and map already current"))
    else:
        h = open(os.path.join(GBA, "include/constants/songs.h")).read() if os.path.isdir(GBA) else ""
        have = [u for u in todo if re.search(r"^#define\s+%s\b" % slot(u).upper(), h, re.M)]
        mids = dict(midis)
        stale = [u for u in have if (open(os.path.join(GBA, "sound/songs/midi/%s.mid" % slot(u)), "rb").read()
                                     if os.path.exists(os.path.join(GBA, "sound/songs/midi/%s.mid" % slot(u)))
                                     else None) != mids[u]]
        print("  engine: %d of %d slots exist, %d of them holding another MIDI (%s); --write would add the rest (four "
              "lines each), write the MIDIs and point the groves' maps at them" %
              (len(have), len(todo), len(stale), ", ".join(stale) or "none"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
