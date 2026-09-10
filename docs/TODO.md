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

---

## Ready — decided, unblocked, nobody has done it

| | what | where | from |
|---|---|---|---|
| **T-02** | **The Musai branch and STARR are still 78% off-type.** The three starters were curated (2.7a); the same treatment is owed to the other four of the thirteen retyped. `tools/port_starters.py` is the pattern to copy | `tools/`, `level_up_learnsets.h` | 2.7a |
| **T-16** | **Per-gym battle backdrops.** Eight benchmarks, eight rooms, one backdrop, and it is the one place decoration IS the argument: 5.3 gives each gym a lever and the backdrop can be the room you met it in. ***Costed wrong when it was proposed** — "ROM-only, cheap" is true of the BYTES and false of the work.* **Gen 3 keys the backdrop off ten TERRAIN types, each a full tileset, tilemap and palette in `graphics/battle_terrain/`** — so reassigning an existing one per gym is a data change, and eight gym-specific ones is **eight new tilesets**. *Decide which of the two before starting* | `graphics/battle_terrain/`, `src/battle_bg.c` | 5.3, 9.4 |
| **T-19** | **The Warehouse, both ends.** 8.2a's Act 2 is written and four of its scenes are in the ROM; **these two are not.** Scorn and Ty in one room and *Scorn does not recognise him*; **Ty approaches and hands over the package**; and Crystal reads it, which is the last scene. *The package has to exist as an item or a flag before either end can be written* | `engineGba`, Five Island + Blanche | 8.2a |
| **T-21** | **The Tanoby chambers as 4.24's translations.** Seven Braille chambers, seven accounts of one event, and the *translation* is what you can read once you have been the other people. **The vehicle is already built** — Braille is text you cannot read until you hold the key | `engineGba`, Seven Island | 8.2a, 4.24 |
| **T-22** | **The doctrine's room.** 4.33's scene and its six prohibitions: he is already talking when you walk in, no dialogue choice, you may leave mid-sentence, and **nothing in the game agrees or disagrees with him afterwards.** *The test is one line — delete him, and see whether anything else changes* | `engineGba`, an island | 4.33 |

---

## Blocked — decided, but something has to happen first

| | what | blocked on | from |
|---|---|---|---|
| **T-05** | **Callow and The Bleed share their music.** *8.1's second theme cannot be given to either until they have a slot of their own* | **A track that does not exist yet.** *Re-read 2026-09-10 and the ticket was aimed at the wrong repo:* `data/maps/songs.asm` is the **Game Boy** build, which CLAUDE.md says is a reference and not updated further. **On the GBA it is one field in a map's `.json`** — so the plumbing is not the blocker at all. `song-status.md` lists eleven compositions still unassigned, and this wants one of them | 7.3, 8.1 |
| **T-09** | **Two ERRATA cards from *The Painted Mirror*** — *a door that stopped being a door and went back to being lines*, and *a pattern read as a purpose*. Both are Benchmark 1's subject and both fit the `KNOWN FAULT:` format already in the room | **No free sign slot.** Slate museum 1F has four `bg_events` — two CORE cards, two HEARSAY journal entries; 2F's eight all point at the shuttle or the moon stone. Needs new `bg_events` in `map.json`, which needs knowing which tiles are display cases | lineage 3b |
| **T-10** | **The missing key signature as a puzzle** — notes reading flat because the key is absent, and giving them the key lifts them. **2.6's one-clause test for CONTEXT as a room rather than a definition**, and 5.3 names *the room* as one of four levers a grinder cannot grind | Wants **Brazen gym**, which is T-03's territory. Sequence it after | lineage 3b, 5.3 |
| **T-11** | **The 87 unreachable routines.** 2.10 renamed 269 of 356 — every routine the player can meet in this game | The rest wait on **the bestiary**, not on a decision | 2.10 |

| **T-23** | **Sevii tier 3** — 35 place names, and ~9,500 words rewritten to 8.2a's tone rule: *Kanto tells you what things are; the islands tell you how they look from where the speaker is standing* | **Tiers 1 and 2 being in play.** 8.2a's own condition, and the same one the original deferral used — *8 exists because the graveyard is full of projects that designed 151 creatures and shipped zero towns* | 8.2a |

---

## Wants a decision first — these are Open log items, listed only so the trail is here

*Do not work these. They are questions, and the answer belongs in `vision.md`.*

- **THRASHING's ownership** — is *"the state no type owns"* the point, or does it want LOGIC? (2.7)
- **THROTTLED's five strays** — SIGNAL owns it six to five (2.7)
- **SUSPENDED's six sleep moves** — CONTEXT owns the concept; retyping the moves is a balance question (2.7)
- **`PKRS` still says PKRS** — the condition has no place in the lexicon yet (9.15)
- **`LEGACY` → `RUST` and `VECTOR` → `FLOAT`** — a gym, a museum and a badge each (8.7)
- **The doctrine's placement, his name, and whether the doctrine has a name** — *not after a type*; `SWARM` is its own step 5's word and `check_lexicon` would catch it (4.33)
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
