# DAEMONS v11.288.22 — release notes

*Released 2026-10-01 10:59 · built against the design bible v11.288*

- **Engine**: CodeMusic/pokefirered-daemons `bc7cba35f` (context-content)
- **Design**: CodeMusic/DAEMONS `53e0a3cc`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `8d7a9deb7ad6229e8f86044191b12f51079969d1` |
| `daemonsContext.gba` | CONTEXT | `41dd8cf379a87f008663679b283084d9801510a8` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `fed680d652fd63edc848de0c7f86c918022f30bd` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `c757e13c5bb65cdc43be77a8c63fbabd6725240e` |

## The engine since v11.288.21

- `bc7cba35f` T-221: all fourteen groves -- thirteen more clearings, their doors, and thirty-two daemons
- `a5f9926e0` T-327: LENSMUSAI, MASKMUSAI, SEMAPHORE and KERNEL drawn -- reached by evolving, they still wore vanilla's picture (DRAFT)
- `5a211281f` T-324: VERDIGRIS DEPT. STORE's SERVICE COUNTER again -- the move COUNTER's rename had caught it
- `c643263e1` T-328: the thank-you card holds 11% longer (210 -> 233 frames)
- `9a61e7ba2` T-325: a gangway from the pier to the far quay once the ship has sailed, so the singing fir can be walked to

## The design and tools since v11.288.21

- `53e0a3cc` Goal run, batch 2: T-221 groves, T-325 gangway, T-327 reach fix and four sprites, T-328, reviews T-321/T-322/T-324 recorded (engine 9a61e7ba2..bc7cba35f)
- `debfb191` ROM release v11.288.21: the first batch of yes-to-all -- WHAT YOU CHOSE, twenty documents, CONTEXT's entries, TANOBY, the runners

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
