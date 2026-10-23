# DAEMONS v11.309.7 — release notes

*Released 2026-10-23 11:51 · built against the design bible v11.309*

- **Engine**: CodeMusic/pokefirered-daemons `4534997ae` (context-content)
- **Design**: CodeMusic/DAEMONS `8c825e8e`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `a64f2c5a542e1b91278eb23a62cc5d7196019788` |
| `daemonsContext.gba` | CONTEXT | `30c0c01781b77ac0a3a58f607bfa4538f9658054` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `dd9eb3058709c31312e7e3750fc61c9a2119f872` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `88e989fc6eb9143c46ea236aaff8e4134f8018c9` |

## The engine since v11.309.6

- `4534997ae` T-438 batch C: a grove's bush keeps its tell on the new bush
- `6b1f49ea6` T-444: HEARSAY's portraits load one palette, not sixteen
- `94a71251e` T-443: the walked-on grass shows in winter, and takes every tint the ground does
- `7d3697878` T-438 batch C: the general ground, in our own hand (the user approved pass 3, 2026-10-22)

## The design and tools since v11.309.6

- `8c825e8e` T-438 C: the grove bush's tell follows the new bush (engine 4534997ae); gbadedupe's 20 new duplicates recorded
- `e7b73b8c` T-438 C, T-443, T-444: the tools, the routes and the checks for engine 7d3697878, 94a71251e, 6b1f49ea6
- `e5c30dd5` TODO: T-438 batch C built (engine 7d3697878); T-443 struck (engine 94a71251e); T-444 struck (engine 6b1f49ea6)
- `c53c71a3` TODO: caves approved; the cast's new lines approved; PROTEUS battles in its edition's shape (follow-up)
- `2d8020bf` TODO: T-444 the Fame Checker portraits' 512-byte palettes
- `7aa6091b` qa: T-439 the cast built, T-440, T-442
- `65a5f7c8` ROM release v11.309.6: the unused sprites recast (T-439) -- a kingfisher who photographs your follower in colour, a peppered moth, an ermine, a sloth, a mynah, a secretary bird, a ptarmigan, a muskrat and a grebe on the water, PROTEUS's two shapes; PROTEUS's CONTEXT art (T-440); no one goes black behind a field routine's banner (T-442)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
