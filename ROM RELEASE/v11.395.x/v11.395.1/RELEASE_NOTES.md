# DAEMONS v11.395.1 — release notes

*Released 2026-11-18 00:59 · built against the design bible v11.395*

- **Engine**: CodeMusic/pokefirered-daemons `3dd7db7fc` (context-content)
- **Design**: CodeMusic/DAEMONS `11f70c83`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `984efc555fda417aa4cc6f67335a7aae2a6fa6c7` |
| `daemonsContext.gba` | CONTEXT | `22ee8717eba3f458484c20612916e04949031364` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `95e6e44107c2ddd390d51dae4db9bb10757325e4` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `74be37164bc007af7a070582fd0be8f14ae295c3` |

## The engine since v11.392.1

- `3dd7db7fc` T-587: what DAVID's compass does once read (the user, 2026-11-17; DRAFT). Read, the rose opens holding and the needle swings from north to one of eight bearings for where you stand (Compass_Aim): a BENCHMARK gym, it will not settle; DOLDRUM CAVE spins until FLAG_UNDERSTANDING_FIRST, then settles on the way in; a dark cave or THE BLACKOUT points to the way in (the arrival warp, or the tile set down on) with the rose dark and the needle the one faint glow (window palette row 13 only: THE BLACKOUT's rows 0..12 untouched); surfing, the nearest land within 24 tiles; both torn halves held (HERMETIC, EUDAIMON), in HALFTONE TOWN, DAEMON TOWER's door; anywhere else outside BLANCHE TOWN, MOM's house, bearing taken on the region map's cells (DaemonsMapsecPlace) from outdoors or the escape warp; from the islands' sheets, north-east. Never the clock, the GUIDE, a layer or a grove. No EWRAM or IWRAM; no words.
- `521ac9c67` T-586: DAVID's compass and the NEXUS arrival (the user, 2026-11-17; every word and the drawing DRAFT). DAVID, rubbed, goes back to his book ("It has every step in it. / It never says where to look.") and the player chooses (MULTICHOICE_DAVID_ADVICE): KEEP READING -- still seasick, the ship waits, ask again (FLAG_TEMP_1 skips the rub within a visit); LOOK OUT THE PORTHOLE -- he steadies ("in one long line that held still"), then PRUNE, the band's sheet as before and the COMPASS ("I can see where I'm going now. / You'll need this more than I do."), and only then VAR_MAP_SCENE_VERMILION_CITY = 1. ITEM_COMPASS (was ITEM_0FC, unused), its icon from DAEMONS tools/gencompass.py, FieldUseFunc_Compass -> EventScript_Compass -> special Compass_Open (src/daemons_compass.c): the rose over the field on graph paper, lettered in the ship painting's mirror alphabet (M V H D); up/down turn a letter, left/right choose one, no words on screen; wrong, the needle spins; N E S W, the rose holds, the needle swings to north and rests with SE_PIN, and FLAG_COMPASS_READ (DAEMONS flags + 0x1F0) is set. With it read, EventScript_SingingFir (DAEMONS tools/gbanexusmap.py) asks special Compass_CurrentMap and warps from a grove's fir to the cell before that grove's NEXUS door; the pier's fir, and every fir without it, still at the Christmas tree. DEBUG -> GAME EVENTS: DAVID'S COMPASS and THE COMPASS, READ. Heap only while open; no EWRAM or IWRAM.
- `7627ffeb2` README: the release line names v11.392.1

## The design and tools since v11.392.1

- `11f70c83` TODO: Redmine's mirror (T-587 closed, pokefirered-daemons@3dd7db7fc)
- `566051f1` T-587: DAVID's compass once read (engine pokefirered-daemons@3dd7db7fc, DRAFT) -- tools/routes/film_t587_compass_uses.json films the rose in THE BLACKOUT, DOLDRUM CAVE before and after understanding, DOLDRUM CITY, surfing, HALFTONE TOWN without and with the torn book's halves, and a BENCHMARK gym (qa 18Nov2026 T587 1-8)
- `8607e086` TODO: Redmine's mirror (T-586 closed, pokefirered-daemons@521ac9c67)
- `1d6c5e71` T-586: DAVID's compass and the NEXUS arrival (engine pokefirered-daemons@521ac9c67, DRAFT) -- gbanexusmap.py's singing fir, with FLAG_COMPASS_READ, warps out of a grove beside that grove's own NEXUS tree (arrive_at, the cell its door answers from); tools/gencompass.py draws the bag icon; tools/routes/film_t586_compass.json films DAVID both ways, the rose wrong then right and a grove trip before and after (qa 17Nov2026 T586 30-36)
- `bd4a8751` TODO: Redmine's mirror (the compass's uses)
- `97bc410d` TODO: Redmine's mirror (DAVID's compass)
- `4c7291fc` Bible v11.395, T-585: the magpie found its stone (the user) -- "It was warm, the day I found it."
- `11219315` Bible v11.394, T-585: THE GARDEN OF ECHOES as the three at the fir (the user, by multiple choice: A); lineage 4.7 and the draft record the pick; TODO mirrored from Redmine
- `0c9b5fc4` Lineage 4.7: The Garden of Echoes (Seeing Sharp, 2025-06-11), three ways of holding one experience; three ways into the game drafted (docs/garden-of-echoes-draft.md, DRAFT, nothing in the engine)
- `0d975cec` Bible v11.393: our own instruments, the sound census done (T-565 batch 12, v11.392.1)
- `a2c501c8` qa: T-565 batch 12's instruments as built, the sheet sent with the push
- `5d5fee30` README and wiki Home name v11.392.1: our own songs on our own instruments
- `21ea79d9` ROM release v11.392.1: T-565 batch 12, our own instruments under our older songs (DRAFT); seals v11.391.x

## The design bible's own entry for v11.395

### v11.395 — 2026-11-17

- **The magpie found its stone** (T-585; the user, 2026-11-17): its first line is now "It was warm, the day I found it." (DRAFT), not "took" -- the magpie was given the light as the hare was, and its mistake is the keeping, not the taking; "took" would have judged it before the player could. In 3.4, and in `docs/garden-of-echoes-draft.md`.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
