# DAEMONS v11.291.8 — release notes

*Released 2026-10-03 08:15 · built against the design bible v11.291*

- **Engine**: CodeMusic/pokefirered-daemons `ecf9a9eee` (context-content)
- **Design**: CodeMusic/DAEMONS `6c6a1724`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `c40795fb23f4e55f4a4bf68412bf08e94e58a047` |
| `daemonsContext.gba` | CONTEXT | `2b34a1782722386a9cee0d47c95bda79d13f22cc` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `ed9e0580a84c539f5e70d19a36929c4d32f240df` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `e2c073e5cd978cbdc4d601949078f4384a865ce8` |

## The engine since v11.291.7

- `ecf9a9eee` T-210: the six routines batch 6 brought in, approved by the user (DRAFT)

## The design and tools since v11.291.7

- `6c6a1724` T-210: the six batch 6 routines approved and built; the legendaries begin with the user
- `e310db77` qa: T-210 batch 6 and EPIPHANY's line as built
- `086efbaf` ROM release v11.291.7: six routines, EPIPHANY's line as a real animal, and the last batch before the legendaries (T-210 batch 6)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
