# DAEMONS v11.301.9 — release notes

*Released 2026-10-16 17:18 · built against the design bible v11.301*

- **Engine**: CodeMusic/pokefirered-daemons `5aa2115c3` (context-content)
- **Design**: CodeMusic/DAEMONS `900b3804`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `7e35727036434d988e25af2ef34959eb205b5a20` |
| `daemonsContext.gba` | CONTEXT | `e95434eaa13075ba30af98a669900a1c54509150` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `cb5094e27c676753a4d7acf393ea959f094f60f9` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `2049c5efe4130d72d2319170c25cef676889e6a1` |

## The engine since v11.301.8

- `5aa2115c3` The glitch on MISSINGNO's encounter (the user, 2026-10-16): wild or scripted, the screen tears before the battle begins; DaemonsGlitch_Start lets a non-script caller run it

## The design and tools since v11.301.8

- `900b3804` T-414 (engine 5aa2115c3): the glitch on MISSINGNO's encounter
- `0d606e87` qa: the BOX-3 speaking with checked mouths (companion C-138)
- `f6a0161a` ROM release v11.301.8: the fir in B-flat with the painting's colours and MUS_NEXUS with it (T-409), SCORN's converged party (T-413)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
