# DAEMONS v11.296.3 — release notes

*Released 2026-10-08 08:13 · built against the design bible v11.296*

- **Engine**: CodeMusic/pokefirered-daemons `154ef86f6` (context-content)
- **Design**: CodeMusic/DAEMONS `95caf6e0`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `eb1a346c0e7100992360d2bafb1055dbbaa056e6` |
| `daemonsContext.gba` | CONTEXT | `a3f8f513f5163fe9caf2e4eaa7bbdbfbc58e66ec` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `9f583e975270174f769d0f5951cf41e9486e0786` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `89b3f585928a7ea64f5d2616b47dedb0bd51c903` |

## The engine since v11.296.2

- `154ef86f6` T-387: GOTO is not a bird -- the player comes apart into the splash's 0s and 1s, a ribbon of its notes comes down a swoop of its own (a parabola from above the corner, with a travelling wave along it), and the code goes off with the music; arriving, the ribbon brings the code down and it flickers back into the player

## The design and tools since v11.296.2

- `95caf6e0` T-387 done: GOTO is not a bird -- the player comes apart into code and goes with the music, along a swoop of its own (engine 154ef86f6)
- `8ecf3fd2` T-386 done: the field-test route plays on the release ROM -- 18 of 19 in one run, and the grove (flaky on Route 2's ledges) passes alone
- `3030a03d` T-386: the release field-test route plays all 19 stops -- the walker goes around a scene's trigger when there is another way (CINNABAR's locked gym door and the Reading Room's doorway re-planned through themselves forever), the Reading Room's door is met by stepping up from the door, the museum's scene var is set after GOTO lands, and a route that loads its own ROM is checked against the build after the load
- `30659000` T-386: the release field-test route (19 stops, each back to BLANCHE by loadstate, GOTO to its town, walk in) -- 14 of its first 16 stops passed on the release ROM; continue waits out the recap, GOTO plays out an arrival scene, the START menu is read until it is built. The rest waits on the theatre being started again (the disk filled and its mGBA closed)
- `1720bf76` qa: a release route gets about by GOTO (T-384, T-386)
- `26fa7340` T-386: the theatre swaps ROMs and continues games with no click -- load debug|release, continue (by gMain.callback2, not frame counts), save in the game (START's two columns steered); the DEBUG build saved at PALLET, the release ROM continued there, and a release route's goto flew to VERMILION and fly to CELADON (0 stops failed)
- `7961116c` T-386, the groundwork: the theatre script can load another ROM (emu:loadFile, its save, a reset), reset, and save or load a moment; a route can savestate NAME and loadstate NAME -- so a release route needs no click in the theatre's window. Written, not yet run: the running script must be reloaded once
- `9bcca740` T-384: a route gets about by GOTO on the ROM players get -- fly MAP_FOLDER plays GOTO as a player does (START, DAEMON, a daemon, GOTO, the region map's cursor read from RAM and steered to the town's cell from the ROM's own table), and a release route's goto flies; played in the theatre to four towns and refused cleanly indoors. T-386 filed: a release copy of the field-test route. engine.md: a flight moves gSaveBlock1 too
- `e54a4794` qa: FLARE's WHAT REMOTE IS THIS and the scrolling lists
- `49406952` ai/n8n daemon/talk: 'local' means only local -- a failed local turn falls back to OpenRouter only when the companion asked for auto (pushed live)
- `e5bcc41f` qa: LONGWAVE's FIND IT on the CC1101
- `52971cca` qa: the CC1101's low-battery warning (C-63)
- `f9d903af` qa: LONGWAVE's WHAT'S ON THE AIR on the CC1101
- `fe6f8889` ai/n8n daemon/talk: the goal's one next step, told to the model only when asked about it (never nags), and markdown stripped from what is spoken; pushed live to the internal n8n (companion C-64, C-66)
- `242a272c` qa: the CC1101 talking (C-66) and WI-FI MOTION (C-70)
- `bfd73461` qa: T-385, the GUIDE's day line before and after (v11.296.2)
- `2c144237` ROM release v11.296.2: the GUIDE follows the Xenith week (T-385)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
