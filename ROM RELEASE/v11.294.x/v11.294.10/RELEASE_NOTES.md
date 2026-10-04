# DAEMONS v11.294.10 — release notes

*Released 2026-10-03 23:30 · built against the design bible v11.294*

- **Engine**: CodeMusic/pokefirered-daemons `cc47d4f05` (context-content)
- **Design**: CodeMusic/DAEMONS `28e68a1a`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `34288879d3a4b83567705e4cc5349c1d78854999` |
| `daemonsContext.gba` | CONTEXT | `980fa126f9fd8707e75dd432a7facf3953394bca` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `2b2cf40aa009ddcbb968420c9482b49d26ffed7a` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `e40952e76a05f724f62e74d4eef2068fdabcd235` |

## The engine since v11.294.9

- `cc47d4f05` T-364: the OWL's note approved by the user
- `a0fdaac85` T-365: the OWL keeps his own colours in CALLOW SCHOOL, and CALLOW's people theirs

## The design and tools since v11.294.9

- `28e68a1a` T-365 closed (engine a0fdaac85): the OWL's colours; check_reach fails on two tags in one palette slot (trap 17); T-364's note approved (engine cc47d4f05)
- `f4e8d9e3` ROM release v11.294.9: the OWL stays until BRAZEN (T-364)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
