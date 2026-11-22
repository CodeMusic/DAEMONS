# DAEMONS v11.412.8 — release notes

*Released 2026-11-22 13:22 · built against the design bible v11.412*

- **Engine**: CodeMusic/pokefirered-daemons `d9ca5b780` (context-content)
- **Design**: CodeMusic/DAEMONS `41df5895`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `b3240ee62b912b3505471a5ed3707995508f39d9` |
| `daemonsContext.gba` | CONTEXT | `db2b23448fc96797ae6ff12b77fe7a648651c0a9` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `cc76e73418dd314bcf62c75180be9e909fe48440` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `cb50a3902917fb20daca9c4f3f5780d1a0780485` |

## The engine since v11.412.7

- `d9ca5b780` T-604: the shiny-song table follows stage 1's new shiny palettes (genshinysongs --write; only the nine forms' rows move)
- `9625c272c` T-604: stage 1 -- nine later forms colour in as they learn their part: a region in the new part's colours (ROVERSEER's ears, ROVERBYTE's SIGNAL cap, RUBRIC's red-pen faces and grid, CANON's brass drawers, LOCUS's amber tail, MANIFOLD's mulberry LATENT underside and wing tips, REFORGE's ember forge, LANGMUSAI's coral tail and antennae, HOPE's coral wing tips and tail feather), DRAFT
- `b15b3aff5` T-602: shiny songs (DRAFT) -- a shiny sings its kind's song with the notes its shiny palette moved (src/data/daemon_song_shiny.h, 1364 notes in 380 forms, from DAEMONS tools/genshinysongs.py --write): SONG_SHINY on DaemonSong_Start and a shiny flag on DaemonSong_Hum, DaemonSong_MonMode; the INDEX's SONG, the follower's song and hum, the party's SING and the evolution scene sing a shiny as a shiny; the summon and T-597's colours stay its kind's
- `9a4475a8c` README: latest is v11.412.7

## The design and tools since v11.412.7

- `41df5895` Tickets mirror from Redmine
- `b85da7f5` Merge branch 't604'
- `87c4d562` qa C-433 (4, 5): QUIZ and MINE
- `c47dd369` qa: C-434 the BACKUP card on a scratch hub -- off, the recovery code shown once, on
- `d2a5980d` C-321: THE COMPANION reprinted with the DREAM-BOOKS shelf's covers whole (companion 37dcf5d8)
- `36117267` T-604: stage 1 -- nine later forms colour in as they learn their part (engine 9625c272c, companion 94e4e520), DRAFT
- `e125e103` C-321: THE COMPANION reprinted with BALANCE lit and "1 STEP" (companion 7aead917)
- `b4a0769a` qa C-321: THE COMPANION's new pages (THE WEEK'S BALANCE, MENTIONS FROM YOUR DAEMON, the DREAM-BOOKS)
- `57e2a71d` C-321: THE COMPANION covers THE WEEK'S BALANCE, MENTIONS FROM YOUR DAEMON and the DREAM-BOOKS (DRAFT) -- the STALE TestFlight 994 and 995 shipped with
- `6bc9a438` Tickets mirror: T-602 closed
- `2e00f371` T-602: genshinysongs --write -- the engine's shiny table (engine pokefirered-daemons@b15b3aff5; the user, 2026-11-22: "Yes, build it"; DRAFT)
- `871c7b0f` qa: T-606 played in the theatre -- the mending first, the ball where INIT knelt, the book from the bag; its route waits out a new day's dream and checks the book is held
- `d4219656` qa C-433 (3): LEARNING
- `7fb23dd2` qa C-433 (2): RECIPES
- `2c6aec17` T-604 (draft): stage 1 -- a region in the new part's colours for the starters' later forms and the story daemons' (ROVERSEER, ROVERBYTE, RUBRIC, CANON, LOCUS, MANIFOLD, REFORGE, LANGMUSAI, HOPE), recoloured from each drawing; judged by gencolourbysong's own maths; contact sheet (DRAFT)
- `80cd019a` E-12: tickets.py mind -- a lane's WORKING MEMORY on EUDAIMONIA, written as the lane (eudaimonia 0bd475f); CLAUDE.md: hold what is in flight, waiting and next with the handoff
- `2481b657` qa C-433 (1): THE REWARD SHELF
- `141f9c11` The Fourth Review's witching-hour finding keeps its point and loses the hour's code (the user, 2026-11-22, by multiple choice: "Mark it private"): the condition now reads [private: vision-unredacted 4.39]; The-Fourth-Review.pdf reprinted.
- `7c78d6b7` T-602: shiny songs drafted -- tools/genshinysongs.py: a shiny's song is its kind's, its words' notes stepped toward the notes its shiny palette's colours name (SYNESTHESIA), the contour, opening, cadence, rhythm and learning kept; sampler and sheets in audio/drafts/t602_shiny (DRAFT)
- `073fbaff` Merge branch 'main' of https://github.com/CodeMusic/DAEMONS
- `af988be9` Tickets mirror: T-445 closed
- `767462fa` qa: C-419 (3) PLAY FREELY summons (22Nov C419 13)
- `d395afa6` PDFs reprinted for v11.412.7: THE PLAYER'S MANUAL (THE SPELL LEFT RUNNING among the books) and THE SPELL LEFT RUNNING (T-606)
- `e80723ec` C-419 (3): gensongs.py exports T-598's openings into the companion's songs.json (summons), so the app's PLAY FREELY hears a daemon's song as the game's PLAY does
- `2ef46e4b` qa: T-445 the LURID gatehouse, THE PALE and TENDED BEDS (v11.412.7)
- `bf66c0f8` README and wiki: latest is v11.412.7
- `fb6fbcec` ROM release v11.412.7: T-445 THE WALLED GARDEN's gatehouse in LURID, its last Nintendo tiles redrawn -- THE PALE and TENDED BEDS (DRAFT art)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
