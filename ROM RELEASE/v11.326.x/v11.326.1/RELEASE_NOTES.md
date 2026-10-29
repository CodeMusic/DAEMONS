# DAEMONS v11.326.1 — release notes

*Released 2026-10-29 12:39 · built against the design bible v11.326*

- **Engine**: CodeMusic/pokefirered-daemons `157902645` (context-content)
- **Design**: CodeMusic/DAEMONS `4124cf0e`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `dc37d06e23ef475dd122951a427e66f057beb0be` |
| `daemonsContext.gba` | CONTEXT | `a3f9c2422a7215dce6aba501ed0a5f85f31b281a` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `9b99e3514a45df12937f9772270769f8c544d154` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `43b818634e046c8e52e36c0c335d05a9ed085937` |

## The engine since v11.325.1

- `157902645` T-481 A: the battle backgrounds keep the calendar -- the season, the holiday, the weekday, the hour
- `ae6bc9901` README: latest release v11.325.1

## The design and tools since v11.325.1

- `4124cf0e` TODO: T-485 drafted and the user's answers; T-486's strength follows the clock (the user); engine.md's numbers
- `4df3d2c4` Bible v11.326: Al is 4.3, not 4.4
- `8ccf66d3` Bible v11.326: Al after the REVIEW BOARD, a plateau with one crack (T-487); a stale Open question struck
- `6feab0c4` T-481 A: gbabattlebg.py --write --approved (the battle calendar's tables into the engine), check_generators runs it with --approved, and the theatre route that films it
- `5ac9524d` T-485 draft: OSRIC HATTER's house on QUICKSILVER -- the leaning hat at (9..11,11..13) in row 12 (28 of 30 free tiles), the room of stopped clocks, the stoat, eleven riddles measured, four questions (DRAFT)
- `604fc8de` TODO: T-483 first part, T-482, T-486's warning page -- released v11.325.1
- `330ace6c` manual: BOOKS -- the two books side by side and the GUIDE's margins; THE HERMETIC LAYER as a rumour, with its real history (never where or how) -- the user, relayed by the README/wiki session; qa 29Oct2026 T467 37-38
- `050d58fb` README and wiki: the newest release is v11.325.1
- `57abc41d` manual: rebuilt for v11.325.1
- `15ffc999` ROM release v11.325.1: T-483 THE HERMETIC LAYER in the game (the book, its unlock, the world's breath, the handless clock, Halloween's costume); T-482 the battle's ground breathes; T-486 the only glitch; v11.322.x sealed

## The design bible's own entry for v11.326

### v11.326 — 2026-10-29

### Al: a plateau, with one crack

- ***Al Clear (Open since the start), the user by multiple choice***: **after the REVIEW BOARD he stays the incumbent, and once, late, nearly notices** -- *"...It was wrong about that. / Probably a rounding error."* (DRAFT). No arc, no rescue. T-487.
- ***Open log***: "Does the player meet Scorn before Halftone Tower?" struck -- 8.6 had settled it (the Verdigris basement).

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
