# DAEMONS v11.304.7 — release notes

*Released 2026-10-18 17:38 · built against the design bible v11.304*

- **Engine**: CodeMusic/pokefirered-daemons `08acb5f6a` (context-content)
- **Design**: CodeMusic/DAEMONS `9ffa1817`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `32768447d6bc089296bfd0af7c94dbb76099830e` |
| `daemonsContext.gba` | CONTEXT | `3548caebd0e00bbbb11cd06966862f9aaf3daf2c` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `b1f6c4d3ae730cc459b9c04dcd4f84b035a2a1e0` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `78649347570ab03b00ee715633f7f609eefc3ac2` |

## The engine since v11.304.6

- `08acb5f6a` T-417 PLAY leftovers: the last key, SELECT for the BAND'S SHEET's key, real icons, notes under the staff (DRAFT)
- `4d474283f` T-425 (the user, 2026-10-18, by ear): PLAY's voices move onto OUR OWN harp and flute
- `5b2eaaa4e` README: the game at v11.304.6 -- weather's second phase, the holidays, PLAY's seven songs, each grove its own music, colour is friendship, the GAME CORNER as the companion's CASINO, the DREAM LOG and the pairs; the debug DATE row; music re-counted

## The design and tools since v11.304.6

- `9ffa1817` qa: T-426 PLAY on the site
- `9f9e2587` TODO: T-392 planned and its five questions answered (the user)
- `d4df9e2f` T-417 leftovers: genplayicons.py draws the HARP's and FLUTE's bag icons (engine 08acb5f6a); budgets
- `e783b3d6` T-425: geninstruments.py writes the game's HARP and FLUTE too; genplaysounds.py plays them (engine 4d474283f)
- `a52def61` README and wiki: the game at v11.304.6 -- the holidays and the months' colours, weather lifting its routines, PLAY's seven songs, colour is friendship, the GAME CORNER, the DREAM LOG; the companion's CASINO in context and its six tabs (engine README 5b2eaaa4e)
- `dd91f78e` TODO: T-424 released and settled by the user; T-421 gains two small finds
- `85a766d9` qa: T-424, T-422 fixes
- `881c4dc9` T-426: companion_export writes play.json and the game's note sprites -- PLAY for the devices and the phone (the user)
- `c6bd15fc` tools/geninstruments.py: our own HARP and FLUTE (T-425), writing audio/instruments byte for byte as committed
- `2945f462` ROM release v11.304.6: saturation is friendship (T-424); the CASINO's help card, its day's reason, the lead daemon dancing and one line (T-422)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
