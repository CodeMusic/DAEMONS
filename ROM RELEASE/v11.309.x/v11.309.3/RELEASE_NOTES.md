# DAEMONS v11.309.3 — release notes

*Released 2026-10-22 09:25 · built against the design bible v11.309*

- **Engine**: CodeMusic/pokefirered-daemons `454b4a747` (context-content)
- **Design**: CodeMusic/DAEMONS `a927e753`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `fa9899f1b3460eecc2cc792022ec5f4184e064ca` |
| `daemonsContext.gba` | CONTEXT | `057fd2d1a47873ef31e973300fa89f959b7f952a` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `a52607baa15bea8b53d9e4dd7577dbc52241ae51` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `d8fd20e8e748fea75f37feb23a43df8f87791d49` |

## The engine since v11.309.2

- `454b4a747` T-433: items and moments move feelings and friendship (the user's answers, 2026-10-21)

## The design and tools since v11.309.2

- `a927e753` T-433 built (engine 454b4a747): items and moments move feelings; feelings-items.json route
- `3c9d3cbd` T-439 draft: the moth and secretary bird strengthened
- `c3e6dd79` TODO: T-439 the cast approved (push the moth and secretary bird), places, winter coat by palette patch
- `b0df04f5` T-439 draft: the cast drawn (not in the engine)
- `31e46f24` TODO: T-438 batch A doors approved (fix OAK's knob, palette rows, the tile overlap); T-439 sloth and ermine
- `787029fb` TODO: T-439 the user's cast choices; T-440 PROTEUS's CONTEXT art is still vanilla
- `226ba17a` T-438 batch A draft: the doors (not in the engine)
- `6b5f50e7` qa: T-437 the SCREEN draft, T-438 the census
- `af73d432` T-437 draft: SCREEN, tools/gbafont.py (not yet written into the engine)
- `3366d218` TODO: T-439 the unused sprites, repurposed (the user, 2026-10-22)
- `13074243` TODO: T-438 the user's order and methods (doors, effects, ground; interiors in place; a look per cave)
- `242afee1` TODO: T-437 the user chose SCREEN (draft first; the companion adopts it)
- `c6748e38` TODO: T-437 font planned (KERNEL recommended); T-438 census -- people done, 67.5% of tile draws still vanilla
- `81d8b0f5` TODO: T-438 the rest of the overworld art (the user, 2026-10-22)
- `1982a150` TODO: T-50 one Muse Glimmer run authorised (500 turns, CONTENT new game, after T-433); T-437 a DAEMONS pixel font
- `e68e5d1d` TODO: T-436 the theatre walks on water (the user, 2026-10-22)
- `52057c2e` qa: T-434 the water path grove door, T-435 the pier boardwalk
- `8e210dee` ROM release v11.309.2: no NEXUS door strands you -- SIX ISLAND WATER PATH's grove door moves into the channel (T-434); a wooden boardwalk to the S.S. ANNE pier's fir, with the ship and without (T-435); check_reach walks the whole world

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
