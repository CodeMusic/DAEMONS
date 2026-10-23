# DAEMONS v11.309.8 — release notes

*Released 2026-10-23 13:32 · built against the design bible v11.309*

- **Engine**: CodeMusic/pokefirered-daemons `e36b76c94` (context-content)
- **Design**: CodeMusic/DAEMONS `7a5156e3`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `253387749911ae361ade40cc67ad849c769280c5` |
| `daemonsContext.gba` | CONTEXT | `35569c7514b617542b7d43590a6c231eb5382c80` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `a68ecedd6432f4f13cf6b78c9dfad2c21ae752ff` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `779e241d4200124b20c5304e7896077ad2ed99d1` |

## The engine since v11.309.7

- `e36b76c94` T-440 follow-up: a wild PROTEUS battles in its edition's own shape
- `80f4553d8` T-438 batch D: the interiors redrawn in place, in timber (the user approved 2026-10-22)

## The design and tools since v11.309.7

- `7a5156e3` TODO: T-438 the remaining caves approved (OTHER CAVE cycles four lights); T-445 the cave previews
- `2b0e54db` qa: T-438 the caves drafts
- `a46b956c` T-438 batch E draft: the remaining caves (not in the engine)
- `41130e3d` TODO: T-438 batch D BUILT (engine 80f4553d8); T-440 follow-up built (engine e36b76c94); engine.md's budget
- `b1130a0f` T-440 follow-up: CONTENT's PROTEUS front carries ALL EDGES below (genproteus, gbasprite); gbaowslots reads a 64x128 sheet's top half, so deoxys_n.png no longer drifts (engine e36b76c94)
- `6f02b73f` T-438 batch D: gbabuilding writes over vanilla's tile (a second --write is a no-op); gbaguideshelf redraws the GUIDE's book from the new bookcase; the interiors routes (engine 80f4553d8)
- `c6f5e24c` qa: T-438 batch C, T-443, T-444 built
- `fd170330` ROM release v11.309.7: the ground redrawn -- chunky rock, our own fences, bushes, hedges, signs and the ribbed blue roof (T-438 batch C); the walked-on grass shows in winter and takes the grove moods and the early fade (T-443); the Fame Checker's portraits load one palette, and a check guards every palette load (T-444)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
