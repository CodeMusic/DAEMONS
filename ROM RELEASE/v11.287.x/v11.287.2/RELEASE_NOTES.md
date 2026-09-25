# DAEMONS v11.287.2 — release notes

*Released 2026-09-25 12:30 · built against the design bible v11.287*

- **Engine**: CodeMusic/pokefirered-daemons `36f23bff9` (context-content)
- **Design**: CodeMusic/DAEMONS `1a410609`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `27cd9da1127add686d9046fb6ce05e7dce105035` |
| `daemonsContext.gba` | CONTEXT | `1246ca880762b290c38a182342a8677d36d28e50` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `78f9df97c058449ed500bd2645cc0313d7100120` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `98db0038ab7330e896e142aaab925041db9a0f36` |

## The engine since v11.287.1

- `36f23bff9` T-277: a clock nobody set is no clock
- `a7c2ca79a` T-276: the light changes while you stand in it

## The design and tools since v11.287.1

- `1a410609` T-277 closed: a clock nobody set is no clock (engine.md trap 31 updated)
- `42f72426` T-276 closed: the light changes while you stand in it; engine.md's budgets (748 B of EWRAM free)
- `64d84e9a` ROM release: the Guide's margins, the USER card's brain and BENCHMARKS; v11.286.x sealed

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
