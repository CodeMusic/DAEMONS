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
| **T-04** | **Dialogue lines still naming a vanilla type** — *"a GRASS-type DAEMON"*. **Counted 2026-09-10: 27 lines across 14 maps**, not the nineteen the Open log remembers. Nearly all in gyms. *Was held until 5 settled the Benchmark leaders — **5 has settled**, so this is unblocked* | `engineGba/data/maps/*/text.inc` | 1.2 |
| **T-05** | **Callow and The Bleed share their music** with other maps, so 8.1's second theme needs new `songs.asm` entries before it can be given one | `engineGba`, `songs.asm` | 7.3 |
| **T-12** | **The STREAM has no overworld notification.** The host reports unseen shows only once you are already watching one, and the item description carries the rule. ***Unblocked by T-17*** — there are a thousand flags now | `engineGba`, a map object with a script | 9.16 |
| **T-13** | **The BERRY register.** Forty-three names, a bag pocket, the category word, and a **second name table** in `src/data/berries.h`. A berry is a **handler** — a one-shot that fires on a condition — and the register was derived in 1.6c but not spent. *Renaming only the item strings would leave three surfaces disagreeing, which is 1.7's half-rename failure* | `engineGba`, `tools/port_item_text.py` | 1.6c |
| **T-14** | **The USABLE items are still vanilla** — `REPEL`, `ESCAPE ROPE`, `POKé DOLL`, the vitamins. 1.6 named the ten that undo a state and stopped there | `engineGba/src/data/items.json` | 1.6, 1.6c |
| **T-15** | **`src/data/easy_chat/` keeps a SECOND copy of the vocabulary** — ability, move and species words across twenty-four files, **none of which any naming pass has touched.** `ABILITY_CACOPHONY` is `NO CHANNEL` in `abilities.h` and still `MAGNET PULL` there. *Fenced out of `port_vocab` on 2026-09-10 because a partial sweep of a name table is worse than none* | `engineGba/src/data/easy_chat/` | 1.6c |
| **T-16** | **Per-gym battle backdrops.** Eight benchmarks, eight rooms, one backdrop, and it is the one place decoration IS the argument: 5.3 gives each gym a lever and the backdrop can be the room you met it in. ***Costed wrong when it was proposed** — "ROM-only, cheap" is true of the BYTES and false of the work.* **Gen 3 keys the backdrop off ten TERRAIN types, each a full tileset, tilemap and palette in `graphics/battle_terrain/`** — so reassigning an existing one per gym is a data change, and eight gym-specific ones is **eight new tilesets**. *Decide which of the two before starting* | `graphics/battle_terrain/`, `src/battle_bg.c` | 5.3, 9.4 |
| **T-07** | **Forty-two `fight` occurrences** want a human read — some are the replaced verb, some are people | `engineGba` | 1.2 |
| **T-08** | **~154 `#MON` occurrences** read singular by default and want a human read **on screen, not in the source** | `engineGba` | 1.2 |
| **T-19** | **The Warehouse, both ends.** 8.2a's Act 2 is written and four of its scenes are in the ROM; **these two are not.** Scorn and Ty in one room and *Scorn does not recognise him*; **Ty approaches and hands over the package**; and Crystal reads it, which is the last scene. *The package has to exist as an item or a flag before either end can be written* | `engineGba`, Five Island + Blanche | 8.2a |
| **T-20** | **`RUBY` and `SAPPHIRE` are still vanilla**, and they are the post-game's two MacGuffins — *the two halves of a bridge between systems built apart*, which is the edition split made literal. Celio and the Network Machine scene go with them | `engineGba/src/data/items.json`, One Island | 8.2a |
| **T-21** | **The Tanoby chambers as 4.24's translations.** Seven Braille chambers, seven accounts of one event, and the *translation* is what you can read once you have been the other people. **The vehicle is already built** — Braille is text you cannot read until you hold the key | `engineGba`, Seven Island | 8.2a, 4.24 |
| **T-22** | **The doctrine's room.** 4.33's scene and its six prohibitions: he is already talking when you walk in, no dialogue choice, you may leave mid-sentence, and **nothing in the game agrees or disagrees with him afterwards.** *The test is one line — delete him, and see whether anything else changes* | `engineGba`, an island | 4.33 |

---

## Blocked — decided, but something has to happen first

| | what | blocked on | from |
|---|---|---|---|
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
| **T-01** | ~~**`PC` → `PORT`**~~ | `087665ed5` — *66 places, not the 25 1.7 estimated. CRYSTAL CLEAR's row went 101px → 113 and clipped a 112px menu; the window went to sixteen tiles. Three help lines rewrapped* |
| **T-06** | ~~**`check_lexicon` passes on an empty file.**~~ **An absent README row is a fault now, not agreement.** *It had been reporting "the version agrees in all four places" while testing two of them, and it went quiet at exactly the moment the surface it watches had been destroyed* | this commit |
| **T-17** | ~~**Extend the flag space**~~ | `1c83e6787` — *1,024 flags out of `SaveBlock2`'s filler, so `encryptionKey` never moved and an old save still loads. Two `STATIC_ASSERT`s, both checked by breaking them* |
| **T-03** | ~~**The seven leaders' mechanics** — the parties, Doldrum's healing trainers and Scorn's fixed roll~~ | `4f94d3914` — *six parties rewritten, two mechanics in C, one gym script. GROWTH had no coverage and the design had to change shape rather than be dropped* (9.x, 5.3b) |
