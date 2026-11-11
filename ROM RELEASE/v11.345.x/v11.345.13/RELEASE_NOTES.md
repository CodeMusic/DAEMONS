# DAEMONS v11.345.13 — release notes

*Released 2026-11-10 23:09 · built against the design bible v11.345*

- **Engine**: CodeMusic/pokefirered-daemons `b8f27903c` (context-content)
- **Design**: CodeMusic/DAEMONS `c106eefe`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `0860c957de9aecebf6ec8901a85211aa675a0c41` |
| `daemonsContext.gba` | CONTEXT | `b524f15c4e407d47afb9b10372037274235de26e` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `136a718ecfa039ddbd88359352edb3f30d0cfe72` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `a9511e0cf3f7a8395d6d8fd86364583e225aa72e` |

## The engine since v11.345.12

- `b8f27903c` T-542 batch 3, THE EDGES AND DOORS: 21 of primary/general's last 24 outdoor tiles redrawn in place -- the thin tree in the lobed crown, the islet's rim corners, the sea rock in its twin's pale stones, the quay's edge, FOUR ISLAND's puddle banks -- and the sliding doors as A THE CLEAR PANE, their opening frames redrawn from the closed blocks (gbadoors); the water and underwater battle backgrounds re-derived by gbabattleart (T-527's picks unchanged; they sample the sea rock); no block, behaviour or map moved (the user, 2026-11-10: "A Clear pane"; DRAFT)

## The design and tools since v11.345.12

- `c106eefe` companion_shots: a shot may carry a query (&preview=1)
- `19e373c8` T-542 batch 3 built (engine b8f27903c), THE EDGES AND DOORS, doors A THE CLEAR PANE: gbaprimary APPROVED_B3 {A}, its report checks the engine against all three batches, check_generators runs the third write; gbadoors' sliding frames redrawn; gbabattleart's water and underwater backgrounds re-derived (they sample the sea rock; picks unchanged); engine.md's gfx_data row; qa 10Nov2026 T542 111-119; route t542_edges; T-542 complete but for 4, 301, 503 (DRAFT)
- `a616a1b1` qa: C-320, C-321 -- the bookcase, THE COMPANION's pages, the covers reprinted
- `5ce402ca` C-321: THE COMPANION, the whole companion app as a book (71 pages, DRAFT)
- `a6e5f80b` C-320, C-321: every book a cover for the companion's LIBRARY shelf; the printer and the camera for THE COMPANION
- `0e7f7f34` Reprint all seven books against v11.345.12: every daemon's picture from the current build (the user, 2026-11-10: some still showed sprites from before the Tiiny and the LoRAs)
- `cb40e28d` T-533: drafted and read; to build in step with the ROOTs (the user's pick); the mapping is next, the book private until built
- `247c865f` T-542 batch 3 drafted: THE EDGES AND DOORS (24 tiles), gbaprimary B3 (APPROVED_B3 empty; --draft into gfx/drafts/t542_b3/, --write --batch 3 refuses); dictated: the thin tree's crown, the islet's corners, the sea rock, the quay's edge, FOUR ISLAND's puddle banks (4, 301, 503 stay: all edge); the real choice the sliding doors' glass (A THE CLEAR PANE, B THE READOUT, C THE MANIFESTATION), opening frames drawn by gbadoors; gbageneral LATER_T542 claims all 24; qa 10Nov2026 T542 94-107 (DRAFT)
- `3ef37761` ROM release v11.345.12: T-542 batch 2 the town pieces, cave mouth A (DRAFT)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
