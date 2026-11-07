# DAEMONS v11.342.7 — release notes

*Released 2026-11-07 10:49 · built against the design bible v11.342*

- **Engine**: CodeMusic/pokefirered-daemons `978e4ec10` (context-content)
- **Design**: CodeMusic/DAEMONS `f7aa41ff`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `2cff8599e1489b6cdf8b1b43277fbb5ebabb8846` |
| `daemonsContext.gba` | CONTEXT | `ceea0e22c4eb6d7df467df411950e0f79f76639e` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `c6bfbbffb4e174d9f93600167d55549fa36ce88c` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `ff6ee7509b09e7698d7e02e86b1b84c39a970598` |

## The engine since v11.342.6

- `978e4ec10` T-526: the TRAP TABLE -- THROTTLE TRAP's row whole, and ten TRAP descriptions in its two lines (the user, 2026-11-07)
- `c6744bae5` T-526: 16 item descriptions that still read as FireRed's, redrafted (the user, 2026-11-07: "Build all 16")
- `cfa651de8` T-525: batch 3 of the item icons built -- 57 drawn by hand in code (the user, 2026-11-07: "Build all 57")

## The design and tools since v11.342.6

- `f7aa41ff` T-526 built (engine c6744bae5, 978e4ec10): 16 item descriptions, SUBTLE LAYER a USER's handbook, the TRAP TABLE's rows and two-line TRAPs
- `7bb7786d` T-525: batch 3 of the item icons built (engine cfa651de8) -- the user, 2026-11-07: "Build all 57"
- `0b84c9f3` TODO T-526: the user's answers -- build all 16; USER on the SUBTLE LAYER item and cover; HOLT's ticket and the cookie kept; scarves name the day
- `ad219c56` T-526: item descriptions still FireRed's -- 16 drafted, nothing in the engine (DRAFT, the user away)
- `67f14338` T-525: batch 3 of the item icons drafted -- 57 drawn by hand in code (the GAINs, the held items, the TRAPs), nothing in the engine (DRAFT, the user away)
- `1ea6bc6a` ROM release v11.342.6: T-525 item icons batch 2 -- 47 more drawn by hand (the TUNE dials, vitamins, evolution inputs, TONE forks, drinks, passes, keys, cores)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
