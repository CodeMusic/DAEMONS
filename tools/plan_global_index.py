#!/usr/bin/env python3
"""Plan where every daemon past #151 is met -- a proposal to review, not a write.

    python3 tools/plan_global_index.py                 # the summary
    python3 tools/plan_global_index.py --html out.html # the review page

The request, 2026-09-14: every daemon in the GLOBAL INDEX past #151 should be
findable in the seven islands, some in CONTENT and some in CONTEXT. Measured the
same day: 235 species are numbered past 151 (the Unown placeholders aside),
and 33 of them are met anywhere -- 28 per edition, 5 unique to each.

NOTHING HERE IS WRITTEN TO THE GAME. It derives a placement from the data so a
person can argue with a table instead of with a paragraph. Every rule below is
one line to change, and the page shows what each rule did.

  EDITION   vision.md's Tier 2, "let the rosters lean": CONTENT sees more of
            CONTENT, LOGIC, STRATUM, LEGACY; CONTEXT sees more of CONTEXT,
            LATENT, VECTOR, ENTROPY. A family whose members lean only one way
            is that edition's; a family that leans both ways or neither is
            met in both. Exclusives are why "you cannot complete the Index
            alone" -- and the lean, not a coin, is what decides them.
  HABITAT   by type: FLOW in the water and on the rod; FROZEN in ICEFALL CAVE;
            LATENT and OPAQUE in the LOST CAVE; STRATUM, LEGACY and HARDENED in
            the RUBY PATH and SEVAULT CANYON; ENTROPY on the mountain and SMOKE
            ROAD; GROWTH, SWARM and CORRUPT in the BERRY FOREST and PATTERN
            BUSH; CONTEXT at the ruins; the rest in the open.
  STAGE     a family's first form on islands 1-3, later forms on 4-7, never
            below the level they evolve at -- so a player can meet a line in
            order and still find each form wild.
  ALREADY   the 33 met on the islands today keep their places.
  FIXED     the 16 legendaries are not wild: each gets a proposed fixed
            encounter, and those are design, not derivation.

What it does NOT settle, and the page says so: NAMES. vision.md 2.10 is "a
species the player can meet gets a name", and 8.2b/8.2a hold the islands'
names back -- make 235 meetable and ~200 more need one.
"""
import html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")

TYPE_NAME = {"TYPE_NORMAL": "CONTENT", "TYPE_FIGHTING": "LOGIC", "TYPE_FLYING": "VECTOR",
             "TYPE_POISON": "CORRUPT", "TYPE_GROUND": "STRATUM", "TYPE_ROCK": "LEGACY",
             "TYPE_BUG": "SWARM", "TYPE_GHOST": "LATENT", "TYPE_STEEL": "HARDENED",
             "TYPE_FIRE": "ENTROPY", "TYPE_WATER": "FLOW", "TYPE_GRASS": "GROWTH",
             "TYPE_ELECTRIC": "SIGNAL", "TYPE_PSYCHIC": "CONTEXT", "TYPE_ICE": "FROZEN",
             "TYPE_DRAGON": "EMERGENT", "TYPE_DARK": "OPAQUE"}
LEAN = {"CONTENT": {"TYPE_NORMAL", "TYPE_FIGHTING", "TYPE_GROUND", "TYPE_ROCK"},
        "CONTEXT": {"TYPE_PSYCHIC", "TYPE_GHOST", "TYPE_FLYING", "TYPE_FIRE"}}

# Where a map sits, read off its id, and what kind of place it is.
ISLAND = [("ONE_ISLAND", 1), ("MT_EMBER", 1), ("TWO_ISLAND", 2), ("THREE_ISLAND", 3),
          ("FOUR_ISLAND", 4), ("FIVE_ISLAND", 5), ("SIX_ISLAND", 6), ("SEVEN_ISLAND", 7)]
NOT_OURS = ("ALTERING_CAVE", "TANOBY_RUINS_")        # variable tables, and the chambers' own puzzle
HABITAT = [("ICEFALL_CAVE", "ice"), ("LOST_CAVE", "shadow"), ("RUBY_PATH", "deep rock"),
           ("SUMMIT_PATH", "mountain"), ("MT_EMBER_EXTERIOR", "mountain"), ("KINDLE_ROAD", "mountain"),
           ("SEVAULT_CANYON", "canyon"), ("BERRY_FOREST", "forest"), ("PATTERN_BUSH", "forest"),
           ("RUIN_VALLEY", "ruins"), ("MEMORIAL_PILLAR", "ruins")]
PREF = {"TYPE_ICE": ["ice"], "TYPE_GHOST": ["shadow"], "TYPE_DARK": ["shadow", "ruins"],
        "TYPE_ROCK": ["deep rock", "canyon"], "TYPE_GROUND": ["deep rock", "canyon"],
        "TYPE_STEEL": ["canyon", "deep rock"], "TYPE_FIRE": ["mountain"],
        "TYPE_FIGHTING": ["canyon", "mountain"], "TYPE_DRAGON": ["canyon", "ruins"],
        "TYPE_GRASS": ["forest"], "TYPE_BUG": ["forest"], "TYPE_POISON": ["forest", "shadow"],
        "TYPE_PSYCHIC": ["ruins"], "TYPE_ELECTRIC": ["open"], "TYPE_NORMAL": ["open"],
        "TYPE_FLYING": ["open"]}
# New distinct species a table can take, per kind of slot.
ROOM = {"land_mons": 8, "water_mons": 4, "fishing_mons": 5, "rock_smash_mons": 3}

# The sixteen that are not wild. Proposals, and the page says so.
FIXED = {
    "SPECIES_RAIKOU":    ("Roams the islands after the GLOBAL INDEX", "both", "The engine already roams one beast; which one follows the starter"),
    "SPECIES_ENTEI":     ("Roams the islands after the GLOBAL INDEX", "both", "As above"),
    "SPECIES_SUICUNE":   ("Roams the islands after the GLOBAL INDEX", "both", "As above"),
    "SPECIES_LUGIA":     ("NAVEL ROCK, the deep end", "both", "Needs the same no-ticket ferry THE ANNEX now has"),
    "SPECIES_HO_OH":     ("NAVEL ROCK, the summit", "both", "As above"),
    "SPECIES_CELEBI":    ("BERRY FOREST, once", "both", "A fixed encounter where GROWTH already lives"),
    "SPECIES_JIRACHI":   ("MEMORIAL PILLAR, once", "both", "A wish at a memorial, never remarked on"),
    "SPECIES_REGIROCK":  ("SEVAULT CANYON, behind a sealed door", "CONTENT", "LEGACY leans CONTENT"),
    "SPECIES_REGICE":    ("ICEFALL CAVE, the back room", "both", "FROZEN has no lean"),
    "SPECIES_REGISTEEL": ("RUBY PATH, the lowest floor", "both", "HARDENED has no lean"),
    "SPECIES_LATIOS":    ("Roams the islands", "CONTENT", "One of the pair per edition, so the pair needs a trade"),
    "SPECIES_LATIAS":    ("Roams the islands", "CONTEXT", "The other one"),
    "SPECIES_GROUDON":   ("MT. SMOULDER, the deepest chamber", "CONTENT", "STRATUM leans CONTENT"),
    "SPECIES_KYOGRE":    ("OUTCAST ISLAND, the sea cave", "CONTEXT", "FLOW has no lean; the pair splits so each edition has one"),
    "SPECIES_RAYQUAZA":  ("SEVAULT CANYON, the top, post-game", "both", "EMERGENT and VECTOR lean opposite ways"),
    "SPECIES_DEOXYS":    ("THE ANNEX, after Crystal reads the package", "both", "Already there; the ferry opens once 4.34 is done"),
}


def load():
    names = dict(re.findall(r'\[(SPECIES_\w+)\]\s*=\s*_\("([^"]*)"', open(os.path.join(GBA, "src/data/text/species_names.h")).read()))
    num = {k: int(v) for k, v in re.findall(r"#define (SPECIES_\w+)\s+(\d+)", open(os.path.join(GBA, "include/constants/species.h")).read())}
    types = {}
    info = open(os.path.join(GBA, "src/data/pokemon/species_info.h")).read()
    for m in re.finditer(r"\[(SPECIES_\w+)\]\s*=\s*\{(.*?)\n    \},", info, re.S):
        t = re.search(r"\.types = \{(\w+), (\w+)\}", m.group(2))
        if t:
            types[m.group(1)] = [t.group(1)] if t.group(1) == t.group(2) else [t.group(1), t.group(2)]
    evo, parent = {}, {}
    for m in re.finditer(r"\[(SPECIES_\w+)\]\s*=\s*\{(.*?)\},\s*\n", open(os.path.join(GBA, "src/data/pokemon/evolution.h")).read()):
        for method, param, target in re.findall(r"\{(EVO_\w+),\s*(\w+),\s*(SPECIES_\w+)\}", m.group(2)):
            evo.setdefault(m.group(1), []).append((method, param, target))
            parent.setdefault(target, (m.group(1), method, param))
    maps = {}
    for f in __import__("glob").glob(os.path.join(GBA, "data/maps/*/map.json")):
        j = json.load(open(f))
        maps[j.get("id")] = j.get("region_map_section")
    secs = {s["id"]: s.get("name", s["id"]) for s in json.load(open(os.path.join(GBA, "src/data/region_map/region_map_sections.json")))["map_sections"]}
    wild = json.load(open(os.path.join(GBA, "src/data/wild_encounters.json")))
    return names, num, types, evo, parent, maps, secs, wild


def main():
    names, num, types, evo, parent, maps, secs, wild = load()

    def root(s):
        while s in parent:
            s = parent[s][0]
        return s

    def stage(s):
        n = 0
        while s in parent:
            s = parent[s][0]; n += 1
        return n

    # The island tables, one record per (edition, map, kind).
    tables = []
    met_now = {}
    for grp in wild["wild_encounter_groups"]:
        for enc in grp["encounters"]:
            mp = enc.get("map", "")
            ed = "CONTENT" if "FireRed" in enc.get("base_label", "") else "CONTEXT"
            isl = next((n for k, n in ISLAND if k in mp), None)
            for kind in ROOM:
                mons = (enc.get(kind) or {}).get("mons", [])
                for m in mons:
                    if isl and num.get(m["species"], 0) > 151:
                        met_now.setdefault(m["species"], set()).add((ed, mp, kind))
                if not mons or not isl or any(x in mp for x in NOT_OURS):
                    continue
                hab = next((h for k, h in HABITAT if k in mp), "open")
                sec = maps.get(mp)
                tables.append({"ed": ed, "map": mp, "kind": kind, "island": isl, "tier": 1 if isl <= 3 else 2,
                               "habitat": hab, "place": secs.get(sec, mp), "lo": min(x["min_level"] for x in mons),
                               "hi": max(x["max_level"] for x in mons), "load": 0})

    species = [s for s, n in sorted(num.items(), key=lambda kv: kv[1]) if 152 <= n <= 411 and "OLD_UNOWN" not in s]
    family = {}
    for s in species:
        family.setdefault(root(s), []).append(s)

    def edition(fam_root):
        members = [fam_root] + [s for s in species if root(s) == fam_root]
        ts = {t for s in members for t in types.get(s, [])}
        c, x = bool(ts & LEAN["CONTENT"]), bool(ts & LEAN["CONTEXT"])
        return "CONTENT" if c and not x else "CONTEXT" if x and not c else "both"

    rows = []
    for s in sorted(species, key=lambda s: (stage(s), num[s])):
        base = {"num": num[s], "id": s, "name": names.get(s, s), "types": [TYPE_NAME.get(t, t) for t in types.get(s, [])],
                "family": names.get(root(s), root(s)), "stage": stage(s)}
        if s in FIXED:
            where, ed, why = FIXED[s]
            rows.append({**base, "status": "fixed", "edition": ed, "place": where, "kind": "fixed encounter", "levels": "", "note": why})
            continue
        if s in met_now:
            eds = sorted({e for e, _, _ in met_now[s]})
            places = sorted({secs.get(maps.get(m), m) for _, m, _ in met_now[s]})
            rows.append({**base, "status": "already", "edition": "both" if len(eds) == 2 else eds[0], "place": ", ".join(places),
                         "kind": ", ".join(sorted({k.replace("_mons", "").replace("_", " ") for _, _, k in met_now[s]})), "levels": "", "note": "Met here today; kept"})
            continue
        ed = edition(root(s))
        ts = types.get(s, ["TYPE_NORMAL"])
        kinds = ["water_mons", "fishing_mons"] if "TYPE_WATER" in ts else ["land_mons", "rock_smash_mons"]
        habs = [] if "TYPE_WATER" in ts else [h for t in ts for h in PREF.get(t, ["open"])] + ["open"]
        want_tier = 1 if stage(s) == 0 else 2
        eds = ["CONTENT", "CONTEXT"] if ed == "both" else [ed]
        evo_lv = int(parent[s][2]) if s in parent and parent[s][1] == "EVO_LEVEL" else 0
        best = None
        for kind in kinds:
            for h in (habs or [None]):
                cands = [t for t in tables if t["ed"] == eds[0] and t["kind"] == kind and (h is None or t["habitat"] == h)
                         and t["load"] < ROOM[kind]]
                if not cands:
                    continue
                cands.sort(key=lambda t: (t["tier"] != want_tier, t["load"], t["island"]))
                best = cands[0]
                break
            if best:
                break
        if not best:
            rows.append({**base, "status": "overflow", "edition": ed, "place": "no room", "kind": "", "levels": "", "note": "Every matching table is full"})
            continue
        for e in eds:
            for t in tables:
                if t["ed"] == e and t["map"] == best["map"] and t["kind"] == best["kind"]:
                    t["load"] += 1
        lo = max(best["lo"], evo_lv)
        hi = max(best["hi"], lo + 3)
        note = ("Evolves at %d" % evo_lv) if evo_lv else ("Evolves by %s" % parent[s][1].replace("EVO_", "").replace("_", " ").lower() if s in parent else "First form")
        rows.append({**base, "status": "new", "edition": ed, "place": "%s · island %d" % (best["place"], best["island"]),
                     "map": best["map"], "kind": best["kind"].replace("_mons", "").replace("_", " "), "levels": "%d–%d" % (lo, hi), "note": note})

    rows.sort(key=lambda r: r["num"])
    count = lambda **kw: sum(1 for r in rows if all(r.get(k) == v for k, v in kw.items()))
    summary = {
        "species": len(rows), "already": count(status="already"), "new": count(status="new"),
        "fixed": count(status="fixed"), "overflow": count(status="overflow"),
        "content_only": count(edition="CONTENT"), "context_only": count(edition="CONTEXT"), "both": count(edition="both"),
        "named": sum(1 for r in rows if r["name"] != r["id"].replace("SPECIES_", "").replace("_", " ")),
        "families": len(family),
    }
    print("  %(species)d species past 151: %(already)d already met, %(new)d placed, %(fixed)d fixed, %(overflow)d with no room" % summary)
    print("  edition: %(content_only)d CONTENT only, %(context_only)d CONTEXT only, %(both)d in both" % summary)
    if "--html" in sys.argv:
        out = sys.argv[sys.argv.index("--html") + 1]
        open(out, "w").write(page(rows, summary))
        print("  review page", out)


def page(rows, summary):
    data = json.dumps({"rows": rows, "summary": summary})
    return TEMPLATE.replace("__DATA__", data.replace("</", "<\\/"))


TEMPLATE = r"""<title>Island Census</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Chivo:wght@500;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{
  --ground:#eef2f1; --panel:#ffffff; --ink:#15211f; --muted:#56655f; --rule:#d3dcd9;
  --sea:#0e6b66; --sea-soft:#d8ebe8; --content:#8c6a33; --content-soft:#f1e7d3;
  --context:#a3316f; --context-soft:#f5dfeb; --both:#3e5a55; --both-soft:#e1e9e7;
  --warn:#a14a17; --warn-soft:#f6e2d4;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
  --ground:#0e1615; --panel:#152120; --ink:#dfe8e5; --muted:#93a39e; --rule:#28383a;
  --sea:#58b8ae; --sea-soft:#17332f; --content:#d2ad6b; --content-soft:#2f271a;
  --context:#e67ab3; --context-soft:#361c2a; --both:#9fbcb6; --both-soft:#1d2b29;
  --warn:#e59566; --warn-soft:#35231a;
}}
:root[data-theme="dark"]{
  --ground:#0e1615; --panel:#152120; --ink:#dfe8e5; --muted:#93a39e; --rule:#28383a;
  --sea:#58b8ae; --sea-soft:#17332f; --content:#d2ad6b; --content-soft:#2f271a;
  --context:#e67ab3; --context-soft:#361c2a; --both:#9fbcb6; --both-soft:#1d2b29;
  --warn:#e59566; --warn-soft:#35231a;
}
*{box-sizing:border-box}
body{background:var(--ground);color:var(--ink);font:15px/1.55 "IBM Plex Sans",system-ui,sans-serif;margin:0;padding-inline:20px;padding-block:28px 60px}
.wrap{max-width:1180px;margin:0 auto;display:grid;gap:28px}
h1,h2{font-family:Chivo,"IBM Plex Sans",sans-serif;text-wrap:balance;margin:0}
h1{font-size:34px;letter-spacing:-.01em}
h2{font-size:19px}
.lede{max-width:68ch;color:var(--muted);margin:6px 0 0}
.eyebrow{font:500 11px/1 "IBM Plex Mono",monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--sea)}
.tally{display:flex;flex-wrap:wrap;gap:0;border-block:1px solid var(--rule)}
.tally div{padding:14px 22px 14px 0;margin-right:22px;border-right:1px solid var(--rule)}
.tally div:last-child{border-right:0}
.tally b{display:block;font:500 26px/1.1 "IBM Plex Mono",monospace;font-variant-numeric:tabular-nums}
.tally span{font-size:12px;color:var(--muted)}
.rules{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px 26px}
.rules p{margin:0;max-width:60ch}
.rules strong{display:block;font:500 11px/1.6 "IBM Plex Mono",monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.controls{display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.seg{display:inline-flex;border:1px solid var(--rule);border-radius:6px;overflow:hidden;background:var(--panel)}
.seg button{font:500 13px "IBM Plex Sans",sans-serif;border:0;background:transparent;color:var(--ink);padding:8px 14px;cursor:pointer}
.seg button+button{border-left:1px solid var(--rule)}
.seg button[aria-pressed="true"]{background:var(--sea);color:var(--panel)}
input[type=search]{font:14px "IBM Plex Sans",sans-serif;padding:8px 12px;border:1px solid var(--rule);border-radius:6px;background:var(--panel);color:var(--ink);min-width:0;flex:1 1 220px;max-width:320px}
button:focus-visible,input:focus-visible{outline:2px solid var(--sea);outline-offset:2px}
.count{font:13px "IBM Plex Mono",monospace;color:var(--muted)}
.table{overflow-x:auto;background:var(--panel);border:1px solid var(--rule);border-radius:8px}
table{border-collapse:collapse;width:100%;min-width:900px;font-size:14px}
th{font:500 11px "IBM Plex Mono",monospace;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);text-align:left;padding:10px 12px;border-bottom:1px solid var(--rule);position:sticky;top:0;background:var(--panel)}
td{padding:9px 12px;border-bottom:1px solid var(--rule);vertical-align:top}
tr:last-child td{border-bottom:0}
td.num{font:13px "IBM Plex Mono",monospace;color:var(--muted);font-variant-numeric:tabular-nums;width:48px}
td.name{font-weight:600}
td.name small{display:block;font-weight:400;color:var(--muted);font-size:12px}
.mono{font-family:"IBM Plex Mono",monospace;font-size:13px}
.chip{display:inline-block;font:500 11px/1 "IBM Plex Mono",monospace;letter-spacing:.06em;padding:4px 7px;border-radius:4px;white-space:nowrap}
.ed-CONTENT{color:var(--content);background:var(--content-soft)}
.ed-CONTEXT{color:var(--context);background:var(--context-soft)}
.ed-both{color:var(--both);background:var(--both-soft)}
.st{font:500 11px "IBM Plex Mono",monospace;text-transform:uppercase;letter-spacing:.08em}
.st-new{color:var(--sea)} .st-already{color:var(--muted)} .st-fixed{color:var(--context)} .st-overflow{color:var(--warn)}
.types{color:var(--muted);font-size:12px}
.open{display:grid;gap:10px;max-width:78ch}
.open li{margin-bottom:6px}
.note{color:var(--muted);font-size:13px}
footer{color:var(--muted);font-size:13px;border-top:1px solid var(--rule);padding-top:14px}
@media (max-width:640px){h1{font-size:27px}.tally div{padding-right:14px;margin-right:14px}}
</style>
<div class="wrap">
  <header>
    <div class="eyebrow">CONTEXT / CONTENT · GLOBAL INDEX · a proposal, not yet in the game</div>
    <h1>Island Census</h1>
    <p class="lede">Where every daemon numbered past #151 would be met in the seven islands, and in which edition. Derived by <span class="mono">tools/plan_global_index.py</span> from the game's own tables — every row follows from a rule below, and each rule is one line to change.</p>
  </header>
  <section class="tally" id="tally"></section>
  <section class="rules">
    <p><strong>Edition</strong>Tier 2's lean. A family whose types lean only toward CONTENT (CONTENT · LOGIC · STRATUM · LEGACY) or only toward CONTEXT (CONTEXT · LATENT · VECTOR · ENTROPY) is that edition's; anything else is met in both.</p>
    <p><strong>Habitat</strong>FLOW in the water and on the rod, FROZEN in ICEFALL CAVE, LATENT and OPAQUE in the LOST CAVE, STRATUM · LEGACY · HARDENED in the RUBY PATH and SEVAULT CANYON, ENTROPY on the mountain, GROWTH · SWARM · CORRUPT in the forests, CONTEXT at the ruins.</p>
    <p><strong>Stage and level</strong>A family's first form on islands 1–3, later forms on 4–7, and never below the level it evolves at, so each form of a line is also found wild.</p>
    <p><strong>Kept and fixed</strong>The daemons already met on the islands keep their places. The sixteen legendaries are fixed encounters, and those placements are design proposals, not derivation.</p>
  </section>
  <section>
    <div class="controls">
      <div class="seg" role="group" aria-label="Edition">
        <button type="button" id="ed-all" aria-pressed="true" data-ed="all">All</button>
        <button type="button" id="ed-content" aria-pressed="false" data-ed="CONTENT">CONTENT</button>
        <button type="button" id="ed-context" aria-pressed="false" data-ed="CONTEXT">CONTEXT</button>
      </div>
      <div class="seg" role="group" aria-label="Status">
        <button type="button" id="st-all" aria-pressed="true" data-st="all">Everything</button>
        <button type="button" id="st-new" aria-pressed="false" data-st="new">Placed</button>
        <button type="button" id="st-fixed" aria-pressed="false" data-st="fixed">Fixed</button>
        <button type="button" id="st-already" aria-pressed="false" data-st="already">Already met</button>
      </div>
      <input type="search" id="q" placeholder="Search a name, type or place" aria-label="Search">
      <span class="count" id="count"></span>
    </div>
  </section>
  <section class="table">
    <table>
      <thead><tr><th>#</th><th>Daemon</th><th>Edition</th><th>Where</th><th>Slot</th><th>Levels</th><th>Status</th><th>Why</th></tr></thead>
      <tbody id="rows"></tbody>
    </table>
  </section>
  <section>
    <h2>What this does not settle</h2>
    <ul class="open">
      <li><b>Names.</b> Section 2.10 gives a name to every daemon the player can meet, and 8.2b holds the islands' names back. Making all of these meetable means naming about <span id="unnamed"></span> more, in the islands' register: named for mind, where Kanto's are named for machinery.</li>
      <li><b>The legendaries' places</b> are proposals. LUGIA and HO-OH need NAVEL ROCK opened the way THE ANNEX was; the roamers need the engine's one-roamer limit looked at.</li>
      <li><b>How many daemons a table holds.</b> Each table takes at most a set number of new daemons (land 8, water 4, rod 5, rock 3), so a crowded habitat spills into the next island rather than failing.</li>
      <li><b>Time.</b> If day, night and seasons land (proposed in 9.21), some of these move into time-specific tables instead.</li>
    </ul>
  </section>
  <footer>Generated from <span class="mono">wild_encounters.json</span>, <span class="mono">species_info.h</span> and <span class="mono">evolution.h</span>. Nothing on this page has been written to the ROM.</footer>
</div>
<script>
const DATA = __DATA__;
const S = DATA.summary;
const tally = [["Past #151", S.species], ["Met today", S.already], ["Placed", S.new], ["Fixed", S.fixed], ["CONTENT only", S.content_only], ["CONTEXT only", S.context_only], ["In both", S.both]];
if (S.overflow) tally.push(["No room", S.overflow]);
document.getElementById("tally").innerHTML = tally.map(([k, v]) => `<div><b>${v}</b><span>${k}</span></div>`).join("");
document.getElementById("unnamed").textContent = S.species - S.named;
let ed = "all", st = "all", q = "";
const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;"}[c]));
function render(){
  const needle = q.trim().toLowerCase();
  const rows = DATA.rows.filter(r =>
    (ed === "all" || r.edition === ed || r.edition === "both") &&
    (st === "all" || r.status === st) &&
    (!needle || [r.name, r.family, r.place, r.types.join(" "), r.note].join(" ").toLowerCase().includes(needle)));
  document.getElementById("rows").innerHTML = rows.map(r => `<tr>
    <td class="num">${r.num}</td>
    <td class="name">${esc(r.name)}<small class="types">${esc(r.types.join(" · "))}${r.stage ? " · from " + esc(r.family) : ""}</small></td>
    <td><span class="chip ed-${r.edition}">${r.edition === "both" ? "BOTH" : r.edition}</span></td>
    <td>${esc(r.place)}</td>
    <td class="mono">${esc(r.kind)}</td>
    <td class="mono">${esc(r.levels)}</td>
    <td><span class="st st-${r.status}">${r.status === "new" ? "placed" : r.status}</span></td>
    <td class="note">${esc(r.note)}</td></tr>`).join("");
  document.getElementById("count").textContent = `${rows.length} of ${DATA.rows.length}`;
}
document.querySelectorAll("[data-ed]").forEach(b => b.addEventListener("click", () => {
  ed = b.dataset.ed; document.querySelectorAll("[data-ed]").forEach(x => x.setAttribute("aria-pressed", x === b)); render(); }));
document.querySelectorAll("[data-st]").forEach(b => b.addEventListener("click", () => {
  st = b.dataset.st; document.querySelectorAll("[data-st]").forEach(x => x.setAttribute("aria-pressed", x === b)); render(); }));
document.getElementById("q").addEventListener("input", e => { q = e.target.value; render(); });
render();
</script>
"""

main()
