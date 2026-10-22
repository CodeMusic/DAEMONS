# DAEMONS v11.309.4 — release notes

*Released 2026-10-22 12:19 · built against the design bible v11.309*

- **Engine**: CodeMusic/pokefirered-daemons `b3cc6cb50` (context-content)
- **Design**: CodeMusic/DAEMONS `519e875a`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `e738dcb1bc7b3a4a94ec34c9e479eea478d28e2d` |
| `daemonsContext.gba` | CONTEXT | `4c37bde24acf9fcf455d7fba1d12333e35a02f7d` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `1772f7056257778a2df5cf6ba66e9c760e32dc8f` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `dcb97dd8bf23fcf3bd9d7e5d389d8b3d62610266` |

## The engine since v11.309.3

- `b3cc6cb50` T-438 batch A: the doors open as the buildings are drawn (the user approved 2026-10-22)

## The design and tools since v11.309.3

- `519e875a` TODO: T-433 the user's four calls; T-438 batch B approved, batch C to a second pass
- `d08fc0b9` T-438 batch A built (engine b3cc6cb50): the doors, the arrow, the lab door's handles, the 376-383 overlap
- `5a753af1` TODO: T-438 batch C drafted, waiting on the user
- `40d8db7a` qa: T-438 batch C draft
- `d41f8dc2` T-438 batch C draft: the general ground (not in the engine)
- `a6f2db27` qa: T-438 batch B draft
- `5eba2928` TODO: T-438 batch B drafted (field effects and weather), waiting on the user
- `0d1dea2e` T-438 batch B draft: field effects and weather (not in the engine)
- `0de61951` qa: T-433 items move feelings; T-439 the cast; T-438 the doors draft
- `b60e4341` ROM release v11.309.3: items and moments move feelings and friendship -- potions and revives gladden, the RARE CANDY angers, bitter herbs rankle, the REMNANT unveiled frightens, LEADERS and evolving gladden (T-433, DRAFT values)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
