# DAEMONS v11.314.5 — release notes

*Released 2026-10-28 00:02 · built against the design bible v11.314*

- **Engine**: CodeMusic/pokefirered-daemons `cc027414c` (context-content)
- **Design**: CodeMusic/DAEMONS `c383e852`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `a0541beda234a7cd66c48f69f6455f6d6208cf50` |
| `daemonsContext.gba` | CONTEXT | `68ee98de4051169ad1f85820560b67c3477d8114` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `2694028e808abc931640d95efed3fa45eb28adf8` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `9b04e0d17f6c4b88347df464ebcec46d4692f604` |

## The engine since v11.314.4

- `cc027414c` T-452 batch 7: DYNAMO to MAINFRAME (125-139) with CRANK, CINDER, LENSMUSAI, MASKMUSAI and OVERLAY in the new style, on the user's answers; CRON's gem pale white-cyan; grounding rows, icon palettes, overworld art, follower palettes

## The design and tools since v11.314.4

- `c383e852` TODO: T-452 batch 7 built (engine cc027414c) on the user's answers; CRON's gem pale white-cyan
- `19f52f28` T-452 batch 7 built (engine cc027414c): DYNAMO to MAINFRAME with CRANK, CINDER, LENSMUSAI, MASKMUSAI and OVERLAY as gbasprite's sources, on the user's answers; CRON's gem pale white-cyan
- `f317345d` qa: T-452 batch 6 sheets (v11.314.4)
- `8d51b577` ROM release v11.314.4: T-452 batch 6 (SLURP to TELL) on the user's answers; T-459 B a read on arrival and READS -> THE LOG

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
