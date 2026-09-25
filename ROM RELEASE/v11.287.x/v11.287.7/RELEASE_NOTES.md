# DAEMONS v11.287.7 — release notes

*Released 2026-09-25 17:03 · built against the design bible v11.287*

- **Engine**: CodeMusic/pokefirered-daemons `c38b70e32` (context-content)
- **Design**: CodeMusic/DAEMONS `19b47da5`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `47cd2fb887d105922852d4df6fe27e8a338bc0d7` |
| `daemonsContext.gba` | CONTEXT | `d90e4766794e29d1af3e6af4ea46fd545884eb45` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `c88299735fc2b4fd2960cf242da6361d49eaf105` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `838687f933527b4eaa3f116200eee4e4c4968aa9` |

## The engine since v11.287.6

- `c38b70e32` LOOSE PAGES 7, FOLDS (DRAFT): folding instructions pinned where the 3F's lower painting hangs
- `0e77879d2` T-284: Scorn stood in the only doorway to Ty's room -- the PAYLOAD could not be reached in play

## The design and tools since v11.287.6

- `19b47da5` check_reach: every person, sign and item reachable, against vanilla; gbadocs refuses a spot nobody can stand at
- `e4e9a34a` ROM release v11.287.6: a 12-hour cartridge clock is read

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
