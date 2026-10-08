# DAEMONS v11.297.3 — release notes

*Released 2026-10-08 13:39 · built against the design bible v11.297*

- **Engine**: CodeMusic/pokefirered-daemons `4e48916d0` (context-content)
- **Design**: CodeMusic/DAEMONS `cc145135`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `6483f76b840cc70da8d08e4e914a24cd3b40606a` |
| `daemonsContext.gba` | CONTEXT | `2393847581f8a0d9c725429e835b1af99e1529a1` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `bcc69bdc58e2b0b23163baef56b78894383cd261` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `d754f31ef052928a85a0fb79974c8b53ce31e133` |

## The engine since v11.297.2

- `4e48916d0` T-392 (DRAFT, debug ROMs only until approved): the game's signature in battle -- the splash's 0, 1 and notes as particles (ANIM_TAG_DAEMONS_GLYPHS in the splash's own colours, ANIM_TAG_DAEMONS_INK grey and shaded into a routine's type by AnimTask_DaemonsInk; one sprite, seven paths: stream, rise, fall, ring, converge, sweep, return). The seven union routines get their own scripts carrying both, in the splash's colours (FLUENCY's line read twice, STILLPOINT's rings, RECONNECT's broken line, PRAXIS rising, MEDIAN converging, PANORAMA's sweep, HINDSIGHT going back first); 141 routines of the chart's two sides re-drafted by genanims with bits (CONTENT, LOGIC, STRATUM, LEGACY) or notes (CONTEXT, LATENT, VECTOR, ENTROPY) in their type's ink. The release ROMs keep the approved scripts until the user approves these.

## The design and tools since v11.297.2

- `cc145135` T-392 drafted (engine 4e48916d0): the splash's bits and notes in battle -- the seven union routines' own effects, and 141 routines with bits or notes in their type's ink; genanims learned GLYPH_FAMILIES and --glyphs. Debug ROMs only until approved.
- `7cf1db2f` ROM release v11.297.2: wisdom -- the leaders and their roots, seven union PLUGINs, INSIGHT (T-389, T-390)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
