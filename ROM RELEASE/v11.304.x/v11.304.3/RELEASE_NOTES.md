# DAEMONS v11.304.3 — release notes

*Released 2026-10-18 11:38 · built against the design bible v11.304*

- **Engine**: CodeMusic/pokefirered-daemons `8709f747a` (context-content)
- **Design**: CodeMusic/DAEMONS `4bb1b0ef`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `c461c48463eed76550b732f555e9539f652b24af` |
| `daemonsContext.gba` | CONTEXT | `7eead53db564810be87b7032e7c706ca451c76ed` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `086a17fd4eccc45003d8a5e711ca92d324be7cfb` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `643720fead2a77ad0eb76796f644c7aa05983266` |

## The engine since v11.304.2

- `8709f747a` T-410, T-411, T-412 (approved by the user 2026-10-18): a MARK and its ROOT balance each other; the last note; the DREAM LOG (DRAFT)

## The design and tools since v11.304.2

- `4bb1b0ef` T-410, T-411, T-412 placed (engine 8709f747a, DRAFT): the balances, the last note, the DREAM LOG
- `a1329bbc` TODO: T-415 phase 2 released; LATENT and the five kept (the user)
- `ff22f163` qa: T-415 phase 2
- `c7b2ce7f` ROM release v11.304.2: WEATHER phase 2 -- SIGNAL in storms, LATENT in fog, VECTOR in wind (now on physical routines too), the battle tint and the glint, five weather daemons, NATIVE says IN RAIN (T-415)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
