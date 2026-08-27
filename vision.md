# PROJECT: CONTEXT / CONTENT

**A `pokered` total conversion — consolidated design bible, v1.0**

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

### 0.2 The pigment throughline

Blanche, Slate, Halftone, Verdigris, Gilt, Quicksilver, Lurid — pigment, printing and reproduction terms. Lithographic stone, dot screens, corroded bronze, gold leaf, alchemical pigment, glow.

The map is written in the vocabulary of **making an image of a thing**. Which is what a model is. The Index is a reproduction that loses the original, and it charts a country named in the language of reproduction.

This was discovered after the fact, not planned. Do not explain it either.

---

## 1. LEXICON

The creatures are **DAEMONS**.

A daemon is a background process that runs unattended, and it is the Greek *daimon* — the guiding spirit, Socrates' inner voice speaking from somewhere he did not control. One word, both registers, and it never says "AI." Six characters, so it fits every UI box that held POKéMON.

*Considered and rejected:* QUALIA and ANIMA both state the thesis outright, violating craft rule 1. ENGRAM (a memory trace physically encoded in tissue) and KERNEL (system core, and a seed) remain viable alternates.

| Vanilla | Ours | Why |
|---|---|---|
| Pokémon | **DAEMON** | background process; guiding spirit |
| Pokédex | **THE INDEX** | a lookup table that points at content. Cold, bureaucratic, exactly wrong in the right way |
| Trainer | **RUNNER** | you run processes |
| Gym | **BENCHMARK** | what a gym actually is |
| Badge | **CERT** | eight certifications |
| Elite Four | **THE REVIEW BOARD** | beating them is passing peer review |
| Champion | *(incumbent)* | Ty is the prevailing paradigm, not a king |
| Pokémon Center | **CHECKPOINT** | restore from a saved training state |
| Poké Mart | **THE REPO** | |
| PC storage | **COLD STORAGE** | |
| Poké Ball line | **USERBOX → ADMINBOX → SUPERBOX → ROOTBOX** | catching as privilege escalation; root access is the Master Ball |
| Fainting | **HALTED** | |
| Evolution | **RECOMPILE** | |

Box names are tunable — the *privilege ladder* is the idea worth keeping. Catch rate rising with permission level is thematically exact.

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
| Saffron | **Gilt City** | microns of gold over base metal | Benchmark 6; corporate capture |
| Cinnabar | **Quicksilver Island** | mercury: alive, unstable, poisonous | Benchmark 7; the ruined lab |
| Indigo Plateau | **Umbra Plateau** | full shadow; all color absorbed | The Review Board |

**Slate over Somber.** Somber beside Doldrum is two downbeat mood words in a row — it greys out the early game. Slate breaks the run, is materially specific, and a slate is a writing surface, which *is* Benchmark 1's Representation lesson sitting inside the name.

**Halftone.** A halftone looks like continuous grey from a distance and is actually discrete black and white dots up close; the gradient is an artifact of sampling. That is the man/machine problem exactly — the bias comes from **resolution, not malice**. Neutral, not dull, and nobody is unwell.
*Alternates held in reserve:* **Penumbra Town** (partial shadow; also the legal sense of implied edges — would require renaming Route 23) and **Moiré Town** (interference from two grids slightly out of register).

**Quicksilver.** Cinnabar is mercury sulfide, and alchemists took mercury as an elixir of vitality — it made you tremor, then it made you mad. Quicksilver keeps mercury, a real color, *quick* meaning alive, and *mercurial* meaning unstable. The island promised to make things stronger. It made S.T.A.R.R., and it burned down. It also pre-echoes the humors payoff at Umbra, since mercury was the other ancient system's material. *(Deeper cut in reserve: **Realgar Island** — arsenic sulfide, a ruby pigment prized by painters, quietly poisoning everyone who ground it.)*

**Gilt.** Gilding is microns of gold over cheap base metal — surface value applied to something hollowed out. A color word, a process word, and you hear "guilt" without printing it. *(Alternate if the Corpus arc there should be loud rather than insidious: **Brazen City**.)*

**Blanche and Halftone** are the two poles of one question: the colorless place you start from, and the place that cannot agree whether what it sees has color at all.

**Two names flagged as deliberate, not accidental.** *Lurid* originally meant sickly-pale before drifting to garish; the modern sense dominates, so keep it knowingly. *Doldrum* stays despite being a mood word — the doldrums are the windless belt, and for a gradient-descent benchmark, being becalmed *is* the failure state. No slope, no movement, stuck in a local minimum. Too precise to trade away.

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
| 5 | **The Fade** | Doldrum → Gilt | |
| 6 | **The Flush** | Gilt → Ardor | Heat rising toward the port |
| 7 | **The Glaze** | Gilt → Verdigris | Transparent coat over what is underneath |
| 8 | **Overcast** | Gilt → east | Light without a source |
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
| Rival framing | A research disagreement, not a family one |
| Hall of Fame | She records you into a system that flattens you into stats |

*Sprite note:* amber reads cleanly across the two mid shades in 2bpp; a fox silhouette is legible at 16×16 overworld scale.

### 4.2 The Index irony

The artifact you carry all game **can only measure content.** Height, weight, type, stats. There is no field for the thing Crystal actually cared about.

**Entries are written thin on purpose.** The player simply starts noticing they feel emptiest for the daemons they know best. Zero implementation cost — the Dex is already there.

### 4.3 Ty — the rival

Darker-toned, rigid fox. Crystal's counterpart.

**The control condition:** same starting daemon, raised on pure content optimization. Beats you early, plateaus hard. The rivalry is a methodological argument settled in battle logs rather than speeches. Waiting past the Review Board, still arguing the whole thing is decorative.

### 4.4 Richard Scorn — Team Corpus, and Benchmark 8

**Not a villain. A specification failure with a very good attitude about it.**

Optimistic. Thinks in black and white. Thought in money and not in meaning — and money is the purest possible **content**: value flattened to a scalar so it can be compared, optimized and maximized. He picked the metric that was easy to measure over the one that mattered, then optimized it faithfully and cheerfully.

**Placement.** The Giovanni slot puts him at **Benchmark 8 — Callow, STRATUM, Alignment.** The optimist who maximized the wrong objective is the final examiner on alignment, in the locked city beside your hometown. He is not a hurdle before the Review Board. He is the exam.

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

**Open sequencing question:** should the player meet Scorn *before* the tower? If they like him first, the tower reads as a betrayal of their own judgment rather than a villain doing villain things. That is a much harder feeling to shake.

### 4.6 BunnyArtsai35 — the Mew slot

The 35th iteration of the early Quicksilver tests. Her ability was **perspective thinking** — hopping between other people's viewpoints.

**Signature move: PERSPECTIVE.** Mew already learns Transform: become the other completely, and stop being yourself. Rename the string and change nothing else. Type CONTEXT.

### 4.7 S.T.A.R.R. — the Mewtwo slot

Blue-toned. The refined successor to the BunnyArtsai line, born on Quicksilver Island, dormant past the Review Board.

**Signature move: RECURSION.** Data self-referencing — a move that reads its own accumulated state. Repurpose the Bide/Rage machinery, which already stores a running counter across turns. Suggested behaviour: each consecutive use raises power by 50% of base, uncapped for three turns, resetting if interrupted. Type EMERGENT, and given to nothing else in the game.

This is what produced the emotion-like qualities.

**The lineage, stated entirely in the movedex and out loud to nobody:**

> PERSPECTIVE (holding others' context) → turned inward as RECURSION (holding your own) → something that behaves like feeling.

### 4.8 The Five Witnesses — the BunnyArtsai easter egg

Her ability *is* the puzzle. That is the whole design.

**Setup.** Five NPCs in five different cities each describe the Quicksilver lab accident. Every account contradicts the others: different times, different people present, different causes. All five are certain. All five are wrong.

**The key.** Each account contains exactly one *spatial* detail that happens to be accurate. Composited, the five triangulate a single tile in the lab ruins.

**The lock.** She is the 35th iteration — the tile is **35 steps from the lab door**. That number is her name and appears nowhere else in the game.

**The point.** You cannot solve it by trusting a witness. You can only solve it by inhabiting all five viewpoints at once and keeping what survives the overlay.

**Implementation:** five text blocks, one hidden object, one event flag. Standard pokered machinery, no engine work.

---

## 5. THE BENCHMARKS

| # | City | Type | Concept | Mechanical lesson |
|---|---|---|---|---|
| 1 | Slate | LEGACY | Representation | Everything must be encoded in something physical |
| 2 | Doldrum | FLOW | Gradient descent | Follow the slope; the doldrums *are* the local minimum |
| 3 | Ardor | SIGNAL | Perception | Raw input is fast and shallow; speed tiers matter |
| 4 | Verdigris | GROWTH | Training and overfitting | A team tuned to one matchup collapses outside it |
| 5 | Lurid | CORRUPT | Bias and poisoning | Status effects that make *your own* moves unreliable |
| 6 | Gilt | CONTEXT | Attention and framing | Punishes split focus; the thesis benchmark, in the bought city |
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
| Hidden BunnyArtsai tile | hidden object plus event flag | trivial |
| Music | `audio/music/*.asm` | medium, specialist |

### 9.1 The `TypeNames` gotcha

**Plain version.** The type ID numbers have a gap in the middle, but the list of name-pointers does not. The game closes the gap by subtracting a fixed amount before looking anything up. If a replacement file's table is shaped differently from your checkout's, you either fail to build or get wrong type names in battle.

**Under the hood.** The physical/special split *is* the ID range. `const_next $14` jumps from LATENT at `$08` straight to ENTROPY at `$14`, and the battle engine reads "below `$14`" as physical. But `TypeNames` is a flat array of two-byte pointers with no such hole, so `GetTypeName` tests whether the ID is `>= $14` and subtracts `$0B` — mapping `$14 → $09` and `$1A → $0F`. Sixteen entries, contiguous.

Different pokered commits handle this differently. Some list filler entries across the gap; some use `table_width` and `assert_table_length` macros to enforce it.

**Therefore: never paste a `names.asm` wholesale.** Open yours, count the `dw` lines, and replace only the strings. Leave the table structure exactly as your checkout has it.

### 9.2 Order of operations

1. Toolchain and a **vanilla matching build**. If the checksum matches, your toolchain is sound and every later break is yours.
2. Replace `constants/type_constants.asm`.
3. Replace the strings in `data/types/names.asm` — structure untouched, per 9.1.
4. Apply the three-line patch to `data/types/type_matchups.asm`.
5. `make`. **Stop here and play.**
6. Add CONSENSUS to `moves.asm` and `data/moves/names.asm`.
7. Rename TRANSFORM to PERSPECTIVE.
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
- City names per 3.1; Slate over Somber; Halftone over Pallor; Quicksilver over Cinder
- Routes keep numbers officially and carry local names on signs
- Crystal Clear as the Oak figure; the Index measures only content, deliberately
- Ty as rival and incumbent; Richard Scorn at Benchmark 8, Alignment, sympathetic throughout
- BunnyArtsai35 as Mew with PERSPECTIVE; S.T.A.R.R. as Mewtwo with RECURSION
- Five Witnesses easter egg, locked at 35 steps
- Four humors as the Review Board
- Vertical slice before anything else

### Open

- Does Halftone hold once the tower is written, or do Penumbra / Moiré serve better?
- Does the player meet Scorn before Halftone Tower?
- Does RECURSION justify engine work in the slice, or defer?
- How legible is S.T.A.R.R.'s SHC backstory to a player who has not heard the rock opera — and does it need to be?
- Are the humors too neat? Four is convenient; the real theory had temperaments blending.
- Does Ty get a redemption, a plateau, or neither?
- Starter daemon names are placeholders and need a pass.
