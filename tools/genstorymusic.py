#!/usr/bin/env python3
"""T-565 batch 8: the story set-pieces -- ours, in place of pret's fifteen, and THE WALLED GARDEN's own.

    python3 tools/genstorymusic.py            # report: is the engine current
    python3 tools/genstorymusic.py --write    # write it into engineGba

THE VOICE (the user, 2026-11-17, from one reel of sixteen drafts in voice C): "All sixteen", and THE WALLED GARDEN
"its own slot". genfanfares.py's voicegroup195, as the fanfares, the battle music and the overworld: the HARP and FLUTE
on the tunes, the cartridge under them. CONTAINMENT (vision 7.13) decided the hooks: CRYSTAL CLEAR's only where she is
(her entrance, her lab, her speech's two), AL CLEAR's champion figure only in his two, nobody's on a shared place.

THE CREDITS are a medley of the game's own music in the order it is met, read from genoverworldmusic.py's and
genbattlemusic.py's notes and this file's, each passage at its own tempo, from CRYSTAL's lament to her Reply. They and
NEW_GAME_EXIT play once: no loop markers (a loop of no length would hang the sound driver).

WHAT IT WRITES (engineGba/)
    sound/songs/midi/<slot>.mid      fifteen over pret's in place, and mus_walled_garden (new)
    sound/songs/midi/midi.cfg        each of the fifteen's -G to 195; the new song's line
    sound/song_table.inc, include/constants/songs.h, ld_script.ld   the new song (four lines, engine.md trap 25)
tools/port_music.py's MAP_MUSIC points THE WALLED GARDEN's nine maps at it (the game lane's go-ahead, 2026-11-17).
Each piece's reason is its "why" below. Every note DRAFT.
"""
import os, re, struct, sys

import genbattlemusic as GB
import genfanfares as G
import genoverworldmusic as GO

K = GB
pattern, arp, fb, shift = GO.pattern, GO.arp, GO.fb, GO.shift
S, join, rest, rep, cat, dia = GB.S, GB.join, GB.rest, GB.rep, GB.cat, GB.dia
GBA, MIDI_DIR, CFG = G.GBA, G.MIDI_DIR, G.CFG
TABLE, SONGS_H, LD = G.TABLE, G.SONGS_H, G.LD
VOICEGROUP, TPB = G.VOICEGROUP, G.TPB
FILES = {"OAK": "mus_oak", "OAK_LAB": "mus_oak_lab", "NEW_GAME_INSTRUCT": "mus_new_game_instruct",
         "NEW_GAME_EXIT": "mus_new_game_exit", "ENCOUNTER_RIVAL": "mus_encounter_rival", "RIVAL_EXIT": "mus_rival_exit",
         "ENCOUNTER_GYM_LEADER": "mus_encounter_gym_leader", "SS_ANNE": "mus_ss_anne",
         "ROCKET_HIDEOUT": "mus_rocket_hideout", "DAEMON_TOWER": "mus_poke_tower", "UMBRAL_ASCENT": "mus_victory_road",
         "TRAINER_TOWER": "mus_trainer_tower", "THE_RECORD": "mus_hall_of_fame", "SLOW_PALLET": "mus_slow_pallet",
         "WALLED_GARDEN": "mus_walled_garden", "CREDITS": "mus_credits"}
NEW = {"WALLED_GARDEN": ("MUS_WALLED_GARDEN", "THE WALLED GARDEN's own: a tune inside its walls, light falling in")}

# ---------------------------------------------------------------------------------------------------------------------
# THE PIECES (carried verbatim from the drafts the user heard)
# ---------------------------------------------------------------------------------------------------------------------
PIECES = []

def chords(chs, beats=4):
    return [(c, beats) for c in chs]

# ---- 1. OAK: CRYSTAL CLEAR's entrance -------------------------------------------------------------------------------
_HOOK = "A4:0.5 E5:0.5 D5:0.5 C5:0.5 B4:0.5 C5:0.5 D5:3 r:2"
_FALL = "F5:1 E5:1 D5:1 C5:1 B4:2 G#4:2"
_LAMENT = ["A3+C4+E4", "G3+B3+D4", "F3+A3+C4", "E3+G#3+B3"]
PIECES.append(dict(
    id="OAK", slot="MUS_OAK", bpm=128, meter=4,
    what="CRYSTAL CLEAR's entrance in BLANCHE: she stops you at the grass and walks you to her lab",
    why="Her hook (A E D C B C D, A minor, 128 -- vision 7.6), only where she is, as DEX_RATING has it (7.13). It is "
        "set over the lament bass, A G F E, the falling four notes that have meant a lament since Dido's; the hook is "
        "left on D, unresolved, and the answer falls to E. She opens in the minor (4.17).",
    intro=join(S("oak intro", 4, lead="E4:0.5 A4:0.5 C5:0.5 E5:0.5 r:2", bass="A2:4", perc="r:2 h:0.5 h:0.5 s:1")),
    loop=join(S("oak", 32,
        lead=cat(_HOOK, _FALL, arp(chords(["A3+E4+A4+C5", "G3+D4+G4+B4", "F3+C4+F4+A4", "E3+B3+E4+G#4"]),
                                   [0, 1, 2, 3, 2, 1, 2, 1], 0.5)),
        sing=cat(rest(16), _HOOK, _FALL),
        arp=arp(chords(_LAMENT * 2), [0, 1, 2, 1], 0.5),
        bass=rep("A2:2 A2:1 E2:1 G2:2 G2:1 D2:1 F2:2 F2:1 C3:1 E2:2 E2:1 B2:1", 2),
        perc=cat(rep(K.LIGHT, 7), K.FILL_LIGHT))),
))

# ---- 2. OAK_LAB: her lab, Crystal's Reply -----------------------------------------------------------------------------
_REPLY = "E4:1 C#5:1 B4:0.5 A4:0.5 G#4:1 A4:1 F#4:3"
_REPLY_CH = ["A3+C#4+E4", "F#3+A3+C#4", "D4+F#4+A4", "E3+G#3+B3"]
PIECES.append(dict(
    id="OAK_LAB", slot="MUS_OAK_LAB", bpm=128, meter=4,
    what="CRYSTAL CLEAR's lab",
    why="Crystal's Reply (4.17): the same address as her lament, A at 128, in the major -- its hook (E C# B A G# A F#) "
        "over its own I-vi-IV-V, A, F# minor, D, E, the one progression of hers that holds a minor chord and still "
        "resolves. The lab is the one place that is only hers.",
    intro=join(S("lab intro", 4, lead="E4:0.5 A4:0.5 C#5:0.5 E5:0.5 r:2", bass="A2:4", perc="r:4")),
    loop=join(S("lab", 32,
        lead=cat(_REPLY, "D5:1 F#5:1 E5:1 D5:1 C#5:2 B4:2",
                 arp(chords(["A3+E4+A4+C#5", "F#3+C#4+F#4+A4", "D4+A4+D5+F#5", "E3+B3+E4+G#4"]), [0, 1, 2, 3, 2, 1, 2, 1], 0.5)),
        sing=cat(rest(16), shift(_REPLY, 12), "A5:2 F#5:2 G#5:2 B5:2"),
        arp=arp(chords(_REPLY_CH * 2), [0, 1, 2, 1], 0.5),
        bass=rep("A2:2 E2:2 F#2:2 C#3:2 D3:2 A2:2 E2:2 B2:2", 2),
        perc=rep("k:1 h:1 h:1 h:1", 8))),
))

# ---- 3. NEW_GAME_INSTRUCT: before she speaks ---------------------------------------------------------------------------
PIECES.append(dict(
    id="NEW_GAME_INSTRUCT", slot="MUS_NEW_GAME_INSTRUCT", bpm=128, meter=4,
    what="the new game's first pages, before CRYSTAL CLEAR's speech",
    why="The Reply's four chords, broken on the harp, and no tune: her harmony before she has said anything. The tune "
        "is kept for the moment the player leaves (NEW_GAME_EXIT).",
    intro=[],
    loop=join(S("instruct", 16, lead=arp(chords(["A3+E4+A4+C#5", "F#3+C#4+F#4+A4", "D4+A4+D5+F#5", "E3+B3+E4+G#4"]),
                                         [0, 1, 2, 3, 2, 1, 2, 1], 0.5),
                sing="C#5:4 C#5:4 D5:4 B4:4", bass="A2:4 F#2:4 D3:4 E2:4")),
))

# ---- 4. NEW_GAME_EXIT: leaving into the world (plays once) -------------------------------------------------------------
PIECES.append(dict(
    id="NEW_GAME_EXIT", slot="MUS_NEW_GAME_EXIT", bpm=128, meter=4, jingle=True,
    what="the player shrinking into the world at the end of the new game",
    why="The Reply's hook, once: of every hook in the corpus it is the one that ends somewhere other than where it "
        "began, E to F# (4.20's note on the Scorn hooks), so it plays as the player leaves.",
    intro=join(S("exit", 5, lead="E4:0.5 C#5:0.5 B4:0.5 A4:0.5 G#4:0.5 A4:0.5 F#4:2",
                 sing="r:3 A4:2", bass="A2:3 D2:2", perc="r:3 c:2")),
    loop=[],
))

# ---- 5, 6. AL CLEAR: the rival's two ------------------------------------------------------------------------------------
_AL = ("E5:0.75 E5:0.75 D5:0.5 C5:1 B4:0.5 C5:0.5  A4:2 r:1 C5:0.5 D5:0.5 "
       "E5:0.75 E5:0.75 D5:0.5 C5:1 D5:0.5 E5:0.5  D5:2 r:1 B4:0.5 C5:0.5")
_AL_BASS = pattern("A2 F2 C3 G2", [(0, 0.75), (0, 0.75), (12, 0.5), (0, 0.5), (0, 0.5), (12, 0.5), (0, 0.5)])
PIECES.append(dict(
    id="ENCOUNTER_RIVAL", slot="MUS_ENCOUNTER_RIVAL", bpm=128, meter=4,
    what="AL CLEAR appearing, in all eight of his scenes",
    why="AL is the prevailing paradigm (1), and his champion's battle is built of the most prevailing things in pop "
        "(batch 2). He does not change (4.3: \"No arc\"), so he arrives with that battle's own first four bars from the "
        "very first meeting: A minor, F, C, G, three-three-two.",
    intro=join(S("rival intro", 4, lead="E4:0.5 G#4:0.5 B4:0.5 D5:0.5 E5:2", bass="E2:2 E3:2", perc="s:0.5 s:0.5 s:0.5 s:0.5 c:2")),
    loop=join(S("rival", 16, lead=_AL, arp=arp(chords(["A3+C4+E4", "F3+A3+C4", "C4+E4+G3", "G3+B3+D4"]), [0, 1, 2, 1], 0.25),
                bass=_AL_BASS, perc=rep(K.POP, 4))),
))
PIECES.append(dict(
    id="RIVAL_EXIT", slot="MUS_RIVAL_EXIT", bpm=128, meter=4,
    what="AL CLEAR walking off after each of his scenes",
    why="He leaves exactly as he came: the same four bars, the band thinned out behind him -- the harp, the bass and "
        "the hats.",
    intro=[],
    loop=join(S("exit", 16, lead=_AL, bass=_AL_BASS, perc=rep("h:0.5 h:0.5 h:0.5 h:0.5 h:0.5 h:0.5 h:0.5 h:0.5", 4))),
))

# ---- 7. ENCOUNTER_GYM_LEADER: a BENCHMARK's summons ---------------------------------------------------------------------
_SUBJ = ["B3:1 D4:0.5 F#4:0.5 D4:1 B3:1", "D4:1 G4:0.5 F#4:0.5 D4:1 B3:1", "A3:1 C#4:0.5 D4:0.5 E4:1 A4:1",
         "C#4:1 E4:0.5 D4:0.5 C#4:1 F#4:1"]
PIECES.append(dict(
    id="ENCOUNTER_GYM_LEADER", slot="MUS_ENCOUNTER_GYM_LEADER", bpm=128, meter=4,
    what="the sixteen set pieces before a leader, an ELITE FOUR and the summits (THE NEXUS uses it too)",
    why="The leader's canon subject (batch 2) stated as a summons in octaves, then its first four bars with the second "
        "voice already falling in a bar behind: the test about to run.",
    intro=join(S("summons", 8, lead=cat(_SUBJ[0], _SUBJ[1]), sing=shift(cat(_SUBJ[0], _SUBJ[1]), 12),
                 bass="B2:4 G2:4", perc="c:1 r:3 s:0.5 s:0.5 s:0.5 s:0.5 s:1 s:1")),
    loop=join(S("canon", 16, lead=" ".join(_SUBJ), sing=cat(rest(4), shift(" ".join(_SUBJ[:3]), 12)),
                bass=pattern([(r, 4) for r in "B2 G2 D2 A2".split()], [(0, 1.5), (0, 0.5), (12, 1), (0, 1)]),
                perc=rep("k:1 h:0.5 h:0.5 s:0.5 s:0.5 h:1", 4))),
))

# ---- 8. SS_ANNE: a waltz (bars of three) --------------------------------------------------------------------------------
_WA = "E5:2 D5:1 C5:2 E5:1 D5:2 F5:1 B4:3 F5:2 D5:1 B4:2 D5:1 C5:2 E5:1 G5:3 " \
      "A5:2 G5:1 F5:2 A5:1 G5:2 E5:1 C5:3 F5:2 E5:1 D5:2 B4:1 C5:3 C5:3"
_WA_CH = "C C G7 G7 G7 G C C F F C C Dm G7 C C".split()
_WB = "A4:2 C5:1 E5:2 A5:1 F5:2 E5:1 D5:3 B4:2 D5:1 G5:2 F5:1 E5:2 D5:1 C5:3 " \
      "A4:2 C5:1 B4:2 G#4:1 A4:2 E5:1 F5:3 E5:2 C5:1 D5:2 B4:1 C5:3 G4:3"
_WB_CH = "Am Am Dm Dm G G C C Am E Am F C G7 C G7".split()
_ROOT = {"C": "C3", "G7": "G2", "G": "G2", "F": "F2", "Dm": "D3", "Am": "A2", "E": "E2"}
_PAH = {"C": ("E4", "G4"), "G7": ("D4", "F4"), "G": ("D4", "B3"), "F": ("A3", "C4"), "Dm": ("F4", "A3"), "Am": ("C4", "E4"),
        "E": ("G#3", "B3")}
def _waltz(chs):
    return (" ".join("%s:1 r:2" % _ROOT[c] for c in chs), " ".join("r:1 %s:1 %s:1" % _PAH[c] for c in chs))
_wab, _wap = _waltz(_WA_CH)
_wbb, _wbp = _waltz(_WB_CH)
PIECES.append(dict(
    id="SS_ANNE", slot="MUS_SS_ANNE", bpm=132, meter=3,
    what="the S.S. ANNE, all 26 of her rooms, one visit",
    why="A liner's waltz, in ARDOR's key, C, the port she lies in: THE LIVERY carried her outside into her rooms (T-447), "
        "and this carries the town she is moored at aboard. The flute leads the first sixteen bars and the harp the "
        "next, in A minor.",
    intro=[],
    loop=join(S("waltz A", 48, sing=_WA, bass=_wab, arp=_wap, perc=rep("k:1 h:1 h:1", 16)),
              S("waltz B", 48, lead=_WB, bass=_wbb, arp=_wbp, perc=rep("k:1 h:1 h:1", 15) + " k:1 s:1 s:1")),
))

# ---- 9. ROCKET_HIDEOUT: something running underneath -------------------------------------------------------------------
_CELL = "E4:1 F4:0.5 E4:0.5 G4:1 F#4:1 E4:2 r:2"
PIECES.append(dict(
    id="ROCKET_HIDEOUT", slot="MUS_ROCKET_HIDEOUT", bpm=136, meter=4,
    what="the hideout under VERDIGRIS, the POWER PLANT, DOLDRUM CAVE, the warehouse, one of the REVIEW BOARD's rooms",
    why="Under every map here something runs unattended, which is what a daemon is (1): a pulse a tritone wide that "
        "never resolves (E and A#), a bass that never moves, and a figure that creeps up a semitone every four bars "
        "and drops back.",
    intro=[],
    loop=join(S("hideout", 64, lead=" ".join(shift(rep(_CELL, 2), k) for k in range(4)),
                sing="B5:16 C6:16 C#6:16 D6:16", arp=rep("E4:0.5 A#4:0.5", 64),
                bass=rep("E2:0.5 E2:0.5 E3:0.5 E2:0.5", 32),
                perc=cat(rep("k:0.5 h:0.5 h:0.5 h:0.5 k:0.5 h:0.5 s:0.5 h:0.5", 15), K.FILL))),
))

# ---- 10. POKE_TOWER: DAEMON TOWER -----------------------------------------------------------------------------------------
_TW = "D5 F5 A5 F5 D5 F5 Bb4 D5 G5 F5 E5 D5 C#5 E5 A4 C#5 D5 E5 F5 A5 C6 A5 F5 C5 Bb4 D5 C#5 E5 D5 A4 F4 D4".split()
_TW_CH = ["D4+F4+A4", "Bb3+D4+F4", "G3+Bb3+D4", "A3+C#4+E4", "D4+F4+A4", "F3+A3+C4", "G3+Bb3+D4", "D4+F4+A4"]
PIECES.append(dict(
    id="DAEMON_TOWER", slot="MUS_POKE_TOWER", bpm=92, meter=4,
    what="DAEMON TOWER's seven floors in HALFTONE, and one of the REVIEW BOARD's rooms",
    why="HALFTONE's key, D minor (7.4), and a halftone is a line drawn in dots (3.1): the tune is split note by note "
        "between the harp and the flute, neither playing it whole. Then both play every note, the line continuous, "
        "and the broken chords come in: the tower is where the torn book is mended and colour comes back.",
    intro=[],
    loop=join(
        S("dots", 32, lead=" ".join(("%s:1" % n) if i % 2 == 0 else "r:1" for i, n in enumerate(_TW)),
          sing=" ".join(("%s:1" % n) if i % 2 == 1 else "r:1" for i, n in enumerate(_TW)),
          bass="D3:4 Bb2:4 G2:4 A2:4 D3:4 F2:4 G2:2 A2:2 D2:4"),
        S("line", 32, lead=" ".join("%s:1" % n for n in _TW), sing=" ".join("%s:1" % n for n in _TW),
          arp=arp(chords(_TW_CH), [0, 1, 2, 1], 0.5), bass="D3:4 Bb2:4 G2:4 A2:4 D3:4 F2:4 G2:2 A2:2 D2:4",
          perc=rep("k:1 h:1 h:1 h:1", 8))),
))

# ---- 11. VICTORY_ROAD: THE UMBRAL ASCENT -----------------------------------------------------------------------------------
def _step(k):
    r = 36 + k
    n = lambda d: GB.nn(r + d)
    riff = "%s:0.5 %s:0.5 %s:0.5 %s:0.5 %s:0.5 %s:0.5 %s:0.5 %s:0.5 %s:1 %s:0.5 %s:0.5 %s:2" % (
        n(12), n(15), n(19), n(15), n(12), n(15), n(19), n(22), n(24), n(22), n(19), n(15))
    return riff, "%s:8" % n(31), " ".join("%s:0.5 %s:0.5 %s:0.5 %s:0.5" % (n(0), n(0), n(12), n(0)) for _ in range(4))
_ST = [_step(k) for k in range(12)]
PIECES.append(dict(
    id="UMBRAL_ASCENT", slot="MUS_VICTORY_ROAD", bpm=132, meter=4,
    what="THE UMBRAL ASCENT, Route 23, UMBRA PLATEAU's door, the last two rooms of the REVIEW BOARD",
    why="UMBRA is the floor, and where colour arrives (7.4): low in register, as black is, and climbing a semitone "
        "every two bars through all twelve -- every key a colour has, C to A, and the two the spectrum leaves dark, "
        "A# and B (7.3) -- until the loop is back at the floor: an ascent that never arrives.",
    intro=[],
    loop=join(S("ascent", 96, lead=" ".join(s[0] for s in _ST), sing=" ".join(s[1] for s in _ST),
                bass=" ".join(s[2] for s in _ST), perc=cat(rep(K.ROCK, 23), K.FILL))),
))

# ---- 12. TRAINER_TOWER ------------------------------------------------------------------------------------------------------
_TT = lambda r: " ".join("%s:0.5" % GB.nn(GB.midi(r) + d) for d in [0, 7, 12, 7, 10, 7, 5, 7])
_TT_BLOCKS = ["E4", "F#4", "G4", "A4"]
PIECES.append(dict(
    id="TRAINER_TOWER", slot="MUS_TRAINER_TOWER", bpm=140, meter=4,
    what="TRAINER TOWER on SEVEN ISLAND, its floors and its roof (11 maps)",
    why="A race against the clock: the hats tick in sixteenths and never change, and the riff climbs a step every four "
        "bars, E, F#, G, A, a floor at a time.",
    intro=[],
    loop=join(S("tower", 64, lead=" ".join(rep(_TT(r), 4) for r in _TT_BLOCKS),
                sing=" ".join("%s:4 %s:4 %s:4 %s:4" % (GB.nn(GB.midi(r) + 12), GB.nn(GB.midi(r) + 15), GB.nn(GB.midi(r) + 14),
                                                       GB.nn(GB.midi(r) + 10)) for r in _TT_BLOCKS),
                bass=" ".join(rep("%s:0.5" % GB.nn(GB.midi(r) - 24), 32) for r in _TT_BLOCKS),
                perc=cat(rep(K.SIXTEENS, 15), K.FILL))),
))

# ---- 13. HALL_OF_FAME: THE RECORD ---------------------------------------------------------------------------------------------
_REC = "C5:1 D5:1 E5:1 G5:1 A5:2 B5:1 C6:1 C6:3 G5:1 A5:2 E5:2 F5:1 A5:1 C6:2 G5:2 E5:2 F5:2 D5:1 B4:1 C5:4"
_REC_CH = [("C4+E4+G4", 4), ("F3+A3+C4", 2), ("G3+B3+D4", 2), ("C4+E4+G4", 4), ("A3+C4+E4", 4), ("F3+A3+C4", 4),
           ("C4+E4+G4", 4), ("D4+F4+A3", 2), ("G3+B3+D4", 2), ("C4+E4+G4", 4)]
PIECES.append(dict(
    id="THE_RECORD", slot="MUS_HALL_OF_FAME", bpm=104, meter=4,
    what="THE RECORD: the party entered in the institution's register after the REVIEW BOARD",
    why="BADGE climbs C D E G A and stops on A, the last colour before the two notes that have none (7.14). The "
        "institution records it as complete: here the climb runs on through B to the octave, the one piece in the game "
        "that closes the octave the spectrum leaves open (7.3).",
    intro=join(S("record intro", 4, lead="G3:0.5 C4:0.5 E4:0.5 G4:0.5 C5:2", bass="C3:4", perc="s:0.25 s:0.25 s:0.25 s:0.25 s:1 c:2")),
    loop=join(S("record A", 32, sing=_REC, arp=arp(_REC_CH, [0, 1, 2, 1], 0.5),
                bass="C3:2 G2:2 F2:2 G2:2 C3:2 E3:2 A2:2 E2:2 F2:2 C3:2 C3:2 G2:2 D3:2 G2:2 C3:4",
                perc=cat(K.STATELY_C, rep(K.STATELY, 6), "k:1 h:1 s:0.5 s:0.5 s:0.5 s:0.5")),
              S("record B", 32, lead=shift(_REC, -12), sing=dia(_REC, "C D E F G A B", 2), arp=arp(_REC_CH, [0, 1, 2, 1], 0.5),
                bass="C3:2 G2:2 F2:2 G2:2 C3:2 E3:2 A2:2 E2:2 F2:2 C3:2 C3:2 G2:2 D3:2 G2:2 C3:4",
                perc=cat(K.STATELY_C, rep(K.STATELY, 6), "k:1 h:1 s:0.5 s:0.5 s:0.5 s:0.5"))),
))

# ---- 14. SLOW_PALLET: BLANCHE, slowed ----------------------------------------------------------------------------------------
_BL1 = ("G4:1 E4:1/2 G4:1/2 A4:1 G4:1 E4:1 D4:1/2 E4:1/2 G4:2 A4:1 G4:1/2 E4:1/2 D4:1 C4:1 A3:1 C4:1/2 D4:1/2 E4:2 "
        "A4:1 E5:1 D5:1 C5:1 B4:1 C5:1 D5:2 A4:1 E5:1 D5:1 C5:1 B4:1 C5:1 D5:2")
_BL2 = "C3:1 G3:1 E3:1 G3:1 A3:1 G3:1 E3:1 D3:1 C3:1 E3:1 G3:1 E3:1 D3:1 C3:1 A2:1 C3:1 F3:2 A3:2 G3:2 B3:2 A3:2 C4:2 E3:2 A3:2"
_BL3 = "C3:2 G2:2 C3:2 D3:2 E3:2 A2:2 G3:2 C3:2 F2:2 F2:2 G2:2 G2:2 A2:2 A2:2 A2:2 A2:2"
PIECES.append(dict(
    id="SLOW_PALLET", slot="MUS_SLOW_PALLET", bpm=76, meter=4,
    what="the room where the record is kept, and the champion's room once it is over",
    why="BLANCHE's own theme (7.14), its three lines exactly as the town plays them, at half its speed: home, heard "
        "from the far end of the game. Its second half is CRYSTAL's hook, as it is in the town (7.13). The flute "
        "carries it first, then the harp.",
    intro=[],
    loop=join(S("blanche 1", 32, sing=_BL1, lead=shift(_BL2, 12), bass=_BL3),
              S("blanche 2", 32, lead=_BL1, sing=shift(_BL2, 24), bass=_BL3)),
))

# ---- 15. WALLED_GARDEN (an appended slot; the Safari Zone plays MUS_EVOLUTION today) -----------------------------------------
_WG = "G#4:2 B4:2 A4:3 G#4:1 F#4:2 E4:2 F#4:4 G#4:1 A4:1 B4:2 A4:2 F#4:2 G#4:2 F#4:2 E4:4 " \
      "G#4:2 E4:2 A4:2 B4:2 B4:3 A4:1 F#4:4 E4:2 G#4:2 A4:2 F#4:2 F#4:1 G#4:1 A4:2 E4:4"
_WG_CH = "E A E B E A B E C#m A E B C#m A B E".split()
_LIGHT = {"E": "E5+G#5+B5+E6", "A": "A4+C#5+E5+A5", "B": "B4+D#5+F#5+B5", "C#m": "C#5+E5+G#5+C#6"}
_WG_ROOT = {"E": "E2", "A": "A2", "B": "B2", "C#m": "C#3"}
PIECES.append(dict(
    id="WALLED_GARDEN", slot="MUS_WALLED_GARDEN (new; the Safari Zone's 9 maps re-pointed from MUS_EVOLUTION)", bpm=100, meter=4,
    what="THE WALLED GARDEN's areas and rest houses, which play the evolution music today",
    why="THE WALLED GARDEN's rooms are a glasshouse: light comes in, and nothing is seen out (T-540). The tune never "
        "leaves the five notes between E and B, the garden's walls, while the harp's light falls in from two octaves "
        "above. In LURID's key, E: the garden is LURID's.",
    intro=[],
    loop=join(S("garden", 64, sing=_WG, lead=arp([(_LIGHT[c], 4) for c in _WG_CH], [0, 1, 2, 3, 2, 1, 2, 1], 0.5),
                bass=" ".join("%s:4" % _WG_ROOT[c] for c in _WG_CH), perc=rep("h:2 h:2", 16))),
))

# ---- 16. CREDITS: a medley in the order the game is met, CRYSTAL's first song to her last -------------------------------------
def _slice(tokens, a, b):
    out, t = [], 0.0
    for tok in tokens.split():
        w, d = tok.rsplit(":", 1); d = float(eval(d, {}))
        s, e = t, t + d; t = e
        lo, hi = max(s, a), min(e, b)
        if hi - lo <= 1e-9:
            continue
        keep = w if s >= a - 1e-9 else "r"              # a note begun before the cut is heard as a rest
        out.append("%s:%s" % (keep, fb(hi - lo)))
    return " ".join(out)

def _section(p, a, b):
    """the loop of piece p between beats a and b, every role cut to it"""
    return [(role, _slice(tok, a, b)) for role, tok in p["loop"]]

def _find(pid):
    for src in (PIECES, GO.PIECES, GB.PIECES):
        for p in src:
            if p["id"] == pid:
                return p
    raise KeyError(pid)

CREDITS_PLAN = [("OAK", 0, 32), ("ROUTE3", 0, 32), ("CHECKPOINT", 0, 32), ("DOLDRUM", 0, 32), ("SS_ANNE", 0, 48),
                ("LURID", 0, 48), ("DAEMON_TOWER", 32, 64), ("UNDERTONE", 0, 32), ("SURF", 0, 32), ("CYCLING", 0, 32),
                ("VS_WILD", 0, 48), ("VS_GYM_LEADER", 32, 64), ("UMBRAL_ASCENT", 0, 48), ("VS_CHAMPION", 0, 32),
                ("THE_RECORD", 0, 32), ("OAK_LAB", 0, 32), ("OAK_LAB", 0, 32)]
CODA = [("lead", "A3+C#4+E4:8"), ("sing", "A5:8"), ("bass", "A2:8"), ("perc", "c:8")]
PIECES.append(dict(
    id="CREDITS", slot="MUS_CREDITS", bpm=128, meter=4, credits=True,
    what="the credits, once, at the end",
    why="The game's own music in the order a player meets it, each piece a short passage at its own tempo -- BLANCHE "
        "to the REVIEW BOARD -- opening on CRYSTAL's lament and closing on her Reply, held on A major: \"her first song "
        "in this story and her last are the identical harmonic address\" (4.17).",
    intro=[], loop=[],
))


# ---------------------------------------------------------------------------------------------------------------------
# The MIDI: loops as genbattlemusic.py writes them; a jingle and the credits without a loop, the credits' tempo moving
# ---------------------------------------------------------------------------------------------------------------------
def credits_sections():
    secs = []
    for pid, a, b in CREDITS_PLAN:
        p = _find(pid)
        secs.append((p["bpm"], _section(p, a, b), b - a))
    secs.append((128, CODA, 8))
    return secs


def notes_of(p):
    """[(beat, beats, key, note)], total beats, loop or None, [(beat, bpm)]"""
    if p.get("credits"):
        out, t0, tempos = [], 0.0, []
        for bpm, tracks, beats in credits_sections():
            tempos.append((t0, bpm))
            for role, tok in tracks:
                for b, d, n in GB.parse(tok)[0]:
                    if isinstance(n, str):
                        out.append((t0 + b, d, n, GB.NOISE_KEY[n]))
                    elif role in ("lead", "sing"):
                        out += [(t0 + b, d, role, m) for m in n]
                    else:
                        out.append((t0 + b, d, role, max(n)))
            t0 += beats
        return out, t0, None, tempos
    if p.get("jingle"):
        notes, total, _, tempos = GB.notes_of(dict(p, loop=[("perc", "r:0")]))
        return notes, total, None, tempos
    q = dict(p, intro=p["intro"] or [("perc", "r:0")])
    return GB.notes_of(q)


def song_midi(p):
    notes, total, loop, tempos = notes_of(p)
    tick = lambda beats: int(round(beats * TPB))
    tempo = lambda bpm: b"\xff\x51\x03" + struct.pack(">I", int(round(60e6 / bpm)))[1:]
    ev = [(tick(b), 6 if b else 0, tempo(bpm)) for b, bpm in tempos]
    for key in sorted({k for _, _, k, _ in notes}, key=lambda k: GB.CH[k][0]):
        ch, prog, vol, _ = GB.CH[key]
        ev += [(0, 1, bytes([0xC0 | ch, prog])), (0, 2, bytes([0xB0 | ch, 7, vol])), (0, 3, bytes([0xB0 | ch, 10, 64]))]
    end = tick(total)
    for b, d, key, m in notes:
        ch, _, _, vel = GB.CH[key]
        on = tick(b)
        off = max(on + 1, tick(b + GB.gate(key, d)))
        if loop:
            off = min(off, end)                    # a loop's notes stop at its end: a clean loop point
        ev.append((on, 20, bytes([0x90 | ch, m, vel])))
        ev.append((off, 10, bytes([0x80 | ch, m, 0])))
    if loop:
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
    assert len({GB.CH[k][0] for k in keys}) <= GB.BGM_TRACKS, "%s: too many tracks" % p["id"]
    low = [(k, m) for _, _, k, m in notes if k in ("arp", "harm", "bass") and m < 36]
    assert not low, "%s: %s -- PSG keys under C2 play as C2 (engine.md trap 44)" % (p["id"], low)
    for k in keys - {"lead", "sing"}:              # a PSG track is one note at a time
        span = sorted((b, b + GB.gate(k, d)) for b, d, kk, _ in notes if kk == k)
        assert all(a[1] <= c[0] + 1e-6 for a, c in zip(span, span[1:])), "%s: %s overlaps itself" % (p["id"], k)
    marks = sorted([(b, 1) for b, d, k, _ in notes if k in ("lead", "sing")] +
                   [(b + GB.gate(k, d), -1) for b, d, k, _ in notes if k in ("lead", "sing")])
    level = peak = 0
    for _, s in marks:
        level += s; peak = max(peak, level)
    assert peak <= 4, "%s: %d DirectSound notes at once, and the mixer has five" % (p["id"], peak)


def engine():
    """{path: new contents} for every file this writes."""
    out, cfg = {}, open(CFG, encoding="utf-8").read()
    table = open(TABLE, encoding="utf-8").read()
    h = open(SONGS_H, encoding="utf-8").read()
    ld = open(LD, encoding="utf-8").read()
    prev = r"(?:mus_lurid|mus_walled_garden)"
    for p in PIECES:
        check(p)
        f = FILES[p["id"]]
        out[os.path.join(MIDI_DIR, f + ".mid")] = song_midi(p)
        if p["id"] in NEW:
            const, what = NEW[p["id"]]
            if not re.search(r"^%s\.mid:" % f, cfg, re.M):
                last = list(re.finditer(r"^%s\.mid:.*\n" % prev, cfg, re.M))[-1]
                cfg = cfg[:last.end()] + "%-31s-E -R50 -G%03d -V090\n" % (f + ".mid:", VOICEGROUP) + cfg[last.end():]
            if ("song %s," % f) not in table:
                last = list(re.finditer(r"^\tsong %s, \d+, \d+\n" % prev, table, re.M))[-1]
                table = table[:last.end()] + "\tsong %s, 0, 0\n" % f + table[last.end():]
            if not re.search(r"^#define %s\s" % const, h, re.M):
                ids = [int(x) for x in re.findall(r"^#define (?:SE|MUS)_\w+\s+(\d+)\b(?!x)", h, re.M)]
                last = list(re.finditer(r"^#define (?:MUS_LURID|MUS_WALLED_GARDEN)\s.*\n", h, re.M))[-1]
                line = "#define %-25s %d   // T-565 batch 8: %s (DAEMONS tools/genstorymusic.py)\n" % (const, max(ids) + 1, what)
                h = h[:last.end()] + line + h[last.end():]
            obj = "        sound/songs/midi/%s.o(.rodata);\n" % f
            if obj not in ld:
                last = list(re.finditer(r"^        sound/songs/midi/%s\.o\(\.rodata\);\n" % prev, ld, re.M))[-1]
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
    secs = sum(beats * 60 / bpm for bpm, _, beats in credits_sections())
    print("  %d story pieces on voicegroup%03d; the credits %.0f s" % (len(PIECES), VOICEGROUP, secs))
    if not changed:
        print("  the game: unchanged")
    else:
        print("  the game: %s %d file(s): %s" % ("wrote" if "--write" in sys.argv else "would write", len(changed),
                                                 ", ".join(changed[:6]) + (" ..." if len(changed) > 6 else "")))


if __name__ == "__main__":
    main()
