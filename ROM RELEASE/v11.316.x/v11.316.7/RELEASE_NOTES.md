# DAEMONS v11.316.7 — release notes

*Released 2026-10-28 17:51 · built against the design bible v11.316*

- **Engine**: CodeMusic/pokefirered-daemons `0624b3b39` (context-content)
- **Design**: CodeMusic/DAEMONS `e473173f`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `5b3e6aa82cd6d7b968caa5b908ca4dc2c113de11` |
| `daemonsContext.gba` | CONTEXT | `e5e680eb4d7667a0f6969fb64f743d91b98137ed` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `86b22606e5caf8ba0c01bc68488945d85c5cf709` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `6c0e22df53d84be8b558abc901ae5b8fbf84abf2` |

## The engine since v11.316.6

- `0624b3b39` T-452 batch 19: SINGLETON to OVERTONE (398-411 less PROTEUS, 13) in the new style, on the RECOMMENDED choices -- SINGLETON an orb that is all one eye (the only one-eyed draft, the icon draft, cut to its circle and ringed in ink) and PAIRWISE two of it fused side by side; hand-drawn keys (FEDERATED's four cores, DEUCALION's stone cracks, KHIONE's snowflakes, TALOS's chest bolt, GAIA's two-peaked mountain and tree, OURANOS's cloud, POLYDEUCES's star, CASTOR's dark neck, OVERTONE's rings of sound); the type-hue trap fixed (STEEL's orange irises crimson and yellow cores teal, TALOS's brown, WATER and ICE blues greyed into the ramp), backs the front mirrored with the face out, grounds off; grounding rows, icon palettes, follower art and palettes. PROTEUS keeps T-440's three forms (the user: redrawn as a job of their own).

## The design and tools since v11.316.6

- `e473173f` T-452 batch 19 built (engine 0624b3b39): SINGLETON to OVERTONE (398-411 less PROTEUS, 13), on the RECOMMENDED choices (2026-10-28); drafts in gfx/drafts/t452/x, questions in x/questions.md (28 items), remaining.md (nothing left for the batch method: PROTEUS's three forms and SYMBOL's 28 their own jobs, MISSINGNO kept) -- SINGLETON the one-eyed draft as an orb and PAIRWISE two of it fused (orbs19.py), hand-drawn keys (FEDERATED's four cores, DEUCALION's cracks, KHIONE's snowflakes, TALOS's bolt, GAIA's mountain, OURANOS's cloud, POLYDEUCES's star, CASTOR's dark neck, OVERTONE's rings of sound), the type-hue trap fixed, backs the front mirrored with the face out, grounds off; TODO's T-452 note; scripts batch19.py, chain19.sh, prep19.py, orbs19.py, hand_b19.py, recolour19.py, icons19.py, ba19.py, ba19.sh, view19.py, grid19.py, grp19.py, build19.py and the batch 19 subjects
- `0aa583a7` qa: T-452 batch 18 sheets (v11.316.6)
- `84555947` manual: rebuilt for v11.316.6
- `d5ff95fb` ROM release v11.316.6: T-452 batch 18 (REDACTED to EPIPHANY) on the recommended choices; OVERLOADED's art reaches CASTFORM's normal form

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
