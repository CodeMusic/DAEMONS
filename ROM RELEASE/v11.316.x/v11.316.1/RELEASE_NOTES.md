# DAEMONS v11.316.1 — release notes

*Released 2026-10-28 11:09 · built against the design bible v11.316*

- **Engine**: CodeMusic/pokefirered-daemons `694073b91` (context-content)
- **Design**: CodeMusic/DAEMONS `1b991a40`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `66455c78f8df2a625390da488ae7425d57d006d0` |
| `daemonsContext.gba` | CONTEXT | `ddcffed81c6f22d00a09ca611e5967b2c04e49fd` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `fac59a48dfb4e744aae10fdbc93da8b2d700960d` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `2e69b84238a4d3f4f285e8768e8805de02ef02c9` |

## The engine since v11.315.5

- `694073b91` README: latest release v11.315.5; about 265 daemons drawn in the new style (T-452 batches 12-13)
- `c7f932f6b` T-452 batch 13: STUMP to UNBRANCHED (277-289) in the new style, on the RECOMMENDED choices -- hand-drawn keys (COINFLIP's two-tone coin, MONTECARLO's string of dice, LASVEGAS's die, RUNOFF's drops, SMUDGE's face smear, ECLIPSE's black disc and bright ring, DETOUR's zigzag, UNBRANCHED's back stripe and bundle), the type-hue trap fixed (the FIRE birds' orange beaks and feet crimson; GRASS greens, NORMAL browns greyed into the ramp), backs the front mirrored with the face out, grounds off; grounding rows, icon palettes, follower art and palettes. THE NEXUS eight (253-260) keep their painted art (questions 1A, the 2026-10-09 exception)

## The design and tools since v11.315.5

- `1b991a40` README and wiki: v11.315.5; about 265 daemons in the new style (T-452 batches 12-13)
- `1986100f` Bible v11.316: 9.31 the daemons redrawn with charm (T-452), followers at their own size (T-464)
- `1cb8b1c9` TODO: T-452 batch 13 built (c7f932f6b): 277-289 on the RECOMMENDED choices; THE NEXUS eight keep their painted art (1A)
- `36e1d1ab` T-452 batch 13 built (engine c7f932f6b): STUMP to UNBRANCHED (277-289) on the RECOMMENDED choices (2026-10-28); THE NEXUS eight (253-260) drafted in gfx/drafts/t452/q as reference only and NOT installed (questions 1A: their painted art, the 2026-10-09 exception, stands) -- hand-drawn keys (COINFLIP's coin, MONTECARLO's dice, LASVEGAS's die, RUNOFF's drops, SMUDGE's smear, ECLIPSE's disc and ring, DETOUR's zigzag, UNBRANCHED's stripe and bundle); scripts batch13.py, chain13.sh, hand_b13.py, recolour13.py, icons13.py, ba13.py, ba13.sh, view13.py, grid13.py, build13.py and the batch 13 subjects; batch.py keys THE NEXUS's black ground, sheet_r2.py finds nexus_<name>
- `6db2c4ad` qa: T-452 batch 12 sheets (v11.315.5)
- `1b9ad0b8` ROM release v11.315.5: T-452 batch 12 (REPAY to KAIROS) on the recommended choices

## The design bible's own entry for v11.316

### v11.316 — 2026-10-28

### The daemons redrawn, with charm (T-452, T-464)

- ***9.31***: **the redraw's rules, which had lived only in T-452's row** -- *the sprite-server style at 512 reduced to 64x64; charm over fidelity, one key prop kept, the art agreeing with each INDEX entry; coloured by type, accents near 15% and off other types' hues; icons drawn separately; THE NEXUS keeps its painted art; followers walk as their own small pictures (T-464).* **Thirteen batches built, up to 289.**

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
