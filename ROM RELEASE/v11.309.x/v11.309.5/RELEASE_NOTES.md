# DAEMONS v11.309.5 — release notes

*Released 2026-10-22 13:51 · built against the design bible v11.309*

- **Engine**: CodeMusic/pokefirered-daemons `d57baf43a` (context-content)
- **Design**: CodeMusic/DAEMONS `2fcfcbf4`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `ee4ffaffb6249d1f2d4f986583052b6d4f6fdb36` |
| `daemonsContext.gba` | CONTEXT | `18454dc13d8dfd3c705509a1c2094a59e21afd66` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `9ea45056528b215b40eca6b75621e74ed02547f5` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `1d43b4eca0effb75903839992dcf0bd0b4b6c12c` |

## The engine since v11.309.4

- `d57baf43a` T-433: the user's four calls (2026-10-22)
- `38f1d379b` T-441: the grass you walk through wears the season (the user, 2026-10-22)
- `40166656b` T-438 batch B: the field effects and the weather drawn to sit on our ground (the user approved as drawn, 2026-10-22)

## The design and tools since v11.309.4

- `2fcfcbf4` TODO: T-438 batch B built (engine 40166656b); T-441 struck (engine 38f1d379b); T-433's four calls built (engine d57baf43a)
- `db64b621` check_generators --writes: gbacivictown's saffron_city files carry T-438 batch A's moved blocks (recorded); engine.md's budget after batch B, T-441, T-433
- `94d4225c` TODO: T-438 batch C approved (pass 3 rock, motifs, ribbed roof)
- `9b280ad5` qa: T-438 batch C passes 2 and 3
- `4f68bb71` Two generator drifts: port_states' bare "each turn." override, and ai_models reads the machine
- `24dda98d` T-433: the user's four calls in the route (engine d57baf43a): HOTFIX, the field INTERRUPT, a box release and a party release
- `d78ccb8d` T-438 batch B and T-441 built (engine 40166656b, 38f1d379b): gbafieldfx.py says so; tools/routes/fieldfx.json
- `a17cf836` T-438 batch C draft, third pass: chunky rock, the shared-tile steps fixed
- `86ec51af` TODO: T-438 batch C motifs approved (ribbed roof); rock to a third pass, chunkier
- `4ed5f619` T-438 batch C draft, second pass: solid stone and our own motifs
- `98b8787d` qa: T-438 the doors built
- `069933fb` TODO: T-441 walked-on grass ignores the season (the user, 2026-10-22)
- `ff5ff3ef` ROM release v11.309.4: the doors open as the buildings are drawn -- 30 door animations and the door-mat arrow redrawn; the gold door no longer opens teal; CRYSTAL's lab door handles go with the leaves; no door frames left on CHECKPOINT 2F or SAFFRON (T-438 batch A)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
