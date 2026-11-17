# DAEMONS v11.385.1 — release notes

*Released 2026-11-17 01:07 · built against the design bible v11.385*

- **Engine**: CodeMusic/pokefirered-daemons `eeab33eec` (context-content)
- **Design**: CodeMusic/DAEMONS `67f2dc7f`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `ac006f49ce6c5f955b35cc1e4e961f548d6609ad` |
| `daemonsContext.gba` | CONTEXT | `4d1c8f9b5fc3dbb730475bc9a07338042e305963` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `a7563447fcc2fc431c7a63c73bf5c0d5569cfc28` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `3c943fd22d3a89546437c1359db8bc799128dccc` |

## The engine since v11.384.1

- `eeab33eec` T-565 batch 1: the 20 menu and UI sounds in C BOTH -- a square click under the harp, the flute for held notes, voicegroup196 (the user's pick, DRAFT; tools/genuisounds.py)
- `d66f4f122` README: the release line names v11.384.1

## The design and tools since v11.384.1

- `67f2dc7f` C-396: THE COMPANION's MANUALS table names THE WATCH, THE GLASSES and THE CARDPUTERS; reprinted (76 pages)
- `a67a9eb7` T-565 batch 1: the menu and UI sounds -- tools/genuisounds.py, three drafts by ear, the user's pick C BOTH (DRAFT)
- `e1a4e2dd` Bible v11.385: the fanfares and the small sounds (T-565, v11.384.1)
- `fb6715f2` README and wiki Home name v11.384.1
- `a3372181` ROM release v11.384.1: T-565 the fanfares, jingles, toy piano and pitched sounds, ours, in the voice the user picked -- our harp and flute over the cartridge (DRAFT); seals v11.383.x

## The design bible's own entry for v11.385

### v11.385 — 2026-11-16

- Recorded from release v11.384.1 (a3372181, engine 4e66bd3d3), the Musical Instruments lane's, which sealed v11.383.x:
  - **The fanfares and the small sounds** (T-565, batches 3 and 7 and the pitched sounds), the user's pick "C Both": 16 fanfares and jingles, five pitched sounds, the toy piano, and SE_CHIME, SE_SUNRISE and SE_NIGHTFALL. DRAFT. In 9.5, a new last part, with the sound census and the split.
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
