# DAEMONS v11.370.1 — release notes

*Released 2026-11-15 13:52 · built against the design bible v11.370*

- **Engine**: CodeMusic/pokefirered-daemons `fb7aeb81c` (context-content)
- **Design**: CodeMusic/DAEMONS `96a22039`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `c561f721023e270021a170dc3d6eb452fa0241d2` |
| `daemonsContext.gba` | CONTEXT | `9ad38c95c40aeb6483a09388bdc4fd3b48183ef9` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `4427de5be3af16c9b8e7a3beece0a4eab2df879e` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `f764ff1c82601c30342c69c15b8c8418de28abe9` |

## The engine since v11.369.1

- `fb7aeb81c` T-564: the boot's last pret pieces -- the splash's star becomes the CodeMusic mark, its band graph paper, the title's glint bit rain and its stage a rule (the user's picks, DRAFT; tools/gbatitle.py --t564)
- `5bcba60bb` README: the release line names v11.369.1

## The design and tools since v11.369.1

- `96a22039` qa: C-372 covers plain and enhanced
- `b4c2239c` qa: T-564 the boot built (filmed from reset)
- `02d35a41` T-564 BUILT: the boot's last pret pieces, the user's picks (engine fb7aeb81c)
- `fa5791d9` T-564 DRAFT: the boot's last pret pieces -- A/B/C for the splash's band and star, the title's slash glint and border tiles
- `0d4997ed` TODO: T-564 the boot screens' last pieces (batch 5, the user's pick) and T-565 sound effects and the music still to come (the user, later)
- `b7a18450` Bible v11.370: the INDEX and the map in TERMINAL (T-563, v11.369.1)
- `85684870` README and wiki Home name v11.369.1
- `0f193122` ROM release v11.369.1: T-563 the INDEX and the map -- graph paper, index cards, the AREA UNKNOWN plate, the town map's head as the player's own bust, TERMINAL cursors (DRAFT); seals v11.368.x; two recordings deferred

## The design bible's own entry for v11.370

### v11.370 — 2026-11-15

- Recorded from release v11.369.1 (0f193122, engine 0aee7681c), which sealed v11.368.x:
  - **The INDEX and the map** (T-563), the user's picks: graph paper, index cards, the AREA UNKNOWN plate, the town map's head as the player's own animal bust, TERMINAL cursors. DRAFT.
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
