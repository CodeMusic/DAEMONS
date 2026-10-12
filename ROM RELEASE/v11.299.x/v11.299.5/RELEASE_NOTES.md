# DAEMONS v11.299.5 — release notes

*Released 2026-10-12 14:41 · built against the design bible v11.299*

- **Engine**: CodeMusic/pokefirered-daemons `54a73b231` (context-content)
- **Design**: CodeMusic/DAEMONS `57d35585`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `127d2707999fabe4a175347e2b49ca68fbb5daca` |
| `daemonsContext.gba` | CONTEXT | `aa2d1d12a6e73775a001c39d7f0752af3ae1528d` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `bdd0430da6fc63db51774ad8d55e1cb05f91b820` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `15a751e263af48c1d9a3cae3452162448167f36c` |

## The engine since v11.299.4

- `54a73b231` T-120: MAGMA's five in MAGMA red (the user, 2026-10-12: "fix the magma red") -- tools/t120hoenn.py magmared
- `ca2ae4580` T-120 Group 3: Hoenn's named people and both teams, and BRENDAN and MAY as the grey monkey (tools/gbachar.py h_*)
- `7395922e1` T-120: the old couple's wife redrawn in a plain shawl and dress (the user, 2026-10-12)
- `25a76852f` T-120 Group 2: the 25 Hoenn classes with no FireRed twin, and the cygnet Group 1 missed (tools/gbachar.py h_*)
- `bb8874af8` T-120: the young couple recut whole -- her pale head no longer keys out with the backdrop
- `4c1c7aee3` T-120 Group 1: the 29 Hoenn copies of FireRed classes redrawn from our FireRed portraits (tools/gbachar.py h_*)

## The design and tools since v11.299.4

- `57d35585` qa: C-119 -- 44 daemons with checked eyes (awake, asleep, glad), and six of them in every expression
- `095d8bbe` T-120: MAGMA's five recoloured MAGMA red (engine 54a73b231); six hammerhead drafts for the AQUA admin kept as drafts -- the model draws a hammer, never the head
- `64b32bba` T-120 struck (engine ca2ae4580): Group 3 -- Hoenn's named people, AQUA as sharks, MAGMA as moles, BRENDAN and MAY as the grey monkey; every portrait, back pic and overworld person ours
- `9ed0c300` qa: C-118 and C-119 -- the expressions mock-up, the reference sheet, and the Fire in four states
- `46051949` T-120: the old couple's wife in a plain shawl and dress (engine 7395922e1); Group 3 drafting added to tools/t120hoenn.py
- `9c9233ea` qa: the phone hosting on its own (C-111)
- `d8fd02fe` T-120 Group 2 done (engine 25a76852f): 25 Hoenn classes with no FireRed twin and the missed cygnet, seed 13002, three redrawn
- `5b113068` T-120: the young couple's source keyed flat so her head survives the cut (engine bb8874af8); Group 2 drafting added to tools/t120hoenn.py
- `17e80596` T-400 published: the DAEMONS wiki is live (wiki/publish.sh)
- `7ded7d59` T-120 Group 1 done (engine 4c1c7aee3): the 29 Hoenn copies redrawn from our FireRed portraits, seed 13001, the beauty in red -- tools/t120hoenn.py, gbachar.py h_*
- `fa6cf6c0` T-400: the DAEMONS wiki, written in wiki/ (Home, Playing, Editions, The companion, Building, Releases, Contributing) -- public writing, checked for the four; wiki/publish.sh publishes once the Wiki tab has its first page
- `18e2c64f` T-224 finished (the user): twenty-two of twenty-four NOTEBOOK documents in the game, all approved; LOOSE PAGES 6 and PROSPECTUS 4 left undrafted on purpose
- `99c5a9f8` ROM release v11.299.4: the quest's two halves shown -- ROOTS on the card, the borrowed daemon, artificial flowers, the fact collector (T-379..T-382)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
