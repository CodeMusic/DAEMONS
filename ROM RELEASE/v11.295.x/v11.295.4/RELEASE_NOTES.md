# DAEMONS v11.295.4 — release notes

*Released 2026-10-04 19:42 · built against the design bible v11.295*

- **Engine**: CodeMusic/pokefirered-daemons `4a5895b45` (context-content)
- **Design**: CodeMusic/DAEMONS `feb1e5eb`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `f1766d0f0f2b372eabc6a19a32bb1d334e0bf305` |
| `daemonsContext.gba` | CONTEXT | `faf4f9d82cb3864928195647f4b766dfeb4d1ba8` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `26c120b42f6bc25829dce7c14f4b27a02a046182` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `47be5b3043fad594377ebd7d45324595a5c31c02` |

## The engine since v11.295.3

- *nothing: the same engine commit as the release before*

## The design and tools since v11.295.3

- `feb1e5eb` qa: a step done and undone on the board, and FLARE's remotes (companion C-49, C-51)
- `f9ddfcc1` ROM release v11.295.3: the game unchanged since v11.295.2; the companion's exports grew (growth, base stats, natures, seen copies) for its INDEX, OPUS's margins, meetings and coming home grown

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
