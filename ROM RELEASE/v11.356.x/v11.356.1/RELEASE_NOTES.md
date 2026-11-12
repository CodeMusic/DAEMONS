# DAEMONS v11.356.1 — release notes

*Released 2026-11-12 09:11 · built against the design bible v11.356*

- **Engine**: CodeMusic/pokefirered-daemons `9b620f0d7` (context-content)
- **Design**: CodeMusic/DAEMONS `7167c7c8`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `e690f9db05c78b9e0ac4f5af613c0dca56c62fcc` |
| `daemonsContext.gba` | CONTEXT | `e5f0c2a0edbd0620d95a1915cd28bac16cad075d` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `6102acedf3b66def9e17b2555fc27b8c2002acb3` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `4915676a6b7789ca5ce2d8b37ddaf6efd1a8eb9e` |

## The engine since v11.355.1

- `9b620f0d7` T-546: THE BLACKOUT's dark through THE FIELD STAGE -- no lit rows at the top of a dark frame
- `bac6435c7` README: the release line names v11.355.1

## The design and tools since v11.355.1

- `7167c7c8` T-546: THE BLACKOUT's dark through THE FIELD STAGE (engine 9b620f0d7) -- 0 lit rows; the route plays out a dream first
- `889d0c0b` qa: T-546 THE BLACKOUT filmed, VERBOSE rising (12Nov 2)
- `072885bd` Bible v11.356: THE BLACKOUT in purple with threads of green, released (T-546, v11.355.1)
- `8019f508` README and wiki Home name v11.355.1
- `b6a8f482` ROM release v11.355.1: T-546 THE BLACKOUT in purple with green threads -- the card, the tiles B LIGHT IN THE SEAMS and the dark (daemons_blackout.c); seals v11.354.x

## The design bible's own entry for v11.356

### v11.356 — 2026-11-12

- **9.29:** THE BLACKOUT in purple with threads of green, the user's picks, released in v11.355.1 (T-546).
  - **The rock, LIGHT IN THE SEAMS:** magenta-violet, a green vein down every face, and a green mesh in the seams.
  - **The card:** black but for the threads.
  - **The dark:** black but for the steady threads until VERBOSE, which raises the light with its circle. Once lit, the rock breathes with the pulse.
  - The dark outranks HALFTONE.
- A Settled entry in section 10. DRAFT.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
