#!/usr/bin/env python3
"""PLAY's songs (T-417 P4): docs/play_songs.json -> engineGba/src/data/play_songs.h, and the check that keeps them apart.

    python3 tools/genplaysongs.py            # report: the songs, the check, and whether the header is current
    python3 tools/genplaysongs.py --write    # write the header

PLAY listens to the last sixteen notes after every note and asks whether they END in a song it knows -- ORDER ONLY,
octave and tempo ignored, the KEY counting; the right shape in another key is ALMOST (src/play.c, Listen). So two
songs must never share a shape: if one song's intervals sit anywhere inside another's, playing the longer one meets
the shorter on the way and stops there (an echo, or ALMOST), and the longer can never be finished. The design asked
for "no motif is a suffix of another"; a song heard before its end is the same failure, so this checks every place
inside, which includes the end. It exits 1 if any two collide, so check_generators fails with it.

Each song's notes are written three ways in the header:
    notes   semitones from middle C, as the game plays them when the song is HEARD
    pcs     pitch classes, C 0 .. B 11, which is what is listened for
    steps   staff steps (letters from middle C) for the SONGBOOK's page, moved by whole octaves so the tune sits on
            the staff's lines, and spelled as the key would (flats in a flat key)
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "docs", "play_songs.json")
OUT = os.path.join(ROOT, "engineGba", "src", "data", "play_songs.h")

LETTERS = "CDEFGAB"
NATURAL = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
KEYS = {"C": 0, "Db": 1, "C#": 1, "D": 2, "Eb": 3, "D#": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "Ab": 8,
        "G#": 8, "A": 9, "Bb": 10, "A#": 10, "B": 11}
FLAT_KEYS = {1, 3, 5, 8, 10}            # D FLAT, E FLAT, F, A FLAT, B FLAT: an accidental is written as a flat
MAJOR = (0, 2, 4, 5, 7, 9, 11)
MOTIF_MAX = 12                          # src/play.c
FIRST_SONG_IDS = ["FIR", "NAMING", "STILL", "MEND", "PRACTICE", "STANCE", "NOTICE", "REFLECT"]   # include/constants/play.h


def parse(note):
    """'C#5' -> semitones from C4."""
    letter, rest = note[0], note[1:]
    acc = 0
    while rest and rest[0] in "#b":
        acc += 1 if rest[0] == "#" else -1
        rest = rest[1:]
    return NATURAL[letter] + acc + 12 * (int(rest) - 4)


def step(semi, key):
    """The staff step (letters from C4) the note is written on, spelled as the key spells it."""
    octave, pc = divmod(semi, 12)
    if pc in MAJOR:
        letter = MAJOR.index(pc)
    elif key in FLAT_KEYS:
        letter = MAJOR.index(pc + 1)   # an accidental is never B, so its letter above is in the octave
    else:
        letter = MAJOR.index(pc - 1)
    return letter + 7 * octave


def intervals(pcs):
    return tuple((b - a) % 12 for a, b in zip(pcs, pcs[1:]))


def inside(a, b):
    return any(b[i:i + len(a)] == a for i in range(len(b) - len(a) + 1))


def load():
    data = json.load(open(SRC, encoding="utf-8"))
    songs = []
    for s in data["songs"]:
        key = KEYS[s["key"]]
        semis = [parse(n) for n in s["notes"].split()]
        pcs = [x % 12 for x in semis]
        steps = [step(x, key) for x in semis]
        mean = sum(steps) / len(steps)
        while mean < 3:   # the staff's lines are steps 2-10, the middle one 6
            steps = [x + 7 for x in steps]
            mean += 7
        while mean > 9:
            steps = [x - 7 for x in steps]
            mean -= 7
        frames = s.get("frames") or [s["beat"]] * (len(semis) - 1) + [s["last"]]
        songs.append(dict(s, keyNum=key, semis=semis, pcs=pcs, steps=steps, frames=frames))
    return songs


def check(songs):
    errors = []
    ids = [s["id"] for s in songs]
    if ids != FIRST_SONG_IDS:
        errors.append("songs must be in include/constants/play.h's order %s, not %s" % (FIRST_SONG_IDS, ids))
    for s in songs:
        n = len(s["semis"])
        if not 3 <= n <= MOTIF_MAX:
            errors.append("%s: %d notes (3 to %d)" % (s["id"], n, MOTIF_MAX))
        if len(s["frames"]) != n:
            errors.append("%s: %d frames for %d notes" % (s["id"], len(s["frames"]), n))
        outside = [x for x in s["pcs"] if (x - s["keyNum"]) % 12 not in MAJOR]
        if outside:
            errors.append("%s: notes outside %s major: %s" % (s["id"], s["key"], outside))
        if min(s["semis"]) < -12 or max(s["semis"]) > 24:
            errors.append("%s: beyond the three octaves the instruments bend to" % s["id"])
    titles = notebook_titles()
    if titles != [s["title"] for s in songs]:
        errors.append("src/notebook.c's SONGBOOK titles %s are not the json's %s" % (titles, [s["title"] for s in songs]))
    for a in songs:
        for b in songs:
            if a is not b and inside(intervals(a["pcs"]), intervals(b["pcs"])):
                errors.append("%s's shape is inside %s's: %s would be heard before %s ends"
                              % (a["id"], b["id"], a["title"], b["title"]))
    return errors


def notebook_titles():
    """src/notebook.c's SONGBOOK titles, in order -- the rows the player reads."""
    src = open(os.path.join(ROOT, "engineGba", "src", "notebook.c"), encoding="utf-8").read()
    return re.findall(r'sTitle_Song_\w+\[\]\s*=\s*_\("([^"]*)"\)', src)


def c_str(text):
    return '_("%s")' % text.replace('"', '\\"')


def header(songs):
    out = ["// T-417 PLAY's songs -- written by DAEMONS tools/genplaysongs.py from docs/play_songs.json. Do not edit:",
           "// edit the json and run the tool. Every page is DRAFT; the titles are src/notebook.c's.", ""]
    for s in songs:
        name = "sSong_" + s["id"].title()
        out.append("// %s -- %s, in %s major%s" % (s["title"], s["pair"], s["key"],
                                                     " (motif %s, chosen by the user by ear)" % s["motif"] if s.get("motif") else ""))
        out.append("static const s8 %s_Notes[] = {%s};" % (name, ", ".join(map(str, s["semis"]))))
        out.append("static const u8 %s_Pcs[] = {%s};" % (name, ", ".join(map(str, s["pcs"]))))
        out.append("static const s8 %s_Steps[] = {%s};" % (name, ", ".join(map(str, s["steps"]))))
        out.append("static const u8 %s_Frames[] = {%s};" % (name, ", ".join(map(str, s["frames"]))))
        if s.get("page"):
            out.append("static const u8 %s_Page[] = %s;" % (name, c_str(s["page"])))
        out.append("")
    out.append("static const struct PlaySong sSongs[PLAY_SONG_COUNT] =")
    out.append("{")
    for s in songs:
        name = "sSong_" + s["id"].title()
        out.append("    [PLAY_SONG_%s] = {%s, %s, %s, %d, %d, %s_Notes, %s_Pcs, %s_Steps, %s_Frames, %s},"
                   % (s["id"], s["learned"], s["heard"] or "0", s["understanding"] or "0", s["keyNum"], len(s["semis"]),
                      name, name, name, name, name + "_Page" if s.get("page") else "NULL"))
    out.append("};")
    return "\n".join(out) + "\n"


def main():
    write = "--write" in sys.argv
    songs = load()
    for s in songs:
        print("  %-8s %-24s %-2s  %s" % (s["id"], s["title"], s["key"], " ".join(s["notes"].split())))
    errors = check(songs)
    for e in errors:
        print("  FAIL: " + e)
    if errors:
        return 1
    print("  check: no song's shape sits inside another's (%d songs, O CHRISTMAS TREE among them)" % len(songs))
    text = header(songs)
    old = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else None
    if old == text:
        print("  src/data/play_songs.h: unchanged")
    elif write:
        open(OUT, "w", encoding="utf-8").write(text)
        print("  src/data/play_songs.h: written")
    else:
        print("  src/data/play_songs.h: would write (run with --write)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
