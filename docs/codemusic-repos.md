# The CodeMusic repositories, read as a bestiary

A survey of all 47 repositories at [github.com/CodeMusic](https://github.com/CodeMusic),
read for what they give DAEMONS. Companion to `lineage.md`, which does the same
for the three blogs.

**The finding, stated first.** Two of these are not sources of inspiration for
the game — **they are the game's own argument, already built, years earlier.**

---

## 1. Dexter is the Index, and it was built for real

> *"A real-world Pokédex. Point the lens at a squirrel; Dexter identifies it,
> writes a dex entry **in a flat robotic voice**, speaks it while the text types
> out, and logs it as entry #004."*

4.2 says the artifact the player carries **can only measure content** — height,
weight, type, stats — with no field for the thing Crystal cared about, and that
its entries are *"written thin on purpose"* in a bureaucratic register.

**Dexter is that artifact, shipped.** Down to the flat voice. The critique in 4.2
is not an idea about taxonomy engines in the abstract; it is the author's own
tool, turned over and looked at from the other side. That is worth knowing and
worth never saying in-game.

*Design use:* none directly, and that is the recommendation. The Index already
exists and already does this. **Do not name a daemon Dexter.** The resonance is
strongest left where it is.

## 2. SafetyScribe is 4.10, with the instrument that was missing

> *"A one-button, push-to-talk **witness** & wellbeing companion… when anyone is
> spoken to in a demeaning or abusive way (e.g. condescension, baseless claims
> like `you're forgetting`), SafetyScribe lets you toggle recording, then
> automatically produces a timestamped email report with transcript highlights
> so the organization can take corrective action."*

4.10 is *a competent person removed by a correct-looking process*, and 4.1 turns
on Crystal having no way to be taken seriously afterward. SafetyScribe is the
device that preserves the account when the procedure will not.

**Caution, and it is a real one.** The word *witness* is load-bearing elsewhere
in the design and carries a puzzle with it. A daemon built on this idea risks
walking into that lock and giving away its shape. **Recommend: use the concept,
avoid the word.** A daemon that records what happened so it cannot be denied
belongs in this world — it should not be called WITNESS.

---

## 3. ROVERCUB — a real repo that solves a naming problem

> *"A simplified board implementing Rover's technology."*

8.2 needed a base form for the Reinforcement line and `ROVERRADIO` failed the
9-character cap at 10. **ROVERCUB is 9, is an actual repository, and reads as a
young animal** — which is exactly what a starter should be.

**ROVERCUB → ROVERSEER → ROVERBYTE.** Every stage is a real system, the arc is
explore → model → act, and the names fit without invention.

## 4. PENPHIN runs on a 64×64 RGB matrix

PenphinMind's first embodiment is *"an arcade-style device called Penphin
featuring a 64×64 RGB LED matrix display"*, doing *"generative game creation and
pixel art animation."*

8.6 makes greyscale the design and lets **colour appear exactly once**. Penphin
is the one thing in this author's built world that is literally a colour pixel
display. That is not a coincidence worth explaining, but it is a strong argument
for **Penphin being near the colour moment** rather than anywhere else.

---

## Daemon candidates, ranked by how much they decode

| Source | Reads as | Type | Why |
|---|---|---|---|
| **The-Seer** | a daemon that watches and *switches persona by what it sees* | CONTEXT | The repo already does frame-switching: *"switches persona automatically based on what's on screen"*. That is 4.6's ability in a menu-bar app |
| **CauseAndEffect** | a daemon that timestamps a cause and tracks its effect | CONTEXT / LOGIC | 0.3's loop, instrumented. Nothing else in the corpus is this close to the CFM |
| **PulseEntrain** | a daemon that synchronises with another | SIGNAL | Entrainment is two oscillators locking. A move, arguably, before a creature |
| **CHSAi** | two systems that must interact to produce a third thing | — | Penphin's architecture, written in 2024. Confirms the pattern rather than adding to it |
| **MemoryCleanser** | something that prepares memory by removing from it | LATENT | *"For gpt model training."* Quietly the most sinister repository here |
| **ImprovGPT** | unstructured generation | EMERGENT | The unsupervised temperament as a creature |

**`excuseGPT` deserves its own line.** It is *"infused with 500 excuses, 100 per
emotion, denoted by `~BASE~`, `~MAD~`, `~SAD~`, `~AFRAID~`, `~GLAD~`."`

That is a **five-state affect model the author already built** — and Gen 1 has
**exactly five status conditions** (SLP, PSN, BRN, FRZ, PAR). The mapping is
tempting and mostly works; the flaw is that Gen 1 statuses are uniformly
negative and GLAD is not. Recorded as an idea, not a proposal: renaming statuses
to an emotional taxonomy would make *every battle* say something about feeling,
which is either the best small idea in this document or far too much.

---

## What not to take

Most of the 47 are sites, forks, and course projects, and the temptation with a
list like this is to find a daemon in each one. **The bestiary needs 151 names
and this corpus supplies perhaps eight that decode** — the rest would be cameos
wearing a creature's shape.

8's scope rule applies to bestiaries as much as to towns: *the graveyard is full
of projects that designed 151 creatures and shipped zero towns.*
