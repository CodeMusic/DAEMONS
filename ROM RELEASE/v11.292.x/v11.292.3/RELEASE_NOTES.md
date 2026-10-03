# DAEMONS v11.292.3 — release notes

*Released 2026-10-03 10:36 · built against the design bible v11.292*

- **Engine**: CodeMusic/pokefirered-daemons `25a6e247d` (context-content)
- **Design**: CodeMusic/DAEMONS `e65616aa`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `fc8b9ce501c28205c54c933de8f565b8cd83daf7` |
| `daemonsContext.gba` | CONTEXT | `bf27ff552f4d85cc73783d51c0f1f77747129c38` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `61b0b2b93a5f44090a85172d39f9fce3d1aca8b8` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `bc237ac32647ba8e13204e41fee70db315157c3d` |

## The engine since v11.292.2

- `25a6e247d` T-352: the school's tileset holds 125 tiles now
- `d6eec95f1` T-352: CALLOW SCHOOL's stairs say up or down and which way to step on; the lift looks like a lift
- `1b620d808` T-353, T-354: the exam asks to go on after a section, and resumes where it was left (the user's playthrough)
- `aa66e0a01` T-351: CALLOW SCHOOL's memory floor says seven days, the game's week (the user's playthrough)
- `cc851b93b` T-210: the legendaries' three routines, approved by the user (DRAFT)

## The design and tools since v11.292.2

- `e65616aa` T-349..T-354, the user's playthrough notes: four built, two waiting on a detail; the legendaries' routines approved
- `126b27e8` qa: the 13 legendaries as built
- `77078442` ROM release v11.292.2: the 13 legendaries named, written and drawn -- T-210's naming complete

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
