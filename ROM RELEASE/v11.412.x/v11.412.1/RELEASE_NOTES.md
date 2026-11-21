# DAEMONS v11.412.1 — release notes

*Released 2026-11-21 13:15 · built against the design bible v11.412*

- **Engine**: CodeMusic/pokefirered-daemons `ed40566e3` (context-content)
- **Design**: CodeMusic/DAEMONS `30f24743`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `9f2ff2226c6d0dac60374771be49da300c40b1d3` |
| `daemonsContext.gba` | CONTEXT | `11f19e26ad7ce539e2b04053447cb418c39055d6` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `abd9d3eaccef5beaf419c410e71cd5d15757cbde` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `ee120bbd7da3360d75dd41d65b87e77e2f20b799` |

## The engine since v11.411.1

- `ed40566e3` T-452: the song-colour table follows CANOPY's restored palette (gencolourbysong --write)
- `6d5d62454` T-452: the arm-C trial's verdict (the user, 2026-11-21: build the draft) -- LODESTAR, REFLECTION, BASTET back to their painted NEXUS art and CANOPY to its old tree, whole (art, palettes, coordinates, follower palettes, icon palette; the three NEXUS streak rows off); WIRETAP's and MONOLITH's backs restored; the other 22 keep arm C
- `2fa11ae08` README: latest is v11.411.1

## The design and tools since v11.411.1

- `30f24743` qa: E-6 a daemon employee's page, on a throwaway copy
- `39ad4037` qa: C-444 CAPS with a pretend cap, on the Mac
- `34441d9a` qa: E-1 THE DASHBOARD's first slice, on a throwaway copy
- `fc91b0a3` Tickets mirror: T-452 closed
- `3276c9dc` Merge branch 'main' of https://github.com/CodeMusic/DAEMONS
- `64f4cb80` T-452: arm C's verdict applied (engine pokefirered-daemons@6d5d62454) -- armc_verdict.json 6 revert / 22 keep; gbanexus REDRAWN emptied (the NEXUS three painted again); buildc.py REVERTED takes the six out of its lists; gfx/daemons and gfx/nexus drawings restored
- `cc56e124` Tickets nightly 2026-11-21: the Redmine export (T-581)
- `c0b7d4ec` Book audio: THE KODE DOT recorded (C-442) -- 14.8 min in lodestone, the user's pick (A of three samples: am_onyx and af_nova, 0.97), with the book's own respellings (Kode said as code, kodeOS, kcli, 125 kHz, EM4100); sources 0683890f0bbaf4f1, current. Its chapter marks keep the page's own words while the voice says the respelled ones (bookaudio WRITTEN_MARKS: "The Kode Dot", not "The Code Dot"); THE CARDPUTERS keeps its marks as recorded, so no other recording goes out of date
- `bc3579e0` C-442: THE KODE DOT, a manual for the Dot (16 pages, DRAFT) -- tools/manual.py's twelfth book, read from the companion's docs/KODEDOT.md, CONTEXT.md and firmware/kodedot/ (C-424, C-426): what the Dot is and its five routines; installing it with kcli and giving it the companion's address over its cable; the pad, TOP and BOTTOM; the den (the day, the daemon drawn by the companion, its care kept on the Dot in order until the companion takes it, every word of its foot); ROUTINES and LODESTONE's READ MY TAG, only the user's own tags; the other four; looking after it; what is still to come, a kept tag never leaving the Dot. Nine screens cropped from kode-sim (qa 19Nov2026 C424, C426), one drawing (a care's way home), a graphite cover with the Dot and ANODE (manual_devices). Its own voice, lodestone (the user's pick, A of three samples), with the book's own respellings in bookaudio (Kode said as code, kodeOS, kcli, 125 kHz, EM4100); its shelf cover; releasedocs routes firmware/kodedot/ and KODEDOT.md to it and takes it as a SET UP book. README and the wiki name it. What is not yet seen on the device is marked so
- `e410790d` qa: E-3 THE EASTER EGG, door to play, on a throwaway copy
- `71c18d7d` CLAUDE.md: THE EASTER EGG on EUDAIMONIA's front page (companion C-437)
- `da9f7617` Tickets: a third Redmine project, eudaimonia (E-), mirrored into daemons-eudaimonia's TODO.md (companion C-411's first point)
- `8100e63a` qa: C-436 EUDAIMONIA's sign-in and accounts, on a throwaway copy
- `7c8ee2cf` CLAUDE.md: EUDAIMONIA's first pieces on port 4741, beside the playground (companion C-436)
- `b1d2819e` Bible v11.412: T-452's arm-C trial viewer released (v11.411.1)
- `8338e4cb` THE PLAYER'S MANUAL's book audio re-recorded after v11.411.1 (the user: release now, record after)
- `756c812a` qa: T-452 arm C old and new (v11.411.1)
- `0b1f38a9` README, wiki: the newest release is v11.411.1
- `d010b1ea` ROM release v11.411.1: T-452's arm-C trial viewer, ART C: OLD / NEW in DEBUG (release ROMs unchanged); seals v11.410.x; THE PLAYER'S MANUAL recorded after (the user)

## The design bible's own entry for v11.412

### v11.412 — 2026-11-20

- Recorded from release v11.411.1 (d010b1ea, engine d7c977174), which sealed v11.410.x:
  - **T-452, arm C on trial** (DEBUG only): ART C: OLD / NEW shows the 28 redrawn daemons old against new for the user's keep or revert; the release ROMs unchanged. In 9.31.
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
