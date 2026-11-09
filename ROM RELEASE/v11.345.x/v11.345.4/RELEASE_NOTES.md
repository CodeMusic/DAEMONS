# DAEMONS v11.345.4 — release notes

*Released 2026-11-09 18:01 · built against the design bible v11.345*

- **Engine**: CodeMusic/pokefirered-daemons `a9026628f` (context-content)
- **Design**: CodeMusic/DAEMONS `af2e19bc`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `70c58f998d285cd8189f887590fa7cf04e50467f` |
| `daemonsContext.gba` | CONTEXT | `54000c689b853b8a2ac9890097550b6f68a11365` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `71f57a3d03abe0f88685bd961358dc1c915d6280` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `4aaa59e48a0faf39f0afa41b8f6be9a2b8b98e95` |

## The engine since v11.345.3

- `a9026628f` T-534: the MUSAI pass with grace -- the user's picked words and three sprite notes (DRAFT)

## The design and tools since v11.345.3

- `af2e19bc` T-534 built (engine a9026628f): the MUSAI pass with grace -- the user's picks: 17 INDEX entries redrafted and 7 kept, the SAFARI ZONE and CINNABAR LAB lines (A), the note under MUSAI's box in CELADON's roof room, and three sprite notes drawn in code (LENSMUSAI spring's control line, CAREMUSAI summer's two hulls and one deck, CODEMUSAI's lights 1101); four ROMs exit 0, filmed qa 9Nov2026 T534 19-24 (DRAFT)
- `b7232891` ROM release v11.345.3: T-535 the second item-description sweep -- 39 rows in our words (the berries' fruit, the valuables, shards, mushrooms, milk, mail, POWDER JAR)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
