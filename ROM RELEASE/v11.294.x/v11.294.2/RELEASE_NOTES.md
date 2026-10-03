# DAEMONS v11.294.2 — release notes

*Released 2026-10-03 14:46 · built against the design bible v11.294*

- **Engine**: CodeMusic/pokefirered-daemons `e42fb3d95` (context-content)
- **Design**: CodeMusic/DAEMONS `c434240e`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `ff2c3685a7ac219eefe0ab9485f5c412fecba6f9` |
| `daemonsContext.gba` | CONTEXT | `ffc0a920176eee9ad579d64250aa0ee2e32b4f33` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `4a8effef4879f39a964d7b149a92b135046e6f98` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `33d39548ab24cc09967397493ca9acb403b82faa` |

## The engine since v11.294.1

- `e42fb3d95` school lift: the blue lamp fades with the building (T-355, T-357)
- `3cc9306df` debug kit: the parcel delivered and OPUS's flag set (T-357)
- `19cce2a38` T-353, T-354: on FINISH EXAM, the list shows its last six questions, not a blank row

## The design and tools since v11.294.1

- `c434240e` T-357: the unseen builds seen in the theatre (engine 19cce2a38, 3cc9306df, e42fb3d95)
- `6f144f13` qa: the companion app's three screens (C-05)
- `f4de6ae1` companion_export: RoverRadio's day table in the week (companion C-01)
- `62c073e4` companion_export: the save layout, read from the built game (C-02)
- `ecd2b08f` tools/companion_export.py (companion C-03) and tools/seasons.py (C-14, T-359): one export, one season
- `e884cd47` qa: T-360, the OWL after the DIPLOMA
- `d48f2f66` ROM release: the OWL congratulates and goes over the misses (T-360)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
