# DAEMONS v11.335.6 — release notes

*Released 2026-11-01 12:36 · built against the design bible v11.335*

- **Engine**: CodeMusic/pokefirered-daemons `05202584f` (context-content)
- **Design**: CodeMusic/DAEMONS `6ea8f0f7`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `d62efc05126cda9989d6c5db21ba50c3cdf9ff02` |
| `daemonsContext.gba` | CONTEXT | `114d6fd1bd99cb993003b384ad32eb75946e906a` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `01b4a329f983cd09c1a39dc3e7d0cdd79e56bc92` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `93103ed06c0eacb41683fd40cfa3d49c4b32a9a2` |

## The engine since v11.335.5

- `05202584f` T-483 (5): THE WITCHING HOUR (13) in the SPELLBOOK, the last spell

## The design and tools since v11.335.5

- `6ea8f0f7` qa: C-267 the DAEMONS app icon, three rounds (the user picked H)
- `52f5ed10` TODO: T-483 (5) THE WITCHING HOUR, the last spell (engine 05202584f)
- `42c07b50` T-483 (5): theatre route t483_witching (4/4) -- spell 13, WITCHING (engine 05202584f, unpushed)
- `18bd9bd7` C-267: round 3 DRAFT app icons -- DAEMONS in the logo's letters with the crossing notes as its M, behind MUSAI (H) and the current icon's dog (I), and the word alone (J)
- `e6e30ecb` C-267: round 2 DRAFT app icons -- MUSAI, the current icon's dog and CODEMUSAI under red and blue notes crossing in purple, on A's field with the title's notes rising
- `c3d091a3` C-267: four DRAFT app icon options for the DAEMONS iOS app, and a contact sheet
- `a14d848e` ROM release v11.335.5: T-483 (5) THE PROCESS and THE SEAM in the SPELLBOOK, unlocked by MIRROR on a type and what it fears

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
