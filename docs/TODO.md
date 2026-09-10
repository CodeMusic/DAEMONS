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
| **T-06** | **`check_lexicon` passes on an empty file.** Its README check reads the *working* and *snapshot at v* rows; with no rows it finds no disagreement and reports agreement. **`docs/README.md` was zero bytes twice in two days and the check agreed with it both times.** *Reproduced 2026-09-10: emptied the file, ran the check, got "the version agrees in all four places."* **A check that cannot fail on a missing input is not checking that input** | `tools/check_lexicon.py` | this file's own history |
| **T-07** | **Forty-two `fight` occurrences** want a human read — some are the replaced verb, some are people | `engineGba` | 1.2 |
| **T-08** | **~154 `#MON` occurrences** read singular by default and want a human read **on screen, not in the source** | `engineGba` | 1.2 |

---

## Blocked — decided, but something has to happen first

| | what | blocked on | from |
|---|---|---|---|
| **T-09** | **Two ERRATA cards from *The Painted Mirror*** — *a door that stopped being a door and went back to being lines*, and *a pattern read as a purpose*. Both are Benchmark 1's subject and both fit the `KNOWN FAULT:` format already in the room | **No free sign slot.** Slate museum 1F has four `bg_events` — two CORE cards, two HEARSAY journal entries; 2F's eight all point at the shuttle or the moon stone. Needs new `bg_events` in `map.json`, which needs knowing which tiles are display cases | lineage 3b |
| **T-10** | **The missing key signature as a puzzle** — notes reading flat because the key is absent, and giving them the key lifts them. **2.6's one-clause test for CONTEXT as a room rather than a definition**, and 5.3 names *the room* as one of four levers a grinder cannot grind | Wants **Brazen gym**, which is T-03's territory. Sequence it after | lineage 3b, 5.3 |
| **T-11** | **The 87 unreachable routines.** 2.10 renamed 269 of 356 — every routine the player can meet in this game | The rest wait on **the bestiary**, not on a decision | 2.10 |
| **T-12** | **The STREAM has no overworld notification.** The host reports unseen shows only once you are already watching one, and the item description carries the rule | Wants a **map object with a script** | 9.16 |

---

## Wants a decision first — these are Open log items, listed only so the trail is here

*Do not work these. They are questions, and the answer belongs in `vision.md`.*

- **THRASHING's ownership** — is *"the state no type owns"* the point, or does it want LOGIC? (2.7)
- **THROTTLED's five strays** — SIGNAL owns it six to five (2.7)
- **SUSPENDED's six sleep moves** — CONTEXT owns the concept; retyping the moves is a balance question (2.7)
- **`PKRS` still says PKRS** — the condition has no place in the lexicon yet (9.15)
- **`LEGACY` → `RUST` and `VECTOR` → `FLOAT`** — a gym, a museum and a badge each (8.7)
- **Re-score the one-clause test at 17 types** — CONTEXT's 8/8 was scored without OPAQUE (8.7)

---

## Closed

*Nothing yet. Strike a ticket through here with the commit that closed it, and
leave it where it is.*
