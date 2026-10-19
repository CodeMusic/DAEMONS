# DAEMONS v11.306.8 — release notes

*Released 2026-10-19 17:48 · built against the design bible v11.306*

- **Engine**: CodeMusic/pokefirered-daemons `057598012` (context-content)
- **Design**: CodeMusic/DAEMONS `eb198953`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `28038430dfb5db25105046f6ff68ac65bcee01f8` |
| `daemonsContext.gba` | CONTEXT | `802d786a502449cf327b6a752aa4f1df5e4e2d79` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `8fadde7dfac2de9e5e2a042efac4ebb0f30eed55` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `e85e8a0ece823fb0b94d557cb6e9f4a500be7203` |

## The engine since v11.306.7

- `057598012` T-421: the INDEX's type label moves above the name, clear of the entry's first line

## The design and tools since v11.306.7

- `eb198953` TODO: T-421 -- the INDEX label moved above the name (engine 057598012), battle rain seen, the three refactors done
- `f352ae41` T-421 (3): report-mode previews go through daemonslib.preview(), so a run can keep them out of /tmp
- `6a1cd5e1` T-421 (2): tools/daemonslib.py -- one read_pal, write_pal and upstream() for the tools that copied them
- `839bb160` T-421 (1): archive the six orphan tools to tools/archive/
- `2c786093` TODO: T-421, fix the INDEX type label overlap (the user)
- `c8d42f37` ROM release v11.306.7: legends met by walking in, the last gates past 151 lifted, GOLDSET placed, the INDEX's category lookup fixed; the field test covers the week, 53 of 53 stops pass (T-334)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
