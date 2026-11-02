# DAEMONS v11.337.4 — release notes

*Released 2026-11-02 09:53 · built against the design bible v11.337*

- **Engine**: CodeMusic/pokefirered-daemons `8e4534be4` (context-content)
- **Design**: CodeMusic/DAEMONS `1a3f4017`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `cba8721e07e97845260c392a4d465774c6a5eca8` |
| `daemonsContext.gba` | CONTEXT | `f3f9fe48d514d86d0f695b6cbcfdb87703a4b335` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `f88100e7f17c5a4882a017bba68a532da994cd3e` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `b0b7df32db9dd88c260841b6301bcdc90fac037a` |

## The engine since v11.337.3

- `8e4534be4` T-516: THE SUBTLE LAYER's practices, the recommended four (DRAFT)
- `429478f66` T-513: with THE SUBTLE LAYER held, "Not yet." in purple under Ty's "...No. I am not coming." (DRAFT)

## The design and tools since v11.337.3

- `1a3f4017` qa: C-275, the </> tab on the site
- `98b61a9c` C-270: n8n respells any word ending in daemon (eudaemon, cacodaemon); CLAUDE.md's standing rules say DAEMONS is said DAY-mons
- `4639ba00` TODO: T-513 and T-516 done (engine 429478f66, 8e4534be4)
- `d0e6e7da` T-513, T-516: the route that films Ty's 'Not yet.' and the four practices, and the public pictures (qa 2Nov2026 T516 2-3)
- `187b80fe` TODO: T-513 'Not yet.' and T-516's four practices (the user, by multiple choice)
- `d71c8322` companion_export: THE LOG's weekday for the companion (T-511, C-203) -- day_shift, day_mask, the days as the game names them, and day_comma
- `eba48fcb` ROM release v11.337.3: T-510 CLOSURE on the day's virtue, T-511 THE LOG's weekday, T-512 the INTERPRETER's line, T-514 the GUIDE's bands, T-515 THE CARD HOME

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
