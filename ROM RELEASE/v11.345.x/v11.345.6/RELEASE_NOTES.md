# DAEMONS v11.345.6 — release notes

*Released 2026-11-09 20:21 · built against the design bible v11.345*

- **Engine**: CodeMusic/pokefirered-daemons `3c62cde29` (context-content)
- **Design**: CodeMusic/DAEMONS `8241c752`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `e415ee05ea29959b74dd9a6591d517f03fc4fbde` |
| `daemonsContext.gba` | CONTEXT | `1cdbf5378023997e38341e344da817d5e7f3ff37` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `c1b5a8a01a661cdb2beb1ef6527327690ed3dae3` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `5fc7faa2d5fd20c1580cfe06aebd146226f02176` |

## The engine since v11.345.5

- `3c62cde29` T-536 C, THE FOUNDRY: FOUNDRY CO. and the CORPUS rooms redrawn in place (DRAFT)

## The design and tools since v11.345.5

- `8241c752` T-536 built (engine 3c62cde29): C THE FOUNDRY in FOUNDRY CO. and the CORPUS rooms -- the user, 2026-11-09: "C The foundry"; gbaoffice APPROVED {C} and its report checks the engine, gbadoors redraws both lift doors' frames; four ROMs exit 0, sheets qa 9Nov2026 T536 34-39, route t536_foundry (not filmed); DRAFT
- `d52243aa` T-536 drafted: FOUNDRY CO. and CORPUS interiors redrawn in place, three directions (A BRASS AND STONE, B THE FORM, C THE FOUNDRY) -- tools/gbaoffice.py, sheets gfx/drafts/t536, qa 9Nov2026 T536 31-33; nothing in the engine, APPROVED empty
- `4ff972c8` ROM release v11.345.5: T-530 the menu touch-ups -- the INDEX AREA markers read, the PC's scroll arrows outlined, PARTY and CLOSE BOX in A TERMINAL

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
