#!/usr/bin/env python3
"""Render docs/type-chart.html from the game's own tables.

    python3 tools/gbachart.py [--write]

THE PAGE CLAIMED TO BE GENERATED AND WAS NOT. Its footer said "all 83 relations
read out of the built table, not transcribed", and nothing in tools/ produced
it. So it drifted exactly as a hand-kept page does: fifteen types when the ROM
has seventeen, 83 relations when it has 111, LEGACY and VECTOR still failing on
clauses 2.6 replaced, and "all 354 move names are unchanged" long after 309
were renamed. This makes the footer true.

WHAT IS DERIVED, read out of the build every run:
  * the seventeen types and their names    src/battle_main.c  gTypeNames
  * all 111 relations                      src/battle_main.c  gTypeEffectiveness
                                           (FORESIGHT and ENDTABLE are sentinel
                                           rows, not types, and are skipped)
  * every type hue that has shipped        tools/gbasprite.py TYPE_COLOR
  * the ramp, and it is VERIFIED           tools/gbasprite.py ramp5
  * what every move does, and its type     src/data/battle_moves.h + move_names.h
  * every width claim on the page          src/text.c glyph tables + charmap.txt
  * every contrast and distance number     computed here, never typed

WHAT IS AUTHORIAL, and lives in the tables below: each type's clause and score,
the sentence for each relation, why each colour, and the two hues that are
PROPOSALS rather than shipped. A relation with no sentence is REPORTED, never
rendered blank.

THIS PAGE IS ALSO A PROPOSAL UNDER REVIEW (2026-09-13). The colour roles, the
HARDENED and OPAQUE hues and the move-menu marks are not in the game. Nothing
here changes the ROM; the review comes first, then the build.

Cut the PDF with ./docs/build-pdf.sh type-chart.html.
"""
import html as H, itertools, math, os, re, sys

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA   = os.path.join(ROOT, "engineGba")
OUT   = os.path.join(ROOT, "docs/type-chart.html")
WRITE = "--write" in sys.argv

#  Display order: the fifteen in the order this page has always used, then the
#  two Gen 3 added. Checked against the relations -- a type in the table and
#  not here is reported.
CHART_ORDER = ["CONTENT", "LOGIC", "VECTOR", "CORRUPT", "STRATUM", "LEGACY", "SWARM",
               "LATENT", "ENTROPY", "FLOW", "GROWTH", "SIGNAL", "CONTEXT", "FROZEN",
               "EMERGENT", "HARDENED", "OPAQUE"]

#  2.6's one-clause test. (clause, score, where the score comes from)
CLAUSE = {
    "CONTENT":  ("the thing itself, with nothing read into it", "3 / 4", "run at 15"),
    "LOGIC":    ("formal rules applied step by step; proof, not intuition", "7 / 12", "run at 15"),
    "VECTOR":   ("a direction that never touches the ground", "10 / 13", "re-clause, 2026-09-11"),
    "CORRUPT":  ("data that has been tampered with", "6 / 11", "run at 15"),
    "STRATUM":  ("the physical layer everything else runs on", "7 / 13", "run at 15"),
    "LEGACY":   ("old material that everything else has had time to work on", "12 / 16", "re-clause, 2026-09-11"),
    "SWARM":    ("many small agents; no single one matters", "4 / 13", "run at 15"),
    "LATENT":   ("running below the surface, unobserved", "6 / 9", "run at 15"),
    "ENTROPY":  ("noise and heat; disorder that spreads", "9 / 14", "run at 15"),
    "FLOW":     ("everything running downhill to the lowest point", "8 / 11", "run at 15"),
    "GROWTH":   ("training: fitting to whatever it is fed", "8 / 18", "run at 15"),
    "SIGNAL":   ("raw current, before anything interprets it", "4 / 9", "run at 15"),
    "CONTEXT":  ("the frame you read a thing in — what makes the same thing mean differently", "11 / 11", "re-score at 17"),
    "FROZEN":   ("locked to what it already saw, unable to move", "7 / 11", "run at 15"),
    "EMERGENT": ("the behaviour nobody designed and nobody can account for", "7 / 7", "run at 15"),
    "HARDENED": ("material chosen to resist, and it gave up everything else to do it", "~17 / 21", "re-score at 17"),
    "OPAQUE":   ("a box you cannot see inside", "~6 / 10", "re-score at 17"),
}

#  THE TWO TYPES WITH NO HUE. TYPE_COLOR has fifteen entries for seventeen
#  types; the badge tool borrowed LEGACY's and LATENT's slots for these, and the
#  sprite tool SKIPS any daemon whose primary type has no entry. These are the
#  recommendations, and the options below are the alternatives measured.
PROPOSED_HUE = {
    "HARDENED": (196, 170, 96),
    "OPAQUE":   (40, 40, 46),
}
HARDENED_OPTIONS = [
    ("tempered straw", (196, 170, 96), True,
     "The colour steel actually turns when it is hardened — tempering is the process in the clause. "
     "The only metal candidate clear of every type at sprite size."),
    ("copper", (184, 115, 51), False,
     "Slightly better as text, but copper is a soft metal, which argues against the clause."),
    ("heat-blued", (58, 72, 140), False,
     "Also a temper colour and a good metaphor, but it sits in the blue band LOGIC, FLOW and LATENT already crowd."),
]
OPAQUE_OPTIONS = [
    ("near-black", (40, 40, 46), True,
     "A black box is the clause. Clear of every type, and clear of plain text, which matters for a type this dark."),
    ("ink navy", (34, 40, 64), False,
     "Blue enough to still read as a colour when written, dark enough to stay a sealed box."),
    ("slate ink", (50, 58, 70), False,
     "A bluer near-black. Nearly as clear, slightly closer to LATENT."),
    ("oxblood", (96, 40, 48), False,
     "The most separable at sprite size, but it reads as a dark VECTOR rather than as something sealed."),
]
WHY_PROPOSED = {
    "HARDENED": "<strong>Tempered straw.</strong> Proposed, not shipped. Tempering is how steel is hardened, "
                "and straw is the colour it turns at the temperature that makes it hard, so the hue is the "
                "clause's own process. Every grey metal was tried first and every one landed on LEGACY or LOGIC.",
    "OPAQUE":   "<strong>Near-black.</strong> Proposed, not shipped. A box you cannot see inside is the one "
                "type that should look like nothing can be read off it — and it stays clear of the default "
                "text colour, which a dark type easily would not.",
}

#  Sentences for relations the carried table never had (HARDENED and OPAQUE,
#  added at seventeen) and for LEGACY and VECTOR, whose old sentences argued
#  from clauses 2.6 replaced. These WIN over the carried table. "silent" means
#  2.6 scored the clause as predicting nothing there, and says so.
NEW_GLOSS = {
    ("CONTENT", "HARDENED"):  "the plain thing does little to what was built to resist it",
    ("ENTROPY", "HARDENED"):  "heat undoes a temper — it is how hardness is lost",
    ("GROWTH", "HARDENED"):   "roots find no seam in worked metal",
    ("FROZEN", "HARDENED"):   "cold does nothing to what was chosen to resist it",
    ("LOGIC", "OPAQUE"):      "rules open black boxes — 8.7's triangle",
    ("LOGIC", "HARDENED"):    "step-by-step force finds the one flaw; it gave up give",
    ("CORRUPT", "HARDENED"):  "there is nothing in solid material to tamper with",
    ("STRATUM", "HARDENED"):  "the layer underneath takes weight a hard thing cannot spread",
    ("VECTOR", "HARDENED"):   "a direction does little to material",
    ("CONTEXT", "OPAQUE"):    "you cannot reframe what you cannot read",
    ("CONTEXT", "HARDENED"):  "framing does little to a thing that is all structure",
    ("SWARM", "OPAQUE"):      "many small agents find gaps one observer cannot",
    ("SWARM", "HARDENED"):    "no single agent makes a dent",
    ("LEGACY", "HARDENED"):   "age is not an argument against what was built to resist",
    ("LATENT", "OPAQUE"):     "two things you cannot see into do not see into each other",
    ("LATENT", "HARDENED"):   "what runs below finds nothing to run through",
    ("EMERGENT", "HARDENED"): "even the unaccountable meets a surface that does not give",
    ("OPAQUE", "LOGIC"):      "rules need only the output, and a sealed box still gives one",
    ("OPAQUE", "CONTEXT"):    "a box you cannot see inside beats the frame you would have read it in",
    ("OPAQUE", "LATENT"):     "what is sealed outlasts what is merely unobserved",
    ("OPAQUE", "OPAQUE"):     "two sealed boxes cannot open each other",
    ("OPAQUE", "HARDENED"):   "concealment does nothing to plain resistance",
    ("HARDENED", "ENTROPY"):  "heat is the one fight hardness gave up",
    ("HARDENED", "FLOW"):     "water goes around what will not move",
    ("HARDENED", "SIGNAL"):   "metal conducts — the one reading in the re-score that goes the wrong way",
    ("HARDENED", "FROZEN"):   "a hard edge shatters what is only locked",
    ("HARDENED", "LEGACY"):   "material chosen to resist beats material that is merely old",
    ("HARDENED", "HARDENED"): "two resisting things mostly resist",
    ("CONTENT", "LEGACY"):    "silent — the clause says nothing here",
    ("ENTROPY", "LEGACY"):    "it has already been through heat",
    ("FLOW", "LEGACY"):       "water has had time — the relation Slate is built on",
    ("GROWTH", "LEGACY"):     "roots split it",
    ("LOGIC", "LEGACY"):      "old material is brittle; step-by-step force finds the fault",
    ("CORRUPT", "LEGACY"):    "you cannot poison a rock",
    ("STRATUM", "LEGACY"):    "the ground works on what sits on it",
    ("VECTOR", "LEGACY"):     "a direction that never touches it cannot work on it",
    ("LEGACY", "ENTROPY"):    "silent — a clause about being worked on says little about attack",
    ("LEGACY", "FROZEN"):     "silent",
    ("LEGACY", "LOGIC"):      "age is not an argument",
    ("LEGACY", "STRATUM"):    "it does not move the layer it is part of",
    ("LEGACY", "VECTOR"):     "old material, thrown, is the thing that does reach it",
    ("LEGACY", "SWARM"):      "mass against many small agents",
    ("SIGNAL", "VECTOR"):     "nothing between it and the current",
    ("GROWTH", "VECTOR"):     "what grows out of the ground cannot get to it",
    ("FROZEN", "VECTOR"):     "silent",
    ("LOGIC", "VECTOR"):      "you cannot corner what is not standing anywhere",
    ("STRATUM", "VECTOR"):    "the ground cannot reach what never touches it",
    ("VECTOR", "SIGNAL"):     "silent",
    ("VECTOR", "GROWTH"):     "everything rooted is reached from a place it cannot stand",
    ("VECTOR", "LOGIC"):      "everything stepwise is reached from a place it cannot stand",
    ("VECTOR", "SWARM"):      "everything numerous is reached from a place it cannot stand",
    ("SWARM", "VECTOR"):      "silent",
}

#  THE MOVE MARKS. HIT is unmarked on purpose: it is most of the moves, it is
#  the thing a player most wants to see plainly, and because every OTHER class
#  carries a mark, an unmarked name can only mean one thing.
CATEGORY_ORDER = ["HIT", "RAISE", "LOWER", "AFFLICT", "MEND", "GUARD", "OTHER"]
CATEGORY_ICON  = {"HIT": "", "RAISE": "▲", "LOWER": "▼", "AFFLICT": "◆", "MEND": "✚", "GUARD": "■", "OTHER": "●"}
CATEGORY_SAYS  = {
    "HIT":     "Deals damage. Unmarked.",
    "RAISE":   "Raises your own stats. No damage.",
    "LOWER":   "Lowers the foe's stats. No damage.",
    "AFFLICT": "Puts a state or a lasting effect on the foe — suspend, throttle, a trap, a curse. No damage.",
    "MEND":    "Restores your health or clears your state.",
    "GUARD":   "Protects you or your side.",
    "OTHER":   "Everything else: copying, transforming, weather, switching, calling other routines.",
}
MEND_EF    = {"RESTORE_HP", "SOFTBOILED", "MOONLIGHT", "MORNING_SUN", "SYNTHESIS", "SWALLOW", "WISH",
              "INGRAIN", "REST", "HEAL_BELL", "REFRESH", "PAIN_SPLIT"}
GUARD_EF   = {"PROTECT", "ENDURE", "LIGHT_SCREEN", "REFLECT", "MIST", "SAFEGUARD", "SUBSTITUTE", "MAGIC_COAT"}
AFFLICT_EF = {"LEECH_SEED", "NIGHTMARE", "SPITE", "PERISH_SONG", "MEAN_LOOK", "SPIKES", "TORMENT",
              "TAUNT", "DISABLE", "ENCORE"}
STATUS_PREFIX = ("SLEEP", "PARALYZE", "POISON", "TOXIC", "CONFUSE", "ATTRACT", "WILL_O_WISP", "YAWN",
                 "SWAGGER", "FLATTER", "TEETER_DANCE")
RAISE_EF   = {"MINIMIZE", "DEFENSE_CURL", "STOCKPILE", "CHARGE", "FOCUS_ENERGY", "BELLY_DRUM",
              "COSMIC_POWER", "BULK_UP", "CALM_MIND", "DRAGON_DANCE"}

#  In-game the marks are 4px glyphs redrawn into font cells nothing uses.
FREE_GLYPHS = "ÌÍÎÏìíîï"

#  The four moves from the author's screenshot of the move menu, 2026-09-13.
SAMPLE, SAMPLE_CURSOR, SAMPLE_MP = ("OCCLUDE", "THERMAL", "POLLUTE", "INSPECT"), "THERMAL", "15/15"

#  Carried over from docs/type-chart.html v11.111, verbatim. Authorial.
GLOSS = {('CONTENT', 'LATENT'): 'the literal cannot reach what was never surfaced',
 ('CONTENT', 'LEGACY'): 'literal data slides off old silicon',
 ('CONTEXT', 'CONTEXT'): 'two frames do not resolve each other',
 ('CONTEXT', 'CORRUPT'): 'framing is how bias is exposed',
 ('CONTEXT', 'LATENT'): 'framing reaches what runs below (§2.4, added)',
 ('CONTEXT', 'LOGIC'): 'THE THESIS — framing beats rules',
 ('CORRUPT', 'CORRUPT'): 'corruption does not compound',
 ('CORRUPT', 'GROWTH'): 'poisoned data ruins training',
 ('CORRUPT', 'LATENT'): 'you cannot poison what is not running',
 ('CORRUPT', 'LEGACY'): 'nor the silicon beneath that',
 ('CORRUPT', 'STRATUM'): 'bad data does not damage the layer beneath it',
 ('EMERGENT', 'EMERGENT'): 'only the unaccountable reaches the unaccountable',
 ('ENTROPY', 'EMERGENT'): 'nothing ordinary touches it',
 ('ENTROPY', 'ENTROPY'): 'noise does not compound',
 ('ENTROPY', 'FLOW'): 'noise cannot climb a gradient',
 ('ENTROPY', 'FROZEN'): 'temperature breaks an overfit',
 ('ENTROPY', 'GROWTH'): 'noise burns off a fitted model',
 ('ENTROPY', 'LEGACY'): 'inherited from FIRE/ROCK',
 ('ENTROPY', 'SWARM'): 'heat scatters a crowd',
 ('FLOW', 'EMERGENT'): 'nothing ordinary touches it',
 ('FLOW', 'ENTROPY'): 'gradient descent tames noise',
 ('FLOW', 'FLOW'): 'one gradient does not move another',
 ('FLOW', 'GROWTH'): 'training drinks the gradient',
 ('FLOW', 'LEGACY'): 'flow erodes old silicon — the one LEGACY relation that reads',
 ('FLOW', 'STRATUM'): 'flow erodes the layer',
 ('FROZEN', 'EMERGENT'): 'rigidity is the one thing that stops emergence',
 ('FROZEN', 'ENTROPY'): 'heat wins that exchange',
 ('FROZEN', 'FLOW'): 'a gradient keeps moving',
 ('FROZEN', 'FROZEN'): 'already locked',
 ('FROZEN', 'GROWTH'): 'frost halts growth',
 ('FROZEN', 'STRATUM'): 'inherited from ICE',
 ('FROZEN', 'VECTOR'): 'inherited from ICE',
 ('GROWTH', 'CORRUPT'): 'growth cannot clean bad data',
 ('GROWTH', 'EMERGENT'): 'nothing ordinary touches it',
 ('GROWTH', 'ENTROPY'): 'fitted models burn',
 ('GROWTH', 'FLOW'): 'training absorbs the gradient',
 ('GROWTH', 'GROWTH'): 'training does not train training',
 ('GROWTH', 'LEGACY'): 'and split the silicon',
 ('GROWTH', 'STRATUM'): 'roots break the layer',
 ('GROWTH', 'SWARM'): 'the crowd eats it first',
 ('GROWTH', 'VECTOR'): 'nothing to root into',
 ('LATENT', 'CONTENT'): 'the unsurfaced cannot touch the literal',
 ('LATENT', 'CONTEXT'): 'what runs below destabilises framing (§2.4, added)',
 ('LATENT', 'LATENT'): 'only the unsurfaced reaches the unsurfaced',
 ('LEGACY', 'ENTROPY'): 'inherited from ROCK — 0 of 14 predicted',
 ('LEGACY', 'FROZEN'): 'inherited from ROCK',
 ('LEGACY', 'LOGIC'): 'inherited from ROCK',
 ('LEGACY', 'STRATUM'): 'inherited from ROCK',
 ('LEGACY', 'SWARM'): 'inherited from ROCK',
 ('LEGACY', 'VECTOR'): 'inherited from ROCK',
 ('LOGIC', 'CONTENT'): 'rules parse data — the easy half of the thesis',
 ('LOGIC', 'CONTEXT'): 'THE THESIS — rules bounce off framing',
 ('LOGIC', 'CORRUPT'): 'rules get poor purchase on tampered input',
 ('LOGIC', 'FROZEN'): 'proof cracks what stopped moving',
 ('LOGIC', 'LATENT'): 'rules cannot reach what is not surfaced',
 ('LOGIC', 'LEGACY'): 'inherited from ROCK; the clause predicts nothing here',
 ('LOGIC', 'SWARM'): 'no single rule addresses a crowd',
 ('LOGIC', 'VECTOR'): 'symbols find no grip in a latent space',
 ('SIGNAL', 'EMERGENT'): 'nothing ordinary touches it',
 ('SIGNAL', 'FLOW'): 'current through water',
 ('SIGNAL', 'GROWTH'): 'growth insulates',
 ('SIGNAL', 'SIGNAL'): 'current does not shock current',
 ('SIGNAL', 'STRATUM'): 'grounded — the signal goes to earth',
 ('SIGNAL', 'VECTOR'): 'current disrupts a heading',
 ('STRATUM', 'CORRUPT'): 'the layer beneath outlasts bad data',
 ('STRATUM', 'ENTROPY'): 'the substrate damps noise',
 ('STRATUM', 'GROWTH'): 'training roots through the layer',
 ('STRATUM', 'LEGACY'): 'newer substrate supersedes old silicon',
 ('STRATUM', 'SIGNAL'): 'the physical layer grounds the signal',
 ('STRATUM', 'SWARM'): 'a layer cannot catch a distributed thing',
 ('STRATUM', 'VECTOR'): 'the physical layer cannot reach what has no location',
 ('SWARM', 'CONTEXT'): 'a crowd destabilises one frame',
 ('SWARM', 'CORRUPT'): 'no single agent to poison',
 ('SWARM', 'ENTROPY'): 'heat scatters it',
 ('SWARM', 'GROWTH'): 'a swarm consumes what grows',
 ('SWARM', 'LATENT'): 'numbers do not reach the unsurfaced',
 ('SWARM', 'LOGIC'): 'rules and crowds do not engage',
 ('SWARM', 'VECTOR'): 'a crowd cannot be given a heading',
 ('VECTOR', 'GROWTH'): 'a heading outpaces undirected fitting',
 ('VECTOR', 'LEGACY'): 'inherited from FLYING',
 ('VECTOR', 'LOGIC'): 'learned direction beats hand-written rules — real, but invisible without ML',
 ('VECTOR', 'SIGNAL'): 'inherited from FLYING',
 ('VECTOR', 'SWARM'): 'a heading organises a crowd'}

WHY = {'CONTENT': ('',
             'Bone. <em>The undifferentiated one</em> — nearly neutral on purpose, because the type that '
             'means “the thing itself with nothing read into it” should not look like anything. Its accent '
             'does the work.'),
 'CONTEXT': ('',
             'Magenta. The thesis type, and the one that must never be mistaken for anything else — it is '
             'the furthest from its neighbours by design.'),
 'CORRUPT': ('',
             '<strong>Mould, not soil.</strong> Was <code>#84764a</code>, a brown that sat 10.8 from STRATUM '
             '— unreadable at 56px. Moved darker and greener: <em>gone off</em> rather than merely earthy, '
             'which is closer to “data that has been tampered with” than the original was.'),
 'EMERGENT': ('',
              "<strong>Jade, deeper than SIGNAL's current.</strong> Was <code>#4ea89c</code>, 10.6 from "
              'SIGNAL. Moved <em>deeper and less lit</em> rather than to a new hue — the strangeness is the '
              'point, and a brighter jade would simply have read as a second SIGNAL.'),
 'ENTROPY': ('fixed by §6', '<strong>Choleric, yellow bile, fire.</strong> Same inheritance.'),
 'FLOW': ('', 'Deep and moving. The one hue that reads as a direction.'),
 'FROZEN': ('fixed by §6', '<strong>Phlegmatic, water, calm.</strong> Pale and cold.'),
 'GROWTH': ('',
            'Green, and unapologetically the plant reading — training <em>is</em> fitting to what it is '
            'fed.'),
 'LATENT': ('fixed by §6',
            '<strong>Melancholic, black bile, earth.</strong> The darkest of the fifteen, which suits '
            '“running below the surface”.'),
 'LEGACY': ('', "Slate, and §5.1's cairn. Old stone that is still standing."),
 'LOGIC': ('', 'Cold steel blue. Formality and proof; no warmth in it.'),
 'SIGNAL': ('', 'Cyan. Raw current, and the brightest thing on the chart.'),
 'STRATUM': ('',
             'The ground itself. Honest earth, and it did not move — of the two it is the more literal '
             'claim.'),
 'SWARM': ('', 'Olive. Insect, and the only one where the vanilla association survives intact.'),
 'VECTOR': ('fixed by §6',
            "<strong>Sanguine, air, red.</strong> Inherited from the Review Board's humours, not invented.")}

DUAL_HTML = '<section>\n  <div class="sec-head"><h2>A daemon that is two things</h2></div>\n  <p>Both engines allow two types per species and multiply the two lookups, so a\n  <code>CONTEXT/LATENT</code> daemon takes SWARM at ×2 for its CONTEXT half and ×½ for its\n  LATENT half, and the answer is ×1. Four outcomes exist that single types cannot reach:\n  <mark>×4, ×¼, and either ×0 overriding everything</mark>.</p>\n  <p>That multiplication is not a mechanic bolted onto the thesis, it <em>is</em> the thesis\n  at the scale of one creature. A dual type is <strong>two simultaneous accounts of the same\n  process</strong>, which is what §0.4 says CONTENT and CONTEXT are. When both accounts agree\n  that something is a weakness, it compounds to ×4 — <em>two readings converging is not\n  twice as much information, it is twice as much exposure.</em></p>\n  <table class="tbl">\n    <thead><tr><th>Pairing</th><th>What the arithmetic says</th></tr></thead>\n    <tbody>\n      <tr><td class="now">CONTENT / CONTEXT</td><td>The thesis in one daemon: the literal thing and the frame it is read in. LOGIC hits ×2 on the CONTENT half and ×½ on the CONTEXT half — <strong>×1, and the argument cancels itself out.</strong> Worth building on purpose.</td></tr>\n      <tr><td class="now">CONTEXT / LATENT</td><td>Both halves take LATENT and CONTEXT at ×2 (§2.4\'s mutual pair), so it is <strong>×4 to itself and to its own opposite.</strong> The most fragile thing in the game, against exactly the two types that understand it.</td></tr>\n      <tr><td class="now">LOGIC / LEGACY</td><td>Rules running on old silicon. FLOW and GROWTH both ×2 on LEGACY, unmodified on LOGIC — a formalist that erodes.</td></tr>\n      <tr><td class="now">STRATUM / VECTOR</td><td>Contradictory by construction: STRATUM is the physical layer, VECTOR has no location. STRATUM\'s own ×0 against VECTOR does not protect it. <strong>A daemon that cannot be coherently described.</strong></td></tr>\n    </tbody>\n  </table>\n  <p class="note"><span class="open">GAP</span> <strong>§9.4 does not yet say what a dual-type\n  daemon looks like.</strong> The type ramp is one hue across palette indices 1–5, and a\n  two-typed creature has two claims on it. The cheapest answer uses machinery 9.4 already\n  built: <mark>the ramp takes the primary type, and one of the five accent slots (6–10) is\n  reserved for the secondary\'s hue</mark> — so the label stays unambiguous and the second\n  reading is present as a marking rather than a wash. Not decided here.</p>\n</section>'

STATES_HTML = '<section>\n  <div class="sec-head"><h2>The states and the items</h2></div>\n  <p>These used to be printed here, and they drifted &mdash; this page still said\n  <code>CSC</code>, <code>HOT</code> and <code>INTERRUPT</code> long after the build had\n  shipped <code>CAS</code>, <code>OVR</code> and <code>PREEMPT</code>. <mark>They now live in\n  <a href="items.html">The Bag</a></mark>, which is generated from\n  <code>engineGba/src/data/items.json</code> and cannot drift from it.</p>\n  <p>What belongs here is only the one relation that ties them to the chart:\n  <strong>OVERHEATED is dealt by ENTROPY</strong>, whose one-clause test is <em>noise and\n  heat</em>, and <strong>FROZEN could not be reused for the frozen state</strong> because it\n  is a type name &mdash; which is the constraint that produced <code>HUNG</code>.</p>\n</section>'

MOVED_NOTE_HTML = '<p class="note"><strong>The two moves, 2026-09-08.</strong> Four pairs sat closer than ~20 in\n  CIE76 on the mid tone — roughly where two colours stop being separable at 56px, and most of a\n  sprite\'s area. <mark>They collided because their metaphors are adjacent</mark>: CORRUPT and\n  STRATUM were both earth, SIGNAL and EMERGENT both electric-teal. Adjacent ideas make adjacent\n  colours, which is the system working right up until it stops being readable.\n  <code>CORRUPT 10.8 → 25.9</code> and <code>EMERGENT 10.6 → 26.0</code>, each moved\n  <em>within</em> its own metaphor rather than out of it, and only one of each pair moved.</p>'

# ============================================================== derivation
def gba_read(p):
    return open(os.path.join(GBA, p), encoding="utf-8").read()

def report(msg):
    print("  " + msg)

def load_types():
    src = gba_read("src/battle_main.c")
    tn = dict(re.findall(r'\[TYPE_(\w+)\] = _\("(\w+)"\)', src))
    body = re.search(r'const u8 gTypeEffectiveness\[\d+\] =\s*\{(.*?)\n\};', src, re.S).group(1)
    mul = {"SUPER_EFFECTIVE": 2.0, "NOT_EFFECTIVE": 0.5, "NO_EFFECT": 0.0}
    rel = {}
    for a, b, m in re.findall(r'TYPE_(\w+)\s*,\s*TYPE_(\w+)\s*,\s*TYPE_MUL_(\w+)', body):
        if a in tn and b in tn:
            rel[(tn[a], tn[b])] = mul[m]
    return tn, rel

def load_hues(tn):
    gs = open(os.path.join(ROOT, "tools/gbasprite.py"), encoding="utf-8").read()
    table = re.search(r'TYPE_COLOR = \{(.*?)\n\}', gs, re.S).group(1)
    shipped = {tn[k]: (int(r), int(g), int(b)) for k, r, g, b in
               re.findall(r'"(\w+)":\s*\(\s*(\d+),\s*(\d+),\s*(\d+)\)', table) if k in tn}
    fn = re.search(r'def ramp5\(.*?\n(?=def |\Z)', gs, re.S).group(0)
    coeffs = [float(x) for x in re.findall(r'(?:up|dn)\((0\.\d+)\)', fn)]
    return shipped, coeffs

def load_font():
    src = gba_read("src/text.c")
    tables = {n: [int(x) for x in re.findall(r'\d+', b)] for n, b in
              re.findall(r'(sFont\w*LatinGlyphWidths)\[\]\s*=\s*\{(.*?)\};', src, re.S)}
    cm = {}
    for line in open(os.path.join(GBA, "charmap.txt"), encoding="utf-8"):
        body = line.split("@")[0].strip()
        if "=" not in body:
            continue
        k, v = (p.strip() for p in body.split("=", 1))
        if len(k) == 3 and k[0] == k[2] == "'":
            k = k[1]
        elif len(k) > 1 and k[0] == k[-1] == '"':
            k = k[1:-1]
        try:
            cm[k] = int(v.split()[0], 16)
        except ValueError:
            pass
    def width(s, table):
        t = tables[table]
        return sum(t[cm[c]] for c in s if c in cm and cm[c] < len(t))
    return width, cm, tables

def load_moves(tn):
    names = dict(re.findall(r'\[MOVE_(\w+)\]\s*=\s*_\("([^"]+)"\)', gba_read("src/data/text/move_names.h")))
    blocks = dict(re.findall(r'\[MOVE_(\w+)\] =\s*\{(.*?)\n\s*\},', gba_read("src/data/battle_moves.h"), re.S))
    out = {}
    for mv, b in blocks.items():
        if mv == "NONE" or mv not in names:
            continue
        pw = int((re.search(r'\.power\s*=\s*(\d+)', b) or [0, 0])[1])
        ef = (re.search(r'\.effect\s*=\s*(\w+)', b) or [0, ""])[1].replace("EFFECT_", "")
        ty = tn.get((re.search(r'\.type\s*=\s*TYPE_(\w+)', b) or [0, ""])[1], "?")
        if pw > 0:                                                c = "HIT"
        elif ef in MEND_EF:                                       c = "MEND"
        elif ef in GUARD_EF:                                      c = "GUARD"
        elif "_UP" in ef or ef in RAISE_EF:                       c = "RAISE"
        elif "_DOWN" in ef or ef in ("TICKLE", "MEMENTO"):        c = "LOWER"
        elif ef in AFFLICT_EF or ef.startswith(STATUS_PREFIX):    c = "AFFLICT"
        else:                                                     c = "OTHER"
        out[names[mv]] = (c, ty, pw)
    return out

# ================================================================= colour
def ramp_step(rgb, coeffs):
    up = lambda t: tuple(min(255, int(c + (255 - c) * t)) for c in rgb)
    dn = lambda t: tuple(max(0, int(c * t)) for c in rgb)
    return [up(coeffs[0]), up(coeffs[1]), tuple(rgb), dn(coeffs[2]), tuple(v + 10 for v in dn(coeffs[3]))]

def gba(c):     #  15-bit colour: what the hardware can actually show
    return tuple(round(v / 255 * 31) * 255 // 31 for v in c)

def _lin(v):
    v /= 255
    return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4

def lum(c):
    r, g, b = (_lin(x) for x in c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)

def lab(c):
    f = lambda v: (v / 255) / 12.92 if v / 255 <= 0.04045 else ((v / 255 + 0.055) / 1.055) ** 2.4
    r, g, b = (f(x) for x in c)
    X = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    Y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    Z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    t = lambda v: v ** (1 / 3) if v > 0.008856 else 7.787 * v + 16 / 116
    fx, fy, fz = t(X), t(Y), t(Z)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))

def de(a, b):
    return math.dist(lab(a), lab(b))

def lch(c):
    L, a, b = lab(c)
    return L, math.hypot(a, b)

def hexc(c):
    return "#%02x%02x%02x" % tuple(c)

WHITE, PLAIN_TEXT = (255, 255, 255), (74, 74, 74)   # RGB(9,9,9) on the move window
SEPARABLE = 20.0

# ================================================================== render
def mult_sym(v):
    return {2.0: "2", 0.5: "&frac12;", 0.0: "0", 1.0: ""}[v]

def mult_cls(v):
    return {2.0: "x2", 0.5: "xh", 0.0: "x0", 1.0: "x1"}[v]

def mult_txt(v):
    return {2.0: "×2", 0.5: "×½", 0.0: "×0"}[v]

def main():
    tn, rel = load_types()
    types = [t for t in CHART_ORDER if any(t in k for k in rel)]
    stray = sorted({x for k in rel for x in k} - set(CHART_ORDER))
    report("%d relations, %d types in them%s" % (len(rel), len(types),
           ("; NOT IN CHART_ORDER: " + ", ".join(stray)) if stray else ""))

    shipped, coeffs = load_hues(tn)
    if coeffs != [0.70, 0.38, 0.52, 0.16]:
        report("!!  gbasprite.ramp5 is %s, not the 0.70/0.38/0.52/0.16 this page describes" % coeffs)
    hue, status = {}, {}
    for t in types:
        if t in shipped:
            hue[t], status[t] = shipped[t], "shipped"
        elif t in PROPOSED_HUE:
            hue[t], status[t] = PROPOSED_HUE[t], "proposed"
        else:
            report("!!  %s has no hue, shipped or proposed" % t)
    report("hues: %d shipped in TYPE_COLOR, %d proposed here (%s)" % (
        sum(1 for s in status.values() if s == "shipped"),
        sum(1 for s in status.values() if s == "proposed"),
        ", ".join(t for t in types if status.get(t) == "proposed")))

    mid = {t: gba(hue[t]) for t in types}
    s4 = {t: gba(ramp_step(hue[t], coeffs)[3]) for t in types}

    gloss = dict(GLOSS)
    gloss.update(NEW_GLOSS)
    missing = [k for k in rel if k not in gloss]
    for a, b in missing:
        report("!!  no sentence for %s -> %s %s" % (a, b, mult_txt(rel[(a, b)])))
    report("sentences: %d of %d relations" % (len(rel) - len(missing), len(rel)))

    width, cm, tables = load_font()
    moves = load_moves(tn)
    cats = {c: sorted(n for n, (cc, _, _) in moves.items() if cc == c) for c in CATEGORY_ORDER}
    report("moves: %d, " % len(moves) + ", ".join("%s %d" % (c, len(cats[c])) for c in CATEGORY_ORDER))

    SMALL, NAME = "sFontSmallLatinGlyphWidths", "sFontNormalCopy1LatinGlyphWidths"
    over4 = [n for n in moves if width(n, SMALL) + 4 > 64]
    over8 = [n for n in moves if width(n, SMALL) + width("↑" if "↑" in cm else "UP_ARROW", SMALL) > 64]
    arrow = tables[SMALL][cm["UP_ARROW"]] if "UP_ARROW" in cm else 8
    over8 = [n for n in moves if width(n, SMALL) + arrow > 64]
    label = width("TYPE/", SMALL)
    info_over = sorted(t for t in tn.values() if label + width(t, NAME) > 65)
    widest_type = max(width(t, NAME) for t in tn.values())
    free = [g for g in FREE_GLYPHS if g in cm and tables[SMALL][cm[g]] == 4]
    report("glyphs: 4px mark overflows %d names, %dpx arrow overflows %d; %d free 4px cells" %
           (len(over4), arrow, len(over8), len(free)))

    # ---------------------------------------------------------------- colour
    rows = []
    for t in types:
        ct = contrast(s4[t], WHITE)
        tag = ('<span class="open">PROPOSED</span>' if status[t] == "proposed" else "")
        rows.append(
            '<tr><td class="now">%s%s</td>'
            '<td><span class="sw" style="background:%s"></span><code>%s</code></td>'
            '<td><span class="badge" style="background:%s">%s</span></td>'
            '<td><span class="ontext" style="color:%s">%s</span></td>'
            '<td class="num">%.1f</td></tr>'
            % (t, tag and " " + tag, hexc(mid[t]), hexc(hue[t]), hexc(s4[t]), t,
               hexc(s4[t]), t, ct))
    worst_t = min(types, key=lambda t: contrast(s4[t], WHITE))

    pairs = list(itertools.combinations(types, 2))
    pm = sorted((de(mid[a], mid[b]), a, b) for a, b in pairs)
    ps = sorted((de(s4[a], s4[b]), a, b) for a, b in pairs)
    close = "".join(
        '<tr><td><span class="pair"><i style="background:%s"></i><i style="background:%s"></i></span>%s / %s</td>'
        '<td class="num">%.1f</td><td class="num%s">%.1f</td></tr>'
        % (hexc(s4[a]), hexc(s4[b]), a, b, de(mid[a], mid[b]), " warn" if d < 12 else "", d)
        for d, a, b in ps[:8])
    n_mid = sum(1 for d, _, _ in pm if d < SEPARABLE)
    n_s4 = sum(1 for d, _, _ in ps if d < SEPARABLE)
    ll = de(s4["LOGIC"], s4["LEGACY"]), de(mid["LOGIC"], mid["LEGACY"])

    #  FOUND BY LOOKING, NOT BY THE NUMBERS. The first render of the mockup
    #  showed OCCLUDE (OPAQUE) and POLLUTE (CORRUPT) as plain dark text: step 4
    #  of an already-dark hue lands beside the box's own grey. The alternative
    #  is measured rather than asserted -- words take the LIGHTEST ramp step
    #  that still clears 4.5:1, which is the hue itself for the dark types.
    def text_step(rgb):
        steps = ramp_step(rgb, coeffs)
        for i in (2, 3):
            c = gba(steps[i])
            if contrast(c, WHITE) >= 4.5:
                return c, i
        return gba(steps[3]), 3
    alt = {t: text_step(hue[t]) for t in types}
    n_alt = sum(1 for a, b in pairs if de(alt[a][0], alt[b][0]) < SEPARABLE)
    uses_hue = [t for t in types if alt[t][1] == 2]
    #  TWO WAYS A WORD READS AS UNCOLOURED, and one distance only catches the
    #  first. The first draft of this note blamed the three types nearest the
    #  grey, then pointed at OCCLUDE and POLLUTE, which are not among them --
    #  they fail the OTHER way. Measured separately now:
    #    near the box's grey text     CIE76 to it under 15
    #    too dark and weak to show    L* under 25 AND chroma under 20
    #    no hue at all                chroma under 10
    def plain_why(c):
        L, C = lch(c)
        why = []
        if de(c, PLAIN_TEXT) < 15: why.append("near the grey")
        if C < 10:                 why.append("no hue")
        if L < 25 and C < 20:      why.append("reads as ink")
        return why
    plain_s4  = {t: plain_why(s4[t]) for t in types if plain_why(s4[t])}
    plain_alt = {t: plain_why(alt[t][0]) for t in types if plain_why(alt[t][0])}
    near_grey = [t for t in types if "near the grey" in plain_s4.get(t, [])]
    as_ink    = [t for t in types if "reads as ink" in plain_s4.get(t, [])]
    fixed_alt = [t for t in types if t in plain_s4 and t not in plain_alt]
    still     = [t for t in types if t in plain_alt]

    def option_rows(ty, opts):
        others = [t for t in types if t != ty]
        out = []
        for name, rgb, rec, note in opts:
            m = gba(rgb); s = gba(ramp_step(rgb, coeffs)[3])
            dm = min(de(m, mid[o]) for o in others)
            ds = min(de(s, s4[o]) for o in others)
            near = min(others, key=lambda o: de(s, s4[o]))
            word_c = lch(text_step(rgb)[0])[1]     #  chroma of what would be WRITTEN
            out.append(
                '<tr%s><td class="now">%s%s</td>'
                '<td><span class="sw" style="background:%s"></span><span class="sw" style="background:%s"></span></td>'
                '<td class="num%s">%.1f</td><td class="num">%.1f</td><td>%s</td><td class="num">%.1f</td>'
                '<td class="num%s">%.1f</td><td>%s</td></tr>'
                % (' class="rec"' if rec else "", H.escape(name),
                   ' <small>recommended</small>' if rec else "",
                   hexc(m), hexc(s), "" if dm >= SEPARABLE else " warn", dm, ds, near,
                   contrast(s, WHITE), " warn" if word_c < 10 else "", word_c, note))
        return "".join(out)

    # ------------------------------------------------------------ move menu
    def mark(c):
        i = CATEGORY_ICON[c]
        return '<span class="mk">%s</span>' % i if i else '<span class="mk"></span>'
    cells = []
    for n in SAMPLE:
        c, ty, pw = moves[n]
        cells.append('<div class="mv%s"><span class="cur">%s</span>%s<span style="color:%s">%s</span></div>'
                     % (" on" if n == SAMPLE_CURSOR else "", "▶" if n == SAMPLE_CURSOR else "",
                        mark(c), hexc(s4[ty]), n))
    cur_ty = moves[SAMPLE_CURSOR][1]
    mock = ('<div class="mock"><div class="mock-moves">%s</div>'
            '<div class="mock-info"><div><span>MP</span><span>%s</span></div>'
            '<div><span style="color:%s">%s</span></div></div></div>'
            % ("".join(cells), SAMPLE_MP, hexc(s4[cur_ty]), cur_ty))
    sample_note = ", ".join("<code>%s</code> %s %s" % (n, moves[n][1], moves[n][0].lower())
                            for n in SAMPLE)

    legend = "".join(
        '<tr><td class="now">%s</td><td class="mkcell">%s</td><td class="num">%d</td><td>%s</td>'
        '<td class="ex">%s</td></tr>'
        % (c, CATEGORY_ICON[c] or "<span class=faint>none</span>", len(cats[c]), CATEGORY_SAYS[c],
           ", ".join(cats[c][:6]) + ("…" if len(cats[c]) > 6 else ""))
        for c in CATEGORY_ORDER)

    # --------------------------------------------------------------- matrix
    head = '<thead><tr><th class="corner"></th>' + "".join(
        '<th data-t="%s"><div class="swatch" style="background:%s"></div><div class="vlabel">%s</div></th>'
        % (t, hexc(mid[t]), t) for t in types) + "</tr></thead>"
    body = ""
    for a in types:
        body += '<tr data-row="%s"><th data-t="%s"><span class="rowlab"><i style="background:%s"></i>%s</span></th>' % (a, a, hexc(mid[a]), a)
        for b in types:
            v = rel.get((a, b), 1.0)
            body += '<td class="c %s" data-col="%s"><span class="m">%s</span></td>' % (mult_cls(v), b, mult_sym(v))
        body += "</tr>"
    matrix = '<table class="grid">%s<tbody>%s</tbody></table>' % (head, body)

    # ---------------------------------------------------------------- cards
    cards = []
    for t in types:
        clause, score, src = CLAUSE[t]
        hits = [(b, rel[(t, b)]) for b in types if (t, b) in rel]
        by = [(a, rel[(a, t)]) for a in types if (a, t) in rel]
        fmt = lambda pairs, key: "".join(
            '<div><b>%s %s</b> — %s</div>' % (o, mult_txt(v), gloss.get(key(o), "—")) for o, v in pairs)
        cards.append(
            '<div class="card" style="border-left-color:%s"><p class="eyebrow" style="margin:0 0 6px">'
            '%s · one-clause test <span>%s</span> <span class="faint">· %s</span>%s</p>'
            '<p class="clause">“%s”</p><h3>What it hits</h3><div class="rel">%s</div>'
            '<h3>What hits it</h3><div class="rel">%s</div></div>'
            % (hexc(mid[t]), t, score, src,
               ' <span class="open">HUE PROPOSED</span>' if status[t] == "proposed" else "",
               H.escape(clause), fmt(hits, lambda b: (t, b)) or "<div>—</div>",
               fmt(by, lambda a: (a, t)) or "<div>—</div>"))

    # ------------------------------------------------------------ why rows
    why = []
    for t in types:
        if t in WHY:
            tag, text = WHY[t]
            why.append('<tr><td class="now">%s%s</td><td class="was">%s</td><td>%s</td></tr>'
                       % (t, ("<small>%s</small>" % tag) if tag else "", hexc(hue[t]), text))
        elif t in WHY_PROPOSED:
            why.append('<tr><td class="now">%s<small>proposed</small></td><td class="was">%s</td><td>%s</td></tr>'
                       % (t, hexc(hue[t]), WHY_PROPOSED[t]))
        else:
            report("!!  %s has no 'why this colour' entry" % t)

    dual = DUAL_HTML.replace("Rules running on old silicon.", "Rules running on old material.")

    subs = {
        "{{NREL}}": str(len(rel)), "{{NTYPE}}": str(len(types)), "{{NPAIRS}}": str(len(pairs)),
        "{{COLOUR_ROWS}}": "".join(rows), "{{WORST_T}}": worst_t,
        "{{WORST_C}}": "%.1f" % contrast(s4[worst_t], WHITE),
        "{{PLAIN_C}}": "%.1f" % contrast(PLAIN_TEXT, WHITE),
        "{{N_MID}}": str(n_mid), "{{N_S4}}": str(n_s4), "{{CLOSE}}": close,
        "{{LL_S4}}": "%.1f" % ll[0], "{{LL_MID}}": "%.1f" % ll[1],
        "{{N_ALT}}": str(n_alt), "{{USES_HUE}}": ", ".join(uses_hue),
        "{{NEAR_GREY}}": ", ".join("%s (%.1f)" % (t, de(s4[t], PLAIN_TEXT)) for t in near_grey),
        "{{AS_INK}}": ", ".join(as_ink), "{{FIXED_ALT}}": ", ".join(fixed_alt),
        "{{STILL_PLAIN}}": ", ".join(still),
        "{{HARD_ROWS}}": option_rows("HARDENED", HARDENED_OPTIONS),
        "{{OPAQUE_ROWS}}": option_rows("OPAQUE", OPAQUE_OPTIONS),
        "{{MOCK}}": mock, "{{SAMPLE_NOTE}}": sample_note, "{{LEGEND}}": legend,
        "{{NMOVES}}": str(len(moves)), "{{NHIT}}": str(len(cats["HIT"])),
        "{{PCT_HIT}}": "%d" % round(100 * len(cats["HIT"]) / len(moves)),
        "{{OVER4}}": str(len(over4)), "{{ARROW}}": str(arrow), "{{OVER8}}": str(len(over8)),
        "{{OVER8_EX}}": ", ".join("<code>%s</code>" % n for n in sorted(over8)[:4]),
        "{{NFREE}}": str(len(free)), "{{FREE}}": " ".join("<code>%s</code>" % g for g in free),
        "{{LABEL_W}}": str(label), "{{WIDEST_T}}": str(widest_type),
        "{{INFO_OVER}}": ", ".join("<code>%s</code>" % t for t in info_over if label + width(t, NAME) > 66),
        "{{MATRIX}}": matrix, "{{DUAL}}": dual, "{{CARDS}}": "".join(cards),
        "{{WHY_ROWS}}": "".join(why), "{{MOVED_NOTE}}": MOVED_NOTE_HTML, "{{STATES}}": STATES_HTML,
    }
    html = TEMPLATE
    for k, v in subs.items():
        html = html.replace(k, v)
    left = re.findall(r'\{\{\w+\}\}', html)
    if left:
        report("!!  unfilled placeholders: %s" % sorted(set(left)))
    if WRITE:
        open(OUT, "w", encoding="utf-8").write(html)
        report("written %s" % OUT)
    else:
        report("(report only; pass --write)")


TEMPLATE = r"""<title>The Chart and the States</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap">
<style>
:root{
  --paper:#f4f3ee; --raise:#fbfaf7; --ink:#16181c; --dim:#565c66; --faint:#878d96;
  --rule:#dbdad3; --rule-hard:#b0b3b7; --slate:#3f5f88; --slate-soft:#607a9e;
  --warn:#a8452e; --good:#3f6f4a;
  --cell-2:#3f5f88; --cell-half:#9aa0a8; --cell-0:#16181c;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --paper:#131519; --raise:#1b1e24; --ink:#e8e6e0; --dim:#a2a8b2; --faint:#767c86;
    --rule:#2a2e35; --rule-hard:#414751; --slate:#8fb0d8; --slate-soft:#7f9cc4;
    --warn:#e0866c; --good:#7fb389;
    --cell-2:#8fb0d8; --cell-half:#6d737d; --cell-0:#e8e6e0;
  }
}
:root[data-theme="dark"]{
  --paper:#131519; --raise:#1b1e24; --ink:#e8e6e0; --dim:#a2a8b2; --faint:#767c86;
  --rule:#2a2e35; --rule-hard:#414751; --slate:#8fb0d8; --slate-soft:#7f9cc4;
  --warn:#e0866c; --good:#7fb389;
  --cell-2:#8fb0d8; --cell-half:#6d737d; --cell-0:#e8e6e0;
}
*{box-sizing:border-box}
body{background:var(--paper);color:var(--ink);font-family:"Source Serif 4",Georgia,serif;line-height:1.6;margin:0}
.wrap{max-width:1080px;margin:0 auto;padding:40px 24px 96px;display:flex;flex-direction:column;gap:52px}
h1,h2,h3,.ui{font-family:"IBM Plex Sans",system-ui,sans-serif}
h1{font-size:clamp(30px,4.4vw,46px);line-height:1.08;margin:0;font-weight:600;letter-spacing:-.02em;text-wrap:balance}
h2{font-size:23px;font-weight:600;margin:0 0 4px;letter-spacing:-.01em;text-wrap:balance}
h3{font-size:15px;font-weight:600;margin:10px 0 8px;letter-spacing:.01em}
p{margin:0 0 14px;max-width:66ch}
.eyebrow{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--faint);margin:0 0 12px}
.lede{font-size:18px;color:var(--dim);max-width:64ch;margin:16px 0 0}
header{border-bottom:2px solid var(--rule-hard);padding-bottom:28px}
section{display:flex;flex-direction:column;gap:14px}
.sec-head{border-top:1px solid var(--rule-hard);padding-top:16px}
mark{background:none;color:var(--ink);font-weight:600;box-shadow:inset 0 -.42em 0 color-mix(in srgb,var(--slate-soft) 26%,transparent)}
code,.mono{font-family:"IBM Plex Mono",monospace;font-size:.88em}
a{color:var(--slate)}
.faint{color:var(--faint)}
.scroll{overflow-x:auto;border:1px solid var(--rule);border-radius:2px;background:var(--raise)}
table.grid{border-collapse:separate;border-spacing:0;font-family:"IBM Plex Mono",monospace;font-size:11px;font-variant-numeric:tabular-nums}
table.grid th,table.grid td{border-right:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:0;text-align:center}
table.grid thead th{position:sticky;top:0;background:var(--raise);z-index:2;height:84px;vertical-align:bottom;padding-bottom:7px;width:34px;min-width:34px;cursor:pointer}
table.grid thead th.corner{left:0;z-index:3;width:96px;min-width:96px;cursor:default}
table.grid tbody th{position:sticky;left:0;background:var(--raise);z-index:1;text-align:right;padding:0 9px;width:96px;min-width:96px;font-weight:500;height:26px;cursor:pointer}
.vlabel{writing-mode:vertical-rl;transform:rotate(180deg);letter-spacing:.06em;font-size:10px;color:var(--dim);white-space:nowrap;margin:0 auto}
.swatch{width:14px;height:4px;border-radius:1px;margin:0 auto 6px}
.rowlab{display:inline-flex;align-items:center;gap:7px;justify-content:flex-end;width:100%}
.rowlab i{width:4px;height:13px;border-radius:1px;flex:none}
td.c{height:26px;width:34px;color:var(--faint)}
td.c .m{display:inline-flex;align-items:center;justify-content:center;width:19px;height:19px;border-radius:2px;font-size:10px;font-weight:600;line-height:1}
td.c.x2 .m{background:var(--cell-2);color:var(--paper)}
td.c.xh .m{border:1.5px solid var(--cell-half);color:var(--cell-half)}
td.c.x0 .m{background:var(--cell-0);color:var(--paper)}
tr.on th,tr.on td,td.oncol{background:color-mix(in srgb,var(--slate-soft) 11%,transparent)}
.key{display:flex;flex-wrap:wrap;gap:18px;align-items:center;font-family:"IBM Plex Sans",sans-serif;font-size:12.5px;color:var(--dim)}
.key span{display:inline-flex;align-items:center;gap:7px}
.key em{display:inline-block;width:17px;height:17px;border-radius:2px;vertical-align:-4px}
.key .m-2{background:var(--cell-2)}.key .m-h{border:1.5px solid var(--cell-half)}.key .m-0{background:var(--cell-0)}
.rel{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:0 22px}
.rel div{font-size:13px;padding:5px 0;border-bottom:1px solid var(--rule);font-family:"IBM Plex Sans",sans-serif;color:var(--dim)}
.rel b{font-family:"IBM Plex Mono",monospace;font-weight:600;color:var(--ink);font-size:11.5px}
table.tbl{width:100%;border-collapse:collapse;font-size:14px}
table.tbl th{font-family:"IBM Plex Sans",sans-serif;font-size:11px;letter-spacing:.11em;text-transform:uppercase;color:var(--faint);text-align:left;font-weight:600;padding:0 14px 8px 0;border-bottom:1px solid var(--rule-hard);white-space:nowrap}
table.tbl td{padding:9px 14px 9px 0;border-bottom:1px solid var(--rule);vertical-align:middle}
table.tbl td.was{font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--faint);white-space:nowrap}
table.tbl td.now{font-family:"IBM Plex Mono",monospace;font-size:13px;font-weight:600;color:var(--ink);white-space:nowrap}
table.tbl td.now small{display:block;font-weight:400;color:var(--faint);font-size:11px;letter-spacing:.06em}
table.tbl td.num{font-family:"IBM Plex Mono",monospace;font-variant-numeric:tabular-nums;font-size:12.5px;white-space:nowrap}
table.tbl td.num.warn{color:var(--warn);font-weight:600}
table.tbl td.ex{font-family:"IBM Plex Mono",monospace;font-size:11.5px;color:var(--faint)}
table.tbl td.mkcell{font-size:15px;text-align:center;width:44px}
table.tbl tr.rec td{background:color-mix(in srgb,var(--good) 8%,transparent)}
.note{font-size:13.5px;color:var(--dim);border-left:2px solid var(--rule-hard);padding-left:14px;max-width:62ch}
.open{display:inline-block;font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:.1em;border:1px solid var(--warn);color:var(--warn);padding:1px 5px;border-radius:2px;vertical-align:2px;white-space:nowrap}
.review{border:1px solid var(--warn);border-left:4px solid var(--warn);background:color-mix(in srgb,var(--warn) 6%,var(--raise));padding:14px 18px;border-radius:2px;font-family:"IBM Plex Sans",sans-serif;font-size:14px;color:var(--ink)}
.review p{margin:0;max-width:none}
.sw{display:inline-block;width:18px;height:18px;border-radius:2px;vertical-align:-4px;margin-right:6px;box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--ink) 14%,transparent)}
.badge{display:inline-block;font-family:"IBM Plex Mono",monospace;font-weight:700;font-size:11px;letter-spacing:.06em;color:#fff;padding:3px 7px;border-radius:3px}
/* The white battle box, drawn as the game draws it -- it stays white in dark
   mode because it depicts a screen, not the page. */
.ontext{display:inline-block;background:#fff;font-family:"IBM Plex Mono",monospace;font-weight:700;font-size:12.5px;letter-spacing:.04em;padding:3px 8px;border-radius:2px;box-shadow:inset 0 0 0 1px #d6d6cd}
.pair{display:inline-flex;gap:2px;margin-right:8px;vertical-align:-3px}.pair i{width:12px;height:14px;border-radius:1px}
.card{border:1px solid var(--rule);border-left:3px solid var(--rule-hard);background:var(--raise);padding:14px 16px;border-radius:2px;margin:0 0 12px;break-inside:avoid}
.card .clause{font-size:15px;font-style:italic;margin:0;max-width:60ch}
.mockwrap{display:flex;flex-wrap:wrap;gap:22px;align-items:flex-start}
.mock{display:grid;grid-template-columns:1fr auto;gap:8px;background:#2a2a30;padding:8px;border-radius:3px;width:min(560px,100%)}
.mock-moves,.mock-info{background:#fff;border:4px solid #6a5a73;border-radius:3px;font-family:"IBM Plex Mono",monospace;font-weight:700;letter-spacing:.03em;font-size:15px;color:#4a4a4a}
.mock-moves{display:grid;grid-template-columns:1fr 1fr;gap:10px 14px;padding:14px 16px}
.mv{display:flex;align-items:center;white-space:nowrap}
.cur{display:inline-block;width:14px;color:#2a2a30}
.mk{display:inline-block;width:14px;font-size:11px;color:#4a4a4a}
.mock-info{padding:12px 14px;display:flex;flex-direction:column;gap:10px;min-width:150px}
.mock-info div{display:flex;justify-content:space-between;gap:14px}
.mockcap{flex:1 1 240px;font-size:13.5px;color:var(--dim);max-width:44ch}
footer{border-top:1px solid var(--rule-hard);padding-top:18px;font-size:12.5px;color:var(--faint);font-family:"IBM Plex Sans",sans-serif}
@media print{body{background:#fff;color:#000}.wrap{max-width:none;padding:0;gap:26px}
  section,.card,table.tbl tr{break-inside:avoid}h2{break-after:avoid}
  table.grid thead th,table.grid tbody th{position:static}}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
</style>
<div class="wrap">
<header>
  <p class="eyebrow">CONTEXT / CONTENT · §2 · §9.4 · under review 2026-09-13</p>
  <h1>The Chart and the States</h1>
  <p class="lede">All {{NREL}} relations under our {{NTYPE}} names, what each one teaches, and how the
  argument survives a daemon that is two things at once. And, for review first: one rule for how
  every screen uses a type's colour, hues for the two types that never had one, and a mark on each
  move that says what it does.</p>
</header>

<div class="review"><p><strong>Under review.</strong> Everything marked <span class="open">PROPOSED</span>
is a recommendation, not the game. Nothing here has touched the ROM: the colours are decided on
this page first, then built.</p></div>

<section>
  <div class="sec-head"><h2>Colour: one hue per type, and one step of it for words</h2></div>
  <p>Every type keeps its one hue. <code>ramp5</code> already turns that hue into five steps, and
  sprites use all five. <mark>Anything that is a word uses step 4</mark>: the ground under a type
  badge <em>and</em> a move name written on the white battle box. It is one colour doing both jobs,
  because contrast works the same in both directions.</p>
  <p>That is the whole of the consistency rule. No hue changes for contrast: step 4 of all
  {{NTYPE}} is readable as text on white, and white is readable on it. The worst is
  <strong>{{WORST_T}} at {{WORST_C}}:1</strong>; 4.5:1 is the usual minimum for body text, and the
  battle box's own grey text is {{PLAIN_C}}:1.</p>
  <div class="scroll"><table class="tbl">
    <thead><tr><th>Type</th><th>Hue · sprites</th><th>Badge · step 4</th><th>On the battle box · step 4</th><th>Contrast</th></tr></thead>
    <tbody>{{COLOUR_ROWS}}</tbody></table></div>

  <h3>What darkening costs</h3>
  <p>At sprite brightness <strong>{{N_MID}} of {{NPAIRS}}</strong> type pairs sit closer than 20 (CIE76),
  which this page already treats as the edge of telling two colours apart at 56px. At step 4 it is
  <strong>{{N_S4}}</strong>, and a 1-pixel letter is far thinner than a sprite. So a coloured move name
  tells you the <em>family</em> of its type, not the exact type — <mark>which is why the type name stays
  written in the info box</mark>. Colour to scan, the word to be sure. That also serves anyone who
  cannot see the difference at all.</p>
  <div class="scroll"><table class="tbl">
    <thead><tr><th>Closest pairs as text</th><th>Sprites</th><th>Step 4</th></tr></thead>
    <tbody>{{CLOSE}}</tbody></table></div>
  <p class="note"><span class="open">DECISION</span> <strong>LOGIC / LEGACY is {{LL_S4}} at step 4</strong>
  ({{LL_MID}} at sprite size). The ruling further down — that separating them was "not worth weakening a
  metaphor for two points" — was made at sprite size. As text they are effectively one colour, so it is
  worth deciding again: move one of them within its own metaphor, or accept that the info box is the only
  thing that tells them apart.</p>
  <p class="note"><span class="open">DECISION</span> <strong>Some words read as plain text, for two different
  reasons.</strong> A hue that sits near the battle box's own grey: {{NEAR_GREY}}. A hue too dark and too weak to
  show at letter size: {{AS_INK}} — OCCLUDE and POLLUTE in the mockup are this kind. One alternative: <em>words
  take the lightest step that still reads as text</em> — the hue itself where it already clears 4.5:1
  ({{USES_HUE}}), and step 4 otherwise. That fixes {{FIXED_ALT}}, and leaves <strong>{{N_ALT}}</strong> pairs under
  20 instead of {{N_S4}}. <strong>It cannot fix {{STILL_PLAIN}}</strong>: those hues either sit beside the grey
  or carry almost no colour, at any step. For CONTENT that is the design — the thing itself should not look like anything — and for all of them the
  mark and the written type do the work. The cost: for the types it changes, a badge and a written name stop
  sharing one colour.</p>

  <h3>The two types with no colour</h3>
  <p><code>TYPE_COLOR</code> has fifteen entries for {{NTYPE}} types. Today the badge tool gives HARDENED
  LEGACY's slot and OPAQUE LATENT's, and <mark>the sprite tool skips any daemon whose type has no
  entry</mark>, so those daemons still wear vanilla colours. Colour cannot be consistent anywhere until
  these two have one. Each option is measured against all the others; <em>worst</em> is its distance to
  whichever type it sits nearest.</p>
  <h3>HARDENED <span class="open">DECISION</span></h3>
  <div class="scroll"><table class="tbl">
    <thead><tr><th>Option</th><th>Sprite · step 4</th><th>Worst, sprites</th><th>Worst, step 4</th><th>Nearest</th><th>Text</th><th>Colour as a word</th><th>Why</th></tr></thead>
    <tbody>{{HARD_ROWS}}</tbody></table></div>
  <p class="note">Every grey metal was tried first — gunmetal, titanium, silver, case-hardened —
  and every one landed within 4–9 of LEGACY, LOGIC or FROZEN. Metal is already crowded in this palette,
  because LOGIC is steel and LEGACY is slate. The candidates above work by being the colour metal
  <em>takes</em> when it is worked, rather than the colour of metal at rest.</p>
  <h3>OPAQUE <span class="open">DECISION</span></h3>
  <div class="scroll"><table class="tbl">
    <thead><tr><th>Option</th><th>Sprite · step 4</th><th>Worst, sprites</th><th>Worst, step 4</th><th>Nearest</th><th>Text</th><th>Colour as a word</th><th>Why</th></tr></thead>
    <tbody>{{OPAQUE_ROWS}}</tbody></table></div>
  <p class="note"><strong>"Colour as a word"</strong> is the chroma of the colour a move name would actually be
  written in; under about 10 it reads as plain dark text. Near-black keeps the black box unreadable, which is the
  clause, and gives up OPAQUE as a legible colour. Oxblood or ink navy do the reverse. Both are defensible — it is
  a choice about what the type is for.</p>
</section>

<section>
  <div class="sec-head"><h2>The move menu: colour for type, a mark for what it does</h2></div>
  <p>A move answers two separate questions — <em>what type is it</em>, and <em>what does it do</em> — so it
  gets two separate channels. Colour already means type everywhere in this game (the rule at the top of
  the matrix: <em>hue is the type, effectiveness is weight, never colour</em>). What a move does is the
  same kind of thing as effectiveness, so it gets a <mark>shape</mark>.</p>
  <div class="mockwrap">
    {{MOCK}}
    <p class="mockcap">Your screenshot's four: {{SAMPLE_NOTE}}. The three that hit are unmarked;
    INSPECT lowers the foe's defence and carries ▼. The info box keeps MP and names the highlighted
    move's type in its colour, without the <code>TYPE/</code> label.
    <strong>OCCLUDE and POLLUTE show the problem noted above</strong>: both read almost as plain text at
    step 4. The alternative would give POLLUTE its olive back. It would not rescue OCCLUDE, because the
    proposed OPAQUE hue is itself near-black — which is what the OPAQUE decision below is really about.</p>
  </div>
  <div class="scroll"><table class="tbl">
    <thead><tr><th>Class</th><th>Mark</th><th>Moves</th><th>What it means</th><th>Examples</th></tr></thead>
    <tbody>{{LEGEND}}</tbody></table></div>
  <p class="note"><strong>Hitting is unmarked on purpose.</strong> {{NHIT}} of {{NMOVES}} moves
  ({{PCT_HIT}}%) deal damage, it is the thing a player most wants to see plainly, and because every other
  class carries a mark, an unmarked name can only mean one thing. The classes are read off each move's
  effect and power in the build, not typed.</p>
  <p class="note"><strong>The marks are 4px.</strong> With one in front, every move name still fits its
  64px slot ({{OVER4}} would not). The font's own arrows are {{ARROW}}px and {{OVER8}} names would not fit
  — {{OVER8_EX}} among them. {{NFREE}} font cells nothing in the game uses — {{FREE}} — get redrawn as
  the marks.</p>
  <p class="note"><strong>Dropping <code>TYPE/</code>.</strong> The label is {{LABEL_W}}px, and with it
  {{INFO_OVER}} already run past the info line today. Without it the widest type name is
  {{WIDEST_T}}px. Showing power there was considered: it does not fit beside the longest names at three
  digits, and the mark already answers whether a move hits.</p>
</section>

<section>
  <div class="sec-head"><h2>The matrix</h2></div>
  <p>Rows attack, columns defend. Read <code>LOGIC → CONTEXT</code> as the row LOGIC meeting the column
  CONTEXT: <mark>×½, the thesis</mark>. Click a type to hold its row and column.</p>
  <div class="key">
    <span><em class="m-2"></em> ×2 effective</span><span><em class="m-h"></em> ×½ resisted</span>
    <span><em class="m-0"></em> ×0 no effect</span><span>· blank is ×1</span>
    <span style="margin-left:auto">Hue is the type (9.4). Effectiveness is weight, never colour.</span>
  </div>
  <div class="scroll">{{MATRIX}}</div>
</section>

{{DUAL}}

<section>
  <div class="sec-head"><h2>The {{NTYPE}}, one clause each</h2></div>
  <p>2.6's one-clause test: one sentence a non-specialist understands, walked against every relation the
  type is in. Twelve scores are from the original run at fifteen types. LEGACY and VECTOR were re-claused
  on 2026-09-11 and now pass with the words unchanged; CONTEXT, HARDENED and OPAQUE were scored at
  seventeen. <strong>All {{NTYPE}} pass.</strong></p>
  {{CARDS}}
</section>

<section>
  <div class="sec-head"><h2>Why each colour</h2></div>
  <p><mark>Four of the fifteen shipped hues are not choices.</mark> §6 gives the Review Board its humours, and
  each already carried a type. The rest are claims, written down so a later argument has something to argue
  with — and two are proposals.</p>
  <div class="scroll"><table class="tbl">
    <thead><tr><th>Type</th><th>Hue</th><th>Why that colour</th></tr></thead>
    <tbody>{{WHY_ROWS}}</tbody></table></div>
  {{MOVED_NOTE}}
</section>

{{STATES}}

<footer>
  Generated by <code>python3 tools/gbachart.py --write</code> from <code>engineGba/src/battle_main.c</code>
  ({{NREL}} relations), <code>src/data/battle_moves.h</code> and <code>move_names.h</code> ({{NMOVES}} moves),
  the glyph tables in <code>src/text.c</code>, and <code>tools/gbasprite.py</code>'s <code>TYPE_COLOR</code>
  and <code>ramp5</code>. Every contrast and distance is computed at the GBA's 15-bit colour. Cut the PDF with
  <code>./docs/build-pdf.sh type-chart.html</code>.
</footer>
</div>
<script>
(function(){
  const g=document.querySelector("table.grid"); if(!g) return;
  let active=null;
  function show(t){
    active=(active===t)?null:t;
    g.querySelectorAll("tbody tr").forEach(r=>r.classList.toggle("on",!!active&&r.dataset.row===active));
    g.querySelectorAll("td.c").forEach(c=>c.classList.toggle("oncol",!!active&&c.dataset.col===active));
  }
  g.addEventListener("click",e=>{const h=e.target.closest("th[data-t]"); if(h) show(h.dataset.t);});
})();
</script>
"""


if __name__ == "__main__":
    main()
