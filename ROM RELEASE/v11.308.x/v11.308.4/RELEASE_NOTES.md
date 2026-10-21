# DAEMONS v11.308.4 — release notes

*Released 2026-10-21 17:50 · built against the design bible v11.308*

- **Engine**: CodeMusic/pokefirered-daemons `9aee93607` (context-content)
- **Design**: CodeMusic/DAEMONS `306a0e11`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `4e3e3708c732d372000edea2f4a576015d964a2a` |
| `daemonsContext.gba` | CONTEXT | `9e84d8dec3fa04b73c19358a93645714b9d17594` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `038b98198b4734872f34bd914938aac7a4abac95` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `61086bcb7bf5a4995d8f0ec9de34d37a45805656` |

## The engine since v11.308.3

- `9aee93607` T-431 P2 + P4: the SUMMARY's fourth page -- feelings drawn, never named; vocab: two DAEMON CENTER leftovers -> CHECKPOINT

## The design and tools since v11.308.3

- `306a0e11` T-431 P2+P4 built (engine 9aee93607): the SUMMARY's fourth page and its sixteen lines
- `2cc142e4` ROM release v11.308.3: feelings in the game, phase 1 -- GLAD, MAD, SAD and CALM kept in each daemon, moved by play and fading over hours; DEBUG -> GAME EVENTS -> FEELINGS (T-431 P1)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
