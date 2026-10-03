# DAEMONS v11.294.4 — release notes

*Released 2026-10-03 16:59 · built against the design bible v11.294*

- **Engine**: CodeMusic/pokefirered-daemons `4833b0593` (context-content)
- **Design**: CodeMusic/DAEMONS `0f3be030`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `0a06eef978c99390a2c506655a9fbaafd4dfd4db` |
| `daemonsContext.gba` | CONTEXT | `b2cc179ab11997ab5240c492b1b0725bcce075b8` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `40f54cb361c09712b860e0f45213f392f2403b51` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `d4c4d8d6589d6256f9adb169400df7e178b1e4c1` |

## The engine since v11.294.3

- `4833b0593` OPUS's margins for T-210's first three batches: the starters and the water families (T-356)

## The design and tools since v11.294.3

- `0f3be030` T-356: OPUS's margins, batches 1-3 (engine 4833b0593); reviewsheet.py margins
- `ce84470e` ROM release v11.294.3: AWAY (T-358) -- the party menu asks, the world shows where it is

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
