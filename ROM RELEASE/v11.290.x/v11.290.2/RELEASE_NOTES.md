# DAEMONS v11.290.2 — release notes

*Released 2026-10-01 17:25 · built against the design bible v11.290*

- **Engine**: CodeMusic/pokefirered-daemons `449444209` (context-content)
- **Design**: CodeMusic/DAEMONS `0a3e3066`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `4f3fe15263f1a92740895c6752e5ebac1a305dd9` |
| `daemonsContext.gba` | CONTEXT | `4b1adbcfcfb8eccae5a1c3af82bdebe20a0caad4` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `1bd6b5bcbaa2868b33c78c75a0fed4706c489f42` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `83446b697c875ec52f23cfb435063b2e29d2d8ff` |

## The engine since v11.290.1

- `449444209` T-210: the nine named babies drawn from their parents' sprites (DRAFT) -- VALENCE, RESIDUAL, CRANK, STANDBY, CINDER, STATIC, TELL, PREMISE, RANKLE; icons and streaks follow
- `b73086942` T-120: TEACHY TV's trainer demo shows CRYSTAL, not vanilla's OAK -- the one vanilla portrait a player could still see

## The design and tools since v11.290.1

- `0a3e3066` T-210: nine named babies drawn from their parents' sprites (DRAFT), with the drafts' records; T-120 and T-210 rows updated
- `f906fc1b` T-120: the census walks what can show a trainer portrait -- 80 of the 81 vanilla ones never can (Ruby/Sapphire placeholders); OAK's Teachy TV portrait is CRYSTAL (gbachar crystal_teachy); portraits read 66 of 66
- `aeac658e` TODO: T-333's row names its commits and release
- `b7b3259a` ROM release v11.290.1: QUORUM's line, the 65 INDEX categories; v11.289.x sealed

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
