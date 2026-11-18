#!/usr/bin/env python3
"""T-565 batch 1: the menu and UI sound effects -- three drafts to pick by ear, then ours in place of pret's.

    python3 tools/genuisounds.py                       # report: the twenty sounds, pret's length and ours, APPROVED
    python3 tools/genuisounds.py --draft [DIR]         # each style's .mid files (default audio/drafts/t565_ui)
    python3 tools/genuisounds.py --previews [DIR]      # an .mp3 (or .wav) of every sound in each style, and one
                                                       # "menu session" clip per style (default <draft dir>/previews)
    python3 tools/genuisounds.py --pret-ref DIR        # pret's own twenty and its session, rendered the same way, for
                                                       # comparing by ear -- RETAIL AUDIO: never into a tracked folder
    python3 tools/genuisounds.py --write --approved    # write APPROVED into engineGba (refuses while it is empty)
    python3 tools/genuisounds.py --batch 4 [MODE]      # the same for batch 4, the battle sounds (APPROVED_4, its own
                                                       # drafts in audio/drafts/t565_battle and a "battle moment" clip)
    python3 tools/genuisounds.py --batch 6 [MODE]      # the same for batch 6, the field sounds (APPROVED_6, its own
                                                       # drafts in audio/drafts/t565_field and an "a walk" clip)
    python3 tools/genuisounds.py --batch 10 [MODE]     # the same for batch 10, the moves' SE_M_* sounds (APPROVED_10,
                                                       # audio/drafts/t565_moves, "a battle's moves" in each style,
                                                       # "the palette" in C, MOVES.txt; the report checks the census)

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
    x:2    a noise tick    s:20  a noise shimmer    X:6  a noise thud (a hit landing)    r:4  a rest
    &...   (batch 4) starts with the token before it rather than after it: "X:6 &G4:4" is a thud under a note, and
           "C5:30 &G5:30" a chord. The square layer plays only the first note that starts on a frame (one square 1).
Notes are written in the harp's register; A plays them (not buzzes) an octave up. "b" in a sound replaces its notes
for B (and so for C's harp); "a" the same for A.

LENGTH AND LOUDNESS: no sound's last note ends later than pret's (pret's frames are read from its MIDI, not typed),
and none is louder than pret's at its peak: --previews renders pret's MIDI and ours through the same model and
scales a style's velocities down until it is not. --draft runs the same scaling, so a draft .mid is what was heard.
The model (--previews): m4a's mixer at 13379 Hz for the samples, the PSG synthesised with m4a's frame envelopes, the
noise from m4a's own gNoiseTable. A preview, not the GBA; the sweep and the echo are not modelled, and a pitch bend
is read at a note's start only (so pret's own swoops -- SE_EXP's rise, SE_MUGSHOT, SE_SHINY -- are heard as flat
notes in --pret-ref; ours use no bends, so ours are heard as they are).

BATCH 4 (--batch 4), the battle sounds apart from moves: the same three styles and the same voicegroup196, a little
bigger -- a hit has a noise thud under it, super-effective lands on a chord, not-very-effective deflates, the faint
falls through the pentatonic to the tritone. A sound's tracks never exceed its player's (SE1 3, SE2 9, SE3 1:
SE_LOW_HEALTH has one track, so C plays it with no square under the harp), and SE_LOW_HEALTH keeps pret's loop
(markers "[" and "]", 36 frames). The moves' SE_M_* sounds are batch 10; the instruments lane's are not here.

BATCH 6 (--batch 6), the field sounds: the same three styles on voicegroup196. A door is a thunk (a noise thud under a
short decaying square, a low harp pluck in B), not a melody; the weather is the noise channel -- rain is many small
ticks, "x=74:2" naming a tick's noise key, a lower key a lower noise, so thunder rolls down through the keys -- with
the harp's drips over it in B and C; the warps, the PIN, the unlock and the item sounds keep to the pentatonic. The
weather plays on SE3 (one track), so a "merge" sound puts every layer on that one track (m4a takes a note's voice
when the note starts, so the noise and the harp can share it: one program change before each note, in order); rain,
downpour and thunderstorm keep pret's loops ("[" at 16 frames, "]" at its end). Pret bends and sweeps several of
these (SE_FALL, SE_THUNDER, SE_ESCALATOR, SE_DOOR...); ours use none: a fall is stepped down the pentatonic.
The field uses of SE_M_CUT and SE_M_STRENGTH share their .mid with the battle animations, so they are batch 10's:
here they are SKETCHES only, heard in the "a walk" clip and drafted under batch10_sketch/, never written.

BATCH 10 (--batch 10), the move-animation sounds: 115 SE_M_* sounds in the same three styles on voicegroup196, each
given the type whose routines borrow it most (census10() reads the battle animation scripts and the C tasks they
start; the report fails loudly if the engine's animations have moved a sound to another type) and drawn from that
type's PALETTE in a SHAPE. Batch 6's two sketches are superseded here: Cut is VECTOR's edge, Strength STRATUM's hit.
The notes are not typed per sound but composed by shape_events(), so a palette changed redraws its whole type.
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
NOISE_KEY = {"x": 80, "s": 70, "X": 54}
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
BATCH, LABEL, CLIP = 1, "T-565 batch 1", "menu_session"

# ---------------------------------------------------------------------------------------------------------------------
# BATCH 4: the battle sounds apart from moves (docs/sound-census-2026-11-16.md). The same motif family: Blanche's C
# pentatonic for everything that goes well, the falling tritone (F# to C) for the faint.
# ---------------------------------------------------------------------------------------------------------------------
SOUNDS_4 = [
    dict(id="ball_open", what="a daemon sent out: the ball opening (every battle, every switch)",
         notes="x:2 C5:3 G5:3 ~C6:17"),
    dict(id="effective", what="a hit that lands as the chart expects (every ordinary hit)",
         notes="X:6 &G4:4 C4:30"),
    dict(id="super_effective", what="a hit the chart favours: it lands -- two strikes up, then a chord",
         notes="X:5 &C4:3 G4:3 C5:3 X:8 &E5:34 &G5:34 &~C6:40"),
    dict(id="not_effective", what="a hit the chart resists: it deflates, a falling fourth, quiet",
         notes="X:3 &G4:4 r:1 ^D4:10"),
    dict(id="faint", what="a daemon fainting: down the pentatonic to the falling tritone",
         notes="A5:4 G5:4 E5:4 D5:4 C5:5 r:2 F#4:6 ~C4:18"),
    dict(id="exp", what="the EXP bar filling (stopped when the bar is full, so any point is an ending)",
         notes="^C4:8 ^D4:8 ^E4:8 ^G4:8 ^A4:8 ^C5:8 ^D5:8 ^E5:8 ^G5:8 ^A5:8 ^C6:18"),
    dict(id="exp_max", what="the EXP bar full", notes="G5:4 ~C6:12"),
    dict(id="low_health", what="the low-HP alarm: loops (pret's 36-frame loop) on SE3, which has ONE track",
         notes="E4:6 r:6 ~C4:12", loop=36, mono=True),
    dict(id="flee", what="got away safely: a shimmer and a quick scurry up", notes="s:16 &E5:3 G5:3 A5:3 C6:3 D6:3 ~E6:20"),
    dict(id="mugshot", what="the leaders' and the Four's VS banners: a long rise, then a struck chord",
         notes="s:50 &C4:5 D4:5 E4:5 G4:5 A4:5 C5:5 D5:5 E5:5 G5:5 A5:5 X:6 &C5:70 &G5:70 &~C6:80"),
    dict(id="switch", what="a daemon called back", notes="x:2 G5:3 C5:3"),
    dict(id="ball_throw", what="a ball thrown: a shimmer under a rising arc", notes="s:14 &C5:4 E5:4 G5:4 C6:12"),
    dict(id="ball", what="the ball striking the daemon", notes="x:1 E5:2 C5:3"),
    dict(id="ball_bounce_1", what="the ball's first bounce", notes="x:1 G5:11"),
    dict(id="ball_bounce_2", what="the second, lower", notes="x:1 E5:11"),
    dict(id="ball_bounce_3", what="the third", notes="x:1 ^D5:11"),
    dict(id="ball_bounce_4", what="the fourth, the quietest", notes="x:1 ^C5:11"),
    dict(id="ball_click", what="the ball locking: caught (MUS_CAUGHT follows)", notes="x:2 G5:1 C6:2"),
    dict(id="ball_trade", what="a ball in the trade and the capture's wobble (SE2)", notes="s:4 &E5:3 G5:3 C6:9"),
    dict(id="ball_tray_enter", what="the party tray sliding in", notes="s:6 &^C6:3 ^E6:6"),
    dict(id="ball_tray_ball", what="a ball on the party tray", notes="^G5:3"),
    dict(id="ball_tray_exit", what="the party tray sliding out (SE2)", notes="x:2", b="^C6:2"),
    dict(id="shiny", what="a shiny daemon's sparkle", notes="^G5:3 ^C6:3 ^E6:3 ^G6:3 r:3 ^C6:3 ^E6:3 ~G6:12"),
    dict(id="deoxys_move", what="Birth Island's triangle moving (rare): the tritone, rising and falling",
         notes="s:30 &C5:4 F#5:4 C6:4 F#6:4 ~C6:40 r:6 ^F#5:4 ^C5:20"),
]
APPROVED_4 = {}                                    # the user's picks for batch 4; --write refuses while it is empty
APPROVED_4.update({s["id"]: "C" for s in SOUNDS_4})   # the user, 2026-11-17, by multiple choice: C BOTH (DRAFT)
LEFT_OUT_4 = ["every SE_M_* move sound (batch 10)", "the instruments lane's SE_SUCCESS, SE_FAILURE, SE_DING_DONG, "
              "SE_PC_LOGIN and SE_SHOP", "the songs and fanfares (MUS_CAUGHT, MUS_LEVEL_UP...)"]
# The "battle moment" clip: (seconds, sound[, stopped at]) -- sent out, a hit, super-effective, not-very-effective,
# the EXP bar filling and full, the low-HP alarm looping until the faint, then running away.
SESSION_4 = [(0.00, "ball_open"), (0.90, "effective"), (1.90, "super_effective"), (3.30, "not_effective"),
             (4.00, "exp", 5.30), (5.30, "exp_max"), (5.90, "low_health", 7.90), (7.90, "faint"), (9.00, "flee")]
PLAYER_4 = {"low_health": 3, "ball_trade": 2, "ball_tray_exit": 2}   # song_table.inc: the rest play on SE1
TRACKS = {1: 3, 2: 9, 3: 1}                        # music_player_table.inc: NUM_TRACKS_SE1, _SE2, _SE3

# ---------------------------------------------------------------------------------------------------------------------
# BATCH 6: the field sounds (docs/sound-census-2026-11-16.md, "Field"). Physical things are physical -- a door is a
# noise thud under a short decaying square, a wall a bump, the weather the noise channel -- and anything musical
# (a warp, the PIN, the unlock, the item sounds) keeps to Blanche's C pentatonic; the poison step borrows the falling
# tritone. "x=74:2" is a tick on noise key 74: lower is a lower noise, so thunder rolls down through the keys.
# ---------------------------------------------------------------------------------------------------------------------
def _ticks(frames, keys, gaps, start_key=0):
    """A run of noise ticks `frames` long: rain, applause. Deterministic: the keys and gaps cycle."""
    out, at, k = [], 0, start_key
    while at < frames:
        g = gaps[k % len(gaps)]
        g = min(g, frames - at)
        out.append("x=%d:%d" % (keys[k % len(keys)], g))
        at += g
        k += 1
    return " ".join(out)


_RAIN_IN = "x=78:4 r:5 x=72:3 r:4"                     # 16 frames: the first drops
_RAIN = _ticks(41, (76, 70, 80, 73, 68, 78, 71), (3, 2, 4, 3, 2, 3, 4, 2))      # the loop, 16..57
_RAIN_B = "^G6:8 ^E6:8 r:8 ^C7:8 ^A6:9"                # B's drips over the loop (41 frames)
_POUR = _ticks(25, (66, 60, 70, 63, 58, 68), (2, 2, 1, 2, 2, 1, 2))            # downpour's loop, 16..41
_STORM = _ticks(41, (70, 62, 74, 66, 60, 72), (2, 3, 2, 2, 3, 2))               # thunderstorm's loop, 16..57
_APPLAUSE = _ticks(240, (82, 76, 86, 72, 80, 78, 84, 74, 79), (3, 2, 4, 2, 3, 2, 3, 5, 2, 3))

SOUNDS_6 = [
    # doors and the ways in and out
    dict(id="door", what="a door opening, in or out (every house, every shop)", notes="X:3 &^G3:3 ^C3:10"),
    dict(id="sliding_door", what="an automatic door (the CHECKPOINTS, the marts)", notes="s:10 &^E5:2 ^A5:8"),
    dict(id="exit", what="stepping out over a mat (14 call sites)", notes="x:2 &^G4:3 r:3 x:2 &^E4:3 r:3 x:2 &^C4:10"),
    dict(id="rs_door", what="the Game Corner's and the League's doors", notes="X:4 &^D3:4 r:2 ^A3:4 ^D3:12"),
    dict(id="warp_in", what="a warp taking the player (27 sites: PLAY's door, THE NEXUS, the pads)",
         notes="C5:3 D5:3 E5:3 G5:3 A5:3 C6:3 D6:3 E6:3 ~G6:18"),
    dict(id="warp_out", what="arriving from a warp", notes="G6:3 E6:3 D6:3 C6:3 A5:3 G5:3 E5:3 D5:3 ~C5:20"),
    dict(id="lavaridge_fall_warp", what="dropping through the floor (a field effect; the Tanoby key)",
         notes="s:30 &A5:4 G5:4 E5:4 D5:4 C5:4 A4:4 G4:4 E4:4 D4:4 C4:4 X:8 &^C3:8"),
    dict(id="m_dive", what="diving (a field-only move sound: nothing in battle plays it; pret's FRLG has no sea to "
         "dive in, so it is likely never heard)", notes="s:16 &^G4:3 ^E4:3 ^C4:3 X:4 &^G3:4 r:6 ^C5:3 ^E5:3 ^G5:6"),
    # moving about
    dict(id="ledge", what="a ledge hopped", notes="^E5:3 r:3 X:3 &^C4:3"),
    dict(id="wall_hit", what="walking into a wall (SE2; every step against one)", notes="X:4 &^C3:6"),
    dict(id="bike_hop", what="the bike's hop", notes="x:1 ^G5:3"),
    dict(id="bike_bell", what="the bike's bell", notes="E6:2 G6:10 r:4 E6:2 G6:40"),
    dict(id="puddle", what="a step in a puddle (SE2)", notes="s:6 &^A5:2 ^E6:6"),
    dict(id="fall", what="falling down a hole: pret's is a pitch sweep; ours steps down the pentatonic",
         notes="s:20 &^C6:3 ^A5:3 ^G5:3 ^E5:3 ^D5:3 ^C5:3 ^A4:3 ^G4:3 X:8 &^C3:8"),
    dict(id="ice_break", what="the floor's ice giving way (Victory Road)",
         notes="X:4 &s:14 &^G6:2 ^D6:2 ^A5:2 ^E5:3 ^C5:6"),
    dict(id="ice_crack", what="the floor's ice cracking", notes="x:2 &^E6:2 ^A6:3"),
    dict(id="escalator", what="the escalator's hum", notes="s:96 &^C4:4 r:44 ^G3:4"),
    dict(id="elevator", what="the lift (the school's): a hum, then the ding on arrival",
         notes="s:150 &^C3:4 r:60 ^G2:4 r:82 E5:4 ~C6:40"),
    # events
    dict(id="pin", what='the "!" over a head (31 sites), and an item found', notes="x:1 &C6:3 ~G6:14"),
    dict(id="unlock", what="a lock opening (18 sites; SE2)", notes="x:2 &^G4:2 r:3 X:3 &C5:3 G5:4 ~C6:10"),
    dict(id="repel", what="a REPEL sprayed", notes="s:16 &^C6:2 ^G5:2 ^E5:2 ^C5:8"),
    dict(id="itemfinder", what="the ITEMFINDER's ping", notes="^C6:3 r:5 ^C6:3 r:5 E6:3 ~G6:12"),
    dict(id="field_poison", what="a poisoned daemon hurt by a step: the falling tritone, buzzed",
         notes="!F#4:4 r:2 !C4:10"),
    dict(id="egg_hatch", what="an egg hatching: two cracks and out", notes="X:2 &^E5:2 r:2 X:2 &^G5:2 r:2 x:2 &C6:4 ~E6:9"),
    dict(id="applause", what="the Hall of Fame's applause", notes=_APPLAUSE,
         b="^C6:6 r:20 ^E6:6 r:16 ^G6:6 r:24 ^A6:6 r:14 ^C7:6 r:30 ^G6:6 r:20 ^E6:6 r:40 ^C6:6"),
    dict(id="vend", what="a drink dropping from the machine", notes="X:3 &^C4:3 x:2 ^G4:4"),
    dict(id="bang", what="a heavy door forced open (the Dotted Hole)", notes="X:12 &^C3:12 r:4 X=46:20 &^G2:20"),
    dict(id="ship", what="the SEAGALLOP under way: an engine's thrum",
         notes="s:100 &^C3:3 r:22 ^C3:3 r:22 ^C3:3 r:22 ^C3:3"),
    dict(id="ss_anne_horn", what="the ship's horn: two blasts", notes="~G3:60 &~C3:60 r:20 ~G3:100 &~C3:100"),
    dict(id="truck_move", what="a great weight moving (the Tanoby key; loops, as pret's does, until the script stops it)",
         notes="X=46:6 &^C3:6 r:18 X=42:6 &^G2:6 r:18 " * 4 + "X=46:6 &^C3:6 r:18 X=42:6 &^G2:6 r:18 " * 4,
         loop=(96, 384)),
    dict(id="contest_curtain_fall", what="Bill's teleporter", notes="s:10 &^C6:2 ^G5:2 ^E5:2 ^C5:4"),
    dict(id="contest_mons_turn", what="the VS SEEKER charging", notes="^C5:2 ^E5:2 ^G5:2 ^C6:2 ^E6:2 ^G6:2 r:2 ~C6:8"),
    dict(id="contest_place", what="the slot machine's reel stopping (SE2)", notes="X:3 &C5:3 r:2 G5:4 r:2 ~C6:16"),
    # weather: SE3, one track -- every layer merged onto it
    dict(id="rain", what="rain beginning, then falling (loops 16..57 frames, as pret's)", mono="merge",
         notes=_RAIN_IN + " " + _RAIN, b="^C6:4 r:12 " + _RAIN_B, loop=(16, 57)),
    dict(id="rain_stop", what="rain stopping: the drops thin out", mono="merge",
         notes="x=76:3 r:3 x=70:3 r:5 x=78:2 r:7 x=72:2 r:8", b="^G6:6 r:10 ^E6:8 r:9"),
    dict(id="downpour", what="a downpour (loops 16..41)", mono="merge",
         notes="x=70:3 r:2 x=64:3 r:2 x=68:2 r:2 x=62:2 " + _POUR, b="^C6:4 r:12 ^G5:6 ^E6:6 r:6 ^A5:7",
         loop=(16, 41)),
    dict(id="downpour_stop", what="a downpour easing", mono="merge",
         notes="x=66:2 r:1 x=60:2 r:2 x=68:2 r:3 x=62:2 r:5 x=70:2 r:6 x=64:2", b="^E6:6 r:10 ^C6:10"),
    dict(id="thunderstorm", what="a thunderstorm's rain (loops 16..57; the thunder is SE_THUNDER's)", mono="merge",
         notes="x=72:3 r:3 x=64:3 r:3 x=70:4 " + _STORM, b="^A5:4 r:12 ^E6:8 r:8 ^C6:8 r:8 ^G5:9",
         loop=(16, 57)),
    dict(id="thunderstorm_stop", what="a thunderstorm passing", mono="merge",
         notes="x=70:3 r:2 x=62:3 r:4 x=74:2 r:6 x=66:2 r:9", b="^E6:6 r:12 ^A5:12"),
    dict(id="thunder", what="thunder: a crack, then a roll down through the noise keys",
         notes="x=88:3 X=58:10 X=50:16 X=44:24 X=40:30", b="^C4:3 ^G2:30 &^C3:30 r:20 ^G2:28"),
    dict(id="thunder2", what="thunder, the second (a nearer strike)",
         notes="X=60:4 X=52:12 X=46:22 X=40:30", b="^G2:4 ^C3:34 &^G2:34 r:20 ^C2:10"),
    # SKETCHES for batch 10: the field uses of two move sounds that share their .mid with the battle animations.
    dict(id="m_cut", what="SKETCH (batch 10): Cut in the field, a swish and a snip -- shares se_m_cut.mid with battle",
         notes="s:8 &^G5:3 ^D5:3 x=86:2 &^A5:2 r:2 ^E5:6", sketch=True),
    dict(id="m_strength", what="SKETCH (batch 10): Strength pushing a boulder -- shares se_m_strength.mid with battle",
         notes="X=50:6 &^C3:6 r:2 X=44:12 &^G2:12", sketch=True),
]
APPROVED_6 = {}                                    # the user's picks for batch 6; --write refuses while it is empty
APPROVED_6.update({s["id"]: "C" for s in SOUNDS_6 if s["id"] not in ("m_cut", "m_strength")})   # the user, 2026-11-17, by multiple choice: C BOTH (DRAFT)
LEFT_OUT_6 = ["the field uses of SE_M_CUT, STRENGTH, ROCK_THROW, FLY, DIG and TELEPORT (one .mid each, shared with "
              "the battle animations: batch 10; Cut and Strength sketched here for the clip only)",
              "SE_GLASS_FLUTE (an instrument: the instruments lane's)", "the toy piano SE_NOTE_*",
              "SE_CHIME, SE_SUNRISE, SE_NIGHTFALL (the instruments lane's, built)",
              "the field SE_M_HEAL_BELL and SE_M_MORNING_SUN (the instruments lane's notes)",
              "SE_POKE_JUMP_FAILURE (named only in a comment in start_menu.c; otherwise the wireless minigame)"]
# The "a walk" clip: in at a door, out over the mat, a ledge, the PIN on a found item, a lock, a warp there and back,
# a bush cut and a boulder pushed (batch 10 sketches), then rain with one thunder, and the rain stopping.
SESSION_6 = [(0.00, "door"), (1.00, "exit"), (1.90, "ledge"), (2.60, "pin"), (3.30, "unlock"), (4.10, "warp_in"),
             (5.00, "warp_out"), (5.90, "m_cut"), (6.60, "m_strength"), (7.20, "rain", 9.80), (8.30, "thunder"),
             (9.80, "rain_stop")]
PLAYER_6 = {"wall_hit": 2, "unlock": 2, "puddle": 2, "contest_place": 2, "rain": 3, "rain_stop": 3, "downpour": 3,
            "downpour_stop": 3, "thunderstorm": 3, "thunderstorm_stop": 3}   # song_table.inc: the rest play on SE1


# ---------------------------------------------------------------------------------------------------------------------
# BATCH 10: the move-animation sounds (docs/sound-census-2026-11-16.md, batch 10). 115 SE_M_* sounds, each REPLACED in
# place like every batch before it -- so one .mid serves every routine that borrows it, and each is given the type
# whose routines borrow it most (census10(): a tie goes to the type that is not CONTENT, then to the chart's order;
# OVERRIDE_10 for the four a count cannot settle). Each TYPE has a PALETTE -- a motif, a register and a texture -- so
# a player can learn a type by ear, and each sound is its type's palette played in a SHAPE that matches what the sound
# does (a hit, a beam, a spray, a wave...). The motif family holds: every motif is Blanche's C pentatonic except
# CORRUPT's, the pentatonic with a note bent off it, and a stat falling ends on the falling tritone. The physical
# shapes (a hit, strikes, a bite, a burst, a bind) lean on the noise channel. A sound is written as EVENTS
# ((frame, frames, token)), serialised into the token language above and clamped to pret's own last frame, so it is
# never longer than pret's; the loudness check is the one every batch uses.
# ---------------------------------------------------------------------------------------------------------------------
CHART = ["CONTENT", "LOGIC", "VECTOR", "CORRUPT", "STRATUM", "LEGACY", "SWARM", "LATENT", "ENTROPY", "FLOW", "GROWTH",
         "SIGNAL", "CONTEXT", "FROZEN", "EMERGENT", "HARDENED", "OPAQUE"]
TYPE_OF_VANILLA = {"NORMAL": "CONTENT", "FIGHTING": "LOGIC", "FLYING": "VECTOR", "POISON": "CORRUPT",
                   "GROUND": "STRATUM", "ROCK": "LEGACY", "BUG": "SWARM", "GHOST": "LATENT", "STEEL": "HARDENED",
                   "MYSTERY": "MYSTERY", "FIRE": "ENTROPY", "WATER": "FLOW", "GRASS": "GROWTH", "ELECTRIC": "SIGNAL",
                   "PSYCHIC": "CONTEXT", "ICE": "FROZEN", "DRAGON": "EMERGENT", "DARK": "OPAQUE"}

# m: the motif (harp register; A plays it an octave up), art: how a motif note is played ("" a key, "^" thin, "!" a
# buzz), hold: the last note held (the FLUTE in C), thud: the noise key under a hit (None: no noise under it), tex: the
# texture's noise ("x" ticks, "s" shimmer, "X" rumble; None: none) and its keys, step: the pace in frames.
PALETTE = {
    "CONTENT":  dict(m=["C5", "G5", "C6", "G5"], art="", hold=False, thud=54, tex="x", keys=(80,), step=3,
                     line="bone: the plain fifth C-G in the middle, a square key and one tick -- the undifferentiated"),
    "LOGIC":    dict(m=["C4", "D4", "E4", "G4"], art="", hold=False, thud=50, tex="x", keys=(86,), step=3,
                     line="a proof: steps up C-D-E-G, low-middle, even and firm, each step on a clockwork tick"),
    "VECTOR":   dict(m=["G5", "C6", "G6", "C7"], art="^", hold=False, thud=64, tex="s", keys=(70,), step=2,
                     line="an arrow: leaps of a fifth and an octave, high and thin, over a shimmer of air"),
    "CORRUPT":  dict(m=["E4", "F4", "C4", "F#4"], art="!", hold=False, thud=52, tex="x", keys=(60, 66, 58, 70), step=4,
                     line="the pentatonic with a note bent off it (E-F, C-F#), buzzed, low-middle, over an "
                     "irregular low bubbling"),
    "STRATUM":  dict(m=["C3", "G2", "C3", "E3"], art="^", hold=False, thud=44, tex="X", keys=(46, 42, 48), step=6,
                     line="the floor: C-G at the bottom of the range, slow, a decaying square over the deep rumble"),
    "LEGACY":   dict(m=["G4", "E4", "C4", "A3"], art="", hold=False, thud=50, tex="x", keys=(58, 64, 54), step=4,
                     line="an old chime falling G-E-C-A, middle-low, a dull clack under it"),
    "SWARM":    dict(m=["A5", "G5", "A5", "E5"], art="^", hold=False, thud=70, tex="x", keys=(86, 82, 88, 84), step=1,
                     line="many small things: a fast thin A-G trill, high, in a cloud of quick ticks"),
    "LATENT":   dict(m=["A3", "C4", "E4", "A4"], art="^", hold=True, thud=None, tex=None, keys=(), step=6,
                     line="something waking: A-C-E rising slowly from low, thin, held at the top; no noise at all"),
    "ENTROPY":  dict(m=["E5", "G5", "A5", "G5"], art="", hold=False, thud=60, tex="s", keys=(72, 84, 66, 78, 90),
                     step=2, line="a flicker E-G-A-G, middle-high and quick, over a shimmer and crackling ticks"),
    "FLOW":     dict(m=["A5", "G5", "E5", "D5", "C5"], art="", hold=True, thud=66, tex="s", keys=(64,), step=3,
                     line="a descent: the pentatonic run down A-G-E-D-C, the harp leading, a soft splash, held at the "
                     "bottom"),
    "GROWTH":   dict(m=["C5", "D5", "E5", "G5", "A5"], art="", hold=True, thud=62, tex="x", keys=(82,), step=4,
                     line="fitting: the pentatonic climbing C-D-E-G-A at a steady pace, soft ticks, held at the top"),
    "SIGNAL":   dict(m=["C6", "C6", "G6", "C6"], art="!", hold=False, thud=72, tex="x", keys=(88, 90), step=2,
                     line="current: one high C repeated fast and buzzed, a fifth flicked in, sharp high ticks"),
    "CONTEXT":  dict(m=["E5", "A5", "E5", "A5"], art="", hold=True, thud=None, tex=None, keys=(), step=3,
                     line="a frame: a tremolo between E and A, middle-high, no noise at all, the flute holding it"),
    "FROZEN":   dict(m=["E6", "G6", "C7", "G6"], art="^", hold=False, thud=76, tex="x", keys=(90, 88), step=2,
                     line="brittle: the top of the range, sparse thin E-G-C, a glassy high tick"),
    "EMERGENT": dict(m=["C4", "G4", "E5", "C6"], art="", hold=True, thud=48, tex="s", keys=(70,), step=4,
                     line="the whole range at once: C-G-E-C stacked low to high into one chord, a deep thud"),
    "HARDENED": dict(m=["C5", "C6", "G5", "C6"], art="", hold=False, thud=58, tex="s", keys=(74,), step=3,
                     line="metal: an octave clang C-C, middle, a short metallic shimmer under each strike"),
    "OPAQUE":   dict(m=["A3", "E3", "D3", "A2"], art="!", hold=False, thud=52, tex=None, keys=(), step=4,
                     line="the dark: a low falling fourth A-E, muffled and buzzed, short, no shimmer"),
}

SHAPE_WHAT = {"hit": "a hit", "hits": "strikes", "slash": "an edge", "bite": "jaws closing", "beam": "a beam",
              "burst": "a burst", "spray": "a spray of small things", "wave": "a wave over the field",
              "weather": "weather", "rise": "a stat rising", "fall": "a stat falling (the tritone)", "heal": "a heal",
              "status": "a status taking hold", "call": "a voice or a song", "charge": "a charge building",
              "bind": "a bind squeezing", "tick": "a tick", "swish": "a rush of air", "pop": "a pop",
              "glint": "a glint"}

# (sound, type, shape). The type is census10()'s dominant one, or OVERRIDE_10's; the report says if they drift apart.
TABLE_10 = [
    # CONTENT (39)
    ("m_attract", "CONTENT", "pop"), ("m_baton_pass", "CONTENT", "swish"), ("m_belly_drum", "CONTENT", "hits"),
    ("m_bubble2", "CONTENT", "pop"), ("m_charm", "CONTENT", "status"), ("m_comet_punch", "CONTENT", "hit"),
    ("m_confuse_ray", "CONTENT", "beam"), ("m_double_slap", "CONTENT", "hit"), ("m_double_team", "CONTENT", "swish"),
    ("m_dragon_rage", "CONTENT", "charge"), ("m_flatter", "CONTENT", "pop"), ("m_headbutt", "CONTENT", "hit"),
    ("m_hyper_beam", "CONTENT", "beam"), ("m_leer", "CONTENT", "glint"), ("m_milk_drink", "CONTENT", "heal"),
    ("m_minimize", "CONTENT", "tick"), ("m_moonlight", "CONTENT", "heal"), ("m_perish_song", "CONTENT", "call"),
    ("m_psybeam2", "CONTENT", "beam"), ("m_razor_wind", "CONTENT", "slash"), ("m_razor_wind2", "CONTENT", "slash"),
    ("m_scratch", "CONTENT", "slash"), ("m_self_destruct", "CONTENT", "burst"), ("m_snore", "CONTENT", "call"),
    ("m_swagger", "CONTENT", "rise"), ("m_swagger2", "CONTENT", "status"), ("m_sweet_scent", "CONTENT", "spray"),
    ("m_swift", "CONTENT", "spray"), ("m_swords_dance", "CONTENT", "rise"), ("m_tail_whip", "CONTENT", "pop"),
    ("m_take_down", "CONTENT", "hit"), ("m_teeter_dance", "CONTENT", "status"), ("m_teleport", "CONTENT", "heal"),
    ("m_tri_attack", "CONTENT", "beam"), ("m_uproar", "CONTENT", "call"), ("m_vicegrip", "CONTENT", "bind"),
    ("m_yawn", "CONTENT", "call"), ("m_stat_increase", "CONTENT", "rise"), ("m_stat_decrease", "CONTENT", "fall"),
    # LOGIC (6)
    ("m_detect", "LOGIC", "glint"), ("m_jump_kick", "LOGIC", "hit"), ("m_mega_kick", "LOGIC", "hit"),
    ("m_sky_uppercut", "LOGIC", "rise"), ("m_vital_throw", "LOGIC", "hits"), ("m_vital_throw2", "LOGIC", "hits"),
    # VECTOR (4)
    ("m_cut", "VECTOR", "slash"), ("m_fly", "VECTOR", "swish"), ("m_gust", "VECTOR", "weather"),
    ("m_wing_attack", "VECTOR", "hits"),
    # CORRUPT (5)
    ("m_acid_armor", "CORRUPT", "status"), ("m_bubble3", "CORRUPT", "spray"), ("m_dig", "CORRUPT", "burst"),
    ("m_mist", "CORRUPT", "weather"), ("m_toxic", "CORRUPT", "status"),
    # STRATUM (6)
    ("m_bonemerang", "STRATUM", "hits"), ("m_earthquake", "STRATUM", "wave"), ("m_mega_kick2", "STRATUM", "hit"),
    ("m_sand_attack", "STRATUM", "spray"), ("m_sand_tomb", "STRATUM", "bind"), ("m_strength", "STRATUM", "hit"),
    # LEGACY (2)
    ("m_rock_throw", "LEGACY", "hits"), ("m_sandstorm", "LEGACY", "weather"),
    # SWARM (2)
    ("m_bubble_beam", "SWARM", "beam"), ("m_string_shot", "SWARM", "spray"),
    # LATENT (4)
    ("m_encore", "LATENT", "pop"), ("m_lick", "LATENT", "status"), ("m_nightmare", "LATENT", "call"),
    ("m_string_shot2", "LATENT", "beam"),
    # ENTROPY (6)
    ("m_ember", "ENTROPY", "spray"), ("m_explosion", "ENTROPY", "burst"), ("m_flamethrower", "ENTROPY", "beam"),
    ("m_flame_wheel", "ENTROPY", "swish"), ("m_heat_wave", "ENTROPY", "wave"), ("m_sacred_fire", "ENTROPY", "burst"),
    # FLOW (7)
    ("m_bubble", "FLOW", "spray"), ("m_crabhammer", "FLOW", "hit"), ("m_hydro_pump", "FLOW", "beam"),
    ("m_rain_dance", "FLOW", "weather"), ("m_surf", "FLOW", "wave"), ("m_waterfall", "FLOW", "burst"),
    ("m_whirlpool", "FLOW", "bind"),
    # GROWTH (6)
    ("m_absorb", "GROWTH", "heal"), ("m_absorb_2", "GROWTH", "heal"), ("m_grasswhistle", "GROWTH", "call"),
    ("m_petal_dance", "GROWTH", "spray"), ("m_poison_powder", "GROWTH", "spray"), ("m_sing", "GROWTH", "call"),
    # SIGNAL (4)
    ("m_charge", "SIGNAL", "charge"), ("m_thunderbolt", "SIGNAL", "beam"), ("m_thunderbolt2", "SIGNAL", "status"),
    ("m_thunder_wave", "SIGNAL", "wave"),
    # CONTEXT (12)
    ("m_barrier", "CONTEXT", "glint"), ("m_bind", "CONTEXT", "bind"), ("m_cosmic_power", "CONTEXT", "rise"),
    ("m_horn_attack", "CONTEXT", "hit"), ("m_metronome", "CONTEXT", "call"), ("m_psybeam", "CONTEXT", "beam"),
    ("m_reflect", "CONTEXT", "glint"), ("m_reversal", "CONTEXT", "swish"), ("m_sketch", "CONTEXT", "pop"),
    ("m_solar_beam", "CONTEXT", "beam"), ("m_supersonic", "CONTEXT", "wave"), ("m_dizzy_punch", "CONTEXT", "status"),
    # FROZEN (5)
    ("m_blizzard", "FROZEN", "weather"), ("m_bubble_beam2", "FROZEN", "beam"), ("m_hail", "FROZEN", "spray"),
    ("m_haze", "FROZEN", "weather"), ("m_icy_wind", "FROZEN", "slash"),
    # EMERGENT (2)
    ("m_sacred_fire2", "EMERGENT", "burst"), ("m_twister", "EMERGENT", "wave"),
    # HARDENED (2)
    ("m_harden", "HARDENED", "glint"), ("m_screech", "HARDENED", "call"),
    # OPAQUE (3)
    ("m_bite", "OPAQUE", "bite"), ("m_encore2", "OPAQUE", "call"), ("m_faint_attack", "OPAQUE", "swish"),
]
# Where a count does not decide: no routine borrows it, or a general animation is what a player mostly hears it in.
OVERRIDE_10 = {"m_stat_increase": ("CONTENT", "every stat that rises (General_StatsChange); only SKY_ATTACK borrows it"),
               "m_stat_decrease": ("CONTENT", "every stat that falls (General_StatsChange); no routine borrows it"),
               "m_absorb_2": ("GROWTH", "INGRAIN's and WISH's heal at a turn's end; no routine borrows it"),
               "m_dizzy_punch": ("CONTEXT", "the confusion status (Status_Confusion); no routine borrows it")}
SIGNATURE_10 = {"CONTENT": "m_take_down", "LOGIC": "m_vital_throw2", "VECTOR": "m_wing_attack", "CORRUPT": "m_toxic",
                "STRATUM": "m_earthquake", "LEGACY": "m_rock_throw", "SWARM": "m_string_shot", "LATENT": "m_lick",
                "ENTROPY": "m_ember", "FLOW": "m_bubble", "GROWTH": "m_absorb", "SIGNAL": "m_thunder_wave",
                "CONTEXT": "m_supersonic", "FROZEN": "m_icy_wind", "EMERGENT": "m_twister",
                "HARDENED": "m_harden", "OPAQUE": "m_bite"}
LOOP_10 = {"m_gust": (24, 72), "m_blizzard": (24, 72)}      # pret's own loops ("[" at 24 frames, "]" at 72)

# T-583: THE SHARED ROLES. Three sounds are played by routines of every type, so each spoke CONTENT for all of them:
# SE_M_COMET_PUNCH (a hit: genanims' default cue, and a borrowed vanilla hit), SE_M_MINIMIZE (the tick of every stat
# step a routine draws) and SE_M_MOONLIGHT (the witching hour's light, one script for seventeen routines). The engine
# now plays each by the ROUTINE's type (`playtypesewithpan ROLE`, battle_anim.c), from a table genanims.py writes out
# of role_sounds_10(): CONTENT keeps the sound it had, and every other type gets its own batch-10 sound in the first
# shape of the role's list that it has, the one nearest the shared sound's own length (a tick is short, a light long),
# and no longer than the role's limit, nor one of pret's loops. A type with nothing in the list keeps CONTENT's, and the report says so.
ROLES_10 = {
    "HIT":  dict(se="m_comet_punch", most=60, shapes=["hit", "hits", "bite", "slash", "burst", "bind", "pop", "spray",
                                                      "status", "glint", "swish", "beam"]),
    "TICK": dict(se="m_minimize", most=60, shapes=["tick", "pop", "hits", "hit", "slash", "bite", "spray", "glint",
                                                   "status", "burst", "bind", "rise"]),
    "HEAL": dict(se="m_moonlight", most=120, shapes=["heal", "rise", "glint", "charge", "call", "status", "wave",
                                                     "weather", "beam", "swish", "spray", "pop", "burst", "bind",
                                                     "hits", "hit", "slash", "bite"]),
    # T-589: THE STAT ARROW. General_StatsChange is no routine, so these three are played by the type of the MOVE that
    # changed the stat (the battle engine sends it with the arrow; an ability or an item sends none, and CONTENT's
    # plays). `only` keeps them to that script: SWAGGER and SWAGGER2 are also borrowed by routines, which still play
    # them by name. Capped at 30 frames, STAT_DECREASE's own length, the longest of the arrow's three; a fall never
    # borrows a rise or a heal, nor a rise a fall.
    "RISE":  dict(se="m_swagger", most=30, only="General_StatsChange",
                  shapes=["rise", "glint", "charge", "heal", "status", "pop", "call", "swish", "spray", "beam", "hits",
                          "hit", "slash", "bite", "burst", "bind", "tick", "wave", "weather"]),
    "RISE2": dict(se="m_swagger2", most=30, only="General_StatsChange",
                  shapes=["status", "rise", "glint", "charge", "heal", "pop", "call", "swish", "spray", "beam", "hits",
                          "hit", "slash", "bite", "burst", "bind", "tick", "wave", "weather"]),
    "FALL":  dict(se="m_stat_decrease", most=30, only="General_StatsChange",
                  shapes=["fall", "status", "bind", "pop", "glint", "tick", "swish", "hits", "hit", "bite", "slash",
                          "spray", "burst", "call", "beam", "wave", "weather", "charge"]),
}


def sound_length_10(d):
    """A batch-10 sound's own length in frames: where its last event ends."""
    return max(a + n for a, n, _, _ in tokens(d["notes"]))


def role_sounds_10():
    """{role: {type: (sound id, how)}} -- how is "own" (CONTENT's, the shared sound), "exact" (the type has the role's
    own shape), "nearest" (a later shape in the role's list) or "none" (nothing fits: CONTENT's is kept)."""
    built = build_10()
    length = {d["id"]: sound_length_10(d) for d in built}
    out = {}
    for role, r in ROLES_10.items():
        want = length[r["se"]]
        own = next(d["shape"] for d in built if d["id"] == r["se"])
        row = {}
        for ty in CHART:
            if ty == "CONTENT":
                row[ty] = (r["se"], "own")
                continue
            pick = None
            for shape in r["shapes"]:
                fits = [d["id"] for d in built if d["type"] == ty and d["shape"] == shape and length[d["id"]] <= r["most"]
                        and d["id"] not in LOOP_10]
                if fits:
                    pick = (min(fits, key=lambda s: abs(length[s] - want)), "exact" if shape == own else "nearest")
                    break
            row[ty] = pick or (r["se"], "none")
        out[role] = row
    return out
LEFT_OUT_10 = ["SE_M_HEAL_BELL and SE_M_MORNING_SUN (their field uses -- GOTO's ribbon, the unity and spirits scenes, "
               "the NOTEBOOK -- are the instruments lane's notes, and one .mid serves battle and field alike)",
               "SE_M_DIVE (field only; batch 6's, approved)",
               "SE_M_SPIT_UP, SE_M_HYPER_BEAM2, SE_M_LOCK_ON (outside battle only: the region map, the Fame "
               "Checker, the item-use scene)",
               "SE_M_BLIZZARD2 (only AIR_CUTTER's vanilla task played it, and DAEMONS redrew AIR_CUTTER)",
               "the eight nothing plays: GUST2, FLAME_WHEEL2, FIRE_PUNCH, PAY_DAY, BRICK_BREAK, GIGA_DRAIN, "
               "TRI_ATTACK2, ATTRACT2"]


def note_key(note):
    m = NOTE_RE.match(note)
    return 12 * (int(m.group(3)) + 1) + SEMI[m.group(2)]


def shape_events(pal, shape, F, sid=""):
    """[(frame, frames, token)] -- the palette in this shape, before clamping to F (pret's last frame)."""
    m, art, st, th = pal["m"], pal["art"], pal["step"], pal["thud"]
    top = "~" if pal["hold"] else art                     # how a shape's last, longest note is played
    up = sorted(set(m), key=note_key)
    note = lambda k: art + m[k % len(m)]
    thud = lambda at, n: [(at, n, "X=%d" % th)] if th else []
    keys = pal["keys"] or (80,)
    tex = lambda at, n, i=0: [(at, n, "%s=%d" % (pal["tex"], keys[i % len(keys)]))] if pal["tex"] else []
    v = sum(map(ord, sid)) % len(m)                       # a sound's own turn of the motif, so two hits differ
    ev = []
    if shape == "hit":
        ev += thud(0, 4) + [(0, 3, note(v)), (3, max(4, min(F - 3, 10)), top + m[(v + 1) % len(m)])]
    elif shape == "hits":
        gap = max(3, min(F // 3, 6))
        ev += thud(0, 2) + [(0, 2, note(v))] + thud(gap, 3) + [(gap, max(3, min(F - gap, 8)), note(v + 2))]
        if F >= 3 * gap:
            ev += thud(2 * gap, 3) + [(2 * gap, min(F - 2 * gap, 10), top + m[(v + 1) % len(m)])]
    elif shape == "slash":
        hi = up[::-1]
        ev += tex(0, min(8, F)) + [(0, 2, art + hi[0]), (2, 2, art + hi[1 % len(hi)]), (4, 2, art + hi[2 % len(hi)])]
        ev += [(6, 1, "x=86"), (7, max(3, min(F - 7, 8)), art + hi[-1])]
    elif shape == "bite":
        ev += thud(0, 3) + [(0, 3, note(0)), (0, 3, m[2]), (5, 2, "x=82"), (5, max(4, min(F - 5, 9)), note(1))]
    elif shape == "beam":
        L = min(F, 60)
        t, k = 0, v
        while t + st < L - 2 * st:
            ev.append((t, st, note(k)))
            ev += tex(t, 1, k) if pal["tex"] == "x" and k % 2 == 0 else []
            t, k = t + st, k + 1
        ev += (tex(0, L) if pal["tex"] in ("s", "X") else []) + [(t, max(2, L - t), top + m[k % len(m)])]
    elif shape == "burst":
        L = min(F, 40)
        h = min(L, 12)
        ev += thud(0, h) + [(0, h, x) for x in up] + tex(max(0, h - 2), max(2, L - h), 1)
        ev += [(h, max(2, L - h), top + up[0])]
    elif shape == "spray":
        L, gap = min(F, 36), max(2, 2 * st)
        t, k = 0, v
        while t < L:
            ev += tex(t, 1, k) + [(t + 1, max(1, gap - 1), "^" + m[k % len(m)])]
            t, k = t + gap, k + 1
    elif shape in ("wave", "weather"):
        L = min(F, 120) if shape == "wave" else F
        lp = LOOP_10.get(sid)
        if pal["tex"] in ("x", "X"):
            g = max(2, st)
            t, k = 0, 0
            while t < L:
                ev += tex(t, min(g, L - t), k)
                t, k = t + g, k + 1
        elif pal["tex"] == "s":                          # a loop restarts inside it, so a loop gets its own
            ev += tex(0, lp[0]) + tex(lp[0], L - lp[0]) if lp else tex(0, L)
        seq = m + m[-2::-1] if shape == "wave" else m
        t0 = lp[0] if lp else 0
        gap = max(st * 2, ((lp[1] - lp[0]) if lp else L) // (len(seq) + 1))
        for i, x in enumerate(seq):
            if t0 + i * gap < L:
                ev.append((t0 + i * gap, min(gap, L - t0 - i * gap), ("^" if shape == "weather" else art) + x))
        if lp:
            ev += [(0, st, "^" + m[0]), (st * 2, st, "^" + m[1])]
    elif shape == "rise":
        for i, x in enumerate(up):
            lastone = i == len(up) - 1
            ev.append((i * st, max(4, min(F - i * st, 14)) if lastone else st, (top if lastone else art) + x))
        ev += tex(0, 1)
    elif shape == "fall":
        for i, x in enumerate(up[::-1]):
            ev.append((i * st, st, art + x))
        t, octave = len(up) * st + 2, up[0][-1]
        ev += [(t, 4, "!F#" + octave), (t + 5, max(4, min(F - t - 5, 14)), "^C" + octave)]
    elif shape == "heal":
        L = min(F, 80)
        gap = max(st * 2, L // (len(up) + 2))
        for i, x in enumerate(up):
            ev.append((i * gap, gap, x))
        t = len(up) * gap
        ev += [(t, max(4, L - t), "~" + up[-1])] + ([(0, 1, "x=84")] if pal["tex"] else [])
    elif shape == "status":
        L = min(F, 30)
        t, k = 0, 0
        while t < L - st:
            ev.append((t, st, art + m[k % 2]))
            t, k = t + st, k + 1
        ev += tex(0, L) if pal["tex"] == "s" else tex(0, 2)
    elif shape == "call":
        L = min(F, 150)
        seq = [m[0], m[2], m[1], m[3 % len(m)], m[0]]
        gap = max(st * 2, L // len(seq))
        for i, x in enumerate(seq):
            lastone = i == len(seq) - 1
            ev.append((i * gap, max(4, L - i * gap) if lastone else gap, (top if lastone else art) + x))
    elif shape == "charge":
        L = min(F, 60)
        t, gap = 0, max(4, st * 3)
        while t < L - 12:
            ev += [(t, max(1, min(gap - 1, 3)), "^" + m[0])] + tex(t, 1)
            t, gap = t + gap, max(2, gap - 1)
        ev += [(t, max(4, L - t), top + up[-1])]
    elif shape == "bind":
        L = min(F, 40)
        gap = max(5, L // 3)
        for i in range(3):
            if i * gap < L:
                ev += thud(i * gap, 3) + [(i * gap, 3, note(i % 2))]
    elif shape == "tick":
        ev += [(0, 1, "x=84"), (0, 2, "^" + m[2]), (3, 3, "^" + m[1])]
    elif shape == "swish":
        L = min(F, 30)
        ev += [(0, L, "s=72")]
        for i, x in enumerate(up + up[-2::-1]):
            ev.append((i * 2, 2, "^" + x))
    elif shape == "pop":
        ev += [(0, 1, "x=82"), (0, 2, note(1)), (3, max(3, min(F - 3, 8)), note(2))]
    elif shape == "glint":
        hi = up[::-1]
        ev += [(0, 2, "^" + hi[0]), (3, 2, "^" + hi[1 % len(hi)]), (6, max(3, min(F - 6, 12)), top.replace("!", "^") + hi[0])]
        ev += tex(0, 2) if pal["tex"] == "s" else []
    else:
        raise ValueError(shape)
    return ev


def serialise(events, F):
    """Events -> the token language: each clamped to end by frame F, "&" for a shared start, "&r:n" to step back."""
    evs = sorted(((at, min(n, F - at), tok) for at, n, tok in events if at < F and n >= 1),
                 key=lambda e: (e[0], 0 if e[2][0] in "xsX" else 1))
    out, at, last, first = [], 0, 0, True
    for t, n, tok in evs:
        if not first and t == last:
            out.append("&%s:%d" % (tok, n))
        elif t >= at:
            if t > at:
                out.append("r:%d" % (t - at))
            out.append("%s:%d" % (tok, n))
        else:
            out.append("&r:%d" % (t - last))
            out.append("%s:%d" % (tok, n))
        last, at, first = t, t + n, False
    return " ".join(out)


def build_10():
    """SOUNDS_10 from TABLE_10, each fitted to pret's own length (read from its MIDI)."""
    out = []
    for sid, ty, shape in TABLE_10:
        lp = LOOP_10.get(sid)
        F = lp[1] if lp else frames_of(pret_midi(sid))
        d = dict(id=sid, type=ty, shape=shape, notes=serialise(shape_events(PALETTE[ty], shape, F, sid), F),
                 what="%s, %s" % (ty, SHAPE_WHAT[shape]))
        if lp:
            d["loop"] = lp
        out.append(d)
    return out


def census10():
    """({sound: [(routine, type)]}, {sound: [status or general animation]}) -- which routines' animations play each
    SE_M_*, followed through calls, gotos and the C tasks and sprite templates they start. Read from the engine."""
    s = open(os.path.join(GBA, "data", "battle_anim_scripts.s")).read()
    labels, cur = {}, None
    for l in s.split("\n"):
        m = re.match(r"^(\w+):{1,2}\s*$", l)
        if m:
            if cur is not None and not labels[cur]:
                labels[cur] = ["\tgoto " + m.group(1)]       # two labels on one body
            cur = m.group(1)
            labels[cur] = []
        elif cur:
            labels[cur].append(l)
    src = ""
    for f in sorted(os.listdir(os.path.join(GBA, "src"))):
        if f.startswith("battle_anim") or f == "battle_bg.c":
            src += open(os.path.join(GBA, "src", f)).read() + "\n"
    funcs = {m.group(1): m.group(2) for m in re.finditer(
        r"^(?:static )?(?:void|u8|bool8|s16|u16|bool32|s32) (\w+)\([^;]*?\)\n\{(.*?)^\}", src, re.M | re.S)}
    fsnd = {k: set(re.findall(r"\bSE_M_\w+", v)) for k, v in funcs.items()}
    for _ in range(3):
        for k, v in funcs.items():
            for w in set(re.findall(r"\b(\w+)\b", v)):
                if w in fsnd and w != k:
                    fsnd[k] |= fsnd[w]
    csnd = {k: v for k, v in fsnd.items() if v}
    for m in re.finditer(r"(g\w+)\s*=\s*\{(.*?)\};", src, re.S):
        cb = re.search(r"\.callback\s*=\s*(\w+)", m.group(2))
        if cb and fsnd.get(cb.group(1)):
            csnd[m.group(1)] = fsnd[cb.group(1)]

    def refs(lab, seen):
        if lab in seen or lab not in labels:
            return set()
        seen.add(lab)
        out = set()
        for l in labels[lab]:
            l = l.split("@")[0]
            out |= set(re.findall(r"\bSE_M_\w+", l))
            out |= {"ROLE_" + r for r in re.findall(r"\bplaytypesewithpan\s+TYPE_SE_(\w+)", l)}   # T-583
            for w in set(re.findall(r"\b\w+\b", l)):
                if w in labels and w != lab:
                    out |= refs(w, seen)
                out |= csnd.get(w, set())
        return out
    body = open(os.path.join(GBA, "src/data/battle_moves.h")).read()
    mtype = {mv: re.search(r"\.type = TYPE_(\w+)", b).group(1)
             for mv, b in re.findall(r"\[MOVE_(\w+)\]\s*=\s*\{(.*?)\n    \}", body, re.S)}
    ids = {}                                       # an alias (MOVE_WITCHING_FIRST) gives way to the routine's own name
    for m in re.finditer(r"#define MOVE_(\w+)\s+(\d+)\b", open(os.path.join(GBA, "include/constants/moves.h")).read()):
        k = int(m.group(2))
        if k not in ids or (ids[k] not in mtype and m.group(1) in mtype):
            ids[k] = m.group(1)
    table = re.findall(r"\.4byte (\w+)", re.search(r"gBattleAnims_Moves::\n(.*?)\n\n", s, re.S).group(1))
    by, other = {}, {}
    roles = role_sounds_10() if "playtypesewithpan" in s else {}

    def sid(x, ty):
        """SE_M_X -> m_x; a role (T-583) -> the sound the routine's type plays for it (CONTENT's outside a routine)."""
        if x.startswith("ROLE_"):
            row = roles[x[5:]]
            return row.get(ty, row["CONTENT"])[0]
        return x[3:].lower()
    for i, lab in enumerate(table):
        mv = ids.get(i)
        if not mv or mv == "NONE" or mv not in mtype:
            continue
        ty = TYPE_OF_VANILLA.get(mtype[mv], mtype[mv])
        for x in refs(lab, set()):
            by.setdefault(sid(x, ty), []).append((mv, ty))
    for sec in ("gBattleAnims_StatusConditions", "gBattleAnims_General", "gBattleAnims_Special"):
        for lab in re.findall(r"\.4byte (\w+)", re.search(sec + r"::\n(.*?)\n\n", s, re.S).group(1)):
            for x in refs(lab, set()):
                other.setdefault(sid(x, None), []).append(lab)
    return by, other


def dominant(rows):
    """The type whose routines borrow a sound most; a tie to the one that is not CONTENT, then to the chart's order."""
    count = {}
    for _, t in rows:
        if t in CHART:
            count[t] = count.get(t, 0) + 1
    if not count:
        return None
    best = [t for t in CHART if count.get(t) == max(count.values())]
    return ([t for t in best if t != "CONTENT"] or best)[0]


def census10_drift():
    """Lines where TABLE_10's type is not what the engine's animations make it now, or a battle sound is missing."""
    by, other = census10()
    bad = []
    for sid, ty, _ in TABLE_10:
        want = OVERRIDE_10[sid][0] if sid in OVERRIDE_10 else dominant(by.get(sid, []))
        if want != ty:
            bad.append("%s is %s in TABLE_10, %s by the census" % (sid, ty, want))
    left = {"m_heal_bell", "m_morning_sun"}
    for sid in sorted(set(by) | set(other)):
        if sid not in {t[0] for t in TABLE_10} and sid not in left:
            bad.append("%s plays in battle and is in no batch" % sid)
    return bad


def players_10():
    t = open(os.path.join(GBA, "sound", "song_table.inc")).read()
    return {sid: int(m.group(1)) for sid, _, _ in TABLE_10
            for m in [re.search(r"^\s*song se_%s,\s*(\d+)," % re.escape(sid), t, re.M)] if m and m.group(1) != "1"}


APPROVED_10 = {}                                   # the user's picks for batch 10; --write refuses while it is empty
APPROVED_10.update({sid: "C" for sid, _, _ in TABLE_10})   # the user, 2026-11-17, by multiple choice: C BOTH (DRAFT)
# The "a battle's moves" clip: twelve routines of twelve types, one after another, as a battle plays them.
SESSION_10 = [(0.00, "m_comet_punch"), (0.85, "m_vital_throw2"), (1.75, "m_wing_attack"), (2.65, "m_toxic"),
              (3.45, "m_earthquake", 4.90), (4.95, "m_rock_throw"), (5.90, "m_flamethrower", 7.20),
              (7.30, "m_surf", 8.60), (8.70, "m_thunderbolt"), (9.60, "m_psybeam"), (10.60, "m_icy_wind"),
              (11.30, "m_bite")]
LABELS_10 = {"m_comet_punch": "CONTENT  a hit (TACKLE, POUND, SLAM...)", "m_vital_throw2": "LOGIC    strikes "
             "(DOUBLE KICK, LOW KICK...)", "m_wing_attack": "VECTOR   strikes (WING ATTACK)",
             "m_toxic": "CORRUPT  a status (TOXIC)", "m_earthquake": "STRATUM  a wave (EARTHQUAKE, FISSURE)",
             "m_rock_throw": "LEGACY   strikes (ROCK THROW, ROCK SLIDE)", "m_flamethrower": "ENTROPY  a beam "
             "(FLAMETHROWER)", "m_surf": "FLOW     a wave (SURF)", "m_thunderbolt": "SIGNAL   a beam (THUNDERBOLT)",
             "m_psybeam": "CONTEXT  a beam (PSYBEAM, FUTURE SIGHT...)", "m_icy_wind": "FROZEN   an edge (ICY WIND, "
             "SHEER COLD)", "m_bite": "OPAQUE   jaws (BITE, CRUNCH)"}
PALETTE_CLIP = [(i * 1.0, SIGNATURE_10[t], i * 1.0 + 0.95) for i, t in enumerate(CHART)]


def use_batch(n):
    """Point the module at batch n's sounds, picks, drafts folder and clip."""
    global SOUNDS, APPROVED, LEFT_OUT, SESSION, PLAYER, DRAFTS, BATCH, LABEL, CLIP
    if n == 4:
        SOUNDS, APPROVED, LEFT_OUT, SESSION, PLAYER = SOUNDS_4, APPROVED_4, LEFT_OUT_4, SESSION_4, PLAYER_4
        DRAFTS = os.path.join(ROOT, "audio", "drafts", "t565_battle")
        BATCH, LABEL, CLIP = 4, "T-565 batch 4", "battle_moment"
    elif n == 6:
        SOUNDS, APPROVED, LEFT_OUT, SESSION, PLAYER = SOUNDS_6, APPROVED_6, LEFT_OUT_6, SESSION_6, PLAYER_6
        DRAFTS = os.path.join(ROOT, "audio", "drafts", "t565_field")
        BATCH, LABEL, CLIP = 6, "T-565 batch 6", "a_walk"
        bad = [s["id"] for s in SOUNDS if s.get("sketch") and s["id"] in APPROVED]
        if bad:
            sys.exit("genuisounds: %s are batch 10's sketches (shared with battle), never written here" % bad)
    elif n == 10:
        SOUNDS, APPROVED, LEFT_OUT, SESSION, PLAYER = build_10(), APPROVED_10, LEFT_OUT_10, SESSION_10, players_10()
        DRAFTS = os.path.join(ROOT, "audio", "drafts", "t565_moves")
        BATCH, LABEL, CLIP = 10, "T-565 batch 10", "a_battles_moves"
    elif n != 1:
        sys.exit("genuisounds: --batch is 1 (menus), 4 (battle), 6 (field) or 10 (the moves)")

# velocity by kind and style; C's square layer is quieter than A's
VEL = {"n": 100, "h": 92, "b": 110, "t": 72, "x": 90, "s": 64, "X": 110}
C_SQUARE = 0.9
C_SAMPLE = 0.6

NOISE_RE = re.compile(r"^([xsX])(?:=(\d+))?$")
NOTE_RE = re.compile(r"^([~!^]?)([A-G]#?)(-?\d)$")
SEMI = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}


def tokens(score):
    """[(frame, frames, kind, key)] -- kind n h b t x s X. A token starting "&" starts with the one before it."""
    out, at, last = [], 0, 0
    for tok in score.split():
        what, frames = tok.rsplit(":", 1)
        frames = int(frames)
        if what.startswith("&"):
            what, at = what[1:], last
        last = at
        if what == "r":
            pass
        elif NOISE_RE.match(what):
            m = NOISE_RE.match(what)
            out.append((at, frames, m.group(1), int(m.group(2)) if m.group(2) else NOISE_KEY[m.group(1)]))
        else:
            m = NOTE_RE.match(what)
            assert m, "bad token %r" % tok
            kind = {"": "n", "~": "h", "!": "b", "^": "t"}[m.group(1)]
            out.append((at, frames, kind, 12 * (int(m.group(3)) + 1) + SEMI[m.group(2)]))
        at += frames
    return out


def voiced(snd, style):
    """[(frame, frames, channel, program, key, velocity)] -- the style's notes, before any loudness scaling.
    A "mono" sound (a one-track player, SE3) leaves C's square and noise out: the harp and flute alone. A "merge"
    sound (batch 6's weather, also SE3) keeps every layer and puts them all on the one track."""
    a = tokens(snd.get("a", snd["notes"]))
    b = tokens(snd.get("b", snd["notes"]))
    out, square_at = [], set()
    merge = snd.get("mono") == "merge"
    if style == "A" or (style == "C" and (merge or not snd.get("mono"))):
        k = 1.0 if style == "A" else C_SQUARE
        for at, n, kind, key in a:
            if kind in ("x", "s", "X"):
                out.append((at, n, CH_NOISE, SHIMMER if kind == "s" else TICK, key, VEL[kind] * k))
                continue
            if at in square_at:                       # one square 1: a chord's other notes are the harp's
                continue
            square_at.add(at)
            if kind == "b":
                out.append((at, n, CH_SQUARE, BUZZ, key, VEL["b"] * k))
            elif style == "A":
                out.append((at, n, CH_SQUARE, THIN if kind == "t" else KEY, key + 12, VEL[kind]))
            else:
                out.append((at, min(n, 2), CH_SQUARE, THIN if kind == "t" else CLICK, key + 12, VEL[kind] * k))
    if style in ("B", "C"):
        k = 1.0 if style == "B" else C_SAMPLE
        for at, n, kind, key in b:
            if kind in ("x", "s", "X"):
                continue
            prog = FLUTE if (style == "C" and kind == "h") else HARP
            out.append((at, n, CH_SAMPLE, prog, key + 12 if kind == "b" else key, VEL[kind] * k))
    if merge:
        out = [(at, n, CH_SAMPLE, p, key, v) for at, n, ch, p, key, v in out]
    return out


def loop_span(snd):
    """(start, end) in frames of a sound's loop, or None. An int loop starts at 0 (SE_LOW_HEALTH)."""
    lp = snd.get("loop")
    if lp is None:
        return None
    return (0, lp) if isinstance(lp, int) else tuple(lp)


def vlq(n):
    out = [n & 0x7F]
    n >>= 7
    while n:
        out.insert(0, (n & 0x7F) | 0x80)
        n >>= 7
    return bytes(out)


def to_midi(notes, scale=1.0, loop=None, merge=False):
    """Format 0, one track, a channel per hardware voice; the program set before each note that changes it (with
    `merge`, just before it, so two voices can start on the one channel on one frame). With `loop` (frames, or (start, end)),
    mid2agb's loop markers "[" and "]", as pret's SE_LOW_HEALTH and SE_RAIN have."""
    ev = [(0, 0, b"\xFF\x51\x03" + struct.pack(">I", TEMPO_US)[1:])]
    if loop:
        start, end = (0, loop) if isinstance(loop, int) else loop
        ev += [(start, 0, b"\xFF\x06\x01["), (end, 4, b"\xFF\x06\x01]")]
    for ch in sorted({n[2] for n in notes}):
        ev.append((0, 1, bytes((0xB0 | ch, 7, 127))))
    prog = {}
    for at, n, ch, p, key, vel in sorted(notes):
        if prog.get(ch) != p:
            ev.append((at, 3 if merge else 2, bytes((0xC0 | ch, p))))
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
    order = {"prog": 2, "cc": 0, "bend": 0, "off": 1, "on": 2}    # a program change keeps its place among the notes
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


_KEYSPLIT = {}


def keysplit(voice, key):
    """A voice_keysplit's voice for this key (pret's SE_CONTEST_PLACE plays one): voicegroupNNN, KeySplitTableN."""
    m = re.match(r"voice_keysplit\s+voicegroup(\d+),\s*(\w+)", voice.strip())
    if not m:
        return voice
    table = m.group(2)
    if table not in _KEYSPLIT:
        t = git_show("sound/keysplit_tables.inc")
        rows = (t.decode() if t else open(os.path.join(GBA, "sound", "keysplit_tables.inc")).read()).split("\n")
        i = next(k for k, r in enumerate(rows) if r.startswith(".set %s," % table))
        first, out = int(re.search(r"- (\d+)", rows[i]).group(1)), {}
        for r in rows[i + 1:]:
            b = re.match(r"\s*\.byte\s+(\d+)", r)
            if not b:
                break
            out[first + len(out)] = int(b.group(1))
        _KEYSPLIT[table] = out
    split = _KEYSPLIT[table]
    k = min(max(int(key), min(split)), max(split))
    return voicegroup(int(m.group(1)))[split[k]]


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
        y = render_note(keysplit(voices[p], key), key, v / 127 * vl / 127 * master / 127, dt * spt)
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
            peak = np.abs(render(midi_of(snd, notes, scale), our_voices(), master)).max()
            if peak <= pret_peak * 1.0001:
                break
            scale *= min(0.97, pret_peak / peak)
    return midi_of(snd, notes, scale), scale


def midi_of(snd, notes, scale=1.0):
    return to_midi(notes, scale, snd.get("loop"), snd.get("mono") == "merge")


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


def check_tracks():
    """Every style's channels fit its player's tracks (a MIDI channel is a track to mid2agb)."""
    bad = []
    for snd in SOUNDS:
        cap = TRACKS[PLAYER.get(snd["id"], 1)]
        for st in STYLES:
            n = len({v[2] for v in voiced(snd, st)})
            if n > cap:
                bad.append("%s %s: %d tracks, SE%d holds %d" % (snd["id"], st, n, PLAYER.get(snd["id"], 1), cap))
    return bad


def write_wav_or_mp3(path_noext, y):
    import numpy as np
    y = np.clip(y, -1, 1)
    os.makedirs(os.path.dirname(path_noext), exist_ok=True)
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


def heard(name, y):
    """A sound as its own preview: a looping one three times round (its loop's length each), then a short silence."""
    import numpy as np
    snd = next(s for s in SOUNDS if s["id"] == name)
    span = loop_span(snd)
    if span:
        a, b = int(span[0] / 60 * SR), int(span[1] / 60 * SR)
        y = np.concatenate([y, np.zeros(max(0, b - len(y)))])
        y = np.concatenate([y[:a], np.tile(y[a:b], 3)])
    return np.concatenate([y, np.zeros(SR // 8)])


def session_mix(get, rows=None):
    """The clip: each sound placed at its time; a sound cuts the one before it on the same player, a third field
    stops it there (SE_EXP when the bar is full), and a sound with a loop repeats its loop until then."""
    import numpy as np
    rows = SESSION if rows is None else rows
    clips = []
    for row in rows:
        t, name = row[0], row[1]
        stop = row[2] if len(row) > 2 else None
        y = get(name)
        snd = next(s for s in SOUNDS if s["id"] == name)
        span = loop_span(snd)
        if span and stop is not None:
            a, b = int(span[0] / 60 * SR), int(span[1] / 60 * SR)
            y = np.concatenate([y, np.zeros(max(0, b - len(y)))])
            y = np.concatenate([y[:a], np.tile(y[a:b], int(math.ceil((stop - t) * SR / (b - a))) + 1)])
        if stop is not None:
            y = y[:int((stop - t) * SR)]
        clips.append((int(t * SR), PLAYER.get(name, 1), y))
    total = max(i + len(y) for i, _, y in clips) + SR // 4
    mix = np.zeros(total)
    for k, (i, player, y) in enumerate(clips):
        nxt = next((j for j, p, _ in clips[k + 1:] if p == player), None)
        y = y.copy()
        cut = len(rows[k]) > 2
        if nxt is not None and i + len(y) > nxt:
            y, cut = y[:nxt - i], True
        fade = min(len(y), int(0.004 * SR))
        if cut and fade:
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
            written.append(write_wav_or_mp3(os.path.join(d, sketch_name(snd)), heard(snd["id"], y)))
        written.insert(0, write_wav_or_mp3(os.path.join(outdir, "%s_%s_%s" % (CLIP, st, STYLE_NAMES[st].replace(" ", "_"))),
                                           session_mix(lambda n: cache[n])))
        if BATCH == 10 and st == "C":
            written.insert(1, write_wav_or_mp3(os.path.join(outdir, "the_palette_C_BOTH"),
                                               session_mix(lambda n: cache[n], PALETTE_CLIP)))
    if BATCH == 10:
        write_sidecars(outdir)
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
        write_wav_or_mp3(os.path.join(outdir, "se_%s" % name), heard(name, y))
    write_wav_or_mp3(os.path.join(outdir, "%s_pret" % CLIP), session_mix(lambda n: cache[n]))
    if BATCH == 10:
        write_wav_or_mp3(os.path.join(outdir, "the_palette_pret"), session_mix(lambda n: cache[n], PALETTE_CLIP))
        write_sidecars(outdir)
    print("  pret's reference: %d sounds and the clip in %s (retail audio: keep it out of git)" % (len(cache), outdir))


def write_sidecars(outdir):
    """Batch 10: what is heard when in the two clips -- the battle's moves (CLIP.txt) and the palette (TYPES.txt)."""
    rows = ["# %s -- the same moves in every style, and in pret's (tools/genuisounds.py --batch 10)" % CLIP]
    rows += ["%5.2fs  se_%-16s %s" % (r[0], r[1], LABELS_10[r[1]]) for r in SESSION_10]
    open(os.path.join(outdir, CLIP + ".txt"), "w").write("\n".join(rows) + "\n")
    rows = ["# the_palette -- each type's signature sound, one a second, in the chart's order (C BOTH, and pret's)"]
    rows += ["%5.2fs  %-9s se_%-16s %s" % (r[0], t, r[1], PALETTE[t]["line"]) for t, r in zip(CHART, PALETTE_CLIP)]
    open(os.path.join(outdir, "TYPES.txt"), "w").write("\n".join(rows) + "\n")


def sketch_name(snd):
    """A draft's file name in a style folder: batch 10's sketches go in batch10_sketch/, out of --write's way."""
    return ("batch10_sketch/se_%s" if snd.get("sketch") else "se_%s") % snd["id"]


def draft(outdir):
    drafts = all_drafts()
    for st in STYLES:
        d = os.path.join(outdir, st)
        os.makedirs(d, exist_ok=True)
        for snd in SOUNDS:
            path = os.path.join(d, sketch_name(snd) + ".mid")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            open(path, "wb").write(drafts[(snd["id"], st)][0])
    open(os.path.join(outdir, "voicegroup%03d.inc" % VOICEGROUP), "w").write(MARK_VG + "\n" + "\n".join(VOICES) + "\n")
    rows = ["# %s drafts (tools/genuisounds.py %s--draft): style, sound, pret's frames, ours, velocity scale" % (LABEL, "--batch %d " % BATCH if BATCH != 1 else ""),
            "# A %s / B %s / C %s" % tuple(STYLE_NAMES[s] for s in STYLES)]
    for snd in SOUNDS:
        pret = frames_of(pret_midi(snd["id"]))
        rows.append("%-14s pret %2d  " % (snd["id"] + (" (SKETCH, batch 10)" if snd.get("sketch") else ""), pret) + "  ".join(
            "%s %2d x%.2f" % (st, frames_of(drafts[(snd["id"], st)][0]), drafts[(snd["id"], st)][1]) for st in STYLES))
    open(os.path.join(outdir, "LENGTHS.txt"), "w").write("\n".join(rows) + "\n")
    if BATCH == 10:
        by, other = census10()
        rows = ["# %s: each sound, the type it is drawn from, its shape, and what plays it in battle (census10())"
                % LABEL]
        for ty in CHART:
            mine = [s for s in SOUNDS if s["type"] == ty]
            rows += ["", "%s (%d) -- %s" % (ty, len(mine), PALETTE[ty]["line"])]
            for snd in mine:
                plays = sorted("%s/%s" % (mv, t) for mv, t in by.get(snd["id"], []))
                gen = sorted(set(other.get(snd["id"], [])))
                why = OVERRIDE_10.get(snd["id"], ("", ""))[1]
                rows.append("  se_%-17s %-8s %s%s%s" % (snd["id"], snd["shape"], ", ".join(plays),
                            ("; " if plays and gen else "") + ", ".join(gen), ("  [%s]" % why) if why else ""))
        rows += ["", "LEFT OUT: " + "; ".join(LEFT_OUT)]
        open(os.path.join(outdir, "MOVES.txt"), "w").write("\n".join(rows) + "\n")
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

    if "--batch" in args:
        use_batch(int(arg_after("--batch", "1")))
    bad = check_lengths() + check_tracks()
    if bad:
        sys.exit("genuisounds: longer than pret's, or more tracks than its player: " + "; ".join(bad))
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
            print("genuisounds (%s): APPROVED is empty -- nothing is written until the user picks" % LABEL)
            return 0
        for path, want in engine_target().items():
            mode = "wb" if isinstance(want, bytes) else "w"
            have = open(path, "rb" if mode == "wb" else "r").read() if os.path.exists(path) else None
            if have != want:
                open(path, mode).write(want)
                print("  wrote %s" % os.path.relpath(path, ROOT))
        return 0
    # report
    print("genuisounds (%s): %d sounds in three styles; left out: %s" % (LABEL, len(SOUNDS), "; ".join(LEFT_OUT)))
    for snd in SOUNDS:
        pret = frames_of(pret_midi(snd["id"]))
        ours = [frames_of(to_midi(voiced(snd, st))) for st in STYLES]
        print("    se_%-14s pret %2d frames (%.3fs)   A %2d  B %2d  C %2d   %s"
              % (snd["id"], pret, pret / 60, ours[0], ours[1], ours[2], APPROVED.get(snd["id"], "")))
    if BATCH == 10:
        drift = census10_drift()
        print("  census: %s" % ("; ".join(drift) if drift else "every type is the one the battle animations give it"))
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
