# DAEMONS v11.345.1 — release notes

*Released 2026-11-08 22:28 · built against the design bible v11.345*

- **Engine**: CodeMusic/pokefirered-daemons `1d68b678b` (context-content)
- **Design**: CodeMusic/DAEMONS `e5952f9d`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `a45d15ebeb380705c75d938bb31cc9971b2ba611` |
| `daemonsContext.gba` | CONTEXT | `d1ad4674f56eb74c844b099f3db5d531dc319cf1` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `8c86dc0812a8653a32b05eccbfdafc7081935542` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `f4bc37865b27e4cbef125c7b6c83008be2923476` |

## The engine since v11.344.1

- `1d68b678b` T-532 redraw: the eight weak MUSAI seasonal forms redrawn and approved
- `3ce5d9790` T-532 final art: the MUSAI branch's seasonal forms as the user approved them, four new summers, and each form's own coordinates
- `ea59a4cce` T-532: the MUSAI branch keeps the seasons (placeholder art), and CODEMUSAI's CRYPTOPHASIA

## The design and tools since v11.344.1

- `e5952f9d` genanims: a move borrowing another family's script (T-532 CRYPTOPHASIA plays HYPER VOICE's) is the lender's to draw, so the LOGIC table no longer asks for it -- and a write cannot rewrite HYPER VOICE
- `0fb28750` T-532 redraw built (engine 1d68b678b): the eight weak seasonal forms, "Put all 8 in"; qa T532 36-38
- `27586724` qa C308 18: the dream journal's three lenses (sample dreams, DRAFT)
- `cfc8a274` T-532 final art built (engine 3ce5d9790): the approved seasonal forms, four new summers, each form's own coords; qa T532 29-35
- `10d0eb4c` T-532 final art: the MUSAI branch's seasonal forms by arm C, vehicles pushed (18 forms + 5 summer redraws, front/back/icon/follower); sheets qa T532 21-28
- `aa44a0f9` T-532 plumbing built (engine ea59a4cce): the MUSAI branch's seasonal forms, CRYPTOPHASIA; vision v11.345 (9.34)
- `4ddfff06` ROM release v11.344.1: T-530 menus pass 2 -- the TOOLKIT's cards in type colours, the MART and PLUGIN shop, the INDEX's icons and SCORE area map, the TRAP TABLE's pocket, the hold marks, the PC's box menu and DATA panel; seals v11.343.x

## The design bible's own entry for v11.345

### v11.345 — 2026-11-08

- **9.34, the MUSAI branch keeps the seasons (T-532, the user, by multiple choice).** Each of the six MUSAI has four seasonal forms and wears the one `DaemonsSeason()` gives it -- CONTENT on the northern year, CONTEXT on the southern -- in battle, the party, the PC, the follower, the summary and the INDEX: a display swap, Unown's way (18 picture-only ids; summer is today's art), look only, silent, a battle keeping the season it began in. MASKMUSAI's home season is winter, LENSMUSAI's spring, CAREMUSAI's summer, SEEKMUSAI's autumn; the machines are part of each body, never ridden. 24 INDEX entries, one per form, both editions sharing them. **CRYPTOPHASIA**, CODEMUSAI's own at 30: a LOGIC special hit, 40 and +20 for each other MUSAI in the party still able to fight (to 140). The plumbing is built with placeholder art (copies of today's); the drawings follow. DRAFT words.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
