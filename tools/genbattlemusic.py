#!/usr/bin/env python3
"""T-565 batch 2: the battle music -- ours, in place of pret's nine.

    python3 tools/genbattlemusic.py            # report: is the engine current
    python3 tools/genbattlemusic.py --write    # write it into engineGba

THE VOICE (the user, 2026-11-17, by multiple choice from three drafts of one set of notes -- C as the fanfares, B the
cartridge alone, D C with drums of our own -- "C As the fanfares", and "All nine"): genfanfares.py's voicegroup195,
our HARP and FLUTE on the tunes and the cartridge under them. Its programs, as these use them:
    0 HARP   lead: the tune, plucked          1 FLUTE   sing: the tune, held
    9 SQ1    arp: the chord broken, plucked   4 SQ2     harm: a second line, plucked
    5 WAVE   bass                             6 7 8 NOISE  h s c, and 7 again, low (key 30), for the kick (k)

ONE RULE runs through all nine (vision 7.9, T-559): a battle against a person is at 128, the tempo the human songs
share; against a daemon it is not (the wild at 160, the myths at 132), and S.T.A.R.R. starts at 110, its sleeping
tempo, and wakes to 128. CONTAINMENT (7.13) holds: S.T.A.R.R.'s hook is the only character's hook here, and its slot
plays for nothing else. Each piece's own reason is its "why" below.

WHAT IT WRITES (engineGba/)
    sound/songs/midi/mus_vs_wild.mid and the eight others, each over pret's in place (format 0, 24 ticks a beat, the
                                      loop marked [ and ]), so no constant moves; GetBattleBGM, battle_setup.c and
                                      battle_main.c are untouched -- which battle plays which slot is the game lane's
    sound/songs/midi/midi.cfg         each of the nine's -G to 195 (genfanfares.py writes voicegroup195 itself)
Every note DRAFT.
"""
import os, re, struct, sys

import genfanfares as G

NAMES, TPB, MIDI_DIR, CFG, GBA = G.NAMES, G.TPB, G.MIDI_DIR, G.CFG, G.GBA
midi = G.midi_note
PERC = ("h", "s", "c", "k")
VOICEGROUP = G.VOICEGROUP
ARP_VOICE = 9
# role -> (MIDI channel, program, track volume, velocity), as genfanfares.CHANNELS where the two share a role; the arp
# borrows the pads' channel (no piece here has a pad), the kick takes the tenth
CH = {"lead": (0, 0, 100, 100), "sing": (1, 1, 100, 96), "arp": (2, ARP_VOICE, 44, 100), "harm": (4, 4, 56, 100),
      "bass": (5, 5, 100, 100), "h": (6, 6, 70, 100), "s": (7, 7, 80, 100), "c": (8, 8, 50, 100), "k": (9, 7, 90, 100)}
NOISE_KEY = {"h": 84, "s": 62, "c": 90, "k": 30}
GATE = {"lead": 0.95, "sing": 0.95, "arp": 0.9, "harm": 0.92, "bass": 0.9}     # as the drafts were heard
BGM_TRACKS = G.PLAYER_TRACKS[0]

# ---------------------------------------------------------------------------------------------------------------------
# Notation: NOTE:BEATS, NOTE+NOTE:BEATS, r:BEATS; k s h c for the noise. Helpers build the repeating parts.
# ---------------------------------------------------------------------------------------------------------------------
def nn(m):
    return NAMES[m % 12] + str(m // 12 - 1)

def beats_of(tokens):
    return sum(float(eval(t.rsplit(":", 1)[1], {})) for t in tokens.split())

def rep(s, n):
    return " ".join([s] * n)

def cat(*parts):
    return " ".join(p for p in parts if p)

def rest(b):
    return "r:%g" % b

def pattern(roots, pat):
    """roots: 'E2 E2 C2' or [(root, beats)]; pat: [(semitones, beats)] repeated to fill each root's beats."""
    if isinstance(roots, str):
        roots = [(r, None) for r in roots.split()]
    out = []
    for r, span in roots:
        m = midi(r)
        span = span if span is not None else sum(b for _, b in pat)
        t, k = 0.0, 0
        while t < span - 1e-9:
            off, b = pat[k % len(pat)]
            b = min(b, span - t)
            out.append("%s:%g" % (nn(m + off), b) if off is not None else rest(b))
            t += b; k += 1
    return " ".join(out)

def arp(chords, idx, step):
    """chords: [('E4+B3+G3', beats)]: the chord's notes in idx order, one every step."""
    out = []
    for ch, span in chords:
        ns = ch.split("+")
        t, k = 0.0, 0
        while t < span - 1e-9:
            out.append("%s:%g" % (ns[idx[k % len(idx)]], step))
            t += step; k += 1
    return " ".join(out)

def cycle(notes, n, step, phase=0):
    return " ".join("%s:%g" % (notes[(i + phase) % len(notes)], step) for i in range(n))

def transpose(tokens, semis):
    out = []
    for tok in tokens.split():
        what, b = tok.rsplit(":", 1)
        if what == "r" or what in PERC:
            out.append(tok)
        else:
            out.append("+".join(nn(midi(n) + semis) for n in what.split("+")) + ":" + b)
    return " ".join(out)

def dia(tokens, scale, k):
    """Shift a line k steps along a seven-note scale (scale: pitch-class names), for parallel thirds."""
    pcs = sorted(NAMES.index(n) if n in NAMES else midi(n + "0") % 12 for n in scale.split())
    out = []
    for tok in tokens.split():
        what, b = tok.rsplit(":", 1)
        if what == "r" or what in PERC:
            out.append(tok); continue
        ns = []
        for n in what.split("+"):
            m = midi(n); o, pc = divmod(m, 12)
            if pc not in pcs:
                raise SystemExit("dia: %s is not in the scale %s" % (n, scale))
            j = pcs.index(pc) + k
            ns.append(nn(o * 12 + pcs[j % 7] + 12 * (j // 7)))
        out.append("+".join(ns) + ":" + b)
    return " ".join(out)

def S(label, n, **roles):
    """A section n beats long; every role must fill it exactly."""
    for r, tok in roles.items():
        b = beats_of(tok)
        if abs(b - n) > 1e-6:
            raise SystemExit("%s: %s is %g beats, want %g" % (label, r, b, n))
    return (n, roles)

def join(*secs):
    roles = []
    for _, rs in secs:
        for r in rs:
            if r not in roles:
                roles.append(r)
    return [(r, " ".join(rs.get(r, rest(n)) for n, rs in secs)) for r in roles]


# ---------------------------------------------------------------------------------------------------------------------
# Drum bars
# ---------------------------------------------------------------------------------------------------------------------
ROCK = "k:0.5 h:0.5 s:0.5 h:0.5 k:0.5 k:0.5 s:0.5 h:0.5"
ROCK_C = "c:0.5 h:0.5 s:0.5 h:0.5 k:0.5 k:0.5 s:0.5 h:0.5"
STRAIGHT = "k:0.5 h:0.5 s:0.5 h:0.5 k:0.5 h:0.5 s:0.5 h:0.25 h:0.25"
STRAIGHT_C = "c:0.5 h:0.5 s:0.5 h:0.5 k:0.5 h:0.5 s:0.5 h:0.25 h:0.25"
HALF = "k:0.5 h:0.5 h:0.5 h:0.5 s:0.5 h:0.5 h:0.5 k:0.5"
HALF_C = "c:0.5 h:0.5 h:0.5 h:0.5 s:0.5 h:0.5 h:0.5 k:0.5"
EIGHTS = "k:0.5 h:0.5 s:0.5 h:0.5 k:0.5 h:0.5 s:0.5 h:0.5"
EIGHTS_C = "c:0.5 h:0.5 s:0.5 h:0.5 k:0.5 h:0.5 s:0.5 h:0.5"
SIXTEENS = "k:0.5 h:0.25 h:0.25 s:0.5 h:0.25 h:0.25 k:0.5 h:0.25 h:0.25 s:0.5 h:0.25 h:0.25"
SIXTEENS_C = "c:0.5 h:0.25 h:0.25 s:0.5 h:0.25 h:0.25 k:0.5 h:0.25 h:0.25 s:0.5 h:0.25 h:0.25"
POP = "k:0.5 h:0.25 h:0.25 s:0.5 h:0.25 h:0.25 k:0.5 k:0.5 s:0.5 h:0.5"
POP_C = "c:0.5 h:0.25 h:0.25 s:0.5 h:0.25 h:0.25 k:0.5 k:0.5 s:0.5 h:0.5"
LIGHT = "k:1 h:0.5 h:0.5 s:1 h:0.5 h:0.5"
LIGHT_C = "c:1 h:0.5 h:0.5 s:1 h:0.5 h:0.5"
STATELY = "k:1 h:1 s:1 h:1"
STATELY_C = "c:1 h:1 s:1 h:1"
FILL = "k:0.5 h:0.5 s:0.5 h:0.5 s:0.25 s:0.25 s:0.25 s:0.25 s:0.5 s:0.5"
FILL_LIGHT = "k:1 h:0.5 h:0.5 s:0.5 s:0.5 s:0.5 s:0.5"
ROLL = "s:0.25 s:0.25 s:0.25 s:0.25 s:0.25 s:0.25 s:0.25 s:0.25 s:0.5 s:0.5 s:0.5 s:0.5"

def drums(first, groove, fill, bars=8):
    return cat(first, rep(groove, bars - 2), fill)

# ---------------------------------------------------------------------------------------------------------------------
# THE PIECES
# ---------------------------------------------------------------------------------------------------------------------
PIECES = []

# ---- 1. VS_WILD ------------------------------------------------------------------------------------------------------
_W_A = ("E5:0.5 r:0.5 E5:0.5 G5:0.5 B5:1 A5:0.5 G5:0.5  F#5:1 E5:0.5 D5:0.5 E5:2 "
        "C5:0.5 r:0.5 C5:0.5 E5:0.5 G5:1 A5:0.5 E5:0.5  D5:1 F#5:1 A5:1 G5:0.5 F#5:0.5 "
        "E5:0.5 r:0.5 E5:0.5 G5:0.5 B5:1 D6:0.5 B5:0.5  C6:1 B5:0.5 A5:0.5 B5:2 "
        "G5:0.5 A5:0.5 G5:0.5 E5:0.5 C5:1 E5:1  D5:1 E5:0.5 F#5:0.5 A5:1 F#5:1")
_W_BASS = [(0, 0.5), (0, 0.5), (12, 0.5), (0, 0.5), (0, 0.5), (0, 0.5), (12, 0.5), (0, 0.5)]
PIECES.append(dict(
    id="VS_WILD", slot="MUS_VS_WILD", bpm=160, meter=4,
    what="every wild battle: the single most-heard piece in the game",
    why="An UNBOUND daemon is a background process that runs unattended (1), so under the tune runs a figure that keeps its own "
        "time: three notes, E B G, against a four-beat bar. It crosses the bar line and only comes back into step every "
        "third bar, and it never changes its notes while the harmony moves under it (E minor, C, D, A minor). At 160, "
        "not the people's 128 (7.9): this is not a person.",
    intro=join(S("wild intro", 8, lead=rest(8), bass=pattern("E2 E2", _W_BASS),
                 arp=cycle(["E4", "B3", "G3"], 16, 0.5, phase=2), perc=cat(rep("k:1", 4), ROLL))),
    loop=join(
        S("wild A", 32, lead=_W_A, bass=pattern("E2 E2 C2 D2 E2 E2 C2 D2", _W_BASS), perc=drums(ROCK_C, ROCK, FILL)),
        S("wild B", 32, sing="A5:3 G5:1 E5:2 C5:2 G5:3 E5:1 D5:2 E5:2 B5:3 A5:1 G5:2 E5:2 F#5:2 A5:2 F#5:4",
          bass=pattern("A2 A2 C2 C2 E2 E2 D2 D2", _W_BASS), perc=drums(ROCK_C, ROCK, FILL)),
        S("wild A'", 32, lead=_W_A, sing="G4:4 B4:4 G4:4 F#4:4 G4:4 B4:4 C5:4 A4:4",
          bass=pattern("E2 E2 C2 D2 E2 E2 C2 D2", _W_BASS), perc=drums(ROCK_C, ROCK, FILL)),
    ) + [("arp", cycle(["E4", "B3", "G3"], 192, 0.5))],
))

# ---- 2. VICTORY_WILD -------------------------------------------------------------------------------------------------
_VW_CH = ["E", "A", "E", "B", "E", "A", "B", "E"]
_VW_ARP = {"E": "E4+B3+G#3", "A": "E4+C#4+A3", "B": "F#4+D#4+B3"}
PIECES.append(dict(
    id="VICTORY_WILD", slot="MUS_VICTORY_WILD", bpm=132, meter=4,
    what="after every wild win (follows VS_WILD)",
    why="The wild battle's three-note figure gains a fourth note and now lands on the bar line every bar, and E minor "
        "has turned to E major.",
    intro=join(S("vw intro", 4, lead="B3:0.5 E4:0.5 G#4:0.5 B4:0.5 E5:2", bass="r:2 E2:2",
                 perc="s:0.25 s:0.25 s:0.25 s:0.25 s:0.5 s:0.5 c:2")),
    loop=join(S("vw loop", 32,
        lead="E5:0.5 G#5:0.5 B5:1 G#5:1 E5:1  A5:1 C#6:1 B5:1 A5:1  G#5:1.5 F#5:0.5 E5:2  F#5:1 D#5:1 B4:2 "
             "E5:0.5 G#5:0.5 B5:1 G#5:1 E5:1  C#6:1 B5:1 A5:1 C#6:1  B5:1.5 A5:0.5 F#5:1 D#5:1  E5:4",
        sing="B4:4 C#5:4 B4:4 D#5:4 B4:4 E5:4 D#5:4 E5:4",
        arp=arp([(_VW_ARP[c], 4) for c in _VW_CH], [0, 1, 2, 1], 0.5),
        bass="E2:2 B2:2 A2:2 E3:2 E2:2 B2:2 B2:2 F#2:2 E2:2 B2:2 A2:2 E3:2 B2:2 F#2:2 E2:4",
        perc=cat(LIGHT_C, rep(LIGHT, 6), FILL_LIGHT))),
))

# ---- 3. VS_TRAINER ---------------------------------------------------------------------------------------------------
_T_CALL1 = "G4:0.5 G4:0.5 Bb4:0.5 D5:0.5 C5:0.5 Bb4:0.5 A4:0.5 Bb4:0.5 G4:1 D5:1 G4:2"
_T_ANS1 = "A4:0.5 A4:0.5 C5:0.5 Eb5:0.5 D5:0.5 C5:0.5 Bb4:0.5 C5:0.5 A4:1 Eb5:1 A4:2"
_T_CALL2 = "Bb4:0.5 Bb4:0.5 D5:0.5 F5:0.5 Eb5:0.5 D5:0.5 C5:0.5 D5:0.5 Bb4:1 F5:1 Bb4:2"
_T_ANS2 = "C5:0.5 C5:0.5 Eb5:0.5 G5:0.5 F5:0.5 Eb5:0.5 D5:0.5 Eb5:0.5 C5:1 G5:1 F#5:2"
_T_BASS = [(0, 1), (0, 0.5), (0, 0.5), (12, 0.5), (0, 0.5), (0, 0.5), (0, 0.5)]
_T_ARP_A = [("G3+Bb3+D4", 8), ("F3+A3+Eb4", 8), ("Bb3+D4+F4", 8), ("C4+Eb4+G3", 4), ("D4+F#3+A3", 4)]
_T_BROKEN_B = arp([("Eb4+G4+Bb4+Eb5", 4), ("F4+A4+C5+F5", 4), ("D4+F#4+A4+D5", 4), ("G4+Bb4+D5+G5", 4),
                   ("Eb4+G4+Bb4+Eb5", 4), ("F4+A4+C5+F5", 4), ("D4+F#4+A4+D5", 8)], [0, 1, 2, 1, 3, 2, 1, 2], 0.5)
PIECES.append(dict(
    id="VS_TRAINER", slot="MUS_VS_TRAINER", bpm=128, meter=4,
    what="every trainer battle but the leaders, the ELITE FOUR and the champion: about 700 trainer entries",
    why="A trainer battle is an informal BENCHMARK (1.4): the same test run again. Each two-bar phrase is answered by "
        "the same phrase one step higher, harp then flute, four runs climbing from G to A to B-flat to C, and the "
        "last one reaches F-sharp, a note the key does not have, to get home. At 128, the tempo all the human songs "
        "share (7.9): every battle against a person is at the people's tempo.",
    intro=join(S("trainer intro", 8, lead="r:6 D4:0.5 F#4:0.5 A4:0.5 C5:0.5",
                 bass=pattern("D2 D2", _T_BASS), arp=arp([("D3+F#3+A3", 8)], [0, 1, 2, 1], 0.5),
                 perc=cat(rep("k:1", 4), ROLL))),
    loop=join(
        S("trainer A", 32, lead=cat(_T_CALL1, rest(8), _T_CALL2, rest(8)), sing=cat(rest(8), _T_ANS1, rest(8), _T_ANS2),
          arp=arp(_T_ARP_A, [0, 1, 2, 1], 0.5),
          bass=pattern("G2 G2 F2 F2 Bb2 Bb2 C3 D3", _T_BASS), perc=drums(STRAIGHT_C, STRAIGHT, FILL)),
        S("trainer B", 32, sing="G5:4 A5:4 F#5:4 G5:2 Bb5:2 G5:4 A5:2 C6:2 A5:4 F#5:4", lead=_T_BROKEN_B,
          harm="Eb5:4 F5:4 D5:4 D5:2 G5:2 Eb5:4 F5:2 A5:2 F#5:4 D5:4",
          bass=pattern("Eb2 F2 D2 G2 Eb2 F2 D2 D2", _T_BASS), perc=drums(STRAIGHT_C, STRAIGHT, FILL)),
        S("trainer A'", 32, sing=cat(_T_CALL1, rest(8), _T_CALL2, rest(8)), lead=cat(rest(8), _T_ANS1, rest(8), _T_ANS2),
          arp=arp(_T_ARP_A, [0, 1, 2, 1], 0.5),
          bass=pattern("G2 G2 F2 F2 Bb2 Bb2 C3 D3", _T_BASS), perc=drums(STRAIGHT_C, STRAIGHT, FILL)),
    ),
))

# ---- 4. VICTORY_TRAINER ----------------------------------------------------------------------------------------------
_VT_LEAD = ("G4:0.5 G4:0.5 B4:0.5 D5:0.5 C5:0.5 B4:0.5 A4:0.5 B4:0.5  G4:1 D5:1 G4:2 "
            "E4:0.5 E4:0.5 G4:0.5 C5:0.5 B4:0.5 A4:0.5 G4:0.5 A4:0.5  F#4:1 A4:1 D4:2 "
            "G4:0.5 G4:0.5 B4:0.5 D5:0.5 C5:0.5 B4:0.5 A4:0.5 B4:0.5  G4:1 E5:1 B4:2 "
            "C5:1 B4:1 A4:1 F#4:1  G4:4")
PIECES.append(dict(
    id="VICTORY_TRAINER", slot="MUS_VICTORY_TRAINER", bpm=132, meter=4,
    what="after every trainer win (follows VS_TRAINER)",
    why="The trainer battle's phrase, now in G major, and the two voices play it together a third apart instead of "
        "one answering the other: the runs agree.",
    intro=join(S("vt intro", 4, lead="D4:0.5 G4:0.5 B4:0.5 D5:0.5 G5:2", bass="r:2 G2:2",
                 perc="s:0.25 s:0.25 s:0.25 s:0.25 s:0.5 s:0.5 c:2")),
    loop=join(S("vt loop", 32, lead=_VT_LEAD, sing=dia(_VT_LEAD, "G A B C D E F#", 2),
        arp=arp([("G3+B3+D4", 8), ("C4+E4+G3", 4), ("D4+F#3+A3", 4), ("G3+B3+D4", 4), ("E3+G3+B3", 4),
                 ("C4+E4+G3", 2), ("D4+F#3+A3", 2), ("G3+B3+D4", 4)], [0, 1, 2, 1], 0.5),
        bass="G2:1 G3:0.5 G2:0.5 G2:1 D3:1  G2:1 G3:0.5 G2:0.5 G2:1 D3:1  C3:1 C4:0.5 C3:0.5 C3:1 G2:1  "
             "D3:1 D4:0.5 D3:0.5 D3:1 A2:1  G2:1 G3:0.5 G2:0.5 G2:1 D3:1  E2:1 E3:0.5 E2:0.5 E2:1 B2:1  "
             "C3:1 C3:1 D3:1 D3:1  G2:4",
        perc=cat(LIGHT_C, rep(LIGHT, 6), FILL_LIGHT))),
))

# ---- 5. VS_GYM_LEADER ------------------------------------------------------------------------------------------------
_SUBJ = ["B3:1 D4:0.5 F#4:0.5 D4:1 B3:1", "D4:1 G4:0.5 F#4:0.5 D4:1 B3:1", "A3:1 C#4:0.5 D4:0.5 E4:1 A4:1",
         "C#4:1 E4:0.5 D4:0.5 C#4:1 F#4:1", "D4:0.5 E4:0.5 F#4:0.5 E4:0.5 D4:1 B4:1", "D5:1 B4:0.5 A4:0.5 G4:1 D4:1",
         "A4:1 F#4:0.5 E4:0.5 A4:1 E4:1", "C#5:1 B4:0.5 A4:0.5 F#4:2"]
_SUBJECT = " ".join(_SUBJ)
_L_BASS = [(0, 1.5), (0, 0.5), (12, 1), (0, 1)]
_L_ARP = [("F#4+B4+D5", 4), ("G4+B4+D5", 4), ("F#4+A4+D5", 4), ("E4+A4+C#5", 4)] * 2
_L_B = ("F#4:1 A4:1 D5:1.5 C#5:0.5  E5:1 C#5:1 A4:2  B4:1 D5:1 F#5:1.5 E5:0.5  D5:1 B4:1 G4:2 "
        "F#4:0.5 G4:0.5 A4:1 D5:1 F#5:1  E5:1.5 D5:0.5 C#5:1 A4:1  B4:1 D5:1 G5:1 F#5:0.5 E5:0.5  C#5:2 A4:1 F#4:1")
PIECES.append(dict(
    id="VS_GYM_LEADER", slot="MUS_VS_GYM_LEADER", bpm=128, meter=4,
    what="every BENCHMARK leader and the ELITE FOUR",
    why="A formal BENCHMARK: the same test, run strictly. A canon -- the flute plays exactly what the harp played, one "
        "bar later and an octave up, all the way through, and it can be followed by ear (the eight bars are built so "
        "that each fits both its own chord and the next). Then eight bars in D major where the two play one line "
        "together. 128, the people's tempo.",
    intro=join(S("leader intro", 8, lead=rest(8), bass=pattern([("F#2", 8)], [(0, 0.5), (0, 0.5), (12, 0.5), (0, 0.5)]),
                 arp=arp([("F#4+A#4+C#5", 8)], [0, 1, 2, 1], 0.5),
                 perc=cat(rep("k:1", 4), ROLL))),
    loop=join(
        S("leader canon 1", 32, lead=_SUBJECT, sing=cat(rest(4), transpose(" ".join(_SUBJ[:7]), 12)),
          harm="D4:4 B3:4 F#4:4 C#4:4 D4:4 B3:4 F#4:4 C#4:4",
          bass=pattern("B2 G2 D2 A2 B2 G2 D2 A2", _L_BASS), perc=drums(HALF_C, HALF, FILL)),
        S("leader canon 2", 32, lead=_SUBJECT, sing=transpose(" ".join(_SUBJ[7:] + _SUBJ[:7]), 12),
          arp=arp(_L_ARP, [0, 1, 2, 1], 0.5),
          bass=pattern("B2 G2 D2 A2 B2 G2 D2 A2", _L_BASS), perc=drums(EIGHTS_C, EIGHTS, FILL)),
        S("leader B", 32, lead=_L_B, sing=_L_B,
          arp=arp([("F#4+A4+D5", 4), ("E4+A4+C#5", 4), ("F#4+B4+D5", 4), ("G4+B4+D5", 4), ("F#4+A4+D5", 4),
                   ("E4+A4+C#5", 4), ("G4+B4+D5", 4), ("E4+A4+C#5", 4)], [0, 1, 2, 1], 0.5),
          bass=pattern("D2 A2 B2 G2 D2 A2 G2 A2", _L_BASS), perc=drums(EIGHTS_C, EIGHTS, FILL)),
    ),
))

# ---- 6. VICTORY_GYM_LEADER -------------------------------------------------------------------------------------------
PIECES.append(dict(
    id="VICTORY_GYM_LEADER", slot="MUS_VICTORY_GYM_LEADER", bpm=120, meter=4,
    what="after each leader and the champion, and the champion's room afterwards (savebgm)",
    why="BADGE's climb, in D (D E F# A B, held on the sixth as BADGE holds on A), low on the harp and then high on the "
        "flute; then the canon's eight bars again, the two voices no longer one behind the other but together, a third "
        "apart.",
    intro=join(S("vl intro", 8, lead="A3:0.5 D4:0.5 F#4:0.5 A4:0.5 D5:2 C#5:1 B4:1 A4:2", bass="D2:4 A2:4",
                 perc="c:4 s:0.25 s:0.25 s:0.25 s:0.25 s:0.25 s:0.25 s:0.25 s:0.25 s:1 s:1")),
    loop=join(
        S("vl A", 32,
          lead="D4:0.5 E4:0.5 F#4:0.5 A4:0.5 B4:2  A4:1 G4:1 B4:2  F#4:1 A4:1 D5:2  C#5:1 B4:1 A4:2 "
               "A4:1 F#4:1 D4:2  D5:1 C#5:1 B4:2  G4:1 B4:1 A4:1 C#5:1  D5:4",
          sing="r:4 D5:4 A4:4 E5:4 D5:0.5 E5:0.5 F#5:0.5 A5:0.5 B5:2 F#5:4 D5:2 E5:2 F#5:4",
          arp=arp([("F#4+A4+D5", 4), ("G4+B4+D5", 4), ("F#4+A4+D5", 4), ("E4+A4+C#5", 4), ("F#4+A4+D5", 4),
                   ("F#4+B4+D5", 4), ("G4+B4+D5", 2), ("E4+A4+C#5", 2), ("F#4+A4+D5", 4)], [0, 1, 2, 1], 0.5),
          bass="D2:1 D2:1 A2:1 D2:1  G2:1 G2:1 D3:1 G2:1  D2:1 D2:1 A2:1 D2:1  A2:1 A2:1 E3:1 A2:1 "
               "D2:1 D2:1 A2:1 D2:1  B2:1 B2:1 F#3:1 B2:1  G2:1 G2:1 A2:1 A2:1  D2:2 D3:2",
          perc=drums(STATELY_C, STATELY, "k:1 h:1 s:0.5 s:0.5 s:0.5 s:0.5")),
        S("vl B", 32, lead=_SUBJECT, sing=dia(_SUBJECT, "D E F# G A B C#", 2),
          arp=arp(_L_ARP, [0, 1, 2, 1], 0.5),
          bass="B2:1 B2:1 F#3:1 B2:1  G2:1 G2:1 D3:1 G2:1  D2:1 D2:1 A2:1 D2:1  A2:1 A2:1 E3:1 A2:1 "
               "B2:1 B2:1 F#3:1 B2:1  G2:1 G2:1 D3:1 G2:1  D2:1 D2:1 A2:1 D2:1  A2:2 A2:1 C#3:1",
          perc=drums(STATELY_C, STATELY, "k:1 h:1 s:0.5 s:0.5 s:0.5 s:0.5")),
    ),
))

# ---- 7. VS_CHAMPION --------------------------------------------------------------------------------------------------
_C_A = ("E5:0.75 E5:0.75 D5:0.5 C5:1 B4:0.5 C5:0.5  A4:2 r:1 C5:0.5 D5:0.5 "
        "E5:0.75 E5:0.75 D5:0.5 C5:1 D5:0.5 E5:0.5  D5:2 r:1 B4:0.5 C5:0.5 "
        "E5:0.75 E5:0.75 G5:0.5 E5:1 D5:0.5 C5:0.5  A5:1.5 G5:0.5 F5:1 E5:1 "
        "E5:0.75 D5:0.75 C5:0.5 G4:1 C5:0.5 D5:0.5  D5:3 r:1")
_C_BASS = [(0, 0.75), (0, 0.75), (12, 0.5), (0, 0.5), (0, 0.5), (12, 0.5), (0, 0.5)]
_C_BROKEN = lambda chs: arp([(c, 4) for c in chs], [0, 1, 2, 1, 3, 2, 1, 2], 0.5)
_AM, _F, _C, _G = "A3+C4+E4+A4", "F3+A3+C4+F4", "C4+E4+G4+C5", "G3+B3+D4+G4"
_BB, _DM, _E = "Bb3+D4+F4+Bb4", "D4+F4+A4+D5", "E4+G#4+B4+E5"
PIECES.append(dict(
    id="VS_CHAMPION", slot="MUS_VS_CHAMPION", bpm=128, meter=4,
    what="the champion, AL CLEAR",
    why="AL CLEAR is the prevailing paradigm, not a king (the lexicon's champion row, 1). So his battle is built from the most "
        "prevailing material there is: A minor (7.6 calls it the most common key in popular music), over A minor, F, "
        "C, G -- pop's four-chord loop -- in pop's commonest rhythm (3+3+2). For sixteen bars nothing in it is wrong "
        "and nothing is new. Then the pattern takes in a chord it does not have (B-flat), tries itself in another key "
        "(the same four steps a fourth up, from D minor), and finds its way home the usual way, by E major -- and the "
        "loop starts over, because it has not been beaten yet. 128, the people's tempo.",
    intro=join(S("champion intro", 8, lead="r:4 E4:0.5 G#4:0.5 B4:0.5 D5:0.5 E5:2", bass=pattern("E2 E2", _C_BASS),
                 arp=arp([("E3+G#3+B3", 8)], [0, 1, 2, 1], 0.25),
                 perc=cat(rep("k:1", 4), ROLL))),
    loop=join(
        S("champion A", 32, lead=_C_A, arp=arp([(c, 4) for c in ["A3+C4+E4", "F3+A3+C4", "C4+E4+G3", "G3+B3+D4"] * 2],
                                              [0, 1, 2, 1], 0.25),
          bass=pattern("A2 F2 C3 G2 A2 F2 C3 G2", _C_BASS), perc=drums(POP_C, POP, FILL)),
        S("champion A2", 32, sing=_C_A, harm=dia(_C_A, "A B C D E F G", -2),
          lead=_C_BROKEN([_AM, _F, _C, _G] * 2),
          bass=pattern("A2 F2 C3 G2 A2 F2 C3 G2", _C_BASS), perc=drums(POP_C, POP, FILL)),
        S("champion B", 32, sing="E5:2 C5:2 F5:2 A5:2 G5:3 E5:1 D5:4 E5:2 C5:2 F5:2 A5:2 G5:2 C6:2 Bb5:4",
          lead=_C_BROKEN([_AM, _F, _C, _G, _AM, _F, _C, _BB]),
          bass=pattern("A2 F2 C3 G2 A2 F2 C3 Bb2", _C_BASS), perc=drums(POP_C, POP, FILL)),
        S("champion C", 32, sing="A5:2 F5:2 Bb5:2 F5:2 C6:3 A5:1 G5:4 A5:2 F5:2 D6:2 Bb5:2 B5:4 G#5:4",
          lead=_C_BROKEN([_DM, _BB, "F3+A3+C4+F4", _C, _DM, _BB, _E, _E]),
          bass=pattern("D3 Bb2 F2 C3 D3 Bb2 E2 E2", _C_BASS), perc=drums(POP_C, POP, FILL)),
    ),
))

# ---- 8. VS_LEGEND (bars of six beats) --------------------------------------------------------------------------------
_DACT = [(0, 0.5), (0, 0.25), (0, 0.25)] * 5 + [(0, 0.5), (7, 0.5)]
_LYRE = [0, 1, 2, 1]
def _lyre(chs):
    return arp([(c, 6) for c in chs], _LYRE, 0.5)
_HEX = "k:0.5 h:0.25 h:0.25 k:0.5 h:0.25 h:0.25 s:0.5 h:0.25 h:0.25 k:0.5 h:0.25 h:0.25 k:0.5 h:0.25 h:0.25 s:0.5 s:0.5"
_HEX_C = "c:0.5 h:0.25 h:0.25 k:0.5 h:0.25 h:0.25 s:0.5 h:0.25 h:0.25 k:0.5 h:0.25 h:0.25 k:0.5 h:0.25 h:0.25 s:0.5 s:0.5"
_HEX_FILL = "k:0.5 h:0.25 h:0.25 k:0.5 h:0.25 h:0.25 s:0.5 h:0.25 h:0.25 s:0.25 s:0.25 s:0.25 s:0.25 s:0.25 s:0.25 s:0.25 s:0.25 s:0.5 s:0.5"
_D5, _EB5, _C5L = "D4+A4+D5", "Eb4+Bb4+Eb5", "C4+G4+C5"
_BB5, _F5L, _G5L = "Bb3+F4+Bb4", "F3+C4+F4", "G3+D4+G4"
PIECES.append(dict(
    id="VS_LEGEND", slot="MUS_VS_LEGEND", bpm=132, meter=6,
    what="PROMETHEUS, ASCLEPIUS and ORPHEUS; the roamers BRONTES, TYPHON and BOREAS; TRITON and PHOENIX",
    why="Names out of myth, so an older sound: D Phrygian (the flat second, E-flat against D, and a D held under it), "
        "the harp as a lyre in open fifths, and under everything the dactyl, long-short-short, the foot of Greek epic "
        "verse -- five to a bar and a long-long to close it, so each bar of six beats is a line of hexameter, the metre "
        "of Homer. 132, not the people's 128.",
    intro=join(S("legend intro", 6, lead=_lyre([_D5]), bass=pattern("D2", _DACT), perc="r:5 s:0.5 s:0.5")),
    loop=join(
        S("legend A", 48, lead=_lyre([_D5, _EB5, _D5, _EB5, _D5, _EB5, _C5L, _D5]),
          sing="D5:2 F5:1 A5:2 G5:1  Bb5:2 G5:1 Eb5:3  F5:2 A5:1 D6:2 C6:1  Bb5:1 G5:1 F5:1 Eb5:3 "
               "D5:2 F5:1 A5:2 Bb5:1  G5:2 Eb5:1 Bb4:3  C5:1 Eb5:1 G5:1 F5:1 Eb5:2  D5:6",
          harm="D4:48", bass=pattern("D2 Eb2 D2 Eb2 D2 Eb2 C2 D2", _DACT),
          perc=cat(_HEX_C, rep(_HEX, 6), _HEX_FILL)),
        S("legend B", 48, lead=_lyre([_BB5, _F5L, _G5L, _EB5, _BB5, _F5L, _EB5, _EB5]),
          sing="F5:2 D5:1 Bb4:3  C5:2 F5:1 A5:3  G5:2 Bb5:1 D6:3  C6:2 Bb5:1 G5:3 "
               "F5:2 D5:1 Bb4:3  A4:2 C5:1 F5:3  G5:2 F5:1 Eb5:3  C5:2 Bb4:1 Eb5:3",
          bass=pattern("Bb2 F2 G2 Eb2 Bb2 F2 Eb2 Eb2", _DACT), perc=cat(_HEX_C, rep(_HEX, 6), _HEX_FILL)),
    ),
))

# ---- 9. VS_MEWTWO: S.T.A.R.R. ----------------------------------------------------------------------------------------
_RIFF = "C#4:0.5 F#4:0.5 E4:0.5 D4:0.5 C#4:0.5 B3:0.5 A3:0.5 A3:0.5"
_HOOK1 = "C#5:1 F#5:1 E5:1 D5:1 C#5:1 B4:1 A4:2"
_S8 = [(0, 0.5), (0, 0.5), (12, 0.5), (0, 0.5)]
PIECES.append(dict(
    id="VS_MEWTWO", slot="MUS_VS_MEWTWO", bpm=128, intro_bpm=110, meter=4,
    what="S.T.A.R.R. in DOLDRUM CAVE (vanilla's Mewtwo slot), and nothing else",
    why="It plays only for S.T.A.R.R., so containment (7.13) lets its hook in: C# F# E D C# B A (7.9). It opens at "
        "110, its sleeping tempo, the hook alone and left on a held E as at Quicksilver, then wakes to 128, the "
        "people's tempo (7.9, T-559). Then recursion (4.7): the harp plays the hook every bar as a riff while the flute "
        "plays the same seven notes a bar a note, then two beats a note, then one, until in the last two bars the "
        "flute's hook is the harp's riff.",
    intro=join(S("starr intro", 12, sing=_HOOK1 + " E5:4", harm="F#3:8 E3:4", bass="F#2:8 E2:4")),
    loop=join(
        S("starr A", 32, lead=rep(_RIFF, 8), sing="C#5:4 F#5:4 E5:4 D5:4 C#5:4 B4:4 A4:4 E5:4",
          harm="A3:4 F#3:4 C#4:4 D4:4 A3:4 D4:4 F#3:4 G#3:4",
          bass=pattern([(r, 4) for r in "F#2 D2 A2 B2 F#2 B2 D2 E2".split()], _S8),
          perc=drums("c:1 h:1 s:1 h:1", "k:1 h:1 s:1 h:1", FILL)),
        S("starr B", 32, lead=rep(_RIFF, 8),
          sing="C#5:2 F#5:2 E5:2 D5:2 C#5:2 B4:2 A4:2 C#5:2 F#5:2 E5:2 D5:2 C#5:2 B4:2 A4:2 E5:4",
          bass=pattern([(r, 2) for r in "F#2 D2 A2 B2 F#2 B2 D2 F#2 D2 A2 B2 F#2 B2 D2".split()] + [("E2", 4)], _S8),
          perc=drums(EIGHTS_C, EIGHTS, FILL)),
        S("starr A'", 32, lead=rep(_RIFF, 8), sing=cat(rep(_HOOK1, 3), transpose(rep(_RIFF, 2), 12)),
          arp=arp([("F#4+A4+C#5", 4), ("E4+A4+C#5", 4)] * 3 + [("F#4+A4+C#5", 4), ("E4+G#4+B4", 4)], [0, 1, 2, 1], 0.25),
          bass=pattern([(r, 4) for r in "F#2 A2 F#2 A2 F#2 A2 F#2 E2".split()], _S8),
          perc=drums(SIXTEENS_C, SIXTEENS, FILL)),
    ),
))


# ---------------------------------------------------------------------------------------------------------------------
# The MIDI
# ---------------------------------------------------------------------------------------------------------------------
def parse(tokens):
    t, out = 0.0, []
    for tok in tokens.split():
        what, b = tok.rsplit(":", 1)
        a, _, c = b.partition("/")
        b = float(a) / float(c or 1)
        if what in PERC:
            out.append((t, b, what))
        elif what != "r":
            out.append((t, b, [midi(n) for n in what.split("+")]))
        t += b
    return out, t


def section_len(tracks):
    lens = {round(parse(tok)[1], 4) for _, tok in tracks}
    assert len(lens) == 1, "tracks of unequal length: %s" % lens
    return lens.pop()


def notes_of(p):
    """[(beat, beats, key, note)], total beats, (loop start, loop end), [(beat, bpm)]"""
    out, t0 = [], 0.0
    tempos = [(0.0, p.get("intro_bpm", p["bpm"]))]
    for i, sec in enumerate([p["intro"], p["loop"]]):
        if i == 1:
            loop = t0
            if p.get("intro_bpm"):
                tempos.append((t0, p["bpm"]))
        for role, tok in sec:
            for b, d, n in parse(tok)[0]:
                if isinstance(n, str):
                    out.append((t0 + b, d, n, NOISE_KEY[n]))
                elif role in ("lead", "sing"):
                    out += [(t0 + b, d, role, m) for m in n]
                else:
                    out.append((t0 + b, d, role, max(n)))
        t0 += section_len(sec)
    return out, t0, (loop, t0), tempos


def gate(key, beats):
    return GATE[key] * beats if key in GATE else 2 / TPB


def song_midi(p):
    notes, total, loop, tempos = notes_of(p)
    tick = lambda beats: int(round(beats * TPB))
    tempo = lambda bpm: b"\xff\x51\x03" + struct.pack(">I", int(round(60e6 / bpm)))[1:]
    ev = [(tick(b), 6 if b else 0, tempo(bpm)) for b, bpm in tempos]
    for key in sorted({k for _, _, k, _ in notes}, key=lambda k: CH[k][0]):
        ch, prog, vol, _ = CH[key]
        ev += [(0, 1, bytes([0xC0 | ch, prog])), (0, 2, bytes([0xB0 | ch, 7, vol])), (0, 3, bytes([0xB0 | ch, 10, 64]))]
    end = tick(total)
    for b, d, key, m in notes:
        ch, _, _, vel = CH[key]
        on = tick(b)
        off = min(max(on + 1, tick(b + gate(key, d))), end)     # a loop's notes stop at its end: a clean loop point
        ev.append((on, 20, bytes([0x90 | ch, m, vel])))
        ev.append((off, 10, bytes([0x80 | ch, m, 0])))
    ev.append((tick(loop[0]), 5, b"\xff\x06\x01["))
    ev.append((tick(loop[1]), 30, b"\xff\x06\x01]"))
    ev.sort()
    body, now = b"", 0
    for t, _, e in ev:
        body += G.vlq(t - now) + e
        now = t
    body += b"\x00\xff\x2f\x00"
    return b"MThd" + struct.pack(">IHHH", 6, 0, 1, TPB) + b"MTrk" + struct.pack(">I", len(body)) + body


def check(p):
    notes, total, loop, _ = notes_of(p)
    keys = {k for _, _, k, _ in notes}
    tracks = {CH[k][0] for k in keys}
    assert len(tracks) <= BGM_TRACKS, "%s: %d tracks, the BGM player has %d" % (p["id"], len(tracks), BGM_TRACKS)
    low = [(k, m) for _, _, k, m in notes if k in ("arp", "harm", "bass") and m < 36]
    assert not low, "%s: %s -- m4a plays every PSG key under 36 (C2) as C2 (engine.md trap 44)" % (p["id"], low)
    for k in keys - {"lead", "sing"}:                     # a PSG track is one note at a time
        span = sorted((b, b + gate(k, d)) for b, d, kk, _ in notes if kk == k)
        assert all(a[1] <= c[0] + 1e-6 for a, c in zip(span, span[1:])), "%s: %s overlaps itself" % (p["id"], k)
    marks = sorted([(b, 1) for b, d, k, _ in notes if k in ("lead", "sing")] +
                   [(b + gate(k, d), -1) for b, d, k, _ in notes if k in ("lead", "sing")])
    level = peak = 0
    for _, s in marks:
        level += s; peak = max(peak, level)
    assert peak <= 4, "%s: %d DirectSound notes at once, and the mixer has five" % (p["id"], peak)
    return total


def engine():
    """{path: new contents} for every file this writes."""
    assert G.VOICES[ARP_VOICE].startswith("\tvoice_square_1_alt"), "voicegroup195's program 9 is not the arp's square"
    out, cfg = {}, open(CFG, encoding="utf-8").read()
    for p in PIECES:
        check(p)
        f = "mus_" + p["id"].lower()
        out[os.path.join(MIDI_DIR, f + ".mid")] = song_midi(p)
        cfg, k = re.subn(r"^(%s\.mid:\s+.*?)-G\d+" % re.escape(f), r"\g<1>-G%03d" % VOICEGROUP, cfg, flags=re.M)
        assert k == 1, "midi.cfg has no line for %s" % f
    out[CFG] = cfg
    return out


def main():
    if not os.path.isdir(MIDI_DIR):
        print("  the game: no engineGba/ here, skipped")
        return
    changed = []
    for path, data in engine().items():
        mode = "b" if isinstance(data, bytes) else ""
        old = open(path, "r" + mode, **({} if mode else {"encoding": "utf-8"})).read() if os.path.exists(path) else None
        if old != data:
            changed.append(os.path.relpath(path, GBA))
            if "--write" in sys.argv:
                tmp = path + ".tmp"
                open(tmp, "w" + mode, **({} if mode else {"encoding": "utf-8"})).write(data)
                if os.path.exists(path):
                    os.chmod(tmp, os.stat(path).st_mode)
                os.replace(tmp, path)
    lens = ", ".join("%s %.0f s" % (p["id"], section_len(p["loop"]) * 60 / p["bpm"]) for p in PIECES)
    print("  %d battle pieces on voicegroup%03d; loops: %s" % (len(PIECES), VOICEGROUP, lens))
    if not changed:
        print("  the game: unchanged")
    else:
        print("  the game: %s %d file(s): %s" % ("wrote" if "--write" in sys.argv else "would write", len(changed),
                                                 ", ".join(changed[:6]) + (" ..." if len(changed) > 6 else "")))


if __name__ == "__main__":
    main()
