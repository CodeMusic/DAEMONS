# DAEMONS v11.283.7 — release notes

*Released 2026-09-25 01:52 · built against the design bible v11.283*

- **Engine**: CodeMusic/pokefirered-daemons `96d3b86b9` (context-content)
- **Design**: CodeMusic/DAEMONS `ae565763`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `59c84f72ca10f7c8a8cf5f7e36fb653873bf2211` |
| `daemonsContext.gba` | CONTEXT | `f0e92eaed425f2a66ea8b5707925ad255571b993` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `5dd465db188c1da893e143d6bb31291e4cf6fb0a` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `e57d1368c8d6a0dc83ca0d799bc401c0cdfff118` |

## The engine since v11.283.6

- `96d3b86b9` T-264/T-265: the terminal never repeats itself; the cartridge's clock is read

## The design and tools since v11.283.6

- `ae565763` T-264 closed, T-265 built and waiting: the terminal never repeats; the cartridge's clock
- `dd50ee02` ROM release v11.283.6: PERSPECTIVE is held, not toggled

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
