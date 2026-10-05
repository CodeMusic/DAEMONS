# DAEMONS v11.295.6 — release notes

*Released 2026-10-05 12:41 · built against the design bible v11.295*

- **Engine**: CodeMusic/pokefirered-daemons `3692c5404` (context-content)
- **Design**: CodeMusic/DAEMONS `023c4210`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `5c30a64a9f7712399a3848ab0696c2fd4800db86` |
| `daemonsContext.gba` | CONTEXT | `f61196f141585cd2209b3abb5cb15d25b826f545` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `9473fcc1d47c05d328435e5c5804a5f5c0847328` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `b40d3a0a58954adbbbdb9b4ac729d03d09a91b84` |

## The engine since v11.295.5

- `3692c5404` T-375: the SLATE curator stands upstairs, so his exhibit is "This exhibit", not "The upstairs exhibit"

## The design and tools since v11.295.5

- `023c4210` qa: T-321's three lines where they are spoken
- `e33c8a5d` T-375 closed (engine); T-338 and three of T-321's lines seen; tools/theatre_walk.py, a theatre walker that plans from the map's collision
- `92f4221b` T-367, 5 October: night water on Route 12 and the rival in the lab seen; the NOTEBOOK's documents wait on the user's approval
- `75dd1fb6` T-367, the evening run: the credits, the poster, the START menu and the READING ROOM's turn-away seen in the theatre
- `b12e7db9` qa: T-350 as built and in the STREAM (v11.295.5)
- `cc0f3a9d` ROM release v11.295.5: the clock on the trainer card (T-372), CRYSTAL seen from behind (T-350)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
