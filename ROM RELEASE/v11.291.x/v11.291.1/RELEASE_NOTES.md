# DAEMONS v11.291.1 — release notes

*Released 2026-10-02 10:50 · built against the design bible v11.291*

- **Engine**: CodeMusic/pokefirered-daemons `afab773dd` (context-content)
- **Design**: CodeMusic/DAEMONS `4586e127`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `5b49cf07cdc32f00d4cc797deb25c8006a0a3ba8` |
| `daemonsContext.gba` | CONTEXT | `a1a91bfa35f123bf1e31c19847cf3fbdc94f8f70` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `e048dd6724be76a067b8ae781ca09f558ead8127` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `6b5b206aeabd5d1a6199b81fa0b0298a3130cb93` |

## The engine since v11.290.8

- `afab773dd` T-317: understanding shown in the world, as a faded print (the user's choice, 2026-10-02)

## The design and tools since v11.290.8

- `4586e127` Bible v11.291: the world shows understanding as a faded print (T-317, the user's choice), and seven UNDERSTANDINGS with no eighth (T-252) -- both closed
- `224a9452` qa: the 2026-10-02 pictures -- T-346, T-347 played, T-337's fix, T-340/T-341 played, the hints seen in play, T-317's designs
- `306d1201` ROM release v11.290.8: the leaders say the virtues aloud and CALLOW hears its door (T-346), the CHECKPOINT attendant's dreams (T-347), the grove tell out of the water animation (T-337) -- and the Rev 1 patches proved on the user's own carts (T-344)

## The design bible's own entry for v11.291

### v11.291 — 2026-10-02

### The world catches up as you understand it, and seven is the number (2026-10-02)

- ***The world shows understanding as a faded print*** (T-317, the user's choice of three mock-ups): *every tileset colour drawn 40% of the way to its own grey while four or more understandings are still to come, 18% while one to three are, as painted with all seven. People and daemons keep their colour. Built and played the same day.*
- ***Seven UNDERSTANDINGS, and no eighth*** (T-252, the user).
- *Built the same day, released in v11.290.8: the leaders say each MARK's virtue aloud and CALLOW hears its door (T-346); the CHECKPOINT attendant's dreams for a player who is stuck (T-347); the patches proved on the user's own carts (T-344).*

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
