# DAEMONS v11.348.1 — release notes

*Released 2026-11-11 11:16 · built against the design bible v11.348*

- **Engine**: CodeMusic/pokefirered-daemons `749b63a86` (context-content)
- **Design**: CodeMusic/DAEMONS `70ef03f7`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `de36147f1be4f47e504d734a1e3fa19c87d6d0ef` |
| `daemonsContext.gba` | CONTEXT | `0e6cc15cc9e3b0ea5deec7849cbee1023a145e29` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `faa32c5f2db1153c8dcfeaf9f10b62438d5e2592` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `f814360e96b9f5cbe99d61e71c070085c49ca039` |

## The engine since v11.346.2

- `749b63a86` T-528 (f): the DUET has its tune -- E D D C D E in C, the hook of Between the Worlds (Painted Reflection), sung most in it (12 times), over its mirror E F F G F E: one note at the start and at the end and a fifth apart between, as the two feet of one field line (the user, 2026-11-11, by ear from four drafts: DUET-1)
- `2953baa67` T-447 pair 6, THE ENDING: the LEAGUE as A THE FOUR VESSELS and the HALL OF FAME as A THE INDEX CARD, redrawn in place -- the REVIEW BOARD's four hearing rooms share one floor, ring and wall-light drawing at the same palette index, and each room's own row carries its member's humour (IV PHLEGMATIC row 8, II CHOLERIC row 9, III MELANCHOLIC row 10, I SANGUINE row 11), the vessels standing along the walls; AL CLEAR's room (row 12) and the stone every room shares (row 7); the HALL OF FAME drawn as the record that files you (rows 7, 10, 11). No block, palette row, behaviour or map moved, 0 new tiles; the nine blocks the engine names (doors 0x28E/0x296, the entry 0x29D..0x2A7, LANCE's floor shade 0x311) keep their ids; the RECORD's six lights stay where FLDEFF_HALL_OF_FAME_RECORD sets the balls; the UNION ROOM's tiles and rows 8/9, the front edge 45..47 and batch G's corridor statues untouched (tools/gbalandmarkrooms.py --pair 6 --write --approved; the user, 2026-11-11: "LEAGUE A The four vessels, HALL A The index card"; DRAFT)

## The design and tools since v11.346.2

- `70ef03f71` TODO T-534: the follower too -- the user (2026-11-11) saw the old MUSAI follower behind the player in the DUET's SONGBOOK picture; once the new look is settled, every form's follower is drawn from it in all four seasons (the game lane, after TULIKKO's sparks). The season is already wired: the follower draws through GetIconSpecies -> DaemonsSeasonalSpecies (T-532); the job is the frames, then gbafollower and gbafollowerpal
- `d4ed8139f` Companion manual: the T-Glass chapter (Glasses in the device list, a rewritten GLASSES section, the wiki's T-Glass page) and the reprinted PDF -- the LilyGo T-Glasses session's work, committed as found (the user, 2026-11-11, so the ROM release could run); its firmware (glass.cpp, night.cpp, app.h) is still uncommitted in the companion
- `a60285340` C-328 (companion): companion_export.py writes battle.json -- the type chart as gTypeEffectiveness has it (the argument, unchanged), every routine's power, type, side, accuracy, MP, priority and effect, every species' experience yield, and the game's own battle words, so the companion's battles are fought by the game's rules
- `a0241354b` Bible v11.348: the torn lines' last line (T-519), DUET-1 (T-528), landmark pair 6 (T-447) -- the user's choices of 2026-11-11
- `e2883d142` C-326: THE WATCH read aloud in its own voice -- bookaudio's 'pocket' (af_sky and bf_emma, a little brisk: bright and close, like something you carry; the user picked A of three samples, 2026-11-11), docs/books/audio/the-watch (24.6 min, DRAFT)
- `4dcbcaee1` T-519: THE UNITY BOOK's recording remade with its new last line, sealed by its own key (29.6 min)
- `1fc70accb` T-519: the torn lines -- THE UNITY BOOK's last line finishes both tears, 'Look again, and you will see them both.' (the user, 2026-11-11, by multiple choice; DRAFT); the third vault reprinted
- `dcf5f9201` qa C326: THE WATCH's cover and controls
- `0f1a15fb9` C-326 DRAFT: THE WATCH, a manual for the T-Watch Ultra and the T-Watch S3 (26 pages) -- tools/manual.py's ninth book, read from the companion's firmware and its wiki's watch pages: first steps, the crown and touch, the wrist, the faces and the Ultra's strip, the pages, CARE, talking and INDEX commands, nights and HOURS, walks, BOOKS and THE INDEX and the memory card, meetings, nearby and TOUCHSTONE, play, the battery and trouble; a drawing of the controls; nothing of the night's hour. BOOKS and the crown to be brought up to C-325 when it lands. shelfcovers' watch cover; bookaudio knows the book and waits on the user's pick of three voices
- `28f27e662` qa: C-327 household together -- two devices' daemons in one den, a feed from the watch eaten in the middle (scratch companion)
- `7aa11eb48` T-528 (f): the DUET's tune, DUET-1 (engine 749b63a86) -- E D D C D E in C over its mirror E F F G F E, the user's pick by ear from four drafts; T-528's still-open now only TULIKKO's sparks
- `2dd823905` T-447 pair 6 BUILT (engine 2953baa67): LEAGUE A THE FOUR VESSELS, HALL OF FAME A THE INDEX CARD -- gbalandmarkrooms APPROVED gains {lg: A, hof: A} (the user, 2026-11-11); the write byte-identical to the drafts, a second write a no-op; named blocks, the RECORD's balls, the UNION ROOM and batch G's statues untouched; pairs 4 and 5 still match; check_generators runs --pair 6 --approved; route t447_pair6.json; qa 11Nov2026 T447 68-73 (their README captions went in with 35fd2d90)
- `35fd2d903` qa C-254: THE MIND's five parts, on a throwaway hub
- `267bd9073` build-pdf.sh: judge Chrome by the PDF it writes, not its exit code (it crashes on teardown after writing)
- `b66a08c5c` Bible v11.347: caught up with work built since v11.332 -- the split's steps 1-2 (T-490), the three-book review's placements (T-502..T-505, T-510..T-516), the hatter's sign (T-500), THE OLD WORD (T-517)
- `cb3f4dcdb` TODO: T-319 kept current (engineAi 79620bc): the agent sees AWAY, SPIRITS, a LOAN and a trade; the brief knows v11.346; T-428 seen on the user's iPhone
- `987477024` Merge review-seen-flags: companion_export's SEEN flags from page 64 up, the DUET slot kept out of the companion, genplaysongs' frame range (9a7c61ca)
- `bf8a97eb6` C-321: THE COMPANION re-recorded in its own voice (friend, 58.9 min) for the refreshed book
- `9a7c61ca7` companion_export: the NOTEBOOK's SEEN flags from page 64 up read the second block, as notebook.c's SeenFlag does; a SONGBOOK slot (the DUET) stays out of the companion, tune or none; genplaysongs: every frame 1-255
- `ec9bfd9f9` Merge branch 'main' of https://github.com/CodeMusic/DAEMONS
- `c0a003a3d` qa T533 63-64: the player's manual and QUICK START tell THE ORIGIN OF A DAEMON
- `da6e1631a` qa: C-271 the companion's 44 faces on the T-452 redrawn art, eight sheets (the user confirmed all)
- `d18d1cc3c` qa: C-271 the companion's 44 faces on the T-452 redrawn art, eight sheets (the user confirmed all)
- `d667c2b9b` Player's manual and QUICK START tell THE ORIGIN OF A DAEMON (T-533), on the bedroom shelf from the start, its chapters coming back as you understand; MICRO-START reprinted unchanged (the line would make it six pages); all three against v11.346.2; manual and quick re-recorded
- `d3a38f1c0` C-321: THE COMPANION brought up to the app -- LISTEN on every MANUAL and THE OLD WORD (C-322), the found shelf's other books in readers of their own (T-533's ORIGIN listed in pages.json), every picture retaken; 71 pages
- `96f9e5765` TODO: T-529 closed (game v11.343.4, companion C-304); T-528 released but for the fox's sparks and the DUET's tune
- `eb47b4cf0` T-533: THE ORIGIN OF A DAEMON read whole in its teller's own voice, sealed -- bookaudio's 'musai' (af_river and am_echo, half and half, even and unhurried: the whole before it branched; the user picked A of three samples, 2026-11-11), docs/books/audio/the-origin-audio.zip (11.4 min, DRAFT), opened in the companion once every chapter is back with the book's own last word (bookpdf.vault_key reads it from the last page; written nowhere); the books README's row
- `4c3dcaf8a` T-447 pair 6 DRAFTED: the LEAGUE + the HALL OF FAME, three directions each (nothing in the engine)
- `10d22be62` ROM release v11.346.2: T-447 pair 5, KEEPALIVE PLANT B GROWING UNTENDED and TANOBY A CARVED, NOT LIT (DRAFT)

## The design bible's own entry for v11.348

### v11.348 — 2026-11-11

- **4.40:** THE UNITY BOOK's last line, "Look again, and you will see them both.", finishes the sentences each torn half breaks off (T-519). The DUET's tune is DUET-1, E D D C D E over E F F G F E, which the user picked by ear from four drafts (T-528).
- **9.29:** six landmark pairs are built. The user chose pair 6: the LEAGUE as THE FOUR VESSELS and the HALL OF FAME as THE INDEX CARD (T-447).
- A Settled entry in section 10. Every word is DRAFT.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
