# DAEMONS v11.285.2 — release notes

*Released 2026-09-25 09:02 · built against the design bible v11.285*

- **Engine**: CodeMusic/pokefirered-daemons `b12d77520` (context-content)
- **Design**: CodeMusic/DAEMONS `db0bede5`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `349a9e43937b751f08f402b2ce4c705c9274ed0e` |
| `daemonsContext.gba` | CONTEXT | `7e21a6375da94b1ea7070132d180d1e76ab5390b` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `a3a6e663fdf321788f9b02af06d80dae6a8693d9` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `bd3d53dee90e1f69a89c1b560e077c2374a48f99` |

## The engine since v11.285.1

- `b12d77520` T-300: the Guide's chapters read on one wide page

## The design and tools since v11.285.1

- `db0bede5` T-300: the Guide reads on one wide page (engine b12d77520), at the user's word
- `520100c1` ROM release v11.285.1: The Programmer's Guide to the Human Mind; v11.284.x sealed

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
