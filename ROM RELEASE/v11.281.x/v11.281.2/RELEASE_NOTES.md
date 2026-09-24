# DAEMONS v11.281.2 — release notes

*Released 2026-09-24 08:07 · built against the design bible v11.281*

- **Engine**: CodeMusic/pokefirered-daemons `3ec7170e6` (context-content)
- **Design**: CodeMusic/DAEMONS `3ed23bcb`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `fb05fae091080bd464f72b829322fd8008d5a2d2` |
| `daemonsContext.gba` | CONTEXT | `b64d9f04ffce71e164151b7ff159b0756ebbaf71` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `fedc1c13aee5c29e0ba84090baac971a4d194e26` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `21f80acb32341cf4cae956b5ef830c6fea39592a` |

## The engine since v11.281.1

- `3ec7170e6` T-258: the CHECKPOINT explains a MEME, once

## The design and tools since v11.281.1

- `3ed23bcb` T-258: the CHECKPOINT's MEME line built; the memetics drafts on the private page
- `bc625320` ROM RELEASE: the notes go in git, the ROMs never do; WHERES_THE_ROMS.md says why
- `7a92fbf5` T-259: ROM releases documented in CLAUDE.md, the ticket logged and closed
- `8e85bef5` romrelease.py: find the previous release before filing the new one

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
