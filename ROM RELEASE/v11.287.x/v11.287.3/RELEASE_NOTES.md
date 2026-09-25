# DAEMONS v11.287.3 — release notes

*Released 2026-09-25 13:17 · built against the design bible v11.287*

- **Engine**: CodeMusic/pokefirered-daemons `4f7ca5f83` (context-content)
- **Design**: CodeMusic/DAEMONS `5e1ab9b0`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `26953b28de3cc92f6d9a6f0032743a2af6d3d175` |
| `daemonsContext.gba` | CONTEXT | `a3e50a7b3973935246302b444723c31fb14cc709` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `0d40c1c24dbb1ffbe0c71d10f90ef85d7ecbc938` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `5ab0f71a8a6a964e969ab617dc86d632b201dc49` |

## The engine since v11.287.2

- `4f7ca5f83` T-279: the field effects take the light too
- `d08ab758b` T-278: a day banner never outlives its popup

## The design and tools since v11.287.2

- `5e1ab9b0` T-278, T-279 closed: a day banner never outlives its popup; the field effects take the light
- `ff2bbbec` ROM release: the light changes while you stand in it; an unset clock is no clock

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
