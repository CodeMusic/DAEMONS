# DAEMONS v11.319.1 — release notes

*Released 2026-10-28 21:00 · built against the design bible v11.319*

- **Engine**: CodeMusic/pokefirered-daemons `95686bb16` (context-content)
- **Design**: CodeMusic/DAEMONS `13ca42c2`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `2522d6cd2622eae520c3fba80dfcba0fc4cb35b3` |
| `daemonsContext.gba` | CONTEXT | `24a357aede3c023969bdca8cf1883a2908e4b79a` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `79a23865698e9cb7c5bd063d62ec793c5e774e2a` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `93b026ff2c8e7a832cb629bd3a0e645304647dfb` |

## The engine since v11.316.9

- `95686bb16` T-471: a FEEBAS's BEAUTY survives the feelings taking its byte
- `b902d185e` T-470: every INDEX sort is bounded by its own table
- `e503672e4` T-469: the GLOBAL diploma counts what the cart gives (the user, 2026-10-28: "the cart alone earns it")

## The design and tools since v11.316.9

- `13ca42c2` TODO: T-469 -- the user: the one-shot legends stay out of the diploma
- `560fd0da` Bible v11.319: ITS DREAMS' sixteen titles approved, the hum a motif (T-462)
- `3b1da29d` TODO: T-477 A-Z by our names; T-478 the \l line breaks (found by the review fixes)
- `4d182b50` T-472: tool guards -- gbashoes refuses over the GREBE; check_palettes measures a .pal against its picture
- `56503ac3` TODO: T-471 -- a FEEBAS's BEAUTY survives the feelings (engine 95686bb16)
- `3141b995` TODO: T-470 -- every INDEX sort bounded by its own table (engine b902d185e)
- `1f784bed` TODO: T-469 -- the GLOBAL diploma counts what the cart gives (engine e503672e4)
- `3d82488f` Bible v11.318: 3.8 ITS DREAMS, the carried daemon's dreams (T-462, C-200)
- `68456547` Bible v11.317: the two books asked -- the GUIDE reasons, THE SUBTLE LAYER notices (4.36, 4.38; C-209, C-229, C-230)
- `5f988492` qa: PROTEUS and OVERLOADED forms (v11.316.9)
- `7d264bd2` manual: rebuilt for v11.316.9
- `c95225f7` ROM release v11.316.9: T-452 PROTEUS's three forms and OVERLOADED's weathers; T-475 OVERLOADED's streaks and battle rows

## The design bible's own entry for v11.319

### v11.319 — 2026-10-28

### ITS DREAMS' titles approved (T-462)

- ***3.8 (the user, by multiple choice)***: **all sixteen titles approved as drafted, and the hum kept as a motif** -- *three titles hum, as a suspended process might hear one.* **The DRAFT marks come off once the user has seen them on the device.**

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
