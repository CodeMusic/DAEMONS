# DAEMONS v11.288.10 — release notes

*Released 2026-09-26 13:03 · built against the design bible v11.288*

- **Engine**: CodeMusic/pokefirered-daemons `8215c1802` (context-content)
- **Design**: CodeMusic/DAEMONS `8e1f8c80`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `fcb286206c556a7c1577148227d398a0061786f5` |
| `daemonsContext.gba` | CONTEXT | `8b4c77745e556d203f99faa69dca1ec76683d161` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `86a8b1b27269cf23e3ad3cffc30b65edb70bbf6c` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `70e69a82522b2d165b7c8c080f49086ed48ae4c5` |

## The engine since v11.288.9

- `8215c1802` Ty a red fox (T-298, DRAFT art: portrait, walking sheet with a raised-paw frame, its spritesheet rule); CALLOW's own theme, MUS_CALLOW (T-05, transcribed); the START menu opens on the day's note (T-318)

## The design and tools since v11.288.9

- `8e1f8c80` genty.py writes its palette CRLF, as git checks it out
- `95db7acd` T-298 closed, T-05 built, T-313 and T-318 answered; engine.md trap 35; HOW_TO_PATCH.md, tools/ghrelease.py, tools/genty.py; README's Play it
- `0cd1d15b` ROM release v11.288.9: the family, the DAEMON Designers, the dream sign, the case studies, the Board's copy, Ty's Act 2 voice

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
