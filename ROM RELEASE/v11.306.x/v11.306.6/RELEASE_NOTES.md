# DAEMONS v11.306.6 — release notes

*Released 2026-10-19 09:39 · built against the design bible v11.306*

- **Engine**: CodeMusic/pokefirered-daemons `4cf965983` (context-content)
- **Design**: CodeMusic/DAEMONS `26b8a1d0`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `6770d2640a68a7d29aabf49cc2aa60262db001d2` |
| `daemonsContext.gba` | CONTEXT | `e45f5738c78e3f63c2ecd6b37c1dd566bca89356` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `f5cfad85161e077a52690fefcce0ffda89798694` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `bc4688b761b36eb3822acf307495f0ac252e8bfa` |

## The engine since v11.306.5

- `4cf965983` T-334: the GLOBAL INDEX placement -- 128 daemons in the islands' tables, 16 fixed encounters, trading past 151 (DRAFT)
- `91b6f509a` T-210: the INDEX prints the whole category -- two words and the suffix, measured to its field

## The design and tools since v11.306.5

- `26b8a1d0` T-334: tools/gbaglobalindex.py builds the GLOBAL INDEX placement (engine 4cf965983); T-210's category cut fixed (engine 91b6f509a)
- `156db344` TODO: grove moods kept; the category cut to fix (the user)
- `c7ad03e5` qa: T-408 grove moods
- `5f67bcf5` ROM release v11.306.5: each grove its universe's mood (T-408, DRAFT); the 110 INDEX entries approved (T-210)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
