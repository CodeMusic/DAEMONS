# DAEMONS v11.285.1 — release notes

*Released 2026-09-25 03:45 · built against the design bible v11.285*

- **Engine**: CodeMusic/pokefirered-daemons `72430c16c` (context-content)
- **Design**: CodeMusic/DAEMONS `f5f9a850`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `6fef3f21a038944c6c56455eaab8df33afaf8b0f` |
| `daemonsContext.gba` | CONTEXT | `664e40ef4cf029055f2798351de1768108179401` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `144a073df31488e1c6aaa80c49d574cf36e05080` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `abbfefbf05c684cdb7ef731046c7805226423e9d` |

## The engine since v11.284.1

- `72430c16c` T-300..T-302: THE PROGRAMMER'S GUIDE TO THE HUMAN MIND, found on ONE ISLAND

## The design and tools since v11.284.1

- `f5f9a850` T-305..T-308 closed onto the clock session's T-269..T-272; the Guide on the field-test page
- `634696e9` v11.285: The Programmer's Guide to the Human Mind, found on the islands (4.36)
- `d1a538f7` Claim T-300..T-311: the Programmer's Guide in the game, and what reading it suggested
- `0821a509` ROM release v11.284.1: day and night, reading in battle, the STREAM badge; v11.283.x sealed

## The design bible's own entry for v11.285

### v11.285 — 2026-09-25

### The Programmer's Guide to the Human Mind, found

- ***The user's own book, recovered from `docs/archive/`, is in the game*** (4.36, T-300–T-303): **a key item, `GUIDE`, on the bookshelf in ONE ISLAND's second house** — *the islands' direction (0.6) as one volume, found and never handed over, because 4.3 says method is what survives a handoff.* **Its cover first, then CONTENTS — the sections on the left page, their chapters on the right — then each chapter across the spread**, *in the TEXTBOOK's reader with its own colours and its own cover, drawn from the PDF's.* ***137 pages became 28 entries of about a hundred words***, **printed under four rules** — *about people; only ever "like"; the process, never the pathology; no substance named* — **which `tools/genguide.py` checks word by word.** *Every word is DRAFT until the user approves it.*
- ***Two cuts made writing it***: **the seven centres' colours** (*beside Chapter 9's wrath and envy they tie a colour to a feeling, craft rule 1's one absolute*) **and the glossary's "proto-consciousness"** (*it asserts the machine half*).
- ***`lineage.md` 3c***: **the Guide is a primary source for the thesis** — *Chapter 3 is "Emotions as Contextual Information", Chapter 11 has thoughts as data and feelings as the context that changes how it is read* — **and eight things the game already had are in it**, *from the REMNANT's loop to the ROOTBOX's root access.*
- ***What reading it opened, each the user's to rule on*** (T-304–T-311; *T-305–T-308 turned out to be the clock session's T-269–T-272, logged minutes earlier, and are closed onto them*): **understandings written into its margins; its seven-day table for the day-of-week banner** (*MONDAY's orange 17.3 from ENTROPY*); **the brain and the tabs the user asked for on the USER card, both meeting T-252's "never counted"**; **a dream sign in the unread cave; the case studies as islanders; the REVIEW BOARD's copy with its ethics cut out.**
- ***And one housekeeping rule***: **two sessions cannot both take "the next id"**, *so `TODO.md` can reserve a block in one line and `check_lexicon` reads it* — **T-267 to T-299 for the clock session, T-300 up for this.**

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
