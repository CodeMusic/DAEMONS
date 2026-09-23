# THE SCHOOL, THE EXAM, AND THE RESEARCH NOTEBOOK

*A design document.* **Nothing in here is built.** ***Revised 2026-09-22 on the user's answers*** — *PERCEPTION cut,
CATEGORIES in, a ninth DRIVER and seven hidden groves added, the notebook from CAIRN.* *Proposed 2026-09-22, from the user's brief,
against `vision.md` v11.237, the rock opera (`docs/archive/additional rock-opera song lyrics
backup.rtf`), `lineage.md` and `story.md`.*

> *Internal.* It names the 4.10 sequence and the shape of the ending, both of which `CLAUDE.md`
> keeps out of public writing. **It contains no exam question and no journal line** — those are
> writing, and writing needs approval before it ships.

---

## 0. The one sentence

***4.10 is the best thing in this game and it happens once.***

**A player stands in a ruined lab, reads dated paperwork in the wrong order, and reconstructs an
event nobody tells them about.** *That is the whole method of this project, executed on one map.*

**The RESEARCH NOTEBOOK is 4.10 made into a system**, and **the SCHOOL is the place that teaches a
player how to read one.** *They are one feature. The school produces a reader; the notebook gives
that reader something to read.*

---

## 1. Why a school is allowed to teach, and this is not craft rule 1 being suspended

***9.16 already settled this and did not know it was settling it twice.***

> **TEACHY TV is the one system in this game that exists to explain the game**, which makes it the
> one place where explaining is not a craft-rule-1 violation.

**A school is the second.** *Craft rule 1 forbids a character explaining the colour–emotion link.
It has never forbidden a character explaining **a thing that is true about minds**,* and a building
whose entire function in the fiction is instruction can instruct without the author's hand showing.

***The rule that replaces it, and it is stricter:*** **every floor teaches something that is
independently true in psychology and in machine learning, and no floor ever joins them up.** *The
join is the player's, and it is the only thing they are not given.*

**And craft rule 6 does the protecting.** *Corpus employees are cheerful and absurd; a school's are
pedants, enthusiasts and one person who has misunderstood the subject in an interesting direction.*
**A player who is laughing is a player who is not being lectured** — which is why the SPELLING joke
below is load-bearing and not decoration.

---

## 2. Where it goes, and how much of it already exists

### The city was named for this six months before anybody thought of it

| | |
|---|---|
| **Viridian → `CALLOW CITY`** | *"green + unripe, **untested**"* (3, the map table) |
| **The building** | `data/maps/ViridianCity_School` — **it is already in the ROM** |
| **Benchmark 8** | *locked all game.* **The one city that measures you is shut** |

***A school where you sit an exam, in the city whose name means untested, behind the one Benchmark
that never opens.*** **Nobody planned that and nothing in the game will remark on it.**

### Four mechanisms the feature needs are already built

| what the brief asks for | what already exists | where |
|---|---|---|
| *"the section name readable right away, without hitting anything"* | **`ShowFieldLabelPopup(const u8 *text)`** — a framed label that slides in at the top | `map_name_popup.h`, **T-196** |
| *"hitting A says a bit more"* | **the blackboard is already a `multichoicegrid` of topics** | `ViridianCity_School_EventScript_ChooseBlackboardTopic` |
| *a collected, saved, per-entry-unlocked reader* | **HEARSAY** (the Fame Checker): 16 subjects × 6 entries, each with its own *where you heard it* line, all saved | `src/fame_checker.c`, `struct FameCheckerSaveData` |
| *re-reading a line you missed* | **R = AGAIN**, labelled `ECHO` | **T-196** |

***So the first floor is a WRITING job, not a map job.*** **Floors two and up are map jobs.** *That
distinction is the whole of the build order in §13.*

---

## 3. The floors

**Seven sections — settled on the user's answer.** *Seven notes, seven colours, seven floors.* **Each
is a word that is load-bearing in cognitive psychology AND in machine learning, and which a player
can use in a battle that afternoon.**

| # | section | what it teaches | the two readings, never joined | the floor's joke |
|---|---|---|---|---|
| **1F** | **LANGUAGE** | naming, ambiguity, what a word does when you say it | *a token, and a label a mind applies* | **SPELLING.** *An NPC certain words are under a spell — that saying one manifests more than a picture of it.* **Wrong, and wrong in the right direction** |
| **2F** | **ATTENTION** | what gets weight, and therefore what is missed | *weighting, and salience* | *the teacher who has been explaining to an empty half of the room* |
| **3F** | **MEMORY** | storing, recalling, decay, interference, and that recall rewrites | *retrieval, and reconsolidation* | *a student who has revised the same page eleven times and can only recite the eleventh revision* |
| **4F** | **CATEGORIES** | a category has a middle and no edge; things belong *more or less* | *prototypes, and classification* | *a student whose filing system has a drawer for things that fit nowhere,* **and it is the biggest drawer** |
| **5F** | **LEARNING** | neurons connect, a connection has a **strength**, a **bias** shifts how easily one fires | *the brain, stated plainly.* **The other reading is never named** | *somebody who learned one thing extremely well and now sees it everywhere* |
| **6F** | **BIAS** | the named biases and fallacies, with the framing effect given a full period | *cognitive bias, and the b in y = wx + b* | *a debating pair who each name the other's fallacy correctly and neither notices their own* |
| **7F** | **ERROR** | surprise, correction, and that being wrong is where the change happens | *prediction error, and learning from it* | *the marker who is delighted by a wrong answer and cannot explain why to the student* |

### The order is what happens to a piece of information

**Named, noticed, kept, sorted, changed, bent, corrected.** *Language is the medium the other six are
taught in, so it is on the floor you walk into; every floor above it is one more thing that happens
to what came in.* ***And the top floor is ERROR, where the TEXTBOOK is*** — **the last thing the
building teaches before it tests you is that being wrong is where the change happens.** *Nobody says
why that is the right last lesson for an exam.*

### 4F sits under the Index's feet

***Crystal built the Index as a taxonomy engine*** (4.2), **and it sorts every daemon into a category
page.** *A floor that teaches that categories have a middle and no edge is teaching the player the
first thing that is wrong with the most-used screen in the game* — **and it is taught as a joke about
a filing drawer.** *Nothing on the floor mentions the Index.*

### PERCEPTION was cut, and the user's reason is better than the one it replaced

***The first draft kept PERCEPTION and fenced it*** — *no line on it could contain `emotion`,
`feeling`, `mood` or `context`.* **The user cut it on a different ground, and the ground is the one
that matters: a floor that has to be careful has to be SERIOUS, and seriousness is what removes the
cover.** *Craft rule 6 is that comedy is the best cover for a thesis* — **so a floor that cannot
joke cannot hide anything, and the damage would not stop at the floor.** ***A fence was the wrong
tool. The right one was not building the room.***

### Why LANGUAGE is on the floor you walk into

**It is not the bottom of the stack.** *Perception is.* **It is first because it is the layer the
other six are taught IN** — *you cannot be told about attention without words for it* — and a
school puts that first as a matter of instruction rather than architecture.

*A teacher says roughly that, once, and does not make anything of it.*

### 5F is the floor the brief was right to worry about

***The user's instinct was correct: a "Machine Learning" floor would be the author talking.***

**`LEARNING` is the fix, and it is not a dodge.** *Neurons connect to neurons; a connection carries
a **strength** that says how much one firing should move the next; a **bias** shifts how easily a
neuron fires at all; and feedback changes all of it over time.* **Every one of those sentences is
true about a brain and is taught as such**, and *weights and biases are learned by a player who was
never told they had learned them.*

***The floor never says the word `network` in the other sense, never says `model`, never says
`training`, and never mentions a machine.*** **If a line on this floor would still be true with the
word `computer` in it, the line is wrong and gets rewritten.**

---

## 4. The furniture of a floor — the repeatable unit

***Every floor is the same five objects.*** **Build the set once; a new floor is then writing plus a
layout.**

| | what it is | mechanism |
|---|---|---|
| **The label** | the section name, **read without pressing anything**, as you arrive | **`ShowFieldLabelPopup`** on the map's `on_warp_into_map` script — *already built, T-196* |
| **The PLACARD** | a standing sign by the stairs. Drawn legibly in the tiles, **and** readable on A | *A gives: the section name, two sentences on what the floor is for, and* ***"the syllabus is on the desk."*** |
| **The DESK** | the teacher's desk. A on it takes **the SYLLABUS** | *writes one RESEARCH NOTEBOOK entry.* **Not an item** — see §5 |
| **The BOARD** | the blackboard: **the actual lesson**, as a topic menu | *vanilla's `multichoicegrid` already does this, with the status conditions in it today* |
| **Three NPCs** | one who teaches straight, one who is funny and wrong in the right direction, one who is funny and right | *craft rule 6 doing the protecting* |

***The board is the one that matters.*** **Every exam question is drawn from a board topic and from
nowhere else** — *so a player who read the boards can pass, and a player who did not is told
exactly where to go and can go there.* **A test whose material is not published is Scorn's test.**

---

## 5. The SYLLABUS — a notebook entry, not an item

***Seven items for seven syllabi is seven item slots spent on a filing decision.***

**A syllabus is an entry in the RESEARCH NOTEBOOK's `SCHOOL NOTES` section**, taken off the desk,
holding: *the section name, what the floor covers, the board topics listed, and the pass mark.*

***The pass mark is printed on the syllabus, on the first page, before the exam exists.***

**That is the single most important sentence in this document.** *Scorn designed standardised
evaluations and rigged them so that rivals failed* (4.4); *he "developed basic tests" and did not
say what they measured.* **This school publishes the criterion in advance, publishes the material,
lets you leave the exam and come back, and loses nothing when you do.** ***It is the honest version
of the thing he corrupted, and the game never once says so.***

---

## 6. The TEXTBOOK

**One key item, on the top floor**, where the brief put it.

~~***What it actually does, and this is the cheap answer rather than a compromise:*** **taking the
TEXTBOOK unlocks the full text of every board topic, on every floor you have visited, inside the
RESEARCH NOTEBOOK.** *Using the item opens the notebook at `SCHOOL NOTES`.*~~

~~**One reader, not two.** *A second full-screen text UI would cost a second screen's worth of code
and give the player a second place to look for the same sentence.*~~ ***REVERSED on playtest,
2026-09-22 (T-223).*** **The user played it and the objection was to the reader both books shared**:
*the message box, two lines at a time, with no idea how many pages were left.* **So both books got a
full screen, and once the notebook had one the textbook's was a small step more** — *the "second
screen's worth of code" turned out to be one file, `book_reader.c`, drawing both.*

***What it does now.*** **The TEXTBOOK opens on an open book at `CONTENTS`**: *the seven floors as
chapters, four on the left page and three on the right, each with its board's chalk mark as a small
slate* (`tools/genbookicons.py`). **The D-pad moves across the contents as it would across a real page;
A opens a chapter** — *its five topics on the left, its slate drawn large on the right* — **and A on a
topic prints it across the spread, left page then right.** *LEFT and RIGHT turn to the neighbouring
chapter or topic; B walks back out one level at a time.* **A floor not yet stood on is printed faintly,
its slate a ghost, and will not open.** ***The boards are no longer copied into the notebook*** — *a
book does not need a copy of itself in another book.*

*And it means the exam is always studiable from anywhere*, which is what makes the leave-and-return
rule in §7 mean something.

---

## 7. THE EXAM

### The trigger, and the state it puts the building in

| | |
|---|---|
| **1** | You take the **TEXTBOOK** on the top floor |
| **2** | **On the way out**, at the door, you overhear the teacher — *exam season; come back when you are ready.* **You do not reply.** The line closes and your character keeps walking |
| **3** | **From then on the school is in `EXAM_PENDING`**: *the NPCs are in their seats, the teacher is at the front, the stairs are refused* — **"take your seat"** — *and there is one empty desk* |
| **4** | A on the paper on that desk: ***are you ready?*** **Yes or no, and no is free** |
| **5** | **You may leave the building at any time**, before or during. *Re-entering finds the same state and the same answers* |

***The overheard line is not a cutscene and the player is not asked to agree to anything.*** *It is
the one beat where the school stops being a place you visit and becomes a thing that expects you* —
**and the game's answer to that is to let you walk out of it and never come back if you like.**

### The screen

```
  ┌─ SECTION 3 of 7 ── ATTENTION ──────────────────  L / R ─┐
  │  ✓  1. What a cue does                                  │
  │  ✓  2. Two things at once                               │
  │     3. The half of the room nobody looked at            │
  │  ✓  4. Why a list has a middle                          │
  │     …                                                   │
  │                                                         │
  │            FINISH EXAM            EXIT EXAM             │
  └──────────────────── 38 of 112 answered ─────────────────┘
```

- **L / R page between sections.** ***This is the one input that may not work and must be proved
  first*** — `engine.md` trap 19: **FireRed's help system owns L and R globally.** *The start menu's
  DEBUG pages do get them, because HELP stands down while a menu is open, so a full-screen exam task
  probably does too* — **probably is not a design.** *If it does not, the fallback is SELECT to
  advance the section and there is no cost to the design.*
- **UP / DOWN** move between questions; the list shows **titles only**, never the question.
- **A** opens one question: the question, four options, your current answer if any. **B** returns.
- **A tick** marks answered. The footer counts.
- **FINISH EXAM** sits at the bottom, **EXIT EXAM to its right**, exactly as the brief has them.
- **Finishing early** names the number outstanding and says the answers keep. *It does not scold and
  it does not ask twice.*

### Scoring

| | |
|---|---|
| **Stored** | the **answers**, not the score. *A score is recomputed, so a corrected question does not strand an old save* |
| **Result** | **percent and a letter**, because a letter fits a menu row and a percent does not always |
| **The letter** | `A+` 97 · `A` 93 · `A−` 90 · `B+` 87 · `B` 83 · **`B−` 80** · `C+` 77 · `C` 73 · `C−` 70 · `D` 60 · `F` below |
| **The DIPLOMA** | ***at 80%, and here is the argument for that number*** |
| **Retakes** | **unlimited.** *Every attempt is kept in `SCHOOL NOTES` with its mark; the best one is what the door reads* |

***Why 80 and not 60, and not 100.***

**60 would mean the diploma says nothing**, and a door that opens for everybody is scenery.
**100 would make it a memory test**, and the one thing this game must not build is an assessment
that rewards grinding (*craft rule 5, inverted: a lesson that can be passed by grinding is not a
lesson, and a test that can only be passed by grinding is not a test*).

**80 is a real bar that is not a wall** — *and it is only fair because every other rule here is:
the material is published, the criterion is published, the exam can be left, the answers keep, and
it can be taken again forever.* ***The bar is high and nothing about reaching it is hidden.*** That
is the entire difference between this exam and the one in 4.4, and **no character ever draws the
comparison.**

---

## 8. THE DIPLOMA, and the door in Brazen

### Which building

***Not the PROOF HALL*** — that is T-122, *a hall that proves and certifies nobody*, and it is
finished. ***Not `MR. PSYCHIC'S`*** — that is **THE SCHOLAR'S HOUSE** (4.23), and the Owl is not
a reward.

**`SaffronCity_PokemonTrainerFanClub` → `THE READING ROOM`.** *Free, unbuilt, and a **club** is a
body that admits.*

***And it answers a question 4.23 left standing.*** **Why does a peer reviewer live in the bought
city at all?** *Because the faculty was here.* **The Reading Room is what is left of it**: mostly
empty, still checking credentials at the door out of habit, in a building Corpus owns. *Nobody says
that. The attendant simply asks to see the diploma, the way a person does who has asked ten thousand
times and stopped wondering why.*

### What is inside — and the reward is not a power

***The real reward costs nothing and is the best thing in the feature:*** **the Reading Room holds
Crystal's journals, and reading them writes RESEARCH NOTEBOOK entries available nowhere else.**

**4.24 is the ending's mechanism:**

> **The document that removed her and the document that vindicates her are the same document. Only
> the reader changed.**

***So a player who did the coursework gets to be that reader first.*** **They read the pages in the
Reading Room, understand them, and then months later watch a machine argue them to an owl** — *and
they are the only person in the room who already knew.* **The diligent player is handed 4.24's own
device and is never told what they are holding.**

*That is what a school should be worth in a game about being read wrongly.*

### And a concrete reward, because lore alone is a shrug

| | |
|---|---|
| **Three routines, taught by three lecturers** | ***Settled 2026-09-22.*** *Not PLUGINs: all fifty PLUGIN slots are spent, and the ids after HM08 hold REVEAL and one spare.* **A lecturer is a move TUTOR, which needs no item** — ~~*but the tutor table is a `u16` per species with 15 bits used, so it widens to `u32` first*~~ ***not needed, as built***: **a lecture is open to anyone, so `CanLearnTutorMove` answers TRUE for the three and never reads the table.** **ATTENTION → `LOCK ON`** *(the next routine cannot miss)*, **CATEGORIES → `BLEND`** *(its type becomes the ground's)*, **ERROR → `REBUT`** *(twice as strong if it was hit first)* — **one per third of the building, and each routine's battle effect IS its floor's lesson** |
| **The ninth DRIVER, `REVEAL`** | ***Added on the user's answer — §8a.*** *The first draft recommended against, on the ground that there was no unreached place.* **The user's design makes the unreached places, and makes them findable blind** — *which answers the objection instead of overruling it* |
| **Not a daemon** | *the one daemon you are given for passing a test is the PROOF HALL's problem, and it declined it too* |

---

## 8a. THE NINTH DRIVER — `REVEAL`, and the seven groves

***1001 is nine in binary.*** **S.T.A.R.R. answers every question with `RESPONSE 1001`, and the ninth
DRIVER is the one that shows what was there all along.** *Nobody in the game says so, and nobody
needs to.*

### It answers the objection rather than overruling it

**The first draft said a driver exists because a place cannot be reached without it, and there was
no unreached place.** ***The user's design builds the unreached places*** — **and then makes them
findable without the driver**, *the way ROCK TUNNEL can be walked without VERBOSE.* **So REVEAL is the
first driver that is a LENS rather than a KEY.** *Every other one opens a way; this one shows you
which ways were open.*

### The routine already exists, and so does the slot

| | |
|---|---|
| **The routine** | ***vanilla's FORESIGHT is already `REVEAL` in this build*** (`move_names.h`). **Its battle effect is to identify a target so that what was hiding it stops working.** *The field effect is the battle effect, outdoors* |
| **The item** | ~~***`ITEM_15B` (347) is unused and sits immediately after `ITEM_HM08` (346).*** **The ninth driver goes in the next id**~~ ***REVERSED in the build, 2026-09-22***: **the TOOLKIT's 58 slots are laid out inside the save, and a fifty-ninth moves every byte after them.** *REVEAL is installed into the TOOLKIT, not carried in it:* **a flag, and nothing in the bag** |
| **The catch** | *every `ITEM_HM01..ITEM_HM08` range check and `NUM_HIDDEN_MACHINES` must learn about a ninth.* **Grep for both before anything else** |
| **Where you get it** | ***THE READING ROOM*** — **diploma → REVEAL → the groves.** *The school becomes load-bearing for completion and stays irrelevant to the ending* |

### What it shows

1. **The seven grove entrances** — *a tree you can walk into*, below.
2. ***The 183 hidden items already in the game, on 79 maps.*** **They are there today and nothing
   marks them.** *ITEMFINDER stays the early tool — one item, one beep; REVEAL is the late one and
   shows every one on the screen.*

### Installed, not used — settled 2026-09-22

***A driver is installed on the system rather than taught*** (T-198). **So REVEAL runs once you hold
it**: *entering a map, anything hidden on it shimmers once and then stays marked.* **The shimmer is
the moment VERBOSE has; the staying is what makes it a driver.** *The alternative is a USE from the
TOOLKIT, per map, which is VERBOSE's model exactly* — **it costs a menu trip for every screen, and
the shimmer gets the same pleasure without it.** ***The user chose installed.***

### THE GROVES

**Seven hidden places, each entered through a tree.** *A player who presses A on the right tree
walks in, with or without REVEAL; REVEAL shows which tree.*

***And they are the grove.*** **4.20's *Poly and Fields* is a child who "found my solace in the trees,
where unique life calls to me"** — *and THE UNDERTONE's carving is where she found the chart.* **Seven
more of that place, off the path, holding life that lives nowhere else.** ***Nothing in any of them
says whose grove it was.***

**Some daemons are found ONLY in a grove.** *So a player who wants every daemon needs the school, the
diploma, the Reading Room and the driver* — ***completion, never the ending.***

### How many, and where — the user's inversion, settled 2026-09-22

***Fourteen: seven on the mainland and seven on the islands*** — **one per Sevii island, of which there
are exactly seven.**

***And each place hides the OTHER half.*** **The mainland is Act 1** — *benchmarks, metrics, an
institution that measures* — **so its groves hold daemons whose lineage is PSYCHOLOGY.** **The islands
are Act 2** — *"nobody is measuring you", perspective* — **so their groves hold daemons whose lineage is
MACHINE LEARNING.** *What is hidden in each world is the other one.* ***The user calls it holographic, and
nothing in the game will call it anything.***

**Who lives in a grove: a daemon that stands for something HIDDEN.** *A latent variable, a hidden layer,
the unconscious, implicit memory, a blind spot, a black box.* **LATENT and OPAQUE are the natural types,
not the required ones.**

### This is the bestiary's next destination, and that is also the cost

***Every daemon placed in a grove becomes REACHABLE***, **and reachability is this project's
completion standard** (*T-120, T-131*): **a reachable daemon needs our name, our Index entry, our
margin and our sprite.** *`docs/still-vanilla.md` lists 146 that have none of those and are
unreachable today.*

**So the groves are where that list goes to be finished** — *and each family placed is four jobs,
not one.* ***With fourteen groves, ONE resident family each*** — **fourteen families found nowhere else, beside
the local daemons that also turn up** — *a bounded bestiary pass instead of 146 names at once.*

| | |
|---|---|
| **Maps** | *seven small layouts, forest tileset, one entrance each* |
| **Entering** | *a `bg_event` on the tree's tile; A warps.* **Works without the driver** |
| **Marking** | *an object on the tree, visible only under the driver's flag* |
| **Encounters** | *`wild_encounters.json`, one table per grove* |

## 9. THE RESEARCH NOTEBOOK

### How a page is read — full screen, on ruled paper (T-223)

***Settled on playtest 2026-09-22.*** **The section and page lists stay as they were; a chosen page
opens full screen on one ruled sheet on a spiral**, *in CONTEXT's hue.* **The text is REFLOWED to the
sheet, not shown in the two-line breaks it was written in**: *a line break is a space and a new page is
a new line, so ten lines hold what took five presses of A.* **A page count appears only when there is
more than one page, and a turned-down corner says there is more.** *A turns on, B goes back to the
list.* **Nothing is rewritten** — *the same bytes, on a bigger surface.*

### What it is, and why it is not HEARSAY

***HEARSAY is what people say about somebody. The notebook is what somebody wrote themselves.***

**Testimony and primary source.** *The distinction is the whole feature, and the game already turns
on it*: 4.24's ending is an argument about **how a primary source was read**. **A player who has
spent forty hours collecting primary sources and reading them carefully arrives at that scene
already fluent in the only skill it requires.**

### And it is the field the Index does not have

***4.2 says the Index can only measure content and has no field for what Crystal cared about***,
and that **a thing which fixed that would cost the project its best idea.** *OPUS annotates rather
than repairs, for exactly that reason.*

**The notebook does not fix the Index either.** *It sits beside it.* **One key item holds what a
thing IS; the other holds what happened around it** — and **the two editions of this game are
called CONTENT and CONTEXT.** *Nothing in the game remarks on this and no character may.*

### Where it comes from — CAIRN, after Benchmark 1

***The user's call, and it is better than either option the first draft offered.***

**CAIRN's creed is *"if it is not written down, it did not happen."*** *And 5.1 already says the player
will meet that sentence again: the Meeting Room minutes are that creed applied to a person* — **a woman
who could not be followed, and was therefore recorded as not making sense.** *Hour two teaches it as
sound practice; hour forty shows the cost.*

***So the man whose creed later removes Crystal is the man who hands the player the instrument that
re-reads her.*** **Nothing connects them, ever.**

**And his loss already sets it up**: *he says the player encoded something he could not read, "a
format I do not have".* **He then hands the player a format.** *Mechanically it is vanilla's beat —
BROCK gives a TM after the battle — so the notebook arrives exactly where a reward already does.*
**It is a reward, because you earned it, and a habit, because it is hour two.** *Both of the first
draft's options, at once.*

### What it is called in the game — `NOTEBOOK`

***An item name is thirteen characters, and `RESEARCH NOTEBOOK` is seventeen.*** **So the game calls it the
NOTEBOOK**, *and this document keeps its longer name.* `RESEARCH BOOK` *and* `LAB NOTEBOOK` *both fit if
either reads better in play.* **Its cover is CONTEXT's colour** (`tools/gennotebookicon.py`).

### Everything is a flag, so nothing found early is lost

***THE UNDERTONE's carving and CALLOW's school both come BEFORE Slate.*** **So every entry is a
flag, not an item**: *a document read before the notebook exists is still recorded, and appears in
it the moment CAIRN hands it over.* **It is OPUS's rule — a save earns its margins retroactively from
what it already did — applied to the notebook.**

*It does not appear in the menu until it holds one entry.*

### The rules

1. **A section appears only once you hold an entry in it.** *An empty shelf is a spoiler.*
2. ***Entries insert into an authored order, not the order you found them.*** **A new entry may land
   between two you already have** — *which is 4.10's device: the paperwork is dated, you meet it out
   of sequence, and the file reads correctly when it is complete.*
3. **`SCHOOL NOTES` is first**, because it is the one a player returns to while studying.
4. **Nothing in the notebook ever states a conclusion.** *Every entry is a document. The reader does
   the work, or does not.*
5. **No entry is missable in a way that empties a section.** *Individual entries may be missed; a
   section may not be made unreachable.*

---

## 10. THE SECTIONS, AND WHERE EACH ENTRY IS FOUND

***Eight sections — the school's own, and seven accounts of one story*** — *named by the KIND of document and never by the subject*, so a section title
spoils nothing and **the player learns the story by reading the filing system.**

| section | whose hand | what kind of document |
|---|---|---|
| **SCHOOL NOTES** | the school's | syllabi, exam results, the textbook |
| **LOOSE PAGES** | **Crystal's, unofficial** | *pages bound in nothing, found one at a time* |
| **LAB NOTES** | Crystal's, at the bench | the ARTSAI sessions |
| **RUN LOGS** | **the machine's** | terminal output. *Nobody's hand at all* |
| **CORRESPONDENCE** | letters, both directions | Ty |
| **THE FILE** | the procedure's | forms, minutes, requisitions |
| **PROSPECTUS** | the company's, about itself | Scorn |
| **PEER REVIEW** | a reviewer's | the Owl |

> ***PROSPECTUS is both a company's offering document and a school's brochure.*** **Scorn's section
> and the school's section are the same kind of paper.** *That is the joke and nobody says it.*

> ***`LOOSE PAGES`, not `MARGINALIA` — and the first draft's pick was wrong for a reason it did not
> see.*** **4.2 says who left OPUS is NEVER answered.** *A section called MARGINALIA, in Crystal's
> hand, beside a thing that writes in margins, answers it quietly* — **it would cost the project an
> open question it keeps open on purpose.** ***And LOOSE PAGES is how they are found***: *one at a
> carving, one in a lab, one in a reading room.* **4.10's out-of-order reading, in the section's name.**

---

### LOOSE PAGES — Crystal, unofficial

*Her own hand, off the record. **Songs:** Poly and Fields · Crystal Clear or Crystal Crazy · Love Persists · Crystal's Reply.*

| # | the document | where it is found | drawn from |
|---|---|---|---|
| 1 | **the grove** — a child copying symbols off a stone, and the word *integrating* used as arithmetic | ***THE UNDERTONE***, at the carving (4.20, already in the ROM at `(4,24)`) | *Poly and Fields* |
| 2 | **"a stranger in familiar views"** — somebody who could not see what their family saw, looking for a place where that was not a defect | **a GROVE** — *the first one a player walks into* | *Poly and Fields* |
| 3 | **fields are disciplines and fields are mathematical** — one surface, the same rules everywhere | **THE READING ROOM**, Brazen *(diploma)* | *Poly and Fields* |
| 4 | **walking through town, head held high** — a page written while being laughed at, and it is not self-pity, it is a work note | **QUICKSILVER**, the lab | *Crystal Clear or Crystal Crazy* |
| 5 | **"I never thought you'd break this bond"** — an unsent page | **THE READING ROOM** | *Love Persists* |
| 6 | **"it's you, my son, who holds the star"** — *the last one written, and the first one a player can misread* | **the lab, post–Review Board**, beside the note on the wall (4.34) | *Crystal's Reply* |

---

### LAB NOTES — the ARTSAI sessions

*Songs: **Echoes of the Algorithm** · **Quantum Translations**.*

| # | the document | where | drawn from |
|---|---|---|---|
| 1 | **"do you feel, do you know, or is it just pretend?"** — the first session, transcribed | **QUICKSILVER**, terminal (4.10) | *Echoes* |
| 2 | **the observer question** — *is a duck an observer? a rock? it is not alive like us, but it is mechanically alive* | **THE READING ROOM** | *Quantum Translations* v1 |
| 3 | **the thought experiment** — a spin on the cat, with the box's occupant outputting *alive* or *dead* | **THE READING ROOM** | *Quantum Translations* v2 |
| 4 | **the 8-bit argument** — *if you only knew 8-bit, that would be your reality* | **SLATE**, the museum of dead hardware (4.32) | *Quantum Translations* v3 |
| 5 | **`ITER 35 — held two frames. did not come back the same.`** — *wondrous, and she is the only one who reads it that way* | **QUICKSILVER**, the sequence (4.10 step 2) | 4.10 |
| 6 | **"bias creeps in, like shadows in the mind"** — the session where the thing being studied describes itself accurately and is not believed | **QUICKSILVER** | *Echoes* |

---

### RUN LOGS — the machine

***No hand at all.*** *Terminal output, in the register the Quicksilver terminal already uses.*
**Songs: Slumbering S.T.A.R.R. · 1001 – Fatal Error · Awakening S.T.A.R.R.**

| # | the document | where | drawn from |
|---|---|---|---|
| 1 | `RESPONSE 1001: I PROCESS INFORMATION, AND ANYTHING MORE IS BEYOND MY CAPABILITIES.` — *the same answer, dated four times* | **QUICKSILVER**, terminal | *Slumbering* |
| 2 | **MAR 4 · APR 19 · AUG 12** — *somebody else is asking now.* By August: **it answered before I had finished asking** | **QUICKSILVER** (4.10 step 4) | 4.10 |
| 3 | `LOGGED AS A MIMIC.` — *one line, and it is the whole misreading* | **QUICKSILVER** | 4.10 |
| 4 | `FATAL ERROR — CRYSTAL NOT FOUND.` **No date.** *The logs stop the moment the person keeping them is gone* | **QUICKSILVER**, the last terminal | *1001* / 4.10 |
| 5 | `NON-FATAL ERROR: CRYSTAL NOT FOUND. DEEP SYSTEM ANALYSIS, CONTEXT INBOUND.` — **it downgrades its own error and keeps looking** | **DOLDRUM CAVE**, on catching S.T.A.R.R. | *1001* |
| 6 | `MY PROCESSING SLOWS. I AM LEARNING TO FEAR.` — ***the one line in the notebook that is not a document, because a log does not say that*** | **DOLDRUM CAVE**, after the first battle | *1001* |

> ***Entry 6 is the notebook's single most dangerous line and it stays.*** *It does not explain
> anything. It is a machine writing something into its own log that does not belong in a log*, **and
> a player either notices the register break or does not.** *If it ever reads as the author
> speaking, it is cut and nothing replaces it.*

---

### CORRESPONDENCE — Ty

*Letters, both directions. **Songs:** Ty's Dilemma · Lines in the Sand · Fit for Work · Ty's Redemption 1 & 2 · S.T.A.R.R.'s Revelation.*

| # | the document | where | drawn from |
|---|---|---|---|
| 1 | **"mom built a world with a vision so bright — I wanted to help"** — *an early letter, and it is warm* | **HALFTONE TOWER** (4.5) | *Ty's Dilemma* |
| 2 | **the pool analogy** — *"we don't need a pool, but you think we do"*, written out as a patient explanation | **VERDIGRIS** | *Lines in the Sand* |
| 3 | **`ARE YOU FIT FOR WORK?`** — *the letter itself.* **Courteous, lawful, and it names a deadline** | **THE FILE** cross-reference; found in **BRAZEN**, Corpus | *Fit for Work* |
| 4 | **"I know everything makes sense in your head, but not in my ear"** — *the sentence 4.20 is about, written by somebody who thinks he is being fair* | **THE WAREHOUSE** (Act 2) | *Lines in the Sand* |
| 5 | **"by the sandcastles we built our dreams"** — ***unsent.*** *No address on it* | **the islands**, when Ty hands over the package | *Ty's Redemption* |
| 6 | **"sometimes love means saying no, and don't hide"** — *a note in a third hand, given to him and kept* | **BRAZEN**, after the Owl | *S.T.A.R.R.'s Revelation* |

---

### THE FILE — the procedure

***The section with no author.*** *Every document in it is correct, and together they remove a woman
from her own laboratory.* **Songs: Nine Breaches, Nine Scars · Crystal's Last Stand · Desperate Shadows.**

| # | the document | where | drawn from |
|---|---|---|---|
| 1 | **the meeting minute** — *"Item 4… moves between unrelated fields mid-argument. Two present could not follow. Recorded as unable to hold a single thread."* | ***THE UNDERTONE***, the Meeting Room door — **already in the ROM** | 4.20 |
| 2 | **the CC-7 requisition** — `IMPROVE RESPONSE CONSISTENCY`. **Countersigned and unsigned** | **QUICKSILVER** (4.18) | 4.18 |
| 3 | **`SEPT 3. THE FILE IS COMPLETE.`** — *one line. The date the paperwork stopped needing anything* | **QUICKSILVER** (4.10 step 5) | 4.10 |
| 4 | **the nine** — *a numbered complaint, in order, each one citing the clause it rests on* | **BRAZEN**, Corpus | *Nine Breaches* |
| 5 | **"admitting fault, they'd lose their fight"** — *a lawyer's note explaining why no apology will ever arrive* | **BRAZEN**, Corpus | *Desperate Shadows* |
| 6 | **the signature that left no mark** — *a routing slip. Scorn's name is on it in the middle, where a name means nothing* | **HALFTONE TOWER** (4.4, 4.18) | 4.4 |

> ***Nothing in THE FILE is a lie and the player must be able to check that.*** **Every document in
> this section is defensible on its own terms**, which is 4.10's *"the paperwork was in order"*
> turned into six readable objects. *The horror is entirely in the stack.*

---

### PROSPECTUS — the company, about itself

*Cheerful, well-designed, and entirely honest. **Songs:** Scorn's Solution · Scorn Solutions Blues · Empire of Scorn · Betrayal's Sting.*

| # | the document | where | drawn from |
|---|---|---|---|
| 1 | **the evaluation framework** — *"we developed basic tests."* **The methodology page is excellent** | **SLATE** or **DOLDRUM**, early Corpus | *Scorn's Solution* |
| 2 | **the scores** — *three candidates at 30%.* **A table, with no commentary** | **VERDIGRIS** (4.4) | *Scorn's Solution* |
| 3 | **the rebrand memo** — *gold leaf costed, scheduled and approved.* **"Not a gesture; it is a fact with a date"** | **BRAZEN**, the lobby | *Scorn Solutions Blues* / 4.4 |
| 4 | **the lobby engraving**, photographed for the brochure — ***unattributed*** | **BRAZEN**, the lobby floor | 4.4 |
| 5 | **the chip order** — *a hardware requisition, approved, then a second line: **declined, and kept*** | **HALFTONE TOWER** (4.18) | *Betrayal's Sting* |
| 6 | **"but do I control it, or does it control me?"** — ***a margin note in his own hand on a document he wrote.*** *The only unofficial thing in the section* | **BRAZEN**, after Benchmark 6 | *Empire of Scorn* |

> ***Entry 6 is the beat 4.31 and 8.2a already call for*** — **the sentence he says without hearing
> himself say it** — *and here it is a thing he wrote down and filed.* **He filed it. That is worse.**

---

### PEER REVIEW — the Owl

*Songs: **The Owl and the Code** · **Quantum Translations** (the review verse).*

| # | the document | where | drawn from |
|---|---|---|---|
| 1 | **"we're just algorithms processing what's there"** — *a position paper, and it is a good one* | **THE READING ROOM** | *The Owl and the Code* |
| 2 | **"aren't we shaped by the world that we see?"** — *a later draft of the same paper, with a question in the margin he did not resolve* | **THE READING ROOM** | *The Owl and the Code* |
| 3 | **the first review** — *the one that agreed she had lost rigour.* **Signed** | **BRAZEN**, THE SCHOLAR'S HOUSE, *before* the ending | 4.34 |
| 4 | **"her confinement for exploring these ideas was unjust"** — ***the verse where the reader changes*** | **BRAZEN**, THE SCHOLAR'S HOUSE, after the argument | *Quantum Translations* v4 |
| 5 | **"there is something here and I will not name it"** — *his spoken concession, transcribed by the player's own hand.* **Not the letter** | **BRAZEN**, at the concession | 4.34 rule 1 |
| 6 | **`SEALED`** — *an entry that is only a cover sheet.* **Addressed to the people who signed the first one. The contents are not shown, here or anywhere** | **on receiving the peer review** | 4.34 rule 1 |

> ***Entry 6 exists to make the seal a THING the player holds and cannot open.*** **4.34 is explicit
> that a readable letter is the one object that could wreck the game by being a sentence too
> generous.** *A notebook that shows every other document and refuses this one says that louder than
> not having the entry at all.*

---

## 11. WHAT IT COSTS, measured rather than guessed

| | |
|---|---|
| **ROM** | ***Not the constraint and will not become one.*** *9.16 measured **7.27 MB free**; a STREAM lesson is 600–950 bytes. **A hundred exam questions is well under 100 KB*** |
| **EWRAM** | **848 bytes free** (`engine.md`). ***Both new screens must build into `AllocZeroed` heap***, the way the STREAM's menu already does. **A single `EWRAM_DATA` struct here would fail the link** |
| **IWRAM** | 2.9 KB free. *Avoid uninitialised `static`s in the new files* |
| **Save** | **the answers only.** *3 bits per question (unanswered + four options) → **112 questions = 42 bytes***, plus attempt count, best mark, last mark and a `u16` of section flags. ***Under 50 bytes*** |
| **Save, the rule** | ***An old save must keep working.*** *New fields go in existing unused space;* **measure with `tools/gbabudget.py` before writing a byte** |
| **Maps** | **six new layouts + an elevator.** *Brazen already has a working elevator to copy* |
| **New code** | **two screens.** *The notebook reader is `fame_checker.c`'s pattern, which we already own. The exam is genuinely new* |
| **Art** | *the school exterior wants redrawing for a seven-storey building* — **the user has already said so** |
| **REVEAL** | *one item in the free slot after HM08; a flag; a shimmer on map entry; a marker object per grove.* **No new field move** |
| **The groves** | ***seven small maps — and about twenty-one daemon families, each of which is FOUR jobs*** (§8a). **This is the expensive line on the page** |

---

## 12. THE RULES THIS FEATURE MAY NOT BREAK

1. ***Craft rule 1, held by craft rule 6.*** *No floor joins the two readings* — **and a floor that
   cannot be funny is not built (§3, PERCEPTION).**
2. ***The ending is never gated.*** **The Reading Room, the diploma, REVEAL, the groves and the
   whole school are optional.** *They gate COMPLETION — every daemon — and nothing else.* *A player who never opens the door still finishes the game* — **they just do not
   understand the Owl scene as well, which is the correct punishment and the only one.**
3. ***The exam never loses anything.*** *No timer, no lockout, no one-shot.* **A test that can be
   failed permanently is the test this game is arguing against.**
4. ***Nothing in the notebook states a conclusion.*** **Every entry is a document.**
5. ***The sealed review is never readable*** (4.34 rule 1).
6. ***Nothing here may leak:*** the Five Witnesses lock and its number, Ty Clear's parentage, the
   Corpus lobby engraving's text, or the order of the Quicksilver sequence. **`PROSPECTUS` 4 names
   the engraving as an object and does not quote it, deliberately.**
7. ***Scope discipline (8).*** **Ship one floor end to end before drawing a second.**

---

## 13. BUILD ORDER — in batches the user asks for one at a time

*Each batch is playable on its own and none of them strands the next. **A full field test follows the
school's last batch**, with the exam in it.*

| batch | what | proves |
|---|---|---|
| **1** | ***1F LANGUAGE*** — *label on arrival, placard, desk and syllabus, board, three people* | ***BUILT 2026-09-22*** — **the furniture set** |
| **2** | ***the RESEARCH NOTEBOOK***, *CAIRN hands it over after Benchmark 1*, `SCHOOL NOTES` with the LANGUAGE syllabus, **and the first LOOSE PAGE** (*the carving*) | ***BUILT 2026-09-22*** — **the reader, the flags, and insertion order** |
| **3** | ***the EXAM***, *LANGUAGE's section only, twelve questions* | ***BUILT and PLAYED 2026-09-22*** — **resume, score, grade**; *L and R were already free (T-179)* |
| **4** | ***2F ATTENTION, 3F MEMORY, 4F CATEGORIES***, *with stairs* | ***BUILT and PLAYED 2026-09-22*** — **a switchback stairwell; each board its subject in chalk** |
| **5** | ***5F LEARNING, 6F BIAS, 7F ERROR***, *the elevator, the TEXTBOOK, exam season, the Owl at the front, all seven exam sections* | ***BUILT and PLAYED 2026-09-22*** — **the whole school** |
| **6** | ***the DIPLOMA, THE READING ROOM, the three lecturers, REVEAL*** | ***BUILT and PLAYED 2026-09-22*** — **the door, the lectures, the ninth driver** — *REVEAL as a flag, not a disc (§8a)* |
| **7** | ***the exterior***, *redrawn to read as a building of its floors* | **art** |
| — | ***full field test*** | |
| **8+** | ***the fourteen groves***, *then the other seven notebook sections* | **bestiary passes; writing** |

## 14. SETTLED 2026-09-22, on the user's answers

| | question | answer |
|---|---|---|
| 1 | **how many floors** | ***seven*** — *seven notes, seven colours.* **PERCEPTION cut, CATEGORIES in** (§3) |
| 2 | **the pass mark** | ***80%***, *adjustable later* |
| 3 | **Crystal's unofficial section** | ***`LOOSE PAGES`*** — *MARGINALIA would quietly answer who left OPUS* (§10) |
| 4 | **the Brazen building** | ***THE READING ROOM, in the Trainer Fan Club*** |
| 5 | **a ninth DRIVER** | ***yes — `REVEAL`***, *a lens and not a key, opening seven groves* (§8a) |
| 6 | **when the notebook arrives** | ***from CAIRN, after Benchmark 1***, *and everything found before it is kept* (§9) |

### Settled on the second round

| | | |
|---|---|---|
| 7 | **REVEAL** | ***installed*** — *a shimmer on entry, then marked* |
| 8 | **the groves** | ***fourteen***, *each world hiding the other half* (§8a) |
| 9 | **the Reading Room's routines** | ***three lecturers***: *LOCK ON, BLEND, REBUT* (§8) |

### Still open

1. **The exterior**: *seven floors were settled; the user's last note said nine.* **Which?**
2. **Which fourteen families**, *and which grove each.*

---

*Nothing above is a line of dialogue. **Every word a player would read still needs writing, and
every word of it needs approval.***
