# DAEMONS v11.288.14 — release notes

*Released 2026-09-27 04:28 · built against the design bible v11.288*

- **Engine**: CodeMusic/pokefirered-daemons `73dc5af86` (context-content)
- **Design**: CodeMusic/DAEMONS `e4097271`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `785107c9deea1ab610bf46eb2d3170fab11aca4b` |
| `daemonsContext.gba` | CONTEXT | `15474bc8fb846a713807d1e11893b08a78f8bcbb` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `891422e1c49a7b38a1e11258931e061fcc0a130e` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `60985babf4007dc011d025274563106859e166b0` |

## The engine since v11.288.13

- `73dc5af86` The singing fir on the S.S. ANNE's pier (T-10, DRAFT): O CHRISTMAS TREE without its key and with it, the band's sheet from DAVID, the pier open after the ship sails; the Five Witnesses answer only to every understanding (T-235)

## The design and tools since v11.288.13

- `e4097271` T-10 and T-235 built, T-318 proposed; the redacted bible PDF rebuilt
- `0c47d59b` Redaction, second sweep: the parentage and engraving lines left in vision.md, TODO, lineage, CHANGELOG and two reviews
- `6cab35b9` The four secrets leave the public bible (option (a)): docs/private/ holds them, gitignored; vision.md points there; the v11.288 PDF rebuilt redacted, the older PDFs kept privately
- `94e10fc6` The user's answers (2026-09-27): virtues with the MARKS (T-318), all understandings unlock the Five Witnesses (T-235), the singing tree by the S.S. ANNE (T-10)
- `6ea167ef` ROM release v11.288.13: seven understandings; the week's colour on the menu

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
