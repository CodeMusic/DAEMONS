# DAEMONS v11.297.2 — release notes

*Released 2026-10-08 13:11 · built against the design bible v11.297*

- **Engine**: CodeMusic/pokefirered-daemons `b48740f91` (context-content)
- **Design**: CodeMusic/DAEMONS `064a6aed`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `f5134f7b31573d18d28096f0a8dbd14def8883f3` |
| `daemonsContext.gba` | CONTEXT | `504b0dd2d7d15e279bcb5cb3f44bfbc4f21977f2` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `52d7cab40ba66bec6b5e0f71081e83802578310b` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `c77397c774393c692f0c83071219e4fdc2b9ff50` |

## The engine since v11.297.1

- `b48740f91` T-389, T-390 (DRAFT): wisdom -- a MARK and its ROOT together (bible 0.7). Seven leaders, talked to after the win, say what their MARK taught and where to come back understanding, or, with it held, what the two make together, and hand over the union routine's PLUGIN once (CAIRN/SCHOOL FLUENCY, BASIN/FIRST STILLPOINT, GAUGE/RETURN RECONNECT, TRELLIS/GUIDE PRAXIS, TILT/SCORN MEDIAN, MATTE/READING PANORAMA, ANNEAL/NOTES HINDSIGHT). The seven are new routines 357-363 on vanilla effects; PLUGINs 05, 10, 21, 32, 37, 43, 45 are repointed to them and any daemon can learn them (their old learnset bits gone, their old item balls, mart stock and Pickup slot given other items). An insight arrives on the first step once a MARK and its understanding are both held, and is filed in the NOTEBOOK's new INSIGHT section. The words come from DAEMONS docs/wisdom.json through tools/gbawisdom.py; animations are their type's placeholder until T-392.

## The design and tools since v11.297.1

- `064a6aed` T-389, T-390 done (DRAFT; engine b48740f91): the seven leaders and their roots, the union PLUGINs, INSIGHT -- docs/wisdom.json and tools/gbawisdom.py, the wisdom theatre route, genanims files the seven as borrowed scripts until T-392, check_reach reads flags set through a table; bible: FLUENCY is LEGACY, INSIGHT keeps the MARKS' order
- `b1eae104` ROM release v11.297.1: the manta (T-388) and the PLUGINs' last vanilla words (T-391); v11.296.x sealed

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
