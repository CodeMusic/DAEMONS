#!/usr/bin/env python3
"""T-565 batch 13 (T-593): pret's last music -- ours, in place of pret's fourteen.

    python3 tools/genrestmusic.py            # report: is the engine current
    python3 tools/genrestmusic.py --write    # write it into engineGba

THE VOICE (the user, 2026-11-18, from one reel of fourteen drafts in voice C: "All fourteen"). genfanfares.py's
voicegroup195, as every batch of ours: the HARP and FLUTE on the tunes, the cartridge under them. Six of these a player
hears in this build (the GAME CORNERs, the photo, SUSPEND's song, the UPTIME dance, the walk to the ferry, the STREAM's
menu); the other eight nothing in the build reaches (the slot jingles, TOO_BAD, OBTAIN_ITEM, the STREAM's show, the
UNION ROOM and the two link battles), written so that pret's music is left only where an event ticket or nothing
at all reaches (docs/sound-census-2026-11-16.md). The four in the fanfare
table (src/sound.c) each end inside the frames the engine waits for them. The link battles are genbattlemusic.py's
trainer and leader battles with the harp's and the flute's lines exchanged.

WHAT IT WRITES (engineGba/)
    sound/songs/midi/<slot>.mid      fourteen over pret's in place (no map moves, no new song)
    sound/songs/midi/midi.cfg        each one's -G to 195
Each piece's reason is its "why" below. Every note DRAFT.
"""
import copy, os, re, sys

import genbattlemusic as GB
import genfanfares as G
import genoverworldmusic as GO
import genstorymusic as GS

pattern, arp, fb, shift = GO.pattern, GO.arp, GO.fb, GO.shift
S, join, rest, rep, cat, dia = GB.S, GB.join, GB.rest, GB.rep, GB.cat, GB.dia
GBA, MIDI_DIR, CFG, VOICEGROUP = G.GBA, G.MIDI_DIR, G.CFG, G.VOICEGROUP
FILES = {"GAME_CORNER": "mus_game_corner", "SLOTS_WIN": "mus_slots_win", "SLOTS_JACKPOT": "mus_slots_jackpot",
         "TOO_BAD": "mus_too_bad", "PHOTO": "mus_photo", "JIGGLYPUFF": "mus_jigglypuff", "SCHOOL": "mus_school",
         "FOLLOW_ME": "mus_follow_me", "TEACHY_TV_MENU": "mus_teachy_tv_menu", "TEACHY_TV_SHOW": "mus_teachy_tv_show",
         "OBTAIN_ITEM": "mus_obtain_item", "UNION_ROOM": "mus_union_room", "RS_VS_TRAINER": "mus_rs_vs_trainer",
         "RS_VS_GYM_LEADER": "mus_rs_vs_gym_leader"}

# ---------------------------------------------------------------------------------------------------------------------
# THE PIECES (carried verbatim from the drafts the user heard)
# ---------------------------------------------------------------------------------------------------------------------

PIECES = []

def chords(chs, beats=4):
    return [(c, beats) for c in chs]

# ---- 1-4. THE GAME CORNER: VERDIGRIS and TWO ISLAND, in VERDIGRIS's F# (7.4) ----------------------------------------
_REEL_A = "F#4:0.5 A#4:0.5 C#5:0.5 A#4:0.5 F#4:0.5 C#4:0.5"            # 3 beats
_REEL_B = "C#5:1 D#5:0.5 C#5:0.5 A#4:1 F#4:1"                          # 4 beats
_REEL_C = "F#5:0.5 G#5:0.5 A#5:0.5 G#5:0.5 F#5:1 D#5:1 C#5:1"          # 5 beats
PIECES.append(dict(
    id="GAME_CORNER", slot="MUS_GAME_CORNER", bpm=138, meter=4, heard=True,
    what="the two GAME CORNERs, VERDIGRIS's and TWO ISLAND's",
    why="Three reels (3.9): the harp turns a figure three beats long, the flute one of four, the square one of five, "
        "all in VERDIGRIS's F#. They pass each other all the time and only line up -- all three starting together -- "
        "once every sixty beats, which is the loop.",
    intro=[],
    loop=join(S("reels", 60, lead=rep(_REEL_A, 20), sing=rep(_REEL_B, 15), arp=rep(_REEL_C, 12),
                bass=rep("F#2:1 C#3:1 F#3:1 C#3:1", 15), perc=rep(GB.LIGHT, 15))),
))
PIECES.append(dict(
    id="SLOTS_WIN", slot="MUS_SLOTS_WIN", bpm=138, meter=4, jingle=True, heard=False,
    what="a line pays at the slots (only in the fanfare table: nothing plays it)",
    why="The three reels' first notes, struck together -- a line that pays is the three in step -- then up.",
    intro=join(S("win", 4, lead="F#4:0.5 C#5:0.5 F#5:3", sing="F#5:0.5 A#5:0.5 C#6:3",
                 arp="C#5:0.5 F#5:0.5 A#5:3", bass="F#2:1 C#3:1 F#2:2", perc="s:0.5 s:0.5 c:3")),
    loop=[],
))
PIECES.append(dict(
    id="SLOTS_JACKPOT", slot="MUS_SLOTS_JACKPOT", bpm=138, meter=4, jingle=True, heard=False,
    what="the slots' jackpot (only in the fanfare table: nothing plays it)",
    why="The jackpot is the moment the sixty beats come round: all three reels' figures played at once, from their "
        "first notes, then the three in one rhythm two octaves up to F#.",
    intro=join(S("jackpot", 9, lead=cat(_REEL_A, "C#5:0.5 F#5:0.5 A#5:0.5 C#6:0.5 F#6:4"),
                 sing=cat(_REEL_B, "A#5:0.5 C#6:0.5 F#6:4"),
                 arp=cat(_REEL_C, "C#5:0.5 F#5:0.5 A#5:3"),
                 bass="F#2:1 C#3:1 F#3:1 C#3:1 F#2:1 C#3:1 F#2:3",
                 perc="k:1 h:1 s:1 h:1 k:1 s:0.5 s:0.5 c:3")),
    loop=[],
))
PIECES.append(dict(
    id="TOO_BAD", slot="MUS_TOO_BAD", bpm=138, meter=4, jingle=True, heard=False,
    what="a game lost (the wireless games only: nothing in this build reaches it)",
    why="The near miss: two reels stop on F#, the third one short of it, on F.",
    intro=join(S("too bad", 4, sing="F#5:1 F#5:1 F5:2", lead="F#4:1 A#4:1 A4:2", bass="F#2:2 D2:2", perc="s:1 s:1 c:2")),
    loop=[],
))

# ---- 5. PHOTO: the GAME CORNER's camera, for the TRAINER CARD -----------------------------------------------------------
PIECES.append(dict(
    id="PHOTO", slot="MUS_PHOTO", bpm=138, meter=4, jingle=True, heard=True,
    what="the photograph taken for the TRAINER CARD, upstairs in VERDIGRIS's GAME CORNER",
    why="A photograph is one instant: one chord of VERDIGRIS's F#, struck once, and the snare as the shutter.",
    intro=join(S("photo", 2, lead="F#4+A#4+C#5:2", sing="F#5:2", bass="F#2:2", perc="s:0.25 r:0.25 c:1.5")),
    loop=[],
))

# ---- 6. JIGGLYPUFF: SUSPEND sings in SLATE's CHECKPOINT ---------------------------------------------------------------
PIECES.append(dict(
    id="JIGGLYPUFF", slot="MUS_JIGGLYPUFF", bpm=126, meter=4, jingle=True, heard=True,
    what="SUSPEND singing in SLATE's CHECKPOINT (about 7.6 s; the script waits 455 frames)",
    why="SUSPEND is the light sleep state, which keeps what it holds in memory (vision, the species table). It sings "
        "the CHECKPOINT's own refrain (HEAL's lullaby, batch 5), and every phrase loses notes from its end until one "
        "is left, held -- the song suspended, not stopped.",
    intro=join(S("suspend", 16, sing="E5:1 D5:1 C5:2 G4:1 A4:1 C5:1 r:1 E5:1 D5:1 r:2 C5:4",
                 lead="C4:0.5 G4:0.5 E4:0.5 G4:0.5 C4:0.5 G4:0.5 E4:0.5 G4:0.5 F3:1 A3:1 C4:1 A3:1 C4:2 G3:2 C4:4",
                 bass="C3:4 F2:4 C3:4 C3:4")),
    loop=[],
))

# ---- 7. SCHOOL: the UPTIME Dance, in LONG DROP's house -------------------------------------------------------------------
_UP = ("F#5:0.5 F#5:0.5 D#5:0.5 B4:0.5 D#5:1 F#5:1 G#5:0.5 G#5:0.5 E5:0.5 B4:0.5 E5:1 G#5:1 "
       "A#5:0.5 F#5:0.5 C#6:0.5 A#5:0.5 F#5:1 E5:1 C#5:1 A#4:1 F#4:2")
PIECES.append(dict(
    id="SCHOOL", slot="MUS_SCHOOL", bpm=132, meter=4, heard=True,
    what="the UPTIME Dance in the house in LONG DROP, SEVEN ISLAND (both turns)",
    why="UPTIME \"has never stopped\" (its INDEX entry). A dance in the islands' B whose every phrase ends on F#, the "
        "note that wants B: it never cadences, so it has nowhere to stop, and B comes only as the next bar begins it "
        "again.",
    intro=[],
    loop=join(S("uptime", 16, sing=_UP,
                arp=arp(chords(["B3+D#4+F#4", "E4+G#4+B3", "F#3+A#3+C#4", "F#3+A#3+C#4+E4"]), [0, 1, 2, 1], 0.5),
                bass="B2:1 F#2:1 B2:1 F#2:1 E2:1 B2:1 E2:1 B2:1 F#2:1 C#3:1 F#2:1 C#3:1 F#2:1 C#3:1 F#2:1 A#2:1",
                perc=rep(GB.POP, 4))),
))

# ---- 8. FOLLOW_ME: HOLT walks the player from QUICKSILVER's CHECKPOINT to the ferry --------------------------------------
_FM = ("Bb4:1 D5:1 F5:1 D5:1 Eb5:1 G5:1 Bb5:1 G5:1 F5:1 D5:1 Bb4:1 D5:1 C5:1 A4:1 F4:1 A4:1 "
       "D5:1 Bb4:1 G4:1 Bb4:1 C5:1 Eb5:1 G5:1 Eb5:1 D5:1 F5:1 Bb5:1 F5:1 Eb5:1 C5:1 A4:1 C5:1")
_FM_TOK = _FM.split()
PIECES.append(dict(
    id="FOLLOW_ME", slot="MUS_FOLLOW_ME", bpm=120, meter=4, heard=True,
    what="HOLT walking the player from QUICKSILVER's CHECKPOINT to the ferry for ONE ISLAND",
    why="Follow me: the flute leads and the harp follows it note for note, one beat behind and an octave down -- a "
        "canon, the tune built of thirds so that the follower is always in tune with the leader. In the islands' "
        "B-flat, since that is where the walk goes.",
    intro=[],
    loop=join(S("follow", 32, sing=_FM,
                lead=" ".join([shift(_FM_TOK[-1], -12)] + [shift(t, -12) for t in _FM_TOK[:-1]]),
                bass="Bb2:4 Eb2:4 Bb2:4 F2:4 G2:4 C3:4 Bb2:4 F2:4", perc=rep("k:1 h:1 h:1 h:1", 8))),
))

# ---- 9, 10. THE STREAM (TEACHY TV): its menu and its show --------------------------------------------------------------
_TUNE = "E5 D5 C5 G4 A4 C5 E5 D5 C5 A4 F4 A4 B4 D5 G5 F5".split()
_ROOT = ["C4"] * 4 + ["A3"] * 4 + ["F3"] * 4 + ["G3"] * 4
_STREAM = " ".join("%s:0.5 %s:0.5" % (shift(t + ":1", -12).split(":")[0], r) for t, r in zip(_TUNE, _ROOT))
_READ = " ".join("%s:1" % t for t in _TUNE)
_SB = "C3:4 A2:4 F2:4 G2:4"
PIECES.append(dict(
    id="TEACHY_TV_MENU", slot="MUS_TEACHY_TV_MENU", bpm=112, meter=4, heard=True,
    what="the STREAM's menu (the item that was TEACHY TV)",
    why="A stream is data read as it arrives (the STREAM's description): the harp never stops, two notes a beat, and "
        "a tune is carried in it -- the first of every pair. The second time round the flute reads it out.",
    intro=[],
    loop=join(S("arriving", 16, lead=_STREAM, bass=_SB),
              S("read", 16, lead=_STREAM, sing=_READ, bass=_SB)),
))
PIECES.append(dict(
    id="TEACHY_TV_SHOW", slot="MUS_TEACHY_TV_SHOW", bpm=112, meter=4, heard=False,
    what="a STREAM show (nothing in the build plays it; the shows use the menu's)",
    why="The show is the menu's stream with the tune already read out, and drums under it.",
    intro=[],
    loop=join(S("show", 16, lead=_STREAM, sing=_READ, bass=_SB, perc=rep(GB.LIGHT, 4))),
))

# ---- 11. OBTAIN_ITEM -----------------------------------------------------------------------------------------------------
PIECES.append(dict(
    id="OBTAIN_ITEM", slot="MUS_OBTAIN_ITEM", bpm=128, meter=4, jingle=True, heard=False,
    what="an item received from a decoration, MYSTERY GIFT or the e-Reader (none of which this build reaches)",
    why="The plainest receipt there is: a major chord's notes going up and held, harp under flute.",
    intro=join(S("obtain", 4, sing="C5:0.5 E5:0.5 G5:0.5 C6:2.5", lead="C4:0.5 E4:0.5 G4:0.5 C5:2.5",
                 bass="C2:1.5 C3:2.5", perc="r:1.5 c:2.5")),
    loop=[],
))

# ---- 12. UNION_ROOM: a round -------------------------------------------------------------------------------------------
_P1 = "C5:1 E5:1 G5:2 D5:1 F5:1 B4:2"
_P2 = "E5:0.5 E5:0.5 G5:1 C6:2 B4:0.5 D5:0.5 G5:1 F5:2"
_P3 = "C5:2 C5:2 B4:2 G4:2"
PIECES.append(dict(
    id="UNION_ROOM", slot="MUS_UNION_ROOM", bpm=108, meter=4, heard=False,
    what="the UNION ROOM, where two players' games meet (wireless only: this build reaches no UNION ROOM)",
    why="\"Linking up with the usual friends is fun\" (QUICKSILVER's CHECKPOINT): a round, the flute first, the harp "
        "joining eight beats later and the square eight after that, until all three are singing the same tune at "
        "three different places in it.",
    intro=join(S("joining", 16, sing=cat(_P1, _P2), lead=cat(rest(8), shift(_P1, -12)), bass=rep("C2:4 G2:4", 2))),
    loop=join(S("round", 24, sing=cat(_P3, _P1, _P2), lead=shift(cat(_P2, _P3, _P1), -12), arp=cat(_P1, _P2, _P3),
                bass=rep("C2:4 G2:4", 3), perc=rep(GB.LIGHT, 6))),
))

# ---- 13, 14. The link battles: batch 2's, from the other side -------------------------------------------------------------
def _other_side(src_id, new_id, slot, what):
    p = copy.deepcopy(next(q for q in GB.PIECES if q["id"] == src_id))
    sw = {"lead": "sing", "sing": "lead"}
    for part in ("intro", "loop"):
        p[part] = [(sw.get(r, r), tok) for r, tok in p[part]]
    p.update(id=new_id, slot=slot, what=what, heard=False,
             why="A link battle is the same battle seen from the other player's cartridge: batch 2's %s, note for "
                 "note, with the harp's lines given to the flute and the flute's to the harp." % src_id)
    return p
PIECES.append(_other_side("VS_TRAINER", "RS_VS_TRAINER", "MUS_RS_VS_TRAINER",
                          "a link battle against another player (link only: this build reaches none)"))
PIECES.append(_other_side("VS_GYM_LEADER", "RS_VS_GYM_LEADER", "MUS_RS_VS_GYM_LEADER",
                          "a link battle's other music (link only: this build reaches none)"))

# ---------------------------------------------------------------------------------------------------------------------
# The engine: genstorymusic.py's MIDI writer and checks (loops, voicegroup195)
# ---------------------------------------------------------------------------------------------------------------------
def engine():
    """{path: new contents} for every file this writes."""
    out, cfg = {}, open(CFG, encoding="utf-8").read()
    for p in PIECES:
        GS.check(p)
        f = FILES[p["id"]]
        out[os.path.join(MIDI_DIR, f + ".mid")] = GS.song_midi(p)
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
    print("  %d pieces of pret's last music on voicegroup%03d" % (len(PIECES), VOICEGROUP))
    if not changed:
        print("  the game: unchanged")
    else:
        print("  the game: %s %d file(s): %s" % ("wrote" if "--write" in sys.argv else "would write", len(changed),
                                                 ", ".join(changed[:6]) + (" ..." if len(changed) > 6 else "")))


if __name__ == "__main__":
    main()
