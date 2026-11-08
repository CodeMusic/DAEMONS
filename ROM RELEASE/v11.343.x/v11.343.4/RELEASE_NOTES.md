# DAEMONS v11.343.4 — release notes

*Released 2026-11-07 19:15 · built against the design bible v11.343*

- **Engine**: CodeMusic/pokefirered-daemons `dcc58f014` (context-content)
- **Design**: CodeMusic/DAEMONS `2e5bfc49`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `f890efeb9bece93e49161a7e31538711f3ea2557` |
| `daemonsContext.gba` | CONTEXT | `c84533fbcc723243a0d284a4a9c3575f96e3a0fa` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `07b2f6201c2173df1d7daf435571264deb7ae447` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `2af9e962480b22be614d8618c2cfabe1368df783` |

## The engine since v11.343.3

- `dcc58f014` T-529: THE UNITY BOOK's lens -- L and R turn every page in place between NIGHT, WHOLE and DAWN (vision 4.40; the user, 2026-11-07, by multiple choice)

## The design and tools since v11.343.3

- `2e5bfc49` T-529 built in the game (engine dcc58f014): THE UNITY BOOK's lens on L/R -- NIGHT, WHOLE, DAWN in place, the companion's rules; route tools/routes/t529_lens.json 2/2 (qa 7Nov2026 T529 49-50 private)
- `f9b4f008` ROM release v11.343.3: T-528 the aurora part 2 -- the dawn chorus, TULIKKO the fox, the conjugate light (and the SONGBOOK's empty DUET slot)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
