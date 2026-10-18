# DAEMONS v11.304.6 — release notes

*Released 2026-10-18 16:55 · built against the design bible v11.304*

- **Engine**: CodeMusic/pokefirered-daemons `0ac0c0ca7` (context-content)
- **Design**: CodeMusic/DAEMONS `9ef506f3`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `9407ea1aafe6ab7f0dd7d05cba59847ed3e35bd4` |
| `daemonsContext.gba` | CONTEXT | `a75971c86a743074e596312e26ba118222983a9d` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `548935a46789d217d426ffeb7211010da3999450` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `a7b1d118d43215311be33aa842da2843a0c5af51` |

## The engine since v11.304.5

- `0ac0c0ca7` T-424 (the user, 2026-10-18): saturation is friendship (vision.md 8.5; DRAFT)
- `45ea742a6` T-422 fixes and the machine's surround (the user, 2026-10-18; DRAFT)

## The design and tools since v11.304.5

- `9ef506f3` TODO: T-424 built (engine 0ac0c0ca7, DRAFT)
- `2841ee64` TODO: T-425's companion half done
- `13461daa` audio/instruments: our own HARP and FLUTE (T-425), approved by ear; tools/geninstruments.py follows once the engine job's checks are done
- `ac076df0` TODO: T-425's harp and flute approved by ear (the user)
- `126b40f3` TODO: T-425 -- our own harp and flute, for the game and the companion (the user)
- `845a3e45` TODO: T-422's fixes and surround built (engine 45ea742a6)
- `0af4efc5` TODO: T-425, the companion plays in the game's voice (the user)
- `04abdc84` TODO: T-422's surround to be redrawn (the user)
- `fba8f1e8` qa: C-162 the watch face picker on the phone
- `709f41cf` TODO: T-422 released; two things to fix from the sheet
- `5c22aa0b` qa: T-422
- `4f4cc7c8` ROM release v11.304.5: the GAME CORNER plays as the companion's CASINO -- reels of daemons, luck from the game's own day, the day's note (T-422)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
