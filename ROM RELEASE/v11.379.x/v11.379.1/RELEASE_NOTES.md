# DAEMONS v11.379.1 — release notes

*Released 2026-11-16 14:07 · built against the design bible v11.379*

- **Engine**: CodeMusic/pokefirered-daemons `251e985ce` (context-content)
- **Design**: CodeMusic/DAEMONS `69d8d95c`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `62c377376c69997b9b6fc2984aaac096f9ebf6fd` |
| `daemonsContext.gba` | CONTEXT | `4413dd30f5d1797cff256cd77b1727acc3590289` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `be78c1ca6d3af3d7bb6733290f1170ae2d7689ca` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `3fa725dad6b53de7e9bf3e8d56ba39031cf28ecb` |

## The engine since v11.376.1

- `251e985ce` T-570: the islands' and caves' last tiles, hand-drawn -- rungs-and-rails ladders, broken-lip holes, glare-and-glint ice, the rest in keeping (the user's picks, DRAFT; tools/gbaislands.py --t570); THE BLACKOUT, THE TUNNEL and TANOBY untouched
- `cd7541f4c` README: the release line names v11.376.1

## The design and tools since v11.376.1

- `69d8d95c` T-560: the smoke run from the title screen, played on the Tiiny's 35B (engineAi ef04fc4, 3467d7a)
- `eacf83f5` T-570 BUILT: the last island and cave tiles, the user's picks (engine 251e985ce)
- `ff7a5530` qa: C-380 the Cardputer Zero away from home, through the relay
- `6e54552c` Book audio: the nine recordings behind, made current (subtle, the three sealed books, the player's manual, the companion, playing together, the watch) and THE GLASSES recorded for the first time
- `2dcf60f1` T-506, the manual's two lines softened to rumour (bible v11.379): the user, by multiple choice, "Soften to rumour". The player's manual now says only that nobody agrees how THE HERMETIC LAYER is found (DRAFT), printed again; the Open-log question closed; the T-506 row no longer quotes the old lines.
- `651e468d` qa: C-335, the Ultra's UPDATE in PLACES on a scratch hub
- `4725d53b` qa: C-380 the Cardputer Zero's SYNC and C-215's question
- `1f49e48c` T-547 and T-539 filmed (debug ROM cd7541f4c; qa 16Nov2026 15-21, private): the Blank Tablet's two faces, their thirteenth lines and the old toad (7/7, tools/routes/film_t547_blank_tablet.json); THE UNITY BOOK's LENS page read whole (1/1). T-539 struck.
- `159d9ed4` T-506 DONE, bible v11.378: the third book's gate leaves the public writing
- `45a40811` qa: C-381 the Cardputer Zero's companion screens (HOME, PARTY, CARE, STEP, SAY)
- `954e3b81` Manuals: THE COMPANION tells THE MESH (C-360: every machine sharing the work, THIS PHONE IN THE MESH), THE ENGINE ROOM's KEYS, JOBS, CREATIONS and SAVES (C-361, C-364), and the companion's copy as the true save (C-365); its pictures retaken. THE WATCH: a reading as loud as its sounds (C-324), BOOKS gone back to where it opened. Both reprinted
- `81b99ad6` qa: companion C-385, THE CALENDAR on the twelve-tone wheel
- `a71d4a9a` Companion manual: the months on the twelve-tone wheel, the month's key and the day's beat (companion C-385, C-386: b55523f, dc96dea)
- `98b5e570` Bible v11.377: the books from their sources (T-571, v11.376.1)
- `6614b117` TODO: T-319 kept current to v11.375.1 (engineAi 79a13f0: the PORT's name from FireRed's flag, USERS, DETACH, THE BLANK TABLET); T-560 closed, the 9B thinking-on run unrun by the user's pick (engineAi 49ef4f6)
- `c62fe368` README and wiki Home name v11.376.1
- `c0699909` ROM release v11.376.1: T-571 the books from their sources -- THE SUBTLE LAYER says USER, THE CONTAINER's last page three lines (two DRAFT words); seals v11.375.x; two recordings deferred

## The design bible's own entry for v11.379

### v11.379 — 2026-11-16

- Section 10, Open: **the player's manual keeps neither of the third book's two lines** (T-506; the user, by multiple choice: "Soften to rumour"). The manual's rumour now says only that nobody agrees how THE HERMETIC LAYER is found, or whether it is found at all (DRAFT); `docs/DAEMONS-manual.pdf` printed again. The T-506 row in TODO no longer quotes the old lines.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
