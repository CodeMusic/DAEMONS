# DAEMONS v11.335.5 — release notes

*Released 2026-11-01 11:07 · built against the design bible v11.335*

- **Engine**: CodeMusic/pokefirered-daemons `0c85d5b88` (context-content)
- **Design**: CodeMusic/DAEMONS `22cdfb66`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `497bdd48623721cf31551240d07c4bdd67609d13` |
| `daemonsContext.gba` | CONTEXT | `03730245b7468b5f5881e495df3dec8398022e58` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `28259bc59183c62fde1109b054f2d3ece4d76c33` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `adc2eaac5db883e2d8b63720bb4f5ccf49c8ab27` |

## The engine since v11.335.4

- `0c85d5b88` T-483 (5): THE PROCESS and THE SEAM in the SPELLBOOK, and THE MIRROR's opposed pair

## The design and tools since v11.335.4

- `22cdfb66` qa: C-266 the companion's care looks (companion 7dfe478)
- `04f5eece` TODO: T-483 (5) THE PROCESS and THE SEAM (engine 0c85d5b88); the user: opposed = a type and what it fears
- `7ac6d808` T-483 (5): theatre route t483_process_seam (4/4) and qa 1Nov2026 T483 4-7 -- THE PROCESS and THE SEAM; t483_spellbook's LENS and FIELD now DOWN 11 and 12 (6/6; t483_pull 3/3, t483_room_mirror 3/3, t483_return_hand 3/3 unchanged)
- `cf1f962b` ROM release v11.335.4: T-483 (5) THE RETURN and THE SMALL HAND in the SPELLBOOK, and both hands in one hour

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
