# DAEMONS v11.325.1 — release notes

*Released 2026-10-29 11:32 · built against the design bible v11.325*

- **Engine**: CodeMusic/pokefirered-daemons `a02068ab2` (context-content)
- **Design**: CodeMusic/DAEMONS `811f645c`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `e20618404b8ca042b66323b199bedcc1a66a05a3` |
| `daemonsContext.gba` | CONTEXT | `57e300c14fa0fde9fd942c2354ae815edc3c3f87` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `2eeccf8b3fa1b0947bcbb58df738bc5662a2227a` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `f53f3599b6edb714ea6ab7f517085df4063c2164` |

## The engine since v11.322.1

- `a02068ab2` README: a rumour of a third book (THE HERMETIC LAYER, on the DAEMONS wiki); PENPHIN's pair trade built; latest release v11.322.1
- `a81146f2d` T-483: the costume may be any daemon but the empty slots (264-276), as the companion's costumeOf -- CLUSTER and ARTSAI matched its test vectors only after
- `e9367b88d` T-486: THE HERMETIC LAYER glitches once, on the first page turned past OSRIC HATTER's warning
- `a49361d95` T-483: the book's pages brought up to docs/hermetic-layer.md (OSRIC HATTER's warning, THE LAYERS: 52 entries)
- `73f19dc82` T-483: the handless clock, and Halloween's costume (DRAFT)
- `097001b9a` T-482: the battle's ground breathes red to blue through purple; T-480's shimmer on the same breath
- `6ad9085d1` T-483: THE HERMETIC LAYER, the book, its unlock and the world's pulse (DRAFT)

## The design and tools since v11.322.1

- `811f645c` README and wiki: a rumour of a third book -- THE HERMETIC LAYER, its page under Books (what is said of it, and the real history: the Hermetica, the Emerald Tablet, alchemy, the hatters, grimoires, the witching hour), never where or how; PENPHIN's pair trade built (T-474); v11.322.1
- `7f1a6bf2` qa: T-484's two sheets (left out of 15137c99)
- `9de9e132` T-483 / T-482 / T-486: the theatre route (5/5) and its sheets (qa 29Oct2026 T483 32-34, 36; T482 35) -- engine e9367b88d
- `8e25b9eb` gensubtle: THE HERMETIC LAYER through the same parser (--book hermetic; both by default) -- T-483, engine e9367b88d
- `474873f2` TODO: T-486 wording
- `f1725946` Bible v11.325: the only glitch is THE HERMETIC LAYER's (T-486); LAB NOTES 4 stays struck
- `5168d1b2` Bible v11.324: the backgrounds keep the calendar, the map is a score (3.10); the hour in battle; the hatter's house
- `89b95cbd` TODO: T-485 OSRIC HATTER's house on QUICKSILVER (the user)
- `721cb29b` Bible v11.323: OSRIC HATTER of QUICKSILVER, and THE LAYERS (4.39)
- `15137c99` TODO: T-484 struck -- released v11.322.1; qa sheets
- `88f16ae5` C-238: THE HERMETIC LAYER revised on the user's answers -- THE LAYERS, the warning's madness, OSRIC HATTER of QUICKSILVER
- `eed7c42f` manual: rebuilt for v11.322.1
- `881a9a2e` ROM release v11.322.1: T-449 the map's icons and cursor in ink; T-484 batch G's findings (the plateau's specks, a special NPC's reflection); v11.320.x sealed

## The design bible's own entry for v11.325

### v11.325 — 2026-10-29

### Two open questions closed

- ***A GLITCH (Open since 2026-09-24), the user by multiple choice***: **only in THE HERMETIC LAYER** -- a few frames when the book first opens past OSRIC HATTER's warning, and once at 3:30 in his house; nowhere else, DOLDRUM CAVE as built (4.39, T-486).
- ***LAB NOTES 4 (Open since 2026-09-23)***: **the page stays as built, its lines struck through.**

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
