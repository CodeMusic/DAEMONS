# DAEMONS v11.383.1 — release notes

*Released 2026-11-16 22:08 · built against the design bible v11.383*

- **Engine**: CodeMusic/pokefirered-daemons `62de521c0` (context-content)
- **Design**: CodeMusic/DAEMONS `cd97e377`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `606d7f6da01cc34c34b2d22e9efac7c354bcff34` |
| `daemonsContext.gba` | CONTEXT | `c9a8547b378c4bb39e68e78e4e87577984e814fb` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `3d0e160af2fe27902f38bed679fac82b41427ba4` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `d07554f98ecc540bc07d56ce8cb53b0f030e0c8e` |

## The engine since v11.382.1

- `62de521c0` T-573: the store's cells take the grass as their bottom layer -- vanilla's (tiles 58 and 62 in row 10) pointed row 10 at tiles redrawn for row 7 (check_lexicon); nothing on screen changes
- `907d1b241` T-573: VERDIGRIS DEPT. STORE as its own landmark -- NEW COPPER, polished copper and glass, the first green speck at its foot (the user's pick, DRAFT; tools/gbalandmarks.py)
- `4b6fa7867` README: the release line names v11.382.1

## The design and tools since v11.382.1

- `cd97e377` T-573: the store's cells sit on the grass (gbalandmarks ground), and gbalandmarks reads gbatownslast's LATER_LANDMARKS
- `aabfc6d3` Book audio: THE CARDPUTERS recorded (C-393) -- 24.5 min in tinkerer, the user's pick, with the book's own respellings; sources 7824d358dee97658, current. Recorded after v11.382.1 as the user chose ("Release now, record after"), committed under v11.383.1's HOLD at the game lane's word so its audio gate passes
- `bd9778ca` T-573 BUILT: VERDIGRIS DEPT. STORE, NEW COPPER (engine 907d1b241); gbatownslast keeps a later landmark out of its pick and pins its T-562 pixels; gbalandmarks reports only the approved store
- `f2953caa` Merge PR #2: The Fourth Review, revised for v11.382.1; press kit updated
- `d283143d` The Fourth Review revised for v11.365.1 and again for v11.382.1: every finding re-checked (T-506 now fixed, the first screens nearly closed, the sound census cited); press kit stamped, its cards reprinted with the ROVER line's new art
- `bd8c4fe9` Bible v11.383: the head over the ring (T-572, v11.382.1)
- `642e5760` README and wiki Home name v11.382.1
- `fea739dd` ROM release v11.382.1: T-572 the player's head over the GOTO map's rings; seals v11.381.x; THE CARDPUTERS recorded after (the user)

## The design bible's own entry for v11.383

### v11.383 — 2026-11-16

- Recorded from release v11.382.1 (fea739dd, engine 04464cc40), which sealed v11.381.x:
  - **The head over the ring** (T-572), the user's pick: the player's head draws over the GOTO map's rings, so REASON and INSTINCT can be told apart at a town. DRAFT.
  - Also in the release, outside the bible: THE CARDPUTERS, the eleventh manual (C-393, DRAFT), released before its recording by the user's choice ("Release now, record after"); T-573's department store drafted, nothing picked.
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
