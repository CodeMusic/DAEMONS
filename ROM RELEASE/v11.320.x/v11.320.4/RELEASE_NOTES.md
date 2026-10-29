# DAEMONS v11.320.4 — release notes

*Released 2026-10-29 07:51 · built against the design bible v11.320*

- **Engine**: CodeMusic/pokefirered-daemons `848959312` (context-content)
- **Design**: CodeMusic/DAEMONS `bd8d87de`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `4a807fd7c80626e378d87cb4849aef8cad20773a` |
| `daemonsContext.gba` | CONTEXT | `a3bf4e0786787114b53193283e4999a928830491` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `92e340c69517e460b57b73f5aed6606acb9cab7e` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `aa0f12c4d99a943a920f352c6428f02c1f40bf7c` |

## The engine since v11.320.3

- `848959312` T-480: UNDERCURRENT; the second page's purple mark
- `cfc089932` T-480: the witching hour, the game's half (DRAFT) -- 3:00 to 4:00 AM on the cartridge's clock the party wears a faint, flickering shimmer of THE SUBTLE LAYER's purple (follower, summary, party icons, the player's battlers) and the follower casts no reflection; once the book is held, the battle menu's second screen (R, or DOWN past the bottom row) offers each daemon one routine for its first type, never written into a moveset or the save

## The design and tools since v11.320.3

- `bd8d87de` T-480: genanims files FLOW's hour routine as UNDERCURRENT; the mark's frame
- `ff8fb402` TODO: T-480 built; UNDERCURRENT, SECOND SIGHT dormant, the menu's purple mark (the user)
- `2765698e` T-480: genanims files the witching hour's routines by type (drawn by hand); the theatre route and its frames
- `cfeefae0` qa: C-236 the witching hour on the watches (a mock-up)
- `24960ef7` TODO: T-480 -- ORACLE's SECOND SIGHT
- `b300dfd3` TODO: T-480 -- the user's answers and the shared names (C-236)
- `4bc4565e` TODO: T-480 filed -- the witching hour, the game's half
- `0d83c796` TODO: T-479 struck -- released v11.320.3
- `c407f6e3` manual: rebuilt for v11.320.3
- `6860af02` ROM release v11.320.3: T-479 PENPHIN's INDEX shows both ways in; a trade never writes FIRST MET over a species already seen

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
