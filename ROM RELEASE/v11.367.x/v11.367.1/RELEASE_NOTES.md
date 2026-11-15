# DAEMONS v11.367.1 — release notes

*Released 2026-11-14 20:24 · built against the design bible v11.367*

- **Engine**: CodeMusic/pokefirered-daemons `d1af1713e` (context-content)
- **Design**: CodeMusic/DAEMONS `8cf54e34`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `dc42e709926df92247dcb92dd4fc3a4333840a16` |
| `daemonsContext.gba` | CONTEXT | `7f6f753d208519d0716fdbe2a338ab9cea314a71` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `b2a818563d6472392e0037cab146d3c55daec815` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `9657472ae6cf25723631d805ed29c5e02eecf05a` |

## A note on the book audio

A minor release, released with two recordings deferred (the user, 2026-11-14: "Release now, record after"): THE COMPANION's and the new T-GLASSES book's.

## The engine since v11.366.1

- `d1af1713e` T-552, T-553: the ROVER line and all 24 MUSAI forms redrawn, built (DRAFT)
- `118873c80` README: the release line names v11.366.1

## The design and tools since v11.366.1

- `8cf54e34` TODO: T-552, T-553 name the engine commit as landed (d1af1713e, rebased onto v11.366.1)
- `16f38ca4` Bible v11.367: the field overlays in TERMINAL (T-561, v11.366.1)
- `1861a4b5` T-552, T-553: redraw the weak, then build -- the ROVER line and all 24 MUSAI forms in the ROM (engine c449f7717, DRAFT)
- `03bb88db` T-552, T-553: backs, icons and followers for all 27 at game size (the user: "Yes, draw them")
- `30137edb` TODO: T-562 filed -- the towns' last Nintendo tiles, batch 3 of the 2026-11-14 re-census (the user's pick)
- `b245cf4b` README and wiki Home name v11.366.1
- `e164ecf3` ROM release v11.366.1: T-561 the field overlays -- the trainer's ! as the follower's small screen (no longer yellow), the itemfinder's chevron, the quest log, recap bar, START banner and HELP in TERMINAL (DRAFT); seals v11.365.x; two recordings deferred

## The design bible's own entry for v11.367

### v11.367 — 2026-11-14

- Recorded from release v11.366.1 (e164ecf3, engine 9e489b46e), which sealed v11.365.x:
  - **The field overlays in TERMINAL** (T-561), the user's picks: the trainer's emote as a small screen (no longer yellow), the itemfinder's chevron, the quest log's frame and description bar, the START banner, the HELP screen. DRAFT.
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
