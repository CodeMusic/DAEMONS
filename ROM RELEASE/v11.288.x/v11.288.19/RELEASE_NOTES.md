# DAEMONS v11.288.19 — release notes

*Released 2026-09-29 05:46 · built against the design bible v11.288*

- **Engine**: CodeMusic/pokefirered-daemons `ca2c406ce` (context-content)
- **Design**: CodeMusic/DAEMONS `5bfed788`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `e1a7d45997ed7c2fda047ed7c273a52b180327cf` |
| `daemonsContext.gba` | CONTEXT | `a0c7b13fb6bda044b10d75eb2dd38810357c6e6e` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `94a6d67d4e6214d5f86764b900c95f639c0c0f70` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `bb24ca3a3a075bace75797061cdfac3fefdcbf7b` |

## The engine since v11.288.18

- `ca2c406ce` A thank-you to Satoshi Tajiri after the CodeMusic splash (T-320)

## The design and tools since v11.288.18

- `5bfed788` T-320 closed: the thank-you card is in (engine ca2c406ce)
- `bcc6e6ba` T-320: a thank-you to Satoshi Tajiri in the intro (the user, 2026-09-29), drafts awaiting the user
- `ed1f70bf` check_lexicon fails on specialvar reading a void special; engine.md traps 37-38; EWRAM measured against pristine pokefirered
- `583bf410` ROM release v11.288.18: the INDEX comes clear; the day on the card; virtue over shadow

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
