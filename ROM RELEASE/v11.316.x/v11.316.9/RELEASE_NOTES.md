# DAEMONS v11.316.9 — release notes

*Released 2026-10-28 18:34 · built against the design bible v11.316*

- **Engine**: CodeMusic/pokefirered-daemons `b133f6492` (context-content)
- **Design**: CodeMusic/DAEMONS `3b385a81`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `85d5c1c6e641d08c8e06cb99547748076e335ed5` |
| `daemonsContext.gba` | CONTEXT | `b463db62a0cd444470d0f566df95e2437a3e3d2d` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `06aff4acf41f9bdf36c9d270643fe997521f65af` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `e7f0b2ee6381e22c0848ae54e50a2535c1ad8539` |

## The engine since v11.316.8

- `b133f6492` OVERLOADED's streaks in battle: the castform palette reload stopped wiping them
- `87557e860` T-452 forms: PROTEUS's three forms and OVERLOADED's four bodies in the new style (the user, 2026-10-28: as drawn)

## The design and tools since v11.316.8

- `3b385a81` TODO: T-475 OVERLOADED's streaks (fixed, b133f6492); T-476 generator drift to read
- `ecb3cb2f` TODO: T-452 -- PROTEUS's three forms and OVERLOADED's weathers installed (2026-10-28, the user: as drawn; PROTEUS one row at 11); OVERLOADED's battle positions and streaks fixed (engine 87557e860, b133f6492)
- `19c73b1c` T-452 forms (engine 87557e860, b133f6492): PROTEUS's three forms and OVERLOADED's weathers, as drawn (the user, 2026-10-28)
- `e3747687` qa: SYMBOL's 28 forms (v11.316.8)
- `3b63569c` manual: rebuilt for v11.316.8
- `14b1dd2a` ROM release v11.316.8: T-452 SYMBOL's 28 letter forms redrawn; batch 19's followers regenerated

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
