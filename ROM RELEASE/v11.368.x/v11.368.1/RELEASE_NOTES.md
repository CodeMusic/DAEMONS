# DAEMONS v11.368.1 — release notes

*Released 2026-11-14 21:13 · built against the design bible v11.368*

- **Engine**: CodeMusic/pokefirered-daemons `0dabcb96e` (context-content)
- **Design**: CodeMusic/DAEMONS `d2266d3f`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `bf4575489a0adde97396c240c74a843cdc3737e4` |
| `daemonsContext.gba` | CONTEXT | `e7f1f36df6b8d70d0929f806c96c7ae4f169931f` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `451f35528fef0f6a5b7a40b316c3027233e75e83` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `7095e1f80b865aba4f6bde8c67824bb78a9cd19e` |

## A note on the book audio

A minor release, released with two recordings deferred (the user, 2026-11-14: "Release now, record after"): THE COMPANION's and the new T-GLASSES book's.

## The engine since v11.367.1

- `0dabcb96e` T-562: the towns' last pret tiles, redrawn in each town's own look (DRAFT)
- `7955b7bea` README: the release line names v11.367.1

## The design and tools since v11.367.1

- `d2266d3f` T-562 BUILT (engine 0dabcb96e): the towns' last pret tiles, the user's picks -- 309 tiles and the fountain
- `12dbb3cb` Bible v11.368: the ROVER line and the MUSAI creatures (T-552, T-553, v11.367.1)
- `c94a2c7f` T-562 DRAFTED: the towns' last pret tiles -- gbatownslast.py (APPROVED empty), drafts and sheets
- `a753ac90` README and wiki Home name v11.367.1
- `c2ef44c1` ROM release v11.367.1: T-552/T-553 the ROVER line and all 24 MUSAI forms redrawn, with their backs, icons and followers (the Rover lane, DRAFT); seals v11.366.x; two recordings deferred

## The design bible's own entry for v11.368

### v11.368 — 2026-11-14

- Recorded from release v11.367.1 (c2ef44c1, engine d1af1713e), which sealed v11.366.x:
  - **The ROVER line, one flow again** (T-552): the cub most machine, the seer a seated server on a rack chassis, the byte a white-furred dog. 9.31.
  - **The MUSAI branch, creature first** (T-553): all 24 forms natural creatures keeping MUSAI's head, each season's vehicle as anatomy. 9.34.
  - Both DRAFT; section 10, one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
