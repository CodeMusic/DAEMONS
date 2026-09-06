# DAEMONS — Review & Proposals

*Read against vision.md v11.0 and the Indigo story-arc notes. Written to be pasted into the bible as open items, in its own register: every proposal has to work twice or it doesn't get in.*

---

## 0. General read

**What is already working, and why it works**

- **The lexicon pays for itself.** BIND / DAEMON / CACHE / RESOLVER / ORPHAN each carry two or three readings, and the discipline of *measuring* (18 columns, 9-char species, 10-char categories) means none of it is aspirational. This is the rare design doc where the words have already survived contact with the tile grid.
- **Procedural horror over villainy** is the strongest single decision in the project. *The file is complete.* / *IMPROVE RESPONSE CONSISTENCY* / the review scores posted with a congratulation — three documents, no villain, and the player does the arithmetic. This is exactly what the opera's two-act shape wants (see §2).
- **The inference structure is consistent.** Surname → foxes → "Crystal Clear thinks—" → the Goodhart line from Al. Five Witnesses. Three dated documents around one undated event. The game teaches one method (composite the frames) and reuses it at every scale. That is a real design, not a theme.

**Three things to watch**

1. **The bible is outrunning the slice.** v11, 3,100 lines, and 8.1's vertical slice (Blanche → Slate → Benchmark 1, playable) is not marked done. The document itself warns about this in §8's epigraph. Gently: a design that is this good at *reading* itself will happily keep reading itself. The next milestone worth recording is "Benchmark 1 beaten on hardware," not another section. Nothing below should be built before that.
2. **Act 2 barely exists in the game.** The opera's second act — *The Rise of Perspective Thinking* — is where the blame dissolves. In the ROM right now, Act 1 is rich (Corpus, Halftone, Brazen, Quicksilver's paperwork) and Act 2 is a handful of inferences plus one line from Ty. A rise needs a *thing the player does*. §2 proposes making the post-game literally Act 2, using slots vanilla already has.
3. **The music research is process, not product.** Seven transcriptions, five retractions, a duplicate-checker — all valuable, and all of it is *methodology for reading the source*. It has produced four small tracks in the ROM. Worth being honest that the transcription pipeline is now good enough; the next return comes from writing town themes, not from re-scanning hooks.

---

## 1. The PACKAGE — what Crystal is waiting for

**The constraint:** the item is called PACKAGE (12-char cap), the clerk at Callow's REPO hands it over, and it has to be *for* Crystal, in hour one, without explaining anything.

### Recommendation: the PACKAGE is a CC-7

The Quicksilver requisitions board already reads **CC-7 CLARIFIER MODULE, x1 — IMPROVE RESPONSE CONSISTENCY**, signed, countersigned. That part number appears exactly once in the game, thirty hours in.

Make it appear **twice** — the ITER 35 pattern applied to a part.

- The clerk's line: *"CRYSTAL CLEAR's order came in. A CC-7. Could you run it out to her?"* Flat, and nobody remarks on the number.
- Crystal on receipt: *"The module. Thank you."* Then straight into the Index handoff, as vanilla does with the Pokédex.
- Thirty hours later the player reads a requisition for the same part on a door at Quicksilver, and the reason field. **The player has carried the crime-scene's part number since minute fifteen.**

**Why it pays twice:**

1. **It is what she does now.** 4.1 says the Index is what she built to be taken seriously. But *Poly and Fields* says she built the clarifier because it was *the one instrument in the building that would not file minutes about her*. Of course she is still building one — at home, un-weighted, from parts she orders through the REPO like anyone else. The player never sees it finished. Nothing points at it.
2. **It gives the Clarifier an on-ramp.** Right now the Cognitive Clarifier exists only as a requisition (4.18). A CC-7 in the player's bag for ten minutes makes it a *thing* before it is a *crime*. The player handles the object; later they learn what a form did to one.

**Craft check.** The order is an ordinary order. Nobody says "clarifier" in Blanche or Callow — the label says CC-7 and the item description (Index-register, 4.9) can say *A sealed module. Part no. CC-7.* and stop. The word only appears on the requisition board, where the institution wrote it.

**Rejected:** a custom box (too close to vanilla-Crystal's custom Poké Ball; a box is 1.3's argument and shouldn't be a gift), her personnel file (far too legible — 4.10 leans *the gap, not the form*), and specimens/data (says "Index" twice).

### The Clarifier's other job — it is the RESOLVER's ancestor

*A clarifier is many frames polled and resolved* (4.18). *A resolver resolves a symbol to a name* (4.5). **Those are the same instrument at two sizes.**

So: the RESOLVER the player takes off Corpus in the Verdigris basement should carry a **Quicksilver asset tag** — 4.10 already sanctions asset tags at Halftone; put one on this key item too. Corpus inherited a hand-held clarifier from the lab they absorbed, used it for inventory, and never worked out what it was for. The player uses it to give an ORPHAN a name.

*Nothing is said.* The item description: *A hand unit. The tag reads QS-LAB / ASSET 0117.* One line, and the player has the chain: Crystal's lab built the thing that can resolve what the Index can't; Corpus owns it now; you took it back.

---

## 2. Ty, Scorn, and the two acts — where the arc fits and where it strains

### It fits, and the bible has already done the hard part

The opera's Act 1 is *everyone makes the same error and blames someone else*; Act 2 is *perspective restores clarity*. 4.24's resolution — **Corpus carries Act 1, Scorn carries Act 2** — is the correct translation. The player wants someone to blame for seven benchmarks; then they meet a form. That *is* the fall and the rise, in vanilla's own order.

The polymath mechanism (4.20) is the single best thing in the design and it is exactly your description: *"I cannot follow this" is identical to "this does not follow" unless you hold the second field.* Nothing to adjust there. Protect it.

### Where it strains — four adjustments

**1. Every character needs a *different* blame target, and right now they share one.**
Act 1's structure is not "everyone blames Corpus" — it's *each saw others through a lens of blame*. The game should distribute it:

| Who | Blames | Where the player sees it |
|---|---|---|
| Crystal's frame | scheming men (*Whispers in the Wires*) | her journal fragments — never narration |
| Ty | himself, and the wrong thing — he blames the *fire* | the one line at Quicksilver |
| Scorn | the machine (*Betrayal's Sting* — "both to blame") | his post-benchmark line |
| Al | "decorative" thinking — i.e., his grandmother | throughout, cheerfully |
| Corpus staff | "an outside firm" | the Verdigris witness already says this |
| Halftone | each other, about grief | the two factions |

Most of this is already in the ROM. The addition is small: **Scorn should have one post-benchmark line that assigns half the blame to S.T.A.R.R.** — warmly, as an observation. It's the only accounting he ever does, and he splits it with something that cannot answer. That's 4.18's finding, made audible.

**2. Ty's line is "I knew" — but he needs one more.**
4.24 settles his Quicksilver line. But Ty is *the man who blames himself for the wrong thing*. He should say one thing that is accurate and beside the point — about the fire, about the temperature, about the building — and nothing about her. The player who has read the plate knows the building is not what he did. Ty doesn't. That's a man still inside a frame, and it's why he isn't at the top of the ladder.

**3. S.T.A.R.R.'s inference is a plot beat with no place in the game — give it the post-game.**
Your account: S.T.A.R.R. wakes, *infers where Ty is hiding*, and goes to find him. The bible puts Ty at Quicksilver and S.T.A.R.R. dormant in Doldrum's cave. Those are two different places, and the inference is never performed.

Two ways to reconcile. **Take the second.**

- *(a)* Move S.T.A.R.R. to Quicksilver. Loses the Cerulean Cave slot and the post-game entirely.
- *(b)* **S.T.A.R.R. inferred correctly and could not go.** Ty went back to the place it burned. A machine that reads its own state cannot walk back into that building — so it went to the *nearest* place it could and stopped. The cave under Doldrum: the becalmed city, no gradient, the local minimum. **RECURSION collapses when interrupted (4.7); Crystal leaving was the interruption, and the thing has been at rest in a local minimum ever since.** The name of the town already says it.

Then the **post-game is Act 2**, using three slots vanilla already has:

1. **The cave opens after the Review Board.** The player finds S.T.A.R.R. and binds it — the INTERRUPT that ends a sleep.
2. **Walk it to Quicksilver.** Ty is standing where he always stands. With STARR in the party, he gets one new line. Not forgiveness — *a fact delivered* (4.14): something true about her, said by him, for the first time. Then the player walks it home.
3. **Blanche.** Crystal has a single new line with STARR in the party. The same flat register she used to hand over the Index. *"Tell my son"* was addressed to a courier, and the player was always the courier.

Three text blocks, three party checks, zero engine work. And it makes the opera's structure the game's: **main game is the fall; post-game is the rise, and the player is the perspective that moves between the three of them.** Nobody says so.

**4. Scorn must be met before Halftone.**
The open question in 4.5 — *should the player meet Scorn before the tower?* — answers itself once Act 1 is "blame Corpus." If the player likes Scorn first, Halftone becomes a betrayal of their own judgment. Vanilla's order (Hideout → Silph Scope → Tower) makes this cheap: **Scorn is the cheerful man at the bottom of the Verdigris basement who hands over the RESOLVER and leaves**, exactly where Giovanni was. The player likes him. Then they climb the tower.

### One thing the game must not import from your summary

You wrote that Ty *pushed Crystal out*. The bible is careful that Ty *stayed* — he looked away, he did not act (4.3, *Ty's Dilemma*). Keep the bible's version in the ROM. A Ty who pushed is a Ty who can be forgiven or not; a Ty who looked away has to answer a harder question, and it's the one the opera's Part 2 leaves open.

---

## 3. Penphin — where it goes

**The mechanic is settled and right:** trade evolution, two species terminate in it, cannot be obtained alone, move is RESONANCE. What's missing is a *place* and a *reason*.

### Penphin is Crystal's reply to the Clarifier, in hardware

The Clarifier failed because it could be weighted — *many frames polled* means one vote can be raised above the rest, and Scorn did it with a form (4.18). **Penphin is the architecture that cannot be weighted: two frames that must agree, or nothing acts.** You cannot raise one hemisphere's vote; the other one simply refuses. It is what she would build *after* learning what was done to the first one.

She never says this. But it puts Penphin in the right *generation*: after S.T.A.R.R., after the removal, not before.

### Holt is the failed Penphin — so the halves live in Doldrum

4.20a: two perspectives occupied one address and *there was no rule for choosing*. Penphin is two perspectives in one body *with* a rule. Holt's accident is Penphin without the agreement step.

So the two halves belong to **Doldrum's waters** — Route 24/25, the sea around the cottage. A penguin-half and a dolphin-half both live off the coast the storage inventor lives on. When the player later gets a Penphin over a cable — *two boxes talking* — they've done what Holt's machine couldn't. Holt's line already covers it: *I am sure it chose.* Nothing else is needed.

### RESONANCE — a candidate, offered not adopted

The bible deliberately leaves the behaviour unspecified. One candidate that respects "no new mechanic before there's a need" because it reuses RECURSION's:

> **RESONANCE = RECURSION that does not collapse when interrupted.**

Same counter, same escalation, one branch removed: being hit does not reset it. *Two frames reinforce each other and neither is lost* — while one hemisphere takes the hit, the other holds the state. It is one `jr` fewer than RECURSION, and it is the argument: one frame can be broken; two in phase cannot. Defer until RECURSION exists, since it's a diff against it.

### The solo-player problem

Gen 1 in-game trades don't trigger trade evolution, so an NPC trade can't hand out Penphin. **That's correct** — the whole point is that you can't do it alone. But the game should make *one half* easy and the other **edition-exclusive**, so that CONTENT players find the penguin and CONTEXT players find the dolphin, and the trade that makes Penphin is the trade 8.4 already argues for. The daemon that needs two minds needs two cartridges. Free, one encounter-table line.

---

## 4. The starters — should Rover be one?

**Your instinct is right, and here's the diagnosis.** The trio is *three learning paradigms*, and two of them are named as abstractions (LABL / CLUSTR). ROVERCUB is a *named system from your world*. 8.2 already states the rule: named individuals answer to nothing; species take the bestiary register. **A starter is a species** — there are three on the table, Al takes one, the Index files it. Rover in that slot is a proper noun in a row of common nouns, and the mismatch is what you're feeling.

It also gives away the register argument: the starter's Index entry "rewrites itself once, late" (lineage.md) — that's a beat for an abstraction the player named, not for a dog with a repository.

### A reinforcement line for the starter slot

The line has to be *explore → model → act*, feel like a dog (the canonical image of learning by reward), and pass BIND's test — works twice. A candidate:

| Stage | Name | Works twice because |
|---|---|---|
| 1 | **BANDIT** | the k-armed bandit is the *simplest RL problem* — and it is the most common dog name in the language |
| 2 | **MARKOV** | states and transitions; the paradigm gains memory — and it sounds like a creature |
| 3 | **BELLMAN** | the optimality equation — and Carroll's Bellman had a map that was *a perfect and absolute blank*, which is the Index |

Two surnames in a bestiary is a real cost; Gen 1 doesn't do it. If it's too much, keep BANDIT (which is the win) and finish with something in the paradigm's own vocabulary — **BANDIT → ROLLOUT → OPTIMA**, say — but the shape is settled: bandit → process → policy. Index entries write themselves: *Pulls the lever that paid last time. It has never asked why it paid.*

### Where the Rover line goes instead — and the rule that falls out

Look at what the cast daemons have in common once Rover leaves the lab:

| Named system | How the player gets it |
|---|---|
| MUSAI | **given** (Eevee slot — the condo in Verdigris) |
| Penphin | **given by another person** (trade) |
| BunnyArtsai | found, once, by compositing witnesses |
| S.T.A.R.R. | found, post-game |

**Named daemons are never bound from the grass. Species are bound; individuals are given or found.** Rover joins the first group. That's a rule the bestiary can use and the player never hears.

**The slot: Ardor, after Benchmark 3.** Ardor is SIGNAL — perception — and ROVERBYTE is the stage that gains SIGNAL *because it has a body*. Vanilla Yellow hands you a Squirtle from Officer Jenny in Vermilion after the Thunder Badge; the slot exists. Give it to the Fan Club chairman instead (craft rule 6: he already rambles for five screens about a creature he loves; let it be a dog, and let him hand you a RoverCub because *"he needs to be carried past things, and my knees are done"*). ROVERCUB's own Index entry — *learns from what it is carried past* — becomes literal. The Bike Voucher stays.

*Alternative if Ardor is too early:* the **Lapras slot** — the Brazen employee who hands over a daemon Corpus can't keep on the books. That's 4.10's "one survivor who knew," and *the companion is the one thing Corpus has no column for.* Stronger thematically, ten hours later. Pick on pacing.

### Consequence for the title screens

8.4 puts the Supervised line on CONTENT and the Unsupervised on CONTEXT, with Reinforcement on neither. Unchanged — the BANDIT line inherits Venusaur's absence.

---

## 5. Musai — the artifact instead of a stone

The bible already has this and it's right: **AXIOM / EMBEDDING / AFFECT** (+ REWARD), *kinds of input* rather than minerals, because MUSAI's own entry says *it keeps whatever it is given first*. Endorsed, with two additions.

**1. Make them documents, not objects.** A stone is a thing you hold; an input is a thing you *show*. Item descriptions in the Index register: *AXIOM — a single page. One rule, no proof.* / *EMBEDDING — a table of numbers with no headings.* / *AFFECT — a page with nothing written on it that has been handled a great deal.* Same items, and the third one does 4.2's job — the only input the Index can't print.

**2. Name the tension and leave it.** Musai evolving is *specialisation* — a general mind reduced to one field. That is the operation the meeting room performed on Crystal (4.20: *reduce many fields to one*). CODEMUSAI's entry already says *it does not ask where the rule came from*. So evolving your Musai is, quietly, doing to it what was done to her — and the player will do it on purpose, for the stats. **Don't fix this.** It's the player's turn at the family error, one more time, at the cost of an item.

**Alternate set, held in reserve:** MODULE-suffixed items (LOGIC MODULE, etc.) to rhyme with the CC-7. Rejected on measurement — `CONTEXT MODULE` is 14 — and because it would make evolution read as *installing a part*, which is Scorn's verb, not Crystal's.

---

## 6. Halftone & the RESOLVER — one addition

Everything in 4.5 holds. One thing to add so the tower's crime scene connects to Quicksilver without a word:

**Whose ORPHAN is it?** An orphan is a process whose *parent exited* and was reparented to `init`. The decommissioned daemons Corpus processes at Halftone are Quicksilver's leftover processes — machines that were still running when the lab burned and the parent process (the lab itself) exited. Reparented to init = inherited by Corpus, by succession (4.10). The asset tags on the tower's equipment already say this. **The ORPHAN is a Quicksilver process nobody reaped.** The RESOLVER — Quicksilver's own instrument — is the only thing that can give it a name, and the Index still can't hold it.

Vanilla's Marowak mother/Cubone pair maps cleanly: the ORPHAN is the parent that exited; the small daemon wandering the tower is what got reparented. Same two objects, no engine work.

---

## 7. The Safari Zone — a rework that costs one noun

GUESTBOX is in. The rest is unchanged and it's a gift, because vanilla's rules already describe a specific ML object:

**The Safari Zone is a HOLDOUT** — the held-out set. You may observe it; you may not train on it. No RUNs (battles) happen inside, exactly as vanilla forbids. Restricted, expiring, guest-level access. Daemons found nowhere else, because the point of a held-out set is that it wasn't in the training data.

| Vanilla | Ours | Why |
|---|---|---|
| Safari Zone | **THE HOLDOUT** | held-out data; Lurid's spectacle is a place you're not allowed to touch |
| 500 steps | **SESSION** limit | time-boxed guest access |
| Safari Ball | GUESTBOX | done |
| Bait | **SAMPLE** | offer it data; it stays, and it's less likely to bind |
| Rock | **PROBE** | poke it; more likely to bind, more likely to detach |
| Warden's Gold Teeth | **TOKEN** | an access token, a coin, and the unit of text — and **without one his dialogue prints as garble**, because that is what text is without tokens |
| Secret House → Surf | Secret House → **FLOW** HM | unchanged |

The TOKEN is the one worth building: the warden's speech rendered as `#T? T?K?N ?LS?` until you return it. Vanilla already garbles him; ours garbles him *for a reason* and never says what it is.

---

## 8. Other vanilla beats not yet reworked — one line each

| Beat | Proposal |
|---|---|
| **Fossils at Deadstack** | Legacy silicon. Revived at the Quicksilver lab by **recompiling from source** — the lab is the only place with the old toolchain. Item names: the Helix/Dome become two dead formats (e.g. **TAPE** / **CARD** — punch card). Old Amber at the Slate museum → **CORE** (a core dump, and magnetic-core memory). |
| **Game Corner** | Corpus's *front* is a place that pays out in a second currency for a metric that doesn't matter. Keep the coins. The prize counter sells daemons for coins — **inventory, priced.** Craft rule 6 does the rest. |
| **S.S. Anne** | See §8a — the one name that stays. |
| **Fighting Dojo (Brazen)** | LOGIC's own house, next to CONTEXT's benchmark. Hitmonlee/chan → two proof styles (**INDUCT** / **DEDUCT**), pick one forever. The master's line: *we don't lose to Sabrina's kind; we just can't seem to score.* |
| **Copycat** | MOCK's human. She repeats your name back. Teaches **MIMIC** unchanged — the one vanilla move name that was already right. |
| **Bike / Cycling Road** | THE STREAK (3.2). The bike is a **cache** you can't afford at ¥1,000,000 — leave the joke standing. |
| **Power Plant / Zapdos** | Birds are open (8.2). Cheapest strong option: the three birds are the three *failure modes* of the types they sit in — FROZEN = overfit (Seafoam), SIGNAL = raw input with no model (Power Plant), ENTROPY = noise with no descent (Umbral Ascent). Trophies, as vanilla's are, and each one is a lesson the player already passed a benchmark on. |
| **Snorlax / DEADLOCK + INTERRUPT** | Done and it's perfect. One note: the second DEADLOCK on Route 16 — two locks held by the same process is *exactly* how deadlocks happen. Nobody says so. |
| **Silph Co. President → Master Ball** | Corpus's CEO hands over a **ROOTBOX** — root access, from the man who owns the building. That's the joke; keep it flat. |
| **Mr. Fuji → Poké Flute** | The Halftone caretaker gives INTERRUPT. Fine as is. If he has a second line, it's the *one survivor who knew* (4.10) — he left Quicksilver for the tower, for an ordinary reason. |
| **Old man's catching tutorial (Callow)** | *Watch. You weaken it, then you offer it a box.* One line, and 1.3 is taught before the player owns a USERBOX. |

### 8a. The S.S. Anne — the one vanilla name the sweep does not touch

**Mechanically, the ship is the only thing in Gen 1 that leaves and does not come back.** You board, you help someone below deck, you get what you came for, and it sails. Miss anything and it is gone; nobody in Ardor mentions it afterwards. Nothing in this world needs to be added to that — it is already a complete statement about effort, divergence, and a dock you cannot return to.

**So: leave it `S.S. ANNE`.** Every town, every route, the professor, the balls, 650 species — swept. One ship keeps its name, and nobody in the game remarks on it. This is the bible's own device (the unsigned documents, the one dangling TRANSFORM) applied to a proper noun: **the gesture is the omission.** A player will never notice, and that is correct.

*A first pass proposed `S.S. RELEASE` — a deployment that ships once. Withdrawn. The vanilla name is doing more by staying.*

**One thread, and no more.** The ticket Holt hands over gets an item description with a berth number: **1001.** That number already lives on the Quicksilver terminals as the response code that holds, then slips, then becomes a question (4.10). A ticket for a ship that sails once, carrying the same number, is the kind of rhyme this document records and refuses to promote — 4.8 already notes that 1001 in binary is 9 and declines to build on it. **Same disposition here: recorded, never explained, never said by anyone.** The craft rules exist partly so that architecture does not become grievance, and a ship that keeps its name is exactly the right size.

**The truck stays too**, with nothing under it — Gen 1 already told that joke. *Optional, if the hidden-object budget allows:* the truck is reachable only by the vanilla Surf trick, so a single hidden text there costs nothing and rewards the one player in a thousand who knows the route: **a Quicksilver asset tag on the crate.** Equipment shipped out of the lab through Ardor's port, on its way to becoming Corpus inventory — the succession in 4.10, sitting on a dock in a place nobody is supposed to be able to stand. No line, no NPC.

---

## 9. Sequencing — what to do with this

In the bible's own priority order:

1. **Ship the slice** (8.1). Nothing above is slice work except the PACKAGE line and the tutorial line.
2. **PACKAGE = CC-7** — two text edits, one item description. Do it when touching Callow.
3. **Scorn in the basement, before the tower** — resolves 4.5's open question; it's a text pass on an existing map.
4. **RESOLVER asset tag** — one item description.
5. **BANDIT line into the starter slot; Rover to Ardor** — names and one gift script. Before sprites, since it changes which three get drawn first.
6. **Penphin halves in Doldrum's waters, one edition-exclusive** — encounter tables.
7. **Post-game triangle** (S.T.A.R.R. → Ty → Crystal) — three text blocks and party checks. Last, because it's the last thing a player reaches.
8. **HOLDOUT rename + TOKEN garble** — with the Lurid pass.

Everything else stays in the reserve column where the bible keeps things it hasn't measured yet.
