# DAEMONS v11.294.1 — release notes

*Released 2026-10-03 13:19 · built against the design bible v11.294*

- **Engine**: CodeMusic/pokefirered-daemons `93ec955d8` (context-content)
- **Design**: CodeMusic/DAEMONS `da602d36`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `1462f11dd5132adf04636cecffa2b445b6bafafd` |
| `daemonsContext.gba` | CONTEXT | `434804b3b4371ecd327f989b8d3d1a9b2775dfe7` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `562de69e74fd53e156866c452a39d32a33112120` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `08f3b41b57fa8562079ba23324cdbe0cd8639361` |

## The engine since v11.292.4

- `93ec955d8` T-360: after the DIPLOMA the OWL congratulates you, and offers to go over what your last paper missed (DRAFT)

## The design and tools since v11.292.4

- `da602d36` T-360: the OWL congratulates, and goes over the misses (engine 93ec955d8)
- `3d591687` Bible v11.294: CONTENT keeps the northern year, CONTEXT the southern (T-359, flipped by the user)
- `65a1fcfb` Bible v11.293: the seasons repaint the world in two hemispheres (T-359), and AWAY for the goal companion (T-358)
- `0e60eae7` The anniversary sprint: T-356 OPUS's margins for the 110, T-357 the unseen builds, T-358 AWAY; companion/ linked
- `82f4fc8e` qa: T-355, the lift's lamp
- `2dd0bdc7` ROM release v11.292.4: the school lift's lamp (T-355)

## The design bible's own entry for v11.294

### v11.294 — 2026-10-03

### CONTENT keeps the northern year (2026-10-03)

- ***9.21, flipped by the user the same day***: *CONTENT the northern year, CONTEXT the southern -- CONTENT is the calendar as the game's maker lives it, CONTEXT the same date reframed from the other half of the world. In the Reversed table.*

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
