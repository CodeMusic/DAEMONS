# DAEMONS v11.301.11 — release notes

*Released 2026-10-17 00:08 · built against the design bible v11.301*

- **Engine**: CodeMusic/pokefirered-daemons `24706d670` (context-content)
- **Design**: CodeMusic/DAEMONS `c8935164`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `b8e717f791693ba3bb9f00aa9ac834779e286e6c` |
| `daemonsContext.gba` | CONTEXT | `42003a6226a7303e5d97e240675a7e891969f185` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `0ac23588ea7c60805ee45e14e3fd0ca6e343ef1e` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `70fd47e9dbbcd7bdc46727ad445829ec05ca18ee` |

## The engine since v11.301.10

- `24706d670` T-405 (approved by the user 2026-10-16): the understandings' STREAM lectures -- STILL, NAMING, NOTICE, REFLECT, STANCE, MEND, PRACTICE -- each offered once its understanding is held, never announced (T-252)
- `3f9c10a6a` T-252 (the user, 2026-10-16): the understandings are STILL, NAMING, NOTICE, REFLECT, STANCE, MEND, PRACTICE -- the debug UNDERSTANDINGS page carries them with their places

## The design and tools since v11.301.10

- `c8935164` companion_export.py (companion 1a27330): the GUIDE's link
- `6fbd2e07` qa: the companion's LIBRARY and the GUIDE (C-145), and a ROOT's lesson (T-405)
- `6826be61` qa: C-121 -- the StickS3 on the bench, fitted
- `30e92b2b` T-405 (engine 24706d670, companion e337d87): the understandings' lectures placed and exported
- `2222c6e7` companion_export.py (companion 69cb88c): guide.json and the cover, name painted out
- `6e984110` qa: NATIVE on the companion's INDEX (companion C-143)
- `6576e806` T-252 (engine 3f9c10a6a, companion 1e8cd0f): the understandings named
- `4a982009` ROM release v11.301.10: season and hour homes on the early roads (T-407), NATIVE on the INDEX (T-407), SCORN's gym echoes him (T-413)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
