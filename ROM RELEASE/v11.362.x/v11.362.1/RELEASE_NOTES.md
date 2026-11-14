# DAEMONS v11.362.1 — release notes

*Released 2026-11-14 13:31 · built against the design bible v11.362*

- **Engine**: CodeMusic/pokefirered-daemons `be1d32e95` (context-content)
- **Design**: CodeMusic/DAEMONS `80295796`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `da9240cb15c7d34e36e1495d84e9ecad1fd1535f` |
| `daemonsContext.gba` | CONTEXT | `83f49f9ab3e042f082e989207045bfb0f39d466a` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `00088edad4c28b30044a7a8062eab5f6344f01d9` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `793a52c1cb05762f8da3a5aaaf056d81424548f1` |

## A note on the book audio

A minor release, released with one recording deferred (the user, 2026-11-12: "Release now, record after"): the new T-GLASSES book has not been recorded yet.

## The engine since v11.361.1

- `be1d32e95` T-540: THE WALLED GARDEN's art -- the interiors C THE GLASSHOUSE, the GATEKEEPER's shelf to match, the name card B over the wall (DRAFT)
- `8184c630e` README: the release line names v11.361.1

## The design and tools since v11.361.1

- `80295796` T-540 BUILT (engine be1d32e95): THE WALLED GARDEN's interiors C THE GLASSHOUSE, the GATEKEEPER's shelf to match (gbamuseum's LATER_T540), the name card B over the wall; gbagarden APPROVED {C} and --proof from the ROM; check_generators runs it; every part of T-540 built (DRAFT)
- `cd6878de` T-540: THE WALLED GARDEN's art DRAFTED -- the interiors (tools/gbagarden.py: A THE ARBOUR, B THE LOBBY, C THE GLASSHOUSE; the GATEKEEPER's shelf) and the name card (gbapreviews --cards: gate lit, over the wall, the RINGS from above); APPROVED and CARDS_APPROVED unchanged, nothing in the engine (DRAFT)
- `b924932d` Bible v11.362: the GATEKEEPER released (T-551, v11.361.1)
- `f93c77cb` README and wiki Home name v11.361.1
- `8f233e8d` ROM release v11.361.1: T-551 the GATEKEEPER (the WARDEN renamed, LATENCY kept) and the attendant's dream BEHIND THE WALL (DRAFT); seals v11.360.x; T-GLASSES' recording deferred

## The design bible's own entry for v11.362

### v11.362 — 2026-11-14

- **3.11:** the GATEKEEPER is released in v11.361.1 (T-551). The WARDEN is renamed everywhere a player reads it, and his staff still call him LATENCY. The attendant's dream BEHIND THE WALL comes with it. The build commit had already renamed him in this section.
- A Settled entry in section 10. DRAFT.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
