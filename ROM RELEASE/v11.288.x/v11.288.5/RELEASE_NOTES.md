# DAEMONS v11.288.5 — release notes

*Released 2026-09-25 21:41 · built against the design bible v11.288*

- **Engine**: CodeMusic/pokefirered-daemons `58c587134` (context-content)
- **Design**: CodeMusic/DAEMONS `26d8b710`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `cea605c71b237a7c3599b505a3ea6492dafb1c65` |
| `daemonsContext.gba` | CONTEXT | `9088bbedfc959c7d708b03a96d4f3c2ab63ba863` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `384e6cf704d292121859569692a0942f86854dbc` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `48dadb5e8abe5f890a52be81cbbcb973b4a6f784` |

## The engine since v11.288.4

- `58c587134` T-293: twelve daemons' streaks were never switched on; DARIO follows PSYCHIC F again

## The design and tools since v11.288.4

- `26d8b710` T-293 closed: ten generators brought level, fourteen refuse to undo later work
- `28ee0835` T-292 closed, T-293 opened (bring the stale generators level); engine.md trap 34 points at --writes
- `8a794940` check_generators --writes: every tool's write, for real, in a sandbox; generator_drift.json records the 24 whose write would change committed files, and why (T-292)
- `5eb8e52c` ROM release v11.288.4: PROTEUS drawn as ours on THE ANNEX; the overworld daemons' true-black outline

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
