# DAEMONS v11.345.12 — release notes

*Released 2026-11-10 21:23 · built against the design bible v11.345*

- **Engine**: CodeMusic/pokefirered-daemons `2ec006aa1` (context-content)
- **Design**: CodeMusic/DAEMONS `27e696fa`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `03056b19d22045d7b38942efb6a51f355294977a` |
| `daemonsContext.gba` | CONTEXT | `13bcae982896455e5f9f7127d019d100d1569b9c` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `e420bc3db3b50ba1d6ae1941ca311659933415e3` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `31353cf97954e316066d06474ac99bbef7c12e73` |

## The engine since v11.345.11

- `2ec006aa1` T-542 batch 2, THE TOWN PIECES: 66 of primary/general's tiles redrawn in place in each town's own look -- VERDIGRIS's bronze seams and patina (shown by LURID and ARDOR too), CALLOW's calmed seam (THREE ISLAND's roof in red), the blue house, DOLDRUM's siding, SLATE's ashlar, BRAZEN's hips and kiosk domes, ARDOR's coping, the islands' net -- and the cave mouth as A THE ROCK'S OWN MOUTH; no block, palette, behaviour or map moved (the user, 2026-11-10: "build as drawn; cave mouth A"; DRAFT)

## The design and tools since v11.345.11

- `27e696fa` T-542 batch 2 built (engine 2ec006aa1), THE TOWN PIECES as drawn, cave mouth A THE ROCK'S OWN MOUTH: gbaprimary APPROVED_B2 {A}, its report checks the engine against both batches, check_generators runs both writes; engine.md's gfx_data row; qa 10Nov2026 T542 83-93; route t542_towns (DRAFT)
- `d20fa3da` T-533: the parents and the physics thread picked by multiple choice and drafted (private); every layer in; the row says so
- `588cd7d4` T-533: the captain's layer and the ball talked through by multiple choice and drafted (private); the row says so
- `82c1ef0f` T-542 batch 2 drafted: THE TOWN PIECES (75 tiles) in each town's own look, gbaprimary B2 (APPROVED_B2 empty; --draft into gfx/drafts/t542_b2/, --write --batch 2 refuses); the cave mouth the one real choice (A THE ROCK'S OWN MOUTH, B THE ADIT, C THE PORTAL); gbageneral LATER_T542 claims all 75, so pass 3 no longer draws 298/330; qa 10Nov2026 T542 66-82 (DRAFT)
- `f2bd3652` qa: C-318 WHAT'S NEW on the site (companion 5c7826f)
- `198f05e8` ROM release v11.345.11: T-542 batch 1 the road gates in A HEARTH (DRAFT)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
