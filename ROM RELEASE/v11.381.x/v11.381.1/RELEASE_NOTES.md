# DAEMONS v11.381.1 — release notes

*Released 2026-11-16 20:20 · built against the design bible v11.381*

- **Engine**: CodeMusic/pokefirered-daemons `90d4d474e` (context-content)
- **Design**: CodeMusic/DAEMONS `19363625`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `63f085a5d23fe3fe5e1b89b731383000c654d36e` |
| `daemonsContext.gba` | CONTEXT | `38a278df8ff6dd500f47bdddbcaad85e13295a9e` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `be083f78a39a40479add24733980d18d28435459` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `0a3a3ca8fa2fdddabdb4a50cbda9fdbb972c1218` |

## The engine since v11.380.1

- `90d4d474e` T-574: the ladders down a hole in DEADSTACK, MT. SMOULDER, NAVEL ROCK and TAPPOINT'S as T-570's rungs and rails, and NAVEL ROCK's fall hole as its broken lip (the user's pick; tools/gbacaves.py)
- `637f5751f` README: the release line names v11.380.1

## The design and tools since v11.380.1

- `19363625` TODO: T-565 the split agreed with the Musical Instruments lane; T-574 BUILT
- `80432a31` T-574: gbacaves draws the ladders down a hole as T-570's ladder A (gbaislands' drawing, imported)
- `d1f076bb` TODO: T-565's census done (docs/sound-census-2026-11-16.md); next, the split with the Musical Instruments lane
- `dde09a36` T-565: the sound census -- which MUS_ and SE_ the GBA build still plays as pret made them
- `838d6b23` TODO: T-572 the map ring under the head, T-573 the dept. store a landmark, T-574 gbacaves' ladders; T-565 next (the user's picks)
- `4d6338b7` Bible v11.381: the relearner's carets seen, two drifts put right (v11.380.1)
- `a30d965e` README and wiki Home name v11.380.1
- `dede92d7` ROM release v11.380.1: the relearner's caret arrows seen (three vanilla bugs), ROVERBYTE and MUSAI credit cards rebuilt, DENSE WOOD's grove tell; seals v11.379.x

## The design bible's own entry for v11.381

### v11.381 — 2026-11-16

- Recorded from release v11.380.1 (dede92d7, engine 528a27359), which sealed v11.379.x:
  - **The relearner's CARET arrows seen** (T-566 follow-up): three vanilla bugs had hidden them; fixed on the user's yes.
  - **Two drifts put right**: the ROVERBYTE and MUSAI credit cards rebuilt from their redrawn fronts, and DENSE WOOD's grove tell one pixel back on its trunk.
  - Also in the release, outside the bible: generator guards for T-569, T-570 and the landmarks, the books reprinted after T-571, and the unseen pieces filmed.
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
