# DAEMONS v11.304.2 — release notes

*Released 2026-10-18 10:41 · built against the design bible v11.304*

- **Engine**: CodeMusic/pokefirered-daemons `c72068865` (context-content)
- **Design**: CodeMusic/DAEMONS `709d69be`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `055dc862da429fd398ea828c450e85a449cfb44f` |
| `daemonsContext.gba` | CONTEXT | `fa764600d184f69512d6b3dfe7d7d2f88be931a3` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `76fcefc27bf6759b4c1382c8d2cf16bbdda9c45b` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `0abd2db001d7fc4955f5c80405192fafd3661937` |

## The engine since v11.304.1

- `c72068865` T-415 WEATHER phase 2 (the user, 2026-10-17): STORM's SIGNAL and FOG's LATENT x1.25, the battle tint, the glint, weather daemons, NATIVE IN RAIN (DRAFT)

## The design and tools since v11.304.1

- `709d69be` T-415 phase 2 built (engine c72068865): weather daemons in gbashifts, NATIVE IN RAIN in gbanative, companion native weathers; TODO note
- `c0a8543f` docs: notes for bringing the psychic book into the game (T-423)
- `66c476a9` qa: C-158 -- the casino in context on the T-Watch S3: the seen daemons' reels, almost the jackpot, a near miss, readable colours, SOUND
- `99836316` TODO: T-422 waits on C-158's odds engine
- `ea006921` TODO: T-422 confirmed by the user, next after weather
- `efb04f94` TODO: T-422, the game's CASINO plays like the companion's (relayed; to confirm with the user)
- `ae1c9c77` TODO: T-416 released; its routine looks fold into T-392 (the user)
- `58efcb12` qa: T-416 P3-P4
- `0ef72146` ROM release v11.304.1: HOLIDAYS finished -- holiday daemons, the other edition's on PAIRING DAY and FIR LIGHTS, skies, light, fir glow, fireworks, the quiet days' lines (T-416 P3-P4); seals v11.303.x

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
