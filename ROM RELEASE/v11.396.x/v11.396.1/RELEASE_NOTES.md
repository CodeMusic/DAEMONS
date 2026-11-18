# DAEMONS v11.396.1 — release notes

*Released 2026-11-18 01:42 · built against the design bible v11.396*

- **Engine**: CodeMusic/pokefirered-daemons `c20d4b757` (context-content)
- **Design**: CodeMusic/DAEMONS `bdf78649`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `ae29aec32891b439d6d5bf262a50e388380d5cb1` |
| `daemonsContext.gba` | CONTEXT | `7c12c485532f979df7d8111331eb386e1e719671` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `8d4f78cddfc20177f48828d0bc3320fec26f5f98` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `be52705d363f3f0797299847cfc03658e7533056` |

## The engine since v11.395.1

- `c20d4b757` T-585: THE GARDEN OF ECHOES in ROUTE 24's grove (DRAFT)
- `a36cced0f` README: latest is v11.395.1

## The design and tools since v11.395.1

- `bdf78649` TODO: Redmine's mirror (T-585 closed, pokefirered-daemons@c20d4b757)
- `69299440` T-585: THE GARDEN OF ECHOES in ROUTE 24's grove (engine pokefirered-daemons@c20d4b757, DRAFT) -- gbagrove.py's GARDEN_GROVE/GARDEN_OBJECTS place the hare, magpie, cairn, mole, sheaf and tracks after the LARK; tools/gengarden.py draws the five sprites; tools/routes/film_t585_garden.json films the hare's visit, the magpie and the cold stone, the mole's three visits, PLAY with the mole there, and the grove before the key
- `da662f92` Bible v11.396: DAVID's compass, WHERE never WHEN (T-586, T-587, v11.395.1)
- `84fbdbdf` README, wiki: the newest release is v11.395.1
- `1ac582aa` ROM release v11.395.1: T-586 and T-587 DAVID's compass and its uses (DRAFT); seals v11.392.x

## The design bible's own entry for v11.396

### v11.396 — 2026-11-18

- Recorded from release v11.395.1 (84fbdbdf, engine 521ac9c67 and 3dd7db7fc), which sealed v11.392.x:
  - **DAVID's compass and the NEXUS arrival** (T-586), the user's design: KEEP READING or LOOK OUT THE PORTHOLE; the rose in the mirror alphabet; a read compass lands a grove's fir at that grove's own NEXUS door. DRAFT.
  - **Where it points once read** (T-587), the user's rule: only where something already means something, WHERE never WHEN. DRAFT. Both in 3.4, after the three at the fir.
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
