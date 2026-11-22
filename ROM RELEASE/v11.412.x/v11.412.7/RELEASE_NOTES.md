# DAEMONS v11.412.7 — release notes

*Released 2026-11-22 10:21 · built against the design bible v11.412*

- **Engine**: CodeMusic/pokefirered-daemons `f9d572554` (context-content)
- **Design**: CodeMusic/DAEMONS `5a5132fd`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `4d4c954a2438bdcee1978496f874384dcc7055d9` |
| `daemonsContext.gba` | CONTEXT | `5f4a71dbbb0f827e5343ae84ffe085b6f2542ebb` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `47e0adcb0d0aa60c1162faf7ca1e5a2e90c0e7f0` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `06aca393dc0dc433020dba380a4f67d11c684078` |

## The engine since v11.412.6

- `f9d572554` T-606: THE SPELL LEFT RUNNING in the reader (BOOK_SHADOW), its SHADOW BOOK, and found where INIT knelt on DAEMON TOWER's top floor (the user, 2026-11-21/22; words DRAFT)
- `97ba78e07` T-445: LURID gate's green low wall, B TENDED BEDS, its four neighbours matched (DRAFT art)
- `be9dcb421` T-445: LURID gate's last three pret tiles, B THE PALE (DRAFT)
- `91358ed43` README: latest is v11.412.6

## The design and tools since v11.412.6

- `5a5132fd` Player's Manual: THE SPELL LEFT RUNNING among the books (T-606; where it lies left to the game)
- `8650f728` TODO: Redmine's mirror (T-606 closed)
- `ce462e31` qa: T-606 THE SPELL LEFT RUNNING, built -- where it lies, and in the reader (DRAFT)
- `155895bd` Merge branch 'main' into shadow-book
- `673fce5c` T-606: a theatre route for THE SPELL LEFT RUNNING -- the mending first, then the ball where INIT knelt, then the book from the BAG
- `49348c8d` qa C-432 (1): THE WEEK'S BALANCE on TODAY
- `61aeda3a` CLAUDE.md: EUDAIMONIA has one package now (PRAXIS's engine), and THE SPACES (E-9, E-10)
- `015fcb73` T-319: check_agent_vocab lets SING through -- the party menu's command since T-595 (the move SING is LULLABY)
- `96f0d46c` T-606: THE SPELL LEFT RUNNING's voice is the Sorcerer's (A, picked by the user from three samples, 2026-11-22)
- `d1bd8635` T-445: LURID gate's green low wall BUILT, B TENDED BEDS, 45/46/57/58 joined to it (engine 97ba78e07)
- `2ee30810` T-445 (draft): LURID gate's green low wall, three options
- `8ce84a43` T-445: LURID gate's last three pret tiles BUILT, B THE PALE (engine be9dcb421)
- `e58f8d96` T-445 (draft): LURID gate's last three pret tiles
- `a151a14e` qa: T-445 SCORN SOLUTIONS and ERRATA, their cards built and walked into (v11.412.6)
- `4826a5c0` README and wiki: latest is v11.412.6
- `1147295f` ROM release v11.412.6: T-445 SCORN SOLUTIONS and ERRATA are places of their own, each with its name card (DRAFT)
- `9f678e61` Merge branch 'main' into shadow-book
- `596cebfa` T-606: gensubtle writes THE SPELL LEFT RUNNING into the reader (its cover and icon from shadow_art.py); BOOK_SHADOW wired in
- `28deabfd` qa: T-606, THE SPELL LEFT RUNNING's reader pictures and the reader mock with them (DRAFT, branch shadow-book)
- `31c20ffe` T-606: THE SPELL LEFT RUNNING's pictures for the game's reader, its cover and its icon (the user, 2026-11-22: "Yes, draw them"; DRAFT, not on main)
- `a42500e7` T-606: found where INIT knelt, on DAEMON TOWER's top floor once he has gone home (the user, 2026-11-21); the Unity Book lane's two cautions
- `6e1d3179` T-606: THE SPELL LEFT RUNNING is found at DAEMON TOWER (the user, 2026-11-21); the exact spot left open
- `9608c978` qa: T-606, THE SPELL LEFT RUNNING in the game's reader, a mock (DRAFT, branch shadow-book)
- `042907ec` T-606: THE SPELL LEFT RUNNING's game version, drafted -- docs/shadow-book.md, measured by gensubtle --book shadow (the user, 2026-11-21: "Draft the game version"; DRAFT, not on main)
- `f2c0407b` qa: T-606, THE SPELL LEFT RUNNING's identity, six pages (DRAFT, branch shadow-book)
- `30783af4` T-606: THE SPELL LEFT RUNNING's architecture and identity (the user, 2026-11-21: "continue to produce the architecture of the book, the context, and the diagrams, and the look & feel"; DRAFT, not on main)
- `693db9b9` qa: THE SPELL LEFT RUNNING's first draft, six pages (DRAFT, branch shadow-book)
- `ef806e5c` THE SPELL LEFT RUNNING, a book of shadows: the first draft (the user, 2026-11-21; DRAFT, not on main)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
