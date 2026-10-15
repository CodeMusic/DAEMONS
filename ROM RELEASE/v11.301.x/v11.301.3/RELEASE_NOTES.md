# DAEMONS v11.301.3 — release notes

*Released 2026-10-15 15:16 · built against the design bible v11.301*

- **Engine**: CodeMusic/pokefirered-daemons `b7ada8635` (context-content)
- **Design**: CodeMusic/DAEMONS `d21f624c`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `71910e332ac6ba69d6c856ee8512b81961c700a3` |
| `daemonsContext.gba` | CONTEXT | `86c9992dbfbf2751c40644ed1a6486feb853e740` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `64c7cdc7f04f68d8c26ab441d023becebe63de92` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `2d3df01438d08739a9152ef2784354c202bc4bf7` |

## The engine since v11.301.2

- `b7ada8635` T-403 (the user, 2026-10-15): a NOTEBOOK page says where it was found, what it is, and whether it has been read -- a dot beside a page (and its section) until it is opened, here or where it was found; one line under the list saying what it is (DRAFT), and R opening the TOWN MAP on the place it was found (region_map: InitRegionMapFocusedWithExitCB). SEEN flags at DAEMONS_FLAGS_START+0x200; an old save counts everything already filed as read, once. Played in the theatre.
- `fa5b3e144` T-401, the user's answers (2026-10-15): CAIRN: And take this with you.; the Owl's desk shows FIRST REVIEW before READ AGAIN to a player who never read it; the warehouse says A sheet of hotel paper came with it. before filing NO ADDRESS (the cave's two stay silent); every page is filed as copied it into the NOTEBOOK. DRAFT.
- `d886c21dc` T-401 (2026-10-15): NOTEBOOK pages flow as they are handed over -- the READING ROOM's six shelves and THE STONE open their page full screen (the look lines restated each page's first line); the Owl's desk says copied once for two pages; the museum card shows only the card once its page is held; MINUTES keeps its JAN 2; CAIRN says One more thing once; the Mansion's floorboard holds a sheaf, so copied it agrees

## The design and tools since v11.301.2

- `d21f624c` gitignore: a zip in ROM RELEASE carries the ROMs too -- never committed
- `af7ad350` T-403 struck (engine b7ada8635): tools/gbanotebook.py and docs/notebook_notes.json -- each NOTEBOOK entry's place, line and SEEN flag
- `db5922d7` qa: C-121 -- the M5GO on the bench
- `d21a3ff4` engine.md: the budget against vanilla FireRed, and the save -- ROM +520 KB (6.6 MB free), EWRAM +368 B (736 B free), the save blocks unchanged with their slack, 949 flags and 75 vars free; written by gbabudget.py, which now measures pret's pristine build and asks agbcc for sizeof each save block (the user, 2026-10-15)
- `316ea9ae` T-401 answered and built (engine fa5b3e144); T-403 filed: a NOTEBOOK page says where it was found, what it is, and whether it has been read (the user, 2026-10-15)
- `7cbf5acb` T-401 (engine d886c21dc): the deliveries flow -- gbadocs files a spot's pages with one line and a card's page once; five questions left for the user in TODO
- `bbe4dbc7` ROM release v11.301.2: REST restored where the move sweep reached plain English (T-401), and the debug SOUND row reaches every song

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
