# DAEMONS v11.345.5 — release notes

*Released 2026-11-09 19:03 · built against the design bible v11.345*

- **Engine**: CodeMusic/pokefirered-daemons `515c95b80` (context-content)
- **Design**: CodeMusic/DAEMONS `1a39e8e4`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `2ca22eb48a1792a60270ea8814ef7389914b23a7` |
| `daemonsContext.gba` | CONTEXT | `0a17afcf21b85cb49becfb3bef34f7c2434920c4` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `c7c00a0c63c7d156e676a5d420e9c34fb148fac1` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `9d2653b26d77112f9b9bc27e89e0a25ca9db16ca` |

## The engine since v11.345.4

- `515c95b80` T-530 touch-ups: the INDEX AREA markers read, the PC's scroll arrows outlined, PARTY and CLOSE BOX in A TERMINAL

## The design and tools since v11.345.4

- `1a39e8e4` T-530 touch-ups built (engine 515c95b80): the INDEX AREA markers read (the window's fill tile 0x001, paper white, and SCORE's land a step down), the PC's scroll arrows a teal chevron ringed in near-black, PARTY and CLOSE BOX in A TERMINAL -- the user, 2026-11-09: menu touch-ups; four ROMs exit 0, filmed qa 9Nov2026 T530 27-30
- `a692aacb` qa C311 26: the companion's confirmed MUSAI faces on the old art and the new
- `2f0e8015` qa C310 25: each MUSAI in its season in the companion's INDEX (autumn in CONTENT, spring in CONTEXT)
- `9b118de9` port_dialogue: a named --write changes only lines still vanilla, and refuses (naming them) over later work; check_generators runs it
- `b2fd8d3c` ROM release v11.345.4: T-534 the MUSAI pass -- the user's picked words (17 seasonal INDEX entries, SAFARI ZONE, CINNABAR LAB, the CELADON roof note) and three sprite notes

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
