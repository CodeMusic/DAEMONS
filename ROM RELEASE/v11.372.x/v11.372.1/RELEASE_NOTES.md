# DAEMONS v11.372.1 — release notes

*Released 2026-11-15 16:30 · built against the design bible v11.372*

- **Engine**: CodeMusic/pokefirered-daemons `80271363f` (context-content)
- **Design**: CodeMusic/DAEMONS `2bd90707`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `30962a49e51338d35807dd6e6c4cb55900d22c43` |
| `daemonsContext.gba` | CONTEXT | `9e2f36fa1d8867287f49d6127ff4a8fe993eff46` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `224e0e7d20160ccebb6074093502caada50c510a` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `60ce05065014599d9cdc1b845b770193c0216f21` |

## The engine since v11.371.1

- `80271363f` T-568: the new game and the name -- keycaps in the controls guide, the panel's graph paper with a quaver for the ball, CRYSTAL's graph-paper floor and pad, the naming screen's keycap buttons and tabs, bracket cursor, prompt marks and terminal PC icon (the user's picks, DRAFT; tools/gbanewgame.py)
- `cb00af971` README: the release line names v11.371.1

## The design and tools since v11.371.1

- `2bd90707` T-568 BUILT: the new game and the name, the user's picks (engine 80271363f); gbanewgame's report reads the CRLF .pal as written
- `4b98efa4` T-568 DRAFT: the new game and the name -- the census and A/B/C for the art they still draw
- `916ce03b` Bible v11.372: evolving, using, learning (T-566, v11.371.1)
- `af503bf3` TODO: T-568 the new game and the name (batch 7, the user's pick)
- `6a8d0668` README and wiki Home name v11.371.1
- `5a2fdbb7` ROM release v11.371.1: T-566 evolving, using, learning -- the evolution's square wave and its bit, graph paper for an item used, the relearner's paper and carets, the egg's shell (DRAFT); seals v11.370.x; two recordings deferred

## The design bible's own entry for v11.372

### v11.372 — 2026-11-15

- Recorded from release v11.371.1 (5a2fdbb7, engine f85229ba1), which sealed v11.370.x:
  - **Evolving, using, learning** (T-566), the user's picks: the evolution's square wave and its bit, graph paper and carets for an item used, the relearner's paper and caret, the egg's shell. DRAFT. T-567 (the relearner's "move") filed.
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
