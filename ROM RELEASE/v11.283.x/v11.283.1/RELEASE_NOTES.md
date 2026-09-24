# DAEMONS v11.283.1 — release notes

*Released 2026-09-24 10:05 · built against the design bible v11.283*

- **Engine**: CodeMusic/pokefirered-daemons `fc95bd854` (context-content)
- **Design**: CodeMusic/DAEMONS `796391db`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `238651afa7fe37612e68d3a730022619786e5934` |
| `daemonsContext.gba` | CONTEXT | `8caa07fa89475e198c361cf175e773b603175af1` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `2738388880efbd91f16064e86cb21e209040e467` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `c2eb8673e2016e38c347167e4a0a9598d59ec12a` |

## The engine since v11.282.2

- `fc95bd854` The choice at the title is not a gender: five lines that said son or lassie

## The design and tools since v11.282.2

- `796391db` v11.283: an audit of what was adopted and never built
- `2da55a47` ROM release v11.282.2: the WARDEN's TOKEN

## The design bible's own entry for v11.283

### v11.283 — 2026-09-24

### An audit of what was adopted and never built

- ***The WARDEN's TOKEN*** (T-260): **8.6 adopted it and vanilla's GOLD TEETH were still in the game** — *the item, its description, four lines, and a key fob drawn by `tools/gentoken.py`. THE HOLDOUT, the SAFARI ZONE's proposed name, is left for the user.*
- ***The choice at the title is not a gender*** (9.10 corrected): **five scripts still called an INSTINCT player a girl and a REASON player a boy** — *each pair now says one thing, and `check_lexicon` fails any branch that does not, beyond the four VOICE pairs written on purpose.*
- ***8.6's "Ty is not in the ROM" is no longer true*** (T-261): *T-19 put him in the warehouse; whether the post-game triangle is still owed is the user's.*
- ***The missing key signature, proposed for a grove*** (T-10): *BRAZEN's maze was approved as it is, and the source has a tree sing the song.*
- *4.35's heading said "built nowhere"; the school has been built since 2026-09-22.*

---

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
