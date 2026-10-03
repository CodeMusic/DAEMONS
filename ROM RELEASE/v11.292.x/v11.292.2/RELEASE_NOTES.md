# DAEMONS v11.292.2 — release notes

*Released 2026-10-03 10:10 · built against the design bible v11.292*

- **Engine**: CodeMusic/pokefirered-daemons `fd2525795` (context-content)
- **Design**: CodeMusic/DAEMONS `b3084f64`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `7c7bd52b338077e86a06ba84ca6b7ad1757bc36a` |
| `daemonsContext.gba` | CONTEXT | `12ae03480b08135399b515f88f86fd8e3a764786` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `0d8319e885cf6f895c736999b0b6ae075e2e1a67` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `420fbfe1919bb5f77e1c2095f841417fc367c2d5` |

## The engine since v11.292.1

- `fd2525795` T-210 batch 7: the 13 legendaries, named in the myth register, written and drawn (DRAFT)

## The design and tools since v11.292.1

- `b3084f64` T-210: the count is 110 (18+10+13+12+19+25+13)
- `aca488e9` T-210 batch 7, the legendaries: drafts, art and picks; T-210's naming complete (engine fd2525795)
- `7c6ee049` qa: T-348, the clerk's words
- `19d1226f` ROM release v11.292.1: a shop clerk notices OPUS (T-348); the v11.291 group sealed

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
