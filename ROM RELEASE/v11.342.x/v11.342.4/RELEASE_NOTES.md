# DAEMONS v11.342.4 — release notes

*Released 2026-11-07 00:25 · built against the design bible v11.342*

- **Engine**: CodeMusic/pokefirered-daemons `87bd966f5` (context-content)
- **Design**: CodeMusic/DAEMONS `f2b901ee`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `a701c96914ff501cec5966db5ffc0bdd0c9f1706` |
| `daemonsContext.gba` | CONTEXT | `309a155c8b65c88faff1d954af34843a5a9fa377` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `510c13ff52aded983b6d71233b45c5c429c88181` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `ef3c989a4ca5a0b2cacc60bf3bc4194361209261` |

## The engine since v11.342.3

- `87bd966f5` T-524: the battle box's teal bracket out of BG palette 0 slot 12, into 10
- `e8dc90f41` T-524: the battle UI built in the TERMINAL family (the user, 2026-11-06: "2 Readout")

## The design and tools since v11.342.3

- `f2b901ee` T-524: the battle box's bracket out of the lean's slot (engine 87bd966f5)
- `b612b55b` T-524: the battle UI built (engine e8dc90f41) -- the user, 2026-11-06: "2 Readout"
- `feb68f77` T-524: the battle UI drafted in the TERMINAL family -- two directions, nothing in the engine (DRAFT, the user away)
- `f774d53f` ROM release v11.342.3: T-523 the text window frames (A TERMINAL, all ten, the arrow); T-445 the TANOBY chambers' card

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
