# DAEMONS v11.294.9 — release notes

*Released 2026-10-03 22:37 · built against the design bible v11.294*

- **Engine**: CodeMusic/pokefirered-daemons `93ea779b6` (context-content)
- **Design**: CodeMusic/DAEMONS `dc17e0b3`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `2d118101ec66c8b1fe7257b04b417e0c53b72cf2` |
| `daemonsContext.gba` | CONTEXT | `0948ddbc6bc4a255f0c51eb2ab4fcecfae771c50` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `93332d4adc0d6617a4138e20e85e9ef1f1be47d8` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `37338ac2eed9f49a7be7a7ec3644b8bbd2bf11bf` |

## The engine since v11.294.8

- `93ea779b6` T-364: the OWL stays at the front after the DIPLOMA until BRAZEN, then is home

## The design and tools since v11.294.8

- `dc17e0b3` T-364 closed (engine 93ea779b6): the OWL stays until BRAZEN, the same OWL at home; qa T-364, C-10
- `832d3f03` companion_export: the game's art, streak table and routine types for the companion (C-18); qa C-10, C-18
- `9ef910a9` T-319 kept current (engineAi 05d7d19)
- `c264ee70` ROM release v11.294.8: the seasons (T-359)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
