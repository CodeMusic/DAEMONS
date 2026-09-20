#!/usr/bin/env python3
"""Is every daemon a thing that RUNS? (T-171; vision.md 8.2b)

    python3 tools/checkregister.py            # the counts, and the Kanto names that are not a process
    python3 tools/checkregister.py --all      # every renamed species with its bucket

THE QUESTION, in the user's words: the game is called DAEMONS, a daemon is a process that runs in the background,
and `PING` is one -- `DEADLOCK` is not. It is NOT proposed as a rule. This measures how many do not fit, so the
ruling can be made on a count rather than an impression.

THE BUCKETS. A name is put in exactly one, by hand, and a name missing from the table is REPORTED, never guessed:

    RUNS    a process, program or daemon -- something that is running: PING, CRAWLER, SCHEDULER, REAPER, SLURP
    DOES    an operation a running system performs: FORK, SPAWN, BRANCH, FLOOD, ESCALATE
    HAS     a part or structure it has: HEAP, STACK, BUFFER, PACKET, MUTEX, SECTOR
    STATE   a condition it is IN, which is the user's DEADLOCK case: LATENCY, OVERFLOW, PENDING, SPIKE
    WORLD   a word from outside computing entirely: BLIGHT, SEEDLING, WISP, PULSAR
    MIND    8.2b's psychology register -- the islands, and Act 2 is mind: APATHY, DREAD, TRUST
    MYTH    8.2b's legendaries: ASCLEPIUS, ORPHEUS, PROMETHEUS
    OURS    8.2b's fourth register, the project's own: the MUSAI, the ROVERs, S.T.A.R.R., PIXELBYTE, REFORGE

8.2B IS NOT UP FOR RE-ARGUMENT HERE. The islands are psychology and the legendaries are myth BY RULING, so they
are counted apart rather than judged: the question is asked of KANTO's bestiary, which is the technical register.
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = os.path.join(ROOT, "engineGba")

BUCKET = {
    #  RUNS -- a thing that is running. Several are real programs: ping, echo, driftnet, slurp, uptime, sentry.
    "PING": "RUNS", "ECHO": "RUNS", "CRAWLER": "RUNS", "DRIFTNET": "RUNS", "SLURP": "RUNS", "SCRAPER": "RUNS",
    "INDEXER": "RUNS", "SCHEDULER": "RUNS", "REAPER": "RUNS", "SENTINEL": "RUNS", "SENTRY": "RUNS", "SHELL": "RUNS",
    "TRACER": "RUNS", "TRACKER": "RUNS", "PREDICTOR": "RUNS", "HANDLER": "RUNS", "KEEPER": "RUNS", "GUARDIAN": "RUNS",
    "HAUNTPROC": "RUNS", "ROOTKIT": "RUNS", "SPYWARE": "RUNS", "WORM": "RUNS", "HONEYPOT": "RUNS", "TARPIT": "RUNS",
    "BOOTSTRAP": "RUNS", "RELAY": "RUNS", "BEACON": "RUNS", "UPTIME": "RUNS", "INJECTOR": "RUNS", "BROADCAST": "RUNS",
    "WIRETAP": "RUNS", "MULTICAST": "RUNS", "LOOKOUT": "RUNS", "ALARM": "RUNS", "HEARTBEAT": "RUNS", "SIGKILL": "RUNS",
    #  DOES -- an operation
    "FORK": "DOES", "SPAWN": "DOES", "BRANCH": "DOES", "FLOOD": "DOES", "ESCALATE": "DOES", "PREEMPT": "DOES",
    "SUSPEND": "DOES", "HIBERNATE": "DOES", "INFERENCE": "DOES", "COLDREAD": "DOES", "FERRY": "DOES", "FORGE": "DOES",
    "LOOP": "DOES", "AXIOMKICK": "DOES", "DRAGNET": "DOES", "SNARE": "DOES", "RECALL": "DOES", "RELEASE": "DOES",
    "REPAY": "DOES", "GATHERING": "DOES", "BUILDUP": "DOES", "OVERLAY": "DOES", "CIRCULAR": "DOES",
    #  HAS -- a part or a structure
    "HEAP": "HAS", "STACK": "HAS", "BUFFER": "HAS", "PACKET": "HAS", "PAYLOAD": "HAS", "MUTEX": "HAS",
    "SEMAPHORE": "HAS", "SPINLOCK": "HAS", "THREAD": "HAS", "PIPELINE": "HAS", "KERNEL": "HAS", "SECTOR": "HAS",
    "PARTITION": "HAS", "NIBBLE": "HAS", "COOKIE": "HAS", "LABEL": "HAS", "STUB": "HAS", "MOCK": "HAS",
    "CAPSULE": "HAS", "CLUSTER": "HAS", "BACKBONE": "HAS", "UPSTREAM": "HAS", "MONOLITH": "HAS", "MANIFOLD": "HAS",
    "ENSEMBLE": "HAS", "DUALCORE": "HAS", "TRIPLECORE": "HAS", "MAGTAPE": "HAS", "MAINFRAME": "HAS", "DRUM": "HAS",
    "PUNCHCARD": "HAS", "HOTPATH": "HAS", "TAPPOINT": "HAS", "FOSSILNET": "HAS", "SMOGSTACK": "HAS", "FUSE": "HAS",
    "BREAKER": "HAS", "DYNAMO": "HAS", "COLDVAULT": "HAS", "BADSEED": "HAS", "ENGRAM": "HAS", "SYMBOL": "HAS",
    "PREMISE": "HAS", "GOLDSET": "HAS", "HARDLINE": "HAS", "MIME": "HAS", "QUORUM": "HAS", "SUBSTRATE": "HAS",
    "LANDFILL": "HAS", "STANDBY": "HAS", "BLINDSPOT": "HAS", "PERIPHERY": "HAS", "RESIDUAL": "HAS",
    #  STATE -- a condition the system is IN. The user's own example, DEADLOCK, is the head of this list.
    "DEADLOCK": "STATE", "LIVELOCK": "STATE", "LATENCY": "STATE", "OVERFLOW": "STATE", "PENDING": "STATE",
    "FAULT": "STATE", "SPIKE": "STATE", "SURGE": "STATE", "STAMPEDE": "STATE", "SPAGHETTI": "STATE",
    "EDGECASE": "STATE", "OUTLIER": "STATE", "ANOMALY": "STATE", "OUTBREAK": "STATE", "OVERDRIVE": "STATE",
    "FLICKER": "STATE", "LULL": "STATE", "STATIC": "STATE", "TENSION": "STATE", "TURBULENCE": "STATE",
    "EMERGENCE": "STATE", "SINGULAR": "STATE", "TORPOR": "STATE", "SIMMER": "STATE", "CRANK": "STATE",
    #  WORLD -- outside computing altogether
    "BLIGHT": "WORLD", "SEEDLING": "WORLD", "WEED": "WORLD", "WISP": "WORLD", "PULSAR": "WORLD", "SLUDGE": "WORLD",
    "FUMES": "WORLD", "NOZZLE": "WORLD", "JETSTREAM": "WORLD", "CHILLER": "WORLD", "CRYOGEN": "WORLD",
    "BULLDOZER": "WORLD", "RAMROD": "WORLD", "PINCER": "WORLD", "CLAMPJAW": "WORLD", "MITE": "WORLD",
    "WILDFIRE": "WORLD", "RELIC": "WORLD", "REVENANT": "WORLD", "CAIRNLING": "WORLD", "LOCUS": "WORLD",
    "VICE": "WORLD", "CANON": "WORLD", "RUBRIC": "WORLD", "PROOF": "WORLD", "THEOREM": "WORLD",
    "CONJECTURE": "WORLD", "REBUTTAL": "WORLD", "HUNCH": "WORLD", "TRANCE": "WORLD", "LEMMA MIND": "WORLD",
    "ARMOURING": "WORLD", "BRISTLE": "WORLD", "CINDER": "WORLD", "OMEN": "WORLD", "TELL": "WORLD",
    "BUOYANCY": "WORLD", "CALLOUS": "WORLD", "ILLUSION": "WORLD", "IMITATION": "WORLD", "AMBUSH": "WORLD",
    "HUDDLE": "WORLD", "GRASP": "WORLD", "ENTRAPMENT": "WORLD", "CLINGING": "WORLD", "HOARDING": "WORLD",
    "STARTLE": "WORLD", "VIGILANCE": "WORLD", "RUMINATE": "WORLD", "MISSINGNO": "WORLD",
    #  MIND -- 8.2b's psychology register (the islands)
    "APATHY": "MIND", "DREAD": "MIND", "TRUST": "MIND", "HOPE": "MIND", "GRIEVANCE": "MIND", "RESENTMENT": "MIND",
    "RANKLE": "MIND", "VALENCE": "MIND", "MOOD": "MIND", "COMFORT": "MIND", "ELATION": "MIND", "CRAVING": "MIND",
    "OBSESSION": "MIND", "FIXATION": "MIND", "ATTACHMENT": "MIND", "ABANDON": "MIND", "WITHDRAWAL": "MIND",
    "BROODING": "MIND", "CAPRICE": "MIND", "WHIM": "MIND", "IMPULSE": "MIND", "INSTINCT": "MIND", "DRIVE": "MIND",
    "CUNNING": "MIND", "PRESCIENCE": "MIND", "PROTEUS": "MIND",
    #  MYTH and OURS -- 8.2b's other two registers
    "ASCLEPIUS": "MYTH", "ORPHEUS": "MYTH", "PROMETHEUS": "MYTH",
    "MUSAI": "OURS", "CODEMUSAI": "OURS", "CAREMUSAI": "OURS", "SEEKMUSAI": "OURS", "LENSMUSAI": "OURS",
    "MASKMUSAI": "OURS", "ROVERCUB": "OURS", "ROVERSEER": "OURS", "ROVERBYTE": "OURS", "STARR": "OURS",
    "ARTSAI": "OURS", "PIXELBYTE": "OURS", "REFORGE": "OURS",
}

PAT = r'\[SPECIES_(\w+)\]\s*=\s*_\("([^"]*)"\)'


def names():
    ours = dict(re.findall(PAT, open(os.path.join(E, "src/data/text/species_names.h")).read()))
    up = dict(re.findall(PAT, subprocess.run(["git", "-C", E, "show", "upstream/master:src/data/text/species_names.h"],
                                             capture_output=True, text=True).stdout))
    ids = {m.group(1): int(m.group(2)) for m in re.finditer(r"#define SPECIES_(\w+)\s+(\d+)",
                                                            open(os.path.join(E, "include/constants/species.h")).read())}
    return [(o, "Kanto" if ids.get(c, 999) <= 151 else "beyond") for c, o in ours.items() if up.get(c) not in (None, o)]


def main():
    rows = [(n, where, BUCKET.get(n)) for n, where in names()]
    missing = [n for n, _, b in rows if b is None]
    order = ["RUNS", "DOES", "HAS", "STATE", "WORLD", "MIND", "MYTH", "OURS"]
    print("  %-7s %6s %7s   %s" % ("bucket", "Kanto", "beyond", "what it is"))
    what = {"RUNS": "a thing that runs", "DOES": "an operation it performs", "HAS": "a part it has",
            "STATE": "a condition it is in", "WORLD": "from outside computing", "MIND": "8.2b psychology",
            "MYTH": "8.2b legendaries", "OURS": "8.2b the project's own"}
    for b in order:
        k = sum(1 for _, w, x in rows if x == b and w == "Kanto")
        o = sum(1 for _, w, x in rows if x == b and w == "beyond")
        print("  %-7s %6d %7d   %s" % (b, k, o, what[b]))
    print("  %d names, %d Kanto" % (len(rows), sum(1 for _, w, _ in rows if w == "Kanto")))
    if "--all" in sys.argv:
        for n, w, b in sorted(rows, key=lambda r: (r[2] or "?", r[0])):
            print("  %-7s %-7s %s" % (b, w, n))
    else:
        for b in ("STATE", "WORLD"):
            ns = sorted(n for n, w, x in rows if x == b and w == "Kanto")
            print("\n  KANTO, %s (%d): %s" % (b, len(ns), ", ".join(ns)))
    if missing:
        print("\n  %d NOT IN THE TABLE, so not counted: %s" % (len(missing), ", ".join(sorted(missing))))
        sys.exit(1)


if __name__ == "__main__":
    main()
