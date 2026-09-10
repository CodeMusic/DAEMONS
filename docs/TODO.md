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
| **T-01** | **`PC` → `PORT`.** Four menu strings and ~25 dialogue lines. `\nPC` has no word boundary in front of it, so this is a `port_vocab.py` pass with a flattened match, **not a hand edit** — the half-rename is the failure this project has already had twice | `engineGba`, `tools/port_vocab.py` | 1.7 |
| **T-02** | **The Musai branch and STARR are still 78% off-type.** The three starters were curated (2.7a); the same treatment is owed to the other four of the thirteen retyped. `tools/port_starters.py` is the pattern to copy | `tools/`, `level_up_learnsets.h` | 2.7a |
| **T-03** | **The seven leaders' mechanics.** 5.3 designed what an overlevelled player still runs into; 5.3a put the names and 127 lines in the ROM. **The parties, Doldrum's healing trainers and Scorn's fixed roll are unbuilt** | `engineGba` trainer data | 5.3, 5.3a |
| **T-04** | **Dialogue lines still naming a vanilla type** — *"a GRASS-type DAEMON"*. **Counted 2026-09-10: 27 lines across 14 maps**, not the nineteen the Open log remembers. Nearly all in gyms. *Was held until 5 settled the Benchmark leaders — **5 has settled**, so this is unblocked* | `engineGba/data/maps/*/text.inc` | 1.2 |
| **T-05** | **Callow and The Bleed share their music** with other maps, so 8.1's second theme needs new `songs.asm` entries before it can be given one | `engineGba`, `songs.asm` | 7.3 |
| **T-07** | **Forty-two `fight` occurrences** want a human read — some are the replaced verb, some are people | `engineGba` | 1.2 |
| **T-08** | **~154 `#MON` occurrences** read singular by default and want a human read **on screen, not in the source** | `engineGba` | 1.2 |
| **T-13** | **The Warehouse, both ends.** 8.2a's Act 2 is written and four of its scenes are in the ROM; **these two are not.** Scorn and Ty in one room and *Scorn does not recognise him*; **Ty approaches and hands over the package**; and Crystal reads it, which is the last scene. *The package needs to exist as an item or a flag before either end can be written* | `engineGba`, Five Island + Blanche | 8.2a |
| **T-14** | **`RUBY` and `SAPPHIRE` are still vanilla**, and they are the post-game's two MacGuffins — *the two halves of a bridge between systems built apart*, which is the edition split made literal. Celio and the Network Machine scene go with them | `engineGba/src/data/items.json`, One Island | 8.2a |
| **T-15** | **The Tanoby chambers as 4.24's translations.** Seven Braille chambers, seven accounts of one event, and the *translation* is what you can read once you have been the other people. **The vehicle is already built** — Braille is text you cannot read until you hold the key | `engineGba`, Seven Island | 8.2a, 4.24 |
| **T-16** | **The doctrine's room.** 4.33's scene and its six prohibitions: he is already talking when you walk in, no dialogue choice, you may leave mid-sentence, and **nothing in the game agrees or disagrees with him afterwards.** *The test is one line: delete him, and see whether anything else changes* | `engineGba`, an island | 4.33 |

---

## Blocked — decided, but something has to happen first

| | what | blocked on | from |
|---|---|---|---|
| **T-09** | **Two ERRATA cards from *The Painted Mirror*** — *a door that stopped being a door and went back to being lines*, and *a pattern read as a purpose*. Both are Benchmark 1's subject and both fit the `KNOWN FAULT:` format already in the room | **No free sign slot.** Slate museum 1F has four `bg_events` — two CORE cards, two HEARSAY journal entries; 2F's eight all point at the shuttle or the moon stone. Needs new `bg_events` in `map.json`, which needs knowing which tiles are display cases | lineage 3b |
| **T-10** | **The missing key signature as a puzzle** — notes reading flat because the key is absent, and giving them the key lifts them. **2.6's one-clause test for CONTEXT as a room rather than a definition**, and 5.3 names *the room* as one of four levers a grinder cannot grind | Wants **Brazen gym**, which is T-03's territory. Sequence it after | lineage 3b, 5.3 |
| **T-11** | **The 87 unreachable routines.** 2.10 renamed 269 of 356 — every routine the player can meet in this game | The rest wait on **the bestiary**, not on a decision | 2.10 |
| **T-12** | **The STREAM has no overworld notification.** The host reports unseen shows only once you are already watching one, and the item description carries the rule | Wants a **map object with a script** | 9.16 |
| **T-17** | **Sevii tier 3** — 35 place names, and ~9,500 words rewritten to 8.2a's tone rule: *Kanto tells you what things are; the islands tell you how they look from where the speaker is standing* | **Tiers 1 and 2 being in play.** 8.2a's own condition, and the same one the original deferral used — *8 exists because the graveyard is full of projects that designed 151 creatures and shipped zero towns* | 8.2a |

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

## Closed

| | what | closed by |
|---|---|---|
| **T-06** | ~~**`check_lexicon` passes on an empty file.**~~ **An absent README row is a fault now, not agreement.** *It had been reporting "the version agrees in all four places" while testing two of them, and it went quiet exactly when the surface it watches had been destroyed* | this commit |
