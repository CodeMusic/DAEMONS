# DAEMONS v11.291.5 — release notes

*Released 2026-10-02 17:42 · built against the design bible v11.291*

- **Engine**: CodeMusic/pokefirered-daemons `b2124fa91` (context-content)
- **Design**: CodeMusic/DAEMONS `ea13568e`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `ba6139ca02cec4def24062a34ef1dbcdb2b07dcd` |
| `daemonsContext.gba` | CONTEXT | `f0977f84ee95d684e81bb826e01f18938cf31dc3` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `ef3890a8622186f0615e874e1e14bef16c4ad5d8` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `8904dd38947a218e7f2a194f1fc3699655d46d8a` |

## The engine since v11.291.4

- `b2124fa91` T-210 batch 4: the dragons and fossils named, written and drawn (DRAFT)
- `038ef1b44` T-210: ICICLE SPEAR -> UNROLL, approved by the user (DRAFT)

## The design and tools since v11.291.4

- `ea13568e` T-210 batch 4 and UNROLL: drafts, art and picks (engine b2124fa91)
- `3801b835` T-210: UNROLL approved, and batch 4 is the dragons and fossils, as a goal loop (the user)
- `068c4881` qa: T-210 batch 3 as built
- `25fcf87d` ROM release v11.291.4: the rest of the water-typed families named, written and drawn (T-210 batch 3)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
