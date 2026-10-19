# DAEMONS v11.306.2 — release notes

*Released 2026-10-19 00:38 · built against the design bible v11.306*

- **Engine**: CodeMusic/pokefirered-daemons `39621ac43` (context-content)
- **Design**: CodeMusic/DAEMONS `e16edd29`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `42f37a2a28069af884df22e61ffb8a95c254267c` |
| `daemonsContext.gba` | CONTEXT | `a186ac23b1e12ef57798c872b9793b1d521c37f3` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `10407dd619f5a8accd0d32a23a71d65278fbdb77` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `fc8b920afc304e2d8e2c271235eaa9cff7812217` |

## The engine since v11.306.1

- `39621ac43` DYNAMICPUNCH's description fits its pane once the apostrophe is measured (the user, 2026-10-19)
- `4efbcee49` T-392: PAIRING DAY's heart floats ABOVE the target (the user), two-thirds size, in front of the HP boxes (DRAFT)
- `8df7868dc` T-421 engine LOW: Terminal_RandomNoRepeat with one answer, book_reader's allocations checked, NEXUS_TREE_PALETTE in one place, list scroll arrows read the scroll, a recap CONTINUE gets T-179's fix

## The design and tools since v11.306.1

- `e16edd29` TODO: T-427 confirmed by the user; the take returns to VERDIGRIS after CORPUS falls, with its amount
- `d8412dcf` TODO: T-392's leftovers (the heart above, STILLPOINT in a release battle, seven looks filmed); T-421 worked (engine 8df7868dc, 4efbcee49)
- `382387f5` T-421 (9): engine.md 5 -- START opens the battle theatre, SELECT shows the stats; the box names a poked routine late
- `d06d3419` T-421 (7): check_generators says when it skips gbadocs (its private file missing), in report and --writes
- `6cd96ca2` T-421 (6): index_expand's duplicate ARTSAI and STARR -- the v11.30 lines were dead (the dict kept v11.33's, which ship)
- `16298aca` T-421 (5): gbalabroom's before picture is --before=PNG, not a scratchpad path; gbacard and contactsheet run from anywhere
- `83a9c1ca` T-421 (4): the classic-engine writers write only with --write
- `982cb4a2` T-421 (3): one font-width reader, tools/fontwidth.py -- the apostrophe is 3px, not 0
- `09dbd5ae` T-421 (2): the re.sub over C in gbagrovefamilies, gbanexus, gbaowslots must match exactly once
- `358f4983` T-421 (1): a failed `git show upstream/master:` stops the tool, loudly
- `cf805c14` TODO: T-392 released; the user's three answers
- `367c72f7` qa: T-392 P3
- `f8547f9a` ROM release v11.306.1: T-392 finished -- every signature runs in full, the union routines' own scripts, the holidays' routine looks; seals v11.305.x

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
