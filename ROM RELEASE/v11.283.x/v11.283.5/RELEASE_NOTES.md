# DAEMONS v11.283.5 — release notes

*Released 2026-09-24 12:21 · built against the design bible v11.283*

- **Engine**: CodeMusic/pokefirered-daemons `c77cc3cac` (context-content)
- **Design**: CodeMusic/DAEMONS `dc8f4486`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `0926d32c16133c7dfce167a444c6baad544a0cb5` |
| `daemonsContext.gba` | CONTEXT | `7ac70658387e3a0c4f82322e6ed8465952de07c4` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `62ad82ed4a5a0f635d6bbd833c824e0c062861b5` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `1d79cd0f29f574d0ef09288b40f4545e7b962e28` |

## The engine since v11.283.4

- *nothing: the same engine commit as the release before*

## The design and tools since v11.283.4

- `dc8f4486` TODO: every open ticket closed or waiting on one named decision
- `36bb4b91` ROM release v11.283.4: DEBUG JUMP to CRYSTAL and the WARDEN

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
