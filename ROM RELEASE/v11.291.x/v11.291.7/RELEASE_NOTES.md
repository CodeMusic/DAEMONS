# DAEMONS v11.291.7 — release notes

*Released 2026-10-03 06:12 · built against the design bible v11.291*

- **Engine**: CodeMusic/pokefirered-daemons `175867f8e` (context-content)
- **Design**: CodeMusic/DAEMONS `40450156`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `4b1f264059e5f3b792450d3e2eb0eebaef4a298e` |
| `daemonsContext.gba` | CONTEXT | `8421a4aa8072491f3054097ea55c93a204176339` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `07b1fcdd669d7bc1c9c15cd30b6670283b072b27` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `e0c9d2613e5f33bef35e60f52e3972ea5534a06b` |

## The engine since v11.291.6

- `175867f8e` T-210 batch 6: the last before the legendaries, named, written and drawn (DRAFT)
- `2b62068bd` T-210: EPIPHANY's line redrawn as one real animal, a gliding lizard (the user)
- `863a061e0` T-210: the six routines batch 5 brought in, approved by the user (DRAFT)

## The design and tools since v11.291.6

- `40450156` T-210 batch 6, the six routines and EPIPHANY's line: drafts, art and picks (engine 175867f8e)
- `8d97a89d` check_lexicon: a state's verb forms are worn on purpose, like its adjective (engine 863a061e0)
- `722dc7a0` T-210: the six routines approved, EPIPHANY's line to be redrawn as a real animal, and batch 6 next (the user)
- `e1a3b1b0` qa: T-210 batch 5 as built
- `f1519a8b` ROM release v11.291.6: the early Hoenn routes named, written and drawn (T-210 batch 5)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
