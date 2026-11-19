#!/usr/bin/env python3
"""T-594: THE SONG -- every daemon's song, drafted (vision 9.36; the user, 2026-11-18). DRAFT, nothing approved.

    python3 tools/gensongs.py                     # report: the keys, the parts, the lengths, a few lines in full
    python3 tools/gensongs.py --previews [DIR]    # an .mp3 sampler: whole lines, one part learned a fifth at a time,
                                                  # three daemons of one type (default audio/drafts/t594_songs)
    python3 tools/gensongs.py --sheets [DIR]      # SONGS.txt and a picture of each line's song in its colours
    python3 tools/gensongs.py --json              # the companion's songs.json on stdout (companion_export.py writes it)

THE USER'S WORDS (2026-11-18): "each daemon should also have its own song (based off the daemons name/type/index
entry/cries ...) ... that is its essence. Daemons in an evolutionary chain should respect that family ... each
evolution builds and continues, that ways you hear the earlier forms by ear in the final forms version. Also, daemons
of the same type should have some similar feel between their songs so u can tell they r related by ear." And, by
multiple choice: SONG is its name (it replaces the cry), a note not yet learned is STATIC CLOSING ON THE NOTE, and "a
daemons type could determine the key for which their song is in" -- 18 types, 24 keys, 6 to spare.

THE SHAPE (one PART a form; a form's SONG is its line's parts so far, oldest first):
    the KEY       its form's first type's key (KEYS): the song modulates when a line changes type as it evolves.
    the OPENING   its cry (tools/gencries.py, T-565 batch 11) in the key: the type's motif turned by the line's first
                  name (every form of a line opens alike), its name's length and letters setting how many notes and
                  their rhythm, a pickup from its initial and an approach from its last letter.
    the WORDS     its INDEX entry (CONTENT's) set syllable by syllable: each word moves the tune a step or two, a long
                  word's first syllable held, a comma a breath; then a cadence home to the key's tonic.
    the BASS      its CONTEXT entry: one chord root a bar (I, IV, V, vi from its words), V then I at the close. The
                  content is the tune and the context is what it is heard over.
    the STAGE     a part a fourth lower than the one before (a stage 3 an octave below its first form) and slower, so a
                  final form's song walks down from its first form's voice to its own.
    the LEARNING  every note has the point (0..1 of its part) where it is learned: the opening first (it already
                  cries), the words in order with a little scatter, the last note at exactly 1 -- perfect. Before its
                  point a note is static, closing on it over the last WINDOW of the way.
    the LEVELS    a part runs from the level its form begins (1, or the level it evolved at) to the level it evolves
                  at: its LEVEL evolution, or NOMINAL levels on for one by a stone, a trade or friendship. A final form
                  matures after as many levels as its form before it took; a daemon with no line at MATURE. The
                  companion and the game read the share learned from its experience between the two (expFor).

THE COLOURS (SYNESTHESIA, companion/server/src/synesthesia.ts): a note is drawn in its pitch's colour -- C red, D
orange, E yellow, F green, G blue, A indigo, B violet, a black key the two colours either side of it -- so a player who
has learned the colours can sit at a piano and play what they see (the user). The key's tonic is its colour too.
"""
import hashlib, json, math, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import genuisounds as gs                                   # PALETTE (read only)

OUT_DIR = os.path.join(ROOT, "audio", "drafts", "t594_songs")

# THE KEYS (T-594, DRAFT -- the key table is the user's to approve): a type's tonic is the note whose colour is
# nearest the type's own (tools/gbasprite.py TYPE_COLOR), its mode its character. CONTENT and CONTEXT are a RELATIVE
# pair -- the same seven notes, another centre -- and C major is every white key with nothing added.
KEYS = {
    "CONTENT":  (0, False, "every white key and nothing added: the undifferentiated"),
    "CONTEXT":  (9, True, "CONTENT's seven notes heard from another centre: its relative minor"),
    "VECTOR":   (1, False, "red into orange: sanguine, the arrow"),
    "ENTROPY":  (3, True, "orange into yellow: choleric, the flicker"),
    "LATENT":   (10, True, "indigo into violet: melancholic, something waking"),
    "FROZEN":   (7, False, "blue: phlegmatic, still and clear"),
    "FLOW":     (8, False, "blue into indigo: deep, moving, running down"),
    "LOGIC":    (7, True, "steel blue: a proof, the key of the fugue"),
    "SWARM":    (4, False, "yellow, olive: many small bright things"),
    "CORRUPT":  (5, True, "green gone off: mould"),
    "STRATUM":  (2, False, "orange-brown, the ground: the key of the open strings"),
    "LEGACY":   (2, True, "the old modes: slate, the cairn"),
    "GROWTH":   (5, False, "green: pastoral"),
    "SIGNAL":   (6, False, "green into blue, a carrier: every sharp lit"),
    "EMERGENT": (6, True, "jade, deeper than SIGNAL's current"),
    "HARDENED": (3, False, "tempered straw: the brass key"),
    "OPAQUE":   (11, True, "violet, the last colour before the light goes off"),
    "ORACLE":   (11, False, "violet into the carry: the one with no record"),
}
SPARE = ["A major", "B-flat major", "C minor", "C-sharp minor", "E minor", "G-sharp minor"]
KEY_NAMES = ["C", "D-flat", "D", "E-flat", "E", "F", "F-sharp", "G", "A-flat", "A", "B-flat", "B"]
MINOR_NAMES = ["C", "C-sharp", "D", "E-flat", "E", "F", "F-sharp", "G", "G-sharp", "A", "B-flat", "B"]
MAJOR, MINOR = [0, 2, 4, 5, 7, 9, 11], [0, 2, 3, 5, 7, 8, 10]

# SYNESTHESIA's seven (companion/server/data/palettes.json, the rainbow week's menu colours), Sunday's C to Saturday's B
NOTE_COLOURS = {0: "#B8443E", 2: "#C9702E", 4: "#CFAE34", 5: "#3F9A55", 7: "#3474B0", 9: "#4D4BAE", 11: "#8A4CAE"}
BINARY_GREEN = "#52F77B"                                   # the error carried back (CONTEXT's aurora line)

LEVELISH = {"LEVEL", "LEVEL_ATK_LT_DEF", "LEVEL_ATK_GT_DEF", "LEVEL_ATK_EQ_DEF", "LEVEL_SILCOON", "LEVEL_CASCOON",
            "LEVEL_NINJASK", "LEVEL_SHEDINJA"}
NOMINAL, MATURE = 20, 40                                   # DRAFT: a stone's, a trade's, friendship's part; no line's
WINDOW = 0.12                                              # static closes on a note over this much of its part
# STATIC's candidates, in steps along the key from the true note, the most agreeing first (thirds, fifths, sixths;
# the seconds last, so they are the first to leave); a hiss under them at most this loud
STATIC, STATIC_FLOOR = [2, -2, 4, -3, 5, -4, 1, -1], 0.35
STAGE_DEG = {1: 0, 2: -3, 3: -7}                           # a fourth lower, an octave lower (scale steps)
BPM = {1: 132, 2: 120, 3: 108, 4: 96, 6: 84}               # the type's palette step, fast to slow
PENTA_DEG = [0, 1, 2, 4, 5, 7, 8, 9, 11, 12]               # the cry's two-octave pentatonic, as scale steps
VOWELS = set("AEIOUY")
LOW, HIGH = 48, 88                                         # a part's notes stay inside C3..E6
MAX_SYLLABLES = 14


def h(s, n):                                               # gencries.h, so a line turns its motif as its cry does
    return int(hashlib.md5(s.encode()).hexdigest(), 16) % n


def pc_colours(pc):
    """A pitch's colours: one for a white key, the two either side for a black key (SYNESTHESIA's blend)."""
    pc %= 12
    return [NOTE_COLOURS[pc]] if pc in NOTE_COLOURS else [NOTE_COLOURS[pc - 1], NOTE_COLOURS[(pc + 1) % 12]]


def key_name(tonic, minor):
    return "%s %s" % ((MINOR_NAMES if minor else KEY_NAMES)[tonic], "minor" if minor else "major")


# ---------------------------------------------------------------------------------------------------------------------
# Degrees: a tune is made in scale steps (7 to the octave, an absolute index, C-1 = 0) and only then made into notes
# ---------------------------------------------------------------------------------------------------------------------
def degree_of(note):
    """'C5' -> (absolute scale step in C, accidental): the palette's motifs are written in C."""
    d = "CDEFGAB".index(note[0])
    return 7 * (int(note[-1]) + 1) + d, (1 if "#" in note else 0)


def realise(step, tonic, minor, acc=0):
    """An absolute scale step in the key -> a MIDI note, the tonic kept near C so the register is the motif's."""
    scale = MINOR if minor else MAJOR
    off = tonic if tonic <= 6 else tonic - 12
    return 12 * (step // 7) + off + scale[step % 7] + acc


def syllables(word):
    w = word.lower()
    groups = re.findall(r"[aeiouy]+", w)
    n = len(groups)
    if n > 1 and w.endswith("e") and not w.endswith(("le", "ee", "ye")):
        n -= 1                                             # a silent final e
    return max(1, n)


# ---------------------------------------------------------------------------------------------------------------------
# The species and their lines, from the engine (companion_export.py's own table: the words the companion carries)
# ---------------------------------------------------------------------------------------------------------------------
def species():
    import companion_export as ce
    return {k: v for k, v in ce.species_table().items() if v.get("name") and v["name"] != "?"}


def lines(sp):
    """{form: parent} and each form's path from its line's first form."""
    parent = {}
    for k, s in sp.items():
        for e in s.get("evolutions") or []:
            parent.setdefault(str(e["target"]), k)
    def path(k):
        p = [k]
        while p[-1] in parent and len(p) < 4:
            p.append(parent[p[-1]])
        return p[::-1]
    return parent, {k: path(k) for k in sp}


def own_end(s, start):
    evs = s.get("evolutions") or []
    lv = [int(e["param"]) for e in evs if e["method"] in LEVELISH and int(e["param"]) > start]
    if lv:
        return min(lv)
    return start + NOMINAL if evs else None


def spans(sp, paths):
    """Each form's part: the level it begins and the level it is perfect at."""
    out = {}
    for k in sorted(sp, key=lambda k: len(paths[k])):     # a form's parent first: it begins where that one ends
        path = paths[k]
        start = min(99, out[path[-2]][1]) if len(path) > 1 else 1
        end = own_end(sp[k], start)
        if end is None:                                    # a final form: as many levels as the form before it took
            end = start + (start - out[path[-2]][0]) if len(path) > 1 else MATURE
        out[k] = (start, min(100, max(end, start + 1)))
    return out


# ---------------------------------------------------------------------------------------------------------------------
# A part
# ---------------------------------------------------------------------------------------------------------------------
def opening(name, line, ty):
    """The cry's notes in scale steps: the motif turned by the line, the name's count, rhythm, pickup and approach."""
    pal = gs.PALETTE[ty]
    m = [degree_of(n) for n in pal["m"]]
    rot = h(line, len(m))
    m = m[rot:] + m[:rot]
    if h(line + "r", 2):
        m = m[::-1]
    letters = [c for c in name.upper() if c.isalpha()] or ["A"]
    count = max(3, min(len(m) + 2, len(letters) // 2 + 2))
    notes = []
    for j in range(count):
        st, acc = m[j % len(m)]
        if j >= len(m) and st < m[-1][0] - 4:
            st += 7
        notes.append([st, acc])
    beats = [1.0 if letters[j % len(letters)] in VOWELS else 0.5 for j in range(count)]
    beats[-1] = 2.0
    first, final = letters[0], letters[-1]
    k0 = notes[0][0]
    pk = 7 * (k0 // 7) + PENTA_DEG[(ord(first) - 65) % 10]
    while pk - k0 > 4:
        pk -= 7
    while k0 - pk > 4:
        pk += 7
    if pk == k0:
        pk -= 2
    ap = notes[-1][0] + (1, -2, -3)[ord(final) % 3]
    notes = [[pk, 0]] + notes[:-1] + [[ap, 0], notes[-1]]
    beats = [0.5] + beats[:-1] + [0.5, beats[-1]]
    return notes, beats


def words_of(text):
    """The first sentence of an entry (and the next, if the first is short), as [(word, breath after it)]."""
    flat = re.sub(r"\s+", " ", text or "").strip()
    sentences = [s.strip() for s in re.findall(r"[^.!?]+[.!?]?", flat) if s.strip()]
    out, count = [], 0
    for s in sentences:
        for raw in s.split():
            w = re.sub(r"[^A-Za-z']", "", raw)
            if not w:
                continue
            n = syllables(w)
            if count + n > MAX_SYLLABLES:
                return out
            out.append((w, raw[-1] in ",;:"))
            count += n
        if count >= 6:
            break
    return out


STEPS = [1, -1, 2, -1, 1, -2, 1, -1, 0]


def melody(words, start, tonic_step):
    """Each syllable a note: a word's first letter and length move the tune; it stays within a sixth below and an
    octave above the part's tonic, and never sits on one note three times."""
    notes, beats, cur, prev = [], [], start, None
    for w, breath in words:
        n = syllables(w)
        step = STEPS[(ord(w[0].upper()) - 65 + len(w)) % len(STEPS)]
        for i in range(n):
            s = step if i == 0 else (1 if step >= 0 else -1) * (1 if i == 1 else -1)
            if cur + s > tonic_step + 7:
                s = -abs(s) or -1
            if cur + s < tonic_step - 3:
                s = abs(s) or 1
            if s == 0 and prev == 0:
                s = 1
            cur += s
            prev = s
            notes.append([cur, 0])
            beats.append((1.0 if i == 0 else 0.5) if n > 1 else (0.5 if len(w) <= 3 else 1.0))
        if breath:
            beats[-1] += 0.5
    return notes, beats


def cadence(cur, tonic_step):
    """Home: the step above or the leading note, then the tonic nearest where the tune is."""
    t = tonic_step + 7 * round((cur - tonic_step) / 7)
    return [[t + 1 if cur >= t else t - 1, 0], [t, 0]], [1.0, 2.0]


def bass(context, total, tonic, minor):
    """One root a bar from the CONTEXT entry: I, IV, V or vi (i, iv, v, VI in minor), the last two V and I."""
    words = [re.sub(r"[^A-Za-z]", "", w) for w in (context or "").split()]
    words = [w for w in words if w] or ["context"]
    bars = max(2, math.ceil(total / 4))
    roots = [[0, 3, 4, 5][(ord(words[b % len(words)][0].upper()) + len(words[b % len(words)])) % 4] for b in range(bars)]
    roots[0], roots[-2], roots[-1] = 0, 4, 0
    base = 7 * 4                                           # around C3
    out = []
    for b, r in enumerate(roots):
        length = 4.0 if b < bars - 1 else total - 4 * (bars - 1)
        out.append([realise(base + r, tonic, minor), length])
    return out


def thresholds(n_open, n_rest, seed):
    """Where each note is learned: the opening over 0.06..0.30, the rest over 0.34..1 with a little scatter, the last
    note at exactly 1 (perfect is every note)."""
    t = [round(0.06 + 0.24 * i / max(1, n_open - 1), 3) for i in range(n_open)]
    for i in range(n_rest):
        base = 0.34 + 0.66 * (i + 1) / n_rest
        jit = (h("%s.%d" % (seed, i), 1000) / 1000 - 0.5) * 0.7 / n_rest
        t.append(round(min(0.99, max(0.31, base + jit)), 3))
    t[-1] = 1.0
    return t


def part(k, s, stage, line, span):
    ty = s["types"][0]
    tonic, minor, _ = KEYS[ty]
    o_notes, o_beats = opening(s["name"], line, ty)
    drop = STAGE_DEG[min(3, stage)]                        # the opening sung lower in the key (a fourth, an octave),
    o_notes = [[st + drop, acc] for st, acc in o_notes]    # and the words then go home to the tonic below it
    held = o_notes[-1][0]
    tonic_step = 7 * (held // 7)                           # the tonic in the opening's octave
    w_notes, w_beats = melody(words_of((s.get("entry") or {}).get("CONTENT") or s["name"]), held, tonic_step)
    c_notes, c_beats = cadence((w_notes or o_notes)[-1][0], tonic_step)
    notes, beats = o_notes + w_notes + c_notes, o_beats + w_beats + c_beats
    total = sum(beats)
    beats[-1] += (-total) % 4                              # the last note fills its bar
    midi = [realise(st, tonic, minor, acc) for st, acc in notes]
    while min(midi) < LOW:
        midi = [m + 12 for m in midi]
    while max(midi) > HIGH and min(midi) - 12 >= LOW - 5:
        midi = [m - 12 for m in midi]
    th = thresholds(len(o_notes), len(notes) - len(o_notes), s["name"])
    bpm = round(BPM.get(gs.PALETTE[ty]["step"], 100) * (1 - 0.06 * (stage - 1)))
    return {"name": s["name"], "stage": stage, "type": ty, "key": key_name(tonic, minor), "tonic": tonic, "minor": minor,
            "bpm": bpm, "from": span[0], "to": span[1],
            "notes": [[m, b, t] for m, b, t in zip(midi, beats, th)],
            "bass": bass((s.get("entry") or {}).get("CONTEXT"), sum(beats), tonic, minor)}


def build(sp=None):
    sp = sp or species()
    parent, paths = lines(sp)
    sp_spans = spans(sp, paths)
    parts = {k: part(k, s, len(paths[k]), sp[paths[k][0]]["name"], sp_spans[k]) for k, s in sp.items()}
    return sp, paths, parts


def songs_json(sp=None):
    """songs.json as text, one part and one song a line, so a change to one daemon is one line of its diff."""
    t = songs_table(sp)
    head = {k: v for k, v in t.items() if k not in ("parts", "songs")}
    lines = ["{"] + ['%s: %s,' % (json.dumps(k), json.dumps(v, ensure_ascii=False)) for k, v in head.items()]
    for name in ("parts", "songs"):
        rows = list(t[name].items())
        lines.append('%s: {' % json.dumps(name))
        lines += [' %s: %s%s' % (json.dumps(k), json.dumps(v, separators=(",", ":"), ensure_ascii=False),
                                 "," if i < len(rows) - 1 else "") for i, (k, v) in enumerate(rows)]
        lines.append("}," if name == "parts" else "}")
    return "\n".join(lines) + "\n}\n"


def songs_table(sp=None):
    """The companion's songs.json: every form's part, and each species' song as the forms it is made of."""
    if sp is not None:
        sp = {k: v for k, v in sp.items() if v.get("name") and v["name"] != "?"}
    sp, paths, parts = build(sp)
    return {
        "_about": "T-594 (DAEMONS vision 9.36), written by DAEMONS tools/gensongs.py through companion_export.py -- never "
                  "edit by hand. parts: a form's own part of its line's song (notes [midi, beats, the share of the part "
                  "at which it is learned], bass [midi, beats], bpm, its key, and the levels it is learned between: "
                  "from, the level its form begins, to, the level it is perfect at). songs: a species' song, its line's "
                  "forms oldest first. window: how much of its part static takes to close on a note; static: its candidates, "
                  "steps along the key from the true note, the first kept longest, and its hiss. Every note DRAFT.",
        "window": WINDOW,
        "static": {"candidates": STATIC, "floor": STATIC_FLOOR},
        "keys": {t: {"tonic": v[0], "minor": v[1], "name": key_name(v[0], v[1]), "why": v[2]} for t, v in KEYS.items()},
        "spare": SPARE,
        "colours": {str(pc): pc_colours(pc) for pc in range(12)},
        "binary": BINARY_GREEN,
        "parts": parts,
        "songs": {k: paths[k] for k in sp},
    }


# ---------------------------------------------------------------------------------------------------------------------
# Hearing it: the game's own harp, and static closing on a note not yet learned
# ---------------------------------------------------------------------------------------------------------------------
SR = 22050


def _harp(key, dur, vel):
    import numpy as np
    import gencries as gc
    x, rate, loop = gc.voice("daemons_harp")
    step = rate * 2 ** ((key - 60) / 12) / SR
    n = int((dur + 0.25) * SR)
    pos = np.arange(n) * step
    if loop is not None:
        pos = np.where(pos >= len(x) - 1, loop + (pos - loop) % (len(x) - loop), pos)
    pos = np.clip(pos, 0, len(x) - 2)
    i = pos.astype(int)
    y = x[i] + (x[i + 1] - x[i]) * (pos - i)
    env = np.ones(n)
    k = min(n, int(dur * SR))
    env[k:] = np.linspace(1, 0, n - k)
    return y * env * vel


def key_step(midi, k, tonic, minor):
    """k steps along the key from a note (a note off the key, CORRUPT's bent one, steps from the key note below)."""
    scale = MINOR if minor else MAJOR
    in_key = lambda m: (m - tonic) % 12 in scale
    n = midi
    while not in_key(n):
        n -= 1
    for _ in range(abs(k)):
        n += 1 if k > 0 else -1
        while not in_key(n):
            n += 1 if k > 0 else -1
    return n


def _static(part, key, dur, near, seed):
    """A note not yet learned (the user: "a lot of agreeing potential notes are the static and gradually the noise is
    removed until just the daemon's song note is revealed"): the true note among CANDIDATES in the key, the least
    agreeing leaving first as `near` goes 0..1, each at a breath of its own, over a hiss that fades as it closes."""
    import numpy as np
    from scipy.signal import lfilter
    r = np.random.RandomState(seed)
    n = int(dur * SR)
    keep = round(len(STATIC) * (1 - near))
    cands = [key_step(key, k, part["tonic"], part["minor"]) for k in STATIC[:keep]]
    true_w = 0.25 + 0.75 * near
    out = _harp(key, dur, 0.7 * true_w)[:n]
    out = np.pad(out, (0, max(0, n - len(out))))
    for c in cands:                                         # the cloud: each candidate a little late, a little soft
        lag = int(r.uniform(0, 0.035) * SR)
        z = _harp(c, max(0.05, dur - lag / SR), 0.7 * (1 - true_w) / max(1, len(cands)) * 2.2)[:n - lag]
        out[lag:lag + len(z)] += z
    hiss = lfilter([0.25], [1, -0.75], r.uniform(-1, 1, n))  # the noise under it, gone by the time it is learned
    env = np.minimum(1, np.arange(n) / (0.01 * SR)) * np.minimum(1, (n - np.arange(n)) / (0.04 * SR))
    return out + hiss * env * STATIC_FLOOR * (1 - near) ** 2


def render(form_parts, learned, window=WINDOW):
    """A song as a daemon knows it: each part with the share of it learned (1 for every part before its own)."""
    import numpy as np
    pieces = []
    for p, f in zip(form_parts, learned):
        sec = 60 / p["bpm"]
        total = sum(b for _, b, _ in p["notes"]) * sec + 0.6
        y = np.zeros(int(total * SR) + SR)
        t = 0.0
        for j, (m, b, th) in enumerate(p["notes"]):
            d = b * sec
            if f >= th:
                z = _harp(m, d * 0.95, 0.8)
            else:
                near = max(0.0, min(1.0, (f - (th - window)) / window))
                z = _static(p, m, d * 0.95, near, h("%s.%d" % (p["name"], j), 10 ** 6))
            a = int(t * SR)
            y[a:a + len(z)] += z[:len(y) - a]
            t += d
        t = 0.0
        for m, b in p["bass"]:                              # the context: quiet until the tune is known
            d = b * sec
            z = _harp(m, d * 0.9, 0.22 + 0.25 * f)
            a = int(t * SR)
            y[a:a + len(z)] += z[:len(y) - a]
            t += d
        pieces.append(y[:int(total * SR)])
    y = np.concatenate(pieces) if pieces else np.zeros(SR)
    return y / (np.abs(y).max() or 1) * 0.9


def mp3(path, y):
    import numpy as np, subprocess, wave
    os.makedirs(os.path.dirname(path), exist_ok=True)
    wav = path[:-4] + ".tmp.wav"
    w = wave.open(wav, "wb")
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())
    w.close()
    subprocess.run(["lame", "--quiet", "-b", "64", "-m", "m", wav, path], check=True)
    os.remove(wav)


def by_name(sp, name):
    return next(k for k, s in sp.items() if s["name"] == name)


def sampler_plan(sp, paths):
    """(title, species, learned shares) -- three whole lines, one part learned a fifth at a time, a type's family."""
    plan = []
    for name in ("ROVERBYTE", "RIPPLE", "MONOLITH"):
        k = next((k for k, s in sp.items() if s["name"] == name), None)
        if k:
            plan.append(("%s's whole song (%s)" % (name, " -> ".join(sp[f]["name"] for f in paths[k])), k, [1.0] * len(paths[k])))
    k = by_name(sp, "ROVERCUB")
    for f in (0.0, 0.25, 0.5, 0.75, 0.9, 1.0):
        plan.append(("ROVERCUB, %d%% of its part learned" % round(f * 100), k, [f]))
    flows = [k for k, s in sp.items() if s["types"][0] == "FLOW" and len(paths[k]) == 1][:3]
    for k in flows:
        plan.append(("%s (FLOW, first form)" % sp[k]["name"], k, [1.0]))
    return plan


def previews(outdir):
    import numpy as np
    sp, paths, parts = build()
    plan = sampler_plan(sp, paths)
    reel, listing = [], []
    for title, k, learned in plan:
        y = render([parts[f] for f in paths[k]], learned)
        slug = re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")[:60]
        mp3(os.path.join(outdir, "songs", slug + ".mp3"), y)
        reel += [y, np.zeros(int(1.2 * SR))]
        listing.append("%-60s %5.1f s" % (title, len(y) / SR))
    mp3(os.path.join(outdir, "sampler.mp3"), np.concatenate(reel))
    with open(os.path.join(outdir, "SAMPLER.txt"), "w") as f:
        f.write("T-594 THE SONG, DRAFT: the sampler, in order\n\n" + "\n".join(listing) + "\n")
    print("gensongs: %d clips and sampler.mp3 in %s" % (len(plan), os.path.relpath(outdir, ROOT)))


# ---------------------------------------------------------------------------------------------------------------------
# Seeing it: a line's song in its colours, a note's height its pitch, its length its time
# ---------------------------------------------------------------------------------------------------------------------
def sheet(sp, paths, parts, k, path, learned=None):
    from PIL import Image, ImageDraw, ImageFont
    forms = [parts[f] for f in paths[k]]
    learned = learned or [1.0] * len(forms)
    beat_px, semi_px, pad = 26, 7, 40
    width = int(sum(sum(b for _, b, _ in p["notes"]) for p in forms) * beat_px) + pad * 2 + 20 * len(forms)
    lo = min(m for p in forms for m, _, _ in p["notes"]) - 2
    hi = max(m for p in forms for m, _, _ in p["notes"]) + 2
    height = (hi - lo) * semi_px + 120
    im = Image.new("RGB", (max(width, 640), height), (18, 20, 28))
    d = ImageDraw.Draw(im)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 13)
    except OSError:
        font = ImageFont.load_default()
    for m in range(lo, hi + 1):                            # the staff: a faint line on every C and G
        if m % 12 in (0, 7):
            y = 70 + (hi - m) * semi_px
            d.line([(pad, y), (im.width - pad, y)], fill=(40, 44, 58))
            d.text((6, y - 7), ("C" if m % 12 == 0 else "G") + str(m // 12 - 1), fill=(90, 96, 120), font=font)
    x = pad
    for p, f in zip(forms, learned):
        d.text((x, 8), "%s  %s  Lv %d-%d" % (p["name"], p["key"], p["from"], p["to"]), fill=(230, 230, 240), font=font)
        d.text((x, 26), "%d notes, %d bpm, %s" % (len(p["notes"]), p["bpm"], p["type"]), fill=(150, 150, 170), font=font)
        for m, b, th in p["notes"]:
            w = b * beat_px - 3
            y = 70 + (hi - m) * semi_px - 5
            cols = pc_colours(m)
            if f >= th:
                if len(cols) == 1:
                    d.rounded_rectangle([x, y, x + w, y + 10], 4, fill=cols[0])
                else:                                       # a black key: the two colours either side, split
                    d.rounded_rectangle([x, y, x + w, y + 10], 4, fill=cols[0])
                    d.rectangle([x + w / 2, y, x + w, y + 10], fill=cols[1])
            else:
                d.rounded_rectangle([x, y, x + w, y + 10], 4, outline=(90, 90, 100))
            x += b * beat_px
        x += 20
    d.text((pad, height - 22), "T-594 DRAFT: a note's colour is its pitch (C red, D orange, E yellow, F green, G blue, "
           "A indigo, B violet; a black key split)", fill=(120, 120, 140), font=font)
    im.save(path)


def sheets(outdir):
    sp, paths, parts = build()
    os.makedirs(os.path.join(outdir, "sheets"), exist_ok=True)
    for title, k, learned in sampler_plan(sp, paths):
        if "%" in title:
            continue
        sheet(sp, paths, parts, k, os.path.join(outdir, "sheets", sp[k]["name"].lower() + ".png"), learned)
    k = by_name(sp, "ROVERCUB")
    sheet(sp, paths, parts, k, os.path.join(outdir, "sheets", "rovercub_half_learned.png"), [0.5])
    with open(os.path.join(outdir, "SONGS.txt"), "w") as f:
        f.write(text_report(sp, paths, parts))
    print("gensongs: sheets and SONGS.txt in %s" % os.path.relpath(outdir, ROOT))


def text_report(sp, paths, parts):
    out = ["T-594 THE SONG, DRAFT -- every form's part (tools/gensongs.py)", "", "THE KEYS"]
    for t, (tonic, minor, why) in KEYS.items():
        n = sum(1 for s in sp.values() if s["types"][0] == t)
        out.append("  %-9s %-16s %3d daemons  %s" % (t, key_name(tonic, minor), n, why))
    out.append("  spare: " + ", ".join(SPARE))
    out += ["", "THE PARTS (form, its key, levels, notes, seconds)"]
    for k in sorted(sp, key=lambda k: sp[k]["national"]):
        p = parts[k]
        secs = sum(b for _, b, _ in p["notes"]) * 60 / p["bpm"]
        out.append("  #%03d %-12s %-16s Lv %3d-%-3d %2d notes %4.1f s  song: %s" % (
            sp[k]["national"], p["name"], p["key"], p["from"], p["to"], len(p["notes"]), secs,
            " + ".join(sp[f]["name"] for f in paths[k])))
    return "\n".join(out) + "\n"


def report():
    sp, paths, parts = build()
    secs = [sum(sum(b for _, b, _ in parts[f]["notes"]) * 60 / parts[f]["bpm"] for f in paths[k]) for k in sp]
    print("gensongs: %d daemons, %d parts; a song %.1f to %.1f s, %.1f on average (DRAFT, nothing approved)"
          % (len(sp), len(parts), min(secs), max(secs), sum(secs) / len(secs)))
    used = {key_name(t, m) for t, m, _ in KEYS.values()}
    assert len(used) == len(KEYS), "gensongs: two types share a key"
    for t, (tonic, minor, why) in KEYS.items():
        print("  %-9s %-16s %s" % (t, key_name(tonic, minor), why))
    print("  spare: " + ", ".join(SPARE))
    for name in ("ROVERBYTE",):
        k = by_name(sp, name)
        for f in paths[k]:
            p = parts[f]
            print("  %s part %d, %s, Lv %d-%d: %s" % (p["name"], p["stage"], p["key"], p["from"], p["to"],
                                                      " ".join("%d/%g" % (m, b) for m, b, _ in p["notes"])))


def main():
    a = sys.argv[1:]
    def after(flag, default):
        i = a.index(flag)
        return a[i + 1] if i + 1 < len(a) and not a[i + 1].startswith("--") else default
    if "--json" in a:
        sys.stdout.write(songs_json())
    elif "--previews" in a:
        previews(after("--previews", OUT_DIR))
    elif "--sheets" in a:
        sheets(after("--sheets", OUT_DIR))
    else:
        report()


if __name__ == "__main__":
    main()
