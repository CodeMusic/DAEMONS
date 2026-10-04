# DAEMONS v11.294.8 — release notes

*Released 2026-10-03 20:19 · built against the design bible v11.294*

- **Engine**: CodeMusic/pokefirered-daemons `8f9233114` (context-content)
- **Design**: CodeMusic/DAEMONS `d802355b`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `70071816ef37197dc60cbc3d8f1a1cc27ae09120` |
| `daemonsContext.gba` | CONTEXT | `01f6fc299852efb79c2a56dc44cfbebf151e70ff` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `8466dfd251fcd3bcbcca020527989d66d4623941` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `9b84bf7a65177ac9b5201f76a9a2a37919b96236` |

## The engine since v11.294.7

- `8f9233114` The seasons, by palette, and spring's flowers (T-359)

## The design and tools since v11.294.7

- `d802355b` T-359 built: the seasons (tools/gbaseasons.py); engine.md's budgets rewritten
- `70c4e4aa` ROM release v11.294.7: the name screen in our own look (T-363)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
