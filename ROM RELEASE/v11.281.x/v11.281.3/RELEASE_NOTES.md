# DAEMONS v11.281.3 — release notes

*Released 2026-09-24 09:11 · built against the design bible v11.281*

- **Engine**: CodeMusic/pokefirered-daemons `1716ca57b` (context-content)
- **Design**: CodeMusic/DAEMONS `2500cec2`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `6cc50fb754d064c5155e538df6d1d627e43e7edd` |
| `daemonsContext.gba` | CONTEXT | `300defc7c1f407d95992000fba4f0cacf0444c72` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `0a7d34f8c8390849b80bf8be55fff7943b096e7f` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `52c6ef532ae77d7df38ce57aa946c3881ead04cd` |

## The engine since v11.281.2

- `1716ca57b` T-249: HALFTONE Tower's stones can be read
- `7abb36ffb` T-257: the INDEX writes a page about what you chose

## The design and tools since v11.281.2

- `2500cec2` T-249: the stones read, DRAFT; approval is what is left
- `ec1accd5` T-257: the mechanism built, the words still private
- `a2674b01` ROM releases: BPS patches for every retail revision
- `f31cb043` ROM release v11.281.2: the Index's workings, the tower's stones, the unresolved display, MEME explained

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
