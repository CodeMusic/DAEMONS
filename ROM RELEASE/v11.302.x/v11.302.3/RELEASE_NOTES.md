# DAEMONS v11.302.3 — release notes

*Released 2026-10-17 22:39 · built against the design bible v11.302*

- **Engine**: CodeMusic/pokefirered-daemons `374c06835` (context-content)
- **Design**: CodeMusic/DAEMONS `078cd883`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `7fc8c77af8a3e66cfadcf750577dad28db9c8344` |
| `daemonsContext.gba` | CONTEXT | `4addb998c1e5631385879f6ed688856bb31b69eb` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `8d156bae453c02e58c9d31ffe6bdbe9e4c0868da` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `c1733dd25b0e96274af925212574f55d295b23f8` |

## The engine since v11.302.2

- `374c06835` T-417 P3 (the user, 2026-10-17): the two places -- CONTENT's HARP from a LYREBIRD at CALLOW SCHOOL, CONTEXT's FLUTE under a palm on FINDERS BEACH (DRAFT)

## The design and tools since v11.302.2

- `078cd883` qa: T-417 P3, the LYREBIRD and the palm
- `d2f5f188` TODO: T-416's rules and T-408's grove music decided by the user
- `2ece1ee8` qa: C-148 GLOW on the StickC-Plus -- the four heat routines, run on the user's stick
- `d47b37c3` TODO: T-417 P3 BUILT (engine 374c06835) -- the LYREBIRD gives the HARP at CALLOW, the FLUTE under FINDERS BEACH's palm; genlyrebird.py, genpalm.py
- `2bab91f6` companion_export: SONGBOOK pages (kind song) reach notebook.json; the DEBUG build's pages are left out (T-417)
- `d73be864` ROM release v11.302.2: PLAY P2 -- O CHRISTMAS TREE opens the fir and lights THE NEXUS, the SONGBOOK (T-417)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
