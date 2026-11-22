# DAEMONS v11.412.2 — release notes

*Released 2026-11-21 14:43 · built against the design bible v11.412*

- **Engine**: CodeMusic/pokefirered-daemons `36598161e` (context-content)
- **Design**: CodeMusic/DAEMONS `557450d2`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `ceb72f5177d39555aabfc00f2901cc7f862c5985` |
| `daemonsContext.gba` | CONTEXT | `857f0de008ae27bf1ed10ef288c02da8996123b6` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `f540bf898cb0801637b5282a7e1ec447a556fa1e` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `e833ae614324c91fbec15f8b1114bdb7c9c5b6fc` |

## The engine since v11.412.1

- `36598161e` T-605 (draft): MUSAI grows into seven forms -- SONGMUSAI (SIGNAL) and LANGMUSAI (EMERGENT), every word DRAFT
- `598cc100d` README: latest is v11.412.1

## The design and tools since v11.412.1

- `557450d2` qa: E-1 answering what waits on the user, on a throwaway copy
- `667d28ea` tickets.py ask: a lane puts a question to the user, with its choices (EUDAIMONIA E-1)
- `74c860ec` Tickets mirror: T-605 closed, T-607 opened
- `45795420` T-605 (draft): MUSAI grows into seven forms -- SONGMUSAI and LANGMUSAI, their inputs WAVEFORM and UTTERANCE (engine 36598161e)
- `3d62c074` qa: C-457's captions
- `1e723a4e` qa: C-457, the GamePi20 build seen on the Mac
- `ff5da770` qa: T-452 arm C's verdict, the six reverted (v11.412.1)
- `c35ca258` README and wiki: latest is v11.412.1
- `1502131b` ROM release v11.412.1: T-452 arm C's verdict (six back to their old art, 22 keep), C-442 THE KODE DOT; seals v11.411.x

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
