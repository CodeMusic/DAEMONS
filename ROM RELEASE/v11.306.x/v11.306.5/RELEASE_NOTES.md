# DAEMONS v11.306.5 — release notes

*Released 2026-10-19 08:26 · built against the design bible v11.306*

- **Engine**: CodeMusic/pokefirered-daemons `79d410515` (context-content)
- **Design**: CodeMusic/DAEMONS `fb4765b6`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `969506b770a801ee6065ea96fbf6fbadf7548bdd` |
| `daemonsContext.gba` | CONTEXT | `2c057f89d8f4799ac0b369fea80e05268d087da9` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `2840f1fdeb498250df14480c72b65be2a42ae2b1` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `22ff1e08874468be1536505251a986c36835202a` |

## The engine since v11.306.4

- `79d410515` T-408: each grove's universe in its own light -- its map's BG palettes shifted to the universe's mood (DRAFT)

## The design and tools since v11.306.4

- `fb4765b6` T-408: a palette per grove universe -- tools/gbagrovemood.py (engine 79d410515), DRAFT; gbabudget
- `dd3a9428` T-210: the 110 approved INDEX entries' DRAFT marks come off (the user, 2026-10-19)
- `4c52a01a` T-428: the playground -- CodeMusic/daemons-playground, linked as playground/ (setup.sh step 6/7, gitignored); CLAUDE.md names it; the TODO row built (the user: its own public repo, daemons-playground)
- `ae515f57` qa: T-427 frozen at the fall
- `f0e459be` ROM release v11.306.4: the take VERDIGRIS names freezes at CORPUS's fall (T-427)
- `9a22327a` TODO: T-428 -- the game in a browser, for beta testing (the user), claimed

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
