# DAEMONS — Review 2: the GBA build, and colour

*Read against vision.md as of 2026-09-06 (the pokefirered port). Same register as before: proposals that don't work twice don't get in. Engine claims below were checked against `pret/pokefirered` master today.*

---

## 0. General read of the updates

**What got better**

- **0.4 is the missing foundation and it's the right one.** *Sensation is shared; perception is not* dissolves the edition split, the type chart and the colour cartography into one 2013 sentence. It also retroactively justifies the two-Index rule — which is the sharpest structural idea in the port and was nearly thrown away by copying entries.
- **The slice audit (4.27) is the most honest thing in the document.** *9% ours* is a number nobody wanted and everybody needed. The lab, Vera's house, the Undertone and the Callow gym went from vanilla-with-our-nouns to actual rooms, and *"They are out there running. None of them is waiting for you"* is the best send-off line the project has.
- **Scorn is Giovanni, settled.** One man, one confession, one face — and the basement handoff of the RESOLVER before the tower. The arc's spine is now in the ROM rather than in the bible.
- **The two new types were read off the chart, not invented.** OPAQUE (a black box immune to perspective-taking, opened by reasoning and by collectives) and HARDENED (falls to randomness, reasoning, and whoever owns the ground) are better than "filler," and 9.3's worry is closed.
- **The bestiary discipline held.** Thirty-two names, bounded to the slice, validated against move tables. STUB → ESCALATE as *a security incident told as Magikarp* is exactly the house style.

**Three things to say plainly**

1. **The port is the thing §8 warns about, and the document knows it.** 8.6 recorded *"the bible is outrunning the slice"* as binding on 08-31; the engine moved on 09-03. The spike was a fair test and the gains (abilities, descriptions, a scripting language, friendship) are real — but "the slice is done" is now true of an engine marked *reference*. **The milestone is unchanged: Benchmark 1 beaten, on the GBA build, on hardware.** 4.27–4.31 are the right work toward it. 7.14c–g (the title screen, the face-off, the copyright glyphs, the player's arm) are not, and that's where the last week's hours went.
2. **FireRed brings the Sevii Islands, and nothing in the bible has noticed.** Seven islands, a post-game arc, a Rocket remnant plot — and 8.5 already has Scorn's fourth encounter at *Corpus Warehouse, Five Island.* This is the largest new canvas the port opened and the largest scope trap. §3 below.
3. **The colour question is being argued as art direction. It is a palette flag.** §1.

---

## 1. Colour — the engine already settled the mechanics; only the rule is open

### 1.1 What the port actually gives you (checked today)

`pokefirered` ships a **global field tint** — `gGlobalFieldTintMode` in `fieldmap.c`, with `QL_TINT_NONE / GRAYSCALE / SEPIA`, applied to every tileset and object palette as it is loaded. It exists because **FireRed's Quest Log plays back in sepia**: the game's own record of what you did is rendered without its colour. `palette.c` also carries `TintPalette_GrayScale`, `_SepiaTone` and `_CustomTone(r,g,b)`.

Three consequences, and they answer the technical half of your question outright:

- **You never draw two sprite sets.** A GBA sprite is indices; colour lives in the palette. Grey, partial grey, and full colour are the *same art* with a different 32-byte table. The PERSPECTIVE drain-to-grey (already built) is this — it always was.
- **"Grey town" is a per-map flag**, not a per-map asset. Halftone grey costs one line in its map header handling; Slate too, if you want it.
- **"Grey until X, colour after" is a save-file bit** read at palette-load. The endgame-item idea is implementable in an afternoon. Whether it *should* exist is the design question, below.

And one gift: **the Quest Log is the Index thesis, already in the engine.** A record of the player's own actions, replayed desaturated. Rename it (LOG / RECORD / *the ledger*) and let it stay sepia. Nobody explains why the record has no colour.

### 1.2 The rule — one axis, not a list of exceptions

The current lean — *colour, grey Slate, grey daemons with a type accent, more colour on final forms, a post-game item that colourises everything but Halftone* — is five decisions. The bible's own method is to find the one rule they're all instances of. Here it is:

> **Colour is context. The world has it. Records don't. A daemon has as much of it as it has accumulated.**

Applied:

| Surface | Colour | Why |
|---|---|---|
| **People, towns, overworld** | full colour | 8.6's argument 1 died with the DMG; the three foxes and Scorn's bright red are already load-bearing. Stop mourning it. |
| **The achromatic towns** | a **value ladder**, not five greys | Blanche warm white → Slate blue-grey → **Halftone true grey with a visible dot screen** → Quicksilver cold ash → Umbra near-black. 7.4 already does this for music (*hue sets key, value sets register*). Slate is *slate*-coloured — desaturated, not grey — so Halftone stays the only real grey. **Two grey towns halves Halftone.** |
| **The Index, the Quest Log, the Trainer Card** | grey / sepia, always | *a reproduction that loses the original* — now visible against a colour world (8.6's own inversion) |
| **Daemons** | type ramp + accents (9.4 as amended) — **and saturation scales with friendship** | §1.3 |
| **Umbra** | the value floor; the four humours are the only saturated things in the room | §1.4 |
| **PERSPECTIVE** | drains to grey, takes the target's palette | built; correct; *lossy* is more legible in a colour world than a flash ever was |

### 1.3 Daemon saturation = friendship. This is the thesis, made mechanical, and it costs ~20 lines

Gen 3 has friendship (`MON_DATA_FRIENDSHIP`, 0–255, set to species base on creation, raised by walking and battling with you, lowered by fainting). Vera's grooming ladder in 4.29 already reads it. **Make it drive the type ramp's saturation**: at low friendship the daemon is nearly grey with a hint of its type; at max it's the full ramp. `TintPalette_CustomTone` (or a lerp toward luminance) at sprite-palette load, keyed off the mon's friendship — one hook in the battle palette loader.

Why this and not evolution stage:

- **"More colour on the final form" says power = colour.** That's Digimon's thesis. And 8.2's final stages are *the paradigms' failures* — CANON files novelty as error, MANIFOLD can't name what it found. Making them the most colourful argues the wrong thing.
- **Friendship-saturation says context = colour**, which is the game's actual sentence, performed every battle and stated nowhere. A daemon *gains colour by accumulating experience with you* — and EXP stayed EXP for precisely this reason (1.4).
- **It answers the "am I the villain?" question with a picture.** A bound daemon is grey; a bonded one isn't. The Index shows it grey either way. **The player can see what the record can't.**
- **Corpus's daemons are grey.** Trainer parties are created at species base friendship; set Corpus's trainer class to 0. *The DAEMONS are inventory* — and every Corpus daemon on screen is visibly context-free, and nobody says a word. Craft rule 6, for free.
- **Halftone's decommissioned daemons and the ORPHAN are grey for a reason the town already gives.**
- **Wild daemons** appear at base saturation (a hint of hue). Remote daemons at their owner's. So the "one colour reflecting type" you already have becomes the *floor* of a scale rather than the whole treatment.

*Restraint clause:* this is the only place saturation means anything. Don't also tie it to level, happiness items, or edition.

### 1.4 Umbra without the grey world

8.6's colour moment is gone, and the doc is right that "more saturated" isn't the same instrument. The replacement is *value*: Umbra is the bottom of a descent the achromatic ladder has been making all game — a black room — **and the four humours are the four type anchors** (red VECTOR, yellow ENTROPY, black LATENT, white FROZEN), i.e. the *origin of the daemons' palette*, sitting in the dark insisting emotions are coloured fluids. The player has been reading those four hues on daemons for forty hours and meets them as people at the floor. Colour still arrives; it arrives by contrast with darkness instead of with grey, and it's a stronger beat than the DMG version because it's *explained by nothing and prefigured by everything*.

### 1.5 The post-game "see everything in colour" item — no

Three reasons, each sufficient:

- **It converts colour from an argument into a reward, and a reward is a metric.** The thing that made 8.6 work was that colour *meant* something. Handing it out for beating the Review Board makes it Scorn's kind of thing.
- **It is a Cognitive Clarifier for the player** — an instrument that changes what they perceive. That is craft rule 1's worst violation: *the game handing the player the frame they are standing in* (4.24 says exactly this about the eight-bit passage).
- **Friendship-saturation already does the job, per daemon, earned.** A player who bonded with their team finishes the game in colour. One who didn't, doesn't. Nobody is told.

If you want a post-game visual change, it's the one already adopted: bring S.T.A.R.R. to Ty, then to Crystal. Three lines, no palette.

---

## 2. The fable — what the animal rule newly implies

9.4's three-clause rule (integrated, plain, head-ratio-for-age) is right, and *Robin Hood* / Barks is the correct tradition. Things that fall out of it once you take "fable" seriously:

**1. A fable ends with the moral. This one cuts it.** Aesop's form is *story, then the sentence.* Craft rule 1 is the refusal of that sentence. So the shape of the whole game is **a fable with its last line removed** — which is worth writing into 0.1 as the one-line description of what the craft rules are *for*. Nobody in the game says the moral because the form is defined by withholding it.

**2. In a fable the species is a role — so every cast species is a claim.** Fox = the one who sees (Crystal; and *Ty P. Clear*, the fox who stopped seeing). Snake = the persuader, not the villain — Scorn *persuades*, warmly, and the tradition's trap (Sir Hiss) is already named. Owl = the peer reviewer, settled. Two that the names already decided:
- **HOLT is an otter.** A holt is *literally* an otter's den. The name chose the species before anyone asked, and an otter — a creature at home in two elements — is the man who held two frames in one address.
- **CAIRN** wants something that *carries its record on its back*: a tortoise. Slow, right, and Aesop's most famous winner.
Don't assign species to Corpus staff as a class — a single-species workforce reads as the sneer 3.1 guards against. Mixed species, identical lanyards.

**3. People are fable animals; daemons are creatures. The colour rule is the same for both.** A person's hue is *who they are* (three foxes, a palette apart). A daemon's hue is *what it is* (type) plus *what it has accumulated* (friendship). In both cases colour is identity, never decoration — which is why 9.4 survives the fable and the fable survives 9.4.

**4. Why the animals never bind each other is answered by the form.** In Aesop the fox and the grapes are not the same kind of thing, and nobody asks why. The daemon/person line holds because fables don't explain their ontology — the same reason 4.20a never says Holt wasn't a daemon.

**5. Age by head ratio has a cost worth logging:** Vera reads older than Al by name and younger by sprite. The sprite wins; adjust nothing, but note it so the naming pass for the rest of the Clears doesn't repeat it.

---

## 3. How the arc reaches the player — a beat sheet against the FireRed spine

The bible knows *what* the player infers; this is *where*, in the order they walk. Everything left of the arrow is vanilla structure; right of it is which surface carries the story there.

| Vanilla beat | Story surface | Act |
|---|---|---|
| Lab, CC-7, Index, Vera's house | Crystal's register; *"very good at what it records"*; the map that disagrees with the signs | I — the setup |
| Undertone stone, CAIRN | the chart as an artefact; *if it isn't written down it didn't happen* | I |
| Deadstack, Holt | Corpus, cheerful; the man who was in the box | I — first blame target |
| Ardor, KEEPALIVE, SENTINEL | the falling tree as rooms; nothing explains | I |
| Verdigris basement | **Scorn met, liked, hands over the RESOLVER** | I — the turn |
| Halftone | ORPHAN; the asset tags; the betrayal of the player's own judgment | I — blame peaks |
| Brazen | the review scores, the engraving, Al quoting his father | I — the documents |
| Lurid, HOLDOUT | TOKEN; the held-out set | I |
| Quicksilver | the 1001 log, the plate, the requisition, the minutes, **Ty: "I knew"** | I → the fall completes |
| Callow, Benchmark 8 | Scorn's accounting: *we are both to blame* | I closes |
| Umbra | the humours in the dark; Al on the incumbent's chair | the hinge |
| **Post-game** | S.T.A.R.R. in Doldrum's cave → Ty → Crystal | **II — the rise** |

**And the Sevii Islands are sitting right there.** FireRed gates Cerulean Cave behind the Sevii quest, which is Rocket-remnant material with Giovanni's absence at its centre. That is *Act 2's* shape — the organisation without the man, and the question of what's left when the blame has nowhere to go. Two honest options:

- **Cut them.** Warp the post-game straight to the cave. Cheapest, and the bible's rule.
- **Or Sevii is Act 2**, and the three-block triangle grows into a place. Seven islands with no pigment names yet, a Corpus warehouse the doc already put there, and Lorelei's house — which in our board is the *Phlegmatic* member, at home. It's a real Act 2 canvas. It is also, by a wide margin, the biggest scope commitment since 151 sprites.

Recommendation: **decide this before naming a single island.** Until then, Sevii is cut, and the post-game is the triangle.

---

## 4. Smaller notes

- **LOGIC / INTUITION** (9.10) — one option is a type name and the other isn't, so the pair is asymmetric in the game's own vocabulary, and the player who picks LOGIC picks the type the chart says loses. Either both are types (LOGIC / CONTEXT is wrong — those are the editions' cousins) or neither is. *REASON / FEEL*, or *RULE / READ*, keeps the shape without borrowing a column from the chart.
- **VERA CLEAR** — *vera* is Latin *true*, and Benchmark 8's mark is **TRUE**, handed out by Scorn. Recorded here as a coincidence, and the bible's rule says leave it exactly there.
- **SUBSTRATE as a Game Corner prize** is the best slot-reuse in the update.
- **CONTNT / CONTXT on the badges** — right call, vanilla's precedent, and the middle letter differs. Fine.
- **The Quest Log** needs a name in the lexicon now that it matters. Something that pays twice: *LEDGER* (a record, and the book that records money — CACHE's register).
- **HIBERNATE's entry** (*what comes back is identical; something is missing*) is the teleporter problem in eleven words and should be protected from any future "tightening" pass.

---

## 5. What to do, in order

1. Beat CAIRN on the GBA build, on hardware.
2. Implement the tint rule as a *flag*: Halftone grey, the Index/Log sepia. One afternoon; proves §1.2 in play.
3. Friendship-saturation on daemon palettes. Set Corpus trainer friendship to 0. Play a Corpus fight and look.
4. Decide Sevii — cut or Act 2 — before naming anything there.
5. Only then: title screens, face-offs, arms.
