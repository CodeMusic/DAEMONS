# DAEMONS v11.309.14 — release notes

*Released 2026-10-24 11:39 · built against the design bible v11.309*

- **Engine**: CodeMusic/pokefirered-daemons `c5078dca6` (context-content)
- **Design**: CodeMusic/DAEMONS `9a93dcee`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `651e62b766255259da05e136b12e3073dc7f6293` |
| `daemonsContext.gba` | CONTEXT | `796d1f6a9c5be292b789c9b72d54c94127c37693` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `3bdcb880a9b8abeb5ca42c5301dfa62b40f97894` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `6ec6fb6d003042df96b01ac58e47448a2165ccf8` |

## The engine since v11.309.13

- `c5078dca6` T-438 batch H: LURID, the island kit, DENSE WOOD and QUICKSILVER's one tile redrawn; THE SAME BUSH as a palette split (gTileset_SameBush)

## The design and tools since v11.309.13

- `9a93dcee` T-453: companion_export writes index_cards.json (the INDEX card whole, the understandings and their GUIDE margins) and patches.json (each published release's BPS patches described, targets proved by applying them where the retail builds are cached); companion c854f214
- `97d76c96` qa: C-162 the battery on the watch faces (the picture its README entry names)
- `cceeef63` qa: C-183 the activity panel on the watch (README entry)
- `93caadff` TODO: T-448 what the game must accept from the companion (HANDSHAKE delivery)
- `c6ee3d11` T-438 batch H built (engine c5078dca6): LURID, the island kit, DENSE WOOD, QUICKSILVER's one tile, THE SAME BUSH's split; the landmarks kept
- `eae465b7` TODO: T-453 one self-contained app (game, companion, library, notebook)
- `56b2b0f0` TODO: T-452 daemon art pilot in the concept style; T-453 the iPad app's game half
- `4ff7f9f7` TODO: T-450 the user's choices (line A, the unused slots, from the companion, 60/160)
- `8d2cf8b0` TODO: T-451 the theatre's warp loop on a doormat
- `9f68790a` T-450 carried line drafted: 16 concepts for line A (HANDSHAKE, TETHERING, COROUTINE), seeds recorded (gfx/drafts/t450)
- `3b4fe894` theatre: mom-tour route -- Mom's Field Guide walked on the CONTENT DEBUG build
- `c94f4e2a` TODO: T-449 the user's answers (SCORE, animated sea, frame, overworld water)
- `e2a6129b` TODO: T-450 a line that grows only while carried (C-185)
- `8c3e4e43` qa: C-183 the activity panel on the watch
- `f780ddb9` T-449 region map rebrand drafted: three directions (SCORE, CIRCUIT, SIGNAL) at the real size, same cells (gfx/drafts/t449)
- `533ce419` companion_export: each species' evolutions for the companion (T-448)
- `e809704d` TODO: T-448 evolving on the companion (C-184's game half); T-449 the region map rebranded
- `93d48419` TODO: T-447 the user's answers on the landmarks
- `6db593e4` T-447 landmarks plan drafted: eleven story-derived concepts and sheets (gfx/drafts/landmarks)
- `90ac3da2` TODO: T-447 the landmarks get art of their own, from the story
- `87e1f619` TODO: the user's answers on batch H
- `28806988` T-438 batch H drafted: LURID, QUICKSILVER IS., the island kit (ONE..SEVEN), DENSE WOOD, and THE SAME BUSH's palette split
- `c150f9ab` TODO: T-446 elevator doors drift; qa: batch F next four built
- `ac44e5da` ROM release v11.309.13: ARDOR, HALFTONE, VERDIGRIS and BRAZEN in their own looks -- pantiles and warm iron, a dot screen, verdigris and THE STREAK, brass and gold (T-438 batch F); THE UNDERTONE's grove tell restored (T-337)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
