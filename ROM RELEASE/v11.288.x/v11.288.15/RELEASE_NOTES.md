# DAEMONS v11.288.15 — release notes

*Released 2026-09-27 04:59 · built against the design bible v11.288*

- **Engine**: CodeMusic/pokefirered-daemons `309179562` (context-content)
- **Design**: CodeMusic/DAEMONS `205cf329`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `1290bc631d786fd636ebfd5346e0b53b4dee643c` |
| `daemonsContext.gba` | CONTEXT | `1b6e53a6ba17cd982445e7267f6f9db7707f55fc` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `e14ea7797b626dfbba7ddc2d35c858896363e5c3` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `8f8f51c38f804629c29010705fb8057599a0217f` |

## The engine since v11.288.14

- `309179562` Virtues come with the MARKS (T-318, DRAFT): each held MARK's page says its virtue, and the USER card's portrait comes out of shadow band by band, feet to crown; the witnesses' room confirms the accounts (T-235)

## The design and tools since v11.288.14

- `205cf329` T-318 built, T-235 and T-10 confirmed; story.md and story-readthrough.md made private
- `cf182d98` ROM release v11.288.14: the singing fir; the witnesses answer to every understanding

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
