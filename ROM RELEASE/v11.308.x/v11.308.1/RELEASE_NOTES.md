# DAEMONS v11.308.1 — release notes

*Released 2026-10-21 11:20 · built against the design bible v11.308*

- **Engine**: CodeMusic/pokefirered-daemons `efc3c3d9a` (context-content)
- **Design**: CodeMusic/DAEMONS `529d5c39`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `e23cc229f5b83ce48755520c6b8493c89e787622` |
| `daemonsContext.gba` | CONTEXT | `15dd0112d7faf014daf327c667fe745dfc0c2090` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `ee5d2fcec7035649590c8331fbf3ae2d0557af53` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `563c7e8c477b66e2b576ce3866cce372292b79e9` |

## The engine since v11.307.3

- `efc3c3d9a` T-18 P3: THE FOLLOWER's edge cases, shiny colours, one box a press

## The design and tools since v11.307.3

- `529d5c39` T-18 P3 built (engine efc3c3d9a), T-18 struck: the follower's edge cases, shiny colours, one box a press
- `17cd86d6` TODO: T-431's 16 behaviour lines approved
- `0efed1e7` TODO: T-431 planned, the user's eight answers recorded
- `6b4f6775` Bible v11.308: what you bring keeps its colour in Halftone (8.6a revised, T-430); feelings in the game, never named (4.9, T-431); TODO T-430, T-431
- `1c446fa8` TODO: T-18 P2 released v11.307.3; the user's answers -- one box alternating, item hint kept, emotion emoji and a SUMMARY page, colour in HALFTONE (planning)
- `c3998df2` qa: T-18 P2 talking to the follower
- `da8cbca2` ROM release v11.307.3: talk to your follower -- a line by friendship and one by mood, with a bubble (T-18 P2, DRAFT)

## The design bible's own entry for v11.308

### v11.308 — 2026-10-21

### What you bring keeps its colour (T-430)

- ***8.6a revised (the user)***: **in Halftone you, your daemons, your follower and your own routines' effects keep their colour**; *an effect fades as it crosses and splashes a little colour onto the grey daemon it hits.* **Menus, windows, banners and text stay grey, as do the town and the other side.** *DAEMON TOWER returns to colour floor by floor once INIT is rescued; the town stays grey, and on first sight it tries to flash into colour and fails.* Logged in Reversed and Settled.

### Feelings in the game (T-431)

- ***4.9's affect model extended (the user)***: **the game derives GLAD, MAD, SAD and CALM-AFRAID from play, as the companion does (C-120), with friendship as a fifth value** -- *shown as the follower's daemon-emoji, a new SUMMARY page (a grid, colour the third dimension, unlabelled) and a line of behaviour; never named, never a status.*

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
