# DAEMONS v11.345.3 — release notes

*Released 2026-11-09 16:54 · built against the design bible v11.345*

- **Engine**: CodeMusic/pokefirered-daemons `2bc6f670d` (context-content)
- **Design**: CodeMusic/DAEMONS `d5dd894c`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `e567b86a2bd08190362d7cc4767dc307e59654d4` |
| `daemonsContext.gba` | CONTEXT | `41c04f36fc8b1168db59d1568684790582a93b7a` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `a98edce1745d6c94d13514d80dbdd0a06e8ac51d` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `e1403ee672dc4e00fab106077d7e9fa7a82593e0` |

## The engine since v11.345.2

- `2bc6f670d` T-535: the second item-description sweep -- 39 rows in our words (DRAFT)

## The design and tools since v11.345.2

- `d5dd894c` T-535 built (engine 2bc6f670d): the user, "Build all 38" -- taste only, keep the jokes, name him, match RETRO; all 38 and RETRO MAIL (moved from T526 to T535, redrafted to the four MAILs' pattern) in T535_APPROVED; four ROMs exit 0, filmed qa 9Nov2026 T535 15-18 (DRAFT)
- `86dd17aa` T-535: the second item-description sweep drafted -- 38 rows (valuables, mushrooms, HEART SCALE, shards, MOOMOO MILK, four MAILs, POWDER JAR, each of the 20 berries its own two lines), T535 in port_item_text.py with T535_APPROVED empty, nothing in the engine (DRAFT)
- `62a715b2` ROM release v11.345.2: T-525 item icons batch 4 -- the last 47 (valuables, shards, milk, the cookie, mail, scarves, PEER REVIEW, ENVELOPE, METEORITE, POWDER JAR, 20 berries); every obtainable item's icon is ours

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
