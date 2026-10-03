# DAEMONS v11.291.9 — release notes

*Released 2026-10-03 08:37 · built against the design bible v11.291*

- **Engine**: CodeMusic/pokefirered-daemons `0ca4b7fd1` (context-content)
- **Design**: CodeMusic/DAEMONS `b2a23996`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `5df55d31488ce0ec9e2e552ed5df10ab9f115f0d` |
| `daemonsContext.gba` | CONTEXT | `e435046596f56e0c6a1de0c2ad1c61a14802458f` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `78676809fb16a028671d054f5f3c4b988abef118` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `88c37f644deee6dfa165d15eac50390f33770d37` |

## The engine since v11.291.8

- `0ca4b7fd1` T-265: the weekday comes from the date, not the clock chip's weekday register

## The design and tools since v11.291.8

- `b2a23996` T-210: the 13 legendaries' myth names approved; finished as a goal loop (the user)
- `829bc7d6` T-265: the clock reads on the user's EZ-Flash once its clock setting is on; the weekday now from the date
- `08d5ea3c` ROM release v11.291.8: the six routines batch 6 brought in (T-210)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
