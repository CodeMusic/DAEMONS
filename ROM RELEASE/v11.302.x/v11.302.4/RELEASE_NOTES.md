# DAEMONS v11.302.4 — release notes

*Released 2026-10-17 23:51 · built against the design bible v11.302*

- **Engine**: CodeMusic/pokefirered-daemons `35b0a536f` (context-content)
- **Design**: CodeMusic/DAEMONS `f3b4ef1b`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `c08f2285a439f56f16dbb508d3cebe5f1bc21227` |
| `daemonsContext.gba` | CONTEXT | `c9468796a8b39b6230f02ecc3495d357fb538a5e` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `56b111f0a589d5217dc09dd11ebc35a41cd41b89` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `c31fdd7fa93e3e32f98292de453057f13a43356e` |

## The engine since v11.302.3

- `35b0a536f` T-408 (the user, 2026-10-17): each grove its own music -- 14 loops from the user's own songs, MUS_GROVE_*, each universe its own band on voicegroup191 (tools/gengrovemusic.py)
- `34b59e932` T-417 P4 (the user, 2026-10-17): the seven songs -- heard in their ROOT's places, played back to be learned, and what each does (DRAFT)
- `12411c360` README: the game as it stands at v11.302.3 -- the ROMs by edition name, the debug menu as it is now (GAME EVENTS, JUMP, ENCOUNTER, TIME, SOUND), what a player meets (the clock, seasons, weather, PLAY), and how much is ours, measured against upstream

## The design and tools since v11.302.3

- `f3b4ef1b` T-408 grove music built (engine 35b0a536f): tools/gengrovemusic.py, gbagrove keeps each grove's slot; companion_export gives each SONGBOOK page its key and notes (T-417); T-419 opened for the user's ear
- `1ba8457c` T-417 P4: the seven songs built (engine 34b59e932) -- docs/play_songs.json and tools/genplaysongs.py, its shape check
- `e99f223b` README and wiki: the whole game playable and every daemon ours; the world page (the clock, the seasons in two hemispheres, weather by season, PLAY's HARP and FLUTE, the NOTEBOOK); the debug menu as it is now; the companion's hosts and its CASINO in the game's money (engine README 12411c360)
- `ab715ac7` qa: C-150 -- FLARE's WHAT REMOTE IS THIS on the T-Embed CC1101, its receiver made from the board's own pin
- `a6951530` qa: C-149 -- the CASINO on the T-Embed CC1101, a jackpot
- `7035bc53` qa: C-149 -- the companion's CASINO on the Fire and the M5GO, from their own screens
- `a124827c` TODO: T-416's THE YEAR, T-417 P3's two answers
- `4c4bd6c2` ROM release v11.302.3: PLAY P3 -- the LYREBIRD gives the HARP at CALLOW SCHOOL, the FLUTE under FINDERS BEACH's palm (T-417)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
