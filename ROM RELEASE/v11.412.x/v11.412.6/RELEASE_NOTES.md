# DAEMONS v11.412.6 — release notes

*Released 2026-11-22 01:18 · built against the design bible v11.412*

- **Engine**: CodeMusic/pokefirered-daemons `c8a337567` (context-content)
- **Design**: CodeMusic/DAEMONS `5619de2f`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `2d36286ea62e5fe0346f23c0e90d367bb07170af` |
| `daemonsContext.gba` | CONTEXT | `da9bf9020c560254f171bba47a1e7aec0dd1db36` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `39d55768d2f7b0f10a2468cc2f8bfe73c5de2a60` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `6f485b9db76006b9d9f3dbc1e7f3c7d4873309ca` |

## The engine since v11.412.5

- `c8a337567` T-445: SCORN SOLUTIONS and ERRATA get places and name cards of their own (the user, 2026-11-22; DRAFT names)
- `e5e026ea4` README: latest is v11.412.5

## The design and tools since v11.412.5

- `5619de2f` T-445: SCORN SOLUTIONS and ERRATA's name cards BUILT (engine c8a337567; the user, 2026-11-22: their own place names, SCORN C with the built tick crisp, ERRATA B, two new flags)
- `6c29f6c9` T-445 (draft): SCORN SOLUTIONS and ERRATA, a NEW name card each -- painted from the buildings as built (T-447 pairs 1, 3) on their towns, three seeds each (4621-4626); sheet t445s_new_cards; nothing in the engine
- `d5bbffc5` qa: T-445 the TANOBY chambers' cards, built (v11.412.5)
- `f6ce9de6` README and wiki: latest is v11.412.5
- `c7550c36` ROM release v11.412.5: T-445 the seven TANOBY chambers each show the shared card in their own band colour (DRAFT)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
