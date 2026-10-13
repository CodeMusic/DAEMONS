# DAEMONS v11.300.1 — release notes

*Released 2026-10-13 19:12 · built against the design bible v11.300*

- **Engine**: CodeMusic/pokefirered-daemons `1e50476ad` (context-content)
- **Design**: CodeMusic/DAEMONS `dc5b1f6d`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `e30f77a101a64c04ec2a78942aa1e8749322318b` |
| `daemonsContext.gba` | CONTEXT | `284c5a9586084f453f32b352654f37a55b5a086d` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `bc6923466802e2d24b47e0577b8b88e1376c47d0` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `ada937109ea3cd313606a12a987c94a225f779cd` |

## The engine since v11.299.5

- `1e50476ad` T-120: the AQUA admin is a tiger shark (the user, 2026-10-13), not a second great white beside ARCHIE
- `6e3216bf8` T-393 (the user, 2026-10-13): MIND READER is ANTICIPATE, not LOCK ON -- vanilla's LOCK-ON is in the game under its own name, and two routines with one effect were nearly called the same thing. MIND READER's description already says it predicts what the other will do. The Reading Room's ATTENTION lecturer teaches it (TUTOR_MOVE_ANTICIPATE). DESCEND unchanged: learned by level (HEATSINK 37, ARCHIVER 42); DRIVER08 stays in the debug kit.

## The design and tools since v11.299.5

- `dc5b1f6d` T-120: the AQUA admin as a tiger shark (engine 1e50476ad) -- seed 13017, stripes painted on the head since the model draws none
- `c71119d4` T-393 struck (engine 6e3216bf8; the user, 2026-10-13): MIND READER is ANTICIPATE, vanilla's LOCK-ON keeps its name, and DESCEND was learnable all along (HEATSINK 37, ARCHIVER 42) -- DRIVER08 stays debug-only. Bible v11.300 (4.35, school.md §8 and §10), CHANGELOG, the v11.300 PDF cut and v11.299's removed.
- `4c31fb47` qa: v11.299.5's sheets -- MAGMA red, Group 3 as shipped, six hammerhead tries (T-120)
- `67bf676a` ROM release v11.299.5: every trainer portrait ours -- Hoenn's 81 redrawn in three groups, BRENDAN and MAY as the grey monkey (T-120)

## The design bible's own entry for v11.300

### v11.300 — 2026-10-13

### Two LOCK ONs, and DESCEND (T-393)

- ***4.35, the Reading Room (the user)***: **ATTENTION's routine is `ANTICIPATE`**, *not LOCK ON. MIND READER had been renamed LOCK ON while vanilla's LOCK-ON stayed in the game under its own name, so two routines with one effect were called nearly the same thing; MIND READER's description already said it* predicts *what the other will do, so it took the name that says that. LOCK-ON keeps its own.*
- ***DESCEND stays without a DRIVER (the user)***: *T-391's audit said DESCEND was never given; it has been learned by level since T-36 -- HEATSINK at 37, ARCHIVER at 42. Only DRIVER08, which would teach it, is debug-only, and stays so: FireRed has no deep water, so a DRIVER would teach a routine with nowhere to use it.*

---

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
