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

---

## Ready — decided, unblocked, nobody has done it

| | what | where | from |
|---|---|---|---|
| **T-33** | **`MOON STONE` wants a name.** *Tied to a place rather than a paradigm, so 8.2 held it for the town pass* — **and the town pass is done.** The stone is already written into 4.30, so the name has to survive a room that describes it | `engineGba`, items | 8.2, 4.30 |
| **T-34** | **The starter names are placeholders.** *2.7a retyped the three and 4.26 named thirty-two others around them, so they are now the least finished names in the game* — **and they are the first three the player reads** | `engineGba`, species | 8.2 |
| **T-26** | **Sevii tier 3b — the ~9,500 words.** 8.2a's tone rule, applied to a quarter of the game's map dialogue: *Kanto tells you what things are; the islands tell you how they look from where the speaker is standing.* ***The names are done (T-23) and they were the cheap half*** — 21 places, one tool, one afternoon. **This is 136 maps and 2,043 strings**, and 8.2a is explicit that it is *not a naming pass.* *Do it island by island; the vocabulary pass has already been through, so what is stale is register and plot, not words* | `engineGba/data/maps/`, 136 maps | 8.2a tier 3b |
| **T-16** | **Per-gym battle backdrops.** Eight benchmarks, eight rooms, one backdrop, and it is the one place decoration IS the argument: 5.3 gives each gym a lever and the backdrop can be the room you met it in. ***Costed wrong when it was proposed** — "ROM-only, cheap" is true of the BYTES and false of the work.* **Gen 3 keys the backdrop off ten TERRAIN types, each a full tileset, tilemap and palette in `graphics/battle_terrain/`** — so reassigning an existing one per gym is a data change, and eight gym-specific ones is **eight new tilesets**. *Decide which of the two before starting* | `graphics/battle_terrain/`, `src/battle_bg.c` | 5.3, 9.4 |
| **T-36** | **`WIP — worktree-t36-coherence`.** **The daemon × type × routine coherence sweep.** 2.7a did this for three lines out of seventy-two, by hand, and found the seam: *the retyped thirteen were **78% off-type** against a **45%** baseline.* **The other sixty-nine have never been looked at**, and the question is no longer off-type percentage — *that is measurable and mostly fine* — but whether **a daemon's routines read as things THAT daemon would do.** ECHO invoking REFLECT is right because ECHO is a thing that navigates by reply; nothing has checked whether HEAP, MUTEX or STUB are as lucky. ***Wants a tool, not a conversation***: print each daemon with its types and its full learnset, flag the routines that are off-type AND off-concept, and let a human read the flags. `port_starters.py` is the pattern for the fix once the list exists | `tools/`, new · `level_up_learnsets.h` | 2.7, 2.7a |
| **T-37** | **`WIP — main`.** **`INVOKE` is only on two surfaces.** 1.6 now rules that **a ROUTINE is INVOKED and an ITEM is USED**, and the battle log was corrected to match the menu — *but nothing has swept the rest of the game for the old verb.* **Dialogue, the STREAM's lessons, the help system and the Index all pre-date the rule**, and *"use a move"* in an NPC's mouth is now wrong in a way nothing checks. **The trap is that `use` is also correct constantly** — you use an item, use a BOX, use the PORT — so this is a human read, not a substitution. ***Counted 2026-09-10: 20 dialogue strings pair a use-verb with `move`/`ROUTINE`***, and most also still say `move` where 1.6 says ROUTINE — *"it can still use moves like CUT"*, *"lets you use the move ROCK SMASH"* — **so this ticket and the `move` → `ROUTINE` prose pass are the same read, done once** | `engineGba/data/`, `src/data/text/` | 1.6 |
| **T-35** | **Re-port the harness after every name pass.** *`mappings.json` went stale by **80 species, 266 routines and 121 items** in a single day* — that is the table the agent reads every name out of. **`port_gamedata.py` is one command, and it belongs inside a rename rather than after one.** *`check_agent_vocab` now catches the prompt half; the mappings half still relies on someone running it* | `tools/port_gamedata.py` | this review |
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
