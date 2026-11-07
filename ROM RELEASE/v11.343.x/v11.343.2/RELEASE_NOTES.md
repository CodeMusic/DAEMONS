# DAEMONS v11.343.2 — release notes

*Released 2026-11-07 17:07 · built against the design bible v11.343*

- **Engine**: CodeMusic/pokefirered-daemons `8eea1ac1b` (context-content)
- **Design**: CodeMusic/DAEMONS `427b353e`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `b4d90a2064d37bf9ed3ec5fb6428db7833fdac2e` |
| `daemonsContext.gba` | CONTEXT | `49a4ce19a24378ab8ae1d950df72b883a0fa778e` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `844d3cdc75dce24cf3c51a6bb7a254d6152c04d3` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `215ebdb14a14ff1a792c3aebc4a8568623373eda` |

## The engine since v11.343.1

- `8eea1ac1b` healthbox_elements.png: re-encoded as genthrashicon writes it (pixel-identical; T-524's spliced sheet, so check_generators --writes sees no drift)
- `c99d084c2` T-528 part 1: the aurora -- over DAEMON TOWER every night once the book is mended, in a lit grove's battle sky on the light's nights, and outdoors on those nights once every grove found is lit (vision 4.40; the user, 2026-11-07, by multiple choice)
- `b551cbe20` T-527: SLATE's room in real slate greys -- benchmark_slate.pal was 197-255 in every colour, so the wall and the platforms barely showed in the new room (the user, 2026-11-07: darken it)

## The design and tools since v11.343.1

- `427b353e` companion_export: T-528's two DEBUG rows -- EVERY GROVE LIT reads the 14 FLAG_*_GROVE_LIT (FOUND + 0x10); NIGHTS OF LIGHT left out (an EWRAM override, not save state)
- `152def01` engine.md and items.html regenerated (gbabudget, gbaitems): T-528's memory figures and T-526's item text
- `4944572e` T-528 part 1 built (engine c99d084c2): the aurora over DAEMON TOWER, in a lit grove's battle sky on the light's nights, and outdoors once every grove found is lit -- filmed (tools/routes/t528_aurora_a.json), qa 35-38
- `36b0480c` check_generators --writes really runs gbabattleui, gbaframes and gbapreviews now: each accepts --over-later-work (argparse refused it, exit 2 with no traceback, so their sandboxed writes never ran); gbacalendar_ui, port_item_text and gbaitemicons already took it
- `a8060570` T-527: SLATE's room darkened (engine b551cbe20) -- genbackdrops.py ramps SLATE by Lorelei's lightness over real slate greys in its roof's hue, since a tint that keeps HSV value left it 197-255 in every colour (the user, 2026-11-07: darken it)
- `26c5f1b2` T-528 part 1's rules in its row: the light's nights as arithmetic (a 16-bit hash of the night's day number, one in three) and the seven grove pairs, mainland to island, with a reason each
- `770fda1b` ROM release v11.343.1: T-527 the battle backgrounds in our own hand (A outdoors, B indoors); seals v11.342.x

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
