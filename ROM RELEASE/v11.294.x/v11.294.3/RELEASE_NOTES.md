# DAEMONS v11.294.3 — release notes

*Released 2026-10-03 16:35 · built against the design bible v11.294*

- **Engine**: CodeMusic/pokefirered-daemons `55d5eb068` (context-content)
- **Design**: CodeMusic/DAEMONS `357278e2`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `6fd22a7b3bfb4bfa011015fd54807feefbdd761c` |
| `daemonsContext.gba` | CONTEXT | `275ea296fd74a09c499e7f9d9ec22c540e92c58a` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `e3168f5b57ff853f9e2769a5ba526a8a1136d7d1` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `3f532c3eea35e4ae4d3b1c37a4e53f2d9315613f` |

## The engine since v11.294.2

- `55d5eb068` AWAY: the party menu asks, the game shows where it is, and an AWAY daemon cannot battle, trade or be released (T-358)

## The design and tools since v11.294.2

- `357278e2` T-358: AWAY built (engine 55d5eb068); engine.md trap 41, a save made outside the START menu
- `5d57f866` T-359: the seasons as mock-ups -- tools/seasonmock.py, CALLOW and Route 1
- `f75b3fb4` ROM release v11.294.2: T-357, the unseen builds seen; the FINISH row, the debug kit's clerk, the faded lamp

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
