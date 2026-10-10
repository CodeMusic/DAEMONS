# DAEMONS v11.299.1 — release notes

*Released 2026-10-10 16:18 · built against the design bible v11.299*

- **Engine**: CodeMusic/pokefirered-daemons `8b3604775` (context-content)
- **Design**: CodeMusic/DAEMONS `34235ac0`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `92ace6a0c4bbdcf928f5eea58c546460d1d2d841` |
| `daemonsContext.gba` | CONTEXT | `da434843e3326acdeb22d728577d73408a49cb18` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `ec4c642776d5d1a7a4a7f4f79610d86b0bb162ff` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `795309f630e83788cdbc03ddf510f99daec6e9a6` |

## The engine since v11.298.2

- `8b3604775` T-395: THE NEXUS -- the fir in every grove, flat until its key, and through it a place made entirely of paint

## The design and tools since v11.298.2

- `34235ac0` T-395 done (engine 8b3604775): THE NEXUS -- the fir in every grove, flat until its key; through it a place made of paint whose trees are doors to the groves already found, a Christmas tree home, the GUARDIAN at every door, THE (NOT A) HUNTER, PHOENIX once, the residents in the meadow. tools/gbanexusmap.py (the place, its tileset from spriteforge drafts), gbagrove.py (a fir and a FOUND flag in every grove), gensingingfir.py (the dim fir's palette), genhunter.py (the bear). Bible v11.299: 3.4 THE NEXUS, and 9.4's one exception to colour-by-type for its residents. theatre_route.py accepts two objects on one tile; tools/routes/nexus.json is ready for the theatre. Every word DRAFT.
- `2b28aa46` qa: the companion's SI4732 CHANNEL and LIGHTNING screens (C-101) and the M5Stack Dial's round screens (C-102)
- `6d81bc5e` ROM release v11.298.2: T-397 (one daemon always stays) and T-395's NEXUS residents -- eight new daemons, INDEX 387-394, MISSINGNO 395

## The design bible's own entry for v11.299

### v11.299 — 2026-10-10

### THE NEXUS (2026-10-09/10)

- ***3.4, new (the user, T-395)***: **THE NEXUS, between the groves**, *from THE PAINTED MIRROR.* **The singing fir stands in every grove, flat and washed out until the band's sheet gives it its key; then every fir is a door into a place made entirely of paint** -- *its trees doors to the groves already found (a grove not yet found is a grey tree that grows less real the harder it is tried), one Christmas tree home to the pier, the GUARDIAN a voice at every door, THE (NOT A) HUNTER a bear in red plaid, eight residents of its own (INDEX 387-394, MISSINGNO moved to 395), PENGUIN in the meadow and PHOENIX once.*
- ***9.4, an exception (the user)***: **the NEXUS residents are drawn in full natural colour, as paint, with their type's colour emphasised** -- *the one place a daemon is not coloured by its type, and meant to read as one.*

---

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
