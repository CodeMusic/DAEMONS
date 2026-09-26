#!/usr/bin/env python3
"""Carry our music into the GBA build by writing MIDI.

    python3 tools/port_music.py [--write]

The two engines could not be less alike. The Game Boy build IS the sequencer --
`note C_, 8` writes a frequency into a hardware channel. The GBA has a software
mixer, and pokefirered builds its music from .mid files through mid2agb. So
nothing can be copied; the notes have to be re-emitted in another format.

Which is fine, because the notes are the part worth keeping.

Each track REPLACES the MIDI of a slot that already exists rather than claiming
a new one. Adding a song means a new constant, a new song_table row and every
index after it moving; replacing means none of that. The slots were chosen so
the map that plays them is the map the track was written for:

    titletheme -> mus_title      the front door
    slatecity  -> mus_pewter     Pewter IS Slate City
    thebleed   -> mus_route1     Routes 1 and 2

CONVERSIONS, all of them assumptions worth writing down:
  * eight GB ticks is one quarter note -- our own tracks are built in bars of
    32 ticks as four notes of eight, so this is what we wrote them to mean
  * GB octave N becomes MIDI octave N, so `octave 4 / note C_` is middle C and
    a bass line at `octave 2` lands where a bass line belongs
  * the GB `tempo` value is used as BPM directly
The first two are structural. The third is a guess and the most likely thing to
want tuning by ear.
"""
import os, re, struct, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GB, GBA = os.path.join(ROOT, "engine"), os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv
TPQ, TICKS_PER_QUARTER = 480, 8          # MIDI resolution, GB ticks per quarter

#  Slots that must NOT loop.
JINGLES = {"mus_caught_intro"}

# mus_title is NOT ours any more. 7.14g replaced the Game Boy theme with a
# transcription of the rendered one (tools/stems2midi.py) on voicegroup191, and
# leaving it in the list here meant this tool silently overwrote that file and
# repointed its bank on every run. The entry stays as a record of where the
# track came from; SUPERSEDED keeps the tool's hands off it.
SUPERSEDED = {"mus_title"}

TRACKS = [
    ("titletheme",      "mus_title"),        # the front door -- SUPERSEDED
    ("slatecity",       "mus_slate"),        # Pewter IS Slate City -- its own slot since 2026-09-23
    ("thebleed",        "mus_route1"),       # Routes 1 and 2
    ("brazen",          "mus_brazen"),       # Saffron is BRAZEN; the one added slot
    # Eight more that were written on the Game Boy and had never been carried.
    # Each lands where its town landed: the rename already decided the slot.
    ("pallettown",      "mus_pallet"),       # Pallet is BLANCHE
    ("celadon",         "mus_celadon"),      # Celadon is VERDIGRIS
    ("cinnabar",        "mus_cinnabar"),     # Cinnabar is QUICKSILVER
    ("lavender",        "mus_lavender"),     # Lavender is HALFTONE
    ("vermilion",       "mus_vermillion"),   # Vermilion is ARDOR -- FireRed spells it with two Ls
    ("silphco",         "mus_silph"),
    ("cinnabarmansion", "mus_poke_mansion"),
    # pokered's dungeon3 is Mt Moon and Rock Tunnel; Gen 3 splits them and
    # mt_moon is the one the track was written against.
    ("dungeon3",        "mus_mt_moon"),
    # The binding sound. It is tone data, not noise -- a descending figure that
    # settles -- so it ports like a track. Gen 3 splits the capture jingle into
    # an intro and a fanfare; the intro is the moment the box closes.
    ("sfx/caught_mon",  "mus_caught_intro"),
]
# brazen needed a slot of its own, and getting one was cheaper than first
# thought. Saffron shares MUS_PEWTER with Pewter and Viridian in Gen 1, so
# putting Slate City into that slot handed Brazen the wrong theme as well.
# The song table is POSITIONAL -- mus_title is row 278 and MUS_TITLE is 278 --
# so a row APPENDED at the end shifts nothing. Only an insertion would.
#
# And SLATE needed one too (2026-09-23). Writing it over mus_pewter handed it to
# the FORTY-TWO maps vanilla plays that track in -- CALLOW and every floor of its
# school, BRAZEN's houses, the Reading Room, twenty gatehouses -- when the Game
# Boy build, which is the record, plays SLATE's theme in SLATE and nowhere else
# (engine/data/maps/songs.asm: MUSIC_SLATE_CITY on PEWTER_CITY alone). The
# BRAZEN commit said CALLOW sharing it matched the Game Boy; it did not -- there
# CALLOW shares vanilla's Cities1, which is what it gets back here.
# So mus_pewter is RESTORED from upstream, and SLATE is mus_slate.
VANILLA = ["mus_pewter"]

# Which maps play each town's theme -- and one building that is not a town's. A town's houses play the town's music --
# vanilla's own grouping, kept -- so a theme follows its town indoors and no
# further. The maps not listed keep whatever vanilla gave them.
MAP_MUSIC = {
    "MUS_SLATE":  ["PewterCity", "PewterCity_House1", "PewterCity_House2",
                   "PewterCity_Museum_1F", "PewterCity_Museum_2F"],
    # T-05 (2026-09-26): CALLOW's own theme, Desperate Shadows, transcribed from the user's recording by mp3midi.py into
    # an appended slot like SLATE's. The town, its house and every floor of its school; the gatehouses keep vanilla's.
    "MUS_CALLOW": ["ViridianCity", "ViridianCity_House", "ViridianCity_School", "ViridianCity_School_2F",
                   "ViridianCity_School_3F", "ViridianCity_School_4F", "ViridianCity_School_5F",
                   "ViridianCity_School_6F", "ViridianCity_School_7F"],
    "MUS_BRAZEN": ["SaffronCity", "SaffronCity_House", "SaffronCity_Dojo",
                   "SaffronCity_CopycatsHouse_1F", "SaffronCity_CopycatsHouse_2F",
                   "SaffronCity_PokemonTrainerFanClub", "SaffronCity_MrPsychicsHouse"],
    # 1001 Fatal Error is the ruined lab's -- "the building whose terminals carry the log" (song-status.md).
    # FireRed files the POWER PLANT under the Mansion's track, so the port carried the log's music there
    # too; the Game Boy, the record, files it with the hideout (Dungeon1), and so does this. The Route 21
    # station keeps the lab's: it is a room cut from the Mansion's basement, terminals and all (T-74).
    "MUS_ROCKET_HIDEOUT": ["PowerPlant"],
}

SEMI = {"C_": 0, "C#": 1, "D_": 2, "D#": 3, "E_": 4, "F_": 5,
        "F#": 6, "G_": 7, "G#": 8, "A_": 9, "A#": 10, "B_": 11}

def parse(path):
    """-> (tempo, [channel, ...]) where a channel is [(midi_note|None, ticks)]."""
    text = open(path).read()
    tempo = int(re.search(r'tempo (\d+)', text).group(1))
    chans = []
    # Music channels are declared `Music_X_Ch1::` and SFX channels
    # `SFX_X_Ch5:` -- one colon, different prefix, same body.
    for body in re.split(r'^(?:Music|SFX)_\w+_Ch\d+::?', text, flags=re.M)[1:]:
        octave, events = 4, []
        for line in body.splitlines():
            line = line.split(";")[0].strip()
            m = re.match(r'octave (\d+)', line)
            if m:
                octave = int(m.group(1)); continue
            m = re.match(r'note (\w[_#]), (\d+)', line)
            if m:
                events.append(((octave + 1) * 12 + SEMI[m.group(1)], int(m.group(2)))); continue
            m = re.match(r'rest (\d+)', line)
            if m:
                events.append((None, int(m.group(1))))
        if events:
            chans.append(events)
    return tempo, chans

def vlq(n):
    out = bytearray([n & 0x7F]); n >>= 7
    while n:
        out.insert(0, (n & 0x7F) | 0x80); n >>= 7
    return bytes(out)

# The Game Boy bank, tools/gbavoices.py. pokered declares its channels in order
# -- Pulse 1, Pulse 2, Wave, Noise -- and parse() keeps that order, so channel
# index IS the hardware channel and these four programs are its four voices.
#
# Writing no program change at all was what made these songs play VOICE 0, and
# slot 0 of the banks they pointed at is a KEYSPLIT in ten cases out of eleven.
# Keeping the chiptune texture is a decision; playing a drum-kit key map was not.
GB_GROUP = 192
GB_PROGRAMS = [80, 81, 87, 126]

def track(events, chan, loop=True):
    # The body was written TWICE to fake a loop, which cost double the ROM and
    # still stopped after two passes. mid2agb builds a real GOTO out of a MIDI
    # text meta-event -- "[" for the loop start, "]" for the jump back -- so
    # the body is written once and repeats forever.
    data = bytearray()
    program = GB_PROGRAMS[chan] if chan < len(GB_PROGRAMS) else GB_PROGRAMS[-1]
    data += b"\x00" + bytes([0xC0 | chan, program])   # program change
    for _ in range(1):
        rest = 0
        for note, ticks in events:
            dur = ticks * TPQ // TICKS_PER_QUARTER
            if note is None:
                rest += dur; continue
            data += vlq(rest) + bytes([0x90 | chan, note, 100])
            data += vlq(max(1, dur - 6)) + bytes([0x80 | chan, note, 0])
            rest = 6
    data += b"\x00\xFF\x2F\x00"
    return b"MTrk" + struct.pack(">I", len(data)) + bytes(data)

def midi(tempo, chans, loop=True):
    head = bytearray(b"\x00\xFF\x51\x03") + struct.pack(">I", 60000000 // tempo)[1:]
    if loop:
        # The markers go on the TEMPO track. mid2agb reads text meta-events
        # only in ReadSeqEvents(), which is the first MIDI track, and merges
        # them into every AGB track afterwards.
        end = max(sum(t * TPQ // TICKS_PER_QUARTER for _, t in ev) for ev in chans)
        head += b"\x00\xFF\x01\x01[" + vlq(end) + b"\xFF\x01\x01]"
    head += b"\x00\xFF\x2F\x00"
    out = b"MThd" + struct.pack(">IHHH", 6, 1, len(chans) + 1, TPQ)
    out += b"MTrk" + struct.pack(">I", len(head)) + bytes(head)
    for i, ev in enumerate(chans):
        out += track(ev, i, loop)
    return out

rc = 0
for name, slot in TRACKS:
    if slot in SUPERSEDED:
        continue
    # SFX live in audio/sfx/, and one of ours is ordinary tone data rather than
    # noise, so the same parser carries it. A name with a slash says where.
    rel = name if "/" in name else "music/" + name
    src = os.path.join(GB, "audio/%s.asm" % rel)
    dst = os.path.join(GBA, "sound/songs/midi/%s.mid" % slot)
    if not os.path.exists(src):
        print("  !! no %s" % src); rc = 1; continue
    if not os.path.exists(dst):
        # A slot we added ourselves has no .mid yet; one we invented has no
        # song_table row either, and that is the error worth catching.
        table = open(os.path.join(GBA, "sound/song_table.inc")).read()
        if ("song %s," % slot) not in table:
            print("  !! %s is not in song_table.inc" % slot); rc = 1; continue
    tempo, chans = parse(src)
    notes = sum(1 for c in chans for n, _ in c if n is not None)
    print("  %-16s -> %-16s %d channels, %d notes, tempo %d"
          % (name, slot, len(chans), notes, tempo))
    if not chans:
        print("  !! parsed no channels"); rc = 1; continue
    if WRITE:
        # The binding sound is a jingle: it plays once and hands the screen
        # back. Everything else here is ambient and has to repeat.
        open(dst, "wb").write(midi(tempo, chans, loop=slot not in JINGLES))
# ---- the slots given back to vanilla, and each town's maps
import json, subprocess
def upstream(rel):
    return subprocess.run(["git", "-C", GBA, "show", "upstream/master:" + rel],
                          check=True, capture_output=True).stdout
cfg_up = upstream("sound/songs/midi/midi.cfg").decode()
for slot in VANILLA:
    rel = "sound/songs/midi/%s.mid" % slot
    orig, dst = upstream(rel), os.path.join(GBA, rel)
    same = open(dst, "rb").read() == orig
    print("  %-16s <- upstream        %s" % (slot, "vanilla already" if same else "restored" if WRITE else "would restore"))
    if WRITE and not same:
        open(dst, "wb").write(orig)
moved = []
for song, maps in MAP_MUSIC.items():
    for m in maps:
        path = os.path.join(GBA, "data/maps/%s/map.json" % m)
        raw = open(path).read()
        d = json.loads(raw)
        if d["music"] != song:
            moved.append("%s %s -> %s" % (m, d["music"], song))
            if WRITE:
                open(path, "w").write(raw.replace('"music": "%s"' % d["music"], '"music": "%s"' % song, 1))
print("  maps: %s" % ("; ".join(moved) if moved else "every town's maps play its theme"))

if WRITE and rc == 0:
    # midi.cfg carries mid2agb's -G, and a song whose MIDI says program 80
    # while its .cfg still names a bank without a square there is a silent
    # instrument change. The tool that owns the notes owns the bank too.
    cfg = os.path.join(GBA, "sound/songs/midi/midi.cfg")
    text = open(cfg).read()
    hits = 0
    for _, slot in TRACKS:
        if slot in SUPERSEDED:
            continue
        def point(m):
            global hits
            if m.group(2) == str(GB_GROUP):
                return m.group(0)
            hits += 1
            return "%s%d" % (m.group(1), GB_GROUP)
        text, n = re.subn(r"(^%s\.mid:.*?-G)(\d+)" % re.escape(slot),
                          point, text, flags=re.M)
        if not n:
            print("  !! %s has no midi.cfg line" % slot); rc = 1
    for slot in VANILLA:                # and a restored slot's line is upstream's, bank and all
        up = re.search(r"^%s\.mid:.*$" % re.escape(slot), cfg_up, flags=re.M).group(0)
        text = re.sub(r"^%s\.mid:.*$" % re.escape(slot), lambda m: up, text, flags=re.M)
    if text != open(cfg).read():
        open(cfg, "w").write(text)
    print("  midi.cfg: %d song(s) pointed at voicegroup%d" % (hits, GB_GROUP))
    print("  written")
sys.exit(rc)
