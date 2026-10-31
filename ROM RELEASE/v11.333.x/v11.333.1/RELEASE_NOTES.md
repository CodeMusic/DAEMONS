# DAEMONS v11.333.1 — release notes

*Released 2026-10-31 14:04 · built against the design bible v11.333*

- **Engine**: CodeMusic/pokefirered-daemons `1f232e012` (context-content)
- **Design**: CodeMusic/DAEMONS `d5673bb4`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `4faeaff3aad1d93abff7d39b54053819702534bf` |
| `daemonsContext.gba` | CONTEXT | `923ee95ad9d70689bcc777c836fc234b467b05a5` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `599ed49afe11bbba57e37e1ca5743e1401ce5593` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `f40f39881b62839323315f6ec548fe24cd7951a8` |

## The engine since v11.332.2

- `1f232e012` T-498 (the user, 2026-10-31): the sixth MARK says FORGIVENESS over WRATH, as the week does -- MATTE: "I saw this moment a long time ago. I forgave it then."; "That is forgiveness. Most people stop at the frame."; the insight, the USER card; FLAG_INSIGHT_PATIENCE is FLAG_INSIGHT_FORGIVENESS, the same bit (DRAFT)
- `dc1aec60c` T-493..T-496 (DRAFT): the lioness met four times before the ship, the letter answered at home, a pair of paintings, and not hard but unfamiliar
- `e41d1e091` T-483 Halloween: trick or treat and the Book of Thirteen's card of the day
- `7830af826` T-485: OSRIC HATTER's lines approved by the user -- the DRAFT marks off (comments only; no word changed)
- `121a17906` README: latest release v11.332.2

## The design and tools since v11.332.2

- `d5673bb4` qa: T-498, MATTE says forgiveness -- the words before and after (DRAFT)
- `8635933a` ROM release: v11.332.x sealed -- v11.332.2 kept, the group's notes in ReleaseNotes_v11.332.x.pdf
- `951ca257` T-498 (engine 1f232e012, companion a2f9416): wrath has one answer -- the sixth MARK brings FORGIVENESS over WRATH, as the week does (the user, 2026-10-31; DRAFT)
- `e31da446` qa: T-493 to T-496 -- the two new sprites and the theatre's seven stops (DRAFT)
- `b0d482bc` T-498: wisdom.json -- MATTE's FRAME MARK brings FORGIVENESS (his last line and the insight); notebook_notes.json and the theatre routes follow the flag's new name (the user, 2026-10-31; DRAFT)
- `2bf5fec9` T-493..T-496 (DRAFT): the lioness, the letter, the pair of paintings, not hard but unfamiliar -- bible v11.333 (9.33)
- `f4fb8ab7` qa: C-249 the Tiiny manual and THE TIINY in SETTINGS
- `e02467f5` C-249: A BIGGER MIND, the Tiiny setup manual -- docs/DAEMONS-tiiny-manual.pdf
- `495daa52` TODO: T-498, the sixth MARK says FORGIVENESS over WRATH, as the week does (the user, 2026-10-31); drafting
- `e396e504` qa: C-233 PLAYING TOGETHER on the shelf
- `7414e0fd` .gitignore: the vault unzipped beside itself, docs/books/sealed.pdf, is never committed
- `5ab62a2c` T-497: PLAYING TOGETHER, the social manual -- docs/DAEMONS-social-manual.pdf (A5, 26 pages, thirteen chapters: joining, trading, lending, giving, evolving by trade and PENPHIN, fair play, OUT TOGETHER, friends and dreams, THE COMMONS, the keeper, under the hood, coming next); tools/manual.py --book social prints it from docs/manual-social/ (the player's manual unchanged) and draws {{diagram}} SVGs; ten theatre frames, sixteen companion screens from test companions on synthetic saves; README links it
- `676be35e` T-490: the TRELLIS route -- SPAGHETTI against GARBAGE (special) and FALSETAIL (physical), to replay after a re-judge
- `b8606c1d` qa: T-490 step 2 played in the theatre -- TAMPER reads SP. ATK, TRICKLE in rain, TRELLIS's SPAGHETTI to one GARBAGE
- `3ac66385` CLAUDE.md: a local AI playtester on the Tiiny may run without asking (the user, 2026-10-31)
- `685487f7` T-485: OSRIC HATTER's lines approved (the user) -- lines.md and TODO
- `414e7d6a` wiki: v11.332.2 is from 2026-10-30
- `4b4eac09` README and wiki: v11.332.2; each routine its own category, the weather follows the hit's type (T-490)
- `c3600a25` TODO: T-490 step 2 released v11.332.2; SPAGHETTI left to playtest (the user)
- `723a4d27` manual: rebuilt for v11.332.2
- `0be162d8` ROM release v11.332.2: T-490 step 2 -- weather follows the hit's type; TAMPER, the CORRUPT row, CONSENSUS, PRIOR and WEATHER BALL strike with SP. ATK

## The design bible's own entry for v11.333

### v11.333 — 2026-10-31

- **9.33, The lioness, the letter and the pair of paintings (new section; T-493 to T-496).** The same lioness is met four times before the S.S. ANNE sails: at VIRIDIAN's center, at CERULEAN's, at the gangway and on the deck. On the deck she asks the player to post a letter, and MOM hands over the one-line reply once the ship has gone. A painting's scrambled words, filed from the ship, are read beside its mirrored twin in THE NEXUS. CALLOW SCHOOL's 5F teacher says it isn't hard, only unfamiliar.
- A Settled entry in section 10. Every word is DRAFT.

### Wrath has one answer (T-498)

- ***9.21, the week (the user)***: **the sixth MARK, MATTE's FRAME, brings FORGIVENESS over WRATH, as the GUIDE, THE SUBTLE LAYER and the companion's week say; it brought PATIENCE.** *Every virtue-shadow pair is now the same everywhere; the MARKS keep their own order, one per BENCHMARK. MATTE: "I saw this moment a long time ago. I forgave it then." -- "That is forgiveness. Most people stop at the frame." The insight: "A frame shows what someone did. Forgiveness sees what was there all along, just outside it." DRAFT.*
- ***10, Settled***: **Wrath has one answer.**

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
