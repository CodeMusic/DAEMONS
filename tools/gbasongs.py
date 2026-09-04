#!/usr/bin/env python3
"""Prove what the songs in the ROM actually play. The audio verify-sprites.

    python3 tools/gbasongs.py           # ours
    python3 tools/gbasongs.py --all     # every song in the build

Three audio bugs reached a play-test in this project, and every one of them was
invisible to the build:

  * NO PROGRAM CHANGE. mid2agb emits a VOICE byte only where the MIDI carries
    one. Without it the track plays on whatever instrument is current, which
    was silence.
  * VOICE 0 IS NOT NEUTRAL. In voicegroup137 slot 0 is a keysplit and 1-3 are
    voice_square_1, so a correct transcription came back as Game Boy squares
    on hardware with a sample ROM.
  * NO LOOP MARKER. mid2agb builds a GOTO out of a MIDI text meta-event, and
    only from the FIRST midi track. Twelve songs ended on FINE and stopped.

Each of those compiled cleanly and each needed a human to sit and listen. This
reads the generated assembly instead and says what will come out of the
speaker: which bank, which instrument per track, and whether it repeats.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
ASM = os.path.join(GBA, "sound/songs/midi")

#  What this project wrote. Everything else is upstream's and not our problem.
OURS = ["mus_title", "mus_pallet", "mus_pewter", "mus_route1", "mus_brazen",
        "mus_celadon", "mus_cinnabar", "mus_lavender", "mus_vermillion",
        "mus_silph", "mus_poke_mansion", "mus_mt_moon", "mus_caught_intro"]
JINGLES = {"mus_caught_intro"}          # plays once and hands the screen back

def banks():
    """{voicegroup: [what each program number resolves to]}."""
    out, cur = {}, None
    for ln in open(os.path.join(GBA, "sound/voice_groups.inc")):
        m = re.match(r"^(voicegroup\d+)::", ln)
        if m:
            cur = m.group(1); out[cur] = []; continue
        if cur and ln.strip().startswith("voice"):
            d = re.search(r"DirectSoundWaveData_(\w+)", ln)
            out[cur].append(d.group(1) if d else
                            ("keysplit" if "keysplit" in ln else "PSG"))
    return out

def songs(names):
    bank = banks()
    bad = 0
    for n in names:
        f = os.path.join(ASM, n + ".s")
        if not os.path.isfile(f):
            print("  %-18s -- not built" % n); continue
        body = open(f).read()
        grp = re.search(r"_grp,\s*(voicegroup\d+)", body).group(1)
        voices = [int(x) for x in re.findall(r"VOICE\s*,\s*(\d+)", body)]
        tracks = len(re.findall(r"^%s_\d+:$" % n, body, re.M))
        loops = body.count("GOTO")
        # mid2agb COMPRESSES: a repeated bar becomes a PATT reference and its
        # notes are written once. A low note count beside a high pattern count
        # is a well-compressed song, not a missing one.
        # COUNT THE NOTE NAMES, NOT THE N<len> PREFIXES. mid2agb omits the
        # length on a note whose length repeats, so most note lines are a bare
        # ".byte  Cn3" -- counting N24 found 4 notes in a song that has 32.
        notes = len(re.findall(r"\b[A-G][ns]-?\d\b", body))
        patts = len(re.findall(r"\bPATT\b", body))

        played = [(v, bank.get(grp, [])[v] if v < len(bank.get(grp, [])) else "?")
                  for v in voices]
        psg = [v for v, s in played if s in ("PSG", "keysplit")]
        want_loop = n not in JINGLES
        ok = len(voices) == tracks and not psg and (loops > 0) == want_loop
        bad += not ok
        print("  %-18s %-14s %2d tracks %5d notes %4d patt  %s%s"
              % (n, grp, tracks, notes, patts,
                 "loops" if loops else ("jingle" if not want_loop else "DOES NOT LOOP"),
                 "" if ok else "   <-- check"))
        print("       %s" % ", ".join("%d=%s" % (v, s) for v, s in played))
        if len(voices) != tracks:
            print("       !! %d tracks but %d program changes -- a track will play"
                  " on whatever instrument is current" % (tracks, len(voices)))
        if psg:
            # Not automatically a bug: PSG is a legitimate texture, and these
            # are Game Boy compositions. It is flagged because it should be a
            # DECISION -- it was previously the accident of writing no program
            # change at all.
            print("       ?  programs %s are PSG or a keysplit -- square waves."
                  " Decide, do not inherit" % ", ".join(str(v) for v in psg))
    return bad

def main():
    names = sorted(x[:-2] for x in os.listdir(ASM) if x.startswith("mus_")
                   and x.endswith(".s")) if "--all" in sys.argv else OURS
    print("  %d songs\n" % len(names))
    bad = songs(names)
    print("\n  %s" % ("all clean" if not bad else "%d song(s) need a look" % bad))
    sys.exit(1 if bad else 0)

main()
