# DAEMONS v11.397.1 — release notes

*Released 2026-11-18 02:10 · built against the design bible v11.397*

- **Engine**: CodeMusic/pokefirered-daemons `ecb28b38f` (context-content)
- **Design**: CodeMusic/DAEMONS `a2446d6f`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `39af488836226b95bffda0064f6bc6a13039e846` |
| `daemonsContext.gba` | CONTEXT | `38e623042e980427233082ee5d3b36f7540292a8` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `0bc65c8e7da7173841fda9e98a76a07d66fa5b98` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `c682f4bde178b49986d937fd859c28c0fcb6ca0c` |

## The engine since v11.396.1

- `ecb28b38f` T-584: cries of their own (DRAFT) -- the eleven that borrowed (the NEXUS residents and the carried line) get cry ids 388-398 and their own samples by gencries.py's A+B; MIME no longer repeats HUNCH's score (the no-twins rule)
- `2dbbeaf6d` README: latest is v11.396.1

## The design and tools since v11.396.1

- `a2446d6f` TODO: Redmine's mirror (T-584 closed, pokefirered-daemons@ecb28b38f)
- `a0d59148` T-584: cries of their own (engine pokefirered-daemons@ecb28b38f, DRAFT) -- gencries.py makes the eleven from gbanexus/gbacarried, writes their table rows, enforces no twins (same score or sample; MIME moved, HUNCH kept) and checks a built ROM with --rom; gbanexus/gbacarried emit cry ids
- `2c80b3cb` Bible v11.397: THE GARDEN OF ECHOES built in ROUTE 24's grove (T-585, v11.396.1)
- `525243bd` qa: T-585 the garden of echoes (v11.396.1)
- `c87b0c2a` README, wiki: the newest release is v11.396.1
- `88d78c3d` ROM release v11.396.1: T-585 THE GARDEN OF ECHOES in ROUTE 24's grove (DRAFT); seals v11.395.x

## The design bible's own entry for v11.397

### v11.397 — 2026-11-18

- Recorded from release v11.396.1 (525243bd, engine c20d4b757), which sealed v11.395.x:
  - **THE GARDEN OF ECHOES, built** (T-585) in ROUTE 24's grove: the hare, the magpie, the cairn, the mole, its sheaf and the tracks, five new sprites. DRAFT. In 3.4, where the paragraph now names the grove.
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
