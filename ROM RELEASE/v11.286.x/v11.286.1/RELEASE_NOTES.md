# DAEMONS v11.286.1 — release notes

*Released 2026-09-25 11:26 · built against the design bible v11.286*

- **Engine**: CodeMusic/pokefirered-daemons `e7da4c4ca` (context-content)
- **Design**: CodeMusic/DAEMONS `355df46c`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `3db4060a93139cb36bece8423a89c445e4f42feb` |
| `daemonsContext.gba` | CONTEXT | `2a9786485f28c21264a6e72d44b65e195db33124` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `c421185a4bfa505fea2df526861d9699aba599a3` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `43cf2283c05596b9e26b900a42a945e785f65802` |

## The engine since v11.285.3

- `e7da4c4ca` T-273/T-269/T-274/T-275: DEBUG sets the day; the day's banner, note and trim

## The design and tools since v11.285.3

- `355df46c` v11.286: the week -- named on leaving a building, heard at the terminal, coloured on the CHECKPOINT's trim
- `93a56452` TODO: the user's answers of 2026-09-25 -- the Guide's margins hold the understandings; the day's note heard, its colour on the CHECKPOINT's trim; DEBUG sets the clock
- `f3b84b4a` ROM release: the monkey on the trainer card; B backs out of DEBUG

## The design bible's own entry for v11.286

### v11.286 — 2026-09-25

### The week

- ***The day, named, heard and coloured*** (9.21, T-269, T-273–T-275): **out of a door the name popup slides in again with *F · WEDNESDAY · NIGHT*** *(DRAFT)*; **TUNE at the terminal sounds the day's note first**; **the CHECKPOINT rotunda's trim takes the day's colour**, *the user's rainbow bent where it met a type hue (`tools/gbadaytrim.py`).* ***DEBUG → TIME*** *sets the watch and the weekday.* *The weekday comes from the clock's register, or one day per hour of play.*

---

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
