# DAEMONS v11.412.9 — release notes

*Released 2026-11-22 19:13 · built against the design bible v11.412*

- **Engine**: CodeMusic/pokefirered-daemons `a76bb5d5c` (context-content)
- **Design**: CodeMusic/DAEMONS `70a1c1b6`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `58db574c0d1d4b969083d1e5df347bb1cc346457` |
| `daemonsContext.gba` | CONTEXT | `cdc790bc73ebc51d77868e05b9a2a87d261de0a8` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `d1dd9127e5b7e3a70b0615053068b71a301c10fe` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `88e319764869ac9baccce11c1f99153cf7a0cf4f` |

## The engine since v11.412.8

- `a76bb5d5c` T-604: stage 2 -- twelve more later forms colour in as they learn their part: a region in the new part's colours (RELAY's green neck, BROADCAST's gold flight feathers, OVERFLOW's golden coat, FLOOD's kingfisher-blue wings, INDEXER's vermilion VECTOR forewing tips, SURGE's amber tail and saddle, TRACER's amber wings, STACK's rust boulder arms, SMOGSTACK's yellow smog, ESCALATE's salmon VECTOR belly, SCHEDULER's STRATUM pads and chest plate, ANOMALY's gold horns and wings), DRAFT
- `bff3f856b` README: latest is v11.412.8

## The design and tools since v11.412.8

- `70a1c1b6` Merge branch 't604s2'
- `29621273` gencasino.py: read the companion's slots.ts from server/src/game/ (C-428 moved it), the old place for a checkout from before
- `dd65cc16` T-604: stage 2 -- twelve later forms colour in as they learn their part (engine a76bb5d5c, companion b9d326fd), DRAFT
- `20716e3e` T-604 (draft): stage 2 -- twelve more later forms get a region in their new part's colours
- `cb36ffe2` qa: T-604 stage 1, the nine later forms, built (v11.412.8)
- `cbccb3d4` README and wiki: latest is v11.412.8
- `2dd98373` ROM release v11.412.8: T-604 stage 1 (nine later forms colour in as they learn their part) and T-602 shiny songs (DRAFT)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
