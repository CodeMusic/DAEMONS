# DAEMONS v11.308.2 — release notes

*Released 2026-10-21 14:25 · built against the design bible v11.308*

- **Engine**: CodeMusic/pokefirered-daemons `db1ba7b58` (context-content)
- **Design**: CodeMusic/DAEMONS `4eeb104c`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `5bfb320d8edad20686686548d19700ad6da4957b` |
| `daemonsContext.gba` | CONTEXT | `7c02f8e0d766e4606858ec2b66d3775a5b3cc1b3` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `08bbe1220e57063762506481c16d5d3488ab03f2` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `f6518a419a2d1eea314aa9f3654483c07c127224` |

## The engine since v11.308.1

- `db1ba7b58` T-432: shiny colours for every daemon -- 386 shiny.pal from DAEMONS tools/genshiny.py (one shiny per type, ~16 dE within the type; the pale types' light end tinted, FROZEN to a clear ice-blue; coloured accents turned to the opposite hue; UNOWN and THE NEXUS's eight keep theirs); the follower's shiny set regenerated (gbafollowerpal.py, 421 differ, 14 KB)
- `d2757b3b5` T-430: the user's answers -- the foe shows a share of your routine's wash; the splash is the routine's type; the first sight waits for you to walk freely
- `842d74b7c` T-430: what you bring keeps its colour in HALFTONE; T-18 follow-up: the follower goes into the CHECKPOINT's machine

## The design and tools since v11.308.1

- `4eeb104c` T-432 struck: shiny colours written into the engine; generator_drift's PENDING entries removed
- `83996069` T-430 struck: CONTEXT passes too (engine 842d74b7c, d2757b3b5)
- `8735532e` TODO: T-431 emoji drafted and approved (the screen, red hot, 16x16)
- `8ac9923e` T-430: the user's four answers built (engine d2757b3b5); halftone-colour route passes 8/8 in CONTENT
- `87a99c26` T-431 P3 draft: tools/genemoji.py and the 27 faces (not in the engine)
- `2718fb3e` T-430 built (engine 842d74b7c): what you bring keeps its colour in HALFTONE; T-18 follow-up at the CHECKPOINT's machine
- `461a23ab` TODO: T-432 every shiny palette approved; only the write and release left
- `2fdac92c` T-432: FROZEN's tell pushed further (the user)
- `98a6091f` T-432: the pale types' stronger tell; gbasprite leaves shiny.pal to genshiny
- `ce1457a7` TODO: T-432 drafted; the user's four answers
- `794024da` T-432 draft: tools/genshiny.py (report and --sheet; not written)
- `2406b211` TODO: T-432 shiny colours for every daemon (the user, 2026-10-21)
- `79c8b2fe` qa: T-18 P3 the follower's edge cases
- `79cc14df` ROM release v11.308.1: the follower's edge cases -- tall grass, reflections, ledges, ice, dark caves, AWAY and egg leads, Continue; shiny colours; one box a press (T-18 P3, struck); seals v11.307.x

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
