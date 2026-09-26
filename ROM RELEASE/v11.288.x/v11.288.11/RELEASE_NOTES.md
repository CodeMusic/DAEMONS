# DAEMONS v11.288.11 — release notes

*Released 2026-09-26 17:37 · built against the design bible v11.288*

- **Engine**: CodeMusic/pokefirered-daemons `1d57bab98` (context-content)
- **Design**: CodeMusic/DAEMONS `80b4f2b1`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `0ea97e5cd15b89c114c25b0b5978cb9897d7ec6a` |
| `daemonsContext.gba` | CONTEXT | `1cd5ba102376a73222a76243cdb33611af914e92` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `8457d98cbc6591d0673e64f0afd7c438df197171` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `267e4a218a0821f2345169775b50a4aed26531ea` |

## The engine since v11.288.10

- `1d57bab98` QR codes at the end of FOLDS and the Guide (T-315; even-aligned, engine.md trap 36); DAVID's line rewrapped
- `9369ce0e8` DAVID captains the S.S. ANNE (T-313, DRAFT: his sheet from DAD's, his lines); the shoes show who gave them (T-256: soles and trims on their own palette indices, yellow/black from MOM, black/red from DAD)

## The design and tools since v11.288.10

- `80b4f2b1` T-256, T-315 closed; T-313 built; engine.md trap 36; tools/gendavid.py, gbashoes.py, gbaqr.py
- `4caba127` HOW_TO_PATCH.md names the patches as GitHub shows them; ghrelease.py --refresh; v11.288.10 published with its four patches
- `877a0dff` ROM release v11.288.10: Ty a red fox, CALLOW's own theme, the menu's note; the first release published with its patches

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
