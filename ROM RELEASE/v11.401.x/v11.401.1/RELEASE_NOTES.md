# DAEMONS v11.401.1 — release notes

*Released 2026-11-18 15:38 · built against the design bible v11.401*

- **Engine**: CodeMusic/pokefirered-daemons `de196c85c` (context-content)
- **Design**: CodeMusic/DAEMONS `faa27ba8`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `9603a03b70d3584b601b8c66bc3bf111640a12a8` |
| `daemonsContext.gba` | CONTEXT | `fcaeed41533b72076e7df3586af78541dd180ccb` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `45616c06adf48523eb4bf14c81a3db1ef169d2b8` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `828fdfdd4155631d0b143cbebe12b11e2be3d9b4` |

## The engine since v11.399.1

- `de196c85c` T-490 step 3: contact is physical, applied (the user, 2026-11-18, every recommendation) -- 67 routines change side (18 to PHYSICAL, 49 to SPECIAL; 10 kept by ruling: LOCK, BACKPROP, OCCLUDE, OVERTRAIN, SLUICE, EMERGE, BURNOUT SPECIAL; UPHEAVAL, TREMOR, BALLISTIC PHYSICAL); the blast halves the defence the hit strikes; Thick Fat halves the stat an ENTROPY or FROZEN hit uses; PAGE FAULT's words (DRAFT)
- `b4f09c0ad` T-592: the six MUS_FUCHSIA maps play the music of the map their door opens onto
- `521a06af6` T-591: the day's symbol on a dream in the DREAM LOG (T-531, DRAFT)
- `1c8df4e59` README: latest is v11.399.1

## The design and tools since v11.399.1

- `faa27ba8` TODO: Redmine's mirror (T-490 closed, pokefirered-daemons@de196c85c)
- `ea814b3f` T-490 step 3: gbasplit.py APPROVED with the user's 10 keeps and written (engine pokefirered-daemons@de196c85c); check_generators runs its write with --approved
- `2542f51f` TODO: Redmine's mirror (T-592 closed, T-593 opened)
- `bc077a08` T-592: the six MUS_FUCHSIA maps play their town's music (engine pokefirered-daemons@b4f09c0ad) -- port_music.py's MAP_MUSIC points each at the map its door opens onto; song-status and the census say MUS_FUCHSIA plays nowhere; T-565's 48 songs heard (qa 18Nov2026 T565 29)
- `96a6ec4f` T-490 step 3 (draft): tools/gbasplit.py reports the 77 routines off 'contact is physical' and their 14 judgement calls; writes only with --write --approved once APPROVED is set
- `0ec8fb81` TODO: Redmine's mirror (T-591 closed, pokefirered-daemons@521a06af6)
- `aeca378d` T-591 BUILT: the day's symbol on a dream in the DREAM LOG (engine pokefirered-daemons@521a06af6, DRAFT); bible v11.401 -- tools/gbadaysymbol.py draws the 49 frames from gendaysymbol's approved paths and each dream's centre table; tools/routes/film_t591_day_symbol.json films a WEDNESDAY dream and one with no day (qa 18Nov2026 T591 26, and 27-28 private: NOTEBOOK pages)
- `15786912` TODO mirrored from Redmine: T-518 and T-519 closed (the user, 2026-11-18: "Close both")
- `6679a27c` qa: C-412 the dream's centre on its symbol (companion 6b930b5e, DRAFT)
- `2b339c12` Bible v11.400: the stat arrow by type (T-589, v11.399.1); a dream's symbol says which centre (T-531, the user: B); 9.5's census claim corrected (23 songs and 43 sounds still pret's)
- `44d79e91` qa: T-589 the stat arrow by type (v11.399.1)
- `fc6737ee` engine.md: the budgets after v11.399.1 (gbabudget --write)
- `05e687a9` README, wiki: the newest release is v11.399.1
- `d366df30` ROM release v11.399.1: T-589 the stat arrow by type (DRAFT); seals v11.398.x

## The design bible's own entry for v11.401

### v11.401 — 2026-11-18

- **The day symbol in the game's DREAM LOG** (T-591, built 2026-11-18, engine 521a06af6, DRAFT): each dream wears the symbol of the weekday it came on, with the spine and its centre lit; the day saved when the dream arrives. In 9.21 and 3.8. Not yet in a release.
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
