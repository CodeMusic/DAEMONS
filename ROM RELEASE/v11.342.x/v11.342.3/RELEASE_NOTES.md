# DAEMONS v11.342.3 — release notes

*Released 2026-11-06 22:35 · built against the design bible v11.342*

- **Engine**: CodeMusic/pokefirered-daemons `20b65bcf0` (context-content)
- **Design**: CodeMusic/DAEMONS `370f2e76`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `da4d641a54ac43f2df32bd4991834380dad86936` |
| `daemonsContext.gba` | CONTEXT | `6e6328b479f46f166c4de7c0901083fee097abb8` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `abaa5cf35f7bc9f77f8ac8c394d18098ac229c98` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `abdca42b2ca19c2bb631347c51407f4a7997c501` |

## The engine since v11.342.2

- `20b65bcf0` T-523: the text window frames and the more-text arrow built (the user, 2026-11-06: A TERMINAL, and "Yes, all of it")
- `77e6e2044` T-445: the TANOBY chambers' card built (the user, 2026-11-06: "Build the top one") -- monean_chamber, the painted card all seven chambers show

## The design and tools since v11.342.2

- `370f2e76` T-523: the text window frames and the arrow built (engine 20b65bcf0) -- the user, 2026-11-06: A TERMINAL, and the whole family
- `d52d658d` T-523: the text window frames and the more-text arrow drafted -- three directions, a family of ten, a new arrow (DRAFT, the user away)
- `0074e1f5` T-445: the TANOBY chambers' card built (engine 77e6e2044) -- the user, 2026-11-06: "Build the top one"
- `a849d560` T-445: the TANOBY chambers' card drafted (batch G is built, engine d45f8c799) -- a DRAFT, the user away
- `1586c28c` TODO T-452: arm C on trial in v11.342.2 -- the user's doubts; no more redraws until they've played old against new
- `217abcf4` ROM release v11.342.2: T-452 arm-C redraws -- 28 daemons (21 full, 7 backs) and 74 icons; LODESTAR, REFLECTION, BASTET leave the painted set

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
