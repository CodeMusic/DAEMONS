# DAEMONS v11.290.4 — release notes

*Released 2026-10-01 18:19 · built against the design bible v11.290*

- **Engine**: CodeMusic/pokefirered-daemons `08d82447b` (context-content)
- **Design**: CodeMusic/DAEMONS `5efa88f3`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `e0d0765d98a68e28558379440e5c05254adb8fc9` |
| `daemonsContext.gba` | CONTEXT | `8778951a7147413581cebcf5df15c3aa89dfbd62` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `b20c08c90d034a1e93dc97c2e8f009956a59cf81` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `c0922711df9bb69b2408fabb370e69aac303a3a2` |

## The engine since v11.290.3

- `08d82447b` T-337: the last three grove doors carry the tell -- VIRIDIAN FOREST's and the BERRY FOREST's tree a dark slot down the trunk, SIX ISLAND's rock a small cave-mouth (DRAFT, tools/gbagrove.py)

## The design and tools since v11.290.3

- `5efa88f3` T-337: gbagrove draws the tell in each tileset (SECONDARY_TELL), and marks a trunk that stands off its door's event (tell_at)
- `bab32a81` ROM release v11.290.3: a grove's tree has a little door, the fir's star twinkles (T-337)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
