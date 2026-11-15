# DAEMONS v11.374.1 — release notes

*Released 2026-11-15 18:34 · built against the design bible v11.374*

- **Engine**: CodeMusic/pokefirered-daemons `46045ed22` (context-content)
- **Design**: CodeMusic/DAEMONS `5626221e`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `3aa05e58698c6877c73d8ca6ef6417bd3cec49f2` |
| `daemonsContext.gba` | CONTEXT | `2e41485344b19852248f5a4f518488eebbfb3e79` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `a61c426db92999cc2a719deaa5d0d2af838ceda0` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `607099c782e095dce92e34bfcc3fba83ccd13b98` |

## The engine since v11.373.1

- `46045ed22` T-567: a MOVE is a ROUTINE in the learning lines -- the relearner's give-up, a routine not learned, four ROUTINES in battle (reworded to fit, DRAFT), none left, STRATUM routines missing, RECYCLE's description
- `e9f550dfd` README: the release line names v11.373.1

## The design and tools since v11.373.1

- `5626221e` T-567 DONE: a MOVE is a ROUTINE in the learning lines (engine 46045ed22), ROUTINE_TALK in port_vocab; T-571 port_vocab has no drift guard
- `bd38f003` Bible v11.374: the islands and the caves (T-569, v11.373.1)
- `d828b131` README and wiki Home name v11.373.1
- `4afad1f6` ROM release v11.373.1: T-569 the islands and the caves -- the island kit, each cave's stones in its own grain, MT. SMOULDER's banked steam, the cave battle background to match; THE BLACKOUT and THE TUNNEL kept (DRAFT); seals v11.372.x; two recordings deferred

## The design bible's own entry for v11.374

### v11.374 — 2026-11-15

- Recorded from release v11.373.1 (4afad1f6, engine 1c758c2e3 + 4c2c60d81), which sealed v11.372.x:
  - **The islands and the caves** (T-569), the user's picks: the island kit, each cave's own grain, MT. SMOULDER's banked steam, the cave battle background to match; THE BLACKOUT kept. DRAFT. 9.29, beside the towns.
  - The last of the 2026-11-14 re-census's eight batches; T-570 holds the single-index tiles left.
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
