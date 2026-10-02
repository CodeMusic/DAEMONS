# DAEMONS v11.291.4 — release notes

*Released 2026-10-02 16:25 · built against the design bible v11.291*

- **Engine**: CodeMusic/pokefirered-daemons `df50b2c54` (context-content)
- **Design**: CodeMusic/DAEMONS `383e96c3`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `9053ae9fa1ba64b07a167137d66575a890879222` |
| `daemonsContext.gba` | CONTEXT | `63b2207b5caf7c4efb9b3cbe41601d5c8b82c5b9` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `de9f53a6c206eaebec5041cee5ac977e647e4e8a` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `8c1ef9808dc080cfde77ee183e8d683aa9d286d5` |

## The engine since v11.291.3

- `df50b2c54` T-210 batch 3: the rest of the water-typed families named, written and drawn (DRAFT)

## The design and tools since v11.291.3

- `383e96c3` T-210 batch 3: drafts, art and picks (engine df50b2c54)
- `1ae98860` qa: T-210 batch 2 as built
- `915d2633` ghrelease: untracked drafts do not make the tree dirty (as romrelease)
- `49a46ce3` ROM release v11.291.3: the nine routines named (T-210), and the Hoenn water families named, written and drawn (T-210 batch 2)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
