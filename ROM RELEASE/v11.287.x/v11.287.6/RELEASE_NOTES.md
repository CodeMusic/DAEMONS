# DAEMONS v11.287.6 — release notes

*Released 2026-09-25 16:26 · built against the design bible v11.287*

- **Engine**: CodeMusic/pokefirered-daemons `954e8199d` (context-content)
- **Design**: CodeMusic/DAEMONS `725afb68`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `52699f4075dc5d733fbf36efe0958b1b50057aeb` |
| `daemonsContext.gba` | CONTEXT | `1087f35306fb598400fd0215d10cde09de94fd24` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `276860d6920465b9a7d9965e34a41b307965fc2f` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `e8466a146ee6d0485de2e5166b7f9937e9166090` |

## The engine since v11.287.5

- `954e8199d` T-265: a clock in 12-hour mode is still a clock -- read its hour with the PM flag instead of refusing it

## The design and tools since v11.287.5

- `725afb68` T-265: a 12-hour clock is read (engine 954e8199d); CHANGELOG v11.287 carries it
- `9dde002b` gbabudget: the ROM row is the 16 MB file and its 9.2 MB contents -- the table said 14.7 of 32 while the paragraph under it said 9.2 of 16
- `3be9ebd3` ROM release v11.287.5: night water on Routes 10 and 12, the brain on your own card only

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
