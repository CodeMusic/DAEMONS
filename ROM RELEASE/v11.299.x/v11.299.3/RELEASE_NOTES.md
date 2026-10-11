# DAEMONS v11.299.3 — release notes

*Released 2026-10-10 20:36 · built against the design bible v11.299*

- **Engine**: CodeMusic/pokefirered-daemons `6533d6553` (context-content)
- **Design**: CodeMusic/DAEMONS `780e7b18`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `59bbc4911fa002746e78d1329391050c39ed123a` |
| `daemonsContext.gba` | CONTEXT | `602ae2c2c0b0cfc919cb3efed84ef0f1a1498dba` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `b7226824eb725a7d02b39e954d8a427892bf4f70` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `e97cb5cada988041cbdaf6564e792d447bbf74bc` |

## The engine since v11.299.2

- `6533d6553` T-395: THE NEXUS painted whole -- no square notches, no rectangle meadows, no repeating floor
- `54e80e2e8` T-395: THE NEXUS's words approved (comments only; the ROM is unchanged)

## The design and tools since v11.299.2

- `780e7b18` T-395: THE NEXUS painted whole (engine 6533d6553) -- the landscape as one picture cut into tiles, its own primary tileset; theatre_route's checker follows an expect after a script's warp; tools/routes/nexus-doors.json walks every grove connection
- `3ad387a9` T-395: the rest of THE NEXUS approved by the user -- the fir's remark, the door and tree prompts, the music, PHOENIX and the meadow's residents, the bear's sprite and the environment art
- `d614cbca` T-395: the GUARDIAN's fifteen lines and the bear's words approved by the user
- `4f561923` ROM release v11.299.2: the bear in THE NEXUS guards DAEMONS (T-395)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
