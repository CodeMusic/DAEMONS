#!/usr/bin/env python3
"""T-565 batch 11: the daemons' cries -- all 388 drafted as THE TYPE'S VOICE, shaped by THE NAME (the user's pick,
2026-11-17; docs/cries-design-2026-11-17.md), checked three ways, and written over pret's in place once approved.

    python3 tools/gencries.py                      # report: the 388, pret's length and ours, the three checks, APPROVED
    python3 tools/gencries.py --draft [DIR]        # each cry as the cartridge holds it (8-bit .wav, 10512 Hz), its
                                                   # bytes measured by the engine's wav2agb (default ~/.cache/daemons/
                                                   # t565_cries_wav: outside git, the .wavs are the write's, not drafts)
    python3 tools/gencries.py --previews [DIR]     # an .mp3 of every cry, the sampler, the six cut at 20 frames and the
                                                   # six backwards (default audio/drafts/t565_cries/all)
    python3 tools/gencries.py --sheets [DIR]       # CRIES.txt (every cry, its shaping, bytes and checks) and a picture
                                                   # of the sampler (default audio/drafts/t565_cries/all)
    python3 tools/gencries.py --pret-ref DIR       # pret's sampler, cut and backwards clips through the same model --
                                                   # RETAIL AUDIO: never into a tracked folder
    python3 tools/gencries.py --write --approved   # write APPROVED's cries over pret's .wav (refuses while it is empty),
                                                   # and the eleven's own (T-584) with their rows and labels
    python3 tools/gencries.py --rom [ROM]          # T-584: prove from a built ROM (and its .elf) that every cry is its
                                                   # own sample, the eleven slots included (default daemonsContent.gba)

THE ENGINE (docs/cries-design-2026-11-17.md has the whole of it): a cry is one sample, mono, 8-bit, 10512 Hz, in
sound/direct_sound_samples/cries/<species>.wav; audio_rules.mk compresses it (wav2agb -b -c -l 1 --no-pad: DPCM, 33
bytes a 64 samples). PlayCryInternal (src/sound.c) plays it as one note at key 60; pitch, length and reversal come
from the cry's MODE, never the species. So a cry REPLACES pret's .wav in place: no table, no constant, no engine code.

T-584, CRIES OF THEIR OWN: the eleven daemons in pret's empty slots (THE NEXUS's eight, tools/gbanexus.py, and the
carried line, tools/gbacarried.py) borrowed another species' cry. Each now has a cry of its own, made the same way and
appended after CHIMECHO's: --write adds the .wav, its sound/direct_sound_data.inc label and a row in both cry tables,
and the two tools point SpeciesToCryId at them. A slot's cap is pret's length for the cry it used to borrow.
THE NO-TWINS RULE (T-584): no two cries may play the same notes at the same times. HUNCH and MIME did (the same type,
lines that turn the motif alike, names of the same consonant-vowel shape and initials that land on one pickup): the
later in the cry table takes a tie: the notes its name's initial and last letter choose (the pickup and the note
before the held one) each step to the next choice, until it is heard as its own.

THE SHAPE, per cry (events()):
    the TYPE      its first type's batch-10 PALETTE (genuisounds.py): the motif, the harp or a thin pluck, a square
                  click under each note, the type's noise texture. A second type holds the last note on the FLUTE, on
                  its own motif's last note (a type with "hold" holds its own).
    the LINE      the line's first daemon's name turns the motif (a rotation, maybe reversed): every stage shares it.
    the STAGE     lower and slower: 0, a fourth, an octave down; each unit of time 20% longer a stage.
    the NAME      how many notes (from its length) and their rhythm and accents: a vowel is long and soft, a
                  consonant short and struck, letter by letter.
    the CAP       never longer than pret's cry for the same species (read from pret's own .wav in upstream/master,
                  so the cap survives our write); the pace is squeezed to fit, never the notes dropped.

THE THREE CHECKS (each mode that changes a cry, src/sound.c):
    DOUBLES   CRY_MODE_DOUBLES cuts at 20 frames (0.335 s): at least two notes must start inside it (the contour is
              heard) and it must carry half the loudest window's energy.
    BACKWARD  GROWL_1 plays the cry reversed for 15 frames (0.25 s), ECHO_START for 25: the cry's last 0.25 s must not
              be near-silent (an eighth of the loudest window's energy at least).
    FAINT     CRY_MODE_FAINT lowers it 3.6 semitones: its lowest note must stay at or above E2 (MIDI 40), and its
              slower playback must fit the 140 frames the cry player holds a cry (pret's own long ones are said, not
              failed: the cap is theirs).
"""
import hashlib, io, os, re, struct, subprocess, sys, tempfile, wave

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import genuisounds as gs                                   # PALETTE, TYPE_OF_VANILLA, CHART (read only)

GBA = os.path.join(ROOT, "engineGba")
CRY_DIR = os.path.join(GBA, "sound", "direct_sound_samples", "cries")
SAMPLES = os.path.join(GBA, "sound", "direct_sound_samples")
WAV2AGB = os.path.join(GBA, "tools", "wav2agb", "wav2agb")
PRET_REF = "upstream/master"
OUT_DIR = os.path.join(ROOT, "audio", "drafts", "t565_cries", "all")
SR, MIX, OUT = 10512, 13379, 32768                         # the cries' rate, m4a's mixer, the previews'
FRAME = 1 / 59.7275
DOUBLES_S, GROWL_S, HOLD_FRAMES, FAINT_SEMIS = 20 * FRAME, 15 * FRAME, 140, (15360 - 14440) / 256

# The user's picks: {"*": "A+B"} for all, or {"Cry_Bulbasaur": "A+B", ...}. --write refuses while it is empty.
APPROVED = {"*": "A+B"}   # the user, 2026-11-17, by multiple choice: all 388, A shaped by B (DRAFT)

STAGE_DROP = {1: 0, 2: -5, 3: -12}
PENTA = [0, 2, 4, 7, 9, 12, 14, 16, 19, 21]                # Blanche's C pentatonic, two octaves: a letter's degree
VOWELS = set("AEIOUY")
FLOOR, CEIL = 45, 96                                       # the register: A2 to C7 before any mode moves it
SIX = ["HEAP", "STACK", "MONOLITH", "SPIKE", "DANGLING", "SINGULAR"]   # the design doc's six
LINES = ["HEAP", "CRAWLER", "CANARY"]                      # the sampler's three whole lines, by their first daemon
NOT_SAMPLED = {"EEVEE", "VAPOREON", "JOLTEON", "FLAREON", "ESPEON", "UMBREON"}   # never chosen for the sampler


# ---------------------------------------------------------------------------------------------------------------------
# The engine's facts: the 388 cries, whose they are, their types, stage and line, and pret's length for each
# ---------------------------------------------------------------------------------------------------------------------
def h(s, n):
    return int(hashlib.md5(s.encode()).hexdigest(), 16) % n


def read(rel):
    return open(os.path.join(GBA, rel), encoding="utf-8").read()


def pret_caps(files):
    """pret's own length for each cry, read from upstream's .wav (falls back to the engine's, with a warning)."""
    caps = {}
    paths = ["%s:sound/direct_sound_samples/cries/%s.wav" % (PRET_REF, f) for f in files]
    try:
        p = subprocess.Popen(["git", "-C", GBA, "cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        out, _ = p.communicate(("\n".join(paths) + "\n").encode())
        pos = 0
        for f in files:
            nl = out.index(b"\n", pos)
            head = out[pos:nl].split()
            if head[-1] == b"missing":
                raise KeyError(f)
            size = int(head[2])
            blob = out[nl + 1:nl + 1 + size]
            pos = nl + 1 + size + 1
            w = wave.open(io.BytesIO(blob))
            caps[f] = w.getnframes() / w.getframerate()
    except (KeyError, ValueError, OSError, IndexError):
        print("gencries: %s is not in the engine's git -- pret's lengths read from the working .wav files instead"
              % PRET_REF, file=sys.stderr)
        for f in files:
            w = wave.open(os.path.join(CRY_DIR, f + ".wav"))
            caps[f] = w.getnframes() / w.getframerate()
    return caps


def own():
    """T-584: the eleven that borrowed a cry, in the order their own follow CHIMECHO's: (label, file, the daemon's
    name, the cry each borrowed -- whose pret length caps its own). Read from the two tools that made them."""
    import gbanexus, gbacarried, gbamusaiforms
    return [("Cry_" + ident, ident.lower(), name, cry) for _, name, ident, _, cry in gbanexus.RESIDENTS] + \
           [("Cry_" + ident, ident.lower(), name, cry) for _, name, ident, cry in gbacarried.LINE] + \
           [("Cry_" + ident, ident.lower(), name, cry) for _, name, ident, cry in gbamusaiforms.LINE]   # T-605


def census():
    labels = re.findall(r"^\s*cry (Cry_\w+)", read("sound/cry_tables.inc"), re.M)
    files = dict(re.findall(r'^(Cry_\w+)::\s*\n\s*\.incbin "sound/direct_sound_samples/cries/(\w+)\.bin"',
                            read("sound/direct_sound_data.inc"), re.M))
    mine = own()
    labels = [l for l in labels if l not in {o[0] for o in mine}] + [o[0] for o in mine]   # theirs follow pret's
    files.update({o[0]: o[1] for o in mine})
    names = dict(re.findall(r'\[SPECIES_(\w+)\] = _\("([^"]*)"\)', read("src/data/text/species_names.h")))
    by_norm = {k.replace("_", "").lower(): k for k in names}
    for alias, slot in re.findall(r"#define SPECIES_(\w+) SPECIES_(OLD_UNOWN_\w)\b", read("include/constants/species.h")):
        by_norm[alias.replace("_", "").lower()] = slot       # SPECIES_REFLECTION is SPECIES_OLD_UNOWN_C
    label_of = {l[4:].lower(): l for l in labels}
    info = read("src/data/pokemon/species_info.h")
    types = {sp: (a, b) for sp, a, b in
             re.findall(r"\[SPECIES_(\w+)\] =\s*\{[^}]*?\.types = \{TYPE_(\w+), TYPE_(\w+)\}", info, re.S)}
    parent = {}
    for frm, body in re.findall(r"\[SPECIES_(\w+)\]\s*=\s*\{(.*?)\}\}", read("src/data/pokemon/evolution.h"), re.S):
        for to in re.findall(r"SPECIES_(\w+)\}", body + "}"):
            parent.setdefault(to, frm)
    caps = pret_caps([files[l] for l in labels if l not in {o[0] for o in mine}])
    for label, f, _, was in mine:                           # the cap: the cry it borrowed until T-584
        caps[f] = caps[files[label_of[was.replace("_", "").lower()]]]
    cries = []
    for i, label in enumerate(labels):
        sp = by_norm.get(label[4:].lower())
        root, stage = sp, 1
        while root in parent and stage < 4:
            root, stage = parent[root], stage + 1
        ty = tuple(dict.fromkeys(gs.TYPE_OF_VANILLA[t] for t in types.get(sp, ("NORMAL", "NORMAL"))))
        name = names[sp] if sp else label[4:].upper()
        cries.append(dict(i=i, label=label, file=files[label], species=sp, name=name, types=ty,
                          stage=min(stage, 3), line=names[root] if sp else name, cap=caps[files[label]]))
    return cries


# ---------------------------------------------------------------------------------------------------------------------
# The voices: the game's HARP and FLUTE (geninstruments.py), a square click and the noise, made at the cry rate
# ---------------------------------------------------------------------------------------------------------------------
_V = {}


def voice(label):
    import numpy as np
    if label in _V:
        return _V[label]
    #  T-588: the voice is what the BUILD makes of the .wav (audio_rules.mk: wav2agb -b), made here from the .wav every
    #  time -- never the .bin a build left behind, which a fresh clone or check_generators' sandbox does not have (and
    #  whose fallback below renders every cry differently: --writes read all 399 as drifting), and which can be stale.
    b = os.path.join(SAMPLES, label + ".bin")
    td = None
    if os.access(WAV2AGB, os.X_OK):
        td = tempfile.mkdtemp(prefix="gencries-voice-")
        b = os.path.join(td, label + ".bin")
        subprocess.run([WAV2AGB, "-b", os.path.join(SAMPLES, label + ".wav"), b], check=True, capture_output=True)
    if os.path.exists(b):
        d = open(b, "rb").read()
        if td:
            import shutil
            shutil.rmtree(td, ignore_errors=True)
        flags, freq, loop, size = struct.unpack("<IIII", d[:16])
        x = np.frombuffer(d[16:16 + size], dtype=np.int8).astype(float) / 128
        _V[label] = (x, freq / 1024, loop if flags & 0x40000000 else None)
    else:                                                   # a fresh clone before a build: the .wav and its smpl loop
        raw = open(os.path.join(SAMPLES, label + ".wav"), "rb").read()
        w = wave.open(io.BytesIO(raw))
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
        k = raw.find(b"smpl")
        loop = struct.unpack("<I", raw[k + 8 + 44:k + 8 + 48])[0] if k >= 0 and \
            struct.unpack("<I", raw[k + 8 + 28:k + 8 + 32])[0] else None
        _V[label] = (x, w.getframerate(), loop)
    return _V[label]


def midi(n):
    k = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[n[0]] + (1 if "#" in n else 0)
    return 12 * (int(n[-1]) + 1) + k


def sampled(v, key, dur, vel, rel=0.06):
    import numpy as np
    x, rate, loop = voice(v)
    step = rate * 2 ** ((key - 60) / 12) / SR
    n = int((dur + rel) * SR)
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


def square(key, dur, duty, vel):
    import numpy as np
    t = np.arange(int(dur * SR)) / SR
    return np.where((t * 440 * 2 ** ((key - 69) / 12)) % 1 < duty, 1.0, -1.0) * vel * np.exp(-8 * t)


def noise(dur, vel, decay, seed, color=1.0):
    import numpy as np
    r = np.random.RandomState(seed)
    y = r.uniform(-1, 1, int(dur * SR))
    if color < 1:
        for j in range(1, len(y)):
            y[j] = y[j - 1] + color * (y[j] - y[j - 1])
    return y * vel * np.exp(-decay * np.arange(len(y)) / SR)


# ---------------------------------------------------------------------------------------------------------------------
# THE SHAPE: A (the type's motif) shaped by B (the name)
# ---------------------------------------------------------------------------------------------------------------------
def events(c):
    """The notes of one cry: [(start s, length s, voice, key, velocity)], and the texture it lays under them."""
    pal = gs.PALETTE[c["types"][0]]
    m = [midi(n) for n in pal["m"]]
    rot = h(c["line"], len(m))                              # the LINE's contour
    m = m[rot:] + m[:rot]
    if h(c["line"] + "r", 2):
        m = m[::-1]
    letters = [ch for ch in c["name"] if ch.isalpha()] or ["A"]
    count = max(3, min(len(m) + 2, len(letters) // 2 + 2))  # the NAME: how many notes
    keys = [m[j % len(m)] + (12 if j >= len(m) and m[j % len(m)] < m[-1] - 7 else 0) for j in range(count)]
    shift = STAGE_DROP[c["stage"]]                          # the STAGE: lower
    while min(keys) + shift < FLOOR:
        shift += 12
    while max(keys) + shift > CEIL:
        shift -= 12
    keys = [k + shift for k in keys]
    beats = [(1.6 if letters[j % len(letters)] in VOWELS else 1.0) for j in range(count)]   # the NAME: rhythm
    accents = [(0.7 if letters[j % len(letters)] in VOWELS else 0.95) for j in range(count)]
    accents[0] = 1.0
    beats[-1] = 2.5
    first, final = letters[0], letters[-1]                  # the NAME: its initial as a pickup, its last letter
    tie = c.get("tie", 0)                                   # THE NO-TWINS RULE: a tie steps the name's two ends on
    pk = keys[0] - keys[0] % 12 + PENTA[(ord(first) - 65 + tie) % 10]   # leading into the held note
    while pk - keys[0] > 7:
        pk -= 12
    while keys[0] - pk > 7:
        pk += 12
    if pk == keys[0]:
        pk -= 3
    ap = keys[-1] + (2, -3, -5)[(ord(final) + tie) % 3]
    pk, ap = [k + 12 if k < FLOOR else k - 12 if k > CEIL else k for k in (pk, ap)]
    keys = [pk] + keys[:-1] + [ap, keys[-1]]
    beats = [0.5] + beats[:-1] + [0.5, beats[-1]]
    accents = [0.75] + accents[:-1] + [0.6, accents[-1]]
    count = len(keys)
    unit = max(0.05, pal["step"] / 60 * 1.6) * (1 + 0.2 * (c["stage"] - 1))   # the STAGE: slower
    unit = min(unit, c["cap"] * 0.9 / (sum(beats) + 0.06 / max(unit, 0.01)))      # the CAP: squeezed, never cut
    unit = max(unit, 0.012)
    two = len(c["types"]) > 1
    out, t = [], 0.0
    for j, (k, b, a) in enumerate(zip(keys, beats, accents)):
        last = j == count - 1
        if last and (pal["hold"] or two):
            kk = (midi(gs.PALETTE[c["types"][-1]]["m"][-1]) + shift) if two else k
            while kk < 52:
                kk += 12
            while kk > CEIL:
                kk -= 12
            out.append((t, unit * b, "daemons_flute", kk, 0.55 * a))
        else:
            out.append((t, unit * b, "daemons_harp", k, (0.6 if pal["art"] == "^" else 0.9) * a))
        t += unit * b
    return out, pal, unit


def score(notes):
    """What a cry plays: each note's start, length, voice and key. Two cries with one score are heard as one."""
    return tuple((round(t, 4), round(d, 4), v, k) for t, d, v, k, _ in notes)


def rendered(cries):
    """Every cry made, in cry-table order, under THE NO-TWINS RULE: a cry whose score an earlier cry already plays
    takes a tie (its name's first and last notes move to the next choice) until it is its own. Returns [(c, y, notes)]."""
    seen, out = {}, []
    for c in cries:
        c["tie"] = 0
        while True:
            notes = events(c)[0]
            if score(notes) not in seen:
                break
            c["tie"] += 1
            assert c["tie"] < 3, "gencries: %s has no last note left that is its own" % c["name"]
        seen[score(notes)] = c["name"]
        y, notes = make(c)
        out.append((c, y, notes))
    return out


def make(c):
    import numpy as np
    notes, pal, unit = events(c)
    y = np.zeros(int(c["cap"] * SR))
    def put(at, p):
        a = int(at * SR)
        if a < len(y):
            p = p[:len(y) - a]
            y[a:a + len(p)] += p
    for j, (t, d, v, k, a) in enumerate(notes):
        put(t, sampled(v, k, d, a))
        put(t, square(k + 12, min(0.03, d), 0.125 if pal["art"] == "^" else 0.5, 0.18 * a))
        if pal["tex"]:
            put(t, noise(0.12 if pal["tex"] == "s" else 0.06, 0.12 * a, {"x": 40, "s": 12, "X": 18}[pal["tex"]],
                         seed=h(c["name"], 997) + j, color=0.25 if pal["tex"] == "X" else 1.0))
    nz = np.nonzero(np.abs(y) > 0.004)[0]
    y = y[:nz[-1] + 1] if len(nz) else y[:1]
    f = min(len(y), int(0.02 * SR))
    if f:
        y[-f:] *= np.linspace(1, 0, f)
    return y / (np.abs(y).max() or 1) * 0.92, notes


# ---------------------------------------------------------------------------------------------------------------------
# THE THREE CHECKS
# ---------------------------------------------------------------------------------------------------------------------
def checks(c, y, notes):
    import numpy as np
    win = max(1, int(GROWL_S * SR))
    e = np.convolve(y ** 2, np.ones(win) / win, mode="valid") if len(y) > win else np.array([np.mean(y ** 2)])
    loud = e.max() or 1e-9
    bad = []
    cut = y[:int(DOUBLES_S * SR)]
    early = sum(1 for n in notes if n[0] < DOUBLES_S - 0.02)
    if early < 2:
        bad.append("DOUBLES: %d note%s in the first 20 frames" % (early, "" if early == 1 else "s"))
    elif np.mean(cut ** 2) < loud / 8:
        bad.append("DOUBLES: the first 20 frames are %.0f%% of its loudest" % (100 * np.mean(cut ** 2) / loud))
    said = []
    if len(c["types"]) > 1 and notes[-1][2] == "daemons_flute" and notes[-1][0] >= DOUBLES_S - 0.02:
        said.append("doubles: the second type's note comes after the cut")
    tail = y[-win:]
    if np.mean(tail ** 2) < loud / 8:
        bad.append("BACKWARD: the last 15 frames are %.0f%% of its loudest" % (100 * np.mean(tail ** 2) / loud))
    low = min(n[3] for n in notes) - FAINT_SEMIS
    if low < 40:
        bad.append("FAINT: lowest note falls to MIDI %.1f" % low)
    slow = len(y) / SR * 2 ** (FAINT_SEMIS / 12)
    if slow > HOLD_FRAMES * FRAME:
        if c["cap"] * 2 ** (FAINT_SEMIS / 12) > HOLD_FRAMES * FRAME:
            said.append("faint: cut at 140 frames, as pret's is")
        else:
            bad.append("FAINT: %.2f s lowered, past the cry player's 140 frames" % slow)
    return bad, early, "; ".join(said)


# ---------------------------------------------------------------------------------------------------------------------
# The cartridge and the model
# ---------------------------------------------------------------------------------------------------------------------
DPCM = [0, 1, 4, 9, 16, 25, 36, 49, -64, -49, -36, -25, -16, -9, -4, -1]


def pcm8(y):
    import numpy as np
    return (np.clip(np.round(y * 127), -128, 127).astype(int) + 128).astype(np.uint8).tobytes()


def wav8(path, y):
    w = wave.open(path, "wb")
    w.setnchannels(1); w.setsampwidth(1); w.setframerate(SR)
    w.writeframes(pcm8(y))
    w.close()


def undpcm(b, size):
    import numpy as np
    out, p = [], 0
    while len(out) < size and p < len(b):
        s = struct.unpack("b", b[p:p + 1])[0]; out.append(s); p += 1; n, first = 1, True
        while n < 64 and p < len(b):
            byte = b[p]; p += 1
            for nib in ((byte & 15,) if first else (byte >> 4, byte & 15)):
                if n < 64:
                    s = ((s + DPCM[nib] + 128) & 255) - 128; out.append(s); n += 1
            first = False
    return np.array(out[:size], dtype=float) / 128


def cartridge(y, wav_path):
    """Write the 8-bit .wav, compress it as audio_rules.mk does, return (bytes in ROM, the sample decoded back)."""
    wav8(wav_path, y)
    with tempfile.TemporaryDirectory() as td:
        b = os.path.join(td, "c.bin")
        subprocess.run([WAV2AGB, "-b", "-c", "-l", "1", "--no-pad", wav_path, b], check=True, capture_output=True)
        d = open(b, "rb").read()
    size = struct.unpack("<I", d[12:16])[0]
    return len(d), undpcm(d[16:], size)


def pret_sample(c):
    import numpy as np
    blob = subprocess.run(["git", "-C", GBA, "show", "%s:sound/direct_sound_samples/cries/%s.wav" % (PRET_REF, c["file"])],
                          capture_output=True, check=True).stdout
    w = wave.open(io.BytesIO(blob))
    return (np.frombuffer(w.readframes(w.getnframes()), dtype=np.uint8).astype(float) - 128) / 128


def play(x, semis=0.0, frames=None, reverse=False, release=0):
    """The cry player: the sample at key 60 moved `semis`, cut after `frames` with m4a's release, through the mixer."""
    import numpy as np
    if reverse:
        x = x[::-1]
    ratio = 2 ** (semis / 12) * SR / MIX
    n = int(len(x) / ratio)
    m = np.interp(np.arange(n) * ratio, np.arange(len(x)), x) * 12 / 15
    if frames is not None:
        k = int(frames * FRAME * MIX)
        if k < len(m):
            per = int(FRAME * MIX)
            env = np.ones(len(m))
            env[k:] = (release / 256) ** ((np.arange(len(m) - k) // per) + 1) if release else 0
            m = (m * env)[:k + per * 40]
    return m[np.minimum((np.arange(int(len(m) * OUT / MIX)) * MIX / OUT).astype(int), len(m) - 1)]


def mp3(path, y):
    import numpy as np
    os.makedirs(os.path.dirname(path), exist_ok=True)
    wav = path[:-4] + ".tmp.wav"
    w = wave.open(wav, "wb")
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(OUT)
    w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())
    w.close()
    subprocess.run(["lame", "--quiet", "-b", "48", "-m", "m", wav, path], check=True)
    os.remove(wav)


def string(parts, gap=0.5):
    import numpy as np
    total = sum(len(p) / OUT + gap for p in parts) + 0.2
    out, at = np.zeros(int(total * OUT)), 0.15
    for p in parts:
        a = int(at * OUT)
        out[a:a + len(p)] += p[:len(out) - a]
        at += len(p) / OUT + gap
    return out


def sampler(cries):
    """About thirty: three whole lines, a daemon of each of the 17 types not yet heard, the shortest and longest."""
    roots = [c for c in cries if c["species"]]
    pick = []
    for first in LINES:
        pick += sorted([c for c in roots if c["line"] == first], key=lambda c: (c["stage"], c["i"]))
    seen = {c["types"][0] for c in pick}
    for ty in gs.CHART:
        if ty in seen:
            continue
        for c in roots:
            if c["types"][0] == ty and c["name"] not in NOT_SAMPLED and c["species"] not in NOT_SAMPLED \
                    and c not in pick:
                pick.append(c); seen.add(ty)
                break
    extra = sorted(roots, key=lambda c: c["cap"])
    for c in (extra[0], extra[-1]):
        if c not in pick:
            pick.append(c)
    for c in list(pick[len(LINES) * 3:]):                    # then the type's daemon grown up: lower and slower
        if len(pick) >= 30:
            break
        grown = [d for d in roots if d["line"] == c["line"] and d["stage"] > c["stage"] and d["name"] not in NOT_SAMPLED]
        if grown:
            d = max(grown, key=lambda d: d["stage"])
            if d not in pick:
                pick.insert(pick.index(c) + 1, d)
    return pick


# ---------------------------------------------------------------------------------------------------------------------
# T-584: the eleven's slots in the engine -- both cry tables and the sample's label -- and proof each is heard as its own
# ---------------------------------------------------------------------------------------------------------------------
def own_tables():
    """{path: new text} for what the eleven need in the cry tables and direct_sound_data.inc (empty when current)."""
    mine = own()
    names = {o[0] for o in mine}
    out = {}
    t = read("sound/cry_tables.inc")
    new = t
    for macro in ("cry", "cry_reverse"):
        rows = re.findall(r"^\t%s (Cry_\w+)\n" % macro, new, re.M)
        want = [l for l in rows if l not in names] + [o[0] for o in mine]
        m = re.search(r"(^\t%s Cry_\w+\n)+" % macro, new, re.M)
        new = new[:m.start()] + "".join("\t%s %s\n" % (macro, l) for l in want) + new[m.end():]
    if new != t:
        out["sound/cry_tables.inc"] = new
    t = read("sound/direct_sound_data.inc")
    new = t
    for label, f, _, _ in mine:
        new = new.replace('\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/cries/%s.bin"\n' % (label, f), "")
    anchor = 'Cry_Chimecho::\n\t.incbin "sound/direct_sound_samples/cries/chimecho.bin"\n'
    assert new.count(anchor) == 1, "gencries: CHIMECHO's sample is not where the eleven follow it"
    new = new.replace(anchor, anchor + "".join('\n\t.align 2\n%s::\n\t.incbin "sound/direct_sound_samples/cries/%s.bin"\n'
                                               % (label, f) for label, f, _, _ in mine))
    if new != t:
        out["sound/direct_sound_data.inc"] = new
    return out


def borrowers():
    """Every slot SpeciesToCryId sends somewhere other than its own cry: [(daemon, what it plays)]. Reads the two
    tools' tables in src/pokemon.c; a value that is a SPECIES_ is a borrowed cry, a number must be its own row."""
    labels = re.findall(r"^\s*cry (Cry_\w+)", read("sound/cry_tables.inc"), re.M)
    label = {o[2]: o[0] for o in own()}
    bad = []
    for sp, val in re.findall(r"\[SPECIES_(\w+) - SPECIES_OLD_UNOWN_\w\] = (\w+),", read("src/pokemon.c")):
        if not val.isdigit():
            bad.append((sp, val.replace("SPECIES_", "")))
        elif sp not in label or label[sp] not in labels or labels.index(label[sp]) != int(val):
            bad.append((sp, "cry %s" % val))
    for o in own():
        if o[2] not in {sp for sp, _ in re.findall(r"\[SPECIES_(\w+) - SPECIES_OLD_UNOWN_\w\] = (\w+),",
                                                     read("src/pokemon.c"))}:
            bad.append((o[2], "no row in SpeciesToCryId's tables"))
    return bad


def rom_check(rom):
    """Read the BUILT ROM: every daemon's cry, as SpeciesToCryId and gCryTable resolve it, is its own sample, and no
    two samples are the same bytes. Returns a list of failures."""
    sym = {}                                                # the .elf beside the ROM, statics included
    for line in subprocess.run(["arm-none-eabi-nm", os.path.splitext(rom)[0] + ".elf"], capture_output=True,
                               text=True, check=True).stdout.splitlines():
        f = line.split()
        if len(f) == 3:
            sym[f[2]] = int(f[0], 16)
    data = open(rom, "rb").read()
    at = lambda a: a - 0x08000000
    u16 = lambda a: struct.unpack("<H", data[at(a):at(a) + 2])[0]
    u32 = lambda a: struct.unpack("<I", data[at(a):at(a) + 4])[0]
    cries = census()
    n = len(cries)
    bad = []
    fwd = [u32(sym["gCryTable"] + 12 * i + 4) for i in range(n)]
    rev = [u32(sym["gCryTable_Reverse"] + 12 * i + 4) for i in range(n)]
    for c, f, r in zip(cries, fwd, rev):
        if f != sym.get(c["label"]) or r != f:
            bad.append("row %d is not %s" % (c["i"], c["label"]))
    if len(set(fwd)) != n:
        bad.append("%d rows share a sample" % (n - len(set(fwd))))
    ends = sorted(set(fwd) | {sym["DirectSoundWaveData_register_noise"]})
    blobs = {}
    for a, b in zip(ends, ends[1:]):
        blobs.setdefault(data[at(a):at(b)].rstrip(b"\0"), []).append(a)
    twins = [v for v in blobs.values() if len(v) > 1]
    if twins:
        bad.append("%d samples are byte-identical to another" % len(twins))
    species = {}
    for name, val in re.findall(r"#define SPECIES_(OLD_UNOWN_\w)\s+(\d+)", read("include/constants/species.h")):
        species[name] = int(val)
    for tab, first, last in (("sNexusCries", "C", "J"), ("sCarriedCries", "K", "M"), ("sMusaiFormCries", "N", "O")):
        if tab not in sym:
            bad.append("%s is not in the .elf" % tab)
            continue
        for k in range(species["OLD_UNOWN_" + last] - species["OLD_UNOWN_" + first] + 1):
            want = [c for c in cries if c["species"] == "OLD_UNOWN_" + chr(ord(first) + k)]
            got = u16(sym[tab] + 2 * k)
            if not want or got != want[0]["i"]:
                bad.append("%s[%d] plays cry %d" % (tab, k, got))
    return bad, n


# ---------------------------------------------------------------------------------------------------------------------
def run_all(cries, measure=False, wav_dir=None):
    rows = []
    for c, y, notes in rendered(cries):
        bad, early, note = checks(c, y, notes)
        nbytes, q = None, None
        if measure:
            nbytes, q = cartridge(y, os.path.join(wav_dir, c["file"] + ".wav"))
        rows.append(dict(c=c, y=y, notes=notes, bad=bad, early=early, note=note, bytes=nbytes, q=q))
    return rows


def summary(rows):
    fails = [r for r in rows if r["bad"]]
    ours = sum(len(r["y"]) for r in rows) / SR
    pret = sum(r["c"]["cap"] for r in rows)
    print("gencries: %d cries, A shaped by B (DRAFT); ours %.1f s against pret's %.1f s" % (len(rows), ours, pret))
    if rows[0]["bytes"] is not None:
        print("  ROM bytes (wav2agb, as built): ours %d, pret's 1,630,415" % sum(r["bytes"] for r in rows))
    else:
        print("  ROM bytes (estimate, 33 a 64 samples): ours about %d" % int(sum(-(-len(r["y"]) // 64) * 33 + 16
                                                                              for r in rows)))
    for kind in ("DOUBLES", "BACKWARD", "FAINT"):
        hit = [r for r in rows if any(b.startswith(kind) for b in r["bad"])]
        print("  %-8s %3d fail%s" % (kind, len(hit), "" if len(hit) == 1 else "s") +
              (": " + ", ".join("%s (%s)" % (r["c"]["name"], "; ".join(b for b in r["bad"] if b.startswith(kind)))
                                for r in hit) if hit else ""))
    for kind in ("doubles", "faint"):
        said = [r["c"]["name"] for r in rows if kind + ":" in r["note"]]
        if said:
            what = [n for r in rows for n in r["note"].split("; ") if n.startswith(kind)][0]
            print("  said, not failed (%d) -- %s: %s" % (len(said), what, ", ".join(said)))
    borrowed = borrowers()
    print("  borrowers (SpeciesToCryId): " + (", ".join("%s plays %s" % b for b in borrowed) if borrowed else "none"))
    twins = {}
    for r in rows:
        twins.setdefault(score(r["notes"]), []).append(r["c"]["name"])
        twins.setdefault(pcm8(r["y"]), []).append(r["c"]["name"])
    twins = [v for v in twins.values() if len(v) > 1]
    tied = ["%s (tie %d)" % (r["c"]["name"], r["c"]["tie"]) for r in rows if r["c"].get("tie")]
    print("  twins (one score or one sample): " + ("; ".join(" = ".join(v) for v in twins) if twins else "none") +
          (" -- the no-twins rule moved %s" % ", ".join(tied) if tied else ""))
    assert not twins, "gencries: THE NO-TWINS RULE failed"
    return fails


def sheet_text(rows):
    lines = ["T-565 batch 11 -- every cry, A (the type's voice) shaped by B (the name). DRAFT. tools/gencries.py --sheets",
             "", "%-4s %-16s %-11s %-19s %-2s %-11s %6s %6s %6s  %s" %
             ("id", "cry", "daemon", "types", "st", "line", "pret s", "ours s", "bytes", "checks")]
    for r in rows:
        c = r["c"]
        lines.append("%-4d %-16s %-11s %-19s %-2d %-11s %6.3f %6.3f %6s  %s" % (
            c["i"], c["label"][4:], c["name"], "/".join(c["types"]), c["stage"], c["line"], c["cap"],
            len(r["y"]) / SR, r["bytes"] if r["bytes"] is not None else "-",
            "; ".join(r["bad"]) or ("ok" + (" (%s)" % r["note"] if r["note"] else ""))))
    return "\n".join(lines) + "\n"


def main():
    args = sys.argv[1:]

    def arg_after(flag, default):
        i = args.index(flag)
        return args[i + 1] if i + 1 < len(args) and not args[i + 1].startswith("--") else default

    cries = census()
    if "--rom" in args:
        rom = os.path.abspath(arg_after("--rom", os.path.join(GBA, "daemonsContent.gba")))
        bad, n = rom_check(rom)
        print("gencries --rom %s: %d cries, %s" % (os.path.relpath(rom, ROOT), n,
              "every row its own sample, no two alike, the eleven slots each on their own" if not bad else "FAILED"))
        for b in bad:
            print("  !! " + b)
        return 1 if bad else 0
    if "--pret-ref" in args:
        d = os.path.abspath(arg_after("--pret-ref", ""))
        if not d or os.path.commonpath([d, ROOT]) == ROOT:
            sys.exit("gencries: --pret-ref needs a directory outside the repository (pret's cries are retail audio)")
        pick = sampler(cries)
        mp3(os.path.join(d, "pret_sampler.mp3"), string([play(pret_sample(c)) for c in pick]))
        six = [c for n in SIX for c in cries if c["name"] == n]
        mp3(os.path.join(d, "pret_six_doubles_cut.mp3"),
            string([play(pret_sample(c), frames=20, release=225) for c in six], 0.5))
        mp3(os.path.join(d, "pret_six_backwards.mp3"), string([play(pret_sample(c), reverse=True) for c in six]))
        print("gencries: pret's sampler (%d), cut and backwards clips in %s" % (len(pick), d))
        return 0
    drafting = [a for a in ("--draft", "--previews", "--sheets") if a in args]
    if drafting:
        wav_dir = os.path.abspath(arg_after("--draft", os.path.expanduser("~/.cache/daemons/t565_cries_wav"))) if "--draft" in args else \
            tempfile.mkdtemp(prefix="gencries-")
        os.makedirs(wav_dir, exist_ok=True)
        rows = run_all(cries, measure=True, wav_dir=wav_dir)
        summary(rows)
        if "--previews" in args:
            d = os.path.abspath(arg_after("--previews", OUT_DIR))
            for r in rows:
                mp3(os.path.join(d, "cries", "%03d_%s.mp3" % (r["c"]["i"], r["c"]["name"].lower().replace(" ", "_"))),
                    play(r["q"]))
            by = {r["c"]["name"]: r for r in rows}
            pick = sampler(cries)
            mp3(os.path.join(d, "sampler.mp3"), string([play(by[c["name"]]["q"]) for c in pick]))
            mp3(os.path.join(d, "six_doubles_cut.mp3"),
                string([play(by[n]["q"], frames=20, release=225) for n in SIX], 0.5))
            mp3(os.path.join(d, "six_backwards.mp3"), string([play(by[n]["q"], reverse=True) for n in SIX]))
            mp3(os.path.join(d, "six_fainting.mp3"),
                string([play(by[n]["q"], semis=-FAINT_SEMIS, frames=HOLD_FRAMES, release=200) for n in SIX]))
            open(os.path.join(d, "SAMPLER.txt"), "w").write(
                "The sampler, in order (tools/gencries.py --previews). DRAFT.\n" +
                "".join("%2d  %-11s %-19s stage %d of the %s line\n" % (j + 1, c["name"], "/".join(c["types"]),
                                                                      c["stage"], c["line"])
                        for j, c in enumerate(pick)))
            print("  previews: %d cries, the sampler (%d), the six cut, backwards and fainting, in %s"
                  % (len(rows), len(pick), os.path.relpath(d, ROOT) if d.startswith(ROOT) else d))
        if "--sheets" in args:
            d = os.path.abspath(arg_after("--sheets", OUT_DIR))
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, "CRIES.txt"), "w").write(sheet_text(rows))
            try:
                import matplotlib
                matplotlib.use("Agg")
                import matplotlib.pyplot as plt
                by = {r["c"]["name"]: r for r in rows}
                pick = sampler(cries)
                fig, axes = plt.subplots(5, 6, figsize=(18, 11))
                for ax, c in zip(axes.flat, pick):
                    q = by[c["name"]]["q"]
                    ax.specgram(q, NFFT=256, Fs=SR, noverlap=192, cmap="magma")
                    ax.set_title("%s  %s  %.2fs" % (c["name"], "/".join(c["types"]), len(q) / SR), fontsize=8)
                    ax.set_xticks([]); ax.set_yticks([])
                    ax.axvline(DOUBLES_S, color="cyan", lw=0.8)
                for ax in list(axes.flat)[len(pick):]:
                    ax.axis("off")
                plt.tight_layout()
                plt.savefig(os.path.join(d, "sampler.png"), dpi=55)
            except ImportError:
                pass
            print("  sheets: CRIES.txt and sampler.png in %s" % (os.path.relpath(d, ROOT) if d.startswith(ROOT) else d))
        return 0
    if "--write" in args:
        if "--approved" not in args:
            sys.exit("gencries: --write needs --approved (it writes APPROVED, the user's picks)")
        if not APPROVED:
            print("gencries: APPROVED is empty -- nothing is written until the user picks")
            return 0
        for c, y, _ in rendered(cries):
            if APPROVED.get("*") or APPROVED.get(c["label"]):
                path = os.path.join(CRY_DIR, c["file"] + ".wav")
                with tempfile.TemporaryDirectory() as td:
                    wav8(os.path.join(td, "c.wav"), y)
                    want = open(os.path.join(td, "c.wav"), "rb").read()
                if not os.path.exists(path) or open(path, "rb").read() != want:
                    open(path, "wb").write(want)
                    print("  wrote %s" % os.path.relpath(path, ROOT))
        for rel, text in own_tables().items():              # T-584: the eleven's rows and labels
            open(os.path.join(GBA, rel), "w").write(text)
            print("  wrote %s" % os.path.relpath(os.path.join(GBA, rel), ROOT))
        return 0
    # report
    rows = run_all(cries)
    summary(rows)
    print("  APPROVED: %s" % (APPROVED or "none -- nothing is written"))
    if not APPROVED:
        return 0
    drift = []
    for r in rows:
        c = r["c"]
        if APPROVED.get("*") or APPROVED.get(c["label"]):
            with tempfile.TemporaryDirectory() as td:
                wav8(os.path.join(td, "c.wav"), r["y"])
                path = os.path.join(CRY_DIR, c["file"] + ".wav")
                if not os.path.exists(path) or open(os.path.join(td, "c.wav"), "rb").read() != open(path, "rb").read():
                    drift.append(c["file"])
    drift += own_tables()
    if drift:
        print("  !! the engine is not what the approved write makes: %d (%s)" % (len(drift), ", ".join(drift[:16])))
        return 1
    if borrowers():
        print("  !! a daemon still plays another's cry: run tools/gbanexus.py and tools/gbacarried.py with --write")
        return 1
    print("  the engine is current")
    return 0


if __name__ == "__main__":
    sys.exit(main())
