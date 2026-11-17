# DAEMONS v11.380.1 — release notes

*Released 2026-11-16 19:42 · built against the design bible v11.380*

- **Engine**: CodeMusic/pokefirered-daemons `528a27359` (context-content)
- **Design**: CodeMusic/DAEMONS `a5354056`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `c445cc94d32729ec7e3ee3153b03b77f106bd8af` |
| `daemonsContext.gba` | CONTEXT | `3725b95458422bb5c52c4a6b945065bf7bb98c5d` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `fc28fcf7d629724fa326e0175a8f566e4addce54` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `310efc2dea0b919ee0e09ffc064ef93d426142e8` |

## The engine since v11.379.1

- `528a27359` T-566 follow-up: the relearner's caret arrows can be seen -- sprites switched on in its screen, the down arrow kept in spriteIds[1], and each shown by the list's own scroll (three vanilla bugs; the user's yes)
- `54516e3f0` The tools were right (T-292 drift, read both ways): the ROVERBYTE and MUSAI credit cards rebuilt from their redrawn fronts (gencreditcards), and DENSE WOOD's grove tell one pixel back on its trunk (gbagrove)
- `a0e9f3de0` README: the release line names v11.379.1

## The design and tools since v11.379.1

- `a5354056` qa: T-566 the relearner's caret arrows, seen (engine 528a27359)
- `2b3c6b90` qa: film the unseen (T-564 glint, T-568 PC icon, T-566 arrows/TM/egg, T-561 quest log)
- `03935faa` Books reprinted after T-571: THE SUBTLE LAYER's PDF and the three vaults say USER/USERS and POOL
- `479ff68f` check_generators: shelfcovers is not sandboxed -- it reads and writes the companion's shelf art
- `6765e82f` gbainkpaper refuses a whole-tree write over T-554's bag; port_dialogue's record names T-540's two files
- `ba4f619d` gbacaves and gbaislands keep T-569's and T-570's tiles (check_generators --writes, 2026-11-16)
- `717e1aa2` gbalandmarks: gbatowns.LANDMARKS must hold this tool's boxes, and may hold others' (the KEEPALIVE PLANT's front shares lavender_town)
- `e4571635` engine.md and sprites.md: the numbers refreshed (gbabudget, gbaspritecensus --write; check_generators --writes, 2026-11-16)
- `8f8f6152` THE PLAYER'S MANUAL reprinted against v11.379.1 (STALE after the release; words unchanged)
- `54b3f42a` gbatowns.LANDMARKS holds the GAME CORNER and the KEEPALIVE PLANT's front (T-562 follow-up): its own write can no longer redraw the two T-447 plan boxes gbatownslast keeps
- `7fd0388f` Bible v11.380: the last island and cave tiles (T-570, v11.379.1)
- `792ae845` README and wiki Home name v11.379.1
- `c8518a50` ROM release v11.379.1: T-570 the last island and cave tiles -- rungs-and-rails ladders, broken-lip holes, glare-and-glint ice, the rest in keeping (DRAFT); seals v11.376.x; every book recording current

## The design bible's own entry for v11.380

### v11.380 — 2026-11-16

- Recorded from release v11.379.1 (c8518a50, engine 251e985ce), which sealed v11.376.x:
  - **The last island and cave tiles** (T-570), the user's picks: rungs-and-rails ladders, broken-lip holes, glare-and-glint ice, the rest in keeping; 94 of 134 drawn, 40 left as named. DRAFT. In 9.29, after the islands and the caves.
  - Also in the release, outside the bible: T-560's smoke run from the title screen on the Tiiny's 35B, and every book's recording made current.
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
