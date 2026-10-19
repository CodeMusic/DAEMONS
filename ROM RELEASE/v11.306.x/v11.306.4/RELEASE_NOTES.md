# DAEMONS v11.306.4 — release notes

*Released 2026-10-19 07:49 · built against the design bible v11.306*

- **Engine**: CodeMusic/pokefirered-daemons `065173dd1` (context-content)
- **Design**: CodeMusic/DAEMONS `5c11734c`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `1b0a59d3d2222c389ed9c72da287209a11a32e0a` |
| `daemonsContext.gba` | CONTEXT | `60885a8857962535299ab8c560872f8ba53f3af5` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `be8f7e5b31853be008b79770cdf2b279f6059700` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `c56de3bfa7efe8bbda7f23d2e519c79e66abb65e` |

## The engine since v11.306.3

- `065173dd1` T-427: the take VERDIGRIS names freezes at CORPUS's fall (the user, 2026-10-19)

## The design and tools since v11.306.3

- `5c11734c` T-427: the take VERDIGRIS names freezes at the fall (engine 065173dd1); profile_layout's house_take_at_fall; gbabudget
- `eb304927` TODO: T-334 placement approved; T-408's looks as a palette per universe (the user)
- `7e7a2b2b` TODO: T-210 finished -- all 110 INDEX entries approved by the user, batch by batch
- `d6f51167` TODO: ten finished tickets struck through -- T-392, T-405, T-407, T-409, T-410, T-411, T-412, T-416, T-424, T-425 (the user: close finished tickets)
- `3b317fe8` TODO: T-427 released; the amount freezes at the fall (the user)
- `aadeeb2b` qa: T-427
- `8a45addf` ROM release v11.306.3: what the house keeps goes to CORPUS -- the take in the save, the ledger, the plants, VERDIGRIS after the fall (T-427)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
