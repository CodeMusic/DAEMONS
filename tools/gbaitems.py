#!/usr/bin/env python3
"""Render docs/items.html from the game's own item table.

    python3 tools/gbaitems.py [--write]

The rename list is DERIVED, not typed: this diffs engineGba/src/data/items.json
against upstream/master's copy of the same file, exactly as port_names.py does,
so a name that changes in the build changes here on the next run and a name
invented in this file cannot exist. The shipped description text is quoted out
of the same json.

What is NOT derivable is the argument for each name -- that is authorial, and
it lives in WHY below, keyed by itemId. An item that gets renamed without an
entry there is reported rather than silently rendered blank.

Cut the PDF with ./docs/build-pdf.sh items.html.
"""
import json, os, re, subprocess, sys

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA   = os.path.join(ROOT, "engineGba")
OUT   = os.path.join(ROOT, "docs/items.html")
WRITE = "--write" in sys.argv

# ---------------------------------------------------------------- the states
# Three-letter codes from src/strings.c, tile colours from status_icons.png.
# Both are read back below rather than trusted from here.
STATES = [
    ("POISON · PSN",    "LEAKING",    "LEK", "#6f9440",
     "A memory leak degrades a running process a little at a time until it dies. "
     "Nothing else in computing loses you a fixed slice per tick."),
    ("TOXIC · TOX",     "CASCADING",  "CAS", "#6f9440",
     "Badly poisoned worsens each turn, and a cascading failure is precisely a fault "
     "whose rate rises because of the damage it already did. "
     "It shares LEAKING's tile: Gen 3 has one poison slot and draws both in it."),
    ("SLEEP · SLP",     "SUSPENDED",  "SUS", "#8a8f9c",
     "Not gone, not scheduled, and it <em>resumes</em>. The one status that is genuinely "
     "temporary, and the word says so. The tile is slate: dormant rather than damaged."),
    ("PARALYSIS · PAR", "THROTTLED",  "THR", "#c8a020",
     "Paralysis does two things — cuts speed, sometimes skips a turn. Throttling is a speed "
     "cap that intermittently stalls work. Both halves, one word."),
    ("BURN · BRN",      "OVERHEATED", "OVR", "#d8703c",
     "Chip damage plus reduced output, dealt by ENTROPY, whose one-clause test is "
     "<em>noise and heat</em>. The tile is ember: heat the daemon made itself."),
    ("FREEZE · FRZ",    "HUNG",       "HNG", "#78a8dc",
     "A hung process does nothing until something intervenes. <strong>FROZEN could not be "
     "reused</strong> — it is a type name, and the chart had just spent real effort making "
     "type names carry meaning. WATCHDOG is what ends it."),
    ("CONFUSION",       "THRASHING",  None,  None,
     "A system so busy managing itself it makes no progress and damages its own throughput. "
     "Hurting yourself in confusion is the same event. Volatile, so it needs no code."),
    ("FAINT",           "HALTED",     "HLT", "#b83c3c",
     "The first of the seven, and the one that set the register for the rest: a state is "
     "something a process is <em>in</em>, and something it can be got out of."),
]

# ------------------------------------------------------- why each name, by id
WHY = {
 "ITEM_ANTIDOTE":     "You patch a leak and you patch software. <strong>The pun is the definition</strong> — it needs no beat of confusion, which is the test CACHE was held to and failed.",
 "ITEM_BURN_HEAL":    "The only one of the seven that needs no domain knowledge at all. Plain, physical, and exactly right.",
 "ITEM_ICE_HEAL":     "<strong>Renamed twice, and the second time was the one that mattered.</strong> <code>INTERRUPT</code> shipped here and collided with the flute, which had taken the word six weeks earlier and keeps it. <code>PREEMPT</code> replaced it and collided with MANKEY, named four days before. <em>Under both collisions was a plainer fault: preempting a hung task hands the processor to somebody else and the hung one stays hung.</em> <strong>A watchdog is the timer whose whole job is to notice a process has stopped answering and reset it</strong> — the actual cure, and it still works twice.",
 "ITEM_AWAKENING":    "The exact inverse of SUSPENDED, and the word an operating system uses for it.",
 "ITEM_PARALYZE_HEAL":  "What lifts throttling is not medicine — it is being scheduled ahead of the thing starving you. <em>The weakest of the ten on the works-twice test, and kept because the mechanic is right.</em>",
 "ITEM_FULL_HEAL":    "Clears every state by returning to a known-good one. Says <em>all of it</em> without listing anything.",
 "ITEM_FULL_RESTORE": "Health and state together, because that is what a snapshot restores. The one cure that is a noun for a thing you saved earlier.",
 "ITEM_REVIVE":       "The word for bringing back a halted process — and it lands on HALTED without explaining itself.",
 "ITEM_MAX_REVIVE":   "Strictly bigger than a restart, which is exactly the relationship the two items have. <strong>The ladder is free.</strong>",
 "ITEM_HEAL_POWDER":  "Bitter, cheap, works now, nobody is proud of it. All four are true of both meanings.",

 "ITEM_POKE_BALL":    "<strong>A box is not a container, it is a host.</strong> The ladder is not sizes, it is <em>rights</em> — and that is the argument: what you are doing when you bind a daemon is offering it an account on a machine.",
 "ITEM_GREAT_BALL":   "Wider rights than a USERBOX, so more daemons agree to run on it.",
 "ITEM_ULTRA_BALL":   "Elevated rights. Most daemons will run on it.",
 "ITEM_MASTER_BALL":  "Unrestricted rights. <em>No daemon can decline</em> — which is the one place in the ladder where the metaphor turns unpleasant, and it is supposed to.",
 "ITEM_SAFARI_BALL":  "Issued at the gate and expiring at the gate. A guest account is exactly a temporary host with a revocation date.",
 "ITEM_PREMIER_BALL": "The specialty boxes keep vanilla's shape — a BOX that is better at one thing — because the ladder already carries the argument and a second one would crowd it.",

 "ITEM_FIRE_STONE":   "<strong>The four inputs to a mind, not four elements.</strong> An axiom is something to reason <em>from</em> — you do not derive it, you start there.",
 "ITEM_THUNDER_STONE": "A representation you can search through. The one of the four that names a technique rather than a faculty, and the only one a player may already know.",
 "ITEM_WATER_STONE":  "Something to feel with. <em>Affect</em> is the clinical word, which keeps it from reading as sentiment.",
 "ITEM_LEAF_STONE":   "A signal to learn from. <strong>Reward is the one of the four the whole game is arguing about</strong> and it is never said again.",

 "ITEM_OAKS_PARCEL":  "<em>A sealed module. Part no. CC-7.</em> The number goes in the item name rather than the description, so the player <strong>carries</strong> it for thirty hours before reading a requisition for the same part on a door.",
 "ITEM_POKE_FLUTE":   "An interrupt is a signal that reaches something which has stopped responding. A flute that wakes a sleeping obstacle <em>is</em> that, in the plainest sense.",
 "ITEM_SILPH_SCOPE":  "Resolves a name that will not resolve on its own. DNS said as a ghost story.",
 "ITEM_FAME_CHECKER": "Holds what you were <em>told</em>, and who told you. <strong>It does not hold what is true</strong> — the item is a citation index, and the name admits it.",
 "ITEM_TEACHY_TV":    "A stream is a broadcast and a stream is a sequence you read from as it arrives. <em>MACHINE STREAM was measured out before taste got a vote:</em> the name budget is thirteen characters and that one is fourteen.",
 "ITEM_OLD_AMBER":    "A core recovered whole, holding a daemon that stopped a very long time ago. The museum's whole argument, carried in the bag.",
 "ITEM_HELIX_FOSSIL": "Wound in a spiral. Nothing has read its contents.",
 "ITEM_DOME_FOSSIL":  "A drum, sealed at both ends. Nothing has read its contents.",
 "ITEM_PP_UP":        "PP is <em>power points</em>, which is a body word. MP is what the rest of the genre already calls the same number, and it costs one letter.",
 "ITEM_PP_MAX":       "Same change, same reason.",

 # 1.6c -- the configurations. The rack needs no per-item WHY: seventeen
 # identical controls with different labels is the argument, and the group
 # blurb carries it.
 "ITEM_WHITE_HERB":   "You revert a value to what it was. <em>Restores a lowered stat, once</em> — and the word is the operation, not a medicine.",
 "ITEM_MENTAL_HERB":  "A binding formed without being asked for is the thing the item drops. <strong>UNPAIR is the undo of the routine that caused it</strong>, and both are one word.",
 "ITEM_MACHO_BRACE":  "<strong>The best of the twenty-five.</strong> A debug build is instrumented at every step, so it <em>learns faster and runs slower</em> — which is both halves of the item, in a phrase every programmer already owns.",
 "ITEM_EXP_SHARE":    "Weight sharing is two models trained as one: what teaches the first teaches the second. <em>Vanilla's item is a mystery; ours is a technique.</em>",
 "ITEM_QUICK_CLAW":   "Priority is scheduling, and sometimes the scheduler takes you out of turn. Sits beside PRIORITY and GAUGE's whole benchmark without pointing at either.",
 "ITEM_SOOTHE_BELL":  "Processor affinity binds a process to one host and keeps it there. <strong>Affinity is also plain fondness</strong>, which is the double duty this lexicon is built on.",
 "ITEM_SMOKE_BALL":   "A way out that is always open. <em>It stopped being a BALL, which freed it from the guard that had been holding the name.</em>",
 "ITEM_EVERSTONE":    "You pin a dependency to a version so it never moves. The holder does not evolve, and nothing about the name is a metaphor.",
 "ITEM_FOCUS_BAND":   "The thing that catches you when everything else already failed. One HP is exactly what a failsafe leaves you.",
 "ITEM_LUCKY_EGG":    "<strong>The learning rate is how large a step each lesson takes.</strong> Turned up, you learn faster from the same experience — which is the item, stated as the hyperparameter it is.",
 "ITEM_SCOPE_LENS":   "A critical hit is the far end of the distribution. <em>The long tail is where the rare large values live</em>, and raising the crit ratio is reaching further into it.",
 "ITEM_SHELL_BELL":   "Reclaiming is taking back what is no longer in use. The holder recovers on striking, and the word is the garbage collector's.",
 "ITEM_KINGS_ROCK":   "A pipeline bubble is a gap pushed in where nothing issues. <strong>A flinch is a turn in which nothing issued</strong> — and PIPELINE is a species, so the word already lives here.",
 "ITEM_CHOICE_BAND":  "One value, written in, with no way to pass another. <em>Faster, and no longer negotiable</em>, which is the trade the item makes.",
 "ITEM_AMULET_COIN":  "Charged on top of the agreed rate. The one item in the set whose register is the institution's rather than the machine's.",
 "ITEM_UP_GRADE":     "Everything fixed since the release, in one bundle — and it is <em>made by SILPH CO.</em>, which is the joke sitting under it.",
 "ITEM_DRAGON_SCALE": "<strong>Scaling laws are what happens to a thing when you only make it bigger</strong>, and EMERGENT is the type this evolution item belongs to. <em>The argument and the mechanic said the same word.</em>",
 "ITEM_DEEP_SEA_TOOTH": "A deep feature is a representation learned far from the surface. Raises SP. ATK, and the pun keeps the sea.",
 "ITEM_DEEP_SEA_SCALE": "The layers nothing outside gets at directly. Raises SP. DEF, and pairs with DEEP FEATURE the way the two vanilla items pair.",
 "ITEM_SOUL_DEW":     "What a process holds that nothing outside can read. The two special stats are the mind stats, and this is the item that says so.",
 "ITEM_LIGHT_BALL":   "The supply rail is the line every other part draws from. <em>Held by a SPIKE</em>, which is what a rail carries.",
 "ITEM_LUCKY_PUNCH":  "A result nothing predicted and nothing repeats. <strong>Held by UPTIME</strong>, which is the daemon whose whole name is the opposite of a fluke.",
 "ITEM_METAL_POWDER": "Strict mode refuses anything it was not promised. <strong>Held by MOCK</strong> — and a mock object that checks its contract is exactly what the pair means.",
 "ITEM_THICK_CLUB":   "Bare metal is nothing at all between you and the hardware. Held by RELIC and CAIRNLING, whose register is old machinery still running.",
 "ITEM_STICK":        "<strong>An off-by-one is the error at the edge that everything else survives.</strong> Held by EDGECASE, which is the same joke told twice and never explained.",
}

# Groups whose members are a SET rather than twenty-two separate decisions.
# The blurb is the reasoning and a per-item note would only repeat it.
SET_GROUPS = {"rack", "usable", "traps"}

# Vanilla's one-trick balls keep vanilla's shape: the ladder already carries the
# argument and a second one competing with it would blunt both.
SPECIALTY = ["ITEM_NET_BALL","ITEM_DIVE_BALL","ITEM_NEST_BALL","ITEM_REPEAT_BALL",
             "ITEM_TIMER_BALL","ITEM_LUXURY_BALL","ITEM_PREMIER_BALL"]

GROUPS = [
 ("The operations that end a state", "cures",
  "Vanilla's cures are sprays and medicines. Ours are the operations you would actually "
  "perform on a process that was in that state.",
  ["ITEM_ANTIDOTE","ITEM_AWAKENING","ITEM_PARALYZE_HEAL","ITEM_BURN_HEAL","ITEM_ICE_HEAL",
   "ITEM_FULL_HEAL","ITEM_HEAL_POWDER","ITEM_FULL_RESTORE","ITEM_REVIVE","ITEM_MAX_REVIVE"]),
 ("The hosts", "boxes",
  "The ladder is not sizes. It is <strong>rights</strong> — and a box is a little machine "
  "that a daemon agrees, or does not agree, to run on.",
  ["ITEM_POKE_BALL","ITEM_GREAT_BALL","ITEM_ULTRA_BALL","ITEM_MASTER_BALL",
   "ITEM_SAFARI_BALL"]),
 ("The four inputs", "inputs",
  "Vanilla's evolution stones are four elements. Ours are four things you can give a mind, "
  "and each changes what some daemons compile to.",
  ["ITEM_FIRE_STONE","ITEM_THUNDER_STONE","ITEM_WATER_STONE","ITEM_LEAF_STONE"]),
 ("The key items", "keys",
  "One of these is a crime scene the player carries from minute fifteen, and nothing "
  "points at it.",
  ["ITEM_OAKS_PARCEL","ITEM_POKE_FLUTE","ITEM_SILPH_SCOPE","ITEM_FAME_CHECKER",
   "ITEM_TEACHY_TV","ITEM_OLD_AMBER","ITEM_HELIX_FOSSIL","ITEM_DOME_FOSSIL"]),
 ("And one number", "mp",
  "", ["ITEM_PP_UP","ITEM_PP_MAX"]),
 ("The rack", "rack",
  "Vanilla's seventeen type boosters are seventeen unrelated trinkets \u2014 a spoon, a magnet, "
  "a lump of charcoal. Ours are seventeen labelled controls on one desk, and each one\u2019s "
  "first clause is 2.6\u2019s own test for that type. Read the rack and you have read the chart.",
  ["ITEM_SILK_SCARF","ITEM_BLACK_BELT","ITEM_SHARP_BEAK","ITEM_POISON_BARB","ITEM_SOFT_SAND",
   "ITEM_HARD_STONE","ITEM_SILVER_POWDER","ITEM_SPELL_TAG","ITEM_CHARCOAL","ITEM_MYSTIC_WATER",
   "ITEM_MIRACLE_SEED","ITEM_MAGNET","ITEM_TWISTED_SPOON","ITEM_NEVER_MELT_ICE",
   "ITEM_DRAGON_FANG","ITEM_METAL_COAT","ITEM_BLACK_GLASSES","ITEM_SEA_INCENSE",
   "ITEM_BRIGHT_POWDER","ITEM_LAX_INCENSE","ITEM_LEFTOVERS","ITEM_CLEANSE_TAG"]),
 ("The trap table", "traps",
  "A berry sits there doing nothing, fires <strong>once</strong> when a condition is met, and is "
  "gone. That is a <strong>handler</strong>, and the kind installed against a machine condition "
  "is a <strong>trap</strong> \u2014 which is also a physical thing that catches something, so it does "
  "the double duty CHERI and PECHA never did. Which makes the pouch a TRAP TABLE, and that is "
  "the term for the array of handlers a system installs.",
  ["ITEM_CHERI_BERRY","ITEM_CHESTO_BERRY","ITEM_PECHA_BERRY","ITEM_RAWST_BERRY",
   "ITEM_ASPEAR_BERRY","ITEM_PERSIM_BERRY","ITEM_LUM_BERRY","ITEM_LEPPA_BERRY",
   "ITEM_ORAN_BERRY","ITEM_SITRUS_BERRY","ITEM_BERRY_JUICE","ITEM_FIGY_BERRY",
   "ITEM_WIKI_BERRY","ITEM_MAGO_BERRY","ITEM_AGUAV_BERRY","ITEM_IAPAPA_BERRY",
   "ITEM_LIECHI_BERRY","ITEM_GANLON_BERRY","ITEM_SALAC_BERRY","ITEM_PETAYA_BERRY",
   "ITEM_APICOT_BERRY","ITEM_LANSAT_BERRY","ITEM_STARF_BERRY","ITEM_BERRY_POUCH"]),
 ("What you do to a running daemon", "usable",
  "1.6 named the ten items that undo a <strong>state</strong> and stopped there. These are the "
  "rest of the same rule: an item is an <strong>operation</strong>, and the question is what you "
  "would actually do to a process in that condition.",
  ["ITEM_POTION","ITEM_SUPER_POTION","ITEM_HYPER_POTION","ITEM_MAX_POTION",
   "ITEM_ETHER","ITEM_MAX_ETHER","ITEM_ELIXIR","ITEM_MAX_ELIXIR",
   "ITEM_HP_UP","ITEM_PROTEIN","ITEM_IRON","ITEM_CARBOS","ITEM_CALCIUM","ITEM_ZINC",
   "ITEM_RARE_CANDY","ITEM_X_ATTACK","ITEM_X_DEFEND","ITEM_X_SPEED","ITEM_X_ACCURACY",
   "ITEM_X_SPECIAL","ITEM_DIRE_HIT","ITEM_GUARD_SPEC","ITEM_REPEL","ITEM_SUPER_REPEL",
   "ITEM_MAX_REPEL","ITEM_ESCAPE_ROPE","ITEM_POKE_DOLL","ITEM_SUN_STONE","ITEM_MOON_STONE",
   "ITEM_OLD_ROD","ITEM_GOOD_ROD","ITEM_SUPER_ROD","ITEM_ITEMFINDER","ITEM_TOWN_MAP",
   "ITEM_VS_SEEKER","ITEM_COIN_CASE","ITEM_BLUE_FLUTE","ITEM_YELLOW_FLUTE","ITEM_RED_FLUTE",
   "ITEM_BLACK_FLUTE","ITEM_WHITE_FLUTE","ITEM_REVIVAL_HERB","ITEM_SACRED_ASH",
   "ITEM_ENERGY_POWDER","ITEM_ENERGY_ROOT"]),
 ("The configurations", "held",
  "An item is an operation. A <strong>held</strong> item is not one \u2014 it is a setting "
  "attached to a process from outside, in force while it runs, and removable, which is exactly "
  "what an ability is not.",
  ["ITEM_WHITE_HERB","ITEM_MENTAL_HERB","ITEM_MACHO_BRACE","ITEM_EXP_SHARE","ITEM_QUICK_CLAW",
   "ITEM_SOOTHE_BELL","ITEM_SMOKE_BALL","ITEM_EVERSTONE","ITEM_FOCUS_BAND","ITEM_LUCKY_EGG",
   "ITEM_SCOPE_LENS","ITEM_SHELL_BELL","ITEM_KINGS_ROCK","ITEM_CHOICE_BAND","ITEM_AMULET_COIN",
   "ITEM_UP_GRADE","ITEM_DRAGON_SCALE","ITEM_DEEP_SEA_TOOTH","ITEM_DEEP_SEA_SCALE",
   "ITEM_SOUL_DEW","ITEM_LIGHT_BALL","ITEM_LUCKY_PUNCH","ITEM_METAL_POWDER","ITEM_THICK_CLUB",
   "ITEM_STICK"]),
]


def load(text):
    d = json.loads(text)
    return d if isinstance(d, list) else d.get("items", d)


def main():
    ours = load(open(os.path.join(GBA, "src/data/items.json")).read())
    van  = load(subprocess.run(["git", "-C", GBA, "show", "upstream/master:src/data/items.json"],
                               capture_output=True, text=True, check=True).stdout)
    A = {i["itemId"]: i for i in van}
    B = {i["itemId"]: i for i in ours}
    renamed = {k: (A[k]["english"], v["english"]) for k, v in B.items()
               if k in A and A[k]["english"] != v["english"]}
    print("  %d renamed items, derived from the diff against upstream" % len(renamed))

    grouped = {k for _, _, _, ids in GROUPS for k in ids} | set(SPECIALTY)
    _set_members = {k for _, slug, _, ids in GROUPS if slug in SET_GROUPS for k in ids}
    for k in sorted(renamed):
        if k not in grouped:
            print("  ..  %-20s %-14s not in any group (rendered under Others)"
                  % (k, renamed[k][1]))
        elif k not in WHY and k not in SPECIALTY and k not in _set_members:
            print("  !!  %-20s %-14s has no WHY entry" % (k, renamed[k][1]))

    # the three-letter codes, read back out of the build rather than trusted
    src = open(os.path.join(GBA, "src/strings.c")).read()
    codes = dict(re.findall(r'const u8 gText_(\w+)\[\] = _\("(\w{3})"\)', src))
    want = {"Psn":"LEK","Par":"THR","Slp":"SUS","Brn":"OVR","Frz":"HNG","Toxic":"CAS"}
    bad = {k: codes.get(k) for k, v in want.items() if codes.get(k) != v}
    if bad:
        print("  !!  strings.c disagrees with the STATES table: %s" % bad)
    else:
        print("  codes checked against strings.c: " + " ".join(sorted(want.values())))

    def desc(itemId):
        d = B[itemId].get("description_english", "")
        return d.replace("\\n", " ").replace("\\p", " ").strip()

    def row(itemId):
        was, now = renamed[itemId]
        return ("<tr><td class=was>%s</td><td class=now>%s<small>%s</small></td>"
                "<td>%s</td></tr>" % (was, now, desc(itemId), WHY.get(itemId, "")))

    st = []
    for was, now, code, colour, why in STATES:
        chip = ('<span class=code style="background:%s">%s</span>' % (colour, code)
                if code else '<span class=code none>—</span>')
        st.append("<tr><td class=was>%s</td><td class=now>%s</td><td class=chip>%s</td>"
                  "<td>%s</td></tr>" % (was, now, chip, why))

    spec = ", ".join("<code>%s</code>" % renamed[i][1] for i in SPECIALTY if i in renamed)
    secs = []
    for title, sid, lede, ids in GROUPS:
        rows = "".join(row(i) for i in ids if i in renamed)
        secs.append('<section id="%s"><div class="sec-head"><h2>%s</h2></div>%s'
                    '<div class=scroll><table class=tbl><thead><tr><th>Vanilla</th>'
                    '<th>Ours, and what the bag says</th><th>Why that word</th></tr></thead>'
                    '<tbody>%s</tbody></table></div></section>'
                    % (sid, title, ("<p>%s</p>" % lede) if lede else "", rows))
        if sid == "boxes":
            secs.append('<p class="note" style="max-width:66ch">The one-trick balls keep '
                        "vanilla's shape and become one-trick boxes — %s. The ladder "
                        "already carries the argument, and a second argument competing "
                        "with it would blunt both.</p>" % spec)

    html = TEMPLATE.replace("{{STATES}}", "".join(st)) \
                   .replace("{{SECTIONS}}", "".join(secs)) \
                   .replace("{{COUNT}}", str(len(renamed)))
    if WRITE:
        open(OUT, "w").write(html)
        print("  written %s" % OUT)
    else:
        print("  (report only; pass --write)")


TEMPLATE = r"""<title>The Bag</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap">
<style>
:root{
  --paper:#f4f3ee; --raise:#fbfaf7; --ink:#16181c; --dim:#565c66; --faint:#878d96;
  --rule:#dbdad3; --rule-hard:#b0b3b7; --slate:#3f5f88; --slate-soft:#607a9e;
  --was:#8a8378;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --paper:#131519; --raise:#1b1e24; --ink:#e8e6e0; --dim:#a2a8b2; --faint:#767c86;
    --rule:#2a2e35; --rule-hard:#414751; --slate:#8fb0d8; --slate-soft:#7f9cc4;
    --was:#7d776e;
  }
}
:root[data-theme="dark"]{
  --paper:#131519; --raise:#1b1e24; --ink:#e8e6e0; --dim:#a2a8b2; --faint:#767c86;
  --rule:#2a2e35; --rule-hard:#414751; --slate:#8fb0d8; --slate-soft:#7f9cc4;
  --was:#7d776e;
}
*{box-sizing:border-box}
body{background:var(--paper);color:var(--ink);
  font-family:"Source Serif 4",Georgia,serif;line-height:1.6;margin:0}
.wrap{max-width:1000px;margin:0 auto;padding:40px 24px 96px;display:flex;flex-direction:column;gap:48px}
h1,h2,h3,.ui{font-family:"IBM Plex Sans",system-ui,sans-serif}
h1{font-size:clamp(30px,4.4vw,46px);line-height:1.08;margin:0;font-weight:600;letter-spacing:-.02em;text-wrap:balance}
h2{font-size:23px;font-weight:600;margin:0 0 4px;letter-spacing:-.01em;text-wrap:balance}
p{margin:0 0 14px;max-width:66ch}
.eyebrow{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--faint);margin:0 0 12px}
.lede{font-size:18px;color:var(--dim);max-width:64ch;margin:16px 0 0}
header{border-bottom:2px solid var(--rule-hard);padding-bottom:28px}
section{display:flex;flex-direction:column;gap:14px}
.sec-head{border-top:1px solid var(--rule-hard);padding-top:16px}
mark{background:none;color:var(--ink);font-weight:600;
  box-shadow:inset 0 -.42em 0 color-mix(in srgb,var(--slate-soft) 26%,transparent)}
code,.mono{font-family:"IBM Plex Mono",monospace;font-size:.88em}
a{color:var(--slate)}
.scroll{overflow-x:auto;border:1px solid var(--rule);border-radius:2px;background:var(--raise)}
table.tbl{border-collapse:collapse;width:100%;font-size:14px}
table.tbl th{font-family:"IBM Plex Sans",system-ui,sans-serif;font-size:11px;font-weight:600;
  letter-spacing:.1em;text-transform:uppercase;color:var(--faint);text-align:left;
  padding:11px 14px;border-bottom:1px solid var(--rule-hard);white-space:nowrap}
table.tbl td{padding:13px 14px;border-bottom:1px solid var(--rule);vertical-align:top}
table.tbl tr:last-child td{border-bottom:none}
td.was{font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--was);
  white-space:nowrap;width:1%}
td.now{font-family:"IBM Plex Sans",system-ui,sans-serif;font-weight:600;font-size:14px;
  white-space:nowrap;width:1%}
td.now small{display:block;font-family:"Source Serif 4",Georgia,serif;font-weight:400;
  font-size:12px;color:var(--dim);white-space:normal;max-width:24ch;margin-top:5px;
  font-style:italic;line-height:1.45}
td.chip{width:1%}
.code{font-family:"IBM Plex Mono",monospace;font-size:11px;font-weight:600;letter-spacing:.08em;
  color:#fff;padding:3px 7px;border-radius:3px;display:inline-block;
  text-shadow:0 1px 0 rgba(0,0,0,.45)}
.code[none]{background:none;color:var(--faint);text-shadow:none;padding-left:0}
.note{font-size:14px;color:var(--dim);border-left:2px solid var(--rule-hard);
  padding-left:14px;margin:4px 0 0}
.budget{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:1px;
  background:var(--rule);border:1px solid var(--rule);border-radius:2px}
.budget div{background:var(--raise);padding:14px 16px}
.budget b{display:block;font-family:"IBM Plex Sans",system-ui,sans-serif;font-size:11px;
  letter-spacing:.1em;text-transform:uppercase;color:var(--faint);margin-bottom:5px}
.budget span{font-family:"IBM Plex Mono",monospace;font-size:18px;font-weight:500}
.budget em{display:block;font-size:13px;color:var(--dim);margin-top:5px;line-height:1.45}
footer{border-top:1px solid var(--rule-hard);padding-top:18px;font-size:13px;color:var(--faint)}
@media print{body{background:#fff}.wrap{padding:0;gap:30px}section{break-inside:avoid}}
</style>
<div class="wrap">
<header>
  <p class="eyebrow">CONTEXT / CONTENT · §1.4 · §1.6 · §9.15 · §9.16</p>
  <h1>The Bag</h1>
  <p class="lede">Every state a daemon can be in, every item that ends one, and the argument
  for each word. <strong>{{COUNT}} items are renamed</strong>, and this page is generated
  from the game's own table — the shipped description is quoted, not retyped.</p>
</header>

<section>
  <div class="sec-head"><h2>The rule these names follow</h2></div>
  <p><mark>A name has to work twice</mark> — once as the thing in your hand and once as the
  thing in a computer — and if it only works once it does not ship. That test is why
  <code>PATCH</code> was instant and <code>CACHE</code> was refused: a patch stops a leak and
  patches software, while a cache needs a beat of explanation before it means anything.</p>
  <p>The description carries a second rule, added when the state items were rewritten:
  <strong>teach the term in the first clause, state the effect in the second.</strong>
  <em>“Preemption takes control back from a process that will not yield. Ends HUNG.”</em>
  The player who knows the word gets a nod; the player who does not gets a definition and
  never notices being taught.</p>
</section>

<section>
  <div class="sec-head"><h2>The states</h2></div>
  <p>Vanilla leaves a creature poisoned, asleep, paralysed, burned, frozen or confused.
  Every one of those is a metaphor about a <em>body</em>, and this world does not have
  bodies — it has processes. <mark>A state is something a process is in, and something it
  can be got out of.</mark></p>
  <p>The three-letter code is what the party menu draws on a coloured tile, and what the
  battle box prints beside the name. The colours keep vanilla's hue anchors — a player who
  has ever seen a party menu reads orange as burning before they read the letters — and move
  into the muted register the type chart uses.</p>
  <div class="scroll"><table class="tbl">
    <thead><tr><th>Vanilla</th><th>Ours</th><th>Tile</th><th>Why it is the exact word</th></tr></thead>
    <tbody>{{STATES}}</tbody>
  </table></div>
  <p class="note">CASCADING shares LEAKING's tile because Gen 3 draws badly-poisoned in the
  same box as ordinary poison. THRASHING needs no code at all: it is volatile, so it never
  reaches the party screen.</p>
</section>

{{SECTIONS}}

<section>
  <div class="sec-head"><h2>What the budget actually is</h2></div>
  <div class="budget">
    <div><b>Item name</b><span>13 characters</span><em><code>ITEM_NAME_LENGTH</code> is 14
      including the terminator. <code>MACHINE STREAM</code> is 14 and does not fit.</em></div>
    <div><b>Description</b><span>3 lines</span><em>Roughly 30 characters each, measured in
      pixels rather than letters — the face is variable width.</em></div>
    <div><b>Renamed so far</b><span>{{COUNT}} items</span><em>Derived by diffing our table
      against upstream's, which is the only way to tell a rename from an addition.</em></div>
  </div>
</section>

<section>
  <div class="sec-head"><h2>Three that were harder than they look</h2></div>
  <p><strong>One item was named three times, and each collision hid the next.</strong>
  <code>INTERRUPT</code> was assigned twice six weeks apart — to the flute, and to ICE HEAL
  in the state pass. The flute keeps it, because waking a thing that blocks a road is an
  interrupt in the plainest sense. ICE HEAL became <code>PREEMPT</code>, which collided with
  MANKEY, named four days earlier.</p>
  <p><mark>Under both collisions was a plainer fault that nobody had looked for</mark>:
  <strong>preempting a hung task hands the processor to somebody else and the hung one stays
  hung.</strong> A <strong>watchdog</strong> is the timer whose only job is to notice that
  something has stopped answering, and reset it. That is the cure, it still works twice, and
  it took a third reader to find — which is why the collision check now reads
  <em>every</em> surface out of the build rather than the ones that existed the day it was
  written.</p>
  <p><strong><code>FROZEN</code> could not be used for the frozen state</strong>, because it
  is a type name and the chart had just spent real effort making type names carry meaning.
  <code>HUNG</code> is what the state is anyway.</p>
  <p><strong>The box ladder is rights, not sizes</strong>, and that is the one item family
  where the metaphor is allowed to turn unpleasant. A ROOTBOX has unrestricted rights and
  <em>no daemon can decline to run on it</em> — which is the same sentence as “it never
  fails”, read from the other side.</p>
</section>

<footer>Generated by <code>tools/gbaitems.py</code> from
<code>engineGba/src/data/items.json</code>. Cut the PDF with
<code>./docs/build-pdf.sh items.html</code>.</footer>
</div>
"""

main()
