# DAEMONS v11.288.13 — release notes

*Released 2026-09-26 18:34 · built against the design bible v11.288*

- **Engine**: CodeMusic/pokefirered-daemons `0013244c6` (context-content)
- **Design**: CodeMusic/DAEMONS `4ce06065`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `4b4b1005a7e430d361723ca7b9bebc5cd2485a5f` |
| `daemonsContext.gba` | CONTEXT | `e6449384dfc0970b84b0bf4eedaf7625a34f2edf` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `9205bdfe6cf9fd2f27288b4cadfd090b54da36f4` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `4878f61d66ddc6d9b535551bb591341b48a6a241` |

## The engine since v11.288.12

- `0013244c6` Six more understandings, arrived at on map load, each a note in a GUIDE chapter's margin (T-252, DRAFT); the START menu's frame in the day's colour (T-318)

## The design and tools since v11.288.12

- `4ce06065` T-252 six understandings built (DRAFT), T-318 menu colour built, T-234 types decided
- `3bc4eec2` ROM release v11.288.12: the credits' runners; the AI playtester's brief

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
