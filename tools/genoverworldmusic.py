#!/usr/bin/env python3
"""T-565 batch 5: the everyday overworld music -- ours, in place of pret's nine, and two towns' own.

    python3 tools/genoverworldmusic.py            # report: is the engine current
    python3 tools/genoverworldmusic.py --write    # write it into engineGba

THE VOICE (the user, 2026-11-17, by multiple choice from three drafts of one set of notes -- A the harp and flute, B
the cartridge, C both -- "C Both", and "Split them"): genfanfares.py's voicegroup195, as the fanfares and the battle
music (genbattlemusic.py, whose MIDI writer this uses): the HARP and FLUTE on the tunes, the cartridge under them.

LURID AND DOLDRUM, split as vision 7.4 planned: they shared MUS_FUCHSIA; each now has its own song in its own key --
LURID (E) ScornSolutions Blues, DOLDRUM (G) Poly and Fields -- in two appended slots. tools/port_music.py's MAP_MUSIC
points their maps there (the game lane's go-ahead, 2026-11-17); MUS_FUCHSIA keeps pret's tune for its other six maps.
MUS_PEWTER is ours now (THRESHOLD), so port_music.py no longer restores it.

WHAT IT WRITES (engineGba/)
    sound/songs/midi/<slot>.mid      nine over pret's in place (ROUTE3, ROUTE11, ROUTE24, POKE_CENTER, GYM, PEWTER,
                                     VIRIDIAN_FOREST, CYCLING, SURF) and two new (mus_doldrum, mus_lurid)
    sound/songs/midi/midi.cfg        each of the nine's -G to 195; the two new songs' lines
    sound/song_table.inc, include/constants/songs.h, ld_script.ld   the two new songs (a song is four lines, engine.md
                                     trap 25), on the BGM player
Each piece's reason is its "why" below. Every note DRAFT.
"""
import os, re, sys

import genbattlemusic as GB
import genfanfares as G

K = GB                                               # the helpers the drafts were written with
class F:                                             # (the drafts' F.midi)
    midi = staticmethod(GB.midi)
NAMES = GB.NAMES
shift, dia, S, join, rest, rep, cat = GB.transpose, GB.dia, GB.S, GB.join, GB.rest, GB.rep, GB.cat
transpose = GB.transpose
GBA, MIDI_DIR, CFG = G.GBA, G.MIDI_DIR, G.CFG
TABLE, SONGS_H, LD = G.TABLE, G.SONGS_H, G.LD
VOICEGROUP = G.VOICEGROUP
FILES = {"ROUTE3": "mus_route3", "ROUTE11": "mus_route11", "ROUTE24": "mus_route24", "CHECKPOINT": "mus_poke_center",
         "BENCHMARK": "mus_gym", "THRESHOLD": "mus_pewter", "UNDERTONE": "mus_viridian_forest", "CYCLING": "mus_cycling",
         "SURF": "mus_surf", "DOLDRUM": "mus_doldrum", "LURID": "mus_lurid"}
NEW = {"DOLDRUM": ("MUS_DOLDRUM", "DOLDRUM's own, Poly and Fields over a G that never moves"),
       "LURID": ("MUS_LURID", "LURID's own, ScornSolutions Blues")}

# ---------------------------------------------------------------------------------------------------------------------
# Notation helpers, with exact fractions (a triplet is 1/3)
# ---------------------------------------------------------------------------------------------------------------------
from fractions import Fraction
def fb(b):
    f = Fraction(b).limit_denominator(24)
    return str(f.numerator) if f.denominator == 1 else "%d/%d" % (f.numerator, f.denominator)

def pattern(roots, pat):
    """as the battle drafts' pattern(), with exact fractions (a triplet is 1/3, not 0.333333)"""
    if isinstance(roots, str):
        roots = [(r, None) for r in roots.split()]
    out = []
    for r, span in roots:
        m = F.midi(r)
        span = Fraction(span).limit_denominator(24) if span is not None else sum(Fraction(b).limit_denominator(24) for _, b in pat)
        t, k = Fraction(0), 0
        while t < span:
            off, b = pat[k % len(pat)]
            b = min(Fraction(b).limit_denominator(24), span - t)
            out.append("%s:%s" % (K.nn(m + off), fb(b)) if off is not None else "r:%s" % fb(b))
            t += b; k += 1
    return " ".join(out)

def arp(chords, idx, step):
    out = []
    step = Fraction(step).limit_denominator(24)
    for ch, span in chords:
        ns = ch.split("+"); span = Fraction(span).limit_denominator(24)
        t, k = Fraction(0), 0
        while t < span:
            out.append("%s:%s" % (ns[idx[k % len(idx)]], fb(step)))
            t += step; k += 1
    return " ".join(out)

def shift(tokens, semis):
    return transpose(tokens, semis)

def chords_arp(chs, beats, idx, step):
    return arp([(c, beats) for c in chs], idx, step)


T = "1/3"; TT = "2/3"; FT = "4/3"
PIECES = []

# ---- 1. ROUTE3: the main road -----------------------------------------------------------------------------------------
_R3_LEAD = ("B4:1 D5:0.5 B4:0.5 A4:1 G4:1  E4:1 G4:0.5 A4:0.5 B4:2  C5:1 B4:0.5 A4:0.5 G4:1 E4:1  D4:1 F#4:1 A4:2 "
            "B4:1 D5:0.5 B4:0.5 A4:1 G4:1  E5:1 D5:0.5 B4:0.5 G4:2  A4:1 G4:1 F#4:1 A4:1  G4:4")
_R3_SING = "D5:4 B4:4 E5:4 F#5:4 D5:4 G5:4 E5:2 D5:2 B4:4"
_R3_CH = [("G3+B3+D4", 4), ("E3+G3+B3", 4), ("C4+E4+G3", 4), ("D4+F#3+A3", 4), ("G3+B3+D4", 4), ("E3+G3+B3", 4),
          ("C4+E4+G3", 2), ("D4+F#3+A3", 2), ("G3+B3+D4", 4)]
_R3_BASS = "G2:1 D3:1 G3:1 D3:1  E2:1 B2:1 E3:1 B2:1  C3:1 G2:1 C3:1 G2:1  D3:1 A2:1 D3:1 A2:1 " \
           "G2:1 D3:1 G3:1 D3:1  E2:1 B2:1 E3:1 B2:1  C3:1 G2:1 D3:1 A2:1  G2:1 D3:1 G2:2"
def _r3(semis_tune, semis_bass, first):
    return S("route3 %+d" % semis_tune, 32, lead=shift(_R3_LEAD, semis_tune), sing=shift(_R3_SING, semis_tune),
             arp=shift(arp(_R3_CH, [0, 1, 2, 1], 0.5), semis_tune), bass=shift(_R3_BASS, semis_bass),
             perc=cat(first, rep(K.LIGHT, 6), K.FILL_LIGHT))
PIECES.append(dict(
    id="ROUTE3", slot="MUS_ROUTE3", bpm=126, meter=4,
    what="the game's main road: Routes 3-10 and 16-22, KINDLE ROAD, TREASURE BEACH, BOND BRIDGE, THREE ISLAND's port, "
         "CAPE BRINK (23 maps)",
    why="A road is a modulation between the towns it joins (vision 7), and this slot is a dozen roads at once, so it "
        "never settles: the same eight bars are carried into the next town's key, as THE BLEED carries C into F "
        "(7.14a) -- G (DOLDRUM), then C (ARDOR), then E (LURID), and the loop brings it home to G.",
    intro=[], loop=join(_r3(0, 0, K.LIGHT_C), _r3(-7, 5, K.LIGHT_C), _r3(-3, -3, K.LIGHT_C)),
))

# ---- 2. ROUTE11: the coast road, ARDOR to LURID ---------------------------------------------------------------------
_R11_LEAD = ("E4:2/3 D4:1/3 C4:2/3 D4:1/3 E4:1 G4:1  A4:2/3 G4:1/3 E4:2/3 C4:1/3 A3:2 "
             "F4:2/3 E4:1/3 D4:2/3 C4:1/3 A3:1 C4:1  D4:2/3 E4:1/3 D4:2/3 B3:1/3 G3:2 "
             "E4:2/3 D4:1/3 C4:2/3 D4:1/3 E4:1 G4:1  C5:2/3 B4:1/3 A4:2/3 G4:1/3 E4:2 "
             "F4:2/3 E4:1/3 D4:2/3 F4:1/3 B3:1 D4:1  C4:4")
_R11_SING = "G5:4 E5:4 A5:4 B5:4 G5:4 C6:4 A5:2 B5:2 C6:4"
_R11_CH = [("C4+E4+G4", 4), ("A3+C4+E4", 4), ("F3+A3+C4", 4), ("G3+B3+D4", 4), ("C4+E4+G4", 4), ("A3+C4+E4", 4),
           ("D4+F4+A3", 2), ("G3+B3+D4", 2), ("C4+E4+G4", 4)]
_R11_BASS = pattern("C3 A2 F2 G2 C3 A2", [(0, 4 / 3), (7, 2 / 3), (12, 4 / 3), (7, 2 / 3)]) + " D3:4/3 A2:2/3 G2:4/3 D3:2/3 C3:2 C3:2"
_SHUF = "k:4/3 h:2/3 s:4/3 h:2/3"
def _r11(semis, sing_semis, first):
    return S("route11 %+d" % semis, 32, lead=shift(_R11_LEAD, semis), sing=shift(_R11_SING, sing_semis),
             arp=shift(arp(_R11_CH, [0, 1, 2], 1 / 3), semis), bass=shift(_R11_BASS, semis),
             perc=cat(first, rep(_SHUF, 6), "k:4/3 h:2/3 s:2/3 s:2/3 s:1/3 s:1/3"))
PIECES.append(dict(
    id="ROUTE11", slot="MUS_ROUTE11", bpm=120, meter=4,
    what="Routes 11 to 15: the long coast road from ARDOR round to LURID",
    why="ARDOR is C and LURID is E (7.4), and this is the long way between them: the tune climbs a whole tone every "
        "eight bars, C, D, E, as the road climbs the map, and the loop drops back to C. It lilts in threes, the sea "
        "beside it.",
    intro=[], loop=join(_r11(0, 0, "c:4/3 h:2/3 s:4/3 h:2/3"), _r11(2, 2, "c:4/3 h:2/3 s:4/3 h:2/3"),
                        _r11(4, -8, "c:4/3 h:2/3 s:4/3 h:2/3")),
))

# ---- 3. ROUTE24: out of DOLDRUM --------------------------------------------------------------------------------------
PIECES.append(dict(
    id="ROUTE24", slot="MUS_ROUTE24", bpm=124, meter=4,
    what="Routes 24 and 25, north out of DOLDRUM to the cottage by the sea",
    why="The road out of DOLDRUM stays in DOLDRUM's key, G, but where the town's bass never moves (below), this one "
        "walks: out of the calm, and only as far as a cottage.",
    intro=[],
    loop=join(S("route24", 64,
        lead="G4:0.5 A4:0.5 B4:1 D5:1 B4:1  C5:0.5 B4:0.5 A4:1 E4:2  D4:0.5 E4:0.5 G4:1 B4:1 A4:1  A4:2 F#4:1 D4:1 "
             "G4:0.5 A4:0.5 B4:1 D5:1 E5:1  G5:1 E5:0.5 D5:0.5 C5:2  B4:1 A4:1 G4:1 F#4:1  G4:4 "
             "E4:1 G4:1 B4:2  C5:1 E5:1 C5:2  D5:1 B4:1 G4:2  A4:1 D5:1 A4:2 "
             "E5:1 B4:1 G4:2  C5:1 E5:1 G5:1 E5:1  D5:1 C5:1 B4:1 A4:1  G4:2 D4:2",
        sing="r:16 B5:4 E5:4 D5:4 D5:4 G5:4 E5:4 B5:4 F#5:4 r:16",
        arp=arp([(c, 4) for c in ["G3+B3+D4", "C4+E4+G3", "G3+B3+D4", "D4+F#3+A3", "G3+B3+D4", "C4+E4+G3", "D4+F#3+A3", "G3+B3+D4"] +
                 ["E3+G3+B3", "C4+E4+G3", "G3+B3+D4", "D4+F#3+A3", "E3+G3+B3", "C4+E4+G3", "D4+F#3+A3", "G3+B3+D4"]],
                [0, 1, 2, 1], 0.5),
        bass=pattern("G2 C3 G2 D3 G2 C3 D3 G2 E2 C3 G2 D3 E2 C3 D3 G2", [(0, 1), (7, 1), (12, 1), (7, 1)]),
        perc=cat(K.LIGHT_C, rep(K.LIGHT, 6), K.FILL_LIGHT, K.LIGHT_C, rep(K.LIGHT, 6), K.FILL_LIGHT))),
))

# ---- 4. CHECKPOINT (MUS_POKE_CENTER) -------------------------------------------------------------------------------
_CP_A = "E5:1 D5:1 C5:2  G4:1 A4:1 C5:2  E5:1 D5:1 C5:1 G4:1  A4:2 B4:2"
_CP_ACH = [("C4+E4+G4", 4), ("A3+C4+E4", 4), ("C4+E4+G4", 4), ("F3+A3+C4", 2), ("G3+B3+D4", 2)]
_CP_ABASS = "C3:2 G2:2 A2:2 E2:2 C3:2 G2:2 F2:2 G2:2"
PIECES.append(dict(
    id="CHECKPOINT", slot="MUS_POKE_CENTER", bpm=112, meter=4,
    what="every CHECKPOINT (both floors), THE REPO, VERDIGRIS's store, the colosseums (58 maps)",
    why="A CHECKPOINT restores a saved state (1), so the piece is a rondo: a refrain, something else, the refrain "
        "exactly as it was. The refrain is HEAL's lullaby (E D C, G A C) drawn out, the state this building saves.",
    intro=[],
    loop=join(
        S("cp A", 16, sing=_CP_A, arp=arp(_CP_ACH, [0, 1, 2, 1], 0.5), bass=_CP_ABASS, perc=rep("k:1 h:1 h:1 h:1", 4)),
        S("cp B", 16, lead="F4:1 A4:1 C5:1 A4:1  G4:1 B4:1 D5:2  E4:1 G4:1 C5:1 G4:1  D4:1 F4:1 G4:2",
          arp=arp([("F3+A3+C4", 4), ("G3+B3+D4", 4), ("E3+G3+C4", 4), ("D3+F3+A3", 2), ("G3+B3+D4", 2)], [0, 1, 2, 1], 0.5),
          bass="F2:2 C3:2 G2:2 D3:2 E2:2 C3:2 D3:2 G2:2", perc=rep("k:1 h:1 h:1 h:1", 4)),
        S("cp A2", 16, sing=_CP_A, lead=dia(_CP_A, "C D E F G A B", -2), arp=arp(_CP_ACH, [0, 1, 2, 1], 0.5),
          bass=_CP_ABASS, perc=rep("k:1 h:1 h:1 h:1", 4)),
        S("cp C", 16, lead="A4:1 C5:1 E5:2  D5:1 C5:1 B4:2  C5:1 B4:1 A4:1 G4:1  F4:2 G4:2",
          arp=arp([("A3+C4+E4", 4), ("G3+B3+D4", 4), ("A3+C4+E4", 2), ("E3+G3+B3", 2), ("F3+A3+C4", 2), ("G3+B3+D4", 2)],
                  [0, 1, 2, 1], 0.5),
          bass="A2:2 E2:2 G2:2 D3:2 A2:2 E2:2 F2:2 G2:2", perc=rep("k:1 h:1 h:1 h:1", 4)),
    ),
))

# ---- 5. BENCHMARK (MUS_GYM) ------------------------------------------------------------------------------------------
_SUBJ = ["B3:1 D4:0.5 F#4:0.5 D4:1 B3:1", "D4:1 G4:0.5 F#4:0.5 D4:1 B3:1", "A3:1 C#4:0.5 D4:0.5 E4:1 A4:1",
         "C#4:1 E4:0.5 D4:0.5 C#4:1 F#4:1", "D4:0.5 E4:0.5 F#4:0.5 E4:0.5 D4:1 B4:1", "D5:1 B4:0.5 A4:0.5 G4:1 D4:1",
         "A4:1 F#4:0.5 E4:0.5 A4:1 E4:1", "C#5:1 B4:0.5 A4:0.5 F#4:2"]
def _augment(tokens):
    out = []
    for tok in tokens.split():
        w, b = tok.rsplit(":", 1)
        out.append("%s:%g" % (w, 2 * float(eval(b, {}))))
    return " ".join(out)
_MARCH = "k:1 h:0.5 h:0.5 s:0.5 s:0.5 h:1"
PIECES.append(dict(
    id="BENCHMARK", slot="MUS_GYM", bpm=128, meter=4,
    what="all ten BENCHMARKS, UMBRA PLATEAU's CHECKPOINT and the first of the REVIEW BOARD's rooms",
    why="The leader's battle is a canon on an eight-bar subject (batch 2). In the building, before the test runs, the "
        "subject is heard alone, at half speed, with no second voice yet: the same notes the leader will set against "
        "you. 128, as the battle.",
    intro=[],
    loop=join(S("benchmark", 64, lead=_augment(" ".join(_SUBJ)),
        sing="r:32 F#5:8 D5:8 A5:8 C#5:8",
        arp=arp([(c, 8) for c in ["F#4+B4+D5", "G4+B4+D5", "F#4+A4+D5", "E4+A4+C#5"] * 2], [0, 1, 2, 1], 0.5),
        bass=pattern([(r, 8) for r in "B2 G2 D2 A2 B2 G2 D2 A2".split()], [(0, 1.5), (0, 0.5), (12, 1), (0, 1)]),
        perc=rep(_MARCH, 15) + " k:1 h:1 s:0.5 s:0.5 s:0.5 s:0.5")),
))

# ---- 6. THRESHOLD (MUS_PEWTER) ---------------------------------------------------------------------------------------
PIECES.append(dict(
    id="THRESHOLD", slot="MUS_PEWTER", bpm=112, meter=4,
    what="every gatehouse, the Underground Path's entrances, Route 2's buildings, the Day Care (22 maps)",
    why="A gatehouse stands between two places, and so does its music: every phrase stops on the dominant, a door "
        "held open, and the home chord it leans toward arrives only as the loop begins again.",
    intro=[],
    loop=join(S("threshold", 64,
        lead="F#4:1 A4:1 D5:1 C#5:1  B4:2 A4:1 F#4:1  G4:1 B4:1 D5:1 B4:1  A4:4 "
             "F#4:1 A4:1 D5:1 E5:1  F#5:2 E5:1 D5:1  G5:1 F#5:1 E5:1 B4:1  C#5:2 E5:2 "
             "r:32",
        sing="r:32 D5:2 B4:2 C#5:2 E5:2 F#5:2 C#5:2 D5:4 B4:1 D5:1 G5:2 E5:2 C#5:2 B4:1 G4:1 E4:2 A4:4",
        arp=arp([(c, 4) for c in ["D4+F#4+A4", "B3+D4+F#4", "G3+B3+D4", "A3+C#4+E4", "D4+F#4+A4", "B3+D4+F#4",
                                  "E4+G4+B4", "A3+C#4+E4", "G3+B3+D4", "A3+C#4+E4", "F#3+A3+C#4", "B3+D4+F#4",
                                  "G3+B3+D4", "A3+C#4+E4", "E4+G4+B4", "A3+C#4+E4"]], [0, 1, 2, 1], 0.5),
        bass=pattern("D3 B2 G2 A2 D3 B2 E2 A2 G2 A2 F#2 B2 G2 A2 E2 A2", [(0, 2), (7, 2)]),
        perc=rep("k:1 h:1 h:1 h:1", 16))),
))

# ---- 7. THE UNDERTONE (MUS_VIRIDIAN_FOREST) --------------------------------------------------------------------------
def _undertones(note):
    """a note's first six undertones, f/1..f/6: the octave, the twelfth, two octaves, and f/5, f/6 -- a minor chord"""
    m = F.midi(note)
    return [m, m - 12, m - 19, m - 24, m - 28, m - 31]
def _fall(note, beats=8):
    us = _undertones(note)
    return " ".join("%s:1" % K.nn(u) for u in us) + " %s:%g" % (K.nn(us[-1]), beats - len(us))
_UT = ["E5", "D5", "C5", "B4", "C5", "D5", "A4", "E5"]
PIECES.append(dict(
    id="UNDERTONE", slot="MUS_VIRIDIAN_FOREST", bpm=96, meter=4,
    what="THE UNDERTONE, DIGLETT's cave, SEAFOAM's floors, BERRY FOREST, the DUNSPARCE tunnel, PATTERN BUSH (13 maps)",
    why="An undertone is the colour beneath the colour (4.30), and in acoustics it is the mirror of an overtone: the "
        "frequency a note divides into evenly. Under each long note of the flute the harp falls through that note's "
        "first six undertones, and they make a minor chord a fifth below it, so every chord here is found underneath "
        "its melody note rather than put there: E over A minor, D over G minor, C over F minor, B over E minor.",
    intro=[],
    loop=join(S("undertone", 64,
        sing=" ".join("%s:8" % n for n in _UT),
        lead=" ".join(_fall(n) for n in _UT),
        bass=" ".join("%s:8" % K.nn(_undertones(n)[-1] + (12 if _undertones(n)[-1] < 40 else 0)) for n in _UT),
        perc=rep("h:2 h:2", 15) + " h:1 h:1 c:2")),
))

# ---- 8. CYCLING ------------------------------------------------------------------------------------------------------
_CY_LEAD = ("C4:0.5 D4:0.5 E4:0.5 G4:0.5 A4:1 G4:0.5 E4:0.5  D4:0.5 E4:0.5 C4:1 A3:2 "
            "E4:0.5 D4:0.5 E4:0.5 G4:0.5 A4:1 C5:1  A4:0.5 G4:0.5 E4:0.5 D4:0.5 G4:2 "
            "C4:0.5 D4:0.5 E4:0.5 G4:0.5 A4:1 G4:0.5 E4:0.5  C5:0.5 A4:0.5 G4:1 E4:2 "
            "D4:0.5 E4:0.5 G4:0.5 A4:0.5 G4:0.5 E4:0.5 D4:1  C4:4")
_CY_FIFTHS = [("C3+G3+C4", 4), ("A2+E3+A3", 4), ("D3+A3+D4", 4), ("G2+D3+G3", 4)] * 2
PIECES.append(dict(
    id="CYCLING", slot="MUS_CYCLING", bpm=144, meter=4,
    what="whenever the player rides, in place of the map's own music (from mid-game on, over our towns too)",
    why="BLANCHE's five notes (C D E G A, 7.14), the scale with no semitone, so it has nothing to resolve and never a "
        "reason to stop; the harmony is open fifths only, so not even a chord asks it to.",
    intro=[],
    loop=join(
        S("cycling A", 32, lead=_CY_LEAD, arp=arp(_CY_FIFTHS, [0, 1, 2, 1], 0.5),
          bass=pattern([(r, 4) for r in "C3 A2 D3 G2 C3 A2 D3 C3".split()], [(0, 0.5), (0, 0.5), (12, 0.5), (0, 0.5)]), perc=K.drums(K.ROCK_C, K.ROCK, K.FILL)),
        S("cycling B", 32, sing="G4:2 A4:2 E4:4 D4:2 E4:2 G4:4 A4:2 G4:2 E4:2 C4:2 D4:4 C4:2 D4:2",
          lead=arp(_CY_FIFTHS, [0, 1, 2, 1, 2, 1, 0, 1], 0.5),
          bass=pattern([(r, 4) for r in "C3 A2 D3 G2 C3 A2 D3 C3".split()], [(0, 0.5), (0, 0.5), (12, 0.5), (0, 0.5)]), perc=K.drums(K.ROCK_C, K.ROCK, K.FILL)),
    ),
))

# ---- 9. SURF ---------------------------------------------------------------------------------------------------------
_WAVE = [0, 1, 2, 3, 2, 1]
_SF_CH_A = [("G3+D4+G4+B4", 4), ("E3+B3+E4+G4", 4), ("C3+G3+C4+E4", 4), ("D3+A3+D4+F#4", 4), ("G3+D4+G4+B4", 4),
            ("B2+F#3+B3+D4", 4), ("C3+G3+C4+E4", 4), ("D3+A3+D4+F#4", 4)]
_SF_CH_B = [("E3+B3+E4+G4", 4), ("C3+G3+C4+E4", 4), ("G3+D4+G4+B4", 4), ("D3+A3+D4+F#4", 4), ("E3+B3+E4+G4", 4),
            ("C3+G3+C4+E4", 4), ("A2+E3+A3+C4", 2), ("D3+A3+D4+F#4", 2), ("G3+D4+G4+B4", 4)]
_SF_BASS = [(0, 4 / 3), (7, 2 / 3), (12, 4 / 3), (7, 2 / 3)]
PIECES.append(dict(
    id="SURF", slot="MUS_SURF", bpm=96, meter=4,
    what="whenever the player is on the water",
    why="On the water the music is in G, the key of blue in the spectrum-to-pitch mapping (7.2: blue, 470 nm, is G) "
        "-- DOLDRUM's key too, the becalmed sea. The harp rolls up and down each chord in threes, a swell; the flute "
        "rides it.",
    intro=[],
    loop=join(
        S("surf A", 32, sing="B4:3 A4:1 G4:2 E4:2 E5:3 D5:1 A4:4 B4:3 D5:1 F#5:2 D5:2 E5:2 G5:2 F#5:4",
          lead=arp(_SF_CH_A, _WAVE, 1 / 3), bass=pattern("G2 E2 C3 D3 G2 B2 C3 D3", _SF_BASS),
          perc=rep("h:4/3 h:2/3 h:4/3 h:2/3", 8)),
        S("surf B", 32, sing="G5:3 F#5:1 E5:2 C5:2 D5:2 B4:2 A4:4 B4:3 C5:1 E5:2 G5:2 E5:2 F#5:2 G5:4",
          lead=arp(_SF_CH_B, _WAVE, 1 / 3),
          bass=pattern([("E2", 4), ("C3", 4), ("G2", 4), ("D3", 4), ("E2", 4), ("C3", 4), ("A2", 2), ("D3", 2), ("G2", 4)], _SF_BASS),
          perc=rep("h:4/3 h:2/3 h:4/3 h:2/3", 7) + " c:4"),
    ),
))

# ---- 10. DOLDRUM: Poly and Fields (an appended slot) -----------------------------------------------------------------
_PF_HOOK = "D5:1 B5:1 A5:0.5 G5:0.5 E5:1 G5:1 D5:3"
PIECES.append(dict(
    id="DOLDRUM", slot="MUS_DOLDRUM (new; DOLDRUM's 7 maps re-pointed from MUS_FUCHSIA)", bpm=110, meter=4,
    what="DOLDRUM, its five houses and the bike shop",
    why="7.4 gave DOLDRUM G and Poly and Fields, which is in G: its hook (D B A G E G D, 4.20) over its own chords, "
        "G, E minor, C, D, at its own 110. DOLDRUM is a becalmed sea, so the bass never leaves G: the chords change "
        "above a sea that does not move.",
    intro=[],
    loop=join(
        S("doldrum A", 32,
          sing=cat(_PF_HOOK, "E5:1 G5:1 C6:1 B5:1 A5:2 F#5:2", rest(16)),
          lead=cat(rest(16), shift(_PF_HOOK, -12), "E4:1 G4:1 A4:1 B4:1 A4:2 F#4:2"),
          arp=arp([(c, 4) for c in ["G3+B3+D4", "E3+G3+B3", "C4+E4+G3", "D4+F#3+A3"] * 2], [0, 1, 2, 1], 0.5),
          bass=rep("G2:2 G3:1 G2:1", 8), perc=rep("k:2 h:1 h:1", 8)),
        S("doldrum B", 32, sing="B5:2 G5:2 E5:2 C5:2 D5:2 B4:2 A4:4 G5:2 E5:2 C6:2 G5:2 F#5:2 A5:2 D5:4",
          lead=arp([(c, 4) for c in ["E3+G3+B3", "C4+E4+G3", "G3+B3+D4", "D4+F#3+A3", "E3+G3+B3", "C4+E4+G3",
                                     "D4+F#3+A3", "D4+F#3+A3"]], [0, 1, 2, 1, 2, 1, 0, 1], 0.5),
          bass=rep("G2:2 G3:1 G2:1", 8), perc=rep("k:2 h:1 h:1", 7) + " k:1 h:1 c:2"),
    ),
))

# ---- 11. LURID: ScornSolutions Blues (an appended slot) --------------------------------------------------------------
_HOOK = "E4:2/3 G4:1/3 B4:1 A4:2/3 G4:1/3 E4:1"
_BLUES = cat(_HOOK, "r:2 D4:2/3 E4:1/3 G4:1", _HOOK, "r:2 B3:2/3 D4:1/3 E4:1",
             shift(_HOOK, 5), "r:2 G4:2/3 A4:1/3 C5:1", _HOOK, "r:2 D4:2/3 E4:1/3 G4:1",
             "B4:2/3 D#5:1/3 F#5:1 A5:2/3 F#5:1/3 D#5:1", "C5:2/3 B4:1/3 A4:1 G4:2/3 E4:1/3 G4:1",
             "E4:2/3 G4:1/3 B4:1 G4:2/3 E4:1/3 D4:1", "F#4:2 D#4:2")
def _first_bars(tokens, beats):
    out, t = 0, 0.0
    for tok in tokens.split():
        if t >= beats - 1e-9:
            break
        t += float(eval(tok.rsplit(":", 1)[1], {})); out += 1
    return out
_NB8 = _first_bars(_BLUES, 32)                       # the flute's chorus an octave up for eight bars, then down
_BOOGIE = [(0, 2 / 3), (0, 1 / 3), (7, 2 / 3), (7, 1 / 3), (10, 2 / 3), (10, 1 / 3), (7, 2 / 3), (7, 1 / 3)]
_TWELVE = "E2 E2 E2 E2 A2 A2 E2 E2 B2 A2 E2 B2"
_STABS = lambda chs: " ".join("r:2/3 %s:1/3 r:2/3 %s:1/3 r:2/3 %s:1/3 r:2/3 %s:1/3" % (c, c, c, c) for c in chs)
_LCH = ["E4+G4+B4"] * 4 + ["A3+C4+E4"] * 2 + ["E4+G4+B4"] * 2 + ["D#4+F#4+A4", "A3+C4+E4", "E4+G4+B4", "D#4+F#4+A4"]
_SHUFFLE = "k:2/3 h:1/3 s:2/3 h:1/3 k:2/3 h:1/3 s:2/3 h:1/3"
PIECES.append(dict(
    id="LURID", slot="MUS_LURID (new; LURID's 7 maps re-pointed from MUS_FUCHSIA)", bpm=118, meter=4,
    what="LURID, its three houses, the warden's house, the gates of THE WALLED GARDEN",
    why="7.4 gave LURID E and ScornSolutions Blues, which is in E minor: so a twelve-bar blues in E minor at its "
        "118, on its hook (E G B A G E, 7.11), the harp's chorus and then the flute's, every hook answered by a "
        "lick. Scorn's own song, in the town 7.4 placed it in.",
    intro=[],
    loop=join(
        S("lurid 1", 48, lead=_BLUES, harm=_STABS([c.split("+")[1] for c in _LCH]),
          bass=pattern(_TWELVE, _BOOGIE), perc=cat("c:2/3 h:1/3 s:2/3 h:1/3 k:2/3 h:1/3 s:2/3 h:1/3", rep(_SHUFFLE, 11))),
        S("lurid 2", 48, sing=cat(shift(" ".join(_BLUES.split()[:_NB8]), 12), " ".join(_BLUES.split()[_NB8:])), lead=_STABS([c.split("+")[0] for c in _LCH]),
          bass=pattern(_TWELVE, _BOOGIE), perc=cat("c:2/3 h:1/3 s:2/3 h:1/3 k:2/3 h:1/3 s:2/3 h:1/3", rep(_SHUFFLE, 10),
                                                   "k:2/3 s:1/3 s:2/3 s:1/3 s:2/3 s:1/3 s:2/3 s:1/3")),
    ),
))


# ---------------------------------------------------------------------------------------------------------------------
# The engine
# ---------------------------------------------------------------------------------------------------------------------
for _p in PIECES:
    if not _p["intro"]:
        _p["intro"] = [("perc", "r:0")]


def engine():
    """{path: new contents} for every file this writes."""
    out, cfg = {}, open(CFG, encoding="utf-8").read()
    table = open(TABLE, encoding="utf-8").read()
    h = open(SONGS_H, encoding="utf-8").read()
    ld = open(LD, encoding="utf-8").read()
    for p in PIECES:
        GB.check(p)
        f = FILES[p["id"]]
        out[os.path.join(MIDI_DIR, f + ".mid")] = GB.song_midi(p)
        if p["id"] in NEW:
            const, what = NEW[p["id"]]
            if not re.search(r"^%s\.mid:" % f, cfg, re.M):
                last = list(re.finditer(r"^(?:se_nightfall|mus_doldrum|mus_lurid)\.mid:.*\n", cfg, re.M))[-1]
                cfg = cfg[:last.end()] + "%-31s-E -R50 -G%03d -V090\n" % (f + ".mid:", VOICEGROUP) + cfg[last.end():]
            if ("song %s," % f) not in table:
                last = list(re.finditer(r"^\tsong (?:se_nightfall|mus_doldrum|mus_lurid), \d+, \d+\n", table, re.M))[-1]
                table = table[:last.end()] + "\tsong %s, 0, 0\n" % f + table[last.end():]
            if not re.search(r"^#define %s\s" % const, h, re.M):
                ids = [int(x) for x in re.findall(r"^#define (?:SE|MUS)_\w+\s+(\d+)\b(?!x)", h, re.M)]
                last = list(re.finditer(r"^#define (?:SE_NIGHTFALL|MUS_DOLDRUM|MUS_LURID)\s.*\n", h, re.M))[-1]
                line = "#define %-25s %d   // T-565 batch 5: %s (DAEMONS tools/genoverworldmusic.py)\n" % (const, max(ids) + 1, what)
                h = h[:last.end()] + line + h[last.end():]
            obj = "        sound/songs/midi/%s.o(.rodata);\n" % f
            if obj not in ld:
                last = list(re.finditer(r"^        sound/songs/midi/(?:se_nightfall|mus_doldrum|mus_lurid)\.o\(\.rodata\);\n", ld, re.M))[-1]
                ld = ld[:last.end()] + obj + ld[last.end():]
        else:
            cfg, k = re.subn(r"^(%s\.mid:\s+.*?)-G\d+" % re.escape(f), r"\g<1>-G%03d" % VOICEGROUP, cfg, flags=re.M)
            assert k == 1, "midi.cfg has no line for %s" % f
    out[CFG], out[TABLE], out[SONGS_H], out[LD] = cfg, table, h, ld
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
    lens = ", ".join("%s %.0f s" % (p["id"], GB.section_len(p["loop"]) * 60 / p["bpm"]) for p in PIECES)
    print("  %d overworld pieces on voicegroup%03d; loops: %s" % (len(PIECES), VOICEGROUP, lens))
    if not changed:
        print("  the game: unchanged")
    else:
        print("  the game: %s %d file(s): %s" % ("wrote" if "--write" in sys.argv else "would write", len(changed),
                                                 ", ".join(changed[:6]) + (" ..." if len(changed) > 6 else "")))


if __name__ == "__main__":
    main()
