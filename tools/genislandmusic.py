#!/usr/bin/env python3
"""T-565 batch 9: the islands, THE MARGINS -- ours, in place of pret's seven.

    python3 tools/genislandmusic.py            # report: is the engine current
    python3 tools/genislandmusic.py --write    # write it into engineGba

THE VOICE (the user, 2026-11-17, from one reel of seven drafts in voice C): "All seven". genfanfares.py's voicegroup195,
as every batch of ours: the HARP and FLUTE on the tunes, the cartridge under them. THE MARGINS lie outside the GAMUT
(vision 0.6), so their towns take the two keys the spectrum leaves without a colour, B-flat and B (7.3: the invented
colour, the one the mind makes -- and the islands are where the mind is the subject). The islands' roads play the
mainland's road (genoverworldmusic.py's ROUTE3) mirrored: the bridge reverses at the ferry (0.6).

WHAT IT WRITES (engineGba/)
    sound/songs/midi/<slot>.mid      seven over pret's in place (no map moves, no new song)
    sound/songs/midi/midi.cfg        each one's -G to 195
Each piece's reason is its "why" below. Every note DRAFT.
"""
import os, re, sys

import genbattlemusic as GB
import genfanfares as G
import genoverworldmusic as GO
import genstorymusic as GS

K = GB
pattern, arp, fb, shift = GO.pattern, GO.arp, GO.fb, GO.shift
S, join, rest, rep, cat, dia = GB.S, GB.join, GB.rest, GB.rep, GB.cat, GB.dia
GBA, MIDI_DIR, CFG, VOICEGROUP = G.GBA, G.MIDI_DIR, G.CFG, G.VOICEGROUP
FILES = {"SEVII_123": "mus_sevii_123", "SEVII_45": "mus_sevii_45", "SEVII_67": "mus_sevii_67",
         "SEVII_ROUTE": "mus_sevii_route", "SEVII_CAVE": "mus_sevii_cave", "SEVII_DUNGEON": "mus_sevii_dungeon",
         "NET_CENTER": "mus_net_center"}

# ---------------------------------------------------------------------------------------------------------------------
# THE PIECES (carried verbatim from the drafts the user heard)
# ---------------------------------------------------------------------------------------------------------------------

PIECES = []

def chords(chs, beats=4):
    return [(c, beats) for c in chs]

def mirror(tokens, scale, axis):
    """a diatonic inversion: every note reflected about `axis` along the seven-note `scale` (pitch-class names)"""
    pcs = sorted(GB.NAMES.index(n) for n in scale.split())
    def deg(m):
        o, pc = divmod(m, 12)
        return o * 7 + pcs.index(pc)
    def note(d):
        o, i = divmod(d, 7)
        return o * 12 + pcs[i]
    a = deg(GB.midi(axis))
    out = []
    for tok in tokens.split():
        w, b = tok.rsplit(":", 1)
        if w == "r" or w in GB.PERC:
            out.append(tok); continue
        out.append("+".join(GB.nn(note(2 * a - deg(GB.midi(n)))) for n in w.split("+")) + ":" + b)
    return " ".join(out)

# ---- 1. SEVII_123: ONE, TWO and THREE ISLAND -------------------------------------------------------------------------
_P = shift("E5:1 C5:1 E5:1 G5:1 A5:2 F5:1 D5:1 C5:1 E5:1 A5:2 B4:2 G4:1 E4:1 "
           "E5:1 G5:1 A5:1 E5:1 F5:2 A5:1 D5:1 G5:1 E5:1 D5:1 B4:1 C5:2 E5:2", -2)
_MAJ = ["Bb3+D4+F4", "Eb4+G4+Bb3", "Bb3+D4+F4", "F3+A3+C4", "Bb3+D4+F4", "Eb4+G4+Bb3", "F3+A3+C4", "Bb3+D4+F4"]
_MIN = ["G3+Bb3+D4", "C4+Eb4+G3", "G3+Bb3+D4", "D4+F4+A3", "G3+Bb3+D4", "C4+Eb4+G3", "D4+F4+A3", "G3+Bb3+D4"]
PIECES.append(dict(
    id="SEVII_123", slot="MUS_SEVII_123", bpm=120, meter=4,
    what="ONE, TWO and THREE ISLAND, their harbours and houses (15 maps)",
    why="THE MARGINS tell how things look from where the speaker is standing (8.2a): the same eight bars twice, the "
        "flute standing in B-flat major, then the harp in G minor -- not one note of the tune changes, only the ground "
        "under it.",
    intro=[],
    loop=join(S("major", 32, sing=_P, arp=arp(chords(_MAJ), [0, 1, 2, 1], 0.5),
                bass=" ".join("%s:2 %s:2" % (GB.nn(GB.midi(c.split("+")[0]) - 12), GB.nn(GB.midi(c.split("+")[0]) - 5)) for c in _MAJ),
                perc=cat(K.LIGHT_C, rep(K.LIGHT, 6), K.FILL_LIGHT)),
              S("minor", 32, lead=_P, arp=arp(chords(_MIN), [0, 1, 2, 1], 0.5),
                bass=" ".join("%s:2 %s:2" % (GB.nn(GB.midi(c.split("+")[0]) - 12), GB.nn(GB.midi(c.split("+")[0]) - 5)) for c in _MIN),
                perc=cat(K.LIGHT_C, rep(K.LIGHT, 6), K.FILL_LIGHT))),
))

# ---- 2. SEVII_45: FOUR and FIVE ISLAND -----------------------------------------------------------------------------------
_PH = {"B": "D#5:0.5 F#5:0.5 B5:1", "E": "G#5:0.5 E5:0.5 B4:1", "G#m": "B4:0.5 D#5:0.5 G#5:1", "F#": "A#5:0.5 F#5:0.5 C#5:1",
       "B2": "F#5:0.5 D#5:0.5 B4:1", "E2": "E5:0.5 G#5:0.5 B5:1", "F#2": "C#6:0.5 A#5:0.5 F#5:1"}
_PAGE1 = ["B", "E", "G#m", "F#", "B2", "E2", "F#2"]
_PAGE2 = ["G#m", "E", "B2", "F#", "G#m", "E2", "F#2"]
def _rev(ph):
    toks = ph.split()
    notes = [t.rsplit(":", 1)[0] for t in toks]
    return "%s:0.5 %s:0.5 %s:1" % (shift(notes[2] + ":1", -12).split(":")[0], shift(notes[1] + ":1", -12).split(":")[0],
                                   shift(notes[0] + ":1", -12).split(":")[0])
_ROOT45 = {"B": "B2", "B2": "B2", "E": "E2", "E2": "E2", "G#m": "G#2", "F#": "F#2", "F#2": "F#2"}
_CH45 = {"B": "B3+D#4+F#4", "B2": "B3+D#4+F#4", "E": "E4+G#4+B3", "E2": "E4+G#4+B3", "G#m": "G#3+B3+D#4",
         "F#": "F#3+A#3+C#4", "F#2": "F#3+A#3+C#4"}
PIECES.append(dict(
    id="SEVII_45", slot="MUS_SEVII_45", bpm=100, meter=4,
    what="FOUR and FIVE ISLAND, their harbours and houses, the Day Care, a resort house (11 maps)",
    why="A margin is also the edge of a printed page (0.6, THE MARGINS): each phrase of the flute is followed by white "
        "space, in B. The second time round the harp writes in the white space -- every phrase answered backwards, an "
        "octave down, a note in the margin.",
    intro=[],
    loop=join(S("page", 32, sing=" ".join("%s r:2" % _PH[c] for c in _PAGE1) + " B5:2 r:2",
                bass=" ".join("%s:4" % _ROOT45[c] for c in _PAGE1) + " B2:4"),
              S("margin", 32, sing=" ".join("%s r:2" % _PH[c] for c in _PAGE2) + " B5:2 r:2",
                lead=" ".join("r:2 %s" % _rev(_PH[c]) for c in _PAGE2) + " r:2 F#4:1 B3:1",
                arp=arp(chords([_CH45[c] for c in _PAGE2] + ["B3+D#4+F#4"]), [0, 1, 2, 1], 0.5),
                bass=" ".join("%s:4" % _ROOT45[c] for c in _PAGE2) + " B2:4", perc=rep("h:2 h:2", 8))),
))

# ---- 3. SEVII_67: SIX and SEVEN ISLAND ------------------------------------------------------------------------------------
_T67 = "F4:1 Bb4:1 C5:1 D5:1 Eb5:2 D5:1 C5:1 D5:1 F5:1 Bb4:2 C5:3 r:1"
_C67 = ["Bb3+D4+F4", "Eb4+G4+Bb3", "G3+Bb3+D4", "F3+A3+C4"]
_cs = lambda c, k: "+".join(GB.nn(GB.midi(n) + k) for n in c.split("+"))
PIECES.append(dict(
    id="SEVII_67", slot="MUS_SEVII_67", bpm=116, meter=4,
    what="SIX and SEVEN ISLAND, their harbours and houses, the canyon house (9 maps)",
    why="The furthest islands, where the two colourless keys meet: each four-bar phrase in B-flat is answered in B, a "
        "semitone higher -- the band at the boundary a classifier's MARGIN names, where the hard cases live (0.6) -- and "
        "the loop steps back down the semitone to begin again.",
    intro=[],
    loop=join(S("67", 64,
        lead=cat(_T67, shift(_T67, 1), arp(chords(_C67), [0, 1, 2, 1, 2, 1, 0, 1], 0.5),
                 arp(chords([_cs(c, 1) for c in _C67]), [0, 1, 2, 1, 2, 1, 0, 1], 0.5)),
        sing=cat(rest(32), shift(_T67, 12), shift(_T67, 13)),
        arp=cat(arp(chords(_C67), [0, 1, 2, 1], 0.5), arp(chords([_cs(c, 1) for c in _C67]), [0, 1, 2, 1], 0.5), rest(32)),
        bass=rep("Bb2:2 F2:2 Eb2:2 Bb2:2 G2:2 D3:2 F2:2 C3:2 B2:2 F#2:2 E2:2 B2:2 G#2:2 D#3:2 F#2:2 C#3:2", 2),
        perc=cat(K.LIGHT_C, rep(K.LIGHT, 6), K.FILL_LIGHT, K.LIGHT_C, rep(K.LIGHT, 6), K.FILL_LIGHT))),
))

# ---- 4. SEVII_ROUTE: the mainland's road, mirrored ---------------------------------------------------------------------------
_R3 = GO.PIECES[0]                                       # ROUTE3 (genoverworldmusic.py's notes)
_R3_LEAD = ("B4:1 D5:0.5 B4:0.5 A4:1 G4:1  E4:1 G4:0.5 A4:0.5 B4:2  C5:1 B4:0.5 A4:0.5 G4:1 E4:1  D4:1 F#4:1 A4:2 "
            "B4:1 D5:0.5 B4:0.5 A4:1 G4:1  E5:1 D5:0.5 B4:0.5 G4:2  A4:1 G4:1 F#4:1 A4:1  G4:4")
assert _R3_LEAD.split() == GO.PIECES[0]["loop"][0][1].split()[:len(_R3_LEAD.split())], "not ROUTE3's own first eight bars"
_R3_SING = "D5:4 B4:4 E5:4 F#5:4 D5:4 G5:4 E5:2 D5:2 B4:4"
_GMAJ = "G A B C D E F#"
_ML = mirror(_R3_LEAD, _GMAJ, "B4")
_MS = mirror(_R3_SING, _GMAJ, "B4")
_MCH = [("G3+B3+D4", 4), ("B3+D4+F#4", 4), ("D4+F#4+A3", 4), ("C4+E4+G3", 4), ("G3+B3+D4", 4), ("B3+D4+F#4", 4),
        ("D4+F#4+A3", 2), ("C4+E4+G3", 2), ("G3+B3+D4", 4)]
_MBASS = "G2:1 D3:1 G3:1 D3:1  B2:1 F#2:1 B2:1 F#2:1  D3:1 A2:1 D3:1 A2:1  C3:1 G2:1 C3:1 G2:1 " \
         "G2:1 D3:1 G3:1 D3:1  B2:1 B2:1 F#2:1 B2:1  D3:1 A2:1 C3:1 G2:1  G2:1 D3:1 G2:2"
def _block(semis):
    return S("mirror %+d" % semis, 32, lead=shift(_ML, semis), sing=shift(_MS, semis),
             arp=shift(arp(_MCH, [0, 1, 2, 1], 0.5), semis), bass=shift(_MBASS, semis),
             perc=cat(K.LIGHT_C, rep(K.LIGHT, 6), K.FILL_LIGHT))
PIECES.append(dict(
    id="SEVII_ROUTE", slot="MUS_SEVII_ROUTE", bpm=124, meter=4,
    what="THE MARGINS' roads, meadows, canyon and ruins outside (18 maps)",
    why="The bridge reverses at the ferry (0.6): the islands' roads play the mainland's main road (ROUTE3, batch 5) "
        "upside down -- the same tune mirrored about its own B, every rise a fall, its chords mirrored with it (G, E "
        "minor, C, D become G, B minor, D, C) -- in the two colourless keys, B-flat and then B.",
    intro=[], loop=join(_block(3), _block(4)),
))

# ---- 5. SEVII_CAVE: the deep ------------------------------------------------------------------------------------------------
_SINK = "F#5 E5 D5 C#5 B4 A4 G4 F#4".split()
_DRIP = "r:1.5 B5:0.5 r:2  r:3 F#6:0.5 r:0.5  r:2.5 D6:0.5 r:1  r:1 C#6:0.5 r:2.5"
PIECES.append(dict(
    id="SEVII_CAVE", slot="MUS_SEVII_CAVE", bpm=84, meter=4,
    what="THE MARGINS' caves -- the LOST CAVE's rooms, the icefall, the canyon tunnels, MT. EMBER's insides (53 maps)",
    why="A continental margin is the zone between the mainland and the deep (0.6), and these are the deep: in B minor, "
        "slow, the flute sinking a step every bar through an octave and climbing back, a held B under everything, and "
        "now and then the harp, high, like water.",
    intro=[],
    loop=join(S("deep", 64, sing=" ".join("%s:4" % n for n in _SINK + _SINK[::-1]), lead=rep(_DRIP, 4),
                harm="B3:16 A3:16 G3:16 F#3:16", bass=rep("B2:8", 8), perc=rep("r:3 h:1", 16))),
))

# ---- 6. SEVII_DUNGEON: TANOBY's chambers (bars of seven) ----------------------------------------------------------------------
_BMIN = "B3 C#4 D4 E4 F#4 G4 A4".split()
def _rot(k):
    return " ".join("%s:1" % _BMIN[(k + i) % 7] for i in range(7))
PIECES.append(dict(
    id="SEVII_DUNGEON", slot="MUS_SEVII_DUNGEON", bpm=120, meter=7,
    what="TANOBY's seven chambers and its key, and the DOTTED HOLE (14 maps)",
    why="The islands are seven, and so are TANOBY's chambers: bars of seven beats, the harp walking the seven notes of B "
        "minor, each bar starting one note further on, so it takes seven bars to come round -- and the flute holds each "
        "bar's first note above it.",
    intro=[],
    loop=join(S("seven", 98, lead=" ".join(_rot(k) for k in range(14)),
                sing=" ".join("%s:7" % GB.nn(GB.midi(_BMIN[k % 7]) + 12) for k in range(14)),
                bass=rep("B2:7", 14), perc=rep("k:1 h:1 s:1 h:1 k:1 s:1 h:1", 13) + " k:1 h:1 s:1 s:1 s:1 s:1 c:1")),
))

# ---- 7. NET_CENTER: ONE ISLAND's CHECKPOINT, CELIO's network ---------------------------------------------------------------
_REF = shift("E5:1 D5:1 C5:2 G4:1 A4:1 C5:2 E5:1 D5:1 C5:1 G4:1 A4:2 B4:2", -2)
def _half(tokens, first):
    out, t = [], 0.0
    for tok in tokens.split():
        w, b = tok.rsplit(":", 1); b = float(b)
        inbar = t % 4
        keep = (inbar < 2) if first else (inbar >= 2)
        out.append(tok if keep else "r:%g" % b)
        t += b
    return " ".join(out)
_NCH = [("Bb3+D4+F4", 4), ("G3+Bb3+D4", 4), ("Bb3+D4+F4", 4), ("Eb4+G4+Bb3", 2), ("F3+A3+C4", 2)]
_NB = "Bb2:2 F2:2 G2:2 D2:2 Bb2:2 F2:2 Eb2:2 F2:2"
PIECES.append(dict(
    id="NET_CENTER", slot="MUS_NET_CENTER", bpm=112, meter=4,
    what="ONE ISLAND's CHECKPOINT, both floors",
    why="CELIO's network carries signals once its two halves meet. The mainland CHECKPOINT's refrain (HEAL's lullaby, "
        "batch 5), in B-flat, split between the harp and the flute, each holding half of every bar -- then the two "
        "halves meet and play it whole.",
    intro=[],
    loop=join(S("split", 16, lead=_half(_REF, True), sing=_half(_REF, False), arp=arp(_NCH, [0, 1, 2, 1], 0.5), bass=_NB,
                perc=rep("k:1 h:1 h:1 h:1", 4)),
              S("met", 16, lead=_REF, sing=dia(_REF, "Bb C D Eb F G A", 2), arp=arp(_NCH, [0, 1, 2, 1], 0.5), bass=_NB,
                perc=rep("k:1 h:1 h:1 h:1", 4))),
))

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
    print("  %d island pieces on voicegroup%03d" % (len(PIECES), VOICEGROUP))
    if not changed:
        print("  the game: unchanged")
    else:
        print("  the game: %s %d file(s): %s" % ("wrote" if "--write" in sys.argv else "would write", len(changed),
                                                 ", ".join(changed[:6]) + (" ..." if len(changed) > 6 else "")))


if __name__ == "__main__":
    main()
