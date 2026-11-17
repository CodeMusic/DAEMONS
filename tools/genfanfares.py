#!/usr/bin/env python3
"""T-565: the fanfares, the jingles, the toy piano and the pitched sounds -- ours, in place of pret's.

    python3 tools/genfanfares.py                     # report: is the engine current
    python3 tools/genfanfares.py --write             # write it into engineGba
    python3 tools/genfanfares.py --preview DIR       # one WAV per piece, as the mixer would play it (13379 Hz, 8-bit)

THE VOICE (the user, 2026-11-16, by multiple choice from three, "C Both"): **our harp and flute carry every tune and
the cartridge holds them up.** The HARP and the FLUTE are PLAY's own (voicegroup193, tools/geninstruments.py); under
them the Game Boy's four channels -- two squares for the chords, the wave for the bass, the noise for the beat -- as
BOUND and the eleven tracks carried from the classic build are. One voicegroup, VOICEGROUP below:
    0 HARP    voicegroup193's harp: a pluck that rings out by itself (lead: short melody notes, and the toy piano)
    1 FLUTE   voicegroup193's flute: held (sing: the held melody)
    2 SQ1     square 1, 12.5%, swelling (pad: the chord's upper note)
    3 SQ2     square 2, 12.5%, swelling (pad: the next note down; a chord of three keeps its top two)
    4 SQ2     square 2, 12.5%, plucked (harm: a second line -- never in a piece that has a pad, so never at once)
    5 WAVE    the wave, voicegroup192's ProgrammableWaveData_6 (bass)
    6 NOISE   a closed tick        7 NOISE  a burst        8 NOISE  a long shimmer
    9 SQ1     square 1, 12.5%, plucked (the battle music's broken chords: tools/genbattlemusic.py, T-565 batch 2)

THE NOTES are written once below, a token at a time (NOTE:BEATS, NOTE+NOTE:BEATS, r:BEATS; h s c for the noise), and
the drafts heard three voices of them (docs/TODO.md T-565). Every MIDI here REPLACES pret's in place, so no constant
moves (the split agreed with the game lane, 2026-11-16); midi.cfg keeps each slot's flags and only its -G changes.

WHAT IT WRITES (engineGba/)
    sound/songs/midi/<slot>.mid       16 songs, 5 sounds, the toy piano's 8 and 3 new sounds (format 0, 24 ticks a beat,
                                      a loop marked [ and ])
    sound/songs/midi/midi.cfg         each slot's -G to 195; the three new sounds' lines
    sound/voice_groups.inc            voicegroup195, just before voicegroup193 (geninstruments.py rewrites from there on)
    src/sound.c                       sFanfares: each of ours waits its own length and its harp's ring, not pret's
    sound/song_table.inc, include/constants/songs.h, ld_script.ld    the three new sounds (a song is four lines,
                                      engine.md trap 25): SE_CHIME, SE_SUNRISE, SE_NIGHTFALL, on SE1 as pret's were
The field's call sites of the three new sounds are code, not generated (daemons_unity.c, daemons_spirits.c,
field_effect.c); battle keeps SE_M_HEAL_BELL, SE_M_MORNING_SUN and SE_M_MOONLIGHT.
"""
import math, os, re, struct, sys, wave

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
MIDI_DIR = os.path.join(GBA, "sound", "songs", "midi")
CFG = os.path.join(MIDI_DIR, "midi.cfg")
VG = os.path.join(GBA, "sound", "voice_groups.inc")
SOUND_C = os.path.join(GBA, "src", "sound.c")
TABLE = os.path.join(GBA, "sound", "song_table.inc")
SONGS_H = os.path.join(GBA, "include", "constants", "songs.h")
LD = os.path.join(GBA, "ld_script.ld")
INSTR = os.path.join(ROOT, "audio", "instruments")

VOICEGROUP = 195
MARK_VG = "voicegroup%03d::  @ T-565: the fanfares and the pitched sounds -- the HARP and FLUTE over the cartridge (DAEMONS tools/genfanfares.py)" % VOICEGROUP
VOICES = [
    "\tvoice_directsound 60, 0, DirectSoundWaveData_daemons_harp, 255, 0, 255, 177",
    "\tvoice_directsound 60, 0, DirectSoundWaveData_daemons_flute, 54, 0, 255, 138",
    "\tvoice_square_1_alt 60, 0, 0, 0, 1, 3, 11, 2",
    "\tvoice_square_2_alt 60, 0, 0, 1, 3, 11, 2",
    "\tvoice_square_2_alt 60, 0, 0, 0, 2, 6, 1",
    "\tvoice_programmable_wave_alt 60, 0, ProgrammableWaveData_6, 0, 7, 15, 2",
    "\tvoice_noise_alt 60, 0, 0, 0, 1, 0, 0",
    "\tvoice_noise_alt 60, 0, 0, 0, 2, 0, 1",
    "\tvoice_noise_alt 60, 0, 0, 2, 7, 3, 4",
    "\tvoice_square_1_alt 60, 0, 0, 0, 0, 2, 6, 1",     # 9: genbattlemusic.py's arp (T-565 batch 2)
]
# role -> (MIDI channel, program, track volume, velocity); the noise's three are by letter
CHANNELS = {"lead": (0, 0, 100, 100), "sing": (1, 1, 100, 96), "pad_hi": (2, 2, 52, 100), "pad_lo": (3, 3, 52, 100),
            "harm": (4, 4, 56, 100), "bass": (5, 5, 100, 100),
            "h": (6, 6, 70, 100), "s": (7, 7, 80, 100), "c": (8, 8, 50, 100)}
NOISE_KEY = {"h": 84, "s": 62, "c": 90}
PLAYER_TRACKS = {0: 10, 1: 3, 2: 9, 3: 1}       # sound/music_player_table.inc
FRAME = 1 / 59.7275
RING = 0.12                                      # seconds for the release to fade before BGM returns
# pret's waits (src/sound.c as pret has it): ours never wait longer, so no pickup is slower than vanilla's -- a harp
# still ringing at the end is cut as its release would have faded it (LEVEL_UP: by about a tenth of a second)
PRET_WAIT = {"FANFARE_LEVEL_UP": 80, "FANFARE_EVOLVED": 220, "FANFARE_OBTAIN_TMHM": 220, "FANFARE_HEAL": 160,
             "FANFARE_OBTAIN_BADGE": 340, "FANFARE_MOVE_DELETED": 180, "FANFARE_POKE_FLUTE": 450,
             "FANFARE_KEY_ITEM": 170, "FANFARE_DEX_EVAL": 196}
TPB = 24

# ---------------------------------------------------------------------------------------------------------------------
# THE PIECES. "fanfare": its sFanfares row, which this writes. "loop": the tracks after it repeat.
# ---------------------------------------------------------------------------------------------------------------------
PIECES = [
  dict(id="LEVEL_UP", file="mus_level_up", fanfare="FANFARE_LEVEL_UP", bpm=180,
       what="every level-up and every item found",
       why="Blanche's pentatonic, rising and stopping on D over C: open, a step taken, nothing to resolve",
       tracks=[("lead", "C6:0.5 E6:0.5 G6:0.5 D6:1.5"), ("pad", "C5+G5:3"), ("bass", "C3:3")]),
  dict(id="HEAL", file="mus_heal", fanfare="FANFARE_HEAL", bpm=120,
       what="every centre's heal", why="a rocking lullaby that comes home: the one fanfare that resolves",
       tracks=[("sing", "E5:0.5 D5:0.5 C5:1 G4:0.5 A4:0.5 C5:2"), ("harm", "C4:1 G4:1 A3:1 E4:1 C4:1"),
               ("bass", "C3:2 A2:1 C3:2")]),
  dict(id="KEY_ITEM", file="mus_obtain_key_item", fanfare="FANFARE_KEY_ITEM", bpm=132,
       what="every key item", why="the title's hook (+2 +1 +2 +2 0, vision 7.10) from A, ending on E: forward, not finished",
       tracks=[("sing", "A4:0.5 B4:0.5 C5:0.5 D5:0.5 E5:0.75 E5:2.25"), ("pad", "A3+E4:2 F3+C4:1.5 E3+B3:1.5"),
               ("bass", "A2:2 F2:1.5 E2:1.5")]),
  dict(id="TMHM", file="mus_obtain_tmhm", fanfare="FANFARE_OBTAIN_TMHM", bpm=150,
       what="a ROUTINE given by someone", why="it loads in stepped repeated pairs and lands on G",
       tracks=[("lead", "C5:0.25 C5:0.25 D5:0.25 D5:0.25 E5:0.25 E5:0.25 G5:0.25 G5:0.25 A5:0.5 G5:0.5 E5:0.5 G5:2.5"),
               ("pad", "r:2 C4+E4:1.5 C4+G4:2.5"), ("bass", "C3:2 A2:1.5 C3:2.5"), ("perc", "h:0.5 h:0.5 h:0.5 h:0.5 r:4")]),
  dict(id="EVOLVED", file="mus_evolved", fanfare="FANFARE_EVOLVED", bpm=120,
       what="the end of every evolution", why="the same three notes twice, the ground changing under the second: still me",
       tracks=[("sing", "E5:0.5 G5:0.5 E5:1 E5:0.5 G5:0.5 E5:2"), ("pad", "C4+G4:2 F3+A3+C4:3"), ("bass", "C3:2 F2:3")]),
  dict(id="EVOLUTION_INTRO", file="mus_evolution_intro", bpm=120,
       what="the start of every evolution", why="a rising pluck into the loop",
       tracks=[("lead", "C4:0.25 E4:0.25 G4:0.25 C5:0.25 E5:1"), ("bass", "r:1 C3:1")]),
  dict(id="EVOLUTION", file="mus_evolution", bpm=120,
       what="while a daemon evolves (and the Safari Zone's maps, until they have their own)",
       why="one held E through four chords: the harmony changes, the note does not",
       tracks=[],
       loop=[("sing", "E5:4 E5:4 E5:4 E5:4"),
             ("harm", "C4:0.5 G4:0.5 E4:0.5 G4:0.5 C4:0.5 G4:0.5 E4:0.5 G4:0.5 "
                      "A3:0.5 E4:0.5 C4:0.5 E4:0.5 A3:0.5 E4:0.5 C4:0.5 E4:0.5 "
                      "F3:0.5 C4:0.5 A3:0.5 C4:0.5 F3:0.5 C4:0.5 A3:0.5 C4:0.5 "
                      "G3:0.5 D4:0.5 B3:0.5 D4:0.5 G3:0.5 D4:0.5 B3:0.5 D4:0.5"),
             ("bass", "C3:4 A2:4 F2:4 G2:4"), ("perc", "r:3 h:1 r:3 h:1 r:3 h:1 r:3 h:1")]),
  dict(id="BADGE", file="mus_obtain_badge", fanfare="FANFARE_OBTAIN_BADGE", bpm=120,
       what="each MARK", why="C D E G A, low then high: the visible spectrum (vision 7.14) climbed to its edge, held on A",
       tracks=[("lead", "C4:0.5 D4:0.5 E4:0.5 G4:0.5 A4:0.5 r:5.5"), ("sing", "r:2.5 C5:0.5 D5:0.5 E5:0.5 G5:0.5 A5:3.5"),
               ("pad", "r:2.5 C4+G4:2 F4+A4+C5:3.5"), ("bass", "C3:2.5 C3:2 F2:3.5"), ("perc", "r:4.5 c:3.5")]),
  dict(id="MOVE_DELETED", file="mus_move_deleted", fanfare="FANFARE_MOVE_DELETED", bpm=132,
       what="a ROUTINE forgotten", why="a figure, then the same figure missing its last note",
       tracks=[("lead", "G4:0.5 C5:0.5 E5:0.5 G5:1 r:0.5 G4:0.5 C5:0.5 E5:0.5 r:1.5"), ("pad", "C4+E4:2.5 r:3.5"),
               ("bass", "C3:2.5 C3:1.5 r:2")]),
  dict(id="DEX_RATING", file="mus_dex_rating", fanfare="FANFARE_DEX_EVAL", bpm=128,
       what="CRYSTAL CLEAR rating the INDEX", why="her own hook (vision 7.6), only where she speaks (7.13), left on D",
       tracks=[("sing", "A4:0.5 E5:0.5 D5:0.5 C5:0.5 B4:0.5 C5:0.5 D5:2"), ("pad", "A3+E4:2 F3+C4:1 G3+D4:2"),
               ("bass", "A2:2 F2:1 G2:2")]),
  dict(id="INTERRUPT", file="mus_poke_flute", fanfare="FANFARE_POKE_FLUTE", bpm=100,
       what="the INTERRUPT, waking what sleeps", why="one call three times, answered by nothing, then acknowledged",
       tracks=[("sing", "G5:0.5 C6:1 r:0.5 G5:0.5 C6:1 r:0.5 G5:0.5 C6:1 r:0.5 r:3"),
               ("lead", "r:6 C5:0.25 E5:0.25 G5:0.25 C6:0.25 E6:2"), ("pad", "r:6.75 C4+G4:2.25"), ("bass", "r:6.75 C3:2.25")]),
  dict(id="CAUGHT", file="mus_caught", bpm=100,
       what="after BOUND, while the binding is named", why="BOUND's key, still settling: each phrase falls, the last one home",
       tracks=[],
       loop=[("sing", "B4:1 G#4:1 E4:2 C#5:1 B4:1 G#4:2 A4:1 G#4:1 F#4:2 E4:4"),
             ("harm", "E4:0.5 G#4:0.5 B4:0.5 G#4:0.5 E4:0.5 G#4:0.5 B4:0.5 G#4:0.5 "
                      "C#4:0.5 E4:0.5 G#4:0.5 E4:0.5 C#4:0.5 E4:0.5 G#4:0.5 E4:0.5 "
                      "A3:0.5 C#4:0.5 E4:0.5 C#4:0.5 B3:0.5 D#4:0.5 F#4:0.5 D#4:0.5 "
                      "E4:0.5 G#4:0.5 B4:0.5 G#4:0.5 E4:2"),
             ("bass", "E3:4 C#3:4 A2:2 B2:2 E3:4")]),     # an octave up from the draft: the PSG holds nothing under C2
  dict(id="ENCOUNTER_BOY", file="mus_encounter_boy", bpm=150,
       what="eyes meet: the male, intense and cool classes", why="a driving A-minor pentatonic riff over a pulsing A",
       tracks=[("lead", "A3+E4:1 r:1"), ("bass", "A2:1 r:1"), ("perc", "s:1 r:1")],
       loop=[("lead", "A4:0.5 A4:0.5 C5:0.5 A4:0.5 D5:0.5 A4:0.5 E5:0.5 D5:0.5 "
                      "A4:0.5 A4:0.5 C5:0.5 A4:0.5 G5:0.5 E5:0.5 D5:0.5 C5:0.5 "
                      "A4:0.5 A4:0.5 C5:0.5 A4:0.5 D5:0.5 A4:0.5 E5:0.5 D5:0.5 "
                      "G4:0.5 G4:0.5 C5:0.5 G4:0.5 D5:0.5 C5:0.5 A4:0.5 G4:0.5"),
             ("bass", " ".join(["A2:0.5"] * 16 + ["F2:0.5"] * 8 + ["G2:0.5"] * 8)),
             ("perc", " ".join(["h:0.5", "h:0.5", "s:0.5", "h:0.5"] * 8))]),
  dict(id="ENCOUNTER_GIRL", file="mus_encounter_girl", bpm=132,
       what="eyes meet: the female, girl and twins classes", why="bright and lilting in threes, C pentatonic turning over",
       tracks=[("lead", "G4:0.5 A4:0.5"), ("bass", "r:1")],
       loop=[("lead", " ".join(n + ":1/3" for n in "E5 D5 C5 D5 E5 G5 A5 G5 E5".split()) + " D5:1 "
                      + " ".join(n + ":1/3" for n in "C5 D5 E5 G5 E5 D5".split()) + " C5:1 A4:1 "
                      + " ".join(n + ":1/3" for n in "E5 D5 C5 D5 E5 G5 A5 G5 E5".split()) + " D5:1 "
                      + " ".join(n + ":1/3" for n in "C5 D5 E5 D5 C5 A4".split()) + " C5:2"),
             ("bass", "C3:1 G2:1 C3:1 G2:1 A2:1 E2:1 A2:1 E2:1 C3:1 G2:1 C3:1 G2:1 F2:1 G2:1 C3:2"),
             ("perc", " ".join(["h:1"] * 16))]),
  dict(id="ENCOUNTER_ROCKET", file="mus_encounter_rocket", bpm=144,
       what="eyes meet: the suspicious, Corpus, and every class without its own",
       why="cheerful in C, then the same figure a semitone down in B, and back: cheerful about the wrong thing",
       tracks=[("lead", "G4:0.5 B4:0.5"), ("bass", "r:1")],
       loop=[("lead", "C5:0.5 r:0.5 E5:0.5 G5:0.5 A5:0.5 G5:0.5 E5:0.5 C5:0.5 "
                      "D5:0.5 r:0.5 E5:0.5 D5:0.5 C5:1 r:1 "
                      "B4:0.5 r:0.5 D#5:0.5 F#5:0.5 G#5:0.5 F#5:0.5 D#5:0.5 B4:0.5 "
                      "C#5:0.5 r:0.5 D#5:0.5 C#5:0.5 B4:1 r:1"),
             ("bass", "C3:0.5 G2:0.5 C3:0.5 G2:0.5 C3:0.5 G2:0.5 C3:0.5 G2:0.5 "
                      "G2:0.5 D3:0.5 G2:0.5 D3:0.5 C3:0.5 G2:0.5 C3:1 "
                      "B2:0.5 F#2:0.5 B2:0.5 F#2:0.5 B2:0.5 F#2:0.5 B2:0.5 F#2:0.5 "
                      "F#2:0.5 C#3:0.5 F#2:0.5 C#3:0.5 B2:0.5 F#2:0.5 B2:1"),
             ("perc", " ".join(["h:0.5", "s:0.5"] * 16))]),
  dict(id="BOOT", file="mus_game_freak", bpm=120,
       what="every boot, the logo's star", why="the classic build's falling note (vision 7.14c): a run down that lands as the star does",
       tracks=[("lead", "A6:1/6 G6:1/6 E6:1/6 D6:1/6 C6:1/6 A5:1/6 C5:5"), ("sing", "r:2 G5:1 C6:3"),
               ("pad", "r:1 C4+G4+D5:5"), ("bass", "r:1 C3:5"), ("perc", "r:1 c:5")]),
  dict(id="SUCCESS", file="se_success", bpm=240, what="a thing worked", why="up a fourth",
       tracks=[("lead", "G5:0.25 C6:1")]),
  dict(id="FAILURE", file="se_failure", bpm=240, what="a thing did not", why="down a semitone, low and short",
       tracks=[("lead", "E4:0.25 D#4:0.75")]),
  dict(id="DING_DONG", file="se_ding_dong", bpm=150, what="the PA and a doorbell", why="a falling major third",
       tracks=[("lead", "E5:1 C5:2")]),
  dict(id="PC_LOGIN", file="se_pc_login", bpm=144, what="signing in to a PORT", why="a connection rising",
       tracks=[("lead", "C5:0.25 G5:0.25 C6:0.25 E6:0.75")]),
  dict(id="SHOP", file="se_shop", bpm=124, what="a purchase", why="a tick and two bright notes",
       tracks=[("lead", "A5:0.25 E6:1"), ("perc", "h:0.25 r:1")]),
  dict(id="CHIME", file="se_chime", new=("SE_CHIME", "the field's bell: GOTO's ribbon, the unity and spirits scenes"),
       bpm=150, what="in the field where SE_M_HEAL_BELL was", why="a pentatonic sparkle falling to C, E ringing above",
       tracks=[("lead", "E6:0.125 D6:0.125 C6:0.125 A5:0.125 G5:0.125 C5:1.5"), ("sing", "r:0.625 E6:1.5")]),
  dict(id="SUNRISE", file="se_sunrise", new=("SE_SUNRISE", "the unity scene at dawn"),
       bpm=100, what="where SE_M_MORNING_SUN was, in the field", why="a slow shimmer rising over a held G",
       tracks=[("lead", "C5:0.25 G5:0.25 D6:0.25 E6:1.25"), ("sing", "G5:2")]),
  dict(id="NIGHTFALL", file="se_nightfall", new=("SE_NIGHTFALL", "the unity scene at night"),
       bpm=100, what="where SE_M_MOONLIGHT was, in the field", why="SUNRISE mirrored: the shimmer falling",
       tracks=[("lead", "E6:0.25 D6:0.25 G5:0.25 C5:1.25"), ("sing", "G5:2")]),
]
# THE TOY PIANO: SE_NOTE_C .. SE_NOTE_C_HIGH keep every call site (the day's note, the singing fir, the holidays); only
# the voice changes -- the HARP, one note, C5 to C6 (pret's sounded C6 to C7 with a fifth above).
TOY = [("se_note_c", 72), ("se_note_d", 74), ("se_note_e", 76), ("se_note_f", 77), ("se_note_g", 79),
       ("se_note_a", 81), ("se_note_b", 83), ("se_note_c_high", 84)]
TOY_RING = 1.5

NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def midi_note(n):
    letter, rest, acc = n[0], n[1:], 0
    while rest and rest[0] in "#b":
        acc += 1 if rest[0] == "#" else -1
        rest = rest[1:]
    return 12 * (int(rest) + 1) + NAMES.index(letter) + acc


def parse(tokens):
    """-> ([(start_beat, beats, notes or perc letter)], total beats)"""
    t, out = 0.0, []
    for tok in tokens.split():
        what, beats = tok.rsplit(":", 1)
        a, _, b = beats.partition("/")
        beats = float(a) / float(b or 1)
        if what in ("h", "s", "c"):
            out.append((t, beats, what))
        elif what != "r":
            out.append((t, beats, [midi_note(n) for n in what.split("+")]))
        t += beats
    return out, t


def section_beats(tracks):
    lens = {round(parse(tok)[1], 4) for _, tok in tracks}
    assert len(lens) <= 1, "tracks of unequal length: %s" % lens
    return lens.pop() if lens else 0.0


def notes_of(piece):
    """[(start_beat, beats, channel key, midi note)] for intro then one loop, plus (loop start, loop end) in beats."""
    out, t0, loop = [], 0.0, None
    for i, sec in enumerate([piece["tracks"], piece.get("loop", [])]):
        if i == 1 and sec:
            loop = [t0, None]
        for role, tok in sec:
            for b, d, n in parse(tok)[0]:
                if isinstance(n, str):
                    out.append((t0 + b, d, n, NOISE_KEY[n]))
                elif role == "pad":
                    top = sorted(n)[-2:]
                    out.append((t0 + b, d, "pad_hi", top[-1]))
                    if len(top) > 1:
                        out.append((t0 + b, d, "pad_lo", top[0]))
                elif role in ("lead", "sing"):
                    out += [(t0 + b, d, role, m) for m in n]
                else:
                    out.append((t0 + b, d, role, max(n) if role == "harm" else min(n)))
        t0 += section_beats(sec)
        if loop and loop[1] is None and i == 1:
            loop[1] = t0
    assert not ({k for _, _, k, _ in out} >= {"harm", "pad_lo"}), "%s: harm and the lower pad share square 2" % piece["id"]
    return out, t0, loop


def gate(key, beats, spb):
    """How long a note sounds, in beats: the harp rings into the next note and not past it; the rest are articulated."""
    if key == "lead":
        sec = beats * spb
        return max(beats, min(0.9, 2 * sec) / spb)
    return {"sing": 1.0, "pad_hi": 0.97, "pad_lo": 0.97, "harm": 0.9, "bass": 0.92}.get(key, 0) * beats or 2 / TPB


def vlq(n):
    b = [n & 0x7F]
    n >>= 7
    while n:
        b.insert(0, 0x80 | (n & 0x7F))
        n >>= 7
    return bytes(b)


def song_midi(piece):
    notes, total, loop = notes_of(piece)
    spb = 60.0 / piece["bpm"]
    tick = lambda beats: int(round(beats * TPB))
    ev = [(0, 0, b"\xff\x51\x03" + struct.pack(">I", int(round(60e6 / piece["bpm"])))[1:])]
    for key in sorted({k for _, _, k, _ in notes}, key=lambda k: CHANNELS[k][0]):
        ch, prog, vol, _ = CHANNELS[key]
        ev += [(0, 1, bytes([0xC0 | ch, prog])), (0, 2, bytes([0xB0 | ch, 7, vol])), (0, 3, bytes([0xB0 | ch, 10, 64]))]
    end = tick(total)
    for b, d, key, m in notes:
        ch, _, _, vel = CHANNELS[key]
        on, off = tick(b), max(tick(b) + 1, tick(b + gate(key, d, spb)))
        if loop:                                       # a loop's notes stop at its end, so the loop point is clean
            off = min(off, end)
        ev.append((on, 20, bytes([0x90 | ch, m, vel])))
        ev.append((off, 10, bytes([0x80 | ch, m, 0])))
        end = max(end, off)
    if loop:
        ev.append((tick(loop[0]), 5, b"\xff\x06\x01["))
        ev.append((tick(loop[1]), 30, b"\xff\x06\x01]"))
    ev.sort()
    body, now = b"", 0
    for t, _, e in ev:
        body += vlq(t - now) + e
        now = t
    body += b"\x00\xff\x2f\x00"
    return b"MThd" + struct.pack(">IHHH", 6, 0, 1, TPB) + b"MTrk" + struct.pack(">I", len(body)) + body


def toy_midi(note):
    piece = dict(id="TOY", bpm=120, tracks=[("lead", "%s:%g" % (NAMES[note % 12] + str(note // 12 - 1), TOY_RING * 2))])
    return song_midi(piece)


def seconds(piece):
    _, total, _ = notes_of(piece)
    return total * 60.0 / piece["bpm"]


def fanfare_frames(piece):
    """The wait: until the last note (a harp's ring included) has sounded and faded, then BGM comes back."""
    notes, total, _ = notes_of(piece)
    spb = 60.0 / piece["bpm"]
    last = max([total] + [b + gate(k, d, spb) for b, d, k, _ in notes]) * spb
    return min(PRET_WAIT[piece["fanfare"]], int(math.ceil((last + RING) / FRAME)))


def check_limits(piece, player):
    notes, _, _ = notes_of(piece)
    chans = {k for _, _, k, _ in notes}
    keys = {CHANNELS[k][0] for k in chans}
    assert len(keys) <= PLAYER_TRACKS[player], "%s: %d tracks on player %d (%d)" % (piece["id"], len(keys), player, PLAYER_TRACKS[player])
    low = [(k, m) for _, _, k, m in notes if k not in ("lead", "sing") and k not in NOISE_KEY and m < 36]
    assert not low, "%s: %s -- m4a plays every PSG key under 36 (C2) as C2 (MidiKeyToCgbFreq)" % (piece["id"], low)
    for k in chans - {"lead", "sing"}:                 # a PSG track is one note at a time
        span = sorted((b, b + d) for b, d, kk, _ in notes if kk == k)
        assert all(a[1] <= b[0] + 1e-6 for a, b in zip(span, span[1:])), "%s: %s overlaps itself" % (piece["id"], k)


def player_of(table, name):
    m = re.search(r"^\tsong %s, (\d+), \d+$" % re.escape(name), table, re.M)
    return int(m.group(1)) if m else None


def engine():
    """{path: new contents} for every file this writes."""
    out = {}
    table = open(TABLE, encoding="utf-8").read()
    cfg = open(CFG, encoding="utf-8").read()
    news = [p for p in PIECES if p.get("new")]
    for p in PIECES:
        player = player_of(table, p["file"])
        check_limits(p, player if player is not None else 1)
        out[os.path.join(MIDI_DIR, p["file"] + ".mid")] = song_midi(p)
    for name, note in TOY:
        out[os.path.join(MIDI_DIR, name + ".mid")] = toy_midi(note)
    # midi.cfg: -G195 for each of ours; the new sounds' lines after the dawn chorus's
    for name in [p["file"] for p in PIECES if not p.get("new")] + [n for n, _ in TOY]:
        cfg, k = re.subn(r"^(%s\.mid:\s+.*?)-G\d+" % re.escape(name), r"\g<1>-G%03d" % VOICEGROUP, cfg, flags=re.M)
        assert k == 1, "midi.cfg has no line for %s" % name
    anchor = re.search(r"^se_dawn_chorus\.mid:.*\n", cfg, re.M)
    add = "".join("%-31s-E -R50 -G%03d -V100 -P4\n" % (p["file"] + ".mid:", VOICEGROUP) for p in news
                  if not re.search(r"^%s\.mid:" % p["file"], cfg, re.M))
    cfg = cfg[:anchor.end()] + add + cfg[anchor.end():]
    out[CFG] = cfg
    # voice_groups.inc
    t = open(VG, encoding="utf-8").read()
    block = "\t.align 2\n%s\n%s\n\n" % (MARK_VG, "\n".join(VOICES))
    if MARK_VG in t:
        k = t.index("\t.align 2\n" + MARK_VG)
        e = t.index("\n\n", k) + 2
        t = t[:k] + block + t[e:]
    else:
        k = t.find("\t.align 2\nvoicegroup193::")
        assert k >= 0, "voice_groups.inc has no voicegroup193 to sit before"
        t = t[:k] + block + t[k:]
    out[VG] = t
    # sound.c: sFanfares
    s = open(SOUND_C, encoding="utf-8").read()
    for p in PIECES:
        if p.get("fanfare"):
            s, k = re.subn(r"(\[%s\]\s*=\s*\{\s*MUS_\w+,\s*)\d+(\s*\})" % p["fanfare"], r"\g<1>%d\g<2>" % fanfare_frames(p), s)
            assert k == 1, "sound.c has no row for %s" % p["fanfare"]
    note = "// T-565: the rows of ours wait their own length and the harp's ring (DAEMONS tools/genfanfares.py)\n"
    if note not in s:
        s = s.replace("static const struct Fanfare sFanfares[] = {", note + "static const struct Fanfare sFanfares[] = {", 1)
    out[SOUND_C] = s
    # the three new sounds: song_table.inc, songs.h, ld_script.ld
    t = table                                          # after the dawn chorus, or after whichever of ours is last there
    for p in news:
        if player_of(t, p["file"]) is None:
            prev = list(re.finditer(r"^\tsong se_(?:dawn_chorus|chime|sunrise|nightfall), \d+, \d+\n", t, re.M))[-1]
            t = t[:prev.end()] + "\tsong %s, 1, 1\n" % p["file"] + t[prev.end():]
    out[TABLE] = t
    h = open(SONGS_H, encoding="utf-8").read()
    for p in news:
        const, what = p["new"]
        if not re.search(r"^#define %s\s" % const, h, re.M):
            ids = [int(x) for x in re.findall(r"^#define (?:SE|MUS)_\w+\s+(\d+)\b(?!x)", h, re.M)]
            line = "#define %-25s %d   // T-565: %s (DAEMONS tools/genfanfares.py)\n" % (const, max(ids) + 1, what)
            last = list(re.finditer(r"^#define SE_(?:DAWN_CHORUS|CHIME|SUNRISE|NIGHTFALL)\s.*\n", h, re.M))[-1]
            h = h[:last.end()] + line + h[last.end():]
    out[SONGS_H] = h
    ld = open(LD, encoding="utf-8").read()
    for p in news:
        obj = "        sound/songs/midi/%s.o(.rodata);\n" % p["file"]
        if obj not in ld:
            prev = list(re.finditer(r"^        sound/songs/midi/se_(?:dawn_chorus|chime|sunrise|nightfall)\.o\(\.rodata\);\n", ld, re.M))[-1]
            ld = ld[:prev.end()] + obj + ld[prev.end():]
    out[LD] = ld
    return out


# ---------------------------------------------------------------------------------------------------------------------
# --preview: the mixer at 13379 Hz, our two samples resampled as m4a does, the PSG synthesised; a preview, not the GBA
# ---------------------------------------------------------------------------------------------------------------------
def preview(outdir):
    import json
    import numpy as np
    SR = 13379
    meta = json.load(open(os.path.join(INSTR, "instruments.json")))

    def sample(name):
        w = wave.open(os.path.join(INSTR, meta[name]["file"]))
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float) / 32768
        return meta[name], np.round(x * 127) / 127

    harp, flute = sample("harp"), sample("flute")

    def ds(inst, m, sec):
        md, x = inst
        step = 2 ** ((m - 60) / 12) * md["sample_rate"] / SR
        rel = md["release_ms"] / 1000
        pos = np.arange(int((sec + rel) * SR)) * step
        if md["loop_start"] is not None:
            ls, le = md["loop_start"], md["loop_end"]
            over = pos >= le
            pos[over] = ls + np.mod(pos[over] - ls, le - ls)
        pos = pos[pos < len(x) - 1]
        i = pos.astype(int)
        y = x[i] * (1 - (pos - i)) + x[i + 1] * (pos - i)
        t = np.arange(len(y)) / SR
        env = np.clip(t / (md["attack_ms"] / 1000), 0, 1) if md["attack_ms"] else np.ones(len(y))
        env[t > sec] *= np.exp(-(t[t > sec] - sec) / (rel / 4))
        return y * env

    def psg(m, sec, duty, a, d, s, r, kind="sq"):
        hz = 440 * 2 ** ((m - 69) / 12)
        n = int((sec + r + 0.02) * SR)
        t = np.arange(n) / SR
        if kind == "sq":
            y = np.where(np.mod(hz * t, 1) < duty, 1.0, -1.0)
        elif kind == "wave":
            y = 1 - 2 * np.abs(2 * np.mod(hz * t, 1) - 1)
        else:
            y = np.random.default_rng(int(m)).choice([-1.0, 1.0], n)
        e = np.where(t < a, t / max(a, 1e-4), np.maximum(s, 1 - (1 - s) * (t - a) / max(d, 1e-4)))
        e[t > sec] *= np.clip(1 - (t[t > sec] - sec) / max(r, 1e-3), 0, 1)
        return y * np.round(e * 15) / 15

    os.makedirs(outdir, exist_ok=True)
    for p in PIECES:
        notes, total, loop = notes_of(p)
        spb = 60.0 / p["bpm"]
        reps = 2 if loop else 1
        length = total * spb * reps + 1.5
        mix = np.zeros(int(length * SR))
        for rep in range(reps):
            for b, d, key, m in notes:
                if rep and b < loop[0]:
                    continue
                at = (b + (rep * (loop[1] - loop[0]) if rep else 0)) * spb
                sec = gate(key, d, spb) * spb
                vol = CHANNELS[key][2] / 127
                if key == "lead":
                    y = ds(harp, m, sec) * 0.9
                elif key == "sing":
                    y = ds(flute, m, sec) * 0.85
                elif key in ("pad_hi", "pad_lo"):
                    y = psg(m, sec, 0.125, 0.02, 0.5, 0.7, 0.1) * 0.11
                elif key == "harm":
                    y = psg(m, sec, 0.125, 0.004, 0.25, 0.4, 0.05) * 0.16
                elif key == "bass":
                    y = psg(m, sec, 0, 0, 1, 1, 0.03, "wave") * 0.55
                else:
                    y = psg(m, {"h": 0.01, "s": 0.05, "c": sec}[key], 0, 0, {"h": 0.012, "s": 0.05, "c": sec / 2.5}[key],
                            0, 0.02, "noise") * {"h": 0.2, "s": 0.32, "c": 0.09}[key]
                i = int(at * SR)
                j = min(len(mix), i + len(y))
                mix[i:j] += y[:j - i]
        nz = np.nonzero(np.abs(mix) > 1e-3)[0]
        mix = mix[:nz[-1] + int(0.15 * SR)] if len(nz) else mix
        mix *= 0.141 / (np.sqrt(np.mean(mix ** 2)) or 1)
        mix *= min(1.0, 0.95 / (np.abs(mix).max() or 1))
        path = os.path.join(outdir, "%s.wav" % p["id"])
        w = wave.open(path, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.round(mix * 127) / 127 * 32767).astype(np.int16).tobytes()); w.close()
    print("  preview: %d pieces in %s" % (len(PIECES), outdir))


def main():
    if "--preview" in sys.argv:
        preview(sys.argv[sys.argv.index("--preview") + 1])
        return
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
    fan = ", ".join("%s %d" % (p["id"], fanfare_frames(p)) for p in PIECES if p.get("fanfare"))
    print("  %d pieces and the toy piano's %d on voicegroup%03d; sFanfares frames: %s" % (len(PIECES), len(TOY), VOICEGROUP, fan))
    if not changed:
        print("  the game: unchanged")
    else:
        print("  the game: %s %d file(s): %s" % ("wrote" if "--write" in sys.argv else "would write", len(changed),
                                                 ", ".join(changed[:6]) + (" ..." if len(changed) > 6 else "")))


if __name__ == "__main__":
    main()
