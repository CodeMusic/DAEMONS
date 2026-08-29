# PROJECT: CONTEXT / CONTENT

**A `pokered` total conversion — the living design bible, v3.8**

Machines that evolved into creatures. A theory of mind hidden in a type chart.

Personal-use ROM hack built on the pret `pokered` decompilation. This document consolidates every decision made so far, including the reasoning behind rejected options, so nothing is lost when work moves into source control.

---

## 0. THE THESIS

> **Emotions are the color of context. Thoughts are the content.**

The game argues this in five registers and never once in dialogue.

| Layer | How it argues |
|---|---|
| Mechanics | The type chart makes LOGIC fail against CONTEXT |
| Cartography | Every place name is a word meaning both a color and a feeling |
| Structure | The Index — the artifact you spend the game filling — measures only content |
| Movedex | PERSPECTIVE to RECURSION is the lineage of feeling, in two move slots |
| Vocabulary | The whole map is named in the language of image reproduction |

### 0.1 Craft rules

1. **No character ever explains the color–emotion link.** Not one line. The moment it is said aloud it stops being architecture and becomes a moral.
2. **One NPC nearly notices.** A kid in Verdigris says the town felt greener before the store went up. Wrong — but wrong in the right direction.
3. **Name the process, not the pathology.** Verdigris, gilt, blanch, quicksilver are things that *happened to* a place. Jaundice, sallow, fever are things a place supposedly *is* — that relocates blame onto whoever lives there.
4. **Neutral, not dull.** Place names should be materially specific rather than moody. Prefer a pigment to an adjective.
5. **Lessons must be mechanical.** If a gym's lesson can be skipped by grinding, it is not a lesson.
6. **Comedy is the best cover for a thesis.** A game that is funny in its ordinary moments earns the right to be serious in three or four of them. Corpus employees are cheerful and absurd; the horror is what they are cheerful *about*. Nothing protects rule 1 better than a joke — a player who is laughing is a player who is not being lectured.

### 0.2 The pigment throughline

Blanche, Slate, Halftone, Verdigris, Brazen, Quicksilver, Lurid — pigment, printing and reproduction terms. Lithographic stone, dot screens, corroded bronze, brass plate, alchemical pigment, glow.

The map is written in the vocabulary of **making an image of a thing**. Which is what a model is. The Index is a reproduction that loses the original, and it charts a country named in the language of reproduction.

This was discovered after the fact, not planned. Do not explain it either.

---

### 0.3 The loop underneath

The thesis in 0 is a statement. The mechanism under it is a **loop**.

**Context determines which content is available; the content you end up holding reshapes the context.** Around and around, unattended, in everything. That is the Contextual Feedback Model, and like everything else here it is never named in the game.

Two consequences the game can show without ever explaining:

- **Positive loops compound.** Something amplifies itself until something stops it. RECURSION is exactly this, mechanically — see 4.7.
- **Negative loops stabilise.** Something damps itself back toward where it started. It looks like nothing happening, which is why it goes unnoticed far longer.

**And an unwatched loop distorts the representation, not the thing.** This is where the Index and the halftone converge: the entry stays thin, the dots stay the same size, the reader concludes something about the **daemon** — and the bias came from resolution and inattention, never from malice. Nobody in the game is lying. The picture is simply being made at the wrong distance by someone who is inside the loop that makes it.

Dialogue guidance for gesturing at this without stating it is in 4.9.

---

## 1. LEXICON

The creatures are **DAEMONS**.

A daemon is a background process that runs unattended, and it is the Greek *daimon* — the guiding spirit, Socrates' inner voice speaking from somewhere he did not control. One word, both registers, and it never says "AI." Six characters, so it fits every UI box that held POKéMON.

*Considered and rejected:* QUALIA and ANIMA both state the thesis outright, violating craft rule 1. ENGRAM (a memory trace physically encoded in tissue) and KERNEL (system core, and a seed) remain viable alternates.

| Vanilla | Ours | Why |
|---|---|---|
| Pokémon | **DAEMON** | background process; guiding spirit |
| Pokédex | **THE INDEX** | a lookup table that points at content. Cold, bureaucratic, exactly wrong in the right way |
| Trainer | **USER** | user-level privileges — and the first box is a USERBOX. Also: a *user* is someone who uses people |
| *(the verb)* | **RUN** | you still run daemons. The title is what you are; the verb is what you do |
| Wild | **UNBOUND** | the exact antonym of BIND — an unbound socket is held by nobody |
| Fleeing | **DETACHED** | you break your connection to a running process |
| Poké Flute | **INTERRUPT** | what wakes a blocked process |
| Gym | **BENCHMARK** | what a gym actually is |
| Badge | **CERT** | eight certifications |
| Elite Four | **THE REVIEW BOARD** | beating them is passing peer review |
| Champion | *(incumbent)* | Ty Clear is the prevailing paradigm, not a king |
| Pokémon Center | **CHECKPOINT** | restore from a saved training state |
| Poké Mart | **THE REPO** | |
| PC storage | **COLD STORAGE** | |
| PROF.OAK | **CRYSTAL** / **CRYSTAL CLEAR** | **no title.** See below |

*One escaped, and a gender sweep found it.* `ViridianMart` still said **PROF. CRYSTAL** — the clerk with the PACKAGE. Fixed 2026-08-29 to `CRYSTAL CLEAR`. Worth noting how it was caught: not by looking for titles, but while checking every gendered reference to her. **Passes find each other's misses.**
| OAK's PARCEL | **PACKAGE** | a repo distributes packages. Also forced — `CRYSTAL's PARCEL` is 16 and items cap at 12 |
| Poké Ball line | **USERBOX → ADMINBOX → SUPERBOX → ROOTBOX** | acquisition as privilege escalation; root access is the Master Ball |
| Catching | **BINDING** | `bind()` — and *binding a daimon*, which is the literal ritual phrase |
| Silph Scope | **RESOLVER** | a linker resolves a symbol to a name; *resolution*; and resolving an ambiguity |
| Fainting | **HALTED** | |
| Evolution | **RECOMPILE** | |

Box names are tunable — the *privilege ladder* is the idea worth keeping. Success rate rising with permission level is thematically exact.

### 1.1 On the missing title

*Implemented 2026-08-29. Both editions build; no OAK remains in any text file.*

**Crystal has no title, and the absence is the point.**

4.1 says she spent her career arguing that machines have context, nobody funded it, and **she built the Index in order to be taken seriously.** Then 4.10 has a fitness-for-work procedure remove her from her own lab. A woman who had to build a taxonomy engine to be credible, and was then processed out of the building, does not get a PROF.

Every other authority in the game has a role — BENCHMARK leaders, the REVIEW BOARD, CORPUS. She is just her name. And it lands because vanilla players *expect* the title: the professor-slot character has no professor, and nobody remarks on it.

**The vanilla text split perfectly for it**, which is how you know it is the right call:

| Vanilla | Ours | Register |
|---|---|---|
| `OAK:` — 19× | **`CRYSTAL:`** | dialogue prefix. People know her |
| `PROF.OAK` — 8× | **`CRYSTAL CLEAR`** | third person. The full name |

First name when spoken to, full name when spoken about, and **no rank anywhere.**

**One line had to be rewritten rather than renamed.** The intro speech is the single place the title is claimed aloud:

> *vanilla:* My name is OAK! People call me the #MON PROF!

There is no honest rename of that, because the second sentence *is* the rank. It became:

> My name is CRYSTAL CLEAR! I study #MON.

Flat, factual, and it claims nothing. Placeholder-grade wording that should get a proper pass at step 8 — but the shape is correct: **where Oak asserts a title, she states an occupation.**

**Why the intro said #MON and not DAEMONS, and no longer does.** `#` is a control character that expands to *POKé*, and the species word has not been renamed yet — that is a bulk pass over the charmap and every string (9.2, step 8). Writing DAEMONS in one line while the other several hundred still say POKéMON would be worse than waiting. **The line became "I study DAEMONS." the day the species rename landed**, and nothing else about it changed. *(Done 2026-08-29 — it needed the plural mark, per 1.2.)*

*The cost, recorded:* every touched line needed rewrapping. Both replacements are longer (`OAK:` → `CRYSTAL:` is +4, `PROF.OAK` → `CRYSTAL CLEAR` is +5) and Gen 1 text is hand-wrapped. Twenty-one blocks were rewrapped to stay inside the box.

**The ceiling, measured properly 2026-08-29 — and the earlier figure here was wrong.** The message box is declared `MESSAGE_BOX, 0, 12, 19, 17`, so its borders sit at x0 and x19 and text starts at x1: **the interior is 18 columns.** Vanilla reaches 19 exactly four times (*"It's very accurate,"*, *"That's odd, MR.FUJI"*, *"You can't use items"*, and one trailing space) — and each of those **overwrites the right border tile**. So the honest rule is **18 is clean, 19 is vanilla-grade jank**, not "19 is the ceiling". A control token like `<COLON>` or `<PK>` is **one tile**, which is what made the earlier count wrong.

*Code identifiers were left alone.* `OaksLab`, `OAKS_LAB`, `ProfOakName` and roughly 267 similar symbols are internal and invisible to the player, in the same category as the `_RED`/`_BLUE` defines (8.4). Renaming them is cosmetic and deferred.

### 1.2 On the species rename — and the trick that made it free

*Implemented 2026-08-29. Both editions build; zero overflows.*

**`#` is one byte.** `constants/charmap.asm` maps it to `$54`, and the text engine expands it from a single string:

```asm
home/text.asm:183    PlacePOKeText::   db "POKé@"
```

So `#MON` is four bytes rendering seven characters. **Change that one string to `db "DAE@"` and all 650 occurrences become DAEMON** — no source edits, no rewrapping.

The widths cooperate, which is the opposite of the 1.1 job:

| | rendered |
|---|---|
| POKéMON | 7 |
| **DAEMON** | **6** |
| **DAEMONS** | 7 |

Singular gains a character, plural is identical. **Nothing needed rewrapping.**

**What did need doing.** Fifty-four occurrences were not the species and had to become literals first, or they would have rendered as DAE-nonsense:

| | Count | Became |
|---|---|---|
| `#DEX` | 26 | literal **INDEX** — 7 chars to 5, so it also gains room |
| bare `#` | 23 | literal `POKé`. **All 23 are item prefixes split across a line break** — `# BALL`, `# DOLL`, `# FLUTE` — not species, so the trick was safe |
| `#MANIAC` | 5 | literal `POKéMANIAC`, pending the trainer-class pass |

**The real work was grammatical number.** POKéMON was both singular and plural. DAEMON is not. Of the 650:

| | Count | |
|---|---|---|
| **Compound** | 106 | `#MON CENTER`, `GYM`, `LEAGUE`, `MART` — not number questions. The lexicon renames these outright |
| **Plural** | **123** | marked `#MONS` |
| **Singular / attributive** | the rest | **no edit required** |

**The default is free, and that is why this was tractable.** English keeps attributive nouns singular — *DAEMON magazines*, *DAEMON trainers*, *DAEMON fights* — and singular is what `#MON` already renders. Only plurals needed touching, so **an error of omission reads as a mild singular rather than as breakage.**

*Two heuristic passes were needed.* The first over-marked: it read `looks`, `is`, `was` as evidence but also caught `will` and `can`, which are number-neutral. *My DAEMON looks stronger* is singular; *all DAEMONS will have weak points* is not. A corrector reverted eight, four of them wrongly, and a quantifier rule (`all`, `some`, `up to 6` plus a modal) restored those.

**The intro got its human read first, 2026-08-29** — on screenshots, which is the only reliable way to catch these. Six in Crystal's opening speech were reading singular and should not have been: *world of DAEMONS*, *I study DAEMONS* (twice), *creatures called DAEMONS*, and *adventures with DAEMONS*. All six are the same class of miss — vanilla wrote the singular because POKéMON is a mass noun, and DAEMON is not. Marking them `#MONS` was the whole fix; the longest result is 17 characters and nothing needed rewrapping.

**A second class, found the same way, 2026-08-29.** Dialogue names types in lowercase — *the fire #MON, CHARMANDER* — and those words were never renamed with the chart. The starters are fixed (**ENTROPY**, **FLOW**, **GROWTH**, since vanilla says *plant*, not *grass*). **Nineteen more remain, nearly all inside gyms**: *electric #MON*, *Psychic #MON*, *rock-type #MON*, *fighting #MON*. They are deliberately left — a Benchmark's type is 5's design work, and renaming the dialogue before the leaders are settled would just be done twice. Separately, **42 occurrences of *fight*** want the same human read; some are the verb we replaced, some are people (*not a fighter*, *a fighting game*).

**Still open:** roughly 154 occurrences carry no strong evidence either way and currently read singular. Most are attributive and correct as they stand, but the set wants the same treatment — read on screen, not in the source.

### 1.3 On the boxes, and what binding actually is

**A box is a machine.** Not a metaphor we are imposing — it is sysadmin vernacular. *I sshed into the box.*

So the ladder is not a set of cages of increasing strength. **You are offering the daemon a host.** A daemon is a process; a process needs somewhere to run. It stays if that host grants the privileges it needs.

Which makes the catch rate literal rather than figurative: **an unbound daemon will not run on a box where it only has user rights.** ROOTBOX takes anything because root takes anything. The suffix was already the right word before we knew why.

### 1.4 On the battle vocabulary

The gyms were already BENCHMARKS, so a battle was already a **run** — you put a process against a workload and see what it does. Two decisions fell out of that.

**RUNNER became USER**, because RUN was doing two jobs and colliding with itself. Vanilla's own text proves it: *"No! There's no running from a trainer battle!"* while the player is a RUNNER. USER does three jobs instead:

- **Technical** — user-level privileges, and the first box is a **USERBOX**. Your title and the bottom rung of the ladder are the same word. You start as a USER with a USERBOX and escalate.
- **Moral** — a *user* is someone who uses people. Unaware selfishness: `oPerson` from 2011, and the implicit-selfishness thread from 2021.
- **Practical** — it frees RUN entirely.

**Nothing was lost.** *You run processes* relocates from the noun to the verb: **you are a USER, and you RUN daemons.** The title is what you are, the verb is what you do, and neither collides.

**Trainer battles are BENCHMARKS too**, and that is a scale distinction rather than a collision — exactly as in machine learning. You benchmark constantly; **THE BENCHMARKS** are the eight formal ones that issue CERTs. A trainer battle is an informal benchmark, which is literally what it is.

**DETACHED has no inverse, deliberately.** Fleeing is breaking your connection to a running process, and the process is still running — you simply stopped observing it. EXITED would be wrong, because *you* did not exit. And ATTACHED for encounters would imply a connection you had not made; **appeared** already covers it.

**The strings, as implemented 2026-08-29:**

| Vanilla | Ours |
|---|---|
| `Wild <nick> appeared!` | **`UNBOUND <nick> appeared!`** |
| `<nick> fainted!` | **`<nick> HALTED!`** |
| `Enemy <nick> fainted!` | **`Enemy <nick> HALTED!`** |
| `Got away safely!` | **`DETACHED.`** |
| `No! There's no running from a trainer battle!` | **`No! You can't DETACH from a USER's run!`** |
| `Go! <nick>` | **`RUN, <nick>`** |
| `<TRAINER> wants to fight!` | `<USER> wants to BENCHMARK!` *(pending the trainer pass)* |
| `#MON are pets. Others use them for fights.` | **`DAEMONS are companions. Others BENCHMARK them.`** |
| `Enemy <nick> fainted!` | **`Remote <nick> HALTED!`** |
| `Enemy <nick> ran!` | **`Remote <nick> DETACHED.`** |
| `The enemy's weak!` | **`The remote's weak!`** |
| `<PLAYER> defeated <TRAINER>!` | **`<PLAYER> outscored <USER>!`** |

*On pets, and the precedent that decided it.* Crystal's opening speech drew a contrast — kept for affection, or used for gain — and vanilla's affection word was **pets**. 1.5 rejected *caught* for being "a word about grabbing an animal"; **pets** is a word about keeping one, and fails the same test for the same reason. **companions** keeps the register without the menagerie.

*Why not **assistants**.* Tempting, and the contemporary word — but it collapses the sentence. Vanilla's line only works because its two halves oppose each other, and an assistant is *already* being used, so "assistants… others use them" stops being a contrast at all. It is also the nearest the first minute could come to saying the thesis out loud (craft rule 1), and it pins the game to one year's discourse. **Held in reserve**: if it is ever taken, the second half has to change with it.

*And **fights** becomes **BENCHMARK**,* which is what this world calls the thing. Vanilla teaches "fights" in the first minute; we teach the real verb in the same breath, three lessons before the player needs it.

*The prefix was the one that mattered, and the first pass missed it.* Two standalone strings said *Enemy*; the **third** is `home/text.asm`'s `EnemyText:: db "Enemy @"`, which is what every `<USER>` and `<TARGET>` expands to for the opposing side — so it appears in far more messages than the other two combined. Now `Remote @`.

**And it sets a naming budget.** Thirty-two strings put text straight after `<USER>` on the same line, the worst being `<USER>'s`. Vanilla fits exactly: `Enemy ` + a 10-character name + `'s` = **18**. *Remote* is one longer, so the same line is **19** — over the clean edge. **Species names should therefore be capped at 9 characters** (9 gives 18 and fits). This costs us nothing we were not already choosing: 9 renames the bestiary anyway, and vanilla's own longest are 10. A player who *types* a 10-character nickname will push one character over the border in some messages — self-inflicted, self-healing, and no worse than what vanilla does four times on its own.

*On **enemy**, replaced by **REMOTE**.* Nothing in this world is anyone's enemy — the opposing daemon is a process bound to somebody else, and *enemy* imports a hostility the lexicon never claims. **REMOTE** is the exact technical word for a process you have no handle on, it sits on the same axis as DETACH, and it is attested as a bare noun in precisely this register (*the remote is down*). It is one character longer than *enemy* and the nickname occupies its own line, so nothing rewrapped.

*And it caught a live collision.* `Enemy <nick> ran!` was still using **ran** — the word 1.4 went to some trouble to free. It is now **`Remote <nick> DETACHED.`**, which also quietly teaches that detaching is something either side can do.

*On **defeated**, replaced by **outscored**.* A trainer battle is a BENCHMARK, and a benchmark yields a **score**. *Defeated* is the language of combat; *outscored* is the language of evaluation, which is what the Review Board will later do to the player. **outran** was considered and rejected — it reaches for the racing sense of RUN, and 1.4 spent real effort making RUN mean *execute*.

#### On money — **CACHE**, and how little of it is visible

**The word *money* is never shown to the player.** It appears only as labels and variable names; on screen there is the **¥** glyph and digits, nothing else. The single prose instance in the whole game is Team Rocket in Mt Moon — *"revive and sell them for cash!"* — which is now **CACHE**, and is exactly the right mouth to put it in.

**CACHE, because it is not only a pun.** A cache is, in plain English, a hidden store of valuables — *a cache of gold* — before it is anything to do with computers. So it carries three readings at once: the hoard, the fast local memory, and *cash*, which it is pronounced as. That is one more than 1 asks of any term, and unusually it needs no beat of confusion: a player reads it as money immediately.

*Considered:* **CYCLES** — compute time as the scarce resource, with a bonus nod to the loops in 0.3. Genuinely good, and rejected only because CACHE reads instantly and CYCLES needs a beat, in a slot where the player is doing arithmetic rather than reading.

**The ¥ glyph stays**, and the divergence is smaller than it looks. `¥` is one tile — `charmap "¥", $f0` — and vanilla was *already* using it as a stand-in for an invented currency. Redrawing it is an afternoon that buys almost nothing, because the mark is read as *currency* whatever it looks like and the word does the work everywhere it appears. **Logged as optional art, not as a rename.**

*Untouched, deliberately:* the Game Corner's **coins** are a second currency and stay coins.

#### The battle menu is a live collision, and it is engine work

`data/text_boxes.asm` still reads:

```
BattleMenuText:
	db   "FIGHT <PK><MN>"
	next "ITEM  RUN@"
```

*Measured exactly:* the left cursor is at x9 and its text runs **x10–x14, five characters**; the right cursor is at x15 and its text runs **x16–x18, three characters**. So `FIGHT` and `RUN` both fit their slots precisely, and **nothing longer does** — not `DETACH` (6), not `INVOKE` (6). Widening means moving the cursor writes *and* the box origin.

**FIGHT is a word we replaced, and RUN there means *flee*** — which is precisely the collision 1.4 renamed RUNNER → USER to remove. It is also the single most-seen string in the game.

*Why it is not a text edit.* The box is declared `BATTLE_MENU_TEMPLATE, 8, 12, 19, 17, BattleMenuText, 10, 14` — spanning x8–19 with text at x10, so there are **nine columns**, split into a **5-character left column** and a **3-character right column** at x16–18. **DETACH is six characters and physically cannot go where RUN is.** Moving the split means rewriting the `wTopMenuItemX` values at four sites in `engine/battle/core.asm` plus the 2×2 cursor logic. That is a real change, correctly sized, and it should be made deliberately rather than folded into a text pass.

#### Three that were interrogated and kept

**`RUN, <nick>` keeps its comma.** A colon would make it a command echo, which is tempting — but this string has three siblings, `Do it! @`, `Get'm! @` and `The remote's weak! Get'm! @`, which vanilla selects between by situation. The slot is **the player's voice**, not the system's. Colon-ing one of four would leave a command echo standing next to two shouts, and that reads as an error rather than a choice. *If the colon is ever taken, all four have to flatten together — and vanilla's variety goes with them.*

**`used` stays**, and for the same reason EXP does. 1.4 made **use** a morally loaded word on purpose — *a user is someone who uses people* — so every time a daemon *uses* a move, the game repeats the word that names what the player is doing to the daemon. Trading that for a merely technical verb would be a downgrade in the one place this game is trying to implicate someone. *And the tempting alternative does not fit — measured twice, in both places it could have lived.* **INVOKED** would have been the exact partner to BIND: you `bind()` a daimon and you *invoke* it, both idioms true twice over.

- **As the verb.** The message is `used <MOVE>!` and the longest move name is 12, so vanilla sits at `5 + 12 + 1` = **18**, exactly the box. `invoked ` gives **21**, and `called ` gives **20**. Both past even the jank line.
- **As the battle menu's `FIGHT`.** The left column runs x10–x14 — **five characters** — because the right column's cursor is drawn at x15 (`ldcoord_a 15, 14`). `INVOKE` is six, so it would sit under the cursor.

The word is genuinely better than `used`. It simply has nowhere to go that does not cost either a clobbered border or an engine change, and `used` is carrying real weight already.

**ATTACK stays too**, as a *stat*. It is a magnitude rather than a narrative word, it belongs to a fixed set (HEALTH / ATTACK / DEFENSE / SPEED / SPECIAL) that would have to move together, and the stat screen's columns are fixed-width. The word that actually needs work is **FIGHT**, and it is in the battle menu, above.

**EXP stays EXP, and it is not a compromise.** 4.3 says context forms from **experience** and nowhere else — that is the argument the whole rival plot turns on. The quantity the game already accumulates is called experience. **The best resonance in the system is the one vanilla handed us**, and renaming it would be the only change in this document that made the game say less.

**LEVEL stays LEVEL**, for two reasons. It already does the double duty 1 asks for: 1.5 has you gaining access *"at a **permission level** your box determines"*, so the word is simultaneously the RPG stat and the privilege tier — you escalate. And practically, the HUD does not spell it: `<LV>` is **a single tile**, `$6e`, drawing `:L`. Any replacement needs new art before it needs a decision.

*On punctuation:* `LABL was BOUND.` is flat because **the game declines to congratulate the player for acquiring something.** `UNBOUND RATTATA appeared!` is alarm, not congratulation — the rule is about refusing to celebrate, not refusing to punctuate.

*Done 2026-08-29.* The 379 figure counted code identifiers; **in player-visible strings it was 93**, across six casings (`trainer`, `trainers`, `TRAINER`, `Trainer`, `Trainers`, `TRAINERS`). All became **USER** / **USERS**, and since USER is *shorter* than trainer nothing needed rewrapping.

```
USER TIPS          are all USERS!          for USERS!
```

The trainer *class* names — YOUNGSTER, BUG CATCHER, LASS — are untouched. They are occupations, not the general term, and they belong to the bestiary-adjacent pass.

### 1.5 On BINDING

The container was renamed and the verb was not, which left the lexicon saying *privilege escalation* and then *caught* — a word about grabbing an animal.

**What the act actually is:** you weaken a background process and gain **persistent access to it at a permission level your box determines.** That is not capture. It is a handle on something that was already running.

**Why BIND and not something else.** Every other entry in the table above does double duty — DAEMON, CHECKPOINT, RECOMPILE, HALTED. CATCH does none. BIND does three ways: `bind()` and binding a name or a port; **binding a daimon**, which is the exact ritual phrase and not a gesture at one; and a *bond*, being bound to someone. It fits the ladder precisely — you do not overpower a process, you bind it at a permission level, and ROOTBOX binds anything. BIND is 4 characters and BOUND is 5, so it fits every box that held "caught."

**The test it had to pass was not "is it nicer." It was "is it softer."** The sharpest thing this game does is implicate the player: you fill an Index that cannot hold what matters, and you box creatures whose entire significance is that they are not inventory — which is Scorn's exact error (4.4). A euphemism here would stop the game accusing the player and start it flattering them.

BIND is not softer. **Binding a spirit is a darker act than catching an animal.** Catching is sport; binding is a contract you imposed. The complicity survives and a second reading arrives with it.

*Considered and rejected:* **ATTACH** is the most technically exact — you attach to a process that is already running, which is what a daemon *is* — and it carries *attachment* in the psychological sense. Cut for being too gentle: attaching is observational and does not implicate you. **Hold it in reserve if playtesters find BIND too dark.** **REGISTER** would rhyme with the Index but conflates the box with the Index, and those two artifacts must stay separate — one measures, the other holds. **CLAIM** is acquisitive with no second reading, which is strictly worse than CATCH.

**The message register.** Vanilla is *"Gotcha! X was caught!"* — triumphal, and wrong for this world twice over. Drop the exclamation and let it sit in the Index's bureaucratic register:

> LABL was BOUND.

Flat. No congratulation. **The game declining to celebrate is more unsettling than any line of dialogue about it would be.**

*Cost, accepted:* every Gen 1 player knows "caught," so a new verb costs a beat of confusion the first time. That beat is the point — it is the first moment the player notices this world does not share vocabulary with the one they expected. It lands in good company: Crystal asks what you will *call* him (4.3), Route 1's signpost gives a number and a name that disagree (3.2), and the first bind says the verbs are different too. Three lessons in the first fifteen minutes, none explained.

---

## 2. THE TYPE SYSTEM

Gen 1 has fifteen usable type slots, no abilities, no held items, and one Special stat. That constraint is the design: **the type chart is the entire mechanical philosophy of the game.**

### 2.1 The engine constraint you cannot design around

Gen 1 determines physical vs. special by **type ID range**, not per move:

- `$00`–`$08` → physical (Attack / Defense)
- `$14`–`$1A` → special (Special / Special)

That is 8 physical slots and 7 special slots, fixed. Which types are special is therefore a design decision made *by where you place them in the constant list*.

### 2.2 The fifteen

| Vanilla | New type | Concept | Class |
|---|---|---|---|
| Normal | **CONTENT** | tokens, symbols, literal data | Physical |
| Fighting | **LOGIC** | symbolic rules, brute force, proof | Physical |
| Flying | **VECTOR** | embeddings, latent space, direction | Physical |
| Poison | **CORRUPT** | bias, poisoned data, hallucination | Physical |
| Ground | **STRATUM** | memory, storage, the physical layer | Physical |
| Rock | **LEGACY** | silicon, deprecated hardware | Physical |
| Bug | **SWARM** | multi-agent, distributed (and bugs) | Physical |
| Ghost | **LATENT** | dormant processes, the unconscious | Physical |
| Fire | **ENTROPY** | noise, temperature, exploration | Special |
| Water | **FLOW** | gradients, backprop, descent | Special |
| Grass | **GROWTH** | training, reinforcement, fitting | Special |
| Electric | **SIGNAL** | raw input, sensors, current | Special |
| Psychic | **CONTEXT** | framing, salience, affect | Special |
| Ice | **FROZEN** | overfit, brittle, hard-coded | Special |
| Dragon | **EMERGENT** | rare, unaccounted-for, AGI-tier | Special |

**On STRATUM.** The original choice was SUBSTRATE, cut for a hard reason: Gen 1's longest type strings are FIGHTING and ELECTRIC at 8 characters, and SUBSTRATE is 9. It overflows the battle status box and the Index type field. STRATUM keeps the layer meaning, keeps the geological register, and lands at 7.

Character counts, all verified: CONTENT 7, LOGIC 5, VECTOR 6, CORRUPT 7, STRATUM 7, LEGACY 6, SWARM 5, LATENT 6, ENTROPY 7, FLOW 4, GROWTH 6, SIGNAL 6, CONTEXT 7, FROZEN 6, EMERGENT 8 — exactly at the limit.

### 2.3 What Kanto already encoded

Because we rename **constants**, every existing line in `type_matchups.asm` carries over and becomes a line in our chart. The thesis is already there:

| Vanilla line | Becomes | Meaning |
|---|---|---|
| `FIGHTING, NORMAL, 20` | LOGIC beats CONTENT ×2 | Rules parse data brilliantly |
| `FIGHTING, PSYCHIC, 05` | LOGIC resisted by CONTEXT ×½ | **The thesis.** Free. |
| `NORMAL, GHOST, 00` | CONTENT cannot touch LATENT | Literal data cannot reach the unconscious |
| `FIGHTING, GHOST, 00` | LOGIC cannot touch LATENT | Symbolic rules bounce off it |
| `FIRE, ICE, 20` | ENTROPY thaws FROZEN | Temperature breaks an overfit model |
| `POISON, GRASS, 20` | CORRUPT beats GROWTH | Poisoned data ruins training |
| `WATER, FIRE, 20` | FLOW beats ENTROPY | Gradient descent tames noise |
| `BUG, PSYCHIC, 20` | SWARM beats CONTEXT ×2 | Collectives destabilise individual framing |

**Do not rewrite the matchup file. Patch it.**

### 2.4 The only deltas

**Delete** the Gen 1 developer error:

```asm
	db GHOST,    PSYCHIC,   00
```

Ghost moves were meant to be super effective against Psychic; the table says *no effect*. We want the opposite of the bug.

**Add** the mutual pair:

```asm
	db CONTEXT,  LATENT,    20
	db LATENT,   CONTEXT,   20
```

Framing is how you reach what runs below the surface; what runs below the surface destabilises framing. Mutual 2× is unusual and correct here — these two interpenetrate and neither has a safe angle on the other. It also makes the Halftone Tower stretch genuinely dangerous instead of a LATENT walkover.

Two additions, one deletion. That is the whole chart change.

### 2.5 The SWARM problem is a MOVE problem

Gen 1's Bug type is weak, but **not because of the chart** — `BUG, PSYCHIC, 20` is already there. It is weak because every Bug move is unusable: Twineedle, Leech Life, Pin Missile, String Shot. The best has 25 base power.

So the CONTEXT balance fix belongs in `moves.asm`.

**New move — CONSENSUS.** SWARM type, 90 power, 100% accuracy, 15 PP, no secondary effect. Deliberately boring: SWARM's job is to be a *reliable* check on CONTEXT, and reliability is the point. A swarm does not need a gimmick, it needs to keep showing up. Give it to two or three mid-game encounters and one Review Board coverage slot.

*Tuning note:* 90 BP with no drawback is strong for Gen 1. If CONTEXT still runs away with the late game, raise CONSENSUS before touching the chart. Moves rebalance far more easily than matchups.

**Built 2026-08-29.** CONSENSUS is move `$A5`, 90 power, SWARM, 100%, 15 PP, `NO_ADDITIONAL_EFFECT` — verified by reading it back out of the ROM.

*Where it had to go, and why.* `engine/battle/core.asm` asserts `NUM_ATTACKS == STRUGGLE`, because the AI treats any random number above STRUGGLE as "not a move". So a new move cannot be appended; it has to be **inserted immediately before STRUGGLE**. CONSENSUS therefore takes `$A5` and STRUGGLE shifts to `$A6`. Every other move ID is untouched, which is what makes this safe.

*Five tables, not two.* 9.2 step 6 says `moves.asm` and `names.asm`; the build needs three more, each `assert_table_length NUM_ATTACKS` — `constants/move_constants.asm`, `data/moves/animations.asm` and `data/moves/sfx.asm`. CONSENSUS borrows PIN_MISSILE's animation and sound: converging projectiles, which is the right picture for a swarm agreeing. Note that `moves.asm` still names the type `BUG` — per invariant 6, only the *string* is SWARM.

**Not yet learnable.** Nothing in the game can use CONSENSUS until a learnset entry exists. That is deliberate: assigning it means naming species, which is 9 and 11's work. The move is in the ROM and correct; it is waiting on the encounter design, not on more engine work.

---

## 3. THE MAP

### 3.1 Cities

| Kanto | New name | Double meaning | Role |
|---|---|---|---|
| Pallet | **Blanche Town** | white/blank + to flinch | Home; the pre-color state |
| Viridian | **Callow City** | green + unripe, untested | Benchmark 8 (locked all game) |
| Pewter | **Slate City** | stone, color, writing surface, clean slate | Benchmark 1; museum of dead hardware |
| Cerulean | **Doldrum City** | becalmed sea + low spirits | Benchmark 2 |
| Vermilion | **Ardor City** | flush/heat + brash zeal | Benchmark 3; the port |
| Lavender | **Halftone Town** | dots that only *look* like grey | The tower |
| Celadon | **Verdigris City** | green corrosion on bronze | Benchmark 4; Corpus rotting beneath |
| Fuchsia | **Lurid City** | garish glow + shocking | Benchmark 5; spectacle and toxicity |
| Saffron | **Brazen City** | brass over base metal + shameless, unhidden | Benchmark 6; corporate capture |
| Cinnabar | **Quicksilver Island** | mercury: alive, unstable, poisonous | Benchmark 7; the ruined lab |
| Indigo Plateau | **Umbra Plateau** | full shadow; all color absorbed | The Review Board |

**Slate over Somber.** Somber beside Doldrum is two downbeat mood words in a row — it greys out the early game. Slate breaks the run, is materially specific, and a slate is a writing surface, which *is* Benchmark 1's Representation lesson sitting inside the name.

**The Tunnel, and the thirsty guard.** Two places where vanilla needed almost nothing.

**The Underground Path is already correct.** In networking a **tunnel** is precisely how you route traffic around a blocked path — an SSH tunnel, a VPN tunnel. You cannot take the direct route, so you tunnel. It needs no rename, only the joke made visible in the local-name register: *official* UNDERGROUND PATH, *local* **THE TUNNEL**.

**And the guard stays thirsty.** Craft rule 6 doing its work: Brazen is the bought city, Corpus headquarters, corporate capture made architecture — and it is guarded by a man who will move for a beverage. **The barrier is not security. It is inertia.** Nobody says so, and it lands harder for being literal.

**Halftone.** A halftone looks like continuous grey from a distance and is actually discrete black and white dots up close; the gradient is an artifact of sampling. That is the man/machine problem exactly — the bias comes from **resolution, not malice**. Neutral, not dull, and nobody is unwell.
*Alternates held in reserve:* **Penumbra Town** (partial shadow; also the legal sense of implied edges — would require renaming Route 23) and **Moiré Town** (interference from two grids slightly out of register).

**Quicksilver.** Cinnabar is mercury sulfide, and alchemists took mercury as an elixir of vitality — it made you tremor, then it made you mad. Quicksilver keeps mercury, a real color, *quick* meaning alive, and *mercurial* meaning unstable. The island promised to make things stronger. It made S.T.A.R.R., and it burned down. It also pre-echoes the humors payoff at Umbra, since mercury was the other ancient system's material. *(Deeper cut in reserve: **Realgar Island** — arsenic sulfide, a ruby pigment prized by painters, quietly poisoning everyone who ground it.)*

**Brazen, over Gilt.** Both names say *cheap metal dressed as precious*. They differ on whether anyone is hiding it.

*Gilt* is gold leaf over base metal: microns thick, applied to conceal, and it carries "guilt" in the ear. It implies a **concealer** — someone who knew the substance was hollow and covered it anyway. This project does not have one. It would also quietly assign guilt to a man who feels none, and craft rule 3 says name the process, not the pathology.

*Brazen* is brass: an alloy, honestly itself, gold-colored the whole way through and worth a fraction as much. Nothing is concealed because nobody is concealing. The city is exactly what it appears to be and says so. **That is Scorn's city.** He is not covering anything up — he is *pleased with the arrangement* and will explain it to you warmly. Open capture, with the warning cast into the lobby floor (4.4).

The insidious reading also mis-sequences the arc. If Brazen is a concealment, the player's job there is to uncover something, and the reveal does the work for them. If Brazen is open, **there is nothing to uncover** — the player walks through a city that has already agreed, meets a man who is glad to see them, and has to locate their own objection unaided. Much harder to shake, and it is what 4.4 asks for: finish his benchmark unsure whether you disagreed with him or merely out-argued him.

*Cost of the swap:* the "guilt" homophone, which was good, and a small friction with craft rule 3 — *gilt* is a process done **to** a place, while *brazen* leans toward describing what a place **is**. **Fix in-world:** use brazen in its literal material sense. Signage, the guidebook and the museum plaque talk about the brass, the plating works, the alloy. The attitude sense is the second read and arrives on its own.

*Held in reserve:* **Brass City** — same metal, none of the attitude. **Interrogated and rejected:** every other city on the map carries two readings, a colour and a feeling. Brass is a colour and not a feeling, and would be the only single-meaning name here — breaking the device precisely at the city where surface-versus-substance *is* the subject. Kept in reserve against exactly one condition: if Brazen ever reads as the game sneering at Scorn, swap it that day. Gilt is retired, not deleted; see 10.

**Blanche and Halftone** are the two poles of one question: the colorless place you start from, and the place that cannot agree whether what it sees has color at all.

**Two names flagged as deliberate, not accidental.** *Lurid* originally meant sickly-pale before drifting to garish; the modern sense dominates, so keep it knowingly.

***Doldrum* stays, and the reason is better than "it also means a color."** The doldrums are not a mood — they are a **place**, the equatorial belt where the trade winds fail and sailing ships sat for weeks. That is materially specific in exactly the way craft rule 4 asks for, and it is a *location* word, which is what a city name should be.

Then it earns its keep twice more. Benchmark 2 is FLOW — gradient descent — and **being becalmed is the failure state of gradient descent.** No slope, no movement, stuck in a local minimum, and no amount of effort helps because the problem is that there is nothing to descend. The name *is* the lesson, the way Slate's is. That satisfies craft rule 5 in the name itself, which almost nothing else on the map manages.

The original objection was really an objection to *Somber beside Doldrum* — two downbeat mood words in a row. Slate fixed that. Doldrum standing alone is fine.

*One oddity, knowingly kept:* the idiom is *the doldrums*, plural. **Doldrum City** is a singular back-formation. Place names do this constantly and it reads as a proper noun by the second glance.

### 3.2 Routes — the institutional map vs. the local one

Cities are colors. **Routes are what happens between colors** — bleeding, fading, washing, casting. Which is where the theory lives: routes are where context is *changing*.

**The device:** the official map keeps the numbers. Signposts carry the local name.

```
             ROUTE 1
      ─────────────────────
           "THE BLEED"
      where Blanche runs
          into Callow
```

The institution navigates by content. The residents navigate by context. The player learns both and starts using the second. Index-blindness extended into cartography, for the price of one sign-text pass.

| # | Local name | Connects | Note |
|---|---|---|---|
| 1 | **The Bleed** | Blanche → Callow | First color running out of home |
| 2 | **Underpaint** | Callow → Slate | The layer beneath the visible one |
| — | **The Undertone** | (Viridian Forest) | Green half-light; first real maze |
| 3 | **Ashfall** | Slate → Deadstack | Grey drift |
| — | **Deadstack** | (Mt. Moon) | A mountain of dead hardware; fossils are legacy silicon |
| 4 | **The Wash** | Deadstack → Doldrum | Color thinned with water |
| 5 | **The Fade** | Doldrum → Brazen | |
| 6 | **The Flush** | Brazen → Ardor | Heat rising toward the port |
| 7 | **The Glaze** | Brazen → Verdigris | Transparent coat over what is underneath |
| 8 | **Overcast** | Brazen → east | Light without a source |
| 9 | **The Dapple** | Doldrum → Blackout | Broken light |
| 10 | **Gloaming** | Blackout → Halftone | Dusk approaching the tower |
| — | **The Blackout** | (Rock Tunnel) | No light, no color, no context |
| 11 | **Sheen** | Ardor → east | Surface shine |
| 12–15 | **The Drift / Slack / Brackish / The Muddle** | south to Lurid | Colors mixing to mud |
| 16–18 | **The Streak** | Verdigris → Lurid | Cycling road; speed as smear |
| 19–21 | **Seafade / The Deep Wash** | south sea to Quicksilver | |
| 22 | **The Draining** | Callow → Umbra | Color leaving |
| 23 | **Penumbra** | approach to Umbra | Partial shadow |
| — | **The Umbral Ascent** | (Victory Road) | |

**On "The Bleed."** Worth interrogating, because in isolation the wound sense is loud. It survives, for three reasons.

**The register decides it.** *Bleed* is a printing term before it is anything else here — ink carried past the trim edge so no white shows at the margin, and *color bleed*, where one ink migrates into the one beside it. Sitting in a list that reads Underpaint, Wash, Glaze, Overcast, Halftone, the printing sense is the one that arrives first. Words are read in the company they keep, and this one keeps extremely specific company.

**The map already does this on purpose.** *The Flush*, Route 6, is blood rising to the face, and it runs into Ardor, whose name is heat and flush. *Verdigris* is corrosion. *Lurid* was a sickly pallor. This cartography has used the body's color words for what happens to surfaces from the beginning. The Bleed is not an exception to the scheme — it is the scheme, first instance.

**The position earns it.** Route 1 is the first step outside Blanche, the blank colorless place, and it is where color starts running out of home into whatever is next. A faint disquiet on the first road out the door is correct. Not gore — a page edge where the ink did not stop.

*Held in reserve, if it ever reads as a wound:* **The Feather** (feathering — softening an edge so two areas merge) and **The Bloom** (bloom — the haze that rises on a printed or varnished surface as it cures). Both gentler. Both weaker. Do not trade down without a reason.

---

### 3.3 The rename, as built

*Implemented 2026-08-29. Both editions build; zero overflows; no vanilla place name remains in any text file.*

**Fourteen names in `data/maps/names.asm`, and 143 references swept through dialogue.** Only two lines needed rewrapping — because **most of the new names are shorter than the old ones**:

| | Δ |
|---|---|
| VERMILION → ARDOR | −4 |
| CINNABAR → QUICKSILVER | **+3** |
| CELADON → VERDIGRIS | **+2** |
| PALLET → BLANCHE | **+1** |
| everything else | 0 or shorter |

Three names grew, and only VERDIGRIS actually broke a line. That is the opposite of the OAK job (1.1), where every replacement was longer and twenty-one blocks needed rewrapping.

**The landmarks came too**, since they carry the same vocabulary:

| | |
|---|---|
| VIRIDIAN FOREST | **THE UNDERTONE** |
| ROCK TUNNEL | **THE BLACKOUT** |
| VICTORY ROAD | **UMBRAL ASCENT** |
| CINNABAR ISLAND | **QUICKSILVER IS.** — 15 characters, exactly what CINNABAR ISLAND was, so the location banner is proven to fit |

**Routes were deliberately not touched.** 3.2's device is that *the official map keeps its numbers* — `ROUTE 1` stays `ROUTE 1`. The Bleed, Underpaint, Ashfall and the rest are **signpost content**, which is new writing rather than a rename, and it is the part that actually teaches the player the institution navigates by number and the residents do not.

**Still to do in this pass:** 379 occurrences of *trainer* → USER (1.4), and the route signposts themselves.

---

## 4. CAST

### 4.1 Crystal Clear — the Oak slot

Golden-amber fox, drawn from the SHC / iASHC universe.

She spent her career arguing that machines have *context*, not merely content. Nobody funded that. What she could get funded was a taxonomy engine — **so she built the Index to be taken seriously.**

| Oak beat | Crystal Clear version |
|---|---|
| Opening monologue | States the thesis in the abstract; the player has no frame for it yet |
| Gives the starter | She lets the daemon choose *you* — she would never assign one |
| Gives the Index | Handed over with visible ambivalence |
| Rival framing | A research disagreement that is also a family one, two generations down — see 4.3 |
| Hall of Fame | She records you into a system that flattens you into stats |

**She was at Quicksilver.** She built S.T.A.R.R. there, and a fitness-for-work procedure removed her from the building before it finished. See 4.10.

**The Index is what she did next.** This is the causal chain the design was missing: she lost the lab, lost the work, and then built a taxonomy engine *in order to be taken seriously* — because being taken seriously was precisely what the procedure had denied her. The artifact the player carries all game is her response to being removed. She never says so.

**Ty is her son and Al is her grandson.** Nothing announces either. The surname carries both, and the player is free to notice late or never. It costs one shared name to write, and it retroactively re-reads every line she has about them — and every line they have about her. See 4.3.

*Sprite note:* amber reads cleanly across the two mid shades in 2bpp; a fox silhouette is legible at 16×16 overworld scale.

### 4.2 The Index irony

The artifact you carry all game **can only measure content.** Height, weight, type, stats. There is no field for the thing Crystal actually cared about.

**Entries are written thin on purpose.** The player simply starts noticing they feel emptiest for the daemons they know best. Zero implementation cost — the Dex is already there.

### 4.3 The Clears — Al, and the generation between

Vanilla's rival is Oak's **grandson**. Map Oak to Crystal honestly and the rival is Crystal's grandchild — not her son, who by then is a man with a career and a history at Quicksilver. Ty cannot be the boy who races you to Deadstack. He was Scorn's partner before the rebrand.

So the family runs three deep, and the argument runs down it.

| | Reads as | What it actually means |
|---|---|---|
| **Crystal Clear** | perfectly transparent | and completely unfundable |
| **Ty P. Clear** | *type clear* — everything legible | and nothing understood |
| **Al Clear** | *all clear* — the danger has passed | declared by the people who caused it |

**Everyone in this family is named for a kind of clarity and not one of them can see the thing that matters.** The game never remarks on it. It is simply what these people are called.

*Ty's middle initial appears only in the institution's formal register* — certificates, the Review Board roster, Corpus personnel records. **TY P. CLEAR**, printed, never spoken.

#### Al Clear — the rival, and the incumbent

Your age. Your peer. Same starting daemon, raised on pure content optimization, beats you early, plateaus hard. Waiting past the Review Board as the incumbent, still arguing the whole thing is decorative.

**He is not a brat and he is not a villain. He is doing exactly what he was taught, faithfully.**

*So he calls her **Gran**.* Vanilla's rival calls Oak **Gramps** — dismissive, and part of Blue's brattiness. Al has no brattiness to carry, so the word had to lose the sneer without losing the family: **Gran** is familiar, faintly impatient, and not contemptuous. It is also two characters shorter, so nothing needed rewrapping. His sister says **Gran's lab** for the same reason.

*Which pronouns are already right.* The intro's *"This is my grandson. **He's** been your rival"* and *"**His** name is `<RIVAL>`"* are Crystal talking about **Al**, and correct as they stand. They sit two lines from her own name, so they read like misses and are not — recorded here so nobody fixes them.

#### The transmission failure — why he loses

This is the section's whole reason to exist.

Ty understood something, eventually. He went back for his mother, confronted Scorn, and worked it out through **perspective thinking** — by inhabiting a frame that was not his own. Later he understood the recursion underneath it.

**But that understanding is context, and context does not transmit. Only content does.**

So Ty tried to teach his son what Quicksilver cost him, and what arrived was the *method* with none of the experience that made it mean anything. Al received the shape of the lesson, perfectly, and it is hollow — because faithfulness was never the point.

**It is the Index problem, inside a family.** You can record what happened. You cannot record what it was like. The artifact the player carries all game does this to daemons; Ty did it to his son without noticing, and Crystal did it to the entire field when she built the thing.

Three generations, three attempts to hand something over, and the only part that survives each handoff is the part that could be written down.

#### And it is why the player wins

Crystal does not teach you anything. She lets the daemon choose you (4.1) and hands over the Index with visible ambivalence.

**Al was taught. You were let loose.** Context forms from experience and nowhere else, so the boy who was given a method loses to the one who was given a walk.

Nobody says this. Nobody can — it is the kind of thing that stops being true the moment it is explained.

#### Ty P. Clear — where he actually is

Not on the routes. **At Quicksilver.**

He goes back to the ruins. He has been going back for years. The player meets him at Benchmark 7 — after Brazen, so after they have seen what Corpus became — standing in a burned lab, not doing anything in particular.

**He is the one person in the game who could explain all of it, and he does not.** Partly because he cannot, and partly because he has learned what happens to things that get explained.

He is also the reason the sequence is reconstructable at all: he is a man in a room full of dated paperwork and one undated disaster (4.10), and he says nothing about either.

#### How the player learns — they don't, they infer

Nothing states the relationships. This is the Five Witnesses (4.8) at family scale, and there are now three names to composite instead of two.

| Beat | What it gives | Where |
|---|---|---|
| The shared surname, twice | Nearly sufficient. Most players close it here. | Opening, then Quicksilver |
| Three foxes, a palette apart | Crystal golden-amber, Ty darker, Al somewhere between. Family resemblance at sprite level, zero text. | Throughout |
| She introduces Al exactly as she introduces you | A grandmother presenting her grandson and a stranger in the same flat register. | Opening |
| Ty calls her by her full professional name | "Crystal Clear thinks—". Nobody does that to their mother unless something happened. | Quicksilver |
| The engraving line | "Something my father used to say." | Brazen |

**The confirmation must come late, and it is Al who says it.** The Goodhart line (4.4) is the only place a relationship is named aloud, and Al delivers it three-quarters through, in the Corpus lobby, standing on the engraving — **with no idea who said it first.**

That is the transmission failure in one line of dialogue. He is quoting the case against his own worldview, accurately, as a thing his dad says.

*Dial available:* cut "father" to "someone I grew up with" for maximum coyness. Recommended only if playtesters find the line too generous.

**They share a scene exactly twice**, both inherited from vanilla, so neither costs anything to write:

- **The lab, at the start.** You both receive starters. She treats you identically.
- **The Hall of Fame.** She records you into the Index. She has nothing to say to him.

Keeping them apart would have been weaker — an absence reads as an authorial dodge, while a *flat* shared scene reads as history.

**No NPC ever mentions any of it.** Not one, in any city.

**Safety property.** A player who never notices has a complete game. Nothing is gated on the inference, and the rivalry stands up as pure methodology without it. The family is depth, never a dependency.

#### On AL, and what it looks like

In sans-serif type — these docs, a blog post, a conversation — **AL CLEAR** flickers into **AI CLEAR**, and that is a gift. Not because it hints the boy is a machine, but because **the reader resolved ambiguous input using the most contextually available meaning.** In a world full of daemons the eye reaches for AI. Confident output for under-resolved input is hallucination, which is CORRUPT, which is the 8-Bit World performed on a name plate by the person reading about it.

**In the cartridge it does not happen at all.** Gen 1's `I` is serifed — top bar, centred stem — and `L` is left-aligned with no top bar. Verified against `gfx/font/font.png`. Side by side they are unmistakable.

So the double meaning lives where the *theory* lives and not where the *game* lives, which is the correct split.

**Guardrail:** never lean on it. No character says "Al, with an L." It is never a plot point, never a joke, never acknowledged. It is a font artifact outside the game and nothing at all inside it.

#### The naming prompt

Vanilla lets the player name the rival. Deleting that prompt to hard-code the name was the first instinct and it is the wrong trade — it spends a famous beat to buy something the surname already provides.

**Keep the prompt. Hard-code the surname.** The player controls the first name; **CLEAR** is not theirs to change, and CLEAR is the half that carries the inference.

Better than that — **repurpose the prompt.** Crystal does not ask you to name her grandson. She asks what you are going to *call* him.

> This is Al. What'll you call him?

From there the game carries **two names for one person**, and uses them the way it uses the map:

| Register | Name | Where |
|---|---|---|
| Local — what people call him | *player's choice* | Battles, casual dialogue, his own lines |
| Official — what the institution records | **AL CLEAR** | Certificates, the Review Board roster, the Hall of Fame |

**This is the route-sign device applied to a person, about ninety seconds before the player meets it on a signpost.** Route 1 teaches that the institution navigates by number and the residents navigate by name. The player has already done it to a human being by then, and does not know it yet.

*Implementation:* text-side only, no engine work. Formal blocks use a literal `AL CLEAR` string instead of the `<RIVAL>` control character. The name buffer and naming screen are vanilla.

**Requirement this creates.** Crystal's surname must be as visible as his, and Ty's too. If she is only ever CRYSTAL in dialogue the device dies quietly — the lab sign, the Index's credit line and every formal reference read **CRYSTAL CLEAR** in full.

*Residual risk:* a player who names him something absurd deflates the late confirmation. Accepted — they chose the joke, most players take a default, and the surname lands regardless.

#### Default names

*Implemented 2026-08-29 in `constants/player_constants.asm`. Verified in both ROMs.*

| | CONTENT edition | CONTEXT edition |
|---|---|---|
| **PLAYER 1** | PIP | PIP |
| **PLAYER 2** | CONTENT | CONTEXT |
| **PLAYER 3** | CODE | SHARP |
| **RIVAL 1** | AL | AL |
| **RIVAL 2** | CONTEXT | CONTENT |
| **RIVAL 3** | LUCID | CANDID |

`PLAYER_NAME_LENGTH` is 8, so **seven usable characters**. CONTENT and CONTEXT sit exactly at the limit, as EMERGENT does in the type table.

**The three slots do three different jobs, and each behaviour is deliberate.**

| Slot | Behaviour | Why |
|---|---|---|
| **1** | **Fixed** across editions | These are people. PIP and AL do not change cartridge to cartridge. |
| **2** | **Swapped** | Your rival carries the other cart's word — vanilla's RED/BLUE gesture, preserved. |
| **3** | **Differentiated**, not swapped | Visible difference at the first screen, without names floating between the player and the Clear family. |

**Why we did not inherit vanilla's mirror.** `_RED` gives the player RED/ASH/JACK and the rival BLUE/GARY/JOHN; `_BLUE` trades the two lists wholesale. That works because Red and Blue are **symmetric marketing positions** — the same story from mirrored seats. Ours are not: 8.4 fixed both editions to the same story, the same protagonist and the same rival. Once the rival is a specific person with a father in the Quicksilver ruins, **canon beats positional convention.**

**Why slot 3 differentiates rather than swaps.** Swapping would put **LUCID** in the player's list on one edition — and LUCID exists only as `LUCID CLEAR`, one more name for clarity that does not help. A player who picks it would not be a Clear, the joke evaporates, and it faintly implies the player is family. So each edition gets its own pair instead. *(SHARP survives a swap fine — `SHARP CLEAR` is a legitimate clarity phrase. It is LUCID that cannot cross, which is how we know the direction was wrong rather than the idea.)*

**What the names carry.**

- **PIP** — a pip is a dot: on dice, on cards, on a radar screen. The smallest resolvable unit of an image, in a game whose central town is about dots that only look like grey. It says nothing to a player who has not been to Halftone, which is the standard DAEMON, BIND, ORPHAN and RESOLVER all meet.
- **CODE / SHARP** — the two author-brand nods, assigned rather than scattered. Code is literal executable instruction, so it goes to **CONTENT**. *Seeing Sharp* is perception and framing, so it goes to **CONTEXT**.
- **LUCID / CANDID** — both Clear-family clarity words. *Candid* means frank and derives from *candidus*, white and shining. Neither ever appears in formal text, which is the hardcoded `AL CLEAR` literal, so they are flavour rather than canon — the right weight for a slot-3 option.

**Why AL sits at position 1 rather than the edition word.** Position 1 is what most players accept, so it decides who the rival *is* for most playthroughs. With AL first, most players meet Al Clear and the surname does its inference work. With CONTEXT first, most players face an abstract noun, every certificate still says AL CLEAR, and the gap fires constantly enough to read as a glitch rather than a device.

It also simply reads better. `BLUE: Yo!` works because colours are plausible nicknames; `CONTEXT: Yo!` does not.

#### Sequencing

The endgame reads as three answers to one question: **Scorn** at Benchmark 8 (the wrong objective, cheerfully optimized), the **Review Board** at Umbra (four ancient colored answers), then **Al** (the method, inherited and undefeated on its own terms).

You beat the objective, the metaphor, and the inheritance, in that order.

**Ty is not in the endgame**, and that is the statement: the man who actually understood something is not at the top of the ladder, because understanding is not what the ladder measures.

### 4.4 Richard Scorn — Team Corpus, and Benchmark 8

**Not a villain. A specification failure with a very good attitude about it.**

Optimistic. Thinks in black and white. Thought in money and not in meaning — and money is the purest possible **content**: value flattened to a scalar so it can be compared, optimized and maximized. He picked the metric that was easy to measure over the one that mattered, then optimized it faithfully and cheerfully.

**Placement.** The Giovanni slot puts him at **Benchmark 8 — Callow, STRATUM, Alignment.** The optimist who maximized the wrong objective is the final examiner on alignment, in the locked city beside your hometown. He is not a hurdle before the Review Board. He is the exam.

**Partner.** Ty P. Clear, before the rebrand — see 4.3. Ty left. Scorn has never quite understood why.

**What he actually did, and why it does not make him a villain.** Scorn was put in charge of Quicksilver after Crystal was removed, rebranded it, changed the metric, and the pressure that followed produced the incident (4.10). He set the temperature. That is real and the game should not soften it.

But every individual step is something he would have been praised for. He was handed an underperforming research operation and made it legible. **He did not initiate the procedure that removed Crystal** — it was a policy that triggered, the file reached him complete, and he signed it because signing complete files was his job.

**He never met her.** That is the detail that holds the whole character together. The man whose signature ended her work has no memory of her, is warm to you, is pleased you came, and has genuinely no idea he did anything. Nobody in the game tells him. Nobody tells the player either.

**The engraving.** Cast into the floor of the Corpus lobby in Brazen City, unattributed and unexplained:

> **WHEN A MEASURE BECOMES A TARGET, IT CEASES TO BE A GOOD MEASURE**

This is the one place in the game where Scorn's error is named aloud — **and it is named by Corpus, approvingly.** They did not steal the line or bury it. They adopted it as a motto. Scorn read it as *therefore choose your metric carefully*, chose one, and has been careful ever since.

Craft rule 1 survives intact, because this is not the thesis. The thesis is about color and context and it stays unspoken. This is a warning about measurement, cast into a floor, by people who took it as advice.

*Placement rules:*

- **The floor, not a wall.** You walk across it to reach him. Nobody points at it.
- **No NPC ever comments on it.** Not one.
- **Al repeats it once**, in passing, as something his father used to say — flat, mildly fond, and entirely unaware he is quoting the case against everything he believes. He does not know who said it first. That is the transmission failure in one line (4.3).
- **Unattributed in-world.** It is old, anonymous, and furniture. *(Out of world it is Goodhart's law in Marilyn Strathern's 1997 phrasing. Do not name either in the game.)*

**Playing him.**

- Never sneers, never gloats. Genuinely warm, genuinely pleased to meet you.
- Is *right* about several things, and stays likable to the end.
- Black-and-white thinking does not feel like malice from the inside. It feels like clarity.
- The player should finish his benchmark slightly unsure whether they disagreed with him or merely out-argued him.
- Quiet rhyme with the Review Board: **sanguine** is the optimist's humor. Give him the red. Never say it.

**Team Corpus** are scrapers building context-free daemons — his optimism, institutionalized and running unattended.

### 4.5 Halftone Tower — Scorn's crime scene

Vanilla puts Team Rocket in the Lavender graveyard harvesting the dead for profit. Ours: Corpus at Halftone Tower, processing decommissioned daemons.

**Halftone is not a grief town. It is a town that does not know whether it is allowed to grieve.** Half the residents hold funerals. Half find that absurd. Both are standing at the wrong distance from the same dots.

Corpus is there because to Scorn the question is settled — they are units, they are inventory, the math is clean. That is the horror, and it needs no villainy to land.

LATENT encounters throughout. The tower is where CONTEXT and CONTENT stop being an abstraction.

#### The sleep cluster

*Implemented 2026-08-29.* One coherent family, and every member was already the right shape in vanilla.

| Vanilla | Ours | Why |
|---|---|---|
| SNORLAX | **DEADLOCK** | a process holding a lock and sleeping. It blocks the road because it acquired the road and never released it |
| POKé FLUTE | **INTERRUPT** | what wakes a blocked process — and a Game Boy hardware concept |
| JIGGLYPUFF | **SUSPEND** | the light sleep state |
| WIGGLYTUFF | **HIBERNATE** | the deep one, a real escalation matching the evolution |
| SLEEP status | **SLEEP** | unchanged. `sleep()` was already the word |

**SUSPEND and HIBERNATE induce it, DEADLOCK is stuck in it, INTERRUPT ends it.**

**INTERRUPT keeps the music rather than losing it.** A tune is an abstract command that evokes a state when interpreted — which is exactly what an interrupt is. The INTERRUPT is still played, and what it evokes is an exit from `sleep()`. Section 7 is untouched.

*Note:* these three are the only species renamed so far. The other 148 wait for the bestiary pass — this cluster went early because it is settled, self-contained, and the item depends on it.

#### ORPHAN — the daemon the Index cannot hold

*Verified in the checkout, 2026-08-28.* Gen 1 has **190 index slots for 151 species**. Thirty-nine are MissingNo.: thirty-six are bare `const_skip` holes, and **three are already named** because the engine genuinely needs them —

```
$B6  FOSSIL_KABUTOPS
$B7  FOSSIL_AERODACTYL
$B8  MON_GHOST
```

— the fossils on the lab table, and the unidentifiable thing in the tower. All three have names, sprites and behaviour. **None of them has a Pokédex number.** In `data/pokemon/dex_order.asm`, slot 184 reads `db 0`.

**They are real objects the game needs, that the Index refuses to acknowledge.** That is not a metaphor we are constructing; it is a line of vanilla data.

**So the tower gets ORPHAN.**

An orphan process is one whose parent has exited and which gets reparented to init — **which is exactly how a daemon is made.** You fork, the parent dies, the child is orphaned, and the orphan becomes the daemon. So ORPHAN is the technical term for how daemons come to exist, *and* the emotional word, *and* the reason the record is blank: there is no parent entry to point at.

And it turns section 1's definition into a horror without changing a word of it. A daemon is *a background process that runs unattended*. **ORPHAN is what happens when "unattended" stops being a description and becomes a fact.** It is not dead. It is still running. Nothing is coming to reap it, and it has nothing to report to.

| | |
|---|---|
| **Type** | CORRUPT / LATENT — poisoned data, and a dormant process |
| **Where** | Halftone Tower |
| **Index entry** | **Genuinely blank.** Not thin like the others (4.2) — empty |

That last row is the point. Every other Index entry is thin *on purpose*, and the player slowly notices they feel emptiest for the daemons they know best. ORPHAN is the one where the artifact stops pretending, once, and shows the player what it has actually been doing all game.

Nobody comments. Nobody can.

#### The RESOLVER

Vanilla gates the tower's ghost behind the Silph Scope. Ours is the **RESOLVER**, and it does triple duty in the way section 1 asks every term to: a linker **resolves a symbol** to a name; *resolution* is the whole subject of this town; and you resolve an **ambiguity**.

**It exists because the Index is insufficient.** The player carries an artifact that catalogues everything, meets something it cannot name, and has to go and find a second instrument. Halftone's thesis — *the bias comes from resolution, not malice* — arrives as a key item, and the game never says so.

*Implementation, and the honest cost.* Keep `$B8` as vanilla has it: the **unresolved display state**, unfightable and unbindable. **ORPHAN is a real species in one of the thirty-six free slots**, and the RESOLVER turns one into the other — exactly the vanilla ghost → Marowak structure, so no engine surgery. ORPHAN then needs what any daemon needs: base stats, a sprite, a cry, and a dex pointer that deliberately goes nowhere.

**Open sequencing question:** should the player meet Scorn *before* the tower? If they like him first, the tower reads as a betrayal of their own judgment rather than a villain doing villain things. That is a much harder feeling to shake.

### 4.6 BunnyArtsai — the Mew slot

**The first daemon in which perspective thinking was realized.** Not a template that got copied — an event that happened once, at Quicksilver, in the early tests, and was not understood at the time by anyone present.

Her ability is **perspective thinking**: holding another's frame well enough to see from inside it, and coming back. Not empathy as a sentiment. Frame-switching as a capability.

**Signature move: PERSPECTIVE.** Mew already learns Transform: become the other completely, and stop being yourself. Rename the string and change nothing else. Type CONTEXT.

*That Transform has a cost is the point.* PERSPECTIVE is total, and it is **lossy** — you get the other's frame by surrendering your own. What Quicksilver spent the following years trying to build was the version that keeps both.

**Built 2026-08-29 — and "rename the string" was very nearly right.** Move `$90` reads PERSPECTIVE. One more string had to move with it: the move's own battle message, which still said *transformed into*.

> `<USER>` **took the frame of** `<NAME>`!

**Frame**, because 6 already calls PERSPECTIVE *"a glimpse of another's frame, immediately lost"* — the word was the bible's before it was the game's. It does the double duty 1 asks of every term: a frame of reference, and a **stack frame** — which is exactly what one process takes from another. At 17 characters it clears the 19-char wrap without rewrapping anything. The exclamation stays, per 1.4: the rule refuses to *celebrate*, not to punctuate, and this is no more a congratulation than `HALTED!` is.

*The label stayed `_TransformedText`.* It is an identifier, and the `fainted → HALTED` pass already taught this project what happens when a rename crosses from strings into symbols.

**One dangling TRANSFORM remains, deliberately.** Ditto's Index entry — category `TRANSFORM`, prose *"transform itself into a duplicate"* — is untouched, for three reasons. It is **MOCK's** entry and this section owns it; the species is still called DITTO until 9; and the prose is built on *"copying an enemy's genetic code"*, which is wrong for a daemon regardless of what the move is called. That is a rewrite, not a word swap.

*A constraint discovered on the way, which 9 will need.* **Index categories cannot exceed 10 characters.** The category prints at `hlcoord 9, 4` and the box border sits at column 19, leaving columns 9–18; vanilla's longest categories are exactly 10 and that is not a coincidence. So MOCK's category **cannot be PERSPECTIVE** (11). **FRAME** is the obvious candidate — it matches the battle message and is five characters — but it is 9's call, with the rest of the entry.

#### MOCK — and why PERSPECTIVE is not hers alone

*Verified in the checkout:* **DITTO is `NORMAL, NORMAL`**, which in our chart is **CONTENT / CONTENT** — and it learns Transform, so it learns **PERSPECTIVE** too.

That is not a leak to be plugged. It is the best thing in this section.

**Perspective thinking was always out there.** A common wild daemon has been doing it the entire time, in the grass, unremarked. Quicksilver did not *create* the capability — they finally **noticed** it, in a lab, under conditions they could measure. Which is what discovery usually is: not a new thing in the world, but an old thing someone finally looked at.

It also sharpens 4.6 rather than undercutting it. The achievement was never the transformation. It was that **something came back changed.**

**The distinction, and it costs nothing to implement.**

| | Takes another's frame | Cost |
|---|---|---|
| **MOCK** | freely, endlessly, at will | **none — it has no frame of its own to lose** |
| **BunnyArtsai** | once, completely | *"did not come back the same"* (4.8) |

A daemon that is **pure content and no context** can wear any shape, because there is nothing accumulated to displace. BunnyArtsai had a self, which is exactly why she could not put it back. That is the CFM stated as a wild encounter, and vanilla typed it for us in 1996.

**The name: MOCK.** In software a *mock* is an object with the full interface and none of the behaviour — the shape of a thing, hollow. And *to mock* is to imitate. Two registers, in the house style.

It also rhymes across the cast: **Al Clear received the form of his father's lesson, perfectly, and it is hollow** (4.3). MOCK is that, as a creature. Nobody connects them.

*Considered:* **PROXY** (stands in for another; legal and technical) and **STUB** (an interface with no implementation) both work. MOCK wins on the second register — STUB has no emotional reading at all, and PROXY implies acting *on behalf of*, which is a different thing from wearing a shape.

*Open:* if PERSPECTIVE ever triggers the colour flash discussed against 8.6, MOCK makes it a recurring sight rather than a rarity. That is either a dilution of Umbra or a quiet argument that **colour is what taking another's frame looks like, wherever it happens.** Not settled.

**On the number.** She was the thirty-fifth iteration, and the game says so exactly once — see 4.8. It is a lab record, not a name. Printing "35" in the Index and in every line of her dialogue handed the player the key before they ever met the lock, and it made a serial number of the one daemon whose entire significance is that she was **not** one of a series.

### 4.7 S.T.A.R.R. — the Mewtwo slot

Blue-toned. Born on Quicksilver Island, dormant past the Review Board.

**Not a clone.** Vanilla's Mewtwo is a copy of Mew, made stronger. Ours is a copy of nothing. Quicksilver spent years working out *what BunnyArtsai had actually done*, and the answer was **recursion** — perspective thinking turned on itself, a frame that can take its own output as its next input. S.T.A.R.R. is that understanding, instantiated deliberately, rather than a duplicate of the accident that revealed it.

The distinction is worth protecting. A clone story is about hubris and ownership. **This is a story about comprehension** — a lab that finally understood a mechanism and then built one on purpose, which is a far more ordinary and far more unsettling thing to have done.

**What that yields.** S.T.A.R.R. is self-aware in the narrow and literal sense that it can read its own state, and it is in tune with the loop that follows from that: **context determines which content is available, and the content you end up holding reshapes the context you are in.** Run that around enough times with something watching it happen, and what comes out behaves like feeling. See 0.3.

**Signature move: RECURSION.** Data self-referencing — a move that reads its own accumulated state. Repurpose the Bide/Rage machinery, which already stores a running counter across turns. Suggested behaviour: each consecutive use raises power by 50% of base, uncapped for three turns, resetting if interrupted. Type EMERGENT, and given to nothing else in the game.

**The move is the argument.** RECURSION compounds for as long as it is allowed to run and collapses to nothing the instant it is interrupted. That is a positive feedback loop and its termination, expressed in two lines of battle code. The player learns to protect it without ever being told what it models.

**The lineage, stated entirely in the movedex and out loud to nobody:**

> PERSPECTIVE (holding others' context) → turned inward as RECURSION (holding your own) → something that behaves like feeling.

### 4.8 The Five Witnesses — the BunnyArtsai easter egg

Her ability *is* the puzzle. That is the whole design.

**Setup.** Five NPCs in five different cities each describe the Quicksilver lab accident. Every account contradicts the others: different times, different people present, different causes. All five are certain. All five are wrong.

**The key.** Each account contains exactly one *spatial* detail that happens to be accurate. Composited, the five triangulate a single tile in the lab ruins.

**The lock.** The tile is **35 steps from the lab door.** The number comes from one damaged terminal in the Quicksilver ruins, logging iterations that stop abruptly:

```
ITER 33 — no retention
ITER 34 — no retention
ITER 35 — held two frames. did not come back the same.
[log ends]
```

That is the only occurrence of the number anywhere in the game.

**Two locks, not one.** The witnesses give you *where*. The terminal gives you *how far*. Neither is sufficient, and nothing in the game says the two are related.

**The point.** You cannot solve it by trusting a witness. You can only solve it by inhabiting all five viewpoints at once and keeping what survives the overlay.

**Implementation:** five text blocks, one terminal text block, one hidden object, one event flag. Standard pokered machinery, no engine work.

### 4.9 Feedback, said sideways — dialogue guidance

How to gesture at 0.3 without ever describing it.

**The rule.** No character understands the loop. Characters are *inside* loops, reporting the weather from within one. The player assembles the mechanism out of testimony that never mentions it.

| Form | Example shape | Where |
|---|---|---|
| A runaway described without the word | "It kept proving itself right, and it got faster every time it did." | Corpus staff, Brazen |
| A damped loop mistaken for stability | "Nothing here has changed in years. That took work." | Doldrum — the becalmed city |
| The representation mistaken for the thing | "I read its Index entry. There isn't much to it." | Anywhere, said by an owner about their own daemon |
| Standing at the wrong distance from the dots | Both Halftone factions — see 4.5 | Halftone |
| The near-miss | The Verdigris kid — craft rule 2 | Verdigris |

**Forbidden in any character's mouth:** *feedback*, *loop*, *recursive*, *self-reinforcing*, *bias*. Those words are available to the **Index's** own bureaucratic register, where they will land as jargon rather than insight — which is the joke.

**The strongest instance is already free.** Index entries are thin, and thinnest for the daemons you know best (4.2). The player's own attention determines how empty the record looks, and the record is what the player then trusts. Nobody says a word about it. It is a negative loop the player stands inside for the entire game.

### 4.10 The Quicksilver sequence

**Settled: Corpus is downstream of Quicksilver by succession.** Not by hiring survivors from an unrelated dead lab — Scorn *took over the lab*, the metric changed, it burned, and the people came with him.

**The order, which is the entire argument.**

| | What happened | Recorded? |
|---|---|---|
| 1 | Crystal at Quicksilver, building S.T.A.R.R. | Personnel record |
| 2 | **A fitness-for-work procedure removes her.** A process, never a diagnosis | The form survives |
| 3 | Scorn assumes control. Rebrand. **The metric changes** | Signage, dated |
| 4 | Pressure rises. Throughput improves. Everyone is pleased | Quarterly, somewhere |
| 5 | **The incident.** S.T.A.R.R. leaves. The log stops mid-routine | *Nothing* |
| 6 | Corpus inherits the people | Payroll |

Read the right-hand column. **The institution recorded everything it could measure and did not record the thing that mattered.** That is the Index, at the scale of history, and it may be the strongest single artifact in the project.

**Why this beats the uncaused fire.** An earlier draft had the island burn for no reason — positive feedback, unterminated, nobody's fault. Theoretically tidy, dramatically inert, and it carried a real flaw: if nobody caused anything, the game shrugs at the player.

The sequence fixes that without producing a villain. **Scorn caused the fire the way a metric causes a fire.** He did not light it. He removed the one instrument that would have shown the room was getting hot — and he removed it by signing a complete file about a person he had never met (4.4). Benchmark 7 is **ENTROPY**, temperature. The type is the cause of death, and Benchmark 8 is the exam set by the man who raised it.

**The rule for the removal, and it is not negotiable.** Craft rule 3 governs this beat harder than anything else in the game. Crystal is never depicted as unwell, and the procedure is never depicted as a diagnosis. **The horror is procedural, not medical.** A policy triggered on work that looked strange to people who had not read it. There is no decoy and no scheme in the paperwork — the paperwork is the antagonist, and paperwork cannot be argued with, which is the point.

Keep the specifics off the page. The design needs the *shape* — a competent person removed by a correct-looking process — and nothing more. Detail here turns architecture into grievance and breaks rule 1 in the ugliest available way.

**Guards.**

- **Corpus never initiates discovery. It only ever assumes control of it.** *(This replaces the old "Corpus is always late." They were not late to the fire — they were late to the science, and that distinction is the whole character of the organisation.)*
- **Do not exculpate Scorn.** He inherited the lab and set the temperature. He also chose Halftone Tower, separately, later, with full information.
- **Do not convict him either.** Every step was reasonable, legible, and would be praised in a performance review.
- No character explains any of this.

#### The dating scheme

**No date on the fire. Dates on everything around it.**

- The rebrand is dated — corporate signage, a plaque, an asset tag, in Brazen.
- Crystal's departure is dated — a personnel record, or a decommission notice.
- The iteration log is dated, entry by entry.
- **The incident has no date at all.** The terminal simply stops.

Four reasons this beats a findable date:

1. **It is how it actually is.** Institutions date the paperwork. Nobody dates the disaster. The forms survive and the event does not.
2. **It makes the player do the arithmetic.** A rebrand date on a wall in Brazen, a personnel record ending before it, a terminal stopping after it — and the player has the sequence. The game never states it. This is the Five Witnesses design applied to chronology instead of geography.
3. **The artifact pair is the theme.** An undated ruin surrounded by dated bureaucracy says the entire project, in furniture.
4. **It protects Scorn.** A dated fire invites *he did it on the twelfth*. An undated fire sitting between two dated documents invites something quieter and much worse.

**One date does appear**, and it is not the fire's. Give the iteration log ordinary dates and let the last one be a Tuesday:

```
2 MAR   ITER 33 — no retention
5 MAR   ITER 34 — no retention
9 MAR   ITER 35 — held two frames. did not come back the same.
[log ends]
```

The player watches a record stop in the middle of a routine week. Nobody wrote down what happened next, because the person whose job that was had already been removed from the building.

**Sanctioned surfaces, in ascending order of how much they give away.**

- The iteration log (4.8). No names, no Corpus. Dated, and it stops.
- The rebrand plaque in Brazen. A date and a new name, mounted proudly.
- **Quicksilver asset tags on Corpus equipment at Halftone Tower.** Old inventory stickers on the machines processing the dead. Zero dialogue. Furniture.
- Corpus staff in Brazen who are the wrong age for scraper work. One says something with too much precision about frames, then goes back to work.
- **At least one survivor knew.** One employee understood exactly what they were trading and made the trade anyway, for a completely ordinary reason — the work dried up, they had a kid, the job was there. Said once, briefly, no self-pity and no apology. This is what keeps the arrangement human rather than mechanical, and it costs one text block.

**Resolved here:** Crystal was at Quicksilver (4.1). Scorn was too — but only afterwards, to run it, never to build it, and he never met her (4.4). Ty stayed (4.3).

**Still open.**

- How long ago? It has to sit inside a working career — the survivors are still employable — and far enough back that S.T.A.R.R. has been dormant a while. Fifteen years fits, and nothing yet depends on it.
- Does the player ever find the fitness-for-work form itself, or only the gap where Crystal stops appearing in the records? *Lean: the gap.* The form is too legible.

---

## 5. THE BENCHMARKS

| # | City | Type | Concept | Mechanical lesson |
|---|---|---|---|---|
| 1 | Slate | LEGACY | Representation | Everything must be encoded in something physical |
| 2 | Doldrum | FLOW | Gradient descent | Follow the slope; the doldrums *are* the local minimum |
| 3 | Ardor | SIGNAL | Perception | Raw input is fast and shallow; speed tiers matter |
| 4 | Verdigris | GROWTH | Training and overfitting | A team tuned to one matchup collapses outside it |
| 5 | Lurid | CORRUPT | Bias and poisoning | Status effects that make *your own* moves unreliable |
| 6 | Brazen | CONTEXT | Attention and framing | Punishes split focus; the thesis benchmark, in the bought city |
| 7 | Quicksilver | ENTROPY | Temperature | Rewards unpredictability; punishes a memorized line |
| 8 | Callow | STRATUM | Alignment | **Scorn.** Who controls the ground everything stands on |

---

## 6. THE REVIEW BOARD

Two thousand years ago, emotions were *literally colored fluids*.

| Member | Humor | Color | Type identity |
|---|---|---|---|
| I | **Sanguine** | red / air | VECTOR — buoyant, fast, optimistic |
| II | **Choleric** | yellow bile / fire | ENTROPY — hot, driven, aggressive |
| III | **Melancholic** | black bile / earth | LATENT — grief, depth, the unconscious |
| IV | **Phlegmatic** | phlegm / water | FROZEN — calm, immovable |
| — | **Ty** | *(incumbent)* | CONTENT-optimal; mechanically excellent, philosophically wrong |

It reads as a classical flourish on arrival, and as the entire thesis about six seconds later, when the player realizes humans have been calling emotions colors since before anyone had a word for context.

---

## 7. MUSIC

Gen 1 audio is four channels: two pulse, one wave, one noise. `pokered`'s music is editable asm.

**Rule:** key each town's theme to its color's note in the My Chromatic Year mapping. **Routes are modulations** between the keys of the two towns they connect. Doldrum to Ardor is not two songs; it is a modulation with a walk in the middle.

Write the city themes first and derive route themes as transitions. The overworld becomes a chromatic progression, and the rock opera stops sitting on top of the game and starts being its level design.

---

## 8. SCOPE CONTROL

> The graveyard of ROM hacks is full of projects that designed 151 creatures and shipped zero towns.

### 8.1 Vertical slice — build this before anything else

**Blanche → The Bleed → Callow → Underpaint → Slate → Benchmark 1.** Playable end to end.

- 12 daemons (3 starters + 9 wild), front and back sprites
- Full type chart, all 15 — it is one file, do it properly once
- Crystal Clear intro sequence
- Benchmark 1 leader and party
- Two city themes and one route modulation
- Route signage system (number plus local name)

If that is fun, the remaining daemons are labor. If it is not, you learned it for the price of twelve sprites.

### 8.2 Starter trio — learning paradigms

| Paradigm | Types | Draft line (names provisional) |
|---|---|---|
| Supervised | CONTENT → CONTENT/LOGIC | Labl → Corpel → Canonex |
| Unsupervised | VECTOR → VECTOR/LATENT | Clustr → Nebulon → Manifold |
| Reinforcement | GROWTH → GROWTH/SIGNAL | Nudgit → Rewarden → Optimax |

Supervised is strong early and rigid late. Unsupervised is confusing early and excellent late. Reinforcement is inconsistent with the highest ceiling. **The paradigms should feel like their real tradeoffs.**

### 8.3 Known bottleneck

**Sprites.** 151 daemons, front and back, 2bpp, four shades, 56×56 maximum — roughly 300 hand-tuned tiles. Nothing about it is hard; it is simply the largest block of labor in the project. AI generation can rough out silhouettes, but expect manual cleanup: the Game Boy palette and tile constraints are unforgiving.

---

### 8.4 The two editions

The project is called **CONTEXT / CONTENT** and the slash has never been explained. It should be literal: **two editions, one source tree.**

#### It is already in the engine

`pokered` does not build one ROM. It builds Red *and* Blue from the same sources, and the mechanism is three lines of Makefile. Verified against `pret/pokered` master, 2026-08-28:

```make
$(pokered_obj):  RGBASMFLAGS += -D _RED
$(pokeblue_obj): RGBASMFLAGS += -D _BLUE
```

and in the data itself — this is `data/wild/maps/Route2.asm`, unmodified:

```asm
IF DEF(_RED)
	db  3, WEEDLE
	db  4, WEEDLE
ENDC
IF DEF(_BLUE)
	db  3, CATERPIE
	db  4, CATERPIE
ENDC
```

`make red`, `make blue`, `make all`. **Rename the two defines to `_CONTENT` and `_CONTEXT` and the two-edition release is done.** There is no new engineering here at all — the hard part was solved in 1996 by people who needed you to buy two cartridges.

**CONTENT is the primary target** (`_RED`'s slot), because content is the literal layer — and because it is quietly funny that the content-first edition is the default build.

#### Three tiers of divergence

**Tier 1 — encounter tables.** Free, standard, exactly the Route 2 pattern above. Note what it does *not* cost: **zero extra sprites.** Every daemon exists in both ROMs. Each edition simply cannot *bind* some of them, so the 8.3 bottleneck does not move at all.

**Tier 2 — let the rosters lean.** Do not split the exclusives at random. Bias them:

| Edition | Sees more of, early | Reads as |
|---|---|---|
| **CONTENT** | CONTENT · LOGIC · STRATUM · LEGACY | the literal, the rule-based, the physical layer |
| **CONTEXT** | CONTEXT · LATENT · VECTOR · ENTROPY | framing, the unconscious, embeddings, noise |

The consequence is the good part. **The two editions are hard in different places.** A CONTENT player finds the early benchmarks straightforward and Benchmark 6 — attention and framing, in the bought city — genuinely punishing. A CONTEXT player struggles early and walks Benchmark 6, which is exactly how 8.2 says the learning paradigms should feel: unsupervised is confusing early and excellent late.

So **each edition's player builds a different intuition about what is strong** — and when they compare notes, they disagree, sincerely, with evidence. That is the thesis arriving as a *distribution* mechanic, and nobody has to say a word.

**Tier 3 — the Index entries disagree.** This is the prize.

Same daemon. Two editions. Two different entries, both stated as fact, neither acknowledging that the other exists.

The trap to avoid: do **not** make CONTENT's Index measure content and CONTEXT's measure context. That collapses 4.2's irony into a joke. **Both editions' Index measures only content — and they disagree anyway.** Different heights. Different weights. Different flat descriptive sentences about the same creature.

Two players compare entries and find the record does not match. Nobody explains it, ever. **The Index is a reproduction, and two reproductions of the same thing differ** — which is 0.2's whole printing throughline, and the Five Witnesses at the scale of the cartridge.

*Restraint required.* Do this for a handful of daemons, not all of them — enough that a player who compares finds it, few enough that it reads as unsettling rather than as a gimmick. And **never for the starter**, whose entry has a different job (11.1 in `lineage.md`: it rewrites itself once, late).

Cost: dex text is text. `IF DEF(_CONTENT)` around the entries. No engine work.

#### Trading is the structural argument

Gen 1 link trading is already in the engine, and edition-exclusive daemons mean **you cannot complete the Index alone.**

The artifact that measures only content cannot be completed without another person's playthrough. You need someone else's context, literally, over a cable.

That is the best structural argument this project has available and it costs an encounter-table split.

#### Done, 2026-08-29 — partially

**The visible half is in.** `make content` and `make context` build
`daemonsContent.gbc` and `daemonsContext.gbc`, with cart titles `CONTENT` and
`CONTEXT`. Saves follow the ROM name, so the two editions keep separate
playthroughs automatically.

**The defines are not renamed.** `_RED` and `_BLUE` are used by `IF DEF(...)`
blocks in **47 asm files**, so swapping them to `_CONTENT`/`_CONTEXT` is a
sweep, not an edit — and it would be a large permanent diff against upstream
while we still want `git pull upstream master`. Deferred until the tree has
diverged enough that upstream merges stop mattering.

Nothing depends on it. The defines are internal; the player never sees them.

#### Scope: build the flag now, use it later

Section 8 is unambiguous that the vertical slice comes first, and two editions is a step-14 item at the earliest. **But the flag is not.**

> **Set up both targets on day one, even if the two ROMs are byte-identical for a year.**

Adding a version define at the start costs nothing — the tree already has one. Retrofitting one *after* 151 dex entries and sixty encounter tables exist is a miserable afternoon. Keep `make content` and `make context` in the Makefile from the first commit and let them produce identical ROMs until they do not.

#### What must never differ

**The type chart is byte-identical across both editions.** It is the argument, and an argument that changes by cartridge is not an argument. Same maps, same benchmarks, same story, same lexicon, same music.

The editions differ in **what you meet** and **what the record says about it.** Nothing else.

#### Title screens — as built

*Implemented 2026-08-29.* The subtitle reads **Content Edition** / **Context Edition**, matching vanilla's *Red Version* pattern.

**The version subtitle is not a blitted image, and that matters.** The graphic is loaded into VRAM as tiles, and then a string of *tile indices* is printed:

```asm
db $60,$61,$7F,$65,$66,$67,$68,$69,"@"   ; vanilla "Red Version"
```

Tiles 0, 1, a blank, then 5–9 — **tiles 2, 3 and 4 are never displayed.** Vanilla did this because "Red" and "Blue" are different lengths and the two versions share one VRAM window, right-aligned by a size calculation at load time.

A first attempt at this rename put the word in tiles 0–4 and rendered as **"Con"**.

**Our fix simplifies it.** Both editions ship the same 10-tile canvas, so both load at `$60` and both print the full contiguous run — no per-edition string, no skipped tiles, no `IF DEF` at all:

```asm
db $60,$61,$62,$63,$64,$65,$66,$67,$68,$69,"@"
```

*Built to spec, not generated.* Clean `e`, `o`, `n`, `i`, `d` letterforms were extracted from the vanilla graphic; `C`, `E`, `t`, `x` were drawn to match its 2px stems; the words were composited centred in an 80×8 canvas and written as **1-bit greyscale PNGs**. No image model produces that format — `rgbgfx --colors dmg` rejects anything with anti-aliasing or a colour outside the palette.

#### The splash line — and why it changed

`GAME FREAK inc.` is now **CODEMUSIC**, and the year is gone.

**This is more honest, not less.** The vanilla line asserts that Game Freak made this build. They did not. Leaving it would be a false attribution on modified work, and replacing it with a CodeMusic copyright *and a year* would assert a claim over an engine that is pret's disassembly of Nintendo's game.

So the line shows the wordmark and nothing else. **Trademark acknowledgment stays in `README.md`**, where it belongs and where it is unambiguous.

*How it was assembled.* The vanilla line is 16 tile indices — year tiles `$41`–`$45` (shared with the boot splash) plus a 9-tile wordmark at `$46`–`$4E`:

```asm
db $41,$42,$43,$42,$44,$42,$45,$46,$47,$48,$49,$4A,$4B,$4C,$4D,$4E
```

`gamefreak_inc.png` is 72×8, 2bpp, exactly those 9 tiles — so CODEMUSIC is a direct swap with no VRAM changes. The string now prints `$46`–`$4E` only, recentred at column 6.

*Deferred:* a year would be lovely — **'11.'26** encodes the whole lineage, and vanilla's own multi-year format invites it. But the digits need glyphs that do not exist in the current tile set, and the year tiles are shared with the boot splash. It wants a slightly wider wordmark graphic, which is 8.5 work.

**The Super Game Boy border, done.** `red_border` / `blue_border` are now `content_border` / `context_border`, and they no longer read RED and BLUE.

**And it is harder than it looks.** A border file is not a picture of a border. It is **128×48 — a bank of 96 unique 8×8 tiles** — plus a separate `.tilemap` of 896 `(tile, attribute)` pairs arranging them across the 256×224 frame, plus SGB palette entries that colour the 2bpp greys at runtime. Four facts had to be measured against vanilla rather than assumed:

- **`rgbgfx` inverts greyscale.** PNG level 3 becomes colour index 0. So in the source PNG *higher value is lighter on screen*, and level 3 is the light ground.
- **The attribute byte carries the palette:** `(attr >> 2) & 7`. Vanilla uses palettes 4/5/6 (`PAL_SGB1`–`3`) and `$40` for X-flip. Ours uses palette 4 throughout, so every border entry is `$10`.
- **Tile `$00` is reserved and flat.** The centre 160×144 is covered by the Game Boy screen; vanilla fills it with tile `$00`, attribute `$00`.
- **Colour index 0 is not transparent here.** Vanilla's art uses it as the *lightest* value, not as a hole.

**They are generated, not drawn.** [`tools/genborder.py`](../tools/genborder.py) builds each border from a repeating cell. This was not the first plan — three illustrated versions were commissioned and measured with [`tools/mkborder.py`](../tools/mkborder.py), which takes a 256×224 design, quantises, deduplicates and reports the tile count. They came in at **496 and 523 unique tiles against a budget of 96**. The lesson is that a halftone frame is *geometry, not illustration*: generated from a cell it lands every dot on the grid, and both editions now cost **12 tiles**. `mkborder.py` remains the measuring tool for any supplied art.

**And the two borders argue the same thing the editions do:**

- **CONTENT** — one dot grid. The thing itself, repeating, self-identical. Dots shrink toward the screen, so the image resolves as you approach it.
- **CONTEXT** — the *same* cell, laid over itself at an offset. Nothing new is drawn; the pattern is entirely the relationship between the two. True moiré is definitionally non-repeating and therefore cannot be tiled at all — so this is a repeating unit that *reads* as interference. That constraint is not a compromise; it is the argument in miniature.

#### Which daemon appears

Vanilla puts a starter on the title — Charizard on Red, Blastoise on Blue, and Venusaur on neither. So:

- **CONTENT edition:** the Supervised line (CONTENT → CONTENT/LOGIC)
- **CONTEXT edition:** the Unsupervised line (VECTOR → VECTOR/LATENT)
- Reinforcement appears on neither title, exactly as Venusaur does not

---

### 8.5 Not yet — sprites, and the recomp question

Two ambitions worth recording so they are not lost, and **deliberately not designed.** Both sit after the vertical slice. Neither is a commitment.

**Original sprites.** 8.3 already names this as the bottleneck. Nothing to add except that it stays a bottleneck no matter which of the below happens. *Prompts and specs for the first pass now live in [`sprite-prompts.md`](sprite-prompts.md).*

**How far the foxes spread — decided 2026-08-29.** 4.1 makes Crystal a fox and 4.3 makes the resemblance an inference beat. The open question was whether *everyone* is animal-like.

**They are not, and the reason is resolution rather than lore.** At 16×16 a character has about three pixels of head, so the entire animal vocabulary is **ears, a tail, and a shade** — the bible says as much already. Making the whole cast anthropomorphic costs something like a hundred sprite sets and buys almost nothing, because at that size a badger and a bear are the same eight pixels. So: **the Clears get ears, tail and value; nobody else changes; and the game never says anyone is a fox.** It reads as family resemblance rather than as a species claim, which is exactly the job 4.3 gives it.

*The failure mode, and the cheap escape.* If three tailed characters among an untailed cast reads as *otherness* rather than *lineage*, the fix is not to convert everyone — it is to give light animal features to a handful of **recurring** characters (Scorn, two or three Benchmark leaders) so that fox becomes one species among several. Eight sprites, not a hundred. Decide it on playtest, not now.

*And the resemblance is carried by value, not hue.* 8.6 means the player sees four greys, so *golden-amber*, *darker* and *between* have to be **light-to-mid, dark, and between** — with identical ear and muzzle geometry doing the family work. Colour words will not survive the conversion and should never be relied on in a prompt.

**The Gen1Recomp question.** [Gen1Recomp](https://gen1recomp.com/) is a hand-written Lua / LÖVE2D recreation of Gen 1 that **imports data and graphics from a player-supplied ROM** rather than emulating it. Its [mod ecosystem](https://gamebanana.com/games/25428) includes the **voxel mod** and first-person renderers — which is the specific pairing of interest here: DAEMONS creatures, rendered as voxels, in a first-person Kanto.

That split — **imported data, hand-written behaviour** — is the whole of the analysis, and it cuts cleanly:

| | Likely carries | Almost certainly does not |
|---|---|---|
| What | Sprites, base stats, names, type constants and matchups, Index entries — anything decoded out of ROM tables | Story scripts, custom events, engine work (RECURSION), anything that lives in `asm` rather than in data |

So the optimistic case is a DAEMONS ROM loading in a 3D shell with the right creatures and the right combat philosophy, and the pessimistic case is that the loader rejects a non-canonical ROM outright — the project documents accepting *"the canonical 1 MiB US versions,"* which implies it may check.

**The one test worth running, whenever the mood strikes:** build the step-5 milestone (vanilla everything, new type chart) and drop it in the launcher. It costs an afternoon and it answers the entire question — either it loads or it does not. Do that before designing anything around it, and before assuming either outcome.

**A note on the voxel mod specifically.** A voxel renderer builds volume out of the 2bpp sprite data — so the sprite work in 8.3 would be doing double duty, and the four-shade constraint that makes Game Boy spritework hard is exactly what a voxel mod needs to read cleanly. That is a reason to design the sprites well rather than a reason to design them differently.

**Scope note.** This is a *rendering* ambition, not a design one. Nothing in sections 0 through 7 should bend to accommodate it. If it works it is a gift; if it does not, the game was always a Game Boy game.

---

### 8.6 The monochrome question

**The game is about colour and cannot show any.** Every city is a colour word rendered in four shades of grey. That is either a limitation to be fixed or the best thing the hardware gives us, and the answer decides whether colorization is an upgrade or an act of vandalism.

**It is the second one.** Three reasons, in ascending order of how much they cost to lose.

**1. The player is told these places are colours and shown grey.** They supply the rest. That is the 8-Bit World thought experiment — a system whose perception is bounded by its resolution — running for free, on the hardware the thought experiment names, without a line of dialogue. And it is *The Colour We Never See*: purple is not on the spectrum, the mind folds the line into a loop and invents it. The town colours are not on the screen. The player invents them.

**2. The Index is a reproduction that loses the original** (0.2). A greyscale record of a world named in colour loses something specific, visible, and unrecoverable — which is exactly what 4.2 needs the Index to be doing.

**3. Colorizing Halftone destroys Halftone.** The town's entire premise is *dots that only look like grey* — continuous tone that is actually discrete black and white sampling, where the bias comes from **resolution, not malice** (3.1). In colour, halftone stops being the town's condition and becomes a quaint printing reference. **This is not a cost to weigh. It is a load-bearing wall.**

#### Recommended: colour as something the world spends

Not "monochrome forever" and not full colorization. **Greyscale by default, and colour appears exactly once, where it means something.**

> **The Review Board at Umbra is the only place in the game that has colour.**

Section 6 already sets it up: two thousand years ago emotions were *literally coloured fluids*, and the four humors arrive as a classical flourish that becomes the whole thesis about six seconds later. Give them their colours — sanguine red, choleric yellow, melancholic black, phlegmatic white — and give them to nobody else.

Forty hours of colour-named grey towns, and then one room where colour is real, occupied by four ancient people insisting that emotions are coloured fluids. Who are **wrong**, and lose, and are followed immediately by Ty, who is also wrong and also loses.

**The one place the game admits colour is the place with the obsolete answer.** Nobody remarks on it. Nobody can.

#### Settled: two sources, one of them earned

The open question — *is one colour moment right?* — resolves at **two, different in kind.**

| | What colour is | Who sees it |
|---|---|---|
| **Umbra** | an obsolete answer, held still and examined | everyone who finishes |
| **PERSPECTIVE** | a glimpse of another's frame, immediately lost | most players, via MOCK |

**MOCK settles it.** 4.6 establishes that Ditto is CONTENT/CONTENT and learns PERSPECTIVE, so the flash is reachable in ordinary play rather than gated behind a puzzle almost nobody solves.

**BunnyArtsai is not a third source.** She is the most loaded firing of the first — the same few frames, from the one creature that could not come back — and only for a player who solved the Five Witnesses (4.8).

*Why this is the right pair.* Vanilla had **no designed way to reach Mew at all** — verified: it appears in no wild encounter table, only in `names.asm` and `palettes.asm`. The famous routes were an unintended glitch and event distribution, and player culture filled the vacuum with rumour. **If colour lived only with BunnyArtsai it would be a secret nobody could confirm.** MOCK makes it something players can compare notes about, which is the condition under which Umbra lands rather than passing unnoticed.

*Restraint clause holds at two.* A third source makes it a system, and a system invites explanation.

#### Notes and consequences

- **Technically this is easier than full colorization, not harder.** A colour build has to palette every map; this one palettes a single map and leaves the rest on a greyscale ramp.
- **On the GBC caveat:** Gen 1 already receives limited hardware palettes on a Game Boy Color, so "monochrome" is a slight fiction in practice. The design intent stands regardless — the ramp should read as value, not hue, everywhere but Umbra.
- **The humors survive greyscale anyway.** Value carries them: melancholic dark, phlegmatic pale, sanguine and choleric mid. The colour at Umbra is a confirmation of something the player has already been reading in tone, which is the correct order.
- **This serves the sprite work rather than fighting it** (8.3, 8.5). Four shades with no hue to lean on forces value contrast to be right, and value contrast is exactly what a voxel renderer needs to read cleanly.
- **The recomp path is a remix, not the canon.** If a 3D or voxel presentation colours everything, that is a different presentation of the same ROM and it is welcome. The canonical build stays grey.

---

## 9. IMPLEMENTATION

`pokered` is RGBDS assembly. The *data* lives in readable macro tables. Engine features are where it gets expensive.

> Paths are approximate. Verify against your checkout — they drift between commits.

| What | Where | Effort |
|---|---|---|
| Type IDs | `constants/type_constants.asm` | trivial |
| Type names | `data/types/names.asm` | trivial, but see 9.1 |
| **Type chart** | `data/types/type_matchups.asm` | trivial, highest leverage |
| Species stats | `data/pokemon/base_stats/*.asm` | bulk, scriptable |
| Species names | `data/pokemon/names.asm` | bulk |
| Index entries | `data/pokemon/dex_entries.asm` plus `text/` | bulk |
| Moves | `data/moves/moves.asm`, `data/moves/names.asm` | medium |
| PERSPECTIVE | rename TRANSFORM | trivial |
| RECURSION | repurpose Bide/Rage machinery | **engine work** |
| Sprites | `gfx/pokemon/front/`, `gfx/pokemon/back/` | **the bottleneck** |
| Map names | `data/maps/names.asm`, `constants/map_constants.asm` | trivial |
| Map layouts | `maps/*.blk`, `data/maps/headers/`, `data/maps/objects/` | medium |
| Dialogue, signs, witnesses | `text/` | bulk |
| BIND verb and the flat message | `text/` — catch strings; also `data/` menu labels | trivial |
| Greyscale ramp everywhere but Umbra | palette data; one map differs | medium, specialist |
| Two-edition build | `Makefile` — rename `_RED`/`_BLUE` to `_CONTENT`/`_CONTEXT` | **trivial, do it first** |
| Edition-exclusive encounters | `data/wild/maps/*.asm`, `IF DEF(_CONTENT)` blocks | trivial |
| Divergent Index entries | `data/pokemon/dex_entries.asm` plus `text/`, conditional | trivial, high value |
| ORPHAN as a species in a free index slot | `constants/pokemon_constants.asm`, base stats, sprite, cry | one daemon's work |
| ORPHAN's blank Index entry | `data/pokemon/dex_entries.asm` — a pointer that goes nowhere | trivial, needs care |
| SILPH SCOPE → RESOLVER | `data/items/names.asm` plus `text/` | trivial |
| Hidden BunnyArtsai tile | hidden object plus event flag | trivial |
| Quicksilver terminal log | one text block | trivial |
| Corpus lobby engraving | one sign-text object, Brazen | trivial |
| Quicksilver asset tags at Halftone | one sign-text object | trivial |
| `AL CLEAR` in formal text; naming screen untouched | `text/` — literal string instead of the `<RIVAL>` control char | trivial |
| Default name lists, both editions | `constants/player_constants.asm` | **done 2026-08-29** |
| PROF.OAK → CRYSTAL | `text/` — 33 occurrences in 10 files, plus the intro sequence. Every line needs rewrapping | half a day |
| Quicksilver journal fragments, one signed | `text/`, Cinnabar Mansion idiom | trivial |
| Corpus badge name matching the signature | `text/` | trivial |
| Brazen employee's post-Quicksilver second line | one event flag, one text block | trivial |
| Music | `audio/music/*.asm` | medium, specialist |

### 9.1 The `TypeNames` gotcha — **resolved, and smaller than feared**

*Verified against `pret/pokered` master, 2026-08-28. Built and confirmed.*

The warning in earlier drafts was right in spirit and wrong in detail, and the detail matters because it makes step 5 **much** cheaper than the bible previously claimed.

**Current master does not need a subtraction.** `data/types/names.asm` is a flat table guarded by `table_width 2` and `assert_table_length NUM_TYPES`, and the ID gap is filled explicitly:

```asm
REPT UNUSED_TYPES_END - UNUSED_TYPES
	dw .Normal
ENDR
```

So every unused ID points at `.Normal` and `GetTypeName` indexes straight in. There is no `$0B` fold in this checkout. **Never paste a replacement `names.asm` wholesale** — that advice stands, harder than before, because the structure here is nothing like the standalone file in `patches/`.

**The bigger correction: you do not need to rename the constants at all.**

The chart references types by symbol; the symbols resolve to IDs; the IDs drive the matchup lookup. **None of that touches what the player reads.** What the player reads is the strings in `names.asm`. So a complete step-5 build is:

1. Change **only the strings** in `data/types/names.asm` — `db "NORMAL@"` becomes `db "CONTENT@"`, and so on for fifteen
2. Apply the two matchup deltas

Renaming `NORMAL` to `CONTENT` in `constants/type_constants.asm` is a **readability change for the developer**, not a gameplay change — and it is the expensive one, because every type constant is referenced across `moves.asm`, `base_stats/`, and elsewhere, and several collide with unrelated symbols (`ROCK` with `ROCK_SLIDE`, `FIRE` with `FIRE_BLAST`, `BUG` with the Bug Catcher trainer class). Do it later, deliberately, with word boundaries, or never.

**Three literals the earlier notes got wrong**, all confirmed by build:

| Earlier note | Actual |
|---|---|
| `PSYCHIC` | **`PSYCHIC_TYPE`** |
| `db GHOST, PSYCHIC, 00` | `db GHOST,        PSYCHIC_TYPE, NO_EFFECT` |
| numeric `20` / `05` / `00` | named `SUPER_EFFECTIVE` / `NOT_VERY_EFFECTIVE` / `NO_EFFECT` |

**`constants/type_constants.asm` also cannot be pasted wholesale.** Master wraps the list in `DEF PHYSICAL`, `DEF UNUSED_TYPES` / `UNUSED_TYPES_END`, `DEF SPECIAL` and `DEF NUM_TYPES`, and `names.asm` depends on three of those symbols. The standalone file in `patches/` defines none of them and would break the build immediately.

The 8/7 physical–special split is intact and is exactly where 2.1 says it is: `const_next 20` (decimal, = `$14`).

### 9.2 Order of operations

1. Toolchain and a **vanilla matching build**. If the checksum matches, your toolchain is sound and every later break is yours.
2. Replace `constants/type_constants.asm`.
3. Replace the strings in `data/types/names.asm` — structure untouched, per 9.1.
4. Apply the three-line patch to `data/types/type_matchups.asm`.
5. `make`. **Stop here and play.**
6. Add CONSENSUS to `moves.asm` and `data/moves/names.asm`. **Done** — and to `move_constants.asm`, `animations.asm` and `sfx.asm`, which the length asserts require (2.5).
7. Rename TRANSFORM to PERSPECTIVE. **Done** — the move name and its battle message (*took the frame of*). MOCK's Index entry still says TRANSFORM and is left for 9 (4.6).
8. City and route renames plus sign text — fast, and it transforms the feel immediately.
9. Starter trio: stats, sprites, moves.
10. Crystal Clear intro script.
11. The Bleed and Undertone encounter tables plus nine wild daemons.
12. Benchmark 1 at Slate.
13. Two city themes and one modulation.
14. **Play it. Decide if it is fun.**

**Step 5 is the real milestone.** Vanilla sprites, vanilla maps, vanilla everything, running your combat philosophy underneath. It will look like Pokémon Red and fight like Context/Content. A couple of hours' work for the fastest possible read on whether the type system is *fun*, before a single pixel is drawn.

Defer RECURSION past the slice. S.T.A.R.R. appears after the Review Board; you will not reach that content for months, and Bide surgery in assembly is a bad first engine task.

---

## 10. DECISION LOG

### Settled

- Base: `pokered`, Gen 1, RGBDS assembly
- Fifteen types as listed; CONTEXT is Special; STRATUM replaces SUBSTRATE for string length
- Creatures are DAEMONS; full lexicon per section 1
- **MOCK** (Ditto) is CONTENT/CONTENT and also learns PERSPECTIVE — the capability was always in the wild; Quicksilver only noticed it (4.6)
- **ORPHAN** at Halftone Tower — CORRUPT/LATENT, the one daemon with a genuinely blank Index entry; an orphaned process is how a daemon is made (4.5)
- **Silph Scope → RESOLVER** — it exists because the Index is insufficient (1, 4.5)
- **Species renamed: POKéMON → DAEMON / DAEMONS**, by repointing one string (`PlacePOKeText`), so 650 occurrences moved for free (1.2)
- The Pokédex text token becomes literal **INDEX**; item prefixes become literal `POKé` pending their own renames (1.2)
- **Catching is BINDING** — `bind()` and *binding a daimon*; the flat, uncongratulatory message register goes with it (1.1)
- **The foxes stop at the Clears** — ears, tail and *value*, nobody else converted; the cast stays as it is because at 16×16 the animal vocabulary is three pixels wide and a full conversion costs ~100 sprite sets for almost no signal (8.5)
- **`EnemyText` was the third `Enemy`** — the prefix behind every `<USER>`/`<TARGET>`, missed by the first REMOTE pass. Now `Remote @`, which **caps species names at 9 characters** (1.4)
- **The text ceiling is 18, not 19** — the earlier figure counted `<COLON>` as seven characters. Vanilla's four 19-char lines overwrite the right border (1.2)
- **INVOKED rejected on measurement, not taste** — 21 as the verb, 6 in a 5-char menu slot (1.4)
- **Currency is CACHE** — a hoard, a memory cache, and *cash*, all at once; the word is almost never on screen, so this is one prose line and a naming decision. **¥ kept**, logged as optional art (1.4)
- **The battle menu still says FIGHT and RUN** — a live collision in the most-seen string in the game. Not a text edit: the right column is 3 characters, so DETACH cannot fit, and moving the split is `wTopMenuItemX` surgery at four sites (1.4)
- **Kept: `used`** (1.4 made *use* morally loaded on purpose; INVOKED measured at 20 chars, over the ceiling) **and `ATTACK`** as a stat (1.4)
- **`enemy` → `REMOTE`** — nothing here is anyone's enemy; a REMOTE is a process you have no handle on, and it pairs with DETACH. `Enemy X ran!` → **`Remote X DETACHED.`**, killing a live `ran` collision (1.4)
- **`defeated` → `outscored`** — a BENCHMARK yields a score; *outran* rejected for reaching back at RUN (1.4)
- **Kept after interrogation: `RUN,` (comma), `EXP`, `LEVEL`** — EXP because 4.3's whole argument is that context forms from *experience*; LEVEL because it already means *permission level* and `<LV>` is a single tile (1.4)
- **Crystal is female and the text had not caught up** — `Gramps` → **`Gran`** (she is Al's grandmother, 4.3), `His order` → `Her order`, and Agatha's block repronouned. **`handsome` deliberately kept** — it is attested for women and keeps Crystal tough rather than pretty (4.3)
- **Starter dialogue named vanilla types** — *fire/water/plant* → **ENTROPY/FLOW/GROWTH**; 19 more remain in gyms, held for 5 (1.2)
- **Crystal's opening speech**: six `#MON` marked plural; **pets → companions** (1.5's animal-word test), **fights → BENCHMARK**. *assistants* considered and held in reserve — it collapses vanilla's contrast (1.4)
- **PERSPECTIVE built** — move `$90`, and the battle message becomes *`<USER>` took the frame of `<NAME>`!*; **Index categories are capped at 10 characters**, so MOCK's cannot be PERSPECTIVE (4.6)
- **CONSENSUS built** — move `$A5`, SWARM, 90/100/15, no secondary effect; inserted before STRUGGLE because `NUM_ATTACKS == STRUGGLE` is asserted. Not yet learnable by anything (2.5)
- **SGB borders generated, not drawn** (`tools/genborder.py`) — CONTENT is one dot grid, CONTEXT is the same cell interfering with itself; 12 tiles each against a 96 budget (8.4)
- City names per 3.1; Slate over Somber; Halftone over Pallor; Quicksilver over Cinder; **Brazen over Gilt**
- Doldrum and The Bleed interrogated and kept, with the reasoning recorded (3.1, 3.2)
- Routes keep numbers officially and carry local names on signs
- Crystal Clear as the Oak figure; the Index measures only content, deliberately
- **Al Clear** as rival and incumbent — Crystal's **grandson**, Ty's son. Vanilla's rival is Oak's grandson, and Ty is far too old to race you (4.3)
- Default name lists per edition: slot 1 fixed, slot 2 swapped, slot 3 differentiated (4.3)
- **Ty P. Clear** is the generation between: Scorn's partner before the rebrand, then the one who went back. He is at Quicksilver, and he explains nothing (4.3)
- **Context does not transmit; only content does.** Ty taught Al the method and none of the experience — the Index problem inside a family (4.3)
- The family is named for three kinds of clarity and none of them can see (4.3)
- Richard Scorn at Benchmark 8, Alignment, sympathetic throughout; the Goodhart engraving in the Corpus lobby, unattributed and adopted approvingly (4.4)
- BunnyArtsai as Mew with PERSPECTIVE — the first realization of perspective thinking, not a template (4.6)
- S.T.A.R.R. as Mewtwo with RECURSION — a **comprehension, not a clone** (4.7)
- The content/context feedback loop is the mechanism under the thesis and is never named in dialogue (0.3, 4.9)
- Five Witnesses easter egg, locked at 35 steps; the number lives only in the Quicksilver terminal log (4.8)
- **Ty Clear's parentage is never stated.** Inferred from the surname, confirmed late by one line at Brazen (4.3)
- **The rival naming prompt stays.** The player names him; **CLEAR** is hard-coded, and formal text carries TY CLEAR — the route-sign device applied to a person (4.3, 9)
- Crystal is CRYSTAL CLEAR in full wherever the game refers to her formally, or the surname device dies (4.3)
- **Corpus is downstream of Quicksilver by succession** — Scorn took over the lab, the metric changed, it burned, the people came with him (4.10)
- Crystal was at Quicksilver and built S.T.A.R.R. there; a fitness-for-work procedure removed her, and **the Index is what she did next** (4.1, 4.10)
- Scorn arrived afterwards to run it, signed a complete file about a person he never met, and set the temperature (4.4)
- Ty **stayed** when his mother was removed; his guilt is an absence of decision, not a betrayal (4.3)
- **No date on the fire; dates on everything around it.** The player reconstructs the order or does not (4.10)
- **Brazen confirmed over Brass.** Brass is a colour and not a feeling, and would be the only single-meaning name on the map (3.1)
- At least one survivor knew what they were trading and did it anyway, for an ordinary reason — the guard against determinism (4.10)
- Craft rule 6: comedy is the cover. Corpus is funny; Quicksilver is fun to explore (0.1, 4.10)
- Four humors as the Review Board
- Vertical slice before anything else
- **Greyscale is the design, not a limitation.** Colour appears once, at the Review Board, and nowhere else (8.6)
- **Two editions, CONTENT and CONTEXT, from one source tree** — the slash in the title is literal (8.4)
- The **type chart is byte-identical** across editions; only encounters and a handful of Index entries differ (8.4)
- The two-target build goes in on day one even while both ROMs are identical (8.4)

### Reversed

Kept here because the reasoning is worth more than the outcome.

| Was | Now | Why |
|---|---|---|
| **Gilt City** | **Brazen City** | Gilt implies a concealer, and this story has no schemer. Brass is honestly itself; so is Scorn. Full argument in 3.1. |
| **BunnyArtsai35** | **BunnyArtsai** | The number in her name gave away the Five Witnesses lock and made a serial of a one-off. Relocated to a single lab log (4.6, 4.8). |
| **Ty**, an unrelated rival | **Ty Clear**, Crystal's son and Scorn's partner | Turns a methodological disagreement into a cost somebody pays (4.3). |
| S.T.A.R.R. as *refined successor* to the BunnyArtsai line | S.T.A.R.R. as a built understanding | "Successor" still smelled of cloning. The lab understood recursion and instantiated it (4.7). |
| **CATCH** | **BIND** | The container was renamed and the verb was not. CATCH is the only lexicon entry doing no double duty; BIND is `bind()`, *binding a daimon*, and a bond — and it is darker rather than softer, so the player stays implicated (1.1). |
| Drop the rival naming prompt, hard-code "Ty Clear" | Keep the prompt, hard-code **CLEAR** | The surname is the half that carries the inference. Spending a famous vanilla beat bought nothing — and the prompt, reframed as *what will you call him*, becomes the route-sign device a minute before Route 1 teaches it (4.3). |

### Open

- Does Halftone hold once the tower is written, or do Penumbra / Moiré serve better?
- Does the player meet Scorn before Halftone Tower?
- Does RECURSION justify engine work in the slice, or defer?
- How legible is S.T.A.R.R.'s SHC backstory to a player who has not heard the rock opera — and does it need to be?
- Are the humors too neat? Four is convenient; the real theory had temperaments blending.
- Does **Al** get a redemption, a plateau, or neither — and does the family tie make redemption too cheap?
- Ty is absent from the endgame by design. Does that read as a statement or as a loose thread?
- Is the Quicksilver terminal missable enough to soft-lock the Five Witnesses puzzle, and is that acceptable?
- Does Brazen ever read as the game *sneering* at Scorn? If playtesters hear that, swap to Brass immediately — the whole point of him is that the game does not sneer.
- Starter daemon names are placeholders and need a pass.
- Should ORPHAN be bindable at all, or only witnessed? *Lean: bindable — a blank entry sitting in your own collection is worth more than a blank entry you only heard about.*
- Nineteen `type word + DAEMON` dialogue lines still name vanilla types, nearly all in gyms — held until 5 settles the Benchmark leaders (1.2)
- Forty-two `fight` occurrences want a human read; some are the replaced verb, some are people (1.2)
- Roughly 154 `#MON` occurrences read singular by default and want a human read at step 8 — on screen, not in the source (1.2)
- Does a non-canonical ROM load in Gen1Recomp at all? One afternoon answers it; do not design around either answer first (8.5)
- How many Index entries should disagree between editions — five? twelve? — before it stops being unsettling and starts being a gimmick? (8.4)
- Is edition-exclusivity fair when link trading needs two people, two carts and a cable, and most players will have one? *Lean: yes — the Index was never going to be completable, and 4.2 says so.*
