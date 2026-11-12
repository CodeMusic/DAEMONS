# DAEMONS v11.354.1 — release notes

*Released 2026-11-11 22:49 · built against the design bible v11.354*

- **Engine**: CodeMusic/pokefirered-daemons `d4277a127` (context-content)
- **Design**: CodeMusic/DAEMONS `e18fd7ea`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `1d85bf65c8332620b66ccaa8843c014416cc3d8d` |
| `daemonsContext.gba` | CONTEXT | `8fb9fb68ccc9ae84fa448329b578ddedab959a85` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `75bddea5161aea6ddec6e4f8351c3bb887e96ef7` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `59ba747f64deb82b0d3558a9c4ef32fc4a7fad46` |

## The engine since v11.353.1

- `d4277a127` T-445: DOLDRUM CAVE's name card BUILT -- A BECALMED, the user's pick 2026-11-11 (still air, a still black pool, one point of light; in colour once understood, inked by the cave's grey filter before; gbapreviews --cards --write --approved; 407 tiles; DRAFT)
- `20c5c6317` README: the release line names v11.353.1

## The design and tools since v11.353.1

- `e18fd7ea` qa: DOLDRUM CAVE's card, built and its directions (108, 109)
- `f5c2be73` T-445: DOLDRUM CAVE's card BUILT, A BECALMED (engine d4277a127) -- the last landmark card but USER TOWER; gbapreviews drafts four directions (BECALMED A/A2, A SIMPLE DRAWING, WRONGLY ARRANGED, THE PAINTED MIRROR) with the unread view through fieldmap.c's drawing tones; T-546 filed: THE BLACKOUT in purple and green threads, card and cave (the user)
- `86f13d19` THE COMPANION re-recorded (friend, 64.0 min) with its GUARDIAN section -- the recording v11.353.1 deferred (bb1e2814)
- `2a84601e` Bible v11.354: every General tile ours, released (T-542 batch 4, v11.353.1)
- `29446d7b` README and wiki Home name v11.353.1
- `9ca40188` ROM release v11.353.1: T-542 batch 4, the last three General edges in B THE TRACE -- every General tile is ours; seals v11.352.x; THE COMPANION's recording deferred (the user: release now, record after)

## The design bible's own entry for v11.354

### v11.354 — 2026-11-11

- **9.29:** every General tile is now ours, released in v11.353.1 (T-542 batch 4). General is the tileset every outdoor map shares. The last three edges are the sand's corner, the forest path's edge and the cliff's foot, drawn in THE TRACE, the user's pick.
- A Settled entry in section 10. DRAFT.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
