# DAEMONS v11.338.3 — release notes

*Released 2026-11-04 23:23 · built against the design bible v11.338*

- **Engine**: CodeMusic/pokefirered-daemons `9b2ed6b10` (context-content)
- **Design**: CodeMusic/DAEMONS `db7e3681`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `2d4d2f45f79fdb7591a813b8b9a66ffa1ce0daa8` |
| `daemonsContext.gba` | CONTEXT | `725959a15a966c50d83c73058a47fb11b1590900` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `b234682d2e97fcef403f3da0024127ddc8debb60` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `cb5ba0c71004efd470f83aa594d50c21fca284a2` |

## The engine since v11.338.2

- `9b2ed6b10` T-521: PLAY made playable -- the BUTTON STRIP, and the seven songs re-taken from the user's recordings with their rhythm

## The design and tools since v11.338.2

- `db7e3681` TODO: T-521's engine commit (9b2ed6b10)
- `029d2111` qa: T-521 PLAY's button strip, a re-taken song matched, the strip back after the echo
- `50c034a0` T-521: PLAY's seven songs re-taken from the user's recordings by ear, with their rhythm (docs/play_songs.json); the ticket, built
- `f7f58290` ROM release v11.338.2: SPIRITS' tone plainer (10/32, the user) and THE HERMETIC LAYER's revised warning

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
