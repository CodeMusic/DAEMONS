# DAEMONS v11.295.3 — release notes

*Released 2026-10-04 17:53 · built against the design bible v11.295*

- **Engine**: CodeMusic/pokefirered-daemons `4a5895b45` (context-content)
- **Design**: CodeMusic/DAEMONS `6e0fdfc9`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `f1766d0f0f2b372eabc6a19a32bb1d334e0bf305` |
| `daemonsContext.gba` | CONTEXT | `faf4f9d82cb3864928195647f4b766dfeb4d1ba8` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `26c120b42f6bc25829dce7c14f4b27a02a046182` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `47be5b3043fad594377ebd7d45324595a5c31c02` |

## The engine since v11.295.2

- *nothing: the same engine commit as the release before*

## The design and tools since v11.295.2

- `6e0fdfc9` qa: the daemon at home and its CARE menu, from the board (companion C-13, C-42)
- `96d5f417` companion_export: base stats and the nature table, so a daemon that grew on the companion comes home with the stats the game would give it (companion C-45)
- `ea8879fe` companion_export: SaveBlock1's seen1 and seen2, so the companion marks a daemon seen the way the game believes it (companion C-15)
- `c72977b6` companion_export: each species' growth rate, so the companion reads a boxed daemon's level from its experience (companion C-24, OPUS's margins)
- `d9b08320` qa: the handheld's four screens, captured from the board (companion C-36, C-37)
- `11e7f953` CLAUDE.md: the companion's updateCompanion.sh and linkCompanion.sh
- `af296e94` qa: T-349's iguana and C-29's settings, filed with the v11.295.2 push
- `ba078a1c` ROM release v11.295.2: the companion's link and emergency return (T-370), the lemur on every CHECKPOINT 2F (T-371), the iguana that reads as one (T-349), and only a well daemon goes AWAY (T-374)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
