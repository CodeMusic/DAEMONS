#!/usr/bin/env python3
"""T-565 batch 1: the menu and UI sound effects -- three drafts to pick by ear, then ours in place of pret's.

    python3 tools/genuisounds.py                       # report: the twenty sounds, pret's length and ours, APPROVED
    python3 tools/genuisounds.py --draft [DIR]         # each style's .mid files (default audio/drafts/t565_ui)
    python3 tools/genuisounds.py --previews [DIR]      # an .mp3 (or .wav) of every sound in each style, and one
                                                       # "menu session" clip per style (default <draft dir>/previews)
    python3 tools/genuisounds.py --pret-ref DIR        # pret's own twenty and its session, rendered the same way, for
                                                       # comparing by ear -- RETAIL AUDIO: never into a tracked folder
    python3 tools/genuisounds.py --write --approved    # write APPROVED into engineGba (refuses while it is empty)

THE SPLIT (docs/TODO.md T-565, agreed with the Musical Instruments lane 2026-11-16): the menu and UI sounds are the
game lane's; SE_SUCCESS, SE_FAILURE, SE_DING_DONG, SE_PC_LOGIN and SE_SHOP are pitched sounds whose notes are the
instruments lane's, so they are not here. Every sound REPLACES pret's .mid in place: no constant, no song table row.
The only sampled voices are voicegroup193's HARP and FLUTE (tools/geninstruments.py); the rest is the cartridge's own
square and noise channels, as pret's are.

THE THREE STYLES (each sound's notes are written once, in SOUNDS below, and each style voices them):
    A TERMINAL   square-wave blips and a noise tick, like a keyboard: the notes an octave up, on square 1
    B HARP KEYS  one plucked HARP note per note, nothing else: the ticks drop out, a "thin" note is a quiet pluck
    C BOTH       A's squares and ticks held under B's harp (quieter, each square cut to a click), and a held note
                 sung by the FLUTE -- the fanfares' voice C (the user's pick, 2026-11-16) brought to the menus

THE VOICEGROUP: one of its own, VOICEGROUP below, written just before voicegroup193 (geninstruments.py rewrites from
there on), so a sound's midi.cfg line keeps its flags (its -V, -P, -R) and only its -G changes:
    0 HARP   voicegroup193's        1 FLUTE  voicegroup193's
    2 KEY    square 1, 50%, held, a quick release (the shape of pret's own SE_SELECT voice)
    3 THIN   square 1, 12.5%, decaying to nothing (a cursor tick)
    4 BUZZ   square 1, 12.5%, held (the error)
    5 CLICK  square 1, 25%, soft (C's square under the harp)
    6 TICK   noise, a closed tick   7 SHIMMER  noise, the 7-bit (metallic) kind, held

THE TOKENS (time in FRAMES: the MIDI is 150 bpm at 24 ticks a beat, so a tick is a frame, 1/60 s):
    G5:3   a note          ~E6:10  a held note (A: a held square; B: harp; C: flute)
    !E4:6  a buzz (an error; A plays the written key, B and C the harp an octave up)
    ^A5:1  a thin note (a cursor; A: the thin square; B: a quiet pluck)
    x:2    a noise tick    s:20  a noise shimmer    r:4  a rest
Notes are written in the harp's register; A plays them (not buzzes) an octave up. "b" in a sound replaces its notes
for B (and so for C's harp); "a" the same for A.

LENGTH AND LOUDNESS: no sound's last note ends later than pret's (pret's frames are read from its MIDI, not typed),
and none is louder than pret's at its peak: --previews renders pret's MIDI and ours through the same model and
scales a style's velocities down until it is not. --draft runs the same scaling, so a draft .mid is what was heard.
The model (--previews): m4a's mixer at 13379 Hz for the samples, the PSG synthesised with m4a's frame envelopes, the
noise from m4a's own gNoiseTable. A preview, not the GBA; the sweep and the echo are not modelled.
"""
import math, os, re, struct, subprocess, sys, wave

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
MIDI_DIR = os.path.join(GBA, "sound", "songs", "midi")
CFG = os.path.join(MIDI_DIR, "midi.cfg")
VG = os.path.join(GBA, "sound", "voice_groups.inc")
SAMPLES = os.path.join(GBA, "sound", "direct_sound_samples")
DRAFTS = os.path.join(ROOT, "audio", "drafts", "t565_ui")
STYLES = ("A", "B", "C")
STYLE_NAMES = {"A": "TERMINAL", "B": "HARP KEYS", "C": "BOTH"}

# The user's picks: {"select": "C", ...}. --write refuses while it is empty.
APPROVED = {}

VOICEGROUP = 196
MARK_VG = ("voicegroup%03d::  @ T-565 batch 1: the menu and UI sounds -- the HARP and FLUTE over the cartridge's "
           "squares and noise (DAEMONS tools/genuisounds.py)" % VOICEGROUP)
VOICES = [
    "\tvoice_directsound 60, 0, DirectSoundWaveData_daemons_harp, 255, 0, 255, 177",
    "\tvoice_directsound 60, 0, DirectSoundWaveData_daemons_flute, 54, 0, 255, 138",
    "\tvoice_square_1_alt 60, 0, 0, 2, 0, 0, 15, 1",
    "\tvoice_square_1_alt 60, 0, 0, 0, 0, 1, 0, 0",
    "\tvoice_square_1_alt 60, 0, 0, 0, 0, 0, 15, 1",
    "\tvoice_square_1_alt 60, 0, 0, 1, 0, 1, 6, 1",
    "\tvoice_noise_alt 60, 0, 0, 0, 1, 0, 0",
    "\tvoice_noise_alt 60, 0, 1, 0, 0, 15, 1",
]
HARP, FLUTE, KEY, THIN, BUZZ, CLICK, TICK, SHIMMER = range(8)
CH_SAMPLE, CH_SQUARE, CH_NOISE = 0, 1, 2          # three tracks at most: SE1 holds three (music_player_table.inc)
NOISE_KEY = {"x": 80, "s": 70}
TEMPO_US = 400000                                 # 150 bpm, 24 ticks a beat: a tick is a frame
TPQ = 24

# ---------------------------------------------------------------------------------------------------------------------
# THE SOUNDS. what: where the game plays it (docs/sound-census-2026-11-16.md). notes: the shared score.
# ---------------------------------------------------------------------------------------------------------------------
SOUNDS = [
    dict(id="select", what="every confirmation and every cursor step in a menu (477 call sites)",
         notes="G5:3 C6:5", b="C6:6"),
    dict(id="boo", what="the answer is no: a wrong choice, a full bag, a locked thing",
         notes="!F#3:7 r:1 !C3:10"),
    dict(id="click", what="a switch thrown: the PC's boxes, the options, the clock",
         notes="x:2 r:3 E6:3"),
    dict(id="use_item", what="an item used", notes="C5:4 E5:4 G5:4 C6:4 ~E6:10"),
    dict(id="win_open", what="the start menu opening", notes="x:2 E5:3 A5:7"),
    dict(id="pc_off", what="the PC turned off", notes="C6:4 G5:4 E5:4 ~C5:8"),
    dict(id="pc_on", what="the PC turned on", notes="!C4:4 r:2 C5:3 D5:3 E5:3 G5:3 A5:3 C6:3 r:4 G5:4 ~C6:26"),
    dict(id="card_open", what="the trainer card opening",
         notes="C5:3 E5:3 G5:3 C6:3 E6:3 r:2 G6:3 r:2 ~E6:19"),
    dict(id="card_flip", what="the trainer card turned over", notes="s:2 ^C6:1"),
    dict(id="card_flipping", what="the trainer card turning", notes="s:20",
         b="^C5:2 ^E5:2 ^G5:2 ^C6:2 ^E6:2 ^G6:2 r:8"),
    dict(id="bag_pocket", what="the bag's pocket changed", notes="x:1 D6:1"),
    dict(id="bag_cursor", what="the bag's cursor moved", notes="^A5:1"),
    dict(id="rs_shop", what="a sale at the counter", notes="x:2 C6:2 E6:2 r:1 ~G6:20"),
    dict(id="save", what="the game saving",
         notes="C5:2 G5:2 C5:2 G5:2 D5:2 A5:2 D5:2 A5:2 E5:2 G5:2 E5:2 G5:2 r:4 C6:3 ~G6:11"),
    dict(id="rotating_gate", what="a rotating gate turned", notes="!G3:4 x:2 r:4 !C4:4 x:2 r:4"),
    dict(id="dex_scroll", what="the INDEX's list scrolled", notes="^E6:2"),
    dict(id="dex_page", what="the INDEX's page turned", notes="E5:3 A5:7"),
    dict(id="help_open", what="the help screen opening", notes="C5:3 E5:3 G5:3 A5:3 ~C6:17"),
    dict(id="help_close", what="the help screen closing", notes="C6:3 A5:3 G5:3 E5:3 ~C5:17"),
    dict(id="help_error", what="the help screen saying no", notes="!G4:5 r:2 !C#4:10"),
]
APPROVED.update({s["id"]: "C" for s in SOUNDS})   # the user, 2026-11-17, by multiple choice: C BOTH (DRAFT)
LEFT_OUT = ["success", "failure", "ding_dong", "pc_login", "shop"]      # the instruments lane's notes

# The "menu session" clip: (seconds, sound) -- the start menu opened, the cursor moved, the bag, an item, a no, back
# out, save. FRLG plays SE_SELECT for a cursor step and for A and B alike.
SESSION = [(0.00, "win_open"), (0.45, "select"), (0.75, "select"), (1.05, "select"), (1.55, "select"),
           (2.05, "bag_pocket"), (2.35, "bag_cursor"), (2.55, "bag_cursor"), (2.75, "bag_cursor"), (3.20, "select"),
           (3.55, "use_item"), (4.35, "select"), (4.75, "boo"), (5.35, "select"), (5.85, "dex_page"),
           (6.25, "dex_scroll"), (6.40, "dex_scroll"), (6.55, "dex_scroll"), (7.00, "select"), (7.40, "save"),
           (8.40, "select")]
PLAYER = {"select": 2}                             # song_table.inc: every other one here plays on SE1

# velocity by kind and style; C's square layer is quieter than A's
VEL = {"n": 100, "h": 92, "b": 110, "t": 72, "x": 90, "s": 64}
C_SQUARE = 0.9
C_SAMPLE = 0.6

NOTE_RE = re.compile(r"^([~!^]?)([A-G]#?)(-?\d)$")
SEMI = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}


def tokens(score):
    """[(frame, frames, kind, key)] -- kind n h b t x s."""
    out, at = [], 0
    for tok in score.split():
        what, frames = tok.rsplit(":", 1)
        frames = int(frames)
        if what == "r":
            pass
        elif what in ("x", "s"):
            out.append((at, frames, what, NOISE_KEY[what]))
        else:
            m = NOTE_RE.match(what)
            assert m, "bad token %r" % tok
            kind = {"": "n", "~": "h", "!": "b", "^": "t"}[m.group(1)]
            out.append((at, frames, kind, 12 * (int(m.group(3)) + 1) + SEMI[m.group(2)]))
        at += frames
    return out


def voiced(snd, style):
    """[(frame, frames, channel, program, key, velocity)] -- the style's notes, before any loudness scaling."""
    a = tokens(snd.get("a", snd["notes"]))
    b = tokens(snd.get("b", snd["notes"]))
    out = []
    if style in ("A", "C"):
        k = 1.0 if style == "A" else C_SQUARE
        for at, n, kind, key in a:
            if kind in ("x", "s"):
                out.append((at, n, CH_NOISE, TICK if kind == "x" else SHIMMER, key, VEL[kind] * k))
            elif kind == "b":
                out.append((at, n, CH_SQUARE, BUZZ, key, VEL["b"] * k))
            elif style == "A":
                out.append((at, n, CH_SQUARE, THIN if kind == "t" else KEY, key + 12, VEL[kind]))
            else:
                out.append((at, min(n, 2), CH_SQUARE, THIN if kind == "t" else CLICK, key + 12, VEL[kind] * k))
    if style in ("B", "C"):
        k = 1.0 if style == "B" else C_SAMPLE
        for at, n, kind, key in b:
            if kind in ("x", "s"):
                continue
            prog = FLUTE if (style == "C" and kind == "h") else HARP
            out.append((at, n, CH_SAMPLE, prog, key + 12 if kind == "b" else key, VEL[kind] * k))
    return out


def vlq(n):
    out = [n & 0x7F]
    n >>= 7
    while n:
        out.insert(0, (n & 0x7F) | 0x80)
        n >>= 7
    return bytes(out)


def to_midi(notes, scale=1.0):
    """Format 0, one track, a channel per hardware voice; the program set before each note that changes it."""
    ev = [(0, 0, b"\xFF\x51\x03" + struct.pack(">I", TEMPO_US)[1:])]
    for ch in sorted({n[2] for n in notes}):
        ev.append((0, 1, bytes((0xB0 | ch, 7, 127))))
    prog = {}
    for at, n, ch, p, key, vel in sorted(notes):
        if prog.get(ch) != p:
            ev.append((at, 2, bytes((0xC0 | ch, p))))
            prog[ch] = p
        v = max(1, min(127, int(round(vel * scale))))
        ev.append((at, 3, bytes((0x90 | ch, key, v))))
        ev.append((at + n, 0, bytes((0x80 | ch, key, 0))))
    ev.sort(key=lambda e: (e[0], e[1]))
    out, t = bytearray(), 0
    for at, _, data in ev:
        out += vlq(at - t) + data
        t = at
    out += b"\x00\xFF\x2F\x00"
    trk = bytes(out)
    return (b"MThd" + struct.pack(">IHHH", 6, 0, 1, TPQ) + b"MTrk" + struct.pack(">I", len(trk)) + trk)


# ---------------------------------------------------------------------------------------------------------------------
# Reading MIDI (pret's and ours) and pret's side of things
# ---------------------------------------------------------------------------------------------------------------------
def parse_midi(data):
    """-> (seconds per tick, [(tick, kind, ch, a, b)]) with kind on/off/prog/cc/bend, every track merged."""
    _, ntr, tpq = struct.unpack(">HHH", data[8:14])
    i, events, tempo = 14, [], 500000

    def rd(j):
        n = 0
        while True:
            c = data[j]
            j += 1
            n = (n << 7) | (c & 0x7F)
            if c < 0x80:
                return n, j
    for _ in range(ntr):
        ln = struct.unpack(">I", data[i + 4:i + 8])[0]
        j, end, t, rs = i + 8, i + 8 + ln, 0, None
        i = end
        while j < end:
            dt, j = rd(j)
            t += dt
            c = data[j]
            if c == 0xFF:
                ty = data[j + 1]
                ln2, k = rd(j + 2)
                if ty == 0x51:
                    tempo = int.from_bytes(data[k:k + ln2], "big")
                j = k + ln2
                continue
            if c in (0xF0, 0xF7):
                ln2, k = rd(j + 1)
                j = k + ln2
                continue
            if c & 0x80:
                rs = c
                j += 1
            hi, ch = rs & 0xF0, rs & 0x0F
            if hi in (0xC0, 0xD0):
                if hi == 0xC0:
                    events.append((t, "prog", ch, data[j], 0))
                j += 1
                continue
            a, b = data[j], data[j + 1]
            j += 2
            if hi == 0x90 and b:
                events.append((t, "on", ch, a, b))
            elif hi in (0x80, 0x90):
                events.append((t, "off", ch, a, 0))
            elif hi == 0xB0:
                events.append((t, "cc", ch, a, b))
            elif hi == 0xE0:
                events.append((t, "bend", ch, a, b))
    order = {"prog": 0, "cc": 0, "bend": 0, "off": 1, "on": 2}
    events.sort(key=lambda e: (e[0], order[e[1]]))
    return tempo / 1e6 / tpq, events


def last_off_seconds(data):
    spt, ev = parse_midi(data)
    return max([e[0] for e in ev if e[1] == "off"] or [0]) * spt


def peak_velocity(data):
    """The loudest note's velocity x its track volume, both 0..1 -- the MIDI's own measure of how loud it asks to be."""
    _, ev = parse_midi(data)
    vol, best = {}, 0.0
    for t, k, ch, a, b in ev:
        if k == "cc" and a == 7:
            vol[ch] = b
        elif k == "on":
            best = max(best, b / 127 * vol.get(ch, 100) / 127)
    return best


def cfg_line(name):
    t = open(CFG, encoding="utf-8").read()
    m = re.search(r"^(se_%s\.mid:\s*)(.*)$" % re.escape(name), t, re.M)
    return m.group(2).strip() if m else None


def master_of(flags):
    m = re.search(r"-V(\d+)", flags or "")
    return int(m.group(1)) if m else 127


def git_show(path):
    """pret's own copy of an engine file (upstream/master), or None."""
    r = subprocess.run(["git", "-C", GBA, "show", "upstream/master:" + path], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def pret_midi(name):
    data = git_show("sound/songs/midi/se_%s.mid" % name)
    if data is None:
        data = open(os.path.join(MIDI_DIR, "se_%s.mid" % name), "rb").read()
    return data


def pret_flags(name):
    t = git_show("sound/songs/midi/midi.cfg")
    t = t.decode() if t else open(CFG, encoding="utf-8").read()
    m = re.search(r"^se_%s\.mid:\s*(.*)$" % re.escape(name), t, re.M)
    return m.group(1).strip()


_VG_CACHE = {}


def voicegroup(n):
    if n not in _VG_CACHE:
        t = git_show("sound/voice_groups.inc")
        rows = (t.decode() if t else open(VG, encoding="utf-8").read()).split("\n")
        i = next(k for k, r in enumerate(rows) if r.startswith("voicegroup%03d::" % n)) + 1
        out = []
        while i < len(rows) and not rows[i].strip().endswith("::") and not rows[i].strip().startswith(".align"):
            if rows[i].strip() and not rows[i].strip().startswith(".include"):
                out.append(rows[i].strip())
            i += 1
        _VG_CACHE[n] = out
    return _VG_CACHE[n]


# ---------------------------------------------------------------------------------------------------------------------
# The model: m4a's mixer for the samples, the PSG synthesised, both a frame at a time
# ---------------------------------------------------------------------------------------------------------------------
SR = 32768
MIX = 13379
FRAME = 1 / 59.7275
DS_GAIN = 12 / 15            # m4aSoundInit's master volume 12 of 15 (src/m4a.c)
PSG_GAIN = 0.25              # one PSG channel at full against a full-scale sample (GBA: 4 channels ~ one DMA channel)
NOISE_TABLE = [0xD7, 0xD6, 0xD5, 0xD4, 0xC7, 0xC6, 0xC5, 0xC4, 0xB7, 0xB6, 0xB5, 0xB4, 0xA7, 0xA6, 0xA5, 0xA4,
               0x97, 0x96, 0x95, 0x94, 0x87, 0x86, 0x85, 0x84, 0x77, 0x76, 0x75, 0x74, 0x67, 0x66, 0x65, 0x64,
               0x57, 0x56, 0x55, 0x54, 0x47, 0x46, 0x45, 0x44, 0x37, 0x36, 0x35, 0x34, 0x27, 0x26, 0x25, 0x24,
               0x17, 0x16, 0x15, 0x14, 0x07, 0x06, 0x05, 0x04, 0x03, 0x02, 0x01, 0x00]   # src/m4a_tables.c
_SAMPLE_CACHE = {}


def load_sample(label):
    import numpy as np
    if label not in _SAMPLE_CACHE:
        d = open(os.path.join(SAMPLES, label.replace("DirectSoundWaveData_", "") + ".bin"), "rb").read()
        flags, freq, loop, size = struct.unpack("<IIII", d[:16])
        x = np.frombuffer(d[16:16 + size + 1], dtype=np.int8).astype(float) / 128
        _SAMPLE_CACHE[label] = (x, freq / 1024, loop if flags & 0x40000000 else None)
    return _SAMPLE_CACHE[label]


def parse_voice(line):
    m = re.match(r"(voice_\w+)\s+(.*)$", line.strip())
    kind, args = m.group(1), [a.strip() for a in m.group(2).split(",")]
    return kind, args


def render_note(voice, key, vel, sec):
    """One note of `sec` seconds held, velocity 0..1 (velocity x volume x master), with its release."""
    import numpy as np
    kind, a = parse_voice(voice)
    if kind.startswith("voice_directsound"):
        x, rate, loop = load_sample(a[2])
        att, dec, sus, rel = (int(v) for v in a[3:7])
        fixed = "no_resample" in kind
        step = (rate if fixed else rate * 2 ** ((key - 60) / 12)) / MIX
        frames = int(sec / FRAME) + 1
        env, levels, released, f = 0 if att < 255 else 255, [], False, 0
        phase = "attack" if att < 255 else "decay"
        while True:
            if f >= frames and not released:
                released = True
            if released:
                env = env * rel >> 8 if rel else 0
                if env <= 0 or len(levels) > frames + 600:
                    break
            elif phase == "attack":
                env = min(255, env + att)
                if env >= 255:
                    phase = "decay"
            elif phase == "decay":
                env = max(sus, env * dec >> 8) if env > sus else sus
                if env <= sus:
                    env = sus
                    phase = "sustain"
            levels.append(env)
            f += 1
        n = int(len(levels) * FRAME * MIX)
        pos = np.arange(n) * step
        if loop is not None:
            over = pos >= len(x) - 1
            pos[over] = loop + np.mod(pos[over] - loop, len(x) - 1 - loop)
        pos = pos[pos < len(x) - 1]
        y = x[pos.astype(int)]
        envs = np.repeat(np.array(levels, float) / 255, int(round(FRAME * MIX)) + 1)[:len(y)]
        y = y[:len(envs)] * envs * vel * DS_GAIN
        return y[(np.arange(int(len(y) * SR / MIX)) * MIX / SR).astype(int)]
    # PSG: m4a's envelope counts 0..15, a step every N frames
    if kind.startswith("voice_square"):
        sq1 = kind.startswith("voice_square_1")
        duty = [0.125, 0.25, 0.5, 0.75][int(a[3 if sq1 else 2]) & 3]
        att, dec, sus, rel = (int(v) for v in (a[4:8] if sq1 else a[3:7]))
    elif kind.startswith("voice_noise"):
        period = int(a[2])
        att, dec, sus, rel = (int(v) for v in a[3:7])
    else:                                                          # programmable wave: a triangle stands in
        att, dec, sus, rel = (int(v) for v in a[3:7])
    goal = max(0, min(15, int(round(vel * 15))))
    target_sus = (goal * sus + 15) >> 4 if sus < 15 else goal
    frames = int(sec / FRAME) + 1
    env, phase, levels, f, cnt = (0 if att else goal), ("attack" if att else "decay"), [], 0, 0
    while True:
        cnt += 1
        if f >= frames:
            if not rel:
                break
            if cnt >= rel:
                env, cnt = env - 1, 0
            if env <= 0 or len(levels) > frames + 600:
                break
        elif phase == "attack":
            if cnt >= att:
                env, cnt = env + 1, 0
            if env >= goal:
                env, phase = goal, "decay"
        elif phase == "decay":
            if env <= target_sus:
                env, phase = target_sus, "sustain"
            elif not dec:
                env, phase = target_sus, "sustain"
            elif cnt >= dec:
                env, cnt = env - 1, 0
        levels.append(max(0, env))
        f += 1
    n = int(len(levels) * FRAME * SR)
    t = np.arange(n) / SR
    if kind.startswith("voice_square"):
        hz = 440 * 2 ** ((key - 69) / 12)
        y = np.where(np.mod(hz * t, 1) < duty, 1.0, -1.0)
    elif kind.startswith("voice_noise"):
        nr43 = NOISE_TABLE[max(0, min(59, int(round(key)) - 21))]
        s, r = nr43 >> 4, nr43 & 7
        clock = 524288 / (r or 0.5) / 2 ** (s + 1)
        width = 7 if period else 15
        steps = int(n * clock / SR) + 2
        lfsr, bits = (1 << width) - 1, np.empty(steps)
        for k in range(min(steps, 400000)):
            bit = (lfsr ^ (lfsr >> 1)) & 1
            lfsr = (lfsr >> 1) | (bit << (width - 1))
            bits[k] = 1.0 if lfsr & 1 else -1.0
        y = bits[np.minimum((t * clock).astype(int), min(steps, 400000) - 1)]
    else:
        hz = 440 * 2 ** ((key - 69) / 12)
        y = 1 - 2 * np.abs(2 * np.mod(hz * t, 1) - 1)
    envs = np.repeat(np.array(levels, float) / 15, int(round(FRAME * SR)) + 1)[:n]
    return y[:len(envs)] * envs * PSG_GAIN


def render(midi_bytes, voices, master=127):
    """The whole sound, mono floats at SR. A PSG note ends the one before it on the same hardware channel (there is
    one square 1, one square 2, one wave, one noise); a sample's notes ring over each other, as m4a's do. A volume
    change during a note (pret's swells) is followed."""
    import numpy as np
    spt, ev = parse_midi(midi_bytes)
    prog, vol, bend, on = {}, {}, {}, {}
    vol_at = {}                                    # ch -> [(tick, volume)]
    notes = []
    for t, k, ch, a, b in ev:
        if k == "prog":
            prog[ch] = a
        elif k == "cc" and a == 7:
            vol[ch] = b
            vol_at.setdefault(ch, []).append((t, b))
        elif k == "bend":
            bend[ch] = ((b << 7 | a) - 8192) / 8192 * 2
        elif k in ("on", "off") and (ch, a) in on:
            t0, v, p, vl, bd = on.pop((ch, a))
            notes.append((t0, t - t0, ch, a + bd, v, vl, p))
        if k == "on":
            on[(ch, a)] = (t, b, prog.get(ch, 0), vol.get(ch, 100), bend.get(ch, 0))
    end = max([e[0] for e in ev] or [0])
    for (ch, a), (t0, v, p, vl, bd) in on.items():
        notes.append((t0, max(1, end - t0), ch, a + bd, v, vl, p))
    if not notes:
        return np.zeros(1)

    def hw(p):
        kind = parse_voice(voices[p])[0]
        for name in ("square_1", "square_2", "programmable_wave", "noise"):
            if kind.startswith("voice_" + name):
                return name
        return None
    parts = []
    for t0, dt, ch, key, v, vl, p in sorted(notes):
        y = render_note(voices[p], key, v / 127 * vl / 127 * master / 127, dt * spt)
        changes = [(tt, vv) for tt, vv in vol_at.get(ch, []) if t0 < tt]
        if changes and vl:
            g = np.ones(len(y))
            for tt, vv in changes:
                g[int((tt - t0) * spt * SR):] = vv / vl
            y = y * g
        parts.append([int(t0 * spt * SR), y, hw(p)])
    for k, part in enumerate(parts):
        if part[2] is None:
            continue
        nxt = next((q[0] for q in parts[k + 1:] if q[2] == part[2] and q[0] > part[0]), None)
        if nxt is not None:
            part[1] = part[1][:nxt - part[0]]
    mix = np.zeros(max(i + len(y) for i, y, _ in parts) + 1)
    for i, y, _ in parts:
        mix[i:i + len(y)] += y
    return mix


# ---------------------------------------------------------------------------------------------------------------------
# What a draft is: the notes, scaled so the model never hears it louder than pret's
# ---------------------------------------------------------------------------------------------------------------------
def our_voices():
    return [v.strip() for v in VOICES]


def pret_render(name):
    flags = pret_flags(name)
    g = int(re.search(r"-G(\d+)", flags).group(1))
    return render(pret_midi(name), voicegroup(g), master_of(flags))


def drafted(snd, style, pret_peak=None):
    """-> (midi bytes, scale). With pret's peak, the velocities come down until the model is not louder."""
    import numpy as np
    notes = voiced(snd, style)
    master = master_of(pret_flags(snd["id"]))
    scale = 1.0
    if pret_peak is not None:
        for _ in range(12):
            peak = np.abs(render(to_midi(notes, scale), our_voices(), master)).max()
            if peak <= pret_peak * 1.0001:
                break
            scale *= min(0.97, pret_peak / peak)
    return to_midi(notes, scale), scale


def all_drafts(verbose=False):
    import numpy as np
    out = {}
    for snd in SOUNDS:
        pp = np.abs(pret_render(snd["id"])).max()
        for st in STYLES:
            data, scale = drafted(snd, st, pp)
            out[(snd["id"], st)] = (data, scale, pp)
    return out


# ---------------------------------------------------------------------------------------------------------------------
# Modes
# ---------------------------------------------------------------------------------------------------------------------
def frames_of(data):
    return int(round(last_off_seconds(data) * 60))


def check_lengths():
    """Every style's last note ends no later than pret's (to the frame)."""
    bad = []
    for snd in SOUNDS:
        pret = frames_of(pret_midi(snd["id"]))
        for st in STYLES:
            ours = frames_of(to_midi(voiced(snd, st)))
            if ours > pret:
                bad.append("%s %s: %d frames, pret's %d" % (snd["id"], st, ours, pret))
    return bad


def write_wav_or_mp3(path_noext, y):
    import numpy as np
    y = np.clip(y, -1, 1)
    wav = path_noext + ".wav"
    w = wave.open(wav, "wb")
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((y * 32767).astype(np.int16).tobytes())
    w.close()
    lame = subprocess.run(["which", "lame"], capture_output=True, text=True).stdout.strip()
    if lame:
        subprocess.run([lame, "--quiet", "-b", "96", "-m", "m", wav, path_noext + ".mp3"], check=True)
        os.remove(wav)
        return path_noext + ".mp3"
    return wav


def session_mix(get):
    """The menu session: each sound placed at its time; a sound cuts the one before it on the same player."""
    import numpy as np
    clips = [(int(t * SR), PLAYER.get(name, 1), get(name)) for t, name in SESSION]
    total = max(i + len(y) for i, _, y in clips) + SR // 4
    mix = np.zeros(total)
    for k, (i, player, y) in enumerate(clips):
        nxt = next((j for j, p, _ in clips[k + 1:] if p == player), None)
        y = y.copy()
        if nxt is not None and i + len(y) > nxt:
            y = y[:nxt - i]
            fade = min(len(y), int(0.004 * SR))
            if fade:
                y[-fade:] *= np.linspace(1, 0, fade)
        mix[i:i + len(y)] += y
    return mix


def previews(outdir):
    import numpy as np
    drafts = all_drafts()
    written = []
    for st in STYLES:
        d = os.path.join(outdir, st)
        os.makedirs(d, exist_ok=True)
        cache = {}
        for snd in SOUNDS:
            data, scale, pp = drafts[(snd["id"], st)]
            y = render(data, our_voices(), master_of(pret_flags(snd["id"])))
            cache[snd["id"]] = y
            written.append(write_wav_or_mp3(os.path.join(d, "se_%s" % snd["id"]), np.concatenate([y, np.zeros(SR // 8)])))
        written.insert(0, write_wav_or_mp3(os.path.join(outdir, "menu_session_%s_%s" % (st, STYLE_NAMES[st].replace(" ", "_"))),
                                           session_mix(lambda n: cache[n])))
    print("  previews: %d files in %s" % (len(written), outdir))
    return written


def pret_ref(outdir):
    import numpy as np
    real = os.path.realpath(outdir)
    if real.startswith(os.path.realpath(ROOT) + os.sep):
        r = subprocess.run(["git", "-C", ROOT, "check-ignore", "-q", real], capture_output=True)
        if r.returncode != 0:
            sys.exit("genuisounds: --pret-ref renders retail audio; give it a folder outside the repository or an ignored one")
    os.makedirs(outdir, exist_ok=True)
    cache = {snd["id"]: pret_render(snd["id"]) for snd in SOUNDS}
    for name, y in cache.items():
        write_wav_or_mp3(os.path.join(outdir, "se_%s" % name), np.concatenate([y, np.zeros(SR // 8)]))
    write_wav_or_mp3(os.path.join(outdir, "menu_session_pret"), session_mix(lambda n: cache[n]))
    print("  pret's reference: %d sounds and the session in %s (retail audio: keep it out of git)" % (len(cache), outdir))


def draft(outdir):
    drafts = all_drafts()
    for st in STYLES:
        d = os.path.join(outdir, st)
        os.makedirs(d, exist_ok=True)
        for snd in SOUNDS:
            open(os.path.join(d, "se_%s.mid" % snd["id"]), "wb").write(drafts[(snd["id"], st)][0])
    open(os.path.join(outdir, "voicegroup%03d.inc" % VOICEGROUP), "w").write(MARK_VG + "\n" + "\n".join(VOICES) + "\n")
    rows = ["# T-565 batch 1 drafts (tools/genuisounds.py --draft): style, sound, pret's frames, ours, velocity scale",
            "# A %s / B %s / C %s" % tuple(STYLE_NAMES[s] for s in STYLES)]
    for snd in SOUNDS:
        pret = frames_of(pret_midi(snd["id"]))
        rows.append("%-14s pret %2d  " % (snd["id"], pret) + "  ".join(
            "%s %2d x%.2f" % (st, frames_of(drafts[(snd["id"], st)][0]), drafts[(snd["id"], st)][1]) for st in STYLES))
    open(os.path.join(outdir, "LENGTHS.txt"), "w").write("\n".join(rows) + "\n")
    print("  drafts: %d sounds x %d styles in %s" % (len(SOUNDS), len(STYLES), outdir))


def engine_target():
    """{path: bytes or text} the approved write makes, from the committed drafts (what was heard)."""
    out = {}
    for name, st in sorted(APPROVED.items()):
        src = os.path.join(DRAFTS, st, "se_%s.mid" % name)
        out[os.path.join(MIDI_DIR, "se_%s.mid" % name)] = open(src, "rb").read()
    cfg = open(CFG, encoding="utf-8").read()
    for name in APPROVED:
        cfg = re.sub(r"^(se_%s\.mid:.*?)-G\d+" % re.escape(name), r"\g<1>-G%d" % VOICEGROUP, cfg, flags=re.M)
    out[CFG] = cfg
    vg = open(VG, encoding="utf-8").read()
    block = MARK_VG + "\n" + "\n".join(VOICES) + "\n\n\t.align 2\n"      # the .align before it is 193's own
    if re.search(r"^voicegroup%03d::" % VOICEGROUP, vg, re.M):
        vg = re.sub(r"^voicegroup%03d::.*?\n\n\t\.align 2\n" % VOICEGROUP, lambda m: block, vg, count=1,
                    flags=re.M | re.S)
    else:
        i = vg.index("voicegroup193::")
        vg = vg[:i] + block + vg[i:]
    out[VG] = vg
    return out


def main():
    args = sys.argv[1:]

    def arg_after(flag, default):
        i = args.index(flag)
        return args[i + 1] if i + 1 < len(args) and not args[i + 1].startswith("--") else default

    bad = check_lengths()
    if bad:
        sys.exit("genuisounds: longer than pret's: " + "; ".join(bad))
    if "--draft" in args:
        draft(os.path.abspath(arg_after("--draft", DRAFTS)))
    if "--previews" in args:
        previews(os.path.abspath(arg_after("--previews", os.path.join(DRAFTS, "previews"))))
    if "--pret-ref" in args:
        pret_ref(os.path.abspath(arg_after("--pret-ref", "")))
    if any(a in args for a in ("--draft", "--previews", "--pret-ref")):
        return 0
    if "--write" in args:
        if "--approved" not in args:
            sys.exit("genuisounds: --write needs --approved (it writes APPROVED, the user's picks)")
        if not APPROVED:
            print("genuisounds (T-565 batch 1): APPROVED is empty -- nothing is written until the user picks")
            return 0
        for path, want in engine_target().items():
            mode = "wb" if isinstance(want, bytes) else "w"
            have = open(path, "rb" if mode == "wb" else "r").read() if os.path.exists(path) else None
            if have != want:
                open(path, mode).write(want)
                print("  wrote %s" % os.path.relpath(path, ROOT))
        return 0
    # report
    print("genuisounds (T-565 batch 1): %d menu and UI sounds in three styles; the instruments lane's %s left out"
          % (len(SOUNDS), ", ".join(LEFT_OUT)))
    for snd in SOUNDS:
        pret = frames_of(pret_midi(snd["id"]))
        ours = [frames_of(to_midi(voiced(snd, st))) for st in STYLES]
        print("    se_%-14s pret %2d frames (%.3fs)   A %2d  B %2d  C %2d   %s"
              % (snd["id"], pret, pret / 60, ours[0], ours[1], ours[2], APPROVED.get(snd["id"], "")))
    print("  APPROVED: %s" % (APPROVED or "none -- nothing is written"))
    if not APPROVED:
        return 0
    drift = [os.path.relpath(p, ROOT) for p, want in engine_target().items()
             if (open(p, "rb").read() if isinstance(want, bytes) else open(p).read()) != want]
    if drift:
        print("  !! the engine is not what the approved write makes: %s" % ", ".join(drift))
        return 1
    print("  the engine is current")
    return 0


if __name__ == "__main__":
    sys.exit(main())
