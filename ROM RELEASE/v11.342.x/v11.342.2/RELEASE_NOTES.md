# DAEMONS v11.342.2 — release notes

*Released 2026-11-06 20:16 · built against the design bible v11.342*

- **Engine**: CodeMusic/pokefirered-daemons `a01ea9d67` (context-content)
- **Design**: CodeMusic/DAEMONS `e74df6e0`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `2c886fd2ace0b3b7ed6b83bb3f34cd00b5473fce` |
| `daemonsContext.gba` | CONTEXT | `ac11d59fff571eeb5e914acde3af737435033adc` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `e297594bf22695c653c2e0c1d4c541f43f35be82` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `2abe84baf6282be0e44a49a0358bbce0c71019e0` |

## The engine since v11.342.1

- `a01ea9d67` T-452 arm C built (the user, 2026-11-06, "Build the good ones"): 28 daemons and 74 icons redrawn in FLUX.2 klein 4B + the pixel-art LoRA

## The design and tools since v11.342.1

- `e74df6e0` nexus.md: LODESTAR, REFLECTION and BASTET left the painted set for the arm-C redraws (T-452, d30db4c3)
- `d30db4c3` T-452 arm C built (engine a01ea9d67): 28 daemons and 74 icons from the arm C drafts, on the user's "Build the good ones" (2026-11-06)
- `df143183` T-452: the redraws drafted in arm C -- the worst ten, batch 13 restyled, the ten mismatched backs, 95 icons (qa sheets 55-57)
- `58aa0a78` qa: the day's README for T-522's shots 52-54
- `f889fea8` T-522: the user's ear -- only the true voice is kept on the phone, the voices' generation, a play mark on the sprite, the name over the overlay (companion 19f6e14); three shots
- `1baa4d11` generator_drift.json: port_dialogue out (it no longer drifts: a whole-tree write refuses); its SaffronGym warning (T-503) moves into port_dialogue.py as a refusal
- `ef7c6373` port_states: skips the third book's files (daemons_hermetic.c, daemons_spellbook.c) -- THE AWAKENING is the book's first spell, not the sleep cure, and a write renamed it RESUME over T-519
- `436f1555` gbaowslots: a write keeps rows added below its variants (T-496's OBJ_EVENT_GFX_LIONESS_BALL) instead of deleting them (the tree was right, the tool stale)
- `ea21b6d2` gbanexusmap: learns T-519's LARK (engine 545de140f) -- her hide in EventScript_FirKeyFlags, EventScript_LarkAtFir and its words -- so a write no longer takes her out of THE NEXUS's scripts.inc and text.inc (the tree was right, the tool stale)
- `754f9aae` sprites.md: gbaspritecensus --write -- the doc was stale: three overworld people added (CALLOW, DOLDRUM, HALFTONE)
- `7ea09991` type-chart.html: gbachart --write -- the doc was stale: 382 moves now (ALIGN, OTHER)
- `c6ccb7b0` engine.md: gbabudget --write -- the doc was stale after T-519, T-452 and T-445 (ROM 11.1 MB, EWRAM 668 B free, 264 flags)
- `c6e59410` port_arcana: find the companion's arcana.json where it is cloned when the checkout has no link, so check_generators --writes' sandbox no longer crashes
- `cff1ea07` TODO: T-437 the SCREEN font's draft ROM, for the user to try
- `6b56b4bd` T-437 DRAFT: SCREEN built into a draft ROM (engine branch t437-screen-font c5e8280e3, not merged)
- `70c42116` T-452: spriteforge.py learns arm C -- --model klein4b, --lora NAME[:STRENGTH], --reference IMAGE (ReferenceLatent)
- `176f5828` TODO: T-452 the pixel-model trial's winner (klein 4B + pixel LoRA) and the user's yes to redraw in it
- `cac98652` T-452: pixel-model trial -- LODESTAR, ROVERCUB, ILLUMINED by four arms, reduced by the existing reducer (qa sheets 46-48)
- `1fcf7dc7` ROM release v11.342.1: only daemons drawn off the ground float in battle (T-452); v11.341.x sealed

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
