# DAEMONS v11.361.1 — release notes

*Released 2026-11-14 11:07 · built against the design bible v11.361*

- **Engine**: CodeMusic/pokefirered-daemons `dc780f8c5` (context-content)
- **Design**: CodeMusic/DAEMONS `5e46a11a`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `5db9df843aa97200764cbde3ecbdf7a97e676b8d` |
| `daemonsContext.gba` | CONTEXT | `1e2358888cc952f2a81fd7c782263f2477356e9a` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `0ec3bc67e1d4e4bcb91c33eac085d7809eb393b6` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `f92f1625c34f915ee20c32ae7e63e03c28a8b4ef` |

## A note on the book audio

A minor release, released with one recording deferred (the user, 2026-11-12: "Release now, record after"): the new T-GLASSES book has not been recorded yet.

## The engine since v11.360.1

- `dc780f8c5` T-551: THE WALLED GARDEN's WARDEN becomes the GATEKEEPER (the user, 2026-11-14), DRAFT
- `9c0714cd2` README: the release line names v11.360.1

## The design and tools since v11.360.1

- `5e46a11a` T-551 built (engine dc780f8c5): THE WALLED GARDEN's WARDEN is the GATEKEEPER, DRAFT
- `65de3487` Bible v11.361: THE WALLED GARDEN released (T-540, v11.360.1); its WARDEN to be the GATEKEEPER, decided (T-551)
- `ff06dee4` qa: companion C-221 -- the link cable through the hub (14Nov 2)
- `48476e42` qa: C-356 THE SIGNS THAT RETURN on a scratch site (14Nov 1; companion 95c1f2a)
- `df63de63` TODO: T-551 filed -- the WARDEN becomes the GATEKEEPER (the user, 2026-11-14), with the attendant's dream BEHIND THE WALL (the user, 2026-11-12)
- `12fc1ee0` README and wiki Home name v11.360.1
- `2dd62609` ROM release v11.360.1: T-540 THE WALLED GARDEN -- the SAFARI ZONE's 85 lines as the user picked them, the place renamed, the RINGS, SIGN OUT (DRAFT); seals v11.358.x; T-GLASSES' recording deferred

## The design bible's own entry for v11.361

### v11.361 — 2026-11-14

- **3.11:** THE WALLED GARDEN, released in v11.360.1 (T-540). Of the 85 lines, 76 were changed and 9 kept, as the user picked.
- **3.11, decided:** the WARDEN becomes the GATEKEEPER (T-551, the user, 2026-11-14). A walled garden is kept at a gate. His staff still call him LATENCY. The attendant's dream BEHIND THE WALL comes with it. Not yet built.
- A Settled entry in section 10. DRAFT.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
