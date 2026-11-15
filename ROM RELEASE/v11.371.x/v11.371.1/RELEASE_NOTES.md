# DAEMONS v11.371.1 — release notes

*Released 2026-11-15 15:12 · built against the design bible v11.371*

- **Engine**: CodeMusic/pokefirered-daemons `f85229ba1` (context-content)
- **Design**: CodeMusic/DAEMONS `c6110035`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `73ab154a4dbed5c20a3300b7521dcf37c1b2bbd8` |
| `daemonsContext.gba` | CONTEXT | `115d7af14e2df9323eb93ff9b35ee82a84eafe6e` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `b5b3ebdb33bf7f59f8b62e9b152983030ce9b527` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `12e205dd1b2bf508b60fad8262d4fd949e9be700` |

## The engine since v11.370.1

- `f85229ba1` T-566: evolving, using, learning -- the evolution's square wave and its bit, graph paper for an item used, carets, the mark, 0 1 dots, the relearner's graph paper and caret arrows, the egg's shell (the user's picks, all A, DRAFT; tools/gbaevolve.py)
- `b51f13d2f` README: the release line names v11.370.1

## The design and tools since v11.370.1

- `c6110035` T-566 BUILT: evolving, using, learning, the user's picks (engine f85229ba1); T-567 the relearner still says move
- `a577df46` T-566 DRAFT: evolving, using, learning -- the census and A/B/C for the art they still draw
- `481b34af` Bible v11.371: the boot screens' last pieces (T-564, v11.370.1)
- `96cfd9e7` TODO: T-566 evolving, using, learning (batch 6, the user's pick)
- `87cf7d06` README and wiki Home name v11.370.1
- `776e4530` ROM release v11.370.1: T-564 the boot's last pret pieces -- the CodeMusic mark leads the splash's trail, graph paper under it, bit rain across the title, a rule at its band edge (DRAFT); seals v11.369.x; two recordings deferred

## The design bible's own entry for v11.371

### v11.371 — 2026-11-15

- Recorded from release v11.370.1 (776e4530, engine fb7aeb81c), which sealed v11.369.x:
  - **The boot screens' last Nintendo pieces** (T-564), the user's picks: the CodeMusic mark leading the splash's trail, graph paper under it, bit rain across the title, a rule at its band edge. DRAFT.
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
