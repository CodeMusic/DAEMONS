# DAEMONS v11.301.7 — release notes

*Released 2026-10-16 10:31 · built against the design bible v11.301*

- **Engine**: CodeMusic/pokefirered-daemons `02bf430fb` (context-content)
- **Design**: CodeMusic/DAEMONS `dae84560`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `ff3af702fb25282af598ca54a69b58b0de729317` |
| `daemonsContext.gba` | CONTEXT | `b26dd6b6fdc99008056cc707cbb854adc8c27aa6` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `50a2e85c0d2b593123692a72d42cc8f9308e4a65` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `3e2a0e470e5fe759f549cade346791b224f8c172` |

## The engine since v11.301.6

- `02bf430fb` Goal B (DRAFT): DaemonsGlitch, a special -- the map's middle layer torn in bands by HBlank DMA and its palettes flickering, then settled; placed nowhere, played from DEBUG -> SOUND -> GLITCH (which stays on the map, unfaded)
- `a5dbe137e` T-409 (DRAFT): in THE NEXUS the Christmas tree's own palette takes the fir's strong light
- `1da69c855` T-409 (DRAFT): the fir's notes seen -- each note lights the map a little and the fir a lot in the painting's colour, the flats a blend in the key; THE NEXUS's own theme, MUS_NEXUS (350), on the fir's notes
- `c1ad7f471` T-408 (the user, 2026-10-16): every grove is a universe -- a sign beside each of THE NEXUS's fourteen doors names it (THE BACKDROPVERSE ... THE CLAYVERSE) and hints where its door is, readable before the grove is found; the game's own sign object, so no tile is spent

## The design and tools since v11.301.6

- `dae84560` qa: the ESP32-S3-BOX-3's faces by voice phase and its device picture (companion C-138)
- `92132c89` qa: the glitch effect draft (goal B, engine 02bf430fb)
- `8e172e7e` T-409: built as DRAFT (engine 1da69c855, a5dbe137e) -- the notes lit, MUS_NEXUS; sent to the user, the key asked
- `92316b53` T-409 (engine 1da69c855): tools/gennexustheme.py writes MUS_NEXUS; gbanexusmap plays it; gbasongs checks CALLOW's and the NEXUS's
- `97ed0cf2` companion_export.py (companion 539a552): the wisdom's flags as numbers
- `93e4c5a7` companion_export.py (companion 7cb1a39): groves.json, the MARKS' wisdom, the PLUGIN and items pockets; the field-test route tops up its repel each stop and clears the Mansion's two trainers before the log
- `bbee9c8c` T-408 (engine c1ad7f471): the universes' names and NEXUS signs in tools/gbanexusmap.py
- `35cb95d1` qa: the device sprites (C-130)
- `0e6c3d03` TODO: the user's answers (2026-10-16) -- T-408's names approved, T-410 in the game too, T-411 keeps craft rule 1 in the game (the PROFILE may title it), T-412 is 21 dreams; the understandings' names to be drafted (T-252)
- `c23823bc` companion_export.py (C-128, C-129, companion 4ac29b6): events.json and school.json
- `a5b0e93e` TODO: T-410 (a MARK and its ROOT say how each balances the other), T-411 (the last note, when every pair is held), T-412 (a DREAM LOG) -- the user, 2026-10-16
- `0b7cb57f` companion_export.py (C-126, C-127, companion 61c9f49): marks.json, regions.json and the eight MARK badges for the PROFILE
- `52a9d61d` TODO: T-405 (STREAM lessons for UNDERSTANDINGS), T-406 (where each daemon was met), T-407 (what it is native to), T-408 (the groves as universes: names, NEXUS signs, looks, music), T-409 (THE NEXUS as Episode 4: the fir's notes as music and as colour) -- the user, 2026-10-16
- `c3aadd74` T-401 closed: the loose pages say what they are about, and every delivery flows (v11.301.2-.3)
- `84f12539` qa: C-121 -- the CoreS3 on the bench
- `e73eec9b` ROM release v11.301.6: THE BAND'S SHEET ends on The Painted Mirror's episode 4 (T-402 closed); the companion reads the NOTEBOOK (C-125)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
