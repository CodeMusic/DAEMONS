# DAEMONS v11.373.1 — release notes

*Released 2026-11-15 18:01 · built against the design bible v11.373*

- **Engine**: CodeMusic/pokefirered-daemons `4c2c60d81` (context-content)
- **Design**: CodeMusic/DAEMONS `e6a3516a`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `4766e8f00c889f02c09a92734cf14f35b0e6d4aa` |
| `daemonsContext.gba` | CONTEXT | `df8fdbfb7a88a1fc71dbe23e23ca0c000bc22618` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `4b3557574a502a57e5da7483ccb66bc65163a055` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `c91f8da8ae1220ff15bf32e8efe2fe6fd7bc9976` |

## The engine since v11.372.1

- `4c2c60d81` T-569: THE TUNNEL back as gbadwellings drew it (its tiles only looked like pret's), and the cave battle background regenerated from the new stones (gbabattleart --write --approved --all)
- `1c758c2e3` T-569: the islands and the caves -- the island kit on SIX/SEVEN, ONE-THREE, FOUR/FIVE, the harbours and DENSE WOOD, each cave's stones in its own grain, MT. SMOULDER's banked steam; THE BLACKOUT kept as T-546 drew it (the user's picks, DRAFT; tools/gbaislands.py)
- `79922dc95` README: the release line names v11.372.1

## The design and tools since v11.372.1

- `e6a3516a` T-569: gbabattleart's cave draft follows the regenerated background
- `f2e9f90e` T-569: THE TUNNEL left to gbadwellings, the cave battle background follows the stones; gbalandmarkrooms knows gbaislands
- `5691c339` T-569 BUILT: the islands and the caves, the user's picks, THE BLACKOUT kept (engine 1c758c2e3); T-570 the 134 single-index tiles left
- `a74ae16d` T-569 DRAFTED: the islands and the caves -- the Nintendo tiles they still draw (batch 8)
- `3810c455` TODO: T-569 the islands and the caves (batch 8, the user's pick)
- `d630d996` Bible v11.373: the new game and the name (T-568, v11.372.1)
- `0e05cce2` README and wiki Home name v11.372.1
- `da8b0dd3` ROM release v11.372.1: T-568 the new game and the name -- keycaps in the controls guide, the panel's graph paper with a quaver, CRYSTAL's graph-paper floor and pad, the naming screen's brackets, prompt and keycaps (DRAFT); seals v11.371.x; two recordings deferred

## The design bible's own entry for v11.373

### v11.373 — 2026-11-15

- Recorded from release v11.372.1 (da8b0dd3, engine 80271363f), which sealed v11.371.x:
  - **The new game and the name** (T-568), the user's picks: keycaps in the controls guide, CRYSTAL's graph-paper floor and pad, SEEKMUSAI's panel with a quaver, the naming screen's keycaps, brackets, prompt and terminal icon. DRAFT.
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
