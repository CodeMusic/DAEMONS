# DAEMONS v11.305.1 — release notes

*Released 2026-10-18 19:14 · built against the design bible v11.305*

- **Engine**: CodeMusic/pokefirered-daemons `9a3fa439c` (context-content)
- **Design**: CodeMusic/DAEMONS `da7973e7`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `e0539ce409d19268c45b553669eb57a80ff82c4d` |
| `daemonsContext.gba` | CONTEXT | `7112a364d00525cf30131149741c68ae962c5c97` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `8d2108e01506ec2310ff8efde6c2dbbcd8c3c514` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `87466861eb8608fe59b8c8b75d4688a01f777b24` |

## The engine since v11.304.7

- `9a3fa439c` T-392 P1: every routine signed -- its own codeword as bits and notes, one table and one hook (DRAFT)
- `0febcd7ef` T-421: every CORPUS STAFF trainer gets an animal name of its own (DRAFT)

## The design and tools since v11.304.7

- `da7973e7` qa: T-423 THE SUBTLE LAYER in the companion's library
- `f190b643` T-423: the companion's book carries each picture's frame count (the phone cannot list the art)
- `042883e3` T-423: gensubtle's companion pictures carry nothing set in the game's font (the companion holds nothing of Nintendo's)
- `dbdcf1ef` T-423: placed in BRAZEN's INTERPRETER home, the shelf sparkling as the GUIDE's does (engine 22c2ac28e)
- `7df9bc3c` T-392 P1: tools/gensignature.py, the glyph drafts retired from genanims, animcensus's miscount fixed; budgets (engine 9a3fa439c)
- `ededc36a` T-423: THE SUBTLE LAYER's public source and its generator -- docs/subtle-layer.md, tools/gensubtle.py, tools/subtle_sprites.py
- `5c336498` qa: T-426 PLAY THE HARP on the phone
- `43741b96` T-423: THE SUBTLE LAYER revised after the user's read -- an open book with 50 ink diagrams, THE CONTAINER in the game's own metaphor, the physics added, and STAYING WHOLE
- `7af14452` TODO: T-421's CORPUS STAFF trainers named (engine 0febcd7ef, DRAFT)
- `15a20e90` Bible v11.305: 3.7 WEATHER, 3.8 THE DREAM LOG, 3.9 THE GAME CORNER; 3.5's one voice; saturation built
- `89cd117e` TODO: T-425's game voice approved by ear; CORPUS STAFF trainers get names (the user)
- `14e1f955` ROM release v11.304.7: one voice -- PLAY on our own harp and flute (T-425); the last key kept, SELECT for the sheet's key, the HARP and FLUTE icons (T-417)

## The design bible's own entry for v11.305

### v11.305 — 2026-10-18

### Weather, the DREAM LOG, the GAME CORNER, one voice (T-415, T-412, T-422, T-424, T-425, T-426)

- ***3.7, new***: **WEATHER**, *special and rare, by season; a boost and a weakened type in battle, the tint and the glint, weather daemons, IN RAIN.*
- ***3.8, new***: **THE DREAM LOG**, *your dreams and hers, titled by the user.*
- ***3.9, new***: **THE GAME CORNER as the companion's CASINO**, *the game's own day setting the luck.*
- ***3.5***: **one voice everywhere** -- *our own harp and flute in the game and the companion; the SONGBOOK playable on the companion.*
- ***8, Saturation is friendship***: **built.**

---

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
