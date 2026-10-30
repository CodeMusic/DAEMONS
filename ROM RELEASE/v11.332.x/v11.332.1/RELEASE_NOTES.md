# DAEMONS v11.332.1 — release notes

*Released 2026-10-29 22:15 · built against the design bible v11.332*

- **Engine**: CodeMusic/pokefirered-daemons `c1315ba44` (context-content)
- **Design**: CodeMusic/DAEMONS `57c75e5a`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `e528948f10680982008cbde1f26545baf0f26c9a` |
| `daemonsContext.gba` | CONTEXT | `708963ecf2c6e6caf91cae088745df79c585aef5` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `4403267a0c6350fe31279ef01aa4930b8e77b267` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `f7a02d9f284cabebaaae7a1ca26787f3f276e6bd` |

## The engine since v11.331.1

- `c1315ba44` T-490 step 1: a routine's own category -- PHYSICAL / SPECIAL / STATUS per move, defaulted so nothing moves
- `1e08e7bde` README: latest release v11.331.1

## The design and tools since v11.331.1

- `57c75e5a` engine.md: the numbers after T-490 step 1
- `4732a809` T-490 step 1: the category marks in gbamovemenu, and the theatre route
- `bd08a07b` gbatitleview: run main() only as a script
- `213ab166` companion_export: every item slot and each item's pocket, for a gift with nothing back (C-223)
- `0114661f` README and wiki: v11.331.1; a daemon given (T-492) and the SINK items (T-488)
- `db197abf` Bible v11.332: the * SINK items and the GIFT released (T-488, T-492, v11.331.1)
- `6f4112c7` TODO: T-492, T-488 struck -- released v11.331.1
- `ab76d5f1` manual: rebuilt for v11.331.1
- `4ef8b401` ROM release v11.331.1: T-492 a daemon given (the GIFT mark); T-488 the sixteen * SINKs; v11.330.x sealed

## The design bible's own entry for v11.332

### v11.332 — 2026-10-29

- **2.12 §2, the `* SINK` items, released in v11.331.1 (T-488).** There are sixteen. Neither ORACLE nor CONTENT has one, because CONTENT is super-effective against nothing. Two of the names overlap ability names: SINK is MINUS's ability and SIGNAL SINK is LIGHTNING ROD's. The user chose to keep both. The bible also lists where each is sold and the four hidden on routes.
- **9.32, the GIFT, released in v11.331.1 (T-492).**
- A Settled entry in section 10. Every word is DRAFT.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
