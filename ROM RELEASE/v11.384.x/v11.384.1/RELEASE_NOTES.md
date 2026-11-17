# DAEMONS v11.384.1 — release notes

*Released 2026-11-16 22:32 · built against the design bible v11.384*

- **Engine**: CodeMusic/pokefirered-daemons `4e66bd3d3` (context-content)
- **Design**: CodeMusic/DAEMONS `fa141712`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `b2bbba426daf4612c5c24854a854e7e49d4b7f57` |
| `daemonsContext.gba` | CONTEXT | `63a494978264c1f1bd8ef44afa8a77f777847cf7` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `b43ad0210ff3d6f9e5c241c39e39cebeba62fff4` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `ac465c9a3fd9b62e4d423e7fe25d045d135d8725` |

## The engine since v11.383.1

- `4e66bd3d3` Merge T-565 (batches 3 and 7, the pitched sounds): the fanfares, jingles, toy piano and seven sounds, ours (5bdd716d8)
- `f1552162f` README: the release line names v11.383.1
- `5bdd716d8` T-565 (batches 3 and 7, and the pitched sounds): the fanfares, jingles, toy piano and seven sounds are ours -- our HARP and FLUTE over the cartridge, the user's pick ("C Both") from three drafts

## The design and tools since v11.383.1

- `fa141712` qa: T-565's fanfares and pitched sounds as built, the sheet sent with the push (16Nov 44)
- `a0c0ed17` Bible v11.384: VERDIGRIS DEPT. STORE as NEW COPPER (T-573, v11.383.1)
- `15b031d9` T-565: batches 3 and 7 and the pitched sounds BUILT (engine 5bdd716d8) -- tools/genfanfares.py writes the fanfares, jingles, toy piano and seven sounds in the voice the user picked, our harp and flute over the cartridge
- `0ebdbc54` README and wiki Home name v11.383.1
- `c067c8de` ROM release v11.383.1: T-573 VERDIGRIS DEPT. STORE as NEW COPPER, its own landmark (DRAFT); seals v11.382.x; every recording current

## The design bible's own entry for v11.384

### v11.384 — 2026-11-16

- Recorded from release v11.383.1 (c067c8de, engine 62de521c0), which sealed v11.382.x:
  - **VERDIGRIS DEPT. STORE as NEW COPPER** (T-573), the user's pick: a landmark drawn from the story, the one copper in the town not yet green. DRAFT. In 9.29, after T-570.
  - Also in the release, outside the bible: THE CARDPUTERS recorded (C-393, the user's "record after" honoured); The Fourth Review revised for v11.382.1.
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
