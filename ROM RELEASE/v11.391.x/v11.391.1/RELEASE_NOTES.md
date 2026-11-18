# DAEMONS v11.391.1 — release notes

*Released 2026-11-17 22:17 · built against the design bible v11.391*

- **Engine**: CodeMusic/pokefirered-daemons `ba5c05d43` (context-content)
- **Design**: CodeMusic/DAEMONS `2d0337b6`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `6e4c96deaf0e8316bc9d54906957f37c6030cb24` |
| `daemonsContext.gba` | CONTEXT | `f048434064f0835c8b4b87f1ba6f66cbcdd04750` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `74b1fea17c72a3cec9f3fd90c95687d6494c432b` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `33b2798520d5b3672257a26cafa6f2959166ae3e` |

## The engine since v11.390.1

- `ba5c05d43` T-565 batch 11: the 388 cries, A shaped by B -- each its type's motif in C BOTH, ordered and timed by its name, a line sharing one contour, lower and slower as it grows (the user's pick, DRAFT; tools/gencries.py); 310 KB smaller than pret's
- `a9585fdf8` README: the release line names v11.390.1

## The design and tools since v11.390.1

- `2d0337b6` T-565 batch 11: the cries approved, all 388 (the user)
- `62de2c55` TODO: Redmine's mirror (cries of their own, later)
- `8281330b` T-565 batch 11: tools/gencries.py -- all 388 cries drafted as A shaped by B, checked three ways (DRAFT; nothing in the engine)
- `1a636826` Bible v11.391: THE MARGINS' music in B-flat and B (T-565 batch 9, v11.390.1)
- `0871ae84` T-565 batch 11: the cries' pick -- A, THE TYPE'S VOICE, shaped by B (the user, 2026-11-17)
- `dc821f69` T-565 batch 11: the cries, a design question -- four approaches with examples for the same six daemons (DRAFT; nothing built)
- `0e51fa77` qa: T-565 batch 9's islands as built, the sheet sent with the push
- `668e604a` README and wiki Home name v11.390.1: THE MARGINS have music of their own
- `78eb5bcd` ROM release v11.390.1: T-565 batch 9, the islands in C, in B-flat and B (DRAFT); seals v11.389.x

## The design bible's own entry for v11.391

### v11.391 — 2026-11-17

- Recorded from release v11.390.1 (78eb5bcd, engine 7e6abcda8), which sealed v11.389.x:
  - **THE MARGINS' music** (T-565 batch 9, the Musical Instruments lane): the islands in voice C, in B-flat and B. DRAFT. In 7.4, after the achromatic towns, and a line in 9.5.
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
