# DAEMONS v11.331.1 — release notes

*Released 2026-10-29 21:14 · built against the design bible v11.331*

- **Engine**: CodeMusic/pokefirered-daemons `a1df61167` (context-content)
- **Design**: CodeMusic/DAEMONS `0eb5936f`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `b92dad9667a04fb49443b3d21fa8a7d3b8ae323f` |
| `daemonsContext.gba` | CONTEXT | `02355732e6c9953f8c0ad01973b64884af2d3fdb` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `d71d875bcb3a7307cecb135e6402afe98592c7d9` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `d5e1035a1419efd97f2c174fd3ffbbd9c4b9a6ac` |

## The engine since v11.330.1

- `a1df61167` T-488 (DRAFT): the * SINK items -- sixteen held items that halve one super-effective hit of their type
- `3e1551ba2` T-492 (DRAFT): a daemon GIVEN -- GIFTED, bit 11 of 0x1E, its own line and FIRST MET: A GIFT
- `247e03c51` README: latest release v11.330.1

## The design and tools since v11.330.1

- `0eb5936f` qa: C-223 GIVE AN ITEM
- `920ac6ad` TODO: T-488 keeps SIGNAL SINK beside LIGHTNING ROD's ability (the user)
- `d0e81b1e` T-488: the * SINK family in the tools -- names and lines, SWARM's palette, the lexicon's allowance
- `124c40f1` T-492: companion_export carries GIFTED (gifted_shift, gifted_mask) and names FIRST MET's A GIFT
- `829c9d2a` qa: C-223 FRIENDS on TRADE
- `15b44a30` README and wiki: v11.330.1; CONSENSUS, SLANT and ALIGN read the party (T-489, T-491)
- `a539a3c9` Bible v11.331: ALIGN and CONSENSUS / SLANT released (T-489, T-491, v11.330.1)
- `50a042a7` TODO: T-489, T-491 struck -- released v11.330.1
- `0ae47630` manual: rebuilt for v11.330.1
- `0f0d28e6` ROM release v11.330.1: T-489 ALIGN; T-491 CONSENSUS and SLANT; v11.329.x sealed

## The design bible's own entry for v11.331

### v11.331 — 2026-10-29

- **ALIGN, released in v11.330.1 (T-489).** ALIGN is routine 382, typed CONTEXT. The foe becomes wholly the user's first type. SCORN's ace knows it in the two CORPUS battles only, which is what the user chose. PLUGIN49 (formerly SNATCH) teaches it and lies on CORPUS HIDEOUT B4F. The frame family's table now marks the reverse as built.
- **CONSENSUS and SLANT, released in v11.330.1 (T-491).** CONSENSUS runs from 90 to 120 as the party's types overlap. SLANT, the CONTEXT routine, runs from 65 to 95 as they diverge. Whether this rewards SCORN's kind of convergence is left to playtest.
- A Settled entry in section 10. Every word is DRAFT.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
