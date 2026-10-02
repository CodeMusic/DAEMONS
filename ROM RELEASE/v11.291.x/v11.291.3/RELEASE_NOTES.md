# DAEMONS v11.291.3 — release notes

*Released 2026-10-02 15:54 · built against the design bible v11.291*

- **Engine**: CodeMusic/pokefirered-daemons `c608ef918` (context-content)
- **Design**: CodeMusic/DAEMONS `812c2f7b`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `4c6a47a26d21d497a4b3af1b4e7ad596daf6a56c` |
| `daemonsContext.gba` | CONTEXT | `f7ab51bf6e1ac0200b4906b942d82b7c7796e4c8` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `af27a9b4bd5460da6dc034eb870a01c23c3bc1d3` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `2fff61e47c4b10157353cbc84f2c3529de751ff0` |

## The engine since v11.291.2

- `c608ef918` T-210 batch 2: the five Hoenn water families named, written and drawn (DRAFT, the user's choice of families)
- `6fd7e24bd` T-210: the nine routines batch 1 brought into scope, named and described (approved by the user, DRAFT)

## The design and tools since v11.291.2

- `812c2f7b` T-210 batch 2: drafts, art and tools/t210apply.py (every approved batch's words into the engine, and a drift report)
- `80a693e1` T-210: the nine routines approved and built; continuing as a goal loop (the user)
- `0b3ffcae` qa: T-210 batch 1 as built
- `a6ed1beb` ROM release v11.291.2: the six starter lines of Johto and Hoenn named, written and drawn (T-210 batch 1)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
