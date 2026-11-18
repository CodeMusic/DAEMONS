# DAEMONS v11.389.1 — release notes

*Released 2026-11-17 21:23 · built against the design bible v11.389*

- **Engine**: CodeMusic/pokefirered-daemons `e97afa9cb` (context-content)
- **Design**: CodeMusic/DAEMONS `dca80834`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `26f8477608157dae7121bd23f466fe0f608123c1` |
| `daemonsContext.gba` | CONTEXT | `1366e66f5b296d785bb9e86de4dc5144b826c745` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `9a0347bfc196d278291618d38af614b3c6e80f01` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `7255f53e995c3f8d44bbb5c5243d518024f08daa` |

## The engine since v11.388.1

- `e97afa9cb` T-565 batch 10: the 115 move sounds in C BOTH -- each type's palette (a motif, a register, a texture) in the shape of what the sound does; hits on the noise channel, a stat falling on the tritone (the user's pick, DRAFT; tools/genuisounds.py --batch 10)
- `b4c743040` README: the release line names v11.388.1

## The design and tools since v11.388.1

- `dca80834` gbalandmarkrooms knows genstorymusic and genuisounds: they name songs and sounds (MUS_HALL_OF_FAME, MUS_SS_ANNE, SE_SS_ANNE_HORN), not tilesets
- `ff82a77e` TODO: Redmine's mirror (T-583 the shared move sounds, later)
- `b3023bff` Bible v11.389: the story's music and the field sounds (T-565 batches 8 and 6, v11.388.1)
- `4447ee78` T-565 batch 10: the move sounds, a palette per type -- 115 SE_M_* in C BOTH (the user's pick, DRAFT; genuisounds.py --batch 10)
- `e5a96b5b` qa: T-565 batch 8's story set-pieces as built, the sheet sent with the push
- `a3c2af4e` README and wiki Home name v11.388.1: the story has music of its own
- `1f4495e2` ROM release v11.388.1: T-565 batch 8, the story set-pieces in C and THE WALLED GARDEN's own song (DRAFT); T-565 batch 6: the 41 field sounds in C BOTH (DRAFT); seals v11.387.x

## The design bible's own entry for v11.389

### v11.389 — 2026-11-17

- Recorded from release v11.388.1 (1f4495e2, engine 586ed7e8b and 8fc425637), which sealed v11.387.x:
  - **The story set-pieces** (T-565 batch 8, the Musical Instruments lane): CRYSTAL CLEAR's entrance and lab, AL CLEAR's two, DAEMON TOWER, the credits' medley and the rest, in voice C; **THE WALLED GARDEN's own song**, `MUS_WALLED_GARDEN`. DRAFT. In 9.5, and a line in 3.11.
  - **The field sounds** (T-565 batch 6, the game lane): 41 in C BOTH. DRAFT. In 9.5.
  - Also in the release, outside the bible: the tickets moved to Redmine (T-581, the user's "Apply and switch"); the TODO files are now its nightly mirror.
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
