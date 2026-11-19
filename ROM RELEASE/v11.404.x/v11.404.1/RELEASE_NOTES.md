# DAEMONS v11.404.1 — release notes

*Released 2026-11-19 01:11 · built against the design bible v11.404*

- **Engine**: CodeMusic/pokefirered-daemons `18c32d360` (context-content)
- **Design**: CodeMusic/DAEMONS `e53ce6bd`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `6f1759948c05be1b8371aec2c2940f00cec49620` |
| `daemonsContext.gba` | CONTEXT | `755d7218838c87d79f927602ff197b81e409b108` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `c806192e6c7740a002517c032e3861031653ee08` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `f62202ab63514e9da86f29f2d6e76126e12e5a9a` |

## The engine since v11.403.1

- `18c32d360` T-438: the TRAINER TOWER elevator doors' frames re-derived from the redrawn tower (gbadoors --write --approved; T-446's rule)
- `a754b6bc9` T-438: TRAINER TOWER's interior in A PROGRESS (AF) -- floors and walls as progress bars with the wall-foot shadow, the furniture as meters, the roof deck plain in our own drawing; the tower's face kept as drawn for T-601 (the user, 2026-11-18/19, DRAFT art)
- `f0627ce29` README: latest is v11.403.1

## The design and tools since v11.403.1

- `e53ce6bd` TODO: Redmine's mirror (T-438 closed)
- `cf02e50c` T-594: THE SONG, every daemon's song drafted (tools/gensongs.py, DRAFT)
- `f97e4a7a` T-438: gbatownslast APPROVED_TOWER AF with the plain roof deck (tower_deck) (engine pokefirered-daemons@a754b6bc9)
- `1dc72f69` TODO: Redmine's mirror (a new ticket: TRAINER TOWER's face, later)
- `097faab5` T-438: TRAINER TOWER v2 drafted -- A PROGRESS with the wall-foot shadow back, AF the furniture as meters, AFB the face banded (DRAFT, nothing approved)
- `de5b21e9` T-438: TRAINER TOWER's interior drafted (gbatownslast --tower: A PROGRESS, B THE LEADERBOARD, C THE RUN; DRAFT, nothing approved)
- `dbeeadd5` Bible v11.404: T-438's last part released (v11.403.1)
- `4607aa02` qa: T-438's last part built (v11.403.1)
- `9bd9cba0` engine.md: the budgets after v11.403.1
- `f46c7930` README, wiki: the newest release is v11.403.1
- `73d569de` ROM release v11.403.1: T-438's last part -- UMBRAL ASCENT's own tiles (A PENUMBRA), THE DOTS' open door, the islands' piling and railing, 8 slivers retinted (DRAFT art); seals v11.402.x

## The design bible's own entry for v11.404

### v11.404 — 2026-11-18

- Recorded from release v11.403.1 (73d569de, engine ee68884b5), which sealed v11.402.x:
  - **T-438's last part** (DRAFT art): UMBRAL ASCENT's own tiles (A PENUMBRA), THE DOTS' open door (A SLAB SUNK), the islands' piling cap and the harbours' railing corner, eight of fifteen slivers retinted, seven left on purpose. In 9.29.
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
