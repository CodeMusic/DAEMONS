# DAEMONS v11.343.3 — release notes

*Released 2026-11-07 18:37 · built against the design bible v11.343*

- **Engine**: CodeMusic/pokefirered-daemons `cd9321301` (context-content)
- **Design**: CodeMusic/DAEMONS `ceda27aa`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `097fe843c0a0f6e1a95cbbbf9aad6a268149f6fe` |
| `daemonsContext.gba` | CONTEXT | `c0975dbbe57ad24b40c883c4d6dbeb60dc66a5ad` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `0a9ff0668d9ac8eef1892a66eb3606059aed73ab` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `134ce9da05ebdba2f296c1a9f8f42cd260213ef6` |

## The engine since v11.343.2

- `cd9321301` T-528 part 2: the dawn chorus, TULIKKO the fox, and the conjugate light (vision 4.40; the user, 2026-11-07, by multiple choice)
- `b0a673da8` T-528 (f): PLAY's SONGBOOK has a DUET slot -- shown, and listened for, only under the conjugate light (Aurora_ConjugateLight); played, it echoes on the instrument held with the other edition's part faint beneath it. Its tune is the user's, by ear, so the slot is empty and never shown (vision 4.40)
- `cfa815654` T-528 (f) early: Aurora_ConjugateLight() in daemons_aurora.h -- the book mended and a party daemon whose met game is the other edition

## The design and tools since v11.343.2

- `ceda27aa` T-518: THE SUBTLE LAYER read aloud again for 'a USER's handbook' (617d0f13) -- one line new, the rest from the cache
- `1c0679c5` qa: T-528 part 2's companion half, the conjugate light in the den (C-306, companion 0671747)
- `8e660d76` T-528 part 2 built (engine cd9321301): the dawn chorus, TULIKKO the fox, the conjugate light -- tools/genchorus.py, tools/gentulikko.py, the route t528_aurora_b (nine stops passed), qa 7Nov2026 T528 40-47
- `f960e556` T-528 (f): the DUET slot in docs/play_songs.json (engine b0a673da8) -- its tune and the other edition's part empty, the user's to choose by ear
- `e0b64234` TODO T-528: the companion's half of part 1 is C-305
- `9b85d66d` qa: T-528's companion half, the aurora's nights in the den (C-305, companion 8dfdeee)
- `eda7ad9a` ROM release v11.343.2: T-528 the aurora part 1 (DAEMON TOWER, the grove skies on light nights, the night outdoors); PEWTER's SLATE darkened

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
