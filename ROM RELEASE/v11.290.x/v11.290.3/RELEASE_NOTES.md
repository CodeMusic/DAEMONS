# DAEMONS v11.290.3 — release notes

*Released 2026-10-01 18:00 · built against the design bible v11.290*

- **Engine**: CodeMusic/pokefirered-daemons `17a08e57e` (context-content)
- **Design**: CodeMusic/DAEMONS `d31e7377`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `98f1736d79bf21d68d2ec4f765bc34dd40a90086` |
| `daemonsContext.gba` | CONTEXT | `c8aa6a3eafa6e340a2b271775698745f183e3d19` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `fb0d1e8e53b3033f5eca16399a1f1ffe99f3919c` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `41415f28687ba77f41285336ad625faaa2cf0dc7` |

## The engine since v11.290.2

- `17a08e57e` T-337: the singing fir's star twinkles -- three frames on an irregular loop (DRAFT, tools/gensingingfir.py)
- `c92e257f9` T-337: a grove's tree has a little door in its trunk, a grove's bush a gap at its foot -- eleven doors and every clearing's way out (DRAFT, tools/gbagrove.py)

## The design and tools since v11.290.2

- `d31e7377` TODO: T-337's row names its engine commits
- `16816441` T-337 closed: gbagrove draws and places the grove's tell (TELL); gensingingfir draws the star's twinkle frames
- `c2442af3` TODO: T-337 -- a grove's tree subtly unlike the others, and the fir's star twinkles (the user)
- `9006c095` ROM release v11.290.2: nine named babies drawn (T-210), CRYSTAL on Teachy TV (T-120)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
