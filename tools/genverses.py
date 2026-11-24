#!/usr/bin/env python3
"""T-613: THE VERSES -- a line's song as one song in verses, a quote a verse, a hidden chorus. DRAFT, nothing approved.

    python3 tools/genverses.py                    # report: the six sample lines, their hooks, and the hook check
    python3 tools/genverses.py --sampler [DIR]    # an .mp3 of each line, sampler.mp3, SAMPLER.txt and a sheet a line
                                                  # (default audio/drafts/t613_verses)
    python3 tools/genverses.py --hooks            # every form's hook, made from a stand-in text, checked unique

THE DESIGN is docs/song-verses-draft.md, with the user's decisions of 2026-11-23:
    a LINE      one key and one tempo, from its first form's first type (KEYS, BPM); each stage's voice lower. A line
                whose first type changes turns to the new key in its chorus.
    a VERSE     a form's own part, set to its QUOTE a note a syllable, so each word appears as it is sung. It opens with
                its HOOK -- its first seven notes, which end on an open, restful note (the third or the fifth), held --
                and answers home to the tonic by its last note. The hook's first step is its type's motif's first step,
                so a type's daemons start alike by ear; the rest is the verse's own. The second type shades the answer:
                the answer opens with that type's motif. The NAME shapes the verse's gesture (TANGENT rises along a
                slope, then goes straight on).
    the HOOK    the cry, and the summon: unique in shape (its buttons on the key wheel) across all 400, so a hook in the
                wrong key can still say whose it almost was.
    the CHORUS  short, between the verses, heard once the final form knows its whole song; its tune is the line's old
                cry (gensongs.opening, the family's sound), set to a few words, and it leads into the next verse's key.
    the BASS    a chord a bar chosen to fit the tune (I, ii, IV, V, vi), a half cadence where the hook ends, V then I.

The quotes: the forms with a quotation in docs/quotations-draft.md (T-599, DRAFT) use it. Every other line is a
PLACEHOLDER, written only so its tune has a rhythm to follow: T-599 writes the real ones. The chorus words are all
placeholders.
"""
import os, random, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import gensongs as g                                       # the keys, the harp, the species and their lines
import genuisounds as gs                                   # a type's motif and its pace

OUT_DIR = os.path.join(ROOT, "audio", "drafts", "t613_verses")
QUOTES_MD = os.path.join(ROOT, "docs", "quotations-draft.md")

HOOK = 7                                                   # the summon's notes (the user, 2026-11-23)
CANDIDATES = 1500                                          # tunes tried a verse; the best that keeps its hook unique
RANGE = {1: (0, 9), 2: (-3, 6), 3: (-6, 3)}                # a stage's tune, in scale steps around its tonic
TONIC_STEP = 7 * 5                                         # the tonic's octave (scale steps, C4 = 35)

# The words. Placeholders are marked; T-599's own quotations are read from its draft.
PLACEHOLDER = {
    "TANGENT": "Go the way the ground falls from here. Tomorrow will have a slope of its own.",
    "PENPHIN": "Wait until both of you agree. Then let the water carry you.",
    "IFTRUE": "What held inside you decides the shape you come out in.",
    "THENCASE": "Fly the path that was expected of you, and fly it bright.",
    "IFFALSE": "Failing inside is not finishing. Go on the other way.",
    "OTHERWISE": "Not every road was written down. Some are only flown at night.",
    "FIRMWARE": "Wear a thing long enough and it becomes the shape of you.",
}
CHORUS = {                                                 # every one a placeholder
    "ROVERBYTE": "From the arms, to the window, to the door.",
    "PENPHIN": "Count the waves, then count to two.",
    "THENCASE": "Pale silk, and what follows.",
    "OTHERWISE": "Dark silk, and what follows anyway.",
    "BIGIRON": "The same, the same, and running still.",
}
# The name's gesture (the user: "the daemons name itself defines a lot"): a contour the verse leans toward. For the
# ~400 these come with the quotes (one word a daemon, from its name and INDEX entry); unset, a verse arches.
GESTURE = {
    "TANGENT": "rise-level", "GRADIENT": "fall", "DOLPHIN": "leap", "PENPHIN": "valley", "ROVERCUB": "arch",
    "ROVERSEER": "rise", "ROVERBYTE": "leap", "HASHSEED": "arch", "IFTRUE": "rise", "THENCASE": "rise",
    "IFFALSE": "fall", "OTHERWISE": "valley", "BOOTROM": "level-rise", "FIRMWARE": "level", "BIGIRON": "fall",
}
SAMPLE = ["ROVERBYTE", "TANGENT", "GRADIENT", "PENPHIN", "THENCASE", "OTHERWISE", "BIGIRON"]

UNSTRESSED = set("a an the of to and or but is it its it's you your we our are was were be been in on at as by for "
                 "from with that than then what who this these those has have had do does not no so if one".split())


# ---------------------------------------------------------------------------------------------------------------------
# Words into syllables, each syllable a note
# ---------------------------------------------------------------------------------------------------------------------
def quotes():
    """T-599's draft quotations by name (the A style where a type has two)."""
    text = open(QUOTES_MD).read()
    out = {}
    for m in re.finditer(r"^\*\*\d{3} ([A-Z0-9 ]+)\*\*.*?\n\n((?:>.*\n)+)", text, re.M):
        lines = [l[1:].strip() for l in m.group(2).splitlines()]
        first = re.sub(r"^\*\*[AB]\*\*\s*", "", lines[0]).strip()
        out[m.group(1).strip()] = first
    return out


def count_syllables(word):
    """gensongs' count, and a silent -es or -ed (waves, carried) not counted as a syllable of its own."""
    n = g.syllables(word)
    w = word.lower()
    if n > 1 and len(w) > 3 and w[-3] not in "aeiouy" and (
            (w.endswith("es") and not re.search(r"(s|c|z|g|sh|ch|x)es$", w))
            or (w.endswith("ed") and not re.search(r"[td]ed$", w))):
        n -= 1
    return n


def split_syllables(word):
    """A word cut into count_syllables(word) pieces at its vowel groups, for printing under the notes."""
    n = count_syllables(word)
    if n == 1:
        return [word]
    spans = [m.start() for m in re.finditer(r"[aeiouyAEIOUY]+", word)][1:n]
    cuts = []
    for s in spans:
        c = s - 1 if s - 1 > (cuts[-1] if cuts else 0) and word[s - 1].isalpha() else s
        if c - 1 > (cuts[-1] if cuts else 0) and word[c - 1:c + 1].lower() in ("th", "sh", "ch", "wh", "ph", "gh"):
            c -= 1                                         # a digraph stays whole: any-thing, some-where
        cuts.append(c)
    pieces, a = [], 0
    for c in cuts:
        pieces.append(word[a:c]); a = c
    pieces.append(word[a:])
    pieces = [p for p in pieces if p]
    while len(pieces) > n:
        pieces[-2:] = [pieces[-2] + pieces[-1]]
    while len(pieces) < n:
        pieces.append("")
    return pieces


def syllabify(text):
    """[(syllable, stressed, word_start, pause)] -- pause 0 none, 1 a comma's breath, 2 a sentence's end."""
    out = []
    for raw in text.split():
        w = re.sub(r"[^A-Za-z']", "", raw)
        if not w:
            continue
        pieces = split_syllables(w)
        pause = 2 if raw[-1] in ".!?" else 1 if raw[-1] in ",;:" else 0
        for i, p in enumerate(pieces):
            if len(pieces) == 1:
                stressed = w.lower() not in UNSTRESSED
            else:
                stressed = i == 0
            out.append([p, stressed, i == 0, pause if i == len(pieces) - 1 else 0])
    return out


def rhythm(syls, hook_end=True):
    """(beats, rests) a syllable: a stressed one a beat, an unstressed a half; a comma lengthens to the next beat and a
    half, a sentence's end to the bar line -- the note held at most two beats and a half, a rest for the rest; the
    hook's last note at least a beat and a half, so the hook rests there."""
    beats, rests, t = [], [], 0.0
    for j, (_, stressed, _, pause) in enumerate(syls):
        b, r = (1.0 if stressed else 0.5), 0.0
        if j == HOOK - 1 and hook_end:
            b = max(b, 1.5)
        if pause == 1:
            b = max(b, 1.0); b += (-(t + b)) % 1.0 + 0.5
        if pause == 2 and j < HOOK - 1 and hook_end:      # a sentence inside the hook: a breath, not a bar's rest
            b = max(b, 1.0)
            r = 0.5
        elif pause == 2 or j == len(syls) - 1:
            b = max(b, 1.5)
            fill = (-(t + b)) % 4.0
            held = min(b + fill, max(b, 2.5))
            r = b + fill - held
            b = held
        beats.append(b)
        rests.append(r)
        t += b + r
    return beats, rests


# ---------------------------------------------------------------------------------------------------------------------
# A tune: tried many ways, scored, the best kept
# ---------------------------------------------------------------------------------------------------------------------
def motif_steps(ty):
    """A type's motif as steps between its notes (scale steps)."""
    if ty not in gs.PALETTE:                              # ORACLE has no motif of its own (MISSINGNO alone)
        return []
    m = [g.degree_of(n)[0] for n in gs.PALETTE[ty]["m"]]
    return [b - a for a, b in zip(m, m[1:])]


def clamp_step(s):
    return max(-4, min(4, s))


def gesture_curve(name, n):
    """The name's contour, 0..1 across the verse, high where the tune should be high."""
    kind = GESTURE.get(name, "arch")
    xs = [i / max(1, n - 1) for i in range(n)]
    f = {"arch": lambda x: 1 - abs(2 * x - 1.3) / 1.3, "rise": lambda x: x, "fall": lambda x: 1 - x,
         "valley": lambda x: abs(2 * x - 1), "level": lambda x: 0.5 + 0.1 * (x > 0.6),
         "rise-level": lambda x: min(1, x * 2.2), "level-rise": lambda x: max(0.2, (x - 0.45) * 1.8),
         "leap": lambda x: 0.2 if x < 0.15 else 1 - 0.6 * x}[kind]
    return [f(x) for x in xs]


def candidate(rng, n, lo, hi, first_step, answer_steps, hook_target):
    """A tune of n scale steps (relative to the tonic): a walk mostly by step, its hook's first step the type's, the
    hook ending on `hook_target`, the answer opening with the second type's motif, home by step at the end."""
    weights = [(0, 3), (1, 11), (-1, 11), (2, 5), (-2, 5), (3, 2), (-3, 2), (4, 1), (-4, 1), (5, 0.5), (-5, 0.5)]
    steps, ws = zip(*weights)
    start = rng.choice([0, 2, 4, 4, 2, -3]) if lo <= 0 else rng.choice([lo + 3, lo + 5])
    start = max(lo, min(hi, start))
    tune = [start]
    j = 1
    while j < n:
        if j == 1 and first_step is not None:
            s = clamp_step(first_step)
        elif j >= HOOK and j < HOOK + len(answer_steps):
            s = clamp_step(answer_steps[j - HOOK])
        else:
            s = rng.choices(steps, ws)[0]
            if len(tune) >= 2 and abs(tune[-1] - tune[-2]) > 2:       # a leap is recovered by a step back
                s = -1 if tune[-1] > tune[-2] else 1
        nxt = tune[-1] + s
        if nxt > hi or nxt < lo:
            nxt = tune[-1] - s if lo <= tune[-1] - s <= hi else tune[-1]
        tune.append(nxt)
        j += 1
    if n > HOOK:                                           # the hook rests on its third or fifth, near where it was
        t = tune[HOOK - 1]
        opts = [x for x in range(lo, hi + 1) if x % 7 == hook_target]
        tune[HOOK - 1] = min(opts, key=lambda x: abs(x - t)) if opts else t
    end = 0 if lo <= 0 <= hi else 7 * round((lo + hi) / 14)
    tune[-1] = end
    if n >= 2:
        tune[-2] = end + (1 if tune[-3 if n >= 3 else -2] >= end else -1)
    return tune


CHORDS = {"I": (0, 2, 4), "ii": (1, 3, 5), "IV": (3, 5, 0), "V": (4, 6, 1), "vi": (5, 0, 2)}


def chord_fit(tune, beats, rests):
    """How much of the tune (by time, a downbeat counted double) sits in the chord that best fits its bar, 0..1."""
    bars, t = {}, 0.0
    for st, b, r in zip(tune, beats, rests):
        bars.setdefault(int(t // 4), []).append((st % 7, b * (2.0 if t % 2 == 0 else 1.0)))
        t += b + r
    got = total = 0.0
    for notes in bars.values():
        total += sum(w for _, w in notes)
        got += max(sum(w for d, w in notes if d in tones) for tones in CHORDS.values())
    return got / (total or 1)


def score(tune, syls, beats, curve, lo, hi, name="", rests=None):
    s = 6 * chord_fit(tune, beats, rests or [0] * len(beats))
    n = len(tune)
    moves = [b - a for a, b in zip(tune, tune[1:])]
    stepwise = sum(1 for m in moves if abs(m) <= 1) / max(1, len(moves))
    s -= 6 * abs(stepwise - 0.68)
    for i in range(len(moves) - 1):                        # leaps recovered
        if abs(moves[i]) > 2 and (moves[i + 1] * moves[i] > 0 or abs(moves[i + 1]) > 2):
            s -= 2
    run = 1
    for i in range(1, n):                                  # no drone
        run = run + 1 if tune[i] == tune[i - 1] else 1
        if run >= 3 and "level" not in GESTURE.get(name, ""):
            s -= 1.5
    peak = max(tune)
    if tune.count(peak) == 1:
        s += 3
        pos = tune.index(peak) / max(1, n - 1)
        if 0.45 <= pos <= 0.85:
            s += 2
    hook = tune[:HOOK]
    if len(set(hook)) >= 4:
        s += 2
    if any(abs(b - a) >= 2 for a, b in zip(hook, hook[1:])):
        s += 1
    if hook[-1] % 7 in (2, 4):
        s += 2
    if hook[-1] == hook[-2]:                               # the hook arrives on its resting note, not sits on it
        s -= 2
    for j, (_, stressed, _, pause) in enumerate(syls):     # a phrase ends on the tonic chord; a stressed syllable lifts
        if pause and j < n - 1 and tune[j] % 7 in (0, 2, 4):
            s += 1
        if stressed and j > 0 and not syls[j - 1][1] and tune[j] >= tune[j - 1]:
            s += 0.4
    if n > HOOK + 3:                                       # the hook's opening shape comes back in the answer
        shape = [hook[1] - hook[0], hook[2] - hook[1]]
        rest = tune[HOOK:]
        if any([rest[i + 1] - rest[i], rest[i + 2] - rest[i + 1]] == shape for i in range(len(rest) - 2)):
            s += 2.5
    span = (hi - lo) or 1                                  # the name's gesture
    dev = sum(abs((t - lo) / span - c) for t, c in zip(tune, curve)) / n
    s -= 8 * dev
    return s


def buttons(tune, minor):
    """The hook as PLAY's seven buttons on its key's wheel: a minor key's relative major (a minor tonic is button 6)."""
    return tuple(((t % 7) + (5 if minor else 0)) % 7 for t in tune[:HOOK])


def compose(name, ty, ty2, text, stage, tonic, minor, taken, seed=""):
    """A verse: (tune in scale steps from the tonic, beats, syllables). `taken` holds the hooks already given out."""
    syls = syllabify(text)
    if len(syls) < HOOK + 2:
        syls += [["la", False, True, 0]] * (HOOK + 2 - len(syls))
    beats, rests = rhythm(syls)
    lo, hi = RANGE[min(3, stage)]
    first = motif_steps(ty)[0] if motif_steps(ty) else None
    answer = motif_steps(ty2)[:3] if ty2 else []
    curve = gesture_curve(name, len(syls))
    rng = random.Random("%s.%s" % (name, seed))
    tried = []
    for c in range(CANDIDATES):
        target = 4 if c % 2 == 0 else 2
        t = candidate(rng, len(syls), lo, hi, first, answer, target)
        tried.append((score(t, syls, beats, curve, lo, hi, name, rests), t))
    tried.sort(key=lambda x: -x[0])
    for sc, t in tried:
        b = buttons(t, minor)
        if b not in taken:
            taken[b] = name
            return {"name": name, "type": ty, "type2": ty2, "tune": t, "beats": beats, "rests": rests, "syls": syls, "score": sc,
                    "tonic": tonic, "minor": minor, "stage": stage, "hook": b}
    raise SystemExit("genverses: no unique hook for %s in %d tries" % (name, CANDIDATES))


def chorus(line_name, first_ty, words, tonic, minor, stage):
    """The hidden chorus: the line's old cry (gensongs.opening) set to a few words, ending on the fifth so the next
    verse is waited for."""
    notes, _ = g.opening(line_name, line_name, first_ty)
    steps = [st for st, _ in notes]
    base = steps[0]
    rel = [st - base + 2 for st in steps]                  # from the third
    syls = syllabify(words)
    n = len(syls)
    tune = [rel[i % len(rel)] + (0 if i < len(rel) else 1) for i in range(n)]
    lo, hi = RANGE[min(3, stage)]
    tune = [max(lo + 2, min(hi + 2, t)) for t in tune]
    tune[-1] = 4 if 4 <= hi + 2 else -3
    beats, rests = rhythm(syls, hook_end=False)
    return {"name": "CHORUS", "tune": tune, "beats": beats, "rests": rests, "syls": syls, "tonic": tonic, "minor": minor,
            "stage": stage, "chorus": True}


# ---------------------------------------------------------------------------------------------------------------------
# Notes and chords
# ---------------------------------------------------------------------------------------------------------------------
def midi_of(seg):
    return [g.realise(TONIC_STEP + t, seg["tonic"], seg["minor"]) + (-12 if seg["stage"] >= 3 else 0)
            for t in seg["tune"]]




def harmony(seg):
    """A chord a bar, the one holding most of the bar's tune (its downbeats weighed more), a half cadence where the
    hook rests, V then I at the end."""
    bars, t = {}, 0.0
    hook_bar = None
    for j, (st, b, r) in enumerate(zip(seg["tune"], seg["beats"], seg["rests"])):
        bar = int(t // 4)
        w = b * (1.5 if t % 2 == 0 else 1.0)
        bars.setdefault(bar, []).append((st % 7, w))
        if j == HOOK - 1:
            hook_bar = bar
        t += b + r
    n = int((t + 3.999) // 4)
    out = []
    for bar in range(n):
        notes = bars.get(bar, [])
        best = max(CHORDS, key=lambda c: sum(w for d, w in notes if d in CHORDS[c]) + (0.3 if c == "I" else 0))
        if bar == hook_bar and not seg.get("chorus") and sum(w for d, w in notes if d in CHORDS["V"]) > 0:
            best = "V"
        out.append(best)
    if seg.get("chorus"):
        out[-1] = "V"
    else:
        out[-1] = "I"
        if n >= 2:
            out[-2] = "V"
    return out, t


def bass_notes(seg, chords):
    out = []
    for c in chords:
        r = CHORDS[c][0]
        root = g.realise(TONIC_STEP - 14 + r, seg["tonic"], seg["minor"])
        fifth = g.realise(TONIC_STEP - 14 + r + 4, seg["tonic"], seg["minor"])
        out += [(root, 2.0), (fifth, 2.0)]
    return out


# ---------------------------------------------------------------------------------------------------------------------
# A line
# ---------------------------------------------------------------------------------------------------------------------
def line_of(final_name, sp, paths, taken, qs):
    k = g.by_name(sp, final_name)
    forms = [sp[f] for f in paths[k]]
    first_ty = forms[0]["types"][0]
    tonic0, minor0, _ = g.KEYS[first_ty]
    bpm = g.BPM.get(gs.PALETTE[first_ty]["step"], 100)
    segs = []
    for i, s in enumerate(forms):
        ty = s["types"][0]
        ty2 = s["types"][1] if len(s["types"]) > 1 else None
        tonic, minor = (tonic0, minor0) if ty == first_ty else g.KEYS[ty][:2]
        name = s["name"]
        text, placeholder = (qs[name], False) if name in qs else (PLACEHOLDER.get(name), True)
        if text is None:
            raise SystemExit("genverses: no words for %s" % name)
        verse = taken.get(("verse", name)) or compose(name, ty, ty2, text, i + 1, tonic, minor, taken["hooks"])
        taken[("verse", name)] = verse
        verse = dict(verse, text=text, placeholder=placeholder)
        if i > 0:
            segs.append(chorus(forms[0]["name"], ty, CHORUS.get(final_name, "And on."), tonic, minor, i + 1))
        segs.append(verse)
    return {"final": final_name, "forms": [s["name"] for s in forms], "bpm": bpm, "segs": segs,
            "chorus_words": CHORUS.get(final_name)}


def render_line(line, with_chorus=True):
    import numpy as np
    sec = 60 / line["bpm"]
    pieces = []
    for seg in line["segs"]:
        if seg.get("chorus") and not with_chorus:
            continue
        mids = midi_of(seg)
        chords, total = harmony(seg)
        y = np.zeros(int((total * sec + 1.0) * g.SR))
        t = 0.0
        for m, b, r in zip(mids, seg["beats"], seg["rests"]):
            z = g._harp(m, b * sec * 0.95, 0.8)
            if seg.get("chorus"):                          # the chorus shines: the tune doubled an octave up
                z = z + 0.35 * g._harp(m + 12, b * sec * 0.95, 1.0)[:len(z)]
            a = int(t * g.SR)
            y[a:a + len(z)] += z[:len(y) - a]
            t += (b + r) * sec
        t = 0.0
        for m, b in bass_notes(seg, chords):
            z = g._harp(m, b * sec * 0.9, 0.3)
            a = int(t * g.SR)
            y[a:a + len(z)] += z[:len(y) - a]
            t += b * sec
        pieces.append(y[:int((total * sec + 0.25) * g.SR)])
    y = np.concatenate(pieces)
    return y / (np.abs(y).max() or 1) * 0.9


def render_hooks(lines):
    import numpy as np
    out, seen = [], set()
    for line in lines:
        sec = 60 / line["bpm"]
        for seg in line["segs"]:
            if seg.get("chorus") or seg["name"] in seen:
                continue
            seen.add(seg["name"])
            mids = midi_of(seg)[:HOOK]
            y = np.zeros(int((sum(seg["beats"][:HOOK]) * sec + 0.8) * g.SR))
            t = 0.0
            for m, b in zip(mids, seg["beats"][:HOOK]):
                z = g._harp(m, b * sec * 0.95, 0.8)
                a = int(t * g.SR)
                y[a:a + len(z)] += z[:len(y) - a]
                t += b * sec
            out += [y, np.zeros(int(0.7 * g.SR))]
    y = np.concatenate(out)
    return y / (np.abs(y).max() or 1) * 0.9


# ---------------------------------------------------------------------------------------------------------------------
# Every form's hook, from a stand-in text, checked unique (the check that runs over all 400 once the quotes exist)
# ---------------------------------------------------------------------------------------------------------------------
def all_hooks(sp, paths, qs, taken):
    lines_done = {}
    for k in sorted(sp, key=lambda k: (len(paths[k]), sp[k]["national"])):
        s = sp[k]
        name = s["name"]
        if ("verse", name) in taken:
            continue
        first_ty = sp[paths[k][0]]["types"][0]
        ty = s["types"][0]
        tonic, minor = g.KEYS[first_ty][:2] if ty == first_ty else g.KEYS[ty][:2]
        text = qs.get(name) or PLACEHOLDER.get(name) or re.sub(r"\s+", " ", (s.get("entry") or {}).get("CONTENT") or name)
        v = compose(name, ty, s["types"][1] if len(s["types"]) > 1 else None, text, len(paths[k]), tonic, minor,
                    taken["hooks"])
        taken[("verse", name)] = v
    hooks = [v["hook"] for key, v in taken.items() if isinstance(key, tuple)]
    return len(hooks), len(set(hooks))


# ---------------------------------------------------------------------------------------------------------------------
# A sheet: each verse and chorus a row, a note's colour its pitch, its syllable under it, the hook marked
# ---------------------------------------------------------------------------------------------------------------------
def sheet(line, path, sp):
    from PIL import Image, ImageDraw, ImageFont
    beat_px, semi_px = 58, 6
    rows = line["segs"]
    width = int(max(sum(s["beats"]) + sum(s["rests"]) for s in rows) * beat_px) + 220
    row_h = []
    for seg in rows:
        m = midi_of(seg)
        row_h.append((max(m) - min(m) + 4) * semi_px + 96)
    im = Image.new("RGB", (max(width, 900), sum(row_h) + 120), (18, 20, 28))
    d = ImageDraw.Draw(im)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 13)
        big = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 17)
        ital = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Italic.ttf", 15)
        serif = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 15)
    except OSError:
        font = big = ital = serif = ImageFont.load_default()
    d.text((20, 14), "%s  --  %s  (%d bpm, one key and tempo a line)" % (" -> ".join(line["forms"]), g.key_name(
        rows[0]["tonic"], rows[0]["minor"]), line["bpm"]), fill=(235, 235, 245), font=big)
    y0 = 52
    for seg, rh in zip(rows, row_h):
        m = midi_of(seg)
        hi = max(m) + 2
        is_ch = seg.get("chorus")
        label = "CHORUS (hidden until the whole song is known)" if is_ch else "%s  %s%s  %s  hook %s" % (
            seg["name"], seg["type"], "/" + seg["type2"] if seg.get("type2") else "",
            g.key_name(seg["tonic"], seg["minor"]), " ".join(note_name(x, seg["tonic"], seg["minor"]).replace("-sharp", "#").replace("-flat", "b") for x in m[:HOOK]))
        d.text((20, y0), label, fill=(200, 190, 255) if is_ch else (230, 230, 240), font=font)
        x, last_end, lift = 160, 0, 0
        for j, (mm, b, rr, syl) in enumerate(zip(m, seg["beats"], seg["rests"], seg["syls"])):
            w = b * beat_px - 4
            y = y0 + 22 + (hi - mm) * semi_px
            cols = g.pc_colours(mm)
            d.rounded_rectangle([x, y, x + w, y + 9], 4, fill=cols[0])
            if len(cols) > 1:
                d.rectangle([x + w / 2, y, x + w, y + 9], fill=cols[1])
            if j < HOOK and not is_ch:
                d.rounded_rectangle([x - 2, y - 2, x + w + 2, y + 11], 5, outline=(255, 255, 255))
            f_ = ital if is_ch else serif
            lift = 16 if (x < last_end + 3 and lift == 0) else 0
            d.text((x, y0 + rh - 44 + lift), syl[0], fill=(210, 200, 255) if is_ch else (220, 220, 230), font=f_)
            if lift == 0:
                last_end = x + d.textlength(syl[0], font=f_)
            x += (b + rr) * beat_px
        if not is_ch and seg.get("placeholder"):
            d.text((160, y0 + rh - 20), "placeholder words, not T-599's", fill=(150, 120, 120), font=font)
        y0 += rh
    d.text((20, im.height - 50), "T-613 DRAFT. A note's colour is its pitch (C red, D orange, E yellow, F green, G blue, "
           "A indigo, B violet; a black key split). The hook (white outline) is the cry and the summon.",
           fill=(130, 130, 150), font=font)
    d.text((20, im.height - 30), "The chorus's words are placeholders; a verse's are T-599's draft where it has one.",
           fill=(130, 130, 150), font=font)
    im.save(path)


SHARP_KEYS = {(7, False), (2, False), (9, False), (4, False), (11, False), (6, False), (4, True), (11, True), (6, True),
              (1, True), (8, True), (9, True), (7, True), (2, True)}
SHARPS = ["C", "C-sharp", "D", "D-sharp", "E", "F", "F-sharp", "G", "G-sharp", "A", "A-sharp", "B"]


def note_name(m, tonic, minor):
    if (tonic, minor) in SHARP_KEYS and (tonic, minor) not in {(2, True), (7, True), (9, True)}:
        return SHARPS[m % 12]
    return g.KEY_NAMES[m % 12]


def text_of(lines, uniq):
    out = ["T-613 THE VERSES -- the sampler, DRAFT (tools/genverses.py)", ""]
    for i, line in enumerate(lines, 1):
        out.append("%d. %s  (%s, %d bpm)" % (i, " -> ".join(line["forms"]), g.key_name(line["segs"][0]["tonic"],
                                                                                         line["segs"][0]["minor"]), line["bpm"]))
        for seg in line["segs"]:
            if seg.get("chorus"):
                out.append("     chorus   *%s*  (placeholder)" % CHORUS.get(line["final"], ""))
            else:
                out.append("     %-9s %s%s" % (seg["name"], seg["text"], "  (placeholder)" if seg["placeholder"] else ""))
                out.append("     %9s hook: %s  (%s)" % ("", " ".join(note_name(m, seg["tonic"], seg["minor"]) for m in midi_of(seg)[:HOOK]),
                                                        g.key_name(seg["tonic"], seg["minor"])))
        out.append("")
    out.append("HOOKS: %d forms given a hook (the six lines' words, every other form's INDEX entry standing in), %d "
               "different -- every one unique in shape, none lengthened, none left out." % uniq)
    return "\n".join(out) + "\n"


def build_lines():
    sp, paths, _ = g.build()
    qs = quotes()
    taken = {"hooks": {}}
    lines = [line_of(n, sp, paths, taken, qs) for n in SAMPLE]
    return sp, paths, qs, taken, lines


def main():
    import numpy as np
    args = sys.argv[1:]
    sp, paths, qs, taken, lines = build_lines()
    if "--sampler" in args:
        i = args.index("--sampler")
        out = args[i + 1] if len(args) > i + 1 and not args[i + 1].startswith("--") else OUT_DIR
        os.makedirs(os.path.join(out, "lines"), exist_ok=True)
        os.makedirs(os.path.join(out, "sheets"), exist_ok=True)
        reel, listing = [], []
        old = g.build()[2]                                 # today's ROVERCUB line, for comparison
        y = g.render([old[f] for f in paths[g.by_name(sp, "ROVERBYTE")]], [1, 1, 1])
        g.mp3(os.path.join(out, "lines", "00_rovercub_line_today.mp3"), y)
        reel += [y, np.zeros(int(1.5 * g.SR))]
        listing.append("%-66s %5.1f s" % ("0. ROVERCUB -> ROVERSEER -> ROVERBYTE as it is TODAY (T-594)", len(y) / g.SR))
        for n, line in enumerate(lines, 1):
            title = "%d. %s" % (n, " -> ".join(line["forms"]))
            y = render_line(line)
            slug = "%02d_%s" % (n, "_".join(f.lower() for f in line["forms"]))
            g.mp3(os.path.join(out, "lines", slug + ".mp3"), y)
            sheet(line, os.path.join(out, "sheets", slug + ".png"), sp)
            reel += [y, np.zeros(int(1.5 * g.SR))]
            listing.append("%-66s %5.1f s" % (title + (", with its chorus" if len(line["forms"]) > 1 else ""),
                                              len(y) / g.SR))
        y = render_hooks(lines)
        g.mp3(os.path.join(out, "lines", "99_every_hook.mp3"), y)
        reel += [y]
        listing.append("%-66s %5.1f s" % ("8. Every form's HOOK alone, in order (its cry, and its summon)", len(y) / g.SR))
        g.mp3(os.path.join(out, "sampler.mp3"), np.concatenate(reel))
        uniq = all_hooks(sp, paths, qs, taken)
        with open(os.path.join(out, "SAMPLER.txt"), "w") as f:
            f.write("T-613 THE VERSES, DRAFT: the sampler, in order\n\n" + "\n".join(listing) + "\n\n" + text_of(lines, uniq))
        print("genverses: %d lines, sampler.mp3, sheets and SAMPLER.txt in %s" % (len(lines), os.path.relpath(out, ROOT)))
        print("genverses: hooks %d given, %d different" % uniq)
        return
    if "--hooks" in args:
        print("genverses: hooks %d given, %d different" % all_hooks(sp, paths, qs, taken))
        return
    uniq = (0, 0)
    print(text_of(lines, uniq))


if __name__ == "__main__":
    main()
