# DAEMONS v11.283.6 — release notes

*Released 2026-09-24 16:36 · built against the design bible v11.283*

- **Engine**: CodeMusic/pokefirered-daemons `d46966ced` (context-content)
- **Design**: CodeMusic/DAEMONS `6ee4e1a0`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `bff41e23cede1d1f947260373fc4455589b784ce` |
| `daemonsContext.gba` | CONTEXT | `220b2337be31b23adfb9fe2d93839a9467f1088b` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `1873fca82e570ea3f78f06a373374f881c84f68a` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `dbef4c12409c39748dbd290d4f04b9c0a5d7b939` |

## The engine since v11.283.5

- `d46966ced` T-263: PERSPECTIVE is held, not toggled

## The design and tools since v11.283.5

- `6ee4e1a0` T-263 logged and closed; the theatre can hold a key across commands (press/release)
- `7fde3a46` ROM release v11.283.5: the backlog, each ticket closed or waiting on one answer

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
