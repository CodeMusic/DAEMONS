# DAEMONS v11.342.6 — release notes

*Released 2026-11-07 03:11 · built against the design bible v11.342*

- **Engine**: CodeMusic/pokefirered-daemons `04fd4b517` (context-content)
- **Design**: CodeMusic/DAEMONS `2918d1bf`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `808e4d33e62804d1aa49fd44301b301353e0c6e9` |
| `daemonsContext.gba` | CONTEXT | `4927c2ce70572a1d83ce74493e677b68c2bf57a9` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `c9271b599de9a00db2ec694fb95f08ffb6746649` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `be74911ccb2cf4ca99a98373a23b56225c2800bc` |

## The engine since v11.342.5

- `04fd4b517` T-525: batch 2 of the item icons built -- 47 drawn by hand in code (the user, 2026-11-07: "Build all 47")

## The design and tools since v11.342.5

- `2918d1bf` TODO T-526: key-item and TONE descriptions still FireRed's (TOKEN CASE, S.S. TICKET, BIKE VOUCHER, a TONE's THRASHING)
- `d1ce7ac8` T-525: batch 2 of the item icons built (engine 04fd4b517) -- the user, 2026-11-07: "Build all 47"
- `8c7e6975` ROM release v11.342.5: T-525 item icons batch 1 -- 41 drawn by hand, each what its DAEMONS item is

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
