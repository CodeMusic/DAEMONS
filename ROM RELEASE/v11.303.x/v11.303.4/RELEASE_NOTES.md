# DAEMONS v11.303.4 — release notes

*Released 2026-10-18 08:05 · built against the design bible v11.303*

- **Engine**: CodeMusic/pokefirered-daemons `73016d9eb` (context-content)
- **Design**: CodeMusic/DAEMONS `bdde620d`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `6e5e7a52a296bc0b624e8aa402dceb4b53224960` |
| `daemonsContext.gba` | CONTEXT | `93247f3145750bda435366cd3e427757f132fc87` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `c70677a714232ca1052509ddbe43054a29231938` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `44ce403e3e3f44e25ce9dd9d61756b7e5fd98bf6` |

## The engine since v11.303.3

- `73016d9eb` T-420: the STREAM's MARK shows no longer share flags with OPUS

## The design and tools since v11.303.3

- `bdde620d` TODO: DEN DAY reads either type (the user); T-421 gains the recap-continue path
- `7a98d6d0` T-420 done (engine 73016d9eb): the STREAM's MARK shows off OPUS's flags; check_lexicon checks every flag range
- `10d0e604` qa: T-416 holidays P1-P2, the rounded islet
- `994ef00b` ROM release v11.303.3: HOLIDAYS P1-P2 -- the month's note and colour on the banner and the card, 36 holidays, gifts once a year, THE YEAR (T-416); BREATHVERSE rounded and timeless (T-417)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
