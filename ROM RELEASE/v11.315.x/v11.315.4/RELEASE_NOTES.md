# DAEMONS v11.315.4 — release notes

*Released 2026-10-28 08:34 · built against the design bible v11.315*

- **Engine**: CodeMusic/pokefirered-daemons `8ac48d8bc` (context-content)
- **Design**: CodeMusic/DAEMONS `4eda2279`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `2d19d3c9f0fb78ab9f6504a489a9646ca006e773` |
| `daemonsContext.gba` | CONTEXT | `714d783f1b50eab382bc44cb3836f86c8eb9ad2e` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `17eb44c05992e63c37d075f44f61e4e2998de493` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `996f8abfa216d845a230992c0b43647cf76aec54` |

## The engine since v11.315.3

- `8ac48d8bc` T-464: the follower walks as its own small picture, not the 28px party bust
- `276c89f98` T-452 batch 11: DUPLEX to CLINGING (203-224, less SIGKILL) in the new style, on the RECOMMENDED choices while the user was away -- hand-drawn keys (GLIDEPATH's glide membrane, CRAVING's belly ring, ATTACHMENT's sucker mouth, IMPULSE's eyes under its fringe), the type-hue trap fixed (CRYWOLF's jaw slab, SIMMER's sprout, OLDBRANCH's blue cells greyed), backs the front mirrored with the face out where today's did not match, today's kept where it did; grounding rows, icon palettes, follower palettes

## The design and tools since v11.315.3

- `4eda2279` T-464 closed (engine 8ac48d8bc): the follower walks as its own small picture -- tools/gbafollower.py
- `b60b94d6` TODO: T-452 batch 11 built (engine 276c89f98) on the RECOMMENDED choices while the user was away (2026-10-28); questions in gfx/drafts/t452/o/questions.md
- `fb26572e` T-452 batch 11 built (engine 276c89f98): DUPLEX to CLINGING (203-224, less SIGKILL), on the RECOMMENDED choices while the user was away (2026-10-28); gfx/drafts/t452/o/questions.md queued for their review -- hand-drawn keys (GLIDEPATH's glide membrane, CRAVING's belly ring, ATTACHMENT's sucker mouth, IMPULSE's eyes under its fringe), the type-hue trap fixed, backs the front mirrored with the face out where today's did not match; scripts batch11.py, chain11.sh, prep11.py, hand_b11.py, hand_b10lib.py, recolour11.py, icons11.py, ba11.py, ba11.sh, view11.py, grid11.py, build11.py, batch.py's longer retry and the batch 11 subjects
- `e67790e1` TODO: T-464 a follower walks larger than the player (the user's finding, 2026-10-28)
- `b15156ef` qa: T-452 batch 10 sheets (v11.315.3)
- `5d40aa35` ROM release v11.315.3: T-452 batch 10 (GOLDSET to RESENTMENT) on the recommended choices, for the user's review

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
