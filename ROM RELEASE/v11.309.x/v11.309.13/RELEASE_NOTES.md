# DAEMONS v11.309.13 — release notes

*Released 2026-10-24 09:17 · built against the design bible v11.309*

- **Engine**: CodeMusic/pokefirered-daemons `dd2bb01ef` (context-content)
- **Design**: CodeMusic/DAEMONS `d1fd2e1c`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `9df9f2cd669215cd89fab7ab709b16a1e5154d17` |
| `daemonsContext.gba` | CONTEXT | `076bcb2258d9d13b3d56e79d8898bd5a9208b6c1` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `661702d53c1baedae84abdb5f6c49b08fa00a540` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `589538581e405b3ed761acad05de61416f68914d` |

## The engine since v11.309.12

- `dd2bb01ef` T-337: THE UNDERTONE's grove tell drawn again over batch F's trunk
- `f8fa96614` T-438 batch F: ARDOR, HALFTONE, VERDIGRIS and BRAZEN's leftovers redrawn, with their palette moves

## The design and tools since v11.309.12

- `d1fd2e1c` T-438 batch F's next four BUILT (engine f8fa96614); T-337 tell restored (engine dd2bb01ef)
- `c1d287dd` qa: T-445 built, batch F next four revised
- `b68f1192` ROM release v11.309.12: every cave's preview painted -- DEADSTACK, THE WRONG WAY, UMBRAL ASCENT, TAPPOINT'S CAVE, THE BLACKOUT, KEEPALIVE PLANT, GLAUCOUS ISLES, STILLFALL CAVE, MT. SMOULDER, THE DOTS, and OTHER CAVE in the light it holds (T-445)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
