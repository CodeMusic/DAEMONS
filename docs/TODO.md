# TODO

**Work that has been decided and not done.**

---

## What belongs here, and what does not

`vision.md`'s decision log has an **Open** list, and it had been carrying two
different kinds of thing at once — genuine questions nobody has answered
(*"Are the humors too neat?"*), and decided work nobody has built (*"`PC` →
`PORT` is decided and not swept"*). Those want different treatment, and mixing
them is why the second kind kept getting lost.

> **The Open log holds a question. This file holds a job.**
> An item moves from Open to here **the moment it stops being a decision**.

**Ids are permanent.** A finished ticket is struck through with the commit that
closed it, never deleted — the same convention the Open log already uses, and
for the same reason: the record of what was decided is worth more than a short
list.

**Add a ticket the moment a request would otherwise live only in a
conversation.** That is what this file is for.

### Claim a ticket before you start it

**Sessions run in parallel and cannot see each other's working trees.** Six
version numbers have now been taken twice because two branches both reached for
the next one, and a ticket is the same hazard with more of the day attached.

> **Mark the ticket `WIP — <branch>`, and get that mark onto `main` BEFORE
> doing the work.** An uncommitted claim is invisible, which makes it worse than
> no claim: it looks like diligence and prevents nothing.

*Clear the mark when the ticket closes.* **A stale `WIP` is the one failure mode
here** — if a branch is gone and the mark is still on, the ticket is free.

### Read the ticket, then check it — the oldest ones are the least true

**A ticket records what was true on the day it was written**, and this file has
been going long enough that the old ones have drifted. ***Four tickets closed on
2026-09-11 had a premise that was wrong, and in every case the ticket's own
claim was the thing that needed correcting rather than the code:***

| | it said | it was |
|---|---|---|
| **T-41** | 41 thin openings | *22 of them were `WRITE`, `FLIP` and `PUSH` — **which 2.8 settled on purpose.** The check was arguing with the design* |
| **T-26** | rewrite ~9,500 words | *a **read** of 9,500 and a rewrite of **18 blocks**, because vanilla already wrote its islanders in register* |
| **T-44** | two false positives | *two, plus **three holes the check had been silent about** — including 77 of 78 stale ability names* |
| **T-34** | the starter names are placeholders | *seven of nine were load-bearing; the other two were a **ten-day-old collision the newcomer caused***, which the git log settled and neither of us remembered correctly |

> **Spend the first twenty minutes proving the ticket, not doing it.** *Measure
> the thing it claims.* **If the number comes back different, that IS the work** —
> and it has been better work than the ticket every time so far.

*The corollary is cheap and worth saying:* **the git log is evidence and memory
is not.** *T-34 turned on which of two names was written first, and the answer
was one `git log -S` away.*

---

## Ready — decided, unblocked, nobody has done it

| | what | where | from |
|---|---|---|---|
| ~~**T-41**~~ | ~~**The 41 thin openings.**~~ ***Closed `7f2df046d` — and the list was wrong.*** **Twenty-two of the forty-one were daemons opening with `WRITE`, `FLIP` or `PUSH`, which 2.8 SETTLED ON PURPOSE.** *A check that fires on a thing the design decided is arguing with it, not measuring it.* `THIN OPENING` is retired and replaced by two flags that mean separate things — **`MIXED SIGNAL`** (*before 10 it does something typed, it is the wrong type, and it never does its own*) and **`LATE TYPE`** (*first on-type damaging routine after 25*) — **which between them caught four the old flag missed.** Eighteen substitutions, nineteen daemons, all four flags now none, off-type 41% | `level_up_learnsets.h` · `tools/gbacoherence.py` | **2.7d**, 2.8 |
| **T-33** | **`MOON STONE` wants a name.** *Tied to a place rather than a paradigm, so 8.2 held it for the town pass* — **and the town pass is done.** The stone is already written into 4.30, so the name has to survive a room that describes it | `engineGba`, items | 8.2, 4.30 |
| **T-16** | **Per-gym battle backdrops.** Eight benchmarks, eight rooms, one backdrop, and it is the one place decoration IS the argument: 5.3 gives each gym a lever and the backdrop can be the room you met it in. ***Costed wrong when it was proposed** — "ROM-only, cheap" is true of the BYTES and false of the work.* **Gen 3 keys the backdrop off ten TERRAIN types, each a full tileset, tilemap and palette in `graphics/battle_terrain/`** — so reassigning an existing one per gym is a data change, and eight gym-specific ones is **eight new tilesets**. *Decide which of the two before starting* | `graphics/battle_terrain/`, `src/battle_bg.c` | 5.3, 9.4 |
| ~~**T-39**~~ | ~~**The cross-gen relatives of our Kanto lines are HALF renamed.**~~ ***Closed `e9dcc84c4` — and there were FOURTEEN, not thirteen.*** *`HITMONTOP` was missing from the ticket's own list.* **Each named from its own line** (2.7f): the sleep ladder gained `STANDBY` below SUSPEND, the argument triad gained `PREMISE` and `CIRCULAR`, and `GOLDSET` is the clean twin of BADSEED off the same BLIGHT. **All four ROMs build and `gbastr` confirms the names through the charmap.** *The tool gap it exposed is the lasting part* — **every check defines "ours" by diffing against upstream, so a daemon we forgot to rename is invisible to all of them** | `engineGba`, species | T-36, 8.2, **2.7f** |
| ~~**T-42**~~ | ~~**`TAINT` was withdrawn in 5.2 and was still in the game.**~~ ***Closed `b8e509ed6`.*** The routine is **`TAMPER`** (CORRUPT's clause as a verb) and the Viridian line is rewritten. **Root cause: `é` is a lowercase cased character**, so `.isupper()` was dropping every accented vanilla name from `port_vocab`'s rename map — *the exact set the pass exists to remove.* **`VETOED` in `check_lexicon` now fails on any withdrawn word in player-visible text**, and `port_vocab` grew an **a/an agreement pass** (17 pre-existing errors) | `tools/`, `engineGba` | 5.2, craft rule 3, **2.7e** |
| **T-38** | **Both story documents go stale silently.** *`story-readthrough.md` had one commit in eleven days and was a whole act behind; `story.md` existed only in a conversation until it was searched for in a transcript.* **Every other surface here has a tool or a check keeping it honest and these two have neither** — they are prose, so the check cannot be a diff. *A date and a "last reconciled against vX" line at the top would at least make the staleness visible* | `docs/`, `tools/` | this review |

---

## Blocked — decided, but something has to happen first

| | what | blocked on | from |
|---|---|---|---|
| **T-05** | **Callow and The Bleed share their music.** *8.1's second theme cannot be given to either until they have a slot of their own* | **A track that does not exist yet.** *Re-read 2026-09-10 and the ticket was aimed at the wrong repo:* `data/maps/songs.asm` is the **Game Boy** build, which CLAUDE.md says is a reference and not updated further. **On the GBA it is one field in a map's `.json`** — so the plumbing is not the blocker at all. `song-status.md` lists eleven compositions still unassigned, and this wants one of them | 7.3, 8.1 |
| **T-10** | **The missing key signature as a puzzle** — notes reading flat because the key is absent, and giving them the key lifts them. **2.6's one-clause test for CONTEXT as a room rather than a definition**, and 5.3 names *the room* as one of four levers a grinder cannot grind | Wants **Brazen gym**, which is T-03's territory. Sequence it after | lineage 3b, 5.3 |
| **T-11** | **The 87 unreachable routines.** 2.10 renamed 269 of 356 — every routine the player can meet in this game | The rest wait on **the bestiary**, not on a decision | 2.10 |


---

## Wants a decision first — these are Open log items, listed only so the trail is here

*Do not work these. They are questions, and the answer belongs in `vision.md`.*

- **THRASHING's ownership** — is *"the state no type owns"* the point, or does it want LOGIC? (2.7)
- **THROTTLED's five strays** — SIGNAL owns it six to five (2.7)
- **SUSPENDED's six sleep moves** — CONTEXT owns the concept; retyping the moves is a balance question (2.7)
- **`PKRS` still says PKRS** — the condition has no place in the lexicon yet (9.15)
- **`LEGACY` → `RUST` and `VECTOR` → `FLOAT`** — a gym, a museum and a badge each (8.7)
- **Whether the doctrine has a name, and whether he has one** — *placement settled by T-22: SIX ISLAND's GREEN PATH, somewhere with nobody to check him.* **Both names were left off on purpose and that may be the answer**: naming the doctrine gives the game a thing to hold, and 4.33's whole rule is that it holds nothing (4.33)
- **Re-score the one-clause test at 17 types** — CONTEXT's 8/8 was scored without OPAQUE (8.7)

---

## Deferred — decided we want it, decided not yet

*Not blocked and not a question. **Someone looked at the cost and said later.***
An item here needs the reason recorded, or it comes back as a fresh idea in a
month and gets re-argued from nothing.

| | what | why not yet |
|---|---|---|
| **T-18** | **A follower daemon.** One walking behind you, Yellow/HGSS style. *"You bind a daemon and you host it" is an abstraction everywhere except here* — a follower is the one place 1.1's argument would be visible rather than stated | ***The only one of the five ideas with a real RAM cost.*** It wants an object-event slot and sprite tables, and `engine.md` puts the free static space at **1.1 KB of EWRAM and 2.9 KB of IWRAM**. **Measure it before promising it** — every other job on this list is ROM-only and free. *Deferred 2026-09-10, by choice rather than by blocker* |

---

## Closed

*Struck through, never deleted. The record of what was decided is worth more
than a short list.*

| | what | closed by |
|---|---|---|
| **T-43** | ~~**Two words carrying a second reading nobody chose**~~ | this commit — ***both stay, and the test that cleared the first found a third nobody had decided.*** **`KILL` is not a tonal break: the lexicon already held the whole event** — *`KILL` the routine, `SIGKILL` a daemon, `DETACH` what vanilla calls fainting.* ***You kill a process and it detaches.*** **Its three siblings agree** — `TERMINATE`, `WIPE`, and ***`FISSURE`, which had never been renamed at all***: a vanilla geological word among three process words, learnable at 41. **`FISSURE` → `SEGFAULT`**, *a fatal fault in the layer everything else runs on, which is 2.6's STRATUM.* **`WEED` is settled by `BLIGHT` → `BADSEED` → `GOLDSET`.** *Recorded as 2.10a* |
| **T-40** | ~~**Vanilla Kanto Index entries under our names**~~ | this commit — ***the ticket said ten and the number is thirty*** (25 in FR, 29 in LG). **And the first measurement said ten too, and was wrong**: *comparing our entries to upstream byte-for-byte reports almost everything as rewritten, because the sweep turned POKéMON into DAEMON inside every one.* ***The comparison has to apply our vocabulary to vanilla first*** — **PULSAR, the daemon that raised the ticket, did not appear in my own first list, which is how the error surfaced.** *Thirty written to both editions in the authored voice; same text in both, which holds the divergence reduction rather than spending it.* **`check_lexicon` now refuses a renamed daemon whose entry is vanilla's** |
| **T-34** | ~~**The starter names are placeholders**~~ | this commit — ***re-cut after all, and the git log is what decided it.*** *First reading: seven of nine were load-bearing and the two odd ones were a device worth promoting.* **The history says otherwise** — `LABL` and `CLUSTR` landed **2026-08-31**, `CLUSTER` landed **2026-09-10** and had never existed on the Game Boy at all, ***so EXEGGCUTE walked into a ten-day-old collision and the newcomer moved.*** **`LABEL` · `CLUSTER` · and EXEGGCUTE to `BOOTSTRAP`**, *which sharpens its own joke — bootstrap aggregating is how an `ENSEMBLE` is built.* **8.2b's register was the argument all along: the technical surface is the undisguised word.** *`check_lexicon` now refuses a name that is another with a vowel dropped — three narrowings, and the rejected ones are in 2.7a* |
| **T-26** | ~~**Sevii tier 3b — the ~9,500 words**~~ | this commit — ***18 blocks of ~750, across all seven islands.*** **The rule held exactly as 8.2a wrote it; the SIZE was wrong by an order of magnitude.** *And the shape of the eighteen is the finding:* **eight island SIGNS, three public NOTICES, four SHOPKEEPERS and three lines from the REVIEW BOARD's own leader** — ***not one ordinary islander***, because vanilla already wrote them as people who happen to be somewhere. **The rule did not need applying to the islands; it needed applying to the institutions standing on them.** *Every remaining sign also asserted a **second vanilla name** — Chrono, Boon, Kin, Quest, Knot — for an island the map calls a number.* **Found on the way: `MT. JITTER`, a mountain in neither column, on five signposts** |
| **T-44** | ~~**`check_agent_vocab` cried wolf twice**~~ | this commit — *both false positives gone: **`PRIORITY/Paralyze Heal` is the glossary working**, and `backtracking confusion` is English.* ***Then testing the checker against sentences it should catch found three holes it had been silent about***: **the town patterns were UPPER-ONLY**, **species were not checked at all** (a hand list cannot hold 151, so nobody wrote one) and **abilities were the same hole from both sides** — `port_gamedata` was missing `ABILITY_NAME`, so the bridge reported `TORRENT` where the ROM says `SPILLOVER`, **77 of 78 stale.** *The live prompt stays scanned, but a hit whose word is no longer in anything we author is reported as history rather than counted as a fault* |
| **T-35** | ~~**Re-port the harness after every name pass**~~ | this commit — *closed by T-44 rather than on its own.* **`port_gamedata.py` now covers `ABILITY_NAME` as well as species, moves, items, maps and objects**, and reports **nothing to do on every table.** ***The ticket's premise was that the tables go stale; the finding was that one table was never in the tool at all***, so re-running it faithfully would never have fixed abilities |
| **T-36** | ~~**The daemon × type × routine coherence sweep**~~ | `546c3394` and its two predecessors — ***the structural half.*** **`SILENT TYPE` reports none and `NO STAB` reports none**, and off-type overall sits at **42% against 2.7a's 45% baseline**. *The tool's first finding was that the premise had moved: the bestiary was already on coverage, so ranking on off-type percentage would have produced a list of nothing.* ***Eight of the thirteen were one fault*** — a two-type line whose last evolution drops the second type's whole vocabulary — **so most of the pass was restoration, not invention.** *The 41 thin openings are **T-41**, split out because the ticket itself asked for that* |
| **T-37** | ~~**`INVOKE` was only on two surfaces**~~ | this commit — *1.6's rule reached the battle log and the menu and nothing else.* **Now the map dialogue, the help system, the battle prompts and the TM descriptions.** ***Most `use` survived and that is the rule working***: a TM is an item, so *"I used TMs to teach good ROUTINES"* was already right. **Ten map blocks and three help blocks are frozen** because the word is the verb or the PC's own command. *Three false positives caught before writing — **"too scared to move"**, **"mimic my every move"** and **"just move to a new town"** — each one a phrase split across a line break, which is why the guard had to become per-BLOCK.* **A pre-existing 291px line in the matchup pane turned up on the way**, 43px past vanilla's own widest, shipped and never measured |
| **T-31** | ~~**`PC` → `PORT`**~~ | this commit — ***it was already done.*** *Of 23 remaining occurrences, 22 are comments, macro docs, C identifiers and asm labels.* **The one player-visible survivor was the EASY CHAT word**, which lived because `port_vocab` is deliberately fenced out of easy chat — *a name table it also learns from* |
| **T-32** | ~~**Nineteen `type word + DAEMON` lines**~~ | this commit — *124 candidates, not nineteen, and **36 of them were the type**: the gyms first, then SWARM, FLOW, FROZEN, CORRUPT, CONTEXT, ENTROPY and EMERGENT elsewhere.* **The chart claims were checked before the words changed** — ours is vanilla's plus one line, so every matchup taught was still true. ***~70 are the ENGLISH word and were left***, which is 1.2's actual point. **Route 9's pun was rebuilt on SWARM rather than left as a joke with nothing under it** |
| **T-29** | ~~**The flight, and the reading**~~ | this commit — ***`BIRTH ISLAND` → `THE ANNEX`***, *the only one of the twenty-two not named by a person who arrived: nobody arrives here, so the name came off a form.* **The flight has two entry points** so a player who reaches the Owl without the package is not stranded. ***The last scene moves here from the lab*** — 8.2a had her read it in a room she had been thrown out of. *She does not ask how you got here. She turns it over, asks one word, walks to the water and opens it facing away, and the script ends with her still facing away.* **Deoxys is turned off** |
| **T-30** | ~~**The gold is not holding**~~ | this commit — *the inversion is done by **order and nothing else**: the buried name is what you read first now and the gold one is last, and no line remarks on it.* **4.4 calls the leaf "not a gesture, a fact with a date", so repainting it would be a gesture** — the game taking a victory lap over a man it has spent forty hours refusing to sneer at. *Nobody touches the sign. It simply stops holding* |
| **T-28** | ~~**Brazen, the Owl — 4.24 staged**~~ | this commit — ***the player only ever hears one side***, which is not economy but the safest way to write it: **the machine's argument never has to be written down, so it can never say the thesis**, and the player infers it from what a scholar answers. *That is 4.24's own structure with Act 1 inverted.* **He is not a fool and he is not beaten** — the turn is not agreement, it is him noticing his own objection applies to him. ***The concession refuses the word twice before making it.*** Gate is a new `DaemonsPartyHasStarr` special, **party rather than caught**, because 4.34 says you *bring* the machine |
| **T-27** | ~~**The lab, post–Review Board: she is not there**~~ | this commit — ***the silence version.*** *Vanilla walks her up to your door and escorts you in; none of it happens.* **You come out of your house after the biggest thing you have done and for the first time nobody is waiting, and nothing says so** — done by leaving one scene var at a value the on-frame table has no entry for, so **no script was deleted and two of them simply have no way to run.** The GLOBAL INDEX is handed over by a man at a desk on being spoken to. ***The note is one bg_event with two states*** — the INDEX unit before, the note after — *so the wall it appears on is one the player has already read once, and the note itself never changes again.* **The 60-species gate went with the escort**, deliberately: an aide saying *you have not earned it yet* reinstates assessment at the moment 8.2a removes it |
| **T-23** | ~~**Sevii tier 3 — the place names**~~ | this commit — *the ticket said 35 places and the reading said three kinds. **A place carrying its island's number is one nobody named**, which is 8.2a's grace note, so those keep the number; **TANOBY and the seven chambers are transliterations of an alphabet 4.24 says nobody reads**, so translating them would translate the one thing whose point is that you cannot; and 2.10 leaves the two islands no player reaches. **That left 21 to name.** `tools/port_sevii.py` owns them and caught both breakages: **seven hand-written `sMapsecName_*` symbols**, and one swept line pushed past the box because `STILLFALL` is two characters longer than `ICEFALL`. **The prose half is T-26** |
| **T-09** | ~~**Two ERRATA cards from *The Painted Mirror*.**~~ | this commit — *the `DISPLAY UNIT` and the `SORTING FRAME`, on the one exhibit case on that floor that had no card at all. **It is wide enough for two and they are read from opposite sides**, so one is met coming in and one going out. The ticket said what was left was "choosing which display case" — **the choice was made by reading which blocks already had a card and finding the one that did not**, and the approach tiles came out of the layout's own `map.bin`. *The words were right the first time; only the line breaks were wrong, and three of nine ran past the box by six pixels* |
| **T-21** | ~~**The Tanoby chambers as 4.24's translations**~~ | this commit — *seven chambers, seven accounts of one event, and **the event is never named**. Nobody in them is lying and nobody is wrong, and it happened anyway. Placed by reading each chamber's own collision — a wall tile with a walkable one under it* |
| **T-19** | ~~**The Warehouse, both ends**~~ | this commit — *the package is `PAYLOAD`, out of `ITEM_LETTER`, which nothing in this game referenced and which was already a letter. **Both men are in the room and SCORN is facing the right way.** TY crosses to you; the walk is the characterisation. CRYSTAL turns it over, asks one word, crosses the room and opens it facing away — **and the script ends with her still facing away*** |
| **T-22** | ~~**The doctrine's room**~~ | this commit — *the scientist on SIX ISLAND's GREEN PATH, eight steps, one per visit, and the ninth clears the flags so he goes round again. **Every prohibition is an absence**, so the script carries the list of what is deliberately not there. `tools/gbamaptiles.py` was written to place him and unblocks T-09 on the way* |
| **T-02** | ~~**The MUSAI branch was 78% off-type**~~ | this commit — *100% in fact, all nineteen. `tools/port_musai.py` takes it to **37%**, under 2.7's 45% baseline, with two deliberate residuals a line. **`FALSIFY` on CODEMUSAI is the pass**: it breaks STEELMAN and PARAPHRASE, and CODEMUSAI exists to be LOGIC against CONTEXT. **S.T.A.R.R. was already at 25%** — the ticket's 78% was the thirteen's average carried onto a name that did not deserve it* |
| **T-08** | ~~**~154 `#MON` occurrences read singular**~~ | this commit — *POKéMON is its own plural; DAEMON is an ordinary noun and is not. **25 sentences force it** and were read one at a time; the rest are genuinely singular or attributive — "rare DAEMON fossils" is a compound noun the way "sheep dog" is* |
| **T-25** | ~~**`FIGHTING DOJO` carried a vanilla type word**~~ | this commit — *`PROOF HALL`. A dojo is where a discipline is practised and a **proof** is what LOGIC produces, so it is the same building said in our words — and narrower than what it replaced, which nothing else in this pass has been* |
| **T-07** | ~~**Forty-two `fight` occurrences**~~ | this commit — *three buckets, and the read was the job. Four were the TYPE said in lower case, eleven were 1.2's replaced verb, and the rest are people: an artist who is not a fighter, a fighting game in a shop, a pro fighter. It also turned up the help system's own copy of the chart* |
| **T-13** | ~~**The BERRY register**~~ | `c4786bd15` — *a berry is a HANDLER, so it is a TRAP, so the pouch is a TRAP TABLE. `src/berry.c` IS the second table the ticket warned about and is left alone: `BERRY_NAME_LENGTH` is six, and its only readers are ENIGMA (unobtainable) and BERRY CRUSH (link-only)* |
| **T-12** | ~~**The STREAM has no overworld notification**~~ | this commit — *nine told-flags out of T-17's block, and the same per-step hook the VS SEEKER and the egg use. Told, not seen: a show you skipped does not nag, and a new MARK still announces* |
| **T-24** | ~~**The A-to-Z picker sorted by vanilla's spellings**~~ | this commit — *`tools/port_ecsort.py` resolves every entry to the string the game will actually draw and re-buckets it. 26 of the 27 lists moved; 1,949 entries in and 1,949 out, and every `numWords` still matches its array — that count is elements, not words, so a marker counts two and a wrong one is an out-of-bounds read* |
| **T-14** | ~~**The USABLE items**~~ | `cddccf293` — *41 named, and 2.8's rule takes out more than half the bag: the drinks, the treasure, the mail, the tickets and the keys are things people own. ITEMFINDER is `GREP`, TOWN MAP is `SITEMAP`, VS SEEKER is `ROLL CALL`* |
| **T-20** | ~~**`RUBY` and `SAPPHIRE`**~~ | `12b5a2e5b` — *`PUBLIC KEY` and `PRIVATE KEY`. Which is which was decided by the plot: CORPUS steals the SAPPHIRE, and stealing a private key is a crime. Exposed `gExpandedPlaceholder_*`, the table behind the `{RUBY}` control code* |
| **T-04** | ~~**Dialogue naming a vanilla type**~~ | `f7f9c1abb` — *28 lines. The type names cannot be swept as WORDS — GRASS is grass almost everywhere — but "X-type" is unambiguous, so the CONSTRUCTION is the unit* |
| **T-15** | ~~**easy_chat's second copy of the vocabulary**~~ | this commit — *smaller than the directory looked: species and moves are stored as CONSTANTS and already read as ours, so only the 70 duplicated ability strings needed moving. Derived by `tools/port_easychat.py`, not listed* |
| **T-01** | ~~**`PC` → `PORT`**~~ | `087665ed5` — *66 places, not the 25 1.7 estimated. CRYSTAL CLEAR's row went 101px → 113 and clipped a 112px menu; the window went to sixteen tiles. Three help lines rewrapped* |
| **T-06** | ~~**`check_lexicon` passes on an empty file.**~~ **An absent README row is a fault now, not agreement.** *It had been reporting "the version agrees in all four places" while testing two of them, and it went quiet at exactly the moment the surface it watches had been destroyed* | this commit |
| **T-17** | ~~**Extend the flag space**~~ | `1c83e6787` — *1,024 flags out of `SaveBlock2`'s filler, so `encryptionKey` never moved and an old save still loads. Two `STATIC_ASSERT`s, both checked by breaking them* |
| **T-03** | ~~**The seven leaders' mechanics** — the parties, Doldrum's healing trainers and Scorn's fixed roll~~ | `4f94d3914` — *six parties rewritten, two mechanics in C, one gym script. GROWTH had no coverage and the design had to change shape rather than be dropped* (9.x, 5.3b) |
