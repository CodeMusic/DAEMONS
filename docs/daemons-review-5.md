---
title: The Fifth Review
---

# About this review

**The Fifth Review** was asked for in one sentence: *is everything cohesive, does it flow in the game, and does it
accomplish what it set out to do?* It reads the design repo and its plans, not the ROM. It comes one day after
the Fourth, so it does not repeat the Fourth; it checks what the Fourth missed, what has happened to its findings,
and where the project's own documents disagree with each other.

| | |
|--|-------|
| **Read against** | design bible **v11.338** (`docs/vision.md`, 9,259 lines) at DAEMONS `036d765e`, 4 November 2026 |
| **Also read** | `docs/TODO.md`, `docs/CHANGELOG.md`, `docs/lineage.md`, `docs/engine.md`, the four earlier reviews, the school, guide, subtle and hermetic layer texts, the manuals, the wiki, the newest release notes |
| **Not read** | the three engine forks, the companion and the playground (absent in this checkout), and no ROM was built or played |
| **How** | four lenses read separately and then put together: the player's path end to end; the mechanics against the thesis; the plans and the process record; drift between the documents. Every finding was re-checked against the bible's own lines before it was kept |

**What this review never prints.** The four things the player is meant to work out appear nowhere below. Where a
finding is that one of them is readable in a tracked file, the page says only that it is, and the lines went to the
author directly.

# The verdict, up front

**The design accomplishes what it set out to do, and it did so about six weeks ago.** The thesis is in the chart,
the chart is identical across both editions, Act 1 is a fable with its last line removed, and the ending is an
argument won by re-reading. That was the goal in section 0, and the record shows it met.

**What has happened since is that the project keeps writing the last line back in.** Not in dialogue, which craft
rule 1 guards well, but in systems: leaders who say what a MARK taught, INSIGHT lines filed in the player's hand, a
GUIDE entry the bible itself calls "the thesis's shape with neither of its words", a virtue week on the MARKS, and a
third book that is allowed to say the moral and now mends a town. Each is defensible. Together they are the moral,
written five times, in a game whose form is defined by withholding it once.

**And the plan is not pointed at finishing.** The bible's own definition of done, *played through and the record
read*, has had one ticket since September and it has never run. The four commits after the Fourth Review were all
outside the game. The eight misfiled tickets, the stale version anchor every session reads first, and the dead
release line in the README are all still as the Fourth found them.

Three things the Fourth Review missed, each checkable, lead the findings below: three of the four secrets are
readable in tracked public files; Benchmark 1 has no mechanic, because its ability was misread; and the ending has
two stall points the design never placed.

# Does it accomplish what it set out to do?

Section 0 names the goal twice: the thesis argued in five registers and never in dialogue, and the shape of
*a fable with its last line removed*. Section 8 adds the scope rule: the slice before the bestiary.

| Set out to do | Done? | Evidence |
|---|---|---|
| **The slice before the bestiary** | **Yes** | 8.1 built and played; 770 unattended steps; every one of the 386 named and placed (9.27); Act 2's six scenes, the ending and the second joining in the ROM |
| **The chart as an argument** | **Yes, for content against context** | LOGIC ×½ CONTEXT holds every lens; 2.6 scores 11/11 for CONTEXT; the chart is byte-identical across editions |
| **The chart as *this* thesis** | **Partly** | The title words CONTENT and CONTEXT never meet in the chart; *emotion* and *colour* reach play only through 9.4's hue, which the bible calls "a label, not a model" (`vision.md:1290`). What a player can infer is *rules bounce off framing*, which is the CFM's symmetry and is sound; it is not "emotions are the colour of context" |
| **Never said in dialogue** | **Yes, in the mouths** | 338 versions and no NPC explains it. The one planted exception (the kid in Verdigris, craft rule 2) is not in the ROM (Fourth Review, finding 27) |
| **The last line withheld** | **Yes in Act 1 and the ending; no in the systems around them** | See *The moral, written five times* below |
| **Lessons mechanical (craft rule 5)** | **Three of eight** | See *Benchmark 1 has no mechanic* and the table under it |

So the honest sentence is: **the game argues content against context beautifully and never says so; the layers
added since late September say the emotional half out loud, in colour grids, seasons, spirits and books, in exactly
the register craft rule 1 forbade for dialogue.**

# Findings

Ranked by how much each matters to the game flowing. Tags are the Third Review's.

## BREAK: three of the four secrets are readable in tracked files

The 2026-09-27 redaction (`CHANGELOG.md:481`) moved the four to `docs/private/` and rewrote the lines left in TODO,
lineage, the changelog and two reviews. **Three of the four still stand in tracked files**: the Witnesses' lock and
its number in the lineage, twice, and derivable from the public bible; the parentage in the public bible and three
changelog entries; the dated order in the school document's notebook table and the Third Review. The engraving is
clean. The exact lines were given to the author directly and are not printed here. **Re-run the redaction over
`lineage.md`, `vision.md`, `CHANGELOG.md`, `school.md` and `daemons-review-3.md`, and add the sweep to the
`check_lexicon` family so it cannot drift back.** Also: `docs/posts/README.md:45-47` lists three secrets, not four.

## BREAK: Benchmark 1 has no mechanic, because DURABLE was misread

5.3 and 5.3b say CAIRN needed nothing because "HEAP, STACK and MONOLITH cannot be knocked out in one blow, at any
level" (`vision.md:5169`, `:5097`; `CHANGELOG.md:3794`). But 2.11 defines DURABLE as vanilla STURDY, "negates
one-hit knockouts" (`vision.md:1931`), and in Gen 3 that ability blocks only the four one-hit-KO routines
(`:1891`). It does not survive a strong hit. A level-40 WRITE one-shots HEAP. Nothing in the changelog rebuilds the
ability. **The first lesson in the game, "a record does not go down to one hit", is a wall with a lesson written
on it.** The fix is small and already named by the design: give DURABLE the later generations' rule (survive any
hit from full HP) in the damage calculation, and 5.3's sentence becomes true.

While here, craft rule 5 by the bible's own descriptions:

| # | lever | survives grinding? |
|---|---|---|
| 1 CAIRN | DURABLE | **No** (above) |
| 2 BASIN | LEFTOVERS and RECOVER, a room with no gradient | Partly: the room is real; "more power does not break a loop" (`:5185`) fails once one hit passes half |
| 3 GAUGE | priority on every member | No: "You will win the damage race" (`:5201`) |
| 4 TRELLIS | screens and status | Partly, and the overfit state is still OPEN (`:1988`) |
| 5 TILT | THRASHING | **Yes**: status ignores level |
| 6 MATTE | ENCORE | **Yes** when it locks a resisted move |
| 7 ANNEAL | variance | No: "You can beat him at a high level" (`:5267`); temperature as a room is OPEN (`:1996`) |
| 8 SCORN | the max roll | No as a mechanic (about +7%); yes as a meaning |

The bible knows this for 4 and 7. It does not know it for 1.

## BREAK: two stall points on the critical path, neither designed

- **The ending's second gate is missing from the ending.** 4.34's order (`vision.md:4503`) reads "the machine
  completes, DOLDRUM CAVE opens, S.T.A.R.R." But the cave has two gates (T-251, T-252; 0.7 `:353`): without the
  FIRST understanding, arrived at by reading the **seventh TANOBY chamber**, the player meets a REMNANT and wakes
  in bed (T-254). TANOBY is not named in 4.34 at all, and 8.2a names it only as content, never as the key. The one
  in-game pointer is BASIN's post-win line (0.7 `:402` admits the FIRST had "no sign, no dream, no line" before it).
  A player who does not revisit Doldrum's gym after the Review Board, and does not solve a vanilla optional boulder
  puzzle, has a dead end dressed as a dream, with T-347's three-heals backstop as the only net. **Put the pointer on
  the path: S.T.A.R.R.'s own terminal register already exists for this.**
- **Act 2 opens on sixty daemons owned** (9.17 `:8466`), "the one nobody remembers". The finale of a game whose
  argument is that the Index cannot hold what matters is gated on a collection count, recorded as a debug finding
  and kept because "both preconditions are real". It is never discussed as a design choice. Decide it, in either
  direction, and write it down.

## BREAK: the moral, written five times

Craft rule 1 holds in dialogue. It has been spent, without being logged as spent, in these places:

1. **The leaders' wisdom** (0.7 `:398`): after a win a leader says what the MARK taught and what to come back
   understanding. 0.7 says "nobody says the sentence; the lines show the gap." They also point.
2. **INSIGHT** (0.7 `:409`): one line per MARK and ROOT pair, in the player's hand, filed in the NOTEBOOK. "Rule 2
   amended, not reversed." It is the fable's last line, seven times, then an eighth.
3. **The GUIDE's INTEGRATION entry** (`:4786`), DRAFT, "the thesis's shape with neither of its words", on a shelf
   reachable in Act 1 because the first ferry runs after Benchmark 7 (Fourth Review, finding 25).
4. **The virtue week on the MARKS** (T-346, T-318, 9.21 `:8686`): GREED, LUST, WRATH printed on the badges, a second
   moral system riding the chart's furniture, with no column in section 5's table.
5. **The third book family** (4.39, 4.40): the one sanctioned exception, which the Fourth Review showed has lost
   both its warrants and grown from one book to three, and now restores a town's colour.

Each is small. The Fourth Review's finding 18, *thirteen systems and one quiet ending*, is the same thing seen from
the player's side. **Rule once on how many times the moral may be written, and strike the rest.** The cheapest
ruling is the Fourth's: bind the mended book face to face with no third voice, and keep the leaders at pointing.

## DRIFT: the thesis's emotional half is said by systems, four times over

A daemon now has four channels for *how well have you kept it*: friendship as saturation (8.6 `:7533`), four
feelings fading over hours on a coloured grid (`:6466`), SPIRITS as a class and a lean (`:5054`), and THE THREE
derived from the first two (`:4918`). The bible's own gloss, "feelings are the weather, SPIRITS is the climate",
concedes one quantity at two timescales, and friendship is already the climate. **A player cannot tell a dull sprite
from a dark one from a sad face; all three come from the same lost battles and boxed days.** And *four* now appears
five times as one thing: the humours, the Review Board, the colour anchors, the seasons, the feelings. The Open log
closed "are the humours too neat?" by saying the neatness is the Board's error (`:9240`), then built the Board's
error into the calendar and the follower's face as truth. Collapse to one visible quantity, or say which one is the
lie.

## DRIFT: contradictions the Reversed table does not hold

- **8.4's trap vs 0.4's ruling.** 8.4 says "do not make CONTENT's Index measure content and CONTEXT's measure
  context" (`:7137`); 0.4 ruled on 2026-09-04 that CONTEXT's entry is "who framed it, who chose, who is not in the
  record" (`:121`). 0.4's defence answers a narrower objection than 8.4 raised. Strike one.
- **8.6's restraint clause** still stands: "colour at two sources; a third makes it a system and a system invites
  explanation" (`:7491`), while colour now carries type, streaks, friendship, SPIRITS, feelings, week, month, season,
  watch, purple noticings, Halftone grey and NEXUS paint. Not reversed, buried.
- **ORPHAN**: 4.5 (`:3508-3544`) presents it as the tower's real species with the blank entry; the Open log
  (`:9253`) closes it the other way (REMNANT to COREFILE, MISSINGNO's entry). The body is stale.
- **Scorn after Benchmark 8**: 8.2a (`:6612`) "he is not the same"; 4.37 (`:4866`) "SCORN is unchanged".
- **4.1's row** says the opening "states the thesis in the abstract" (`:2288`) against 0's "never once in dialogue".
- **Still-OPEN markers on settled things**: 4.33's placement (`:4467`), 4.5's "meet Scorn before the tower?"
  (`:3546`), 4.3's "Ty is not in the endgame" (`:3419`). MATTE is *she* at `:5253` and *his* at `:8692`.
- **8.1 still says "all 15"** (`:6281`); the ROM has run seventeen since 2026-09-10 and the Third Review flagged it.
- **CONTENT / CONTEXT is doing seven jobs**: two types, two editions, two Indexes, day and night, two hemispheres,
  serial and parallel, bottom-up and top-down, a move register. A player meets CONTEXT as a type LATENT beats and
  as the cartridge whose winter is summer, and nothing in play ties the readings together. **BIND** is sold on
  carrying *bond* (1.5) and 8.6 then makes bound and bonded opposites (`:7544`).

## DRIFT: the plans

- **The Fourth Review is unanswered.** No 8.8 rules on it, no ticket carries its top item, and its three cheapest
  fixes (the eight rows under Closed, `CLAUDE.md:20`'s v11.296, `README.md:27`'s v11.335.6) are as found. The four
  commits since are a press kit, two audio-book commits and a textbook PDF: all outside the game, against its freeze.
- **The Third Review's accepted sweeps were never ticketed**: 8.7 "queued as sweeps" the colour, tempo and SLEEP
  sweeps, re-sourcing Brazen's B-section and 4.10's dates; TODO and CHANGELOG carry none. Its "ideas taken"
  (CONVICTION, Al's party desaturating, the Index sprite keeping its saturation) have no hits outside 8.7. The
  vocabulary budget it asked for was never ruled, and 8.7 promised to list the refusals.
- **T-50 has waited 39 days** while 44 bible versions and about 120 tickets landed. It is the only ticket that is
  the bible's definition of done.
- **Done and never struck**: T-456 (built 2026-10-26), T-457 (approved, DRAFT marks off), T-433 (built 2026-10-22),
  T-449 (released; the Fourth Review's table still calls the region map vanilla, which is one correction to it).
- **"Open holds a question, TODO holds a job" is broken both ways**: the Open log's first live entry (`:9173`) is a
  list of DRAFT words to choose; TODO's "Wants a decision first" still lists PKRS, which the log closed as MEME on
  2026-10-29; T-465's row files a bible question as a ticket and says so.
- **Scope, counted** (T-400 to T-520, 121 rows): about 14 wholly outside the game, 9 game-side halves of companion
  features, about 20 the three-book layer, 78 inside the game, and of those more than half are fixes found by
  code reviews or the theatre rather than progress toward 8.1 or 8.10. The design converges; the plan diverges.
- **Stale anchors a fresh session reads first**: `CLAUDE.md:2` ("a `pokered` total conversion"), `CLAUDE.md:20`,
  the T-267 to T-299 reservation (`TODO.md:38`) with ids at T-520, `docs/README.md:20` ("eight traps"; there are
  forty-three), `docs/README.md:24` and `docs/school.md:3` ("nothing in here is built"; fourteen groves and seven
  floors are in the ROM), `docs/README.md:6-7` linking two bible PDFs that do not exist.

## DRIFT: the smaller document drift

- `README.md:27` and `wiki/Home.md:78` name v11.335.6 as newest; v11.337.4 shipped 2026-11-02.
- `wiki/Editions.md:31` says 395 Index entries; the bible, README and the wiki's world page say 398.
- `ROM RELEASE/v11.337.x/v11.337.1/RELEASE_NOTES.md:41` quotes a commit that prints the frightening word, in the one
  file that goes to GitHub Releases. One word to cut.
- `wiki/The-Hermetic-Layer.md:25-26` states the third book's gate as rumour in the same words T-506 is sweeping; add
  it to the ticket. `docs/books/README.md:22` hints the vault's password from text the repo already holds.
- `docs/TODO.md:623` quotes a family member's age; `CHANGELOG.md:521` sets three family members' full names beside
  in-game details. Deliberate (the credits), but the one place a real name sits next to a biographical fact.
- `docs/still-vanilla.md` is about names, calls itself stale, and `docs/README.md:27` lists it as current.
- `docs/eudaimon-layer.md` is named by T-519 as if present; it is the job's output. `docs/TRADING.md` at
  `TODO.md:552` is the companion's file with the repo dropped from the path.

# What is excellent, and should not be touched while the above is fixed

- **The CC-7 fuse**, the gold leaf that lifts by word order, the note that never changes, the sealed PEER REVIEW.
- **The RESEARCH NOTEBOOK's authored order**, and the school's exam as the honest inverse of the rigged one.
- **THE SUBTLE LAYER's register**: attributed, humble, logged. It is how the other books should speak.
- **The engineering record**: generator drift guards, `check_reach`, forty-three traps by symptom, the fresh-clone
  byte compare. No fan project this reviewer knows keeps books like these.

# What to do, in order

The first five finish; none is new design.

1. **Write 1.0 into the bible** (a new 8.8), adopting the Fourth Review's checkable definition, and rule on its 46
   findings the way 8.7 ruled on the Third's, refusals included.
2. **Play it through, once, each edition**, from a new game to THE ANNEX, and read the record. Close T-50 by
   acting on it. Make the run the gate for every new subsystem.
3. **The secrets sweep**, this week: the five files above, then a check that greps for them on every push.
4. **Three small mechanics**: DURABLE survives from full HP; a pointer to the seventh chamber in S.T.A.R.R.'s
   register; a decision on the sixty-daemon gate.
5. **Rule on the moral**: how many places may write it. Bind the mended book face to face; keep the leaders at
   pointing; put INSIGHT behind THE ANNEX or cut it to one line.
6. **Then** the first-screen vanilla (font, tiles, battle themes) and Corpus's own barks, which both reviews name.
7. **Tidy the record so a session can trust it**: the misfiled rows, the four done-but-open tickets, the stale
   anchors, the three contradictions in the Reversed table, and `CLAUDE.md`'s first line.

Everything else, the books, the decks, the devices, the iPad, is 1.x, and the design will be better for having been
played before it is extended again.

*Checked against design bible v11.338 on 4 November 2026. Read from the documents only; no ROM was built or played.*
