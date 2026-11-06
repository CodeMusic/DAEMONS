# DAEMONS v11.342.1 — release notes

*Released 2026-11-06 12:43 · built against the design bible v11.342*

- **Engine**: CodeMusic/pokefirered-daemons `13b34a62f` (context-content)
- **Design**: CodeMusic/DAEMONS `67b10236`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `ca55b1de032bd6378dee7c6da794907f4ece84c3` |
| `daemonsContext.gba` | CONTEXT | `3a7b1f2f60210df6f8864cfee8f2024b6ab4a769` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `a93b8ae66b0ba1fc0a737b17df0486bd395c1f28` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `8111b9bea77eb557795890f123713fd72cac01e0` |

## The engine since v11.341.3

- `13b34a62f` T-452 follow-up: only daemons drawn off the ground float in battle

## The design and tools since v11.341.3

- `67b10236` T-522: the second pass's found mouths filed, and the ticket's row (companion 52e36dc, C-303)
- `0a7be50a` T-452 follow-up: who floats in battle is decided from each drawing (engine 13b34a62f)
- `6b065d0e` TODO: T-452 the pixel-model research and the user's yes to the trial
- `e7d8039f` T-522: the found mouths' sheets filed, and the ticket's row (companion 4b6143b, C-303)
- `5744de03` TODO: T-452's notes moved into its description; the roster walk's findings and the user's choices
- `c98a1939` T-452: the redrawn roster walked -- static audit of all 392 and 22 daemons filmed in battle and following (route t452_roster_walk.json, qa sheets 16-38)
- `bb77b5cb` T-522: the record is read and the telling is only heard -- bible v11.342, the tellings approved, the companion's card as the user described it
- `abe1ff64` TODO: T-452 the roster as built is approved; the open batch questions take their recommended answers (the user)
- `d8f1cfaa` ROM release v11.341.3: every page of the third book's three forms has its own picture (T-519, DRAFT)

## The design bible's own entry for v11.342

### v11.342 — 2026-11-06

- **4.2, the record is read and the telling is only heard (T-522, the user's design).** The tellings are approved as drafted. In the companion a card shows the INDEX entry, and LISTEN (a play mark in a cog) reads it in the device's voice: flat, robotic, a little glitchy. The daemon's own words are never printed: its sprite shimmers, and a tap brings the daemon forward over its card, in its type's den, to say it is thinking and then tell of itself in its own voice, its mouth moving, before it shrinks back (C-303).

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
