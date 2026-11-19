# DAEMONS v11.403.1 — release notes

*Released 2026-11-18 19:44 · built against the design bible v11.403*

- **Engine**: CodeMusic/pokefirered-daemons `ee68884b5` (context-content)
- **Design**: CodeMusic/DAEMONS `3fa1d65f`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `bd0a717a4ca5a69a7530d04a1a93af6433128600` |
| `daemonsContext.gba` | CONTEXT | `a7a1dafa4cb267211ef547e9ff80193746f268e4` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `3edf05cf0574536c73edeaa9148cb6d0369cf24c` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `4d3e1b568e7e144279dc7870702a2969ee5f154f` |

## The engine since v11.402.1

- `ee68884b5` T-438 (last part): UMBRAL ASCENT's own tiles, A PENUMBRA (gTilesetTiles_CaveUmbral); THE DOTS' open door A SLAB SUNK; the islands' piling cap and harbour railing corner; 8 of the 15 slivers retinted (7 left: a retint would show) -- the user, 2026-11-18, DRAFT art
- `ef677123c` README: the release line names v11.402.1

## The design and tools since v11.402.1

- `3fa1d65f` gbageneral: a tile split's palettes come from its header (UMBRAL ASCENT's cave/umbral/ has tiles, no palettes folder) -- gbageneral and gbaprimary ran into it after T-438
- `ed788583` T-438 (last part): gbacaves UMBRAL_APPROVED A and the sliver retint, gbaislands APPROVED_438K (dotted, piling, rail, slivers), reviewsheet reads a tileset header's own tiles (engine pokefirered-daemons@ee68884b5)
- `adcce86f` T-438: UMBRAL ASCENT's own tiles drafted (gbacaves --umbral: A PENUMBRA, B TERRACES, C DUSK GLASS; DRAFT, nothing approved)
- `a5138b88` Bible v11.403: pret's last reachable music released (T-593, v11.402.1)
- `9694be82` README and wiki Home name v11.402.1: every song a player hears is ours
- `c76a67fa` ROM release v11.402.1: T-565 batch 13, pret's last music (DRAFT); seals v11.401.x

## The design bible's own entry for v11.403

### v11.403 — 2026-11-18

- Recorded from release v11.402.1 (c76a67fa, engine ce02dbf00), which sealed v11.401.x:
  - **Pret's last reachable music** (T-593, T-565 batch 13): fourteen songs in voice C over pret's slots (the user: "All fourteen"), so every song a player of this build hears is ours; nine slots stay pret's, none heard, and 43 sound effects. DRAFT. In 9.5.
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
