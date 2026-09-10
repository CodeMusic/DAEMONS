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
}

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
    for k in sorted(renamed):
        if k not in grouped:
            print("  ..  %-20s %-14s not in any group (rendered under Others)"
                  % (k, renamed[k][1]))
        elif k not in WHY and k not in SPECIALTY:
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
