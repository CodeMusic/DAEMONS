# DAEMONS v11.345.11 — release notes

*Released 2026-11-10 19:53 · built against the design bible v11.345*

- **Engine**: CodeMusic/pokefirered-daemons `ae6500985` (context-content)
- **Design**: CodeMusic/DAEMONS `acd728ba`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `03a82bff11d3f3eaa8ffe67f8b5feb32f1f76d86` |
| `daemonsContext.gba` | CONTEXT | `95b84fa9085ff76d64fa3f65e7540be41db6e474` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `6a2ffa3ffd5690b10b1a63364ff3a096e83fd328` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `19193fab2f50790ac09563ea8e1c8ac69eec7f98` |

## The engine since v11.345.10

- `ae6500985` T-542 batch 1, A HEARTH: THE ROAD GATES -- 53 of primary/general's tiles redrawn in place as the toll cottage (thatch, limewash, terracotta piers, leaded lights in oak, flagstone steps, oak posts); no block, palette, behaviour or map moved (the user, 2026-11-10: "A Hearth"; DRAFT)

## The design and tools since v11.345.10

- `acd728ba` T-542 batch 1 built (engine ae6500985), A HEARTH: gbaprimary APPROVED {A}, its report compares the engine with the write, in check_generators; engine.md's gfx_data row; qa 10Nov2026 T542 54-59; route t542_gates (DRAFT)
- `38322a92` C-317: the Tiiny's voice streamed past LiteLLM -- a keyed pass-through for /v1/audio/speech on roverbyteseer :4001 (keys checked by LiteLLM itself)
- `b2670494` T-542 drafted: the primary general tileset's last Nintendo drawings -- census (152 seen; 3 batches) and batch 1 THE ROAD GATES in three directions (A HEARTH, B THE WAYMARK, C THE LATCH), tools/gbaprimary.py; qa 10Nov2026 T542 47-53 (DRAFT)
- `1af38bf2` ROM release v11.345.10: T-541 SLATE's MUSEUM OF ERRATA in A THE SLATE (DRAFT)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
