# DAEMONS v11.316.2 — release notes

*Released 2026-10-28 11:41 · built against the design bible v11.316*

- **Engine**: CodeMusic/pokefirered-daemons `60bc07f52` (context-content)
- **Design**: CodeMusic/DAEMONS `36eee4aa`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `37790e867fa2820e36d31798987d28226137129c` |
| `daemonsContext.gba` | CONTEXT | `b1ca504a3359d8fc91b82af803551e8a29b35348` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `1ec7bb72fa0f4731e9d08d153822e70f2d01c4c2` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `ae14df815f045b910262745405cccb0844e9c291` |

## The engine since v11.316.1

- `60bc07f52` T-452 batch 14: HASHSEED to JACOBIAN (290-310) in the new style, on the RECOMMENDED choices -- hand-drawn keys (HASHSEED's criss-cross seed, IFTRUE's tick, THENCASE's wing chevrons, OTHERWISE's aqua antenna lights, POLICY's leaf fan, BURSTMODE's speed lines, DEFUNCT's split and blank eyes, LONGJUMP's house locket, CHECKMATE's checkerboard belly, TANGENT's arrow crest, JACOBIAN's bill arrows, SPARRING's second glove), the type-hue trap fixed (SHORTJUMP's and LONGJUMP's orange beaks and feet crimson; BUG greens and the WATER lily pads greyed into the ramp), backs the front mirrored with the face out, grounds off; grounding rows, icon palettes, follower art and palettes

## The design and tools since v11.316.1

- `36eee4aa` T-452 batch 14 built (engine 60bc07f52): HASHSEED to JACOBIAN (290-310), on the RECOMMENDED choices (2026-10-28); drafts in gfx/drafts/t452/s (r already held round two's files), questions in s/questions.md (30 items) -- hand-drawn keys (HASHSEED's seed, IFTRUE's tick, THENCASE's chevrons, OTHERWISE's antenna lights, POLICY's leaf fan, BURSTMODE's speed lines, DEFUNCT's split, LONGJUMP's house locket, CHECKMATE's checkerboard, TANGENT's arrow crest, JACOBIAN's bill arrows, SPARRING's second glove), the type-hue trap fixed, backs the front mirrored with the face out; scripts batch14.py, chain14.sh, prep14.py, hand_b14.py, recolour14.py, icons14.py, ba14.py, ba14.sh, view14.py, grid14.py, grp14.py, build14.py and the batch 14 subjects
- `b0e41ed6` qa: T-452 batch 13 sheets (v11.316.1)
- `e8584a3e` ROM release v11.316.1: T-452 batch 13 (STUMP to UNBRANCHED) on the recommended choices; THE NEXUS keeps its painted art; v11.315.x sealed

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
