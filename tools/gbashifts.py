#!/usr/bin/env python3
"""Season and hour homes on the early roads (T-407; the user approved the draft 2026-10-16).

    python3 tools/gbashifts.py            # report: the tables, and whether every daemon in them is ready
    python3 tools/gbashifts.py --write    # engineGba/src/data/wild_shifts.h

The user, 2026-10-16: "some daemons should have season home -- and even time of day -- perhaps it modifies the
common ones". THE RULE, which a player can learn by walking: on every road up to the fourth MARK one 20% common slot
belongs to the SEASON and one 10% slot to the HOUR (dawn, dusk, night; by day it is the route's own). A slot keeps its
level and its odds, so a road's difficulty does not move. The draft and its reasons are
docs/private/draft-seasons-2026-10-16.md; its two answers: REDACTED at L13 on Route 10 by night is fine, and the
editions' type LEAN stays the islands' rule -- here the pairs are exactly the drafted C|X ones.

HOW. Not a header per season x watch (that is up to sixteen copies of every map's water, rods and Rock Smash, and the
copy is where gbanight's night-without-water bug came from): one const table of rows, read after the land slot is
chosen, on top of whichever header (day or night) was chosen -- src/wild_encounter.c's WildShiftSpecies. A row's
`when` holds the seasons in bits 0-3 (DaemonsSeason's order: WINTER SPRING SUMMER AUTUMN) and the watches in bits 4-7
(DaemonsWatch's order: DAY DUSK NIGHT DAWN); the first row whose season bit AND watch bit are both set wins. RAM 0,
save 0. CONTEXT needs nothing extra: DaemonsSeason already returns the edition's own season.

AND THE DAEMONS MUST BE READY. All of these are met nowhere before the League today, so the report checks every one:
a name, front and back drawn (not pret's), an INDEX entry and category of ours in BOTH editions, and streaks. A
daemon that fails is listed and left OUT of the table -- this tool never writes words.
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
OUT = os.path.join(GBA, "src/data/wild_shifts.h")
WRITE = "--write" in sys.argv
UPSTREAM = "upstream/master"

SEASONS = ["WINTER", "SPRING", "SUMMER", "AUTUMN"]       # include/daemons_time.h, SEASON_*
WATCHES = ["DAY", "DUSK", "NIGHT", "DAWN"]               # include/daemons_time.h, WATCH_*

#  map, (season slot, what is there today), SPRING SUMMER AUTUMN WINTER, (hour slot, today), DAWN DUSK NIGHT.
#  "NAME*" is a (day) row: skipped at night. "C|X" is CONTENT's | CONTEXT's. "today" may be "C|X" too (the editions'
#  own split). Written in the DAEMONS names, exactly as the draft's tables.
TABLES = [
    ("MAP_VIRIDIAN_FOREST", (0, "CRAWLER"), ["LACED*", "PERIPHERY", "STARTLE", "ILLUSION"],
                            (5, "SCRAPER"), ["STATIC", "SYN|ACK", "GLIDEPATH"]),
    ("MAP_ROUTE1",  (0, "PACKET"),  ["WHIM*", "STARVED*", "OMEN|DREAD", "INSTINCT"],
                    (4, "PACKET"),  ["HUDDLE", "AMBUSH", "POLL"]),
    ("MAP_ROUTE2",  (1, "PACKET"),  ["TEMPO", "SHORTJUMP*", "WARMUP", "INSTINCT"],
                    (5, "PACKET"),  ["ALARM", "AMBUSH", "SMUDGE"]),
    ("MAP_ROUTE22", (0, "NIBBLE"),  ["LOOPBACK", "DETOUR", "WARNING", "LOCKFILE"],
                    (4, "NIBBLE"),  ["HUDDLE", "HASHCODE", "FIXATION"]),
    ("MAP_ROUTE3",  (1, "PACKET"),  ["DATAGRAM", "PIXELBYTE", "SINKHOLE", "CUNNING|REPAY"],
                    (3, "PREEMPT"), ["VIGILANCE", "GRASP", "RESIDUAL"]),
    ("MAP_ROUTE4",  (1, "NIBBLE"),  ["TENSION", "FEWSHOT", "HOARDING", "LOCKFILE"],
                    (5, "NIBBLE"),  ["CRACKLE", "POSTULATE", "BACKDOOR"]),
    ("MAP_ROUTE24", (0, "SCRAPER"), ["APATHY|MOOD", "PARTICLE", "SPARRING", "TELL"],
                    (4, "SPRAWL|SNARE"), ["LOWBIT", "GRASP", "HONEYTRAP"]),
    ("MAP_ROUTE25", (0, "SCRAPER"), ["TRUST", "TANGENT*", "COMFORT", "PENGUIN"],
                    (4, "SPRAWL|SNARE"), ["ALARM", "SYN|ACK", "POLL"]),
    ("MAP_ROUTE5",  (1, "PACKET"),  ["OVERTONE", "SLOWBURN", "STARTLE", "LOCKFILE"],
                    (5, "PACKET"),  ["TANGENT", "PRISTINE|FORGERY", "SMUDGE"]),
    ("MAP_ROUTE6",  (1, "PACKET"),  ["LACED*", "PARTICLE", "SPARRING", "PENGUIN"],
                    (5, "PACKET"),  ["LOWBIT", "ANODE|CATHODE", "FIXATION"]),
    ("MAP_ROUTE11", (1, "PING"),    ["CRACKLE", "SLOWBURN", "HASHCODE", "TELL"],
                    (2, "SECTOR|WORM"), ["VIGILANCE", "POSTULATE", "ILLUSION"]),
    ("MAP_ROUTE9",  (1, "NIBBLE"),  ["LOOPBACK", "RECALL", "HOARDING", "CUNNING|REPAY"],
                    (2, "SECTOR|WORM"), ["DATAGRAM", "DUPLEX", "BACKDOOR"]),
    ("MAP_ROUTE10", (0, "PING"),    ["TENSION", "SLOWBURN", "OMEN|DREAD", "LOCKFILE"],
                    (4, "PING"),    ["VIGILANCE", "DUPLEX", "REDACTED"]),
    ("MAP_ROUTE8",  (1, "COOKIE"),  ["OVERTONE", "FEWSHOT", "OMEN|DREAD", "CUNNING|REPAY"],
                    (2, "SENTRY|FLICKER"), ["DATAGRAM", "PRISTINE|FORGERY", "FIXATION"]),
    ("MAP_ROUTE7",  (0, "PACKET"),  ["LACED*", "STARVED*", "WARMUP", "TELL"],
                    (4, "PACKET"),  ["HUDDLE", "SYN|ACK", "SMUDGE"]),
]
DRAFT_SEASONS = ["SPRING", "SUMMER", "AUTUMN", "WINTER"]   # the draft's column order
DRAFT_HOURS = ["DAWN", "DUSK", "NIGHT"]
EDITIONS = (("CONTENT", "FIRERED", "FireRed"), ("CONTEXT", "LEAFGREEN", "LeafGreen"))

#  Species the report found unready and the table therefore leaves out (none, 2026-10-16). Name and why.
LEFT_OUT = {}


def read(rel):
    return open(os.path.join(GBA, rel), encoding="utf-8").read()


def upstream(rel, binary=False):
    r = subprocess.run(["git", "-C", GBA, "show", "%s:%s" % (UPSTREAM, rel)], capture_output=True)
    return r.stdout if binary else r.stdout.decode("utf-8", "replace")


def by_name():
    out = {}
    for sp, name in re.findall(r"\[(SPECIES_\w+)\]\s*=\s*_\(\"([^\"]*)\"\)", read("src/data/text/species_names.h")):
        out.setdefault(name, []).append(sp)
    return out


def pick(cell, ed):
    """The DAEMONS name a cell means in edition ed (0 CONTENT, 1 CONTEXT), and whether it is a (day) row."""
    day = cell.endswith("*")
    cell = cell.rstrip("*")
    return (cell.split("|")[ed] if "|" in cell else cell), day


def rows(names):
    """[(edition index, map, slot, when, species constant, daemon name)], in the draft's order."""
    out = []
    for ed in (0, 1):
        for mp, (sslot, _), seasons, (hslot, _), hours in TABLES:
            for col, cell in zip(DRAFT_SEASONS, seasons):
                name, day = pick(cell, ed)
                watches = [w for w in WATCHES if not (day and w == "NIGHT")]
                out.append((ed, mp, sslot, ([col], watches), names[name][0], name))
            for col, cell in zip(DRAFT_HOURS, hours):
                name, _ = pick(cell, ed)
                out.append((ed, mp, hslot, (SEASONS, [col]), names[name][0], name))
    return out


def when_expr(seasons, watches):
    s = "WS_ALL_SEASONS" if len(seasons) == 4 else " | ".join("WS_SEASON(SEASON_%s)" % x for x in seasons)
    if len(watches) == 4:
        w = "WS_ALL_WATCHES"
    elif sorted(watches) == sorted(["DAY", "DUSK", "DAWN"]):
        w = "WS_NOT_NIGHT"
    else:
        w = " | ".join("WS_WATCH(WATCH_%s)" % x for x in watches)
    return s + " | " + w


def readiness(species):
    """{species: [what is missing]} -- name, art, INDEX (both editions), category, streaks."""
    entries, up_entries = read("src/data/pokemon/pokedex_entries.h"), upstream("src/data/pokemon/pokedex_entries.h")
    texts = {e: (read("src/data/pokemon/pokedex_text_%s.h" % e), upstream("src/data/pokemon/pokedex_text_%s.h" % e))
             for e in ("fr", "lg")}
    streaks = read("src/data/pokemon/streaks.h")

    def text_of(src, sym):
        m = re.search(r"const u8 %s\[\] = _\((.*?)\);" % re.escape(sym), src, re.S)
        return m.group(1) if m else None

    def category(src, sp):
        m = re.search(r"\[NATIONAL_DEX_%s\]\s*=\s*\{\s*\.categoryName = _\(\"([^\"]*)\"\)" % sp[8:], src)
        return m.group(1) if m else None

    out = {}
    for sp in sorted(species):
        miss = []
        d = sp[8:].lower()
        for part in ("front.png", "back.png"):
            rel = "graphics/pokemon/%s/%s" % (d, part)
            if not os.path.exists(os.path.join(GBA, rel)):
                miss.append("no " + part)
            elif open(os.path.join(GBA, rel), "rb").read() == upstream(rel, binary=True):
                miss.append(part + " is pret's")
        m = re.search(r"\[NATIONAL_DEX_%s\][^}]*?\.description = (\w+)" % sp[8:], entries, re.S)
        if not m:
            miss.append("no INDEX entry")
        else:
            for e, ed in (("fr", "CONTENT"), ("lg", "CONTEXT")):
                ours, theirs = text_of(texts[e][0], m.group(1)), text_of(texts[e][1], m.group(1))
                if not ours:
                    miss.append("no %s INDEX text" % ed)
                elif ours == theirs:
                    miss.append("%s INDEX text is vanilla's" % ed)
        cat = category(entries, sp)
        if not cat or cat == category(up_entries, sp):
            miss.append("INDEX category is vanilla's")
        if not re.search(r"\[%s\] = TRUE" % sp, streaks):
            miss.append("no streaks")
        out[sp] = miss
    return out


def render(table):
    lines = [
        "//  Generated by tools/gbashifts.py -- edit the tool, not this file.",
        "//  T-407 (the user, 2026-10-16): season and hour homes on the early roads. One 20% land slot belongs to the",
        "//  season and one 10% slot to the hour (dawn, dusk, night); level and odds stay the slot's own. Read after the",
        "//  land slot is chosen, on top of whichever header (day or night) was chosen: the first row for this map and",
        "//  slot whose season bit AND watch bit are both set wins (src/wild_encounter.c, WildShiftSpecies).",
        "",
        "struct WildShift",
        "{",
        "    u8 mapGroup;",
        "    u8 mapNum;",
        "    u8 slot;",
        "    u8 when;     // bits 0-3: SEASON_* (DaemonsSeason), bits 4-7: WATCH_* (DaemonsWatch)",
        "    u16 species;",
        "};",
        "",
        "#define WS_SEASON(s)    (1 << (s))",
        "#define WS_WATCH(w)     (1 << (4 + (w)))",
        "#define WS_ALL_SEASONS  0x0F",
        "#define WS_ALL_WATCHES  0xF0",
        "#define WS_NOT_NIGHT    (WS_ALL_WATCHES & ~WS_WATCH(WATCH_NIGHT))   // a (day) row: skipped at night",
        "",
        "static const struct WildShift sWildShifts[] =",
        "{",
    ]
    for i, (edname, define, _) in enumerate(EDITIONS):
        lines.append("#%s defined(%s)   // %s" % ("if" if i == 0 else "elif", define, edname))
        last = None
        for ed, mp, slot, (ss, ws), sp, name in table:
            if ed != i:
                continue
            if mp != last:
                lines.append("    // %s" % mp[4:])
                last = mp
            lines.append("    { MAP_GROUP(%s), MAP_NUM(%s), %2d, %s, %s },   // %s"
                         % (mp, mp, slot, when_expr(ss, ws), sp, name))
    lines += ["#endif", "};", ""]
    return "\n".join(lines)


def main():
    names = by_name()
    for mp, (sslot, stoday), seasons, (hslot, htoday), hours in TABLES:
        for cell in seasons + hours + [stoday, htoday]:
            for n in cell.rstrip("*").split("|"):
                assert len(names.get(n, [])) == 1, "%s: %r names %s" % (mp, n, names.get(n))
    #  The slot must still hold what the draft says it holds today, in each edition's DAY table.
    import json
    wild = json.loads(read("src/data/wild_encounters.json"))["wild_encounter_groups"][0]["encounters"]
    for ed, (_, _, label) in enumerate(EDITIONS):
        for mp, (sslot, stoday), _, (hslot, htoday), _ in TABLES:
            day = [e for e in wild if e["map"] == mp and label in e["base_label"] and not e["base_label"].endswith("_Night")]
            assert len(day) == 1 and "land_mons" in day[0], (mp, label)
            for slot, today in ((sslot, stoday), (hslot, htoday)):
                want = names[pick(today, ed)[0]][0]
                have = day[0]["land_mons"]["mons"][slot]["species"]
                assert have == want, "%s %s slot %d holds %s, the draft says %s" % (mp, label, slot, have, want)

    table = rows(names)
    species = {sp for _, _, _, _, sp, _ in table}
    ready = readiness(species)
    unready = {sp: m for sp, m in ready.items() if m}
    for sp, why in sorted(unready.items()):
        if sp not in LEFT_OUT:
            print("  !! %s is not ready: %s -- add it to LEFT_OUT or finish it" % (sp, "; ".join(why)))
    if any(sp not in LEFT_OUT for sp in unready):
        return 1
    table = [r for r in table if r[4] not in LEFT_OUT]
    for sp, why in sorted(LEFT_OUT.items()):
        print("  left out: %s -- %s" % (sp, why))

    print("  %d maps, %d rows per edition, %d daemons (%d ready: name, art, INDEX in both editions, streaks)"
          % (len(TABLES), sum(1 for r in table if r[0] == 0), len({r[4] for r in table}), len(ready) - len(unready)))
    new = render(table)
    old = open(OUT).read() if os.path.exists(OUT) else None
    if new == old:
        print("  wild_shifts.h already written")
        return 0
    print("  wild_shifts.h %s" % ("to write" if old is None else "differs"))
    if WRITE:
        open(OUT, "w").write(new)
        print("  written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
