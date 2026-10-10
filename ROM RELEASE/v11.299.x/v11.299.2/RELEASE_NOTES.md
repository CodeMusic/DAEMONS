# DAEMONS v11.299.2 — release notes

*Released 2026-10-10 19:51 · built against the design bible v11.299*

- **Engine**: CodeMusic/pokefirered-daemons `e50fe79be` (context-content)
- **Design**: CodeMusic/DAEMONS `fa1d44b4`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `c3089a90fd72628b46ccf63bdb64a781a1e098ce` |
| `daemonsContext.gba` | CONTEXT | `d4aa4ba5eb30ed2a0e9b33d1039c6a628a20dd74` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `f5cf80e97ae82c840e4d124c8a07bc8e60f32edf` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `749f99b1be7393d5715ff3d4c0c989f7ee45119f` |

## The engine since v11.299.1

- `e50fe79be` T-395: THE (NOT A) HUNTER guards DAEMONS, not animals -- every person here is an animal, the bear too (the user, 2026-10-10)

## The design and tools since v11.299.1

- `fa1d44b4` T-395: the bear's precious ones are DAEMONS (engine e50fe79be; the user: "hurt these animals -- or daemons?")
- `8a7b5cf6` T-395: OPUS's margins for the eight NEXUS residents approved by the user ("Looks great, ship it")
- `4219ac6c` qa: the T-Deck Plus's first screens (C-104)
- `dba1fb96` T-395: THE NEXUS played in the theatre -- tools/routes/nexus.json paced to the fir's song; sheets filed (qa T395 4-7)
- `78eeeb6a` ROM release v11.299.1: THE NEXUS (T-395) -- the fir in every grove, flat until its key, and a place made of paint behind it; v11.298.x sealed

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
