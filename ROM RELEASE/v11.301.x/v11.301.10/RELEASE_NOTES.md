# DAEMONS v11.301.10 — release notes

*Released 2026-10-16 18:00 · built against the design bible v11.301*

- **Engine**: CodeMusic/pokefirered-daemons `73d5a7f4b` (context-content)
- **Design**: CodeMusic/DAEMONS `5bb46c3f`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `cc47ab1845627a1884e7496b32499b15e5c736de` |
| `daemonsContext.gba` | CONTEXT | `5c7f981a138f55abee350214ad28c5529815514b` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `bed7dc0d1fa8e820c475b2b72dd4f304ce3bbe69` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `43968d33729d436f3557f356361e5f50e705868f` |

## The engine since v11.301.9

- `73d5a7f4b` T-407 (the user, 2026-10-16): NATIVE replaces the size comparison on the INDEX area page -- region, and edition, hours and seasons when a daemon keeps to some; a grove's universe once seen (tools/gbanative.py). Every word DRAFT
- `bb86b6fc5` SCORN's gym echoes him (the user, 2026-10-16): its eight trainers' daemons all carry UPHEAVAL / DISCHARGE / FREEZE / RADIATE in his order -- one streak through the building, with his hole (T-413)
- `81c5f790e` T-407 (the user, 2026-10-16): season and hour homes on the early roads -- on 15 roads up to the fourth MARK one 20% grass slot belongs to the season and one 10% slot to the hour (dawn, dusk, night), 105 rows per edition, 61 daemons new to the pre-League game

## The design and tools since v11.301.9

- `5bb46c3f` companion_export.py (companion 295cb74): species' native, from gbanative
- `fe8b946e` T-407 (engine 73d5a7f4b): tools/gbanative.py, NATIVE on the INDEX
- `c2c132be` T-407 (engine 81c5f790e): the season and hour homes built -- tools/gbashifts.py writes wild_shifts.h; gbareach, check_reach and plan_global_index read it
- `4d3d4829` TODO: T-407's line replaces the size box (the user, 2026-10-16)
- `4120f4a1` TODO: T-407's season and hour homes decided (the user, 2026-10-16)
- `ee7bef6f` ROM release v11.301.9: the glitch on MISSINGNO's encounter (T-414)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
