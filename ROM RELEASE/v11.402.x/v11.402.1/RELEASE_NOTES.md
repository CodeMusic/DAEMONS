# DAEMONS v11.402.1 — release notes

*Released 2026-11-18 16:03 · built against the design bible v11.402*

- **Engine**: CodeMusic/pokefirered-daemons `ce02dbf00` (context-content)
- **Design**: CodeMusic/DAEMONS `c3c50b3a`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `790494e1565fdd71afc3e7acae45200dfeb71bbd` |
| `daemonsContext.gba` | CONTEXT | `8d2865168f4caf5cd8712eedcfa0402472119f72` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `0f950ca949490f833cbf09ca740cc81d2649a1b5` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `3fee2769ae4286b382d103b9d388062a46663eb6` |

## The engine since v11.401.1

- `ce02dbf00` T-593: T-565 batch 13, pret's last music -- fourteen ours in voice C (DRAFT)
- `8d8f04976` README: latest is v11.401.1

## The design and tools since v11.401.1

- `c3c50b3a` T-438: the islands' leftovers recounted and drafted (gbaislands --t438k), UMBRAL ASCENT's own tiles drafting (gbacaves --umbral); DRAFT, nothing approved
- `43f0d8af` TODO: Redmine's mirror (T-593 closed)
- `bf05dee4` T-593: T-565 batch 13, pret's last music (engine pokefirered-daemons@ce02dbf00, DRAFT) -- tools/genrestmusic.py writes fourteen in voice C over pret's slots; the census and song-status say pret's music is left only where an event ticket or nothing reaches; heard on the debug ROM (qa 18Nov2026 T593 31)
- `8db1eb53` Bible v11.402: the split's step 3, the day symbol and the six FUCHSIA maps released (v11.401.1)
- `dcb53e13` qa: T-490 step 3 applied (v11.401.1)
- `a7eb99ec` engine.md: the budgets after v11.401.1 (gbabudget --write)
- `686c28a5` README, wiki: the newest release is v11.401.1
- `9d979bd3` ROM release v11.401.1: T-490 step 3 contact is physical (DRAFT words), T-591 the dream's day symbol, T-592 the six FUCHSIA maps' music; seals v11.399.x

## The design bible's own entry for v11.402

### v11.402 — 2026-11-18

- Recorded from release v11.401.1 (9d979bd3, engine de196c85c / b4f09c0ad / 521a06af6), which sealed v11.399.x:
  - **The split's step 3** (T-490): contact is physical, applied -- 67 routines change side (18 PHYSICAL, 49 SPECIAL), ten kept by ruling; the blast halves the defence it strikes and Thick Fat the stat the hit uses; PAGE FAULT's words (DRAFT). In 2.12, whose heading now says three built.
  - **The day symbol in the DREAM LOG** (T-591): released. 3.8.
  - **The six MUS_FUCHSIA maps** (T-592): each plays the music of the map its door opens onto; MUS_FUCHSIA plays nowhere, so 22 song slots are still pret's. 7.4 and 9.5.
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
