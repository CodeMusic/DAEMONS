# DAEMONS v11.315.5 — release notes

*Released 2026-10-28 09:38 · built against the design bible v11.315*

- **Engine**: CodeMusic/pokefirered-daemons `faa0b48df` (context-content)
- **Design**: CodeMusic/DAEMONS `ac678910`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `7193791799b324de583e924f1ee2fcc324cf68b5` |
| `daemonsContext.gba` | CONTEXT | `94b1220da39f01e2538c04938159075851872901` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `f95836d0402d957ac170ad87a22e3d85b6d5389c` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `c0402df7342457be5bdb4d1d756d34bab82ef32e` |

## The engine since v11.315.4

- `faa0b48df` T-452 batch 12: REPAY to KAIROS (225-251, less those drawn before) in the new style, on the RECOMMENDED choices while the user was away -- hand-drawn keys (ILLUSION's spiral orbs, BRONTES's storm cloud, GRIEVANCE's chest diamond, RUMINATE's rock, RECALL's pebble, BROODING's eye slits, KAIROS's wing blur), the type-hue trap fixed (PHOENIX's flames crimson, REPAY's gift rose, BOREAS's gem teal, FIXATION's eye amber, ARMOURING's beak and legs crimson), backs the front mirrored with the face out (BROODING keeps today's shell); grounding rows, icon palettes, follower art and palettes, overworld art for the six legendaries
- `bb8e7b53c` A wiki of its own (wiki/ and wiki/publish.sh): building, the debug build, inside the tree, branches and upstream; the README points at it and the DAEMONS wiki, v11.315.4, and what is new -- T-452's new art, T-464's follower, feelings, landmarks and the region map, ITS DREAMS, THE SUBTLE LAYER, SOUNDINGS, routines signed

## The design and tools since v11.315.4

- `ac678910` reviewsheet: find an entry whose text stem is not the slot's capitalised name (MR_MIME -> Mrmime, HO_OH -> HoOh): MIME's and PHOENIX's were blank
- `6736abfe` T-452 batch 12 built (engine faa0b48df): REPAY to KAIROS (225-251, less those drawn before), on the RECOMMENDED choices while the user was away (2026-10-28); MISSINGNO (252) set aside as a question; gfx/drafts/t452/p/questions.md queued for their review -- hand-drawn keys (ILLUSION's spiral orbs, BRONTES's storm cloud, GRIEVANCE's chest diamond, RUMINATE's rock, RECALL's pebble, BROODING's eye slits, KAIROS's wing blur), the type-hue trap fixed, backs the front mirrored with the face out; scripts batch12.py, chain12.sh, prep12.py, hand_b12.py, recolour12.py, icons12.py, ba12.py, ba12.sh, view12.py, grid12.py, build12.py and the batch 12 subjects
- `5e4c583a` TODO: T-466 closed (f84d2df6): private DEBUG patches, back-filled for v11.315.4
- `f84d2df6` T-466: private DEBUG BPS patches for the testing build -- romrelease writes DEBUG/PATCHES/ (four, against the cached retail bases) and debug_patches.json; --debug-patches-only for a filed release; gitignored; ghrelease refuses any DEBUG patch
- `4c0827f3` README and wiki: v11.315.4; the playground and the one app as ways to play; every repo's wiki; T-452's new art, T-464's follower, feelings, routines signed, the map; ITS DREAMS and THE LOG; SOUNDINGS, evolving while carried, the hub's AX630, the T-Watch Ultra (DAEMONS T-465, companion C-214)
- `606fdfee` qa: T-464 follower sheets and T-452 batch 11 (v11.315.4)
- `0637581c` TODO: T-465 DAEMONS on the T-Watch Ultra (C-214); T-466 DEBUG patches kept private (C-216) -- the user, 2026-10-28
- `fb365414` ROM release v11.315.4: T-452 batch 11 (DUPLEX to CLINGING) on the recommended choices; T-464 followers at the player's size

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
