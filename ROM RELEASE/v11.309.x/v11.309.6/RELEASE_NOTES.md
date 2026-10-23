# DAEMONS v11.309.6 — release notes

*Released 2026-10-23 09:47 · built against the design bible v11.309*

- **Engine**: CodeMusic/pokefirered-daemons `dd3553017` (context-content)
- **Design**: CodeMusic/DAEMONS `b739a186`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `5fe9aece26a08889a005b4d121e3f60051e3ddbb` |
| `daemonsContext.gba` | CONTEXT | `f2564922267c8894d3c30fc0f6e3ba165e3ba896` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `610c728b7948cfe27db337aa92f8d1754cefabd6` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `8ba3ef4565aacead347c9239ebdc52d2f8e6cb68` |

## The engine since v11.309.5

- `dd3553017` T-439: the eleven unused sprites, placed as the cast (the user approved, 2026-10-22)
- `3c56f1a9b` T-440: PROTEUS's battle sheets and form icons drawn from our hooded PROTEUS
- `597f8bab6` T-442: the follower no longer goes black after a field routine's banner

## The design and tools since v11.309.5

- `b739a186` T-438 batch E draft: a look per cave (not in the engine)
- `13b11cbc` TODO: T-439 built (engine dd3553017); T-440 struck (engine 3c56f1a9b); T-442 struck (engine 597f8bab6)
- `0f35500f` T-439: the cast's routes, THE PHOTO's NOTEBOOK row, check_reach knows the coats' patch
- `9aa05793` T-440: tools/genproteus.py, PROTEUS's two shapes in battle and in the party menu
- `466cb816` T-442: gbafieldfx saves its sheets with 16 colours (bits=4), never 256
- `b00381c6` T-438 batch D draft: the stairs and banisters
- `c5e06470` TODO: T-438 batch D interiors approved (timber palette; stairs with it)
- `0666658a` qa: T-438 batch D draft
- `c15d5bf6` T-438 batch D draft: the interiors (not in the engine)
- `1351d777` qa: T-438 batch B and T-441 built
- `82651d10` TODO: T-443 walked-on grass follows the fade and grove moods, and shows in winter (the user)
- `4cd436c3` TODO: T-442 the follower stays black after PRUNE
- `58f22a00` ROM release v11.309.5: field effects and weather redrawn (T-438 batch B); the grass you walk through wears the season (T-441); the item calls (T-433)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
