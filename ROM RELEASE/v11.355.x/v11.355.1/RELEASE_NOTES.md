# DAEMONS v11.355.1 — release notes

*Released 2026-11-12 00:27 · built against the design bible v11.355*

- **Engine**: CodeMusic/pokefirered-daemons `da455aa56` (context-content)
- **Design**: CodeMusic/DAEMONS `fd7e8929`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `cc49a5120750b0a44ac8907fcc6970b95743084a` |
| `daemonsContext.gba` | CONTEXT | `a6da086c7c1e17c0db81fd3ff5680e6c10c9be09` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `d3c2ff9f8d313a478fbc7693ae8015c6ece1cf02` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `c9ab1d3dc17a0b246a6d299e5ba365a2d1b4992f` |

## The engine since v11.354.1

- `da455aa56` T-546: THE BLACKOUT in purple with threads of green -- B LIGHT IN THE SEAMS, the card B only the threads, and the dark
- `eb4cf2e32` README: the release line names v11.354.1

## The design and tools since v11.354.1

- `fd7e8929` qa: T-546 THE BLACKOUT built (12Nov 1)
- `37bb584e` T-546: THE BLACKOUT BUILT (engine da455aa56) -- tiles B LIGHT IN THE SEAMS, card B only the threads, the dark
- `b97f2c38` Bible v11.355: DOLDRUM CAVE's card BECALMED, released (T-445, v11.354.1); every place card ours
- `52d6557d` qa: C-191, C-273, C-296 seen in the iOS app on the Simulator (companion 6851fc0)
- `2d3f6396` README and wiki Home name v11.354.1
- `6dfd5a23` ROM release v11.354.1: DOLDRUM CAVE's name card, A BECALMED (T-445) -- every landmark card ours but USER TOWER; seals v11.353.x

## The design bible's own entry for v11.355

### v11.355 — 2026-11-11

- **9.29:** DOLDRUM CAVE's name card, BECALMED, the user's pick, released in v11.354.1 (T-445). It shows still air, a still black pool and one point of light, in the cave's grey until the cave is understood and in colour after. Every place card is now ours.
- A Settled entry in section 10. DRAFT.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
