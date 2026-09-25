# DAEMONS v11.287.4 — release notes

*Released 2026-09-25 13:48 · built against the design bible v11.287*

- **Engine**: CodeMusic/pokefirered-daemons `8910aa3a4` (context-content)
- **Design**: CodeMusic/DAEMONS `c5a67c0f`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `40f04b7b1287f4b1f4e1d1e887ab76aa95896dbc` |
| `daemonsContext.gba` | CONTEXT | `734369c857c966d4e524bcca4cd5c9ff843ba173` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `7aad6117e5887470a7cb8150b560feb589607a43` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `260076671c268b4f6eb4be0fbd332173e9d5fb10` |

## The engine since v11.287.3

- `8910aa3a4` T-280: L refuses an entry the INDEX cannot open yet, instead of a black blink

## The design and tools since v11.287.3

- `c5a67c0f` T-280 closed: L refuses an entry the INDEX cannot open yet
- `382e588e` engine.md trap 31: mGBA gives CONTENT a clock and CONTEXT none; T-265 notes it
- `eec5fa8e` ROM release: the field effects take the light; a banner never outlives its popup

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
