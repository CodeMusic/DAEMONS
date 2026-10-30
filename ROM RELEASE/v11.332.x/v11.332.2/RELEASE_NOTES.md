# DAEMONS v11.332.2 — release notes

*Released 2026-10-30 18:37 · built against the design bible v11.332*

- **Engine**: CodeMusic/pokefirered-daemons `c93a5ce48` (context-content)
- **Design**: CodeMusic/DAEMONS `89a2d362`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `ac7180af1989ce766c35f7b3267ac876d52e7903` |
| `daemonsContext.gba` | CONTEXT | `b74ef94bf9832cd05125cf140af1ed030e95d835` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `84c88ed25a62fac4915bfa5f6adf1989922c70f8` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `ee91af9fe1ba7ab844d692ed66d544a0188773cb` |

## The engine since v11.332.1

- `c93a5ce48` T-490 step 2: TAMPER, the CORRUPT row, CONSENSUS, PRIOR and WEATHER BALL strike with SP. ATK
- `26feb9a92` T-490 step 2: the weather answers the hit's type, whichever side it strikes with (no change)
- `33d0d9431` README: latest release v11.332.1

## The design and tools since v11.332.1

- `89a2d362` qa: C-256 the TV setup in PLACES
- `bc24ee35` T-490 step 2: the theatre route for TAMPER's side and rain on FLOW (not yet run: the screen was locked)
- `9096ee1a` TODO: T-490 step 1 released v11.332.1; the user's answers for step 2
- `5b024800` TODO: T-496 the lioness, met four times before the ship
- `fb28c919` TODO: T-494 the lioness by the pool sends the letter (one person)
- `74d42c65` TODO: T-493..T-495 the pair of paintings, the letter that answers later, not hard just unfamiliar
- `9f4d906f` qa: T-490 step 1's two category marks (v11.332.1)
- `5304336b` README and wiki: v11.332.1
- `037b71c1` TODO: T-490 step 1 released v11.332.1
- `af6ff222` manual: rebuilt for v11.332.1
- `209b8bc8` ROM release v11.332.1: T-490 step 1 a routine's own category (PHYSICAL / SPECIAL / STATUS), defaulted so nothing moves; v11.331.x sealed
- `704f2aff` qa: the books as PDFs, and C-248's iPad text size before and after
- `ce4f7f92` docs/books: the three books as PDFs -- the GUIDE, THE SUBTLE LAYER, and a sealed vault

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
