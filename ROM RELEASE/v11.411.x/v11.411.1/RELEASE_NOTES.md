# DAEMONS v11.411.1 — release notes

*Released 2026-11-20 21:51 · built against the design bible v11.411*

- **Engine**: CodeMusic/pokefirered-daemons `d7c977174` (context-content)
- **Design**: CodeMusic/DAEMONS `60f52298`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `23c849d1143414a5cc3d69e046cb11976780db3c` |
| `daemonsContext.gba` | CONTEXT | `72ed4b84a73868b12708efecc2d9d69e8ccf8a09` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `6b6fd6edd47a1701ce0ab427ed75407c7e72816f` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `783cbd73b5e69a9676cd2de36599a9c0be6b824c` |

## The engine since v11.410.1

- `d7c977174` T-452: ART C: OLD / NEW, a DEBUG-only viewer for the arm-C trial (the user, 2026-11-20) -- GAME EVENTS steps through the 28 daemons arm C redrew, each in a battle-like scene (terrain, front at the wild spot, back at the player's, both icons), A old/new, B next, SELECT back; the pre-arm-C art (a01ea9d67^) kept under graphics/daemons_armc_old; release ROMs byte-identical (a header in the debug file and callnative, no new .c or special)
- `a3bd7b11c` README and wiki: the playground is in daemons-eudaimonia now (daemons-companion C-438)
- `61bf54c96` README: latest is v11.410.1

## The design and tools since v11.410.1

- `60f52298` companion_export: a DEBUG screen row (R_SCREEN, T-452's ART C: OLD / NEW) has nothing held to read -- skip it
- `21c2014c` T-452: armc_verdict.json, the 28 arm-C daemons pending the user's keep/revert (engine pokefirered-daemons@d7c977174, the viewer)
- `7b9bc36a` C-435: daemons-praxis, PRAXIS's engine, is its own repository
- `851a06f5` daemons-playground becomes daemons-eudaimonia (companion C-438)
- `a3fe501b` Tickets nightly 2026-11-20: the Redmine export (T-581)
- `e4574fef` Bible v11.411: TRAINER TOWER's face released (v11.410.1)
- `4b24869f` qa: T-601 the tower's face, the time posted (v11.410.1)
- `2231232e` README, wiki: the newest release is v11.410.1
- `fd731f7a` ROM release v11.410.1: T-601 TRAINER TOWER's face, the time posted (DRAFT art), and DaemonSong_Listen looking on past an unseen daemon; seals v11.409.x

## The design bible's own entry for v11.411

### v11.411 — 2026-11-20

- Recorded from release v11.410.1 (fd731f7a, engine a4e3cff97), which sealed v11.409.x:
  - **T-601, TRAINER TOWER's face** (DRAFT art): THE TIME POSTED, the user's AFT -- a storey bar a floor, each window a stopwatch. In 9.29.
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
