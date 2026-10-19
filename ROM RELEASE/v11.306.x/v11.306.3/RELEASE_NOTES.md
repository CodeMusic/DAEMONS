# DAEMONS v11.306.3 — release notes

*Released 2026-10-19 01:31 · built against the design bible v11.306*

- **Engine**: CodeMusic/pokefirered-daemons `a292635ec` (context-content)
- **Design**: CodeMusic/DAEMONS `a08a3281`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `67755a21ff567c8e99c60ac47a4746e5aa413922` |
| `daemonsContext.gba` | CONTEXT | `eef85e70a585e07cb552f617e57a9c69ca703421` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `b337c003e1d21581cbc7a03c569c59113b953605` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `3bcdb3bf44af6e0bc742654b5bd6754da587c71e` |

## The engine since v11.306.2

- `a292635ec` T-427: what the house keeps goes to CORPUS -- the take in the save, the ledger, the plants, VERDIGRIS after the fall (DRAFT)

## The design and tools since v11.306.2

- `a08a3281` T-427 built (engine a292635ec, DRAFT): the house's take in profile_layout (sb2.house_take, 4 bytes, signed, plain); check_reach knows SCORN's plants sit behind the guarded door; gbabudget
- `ea098677` Wiki: THE SUBTLE LAYER's cover title set a little lower, off the border (the user, 2026-10-19), as the app and the Tab5 now set it
- `a5aea93c` qa: the wiki GUIDE cover with its author set lower
- `1a68c85c` Wiki: the GUIDE cover's author set lower, clear of the art (the user, 2026-10-19), as the app and the Tab5 now set it
- `f4df8d58` Wiki: the Books page's covers lettered (the user, 2026-10-19) -- wiki/covers.py draws each title over the companion's unlettered art in a common typeface, placed as the app places it, the book at 3x; wiki/images/ holds the two pictures
- `cc112c3a` qa: C-159 a board's sound off, shown on the site as its own (a test server, a copy of the save)
- `05618e1f` ROM release v11.306.2: the code-health pass (T-421), PAIRING DAY's heart above its target, DYNAMICPUNCH's words fitted (T-392)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
