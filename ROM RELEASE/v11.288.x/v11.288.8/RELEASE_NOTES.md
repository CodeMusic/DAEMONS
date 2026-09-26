# DAEMONS v11.288.8 — release notes

*Released 2026-09-26 09:02 · built against the design bible v11.288*

- **Engine**: CodeMusic/pokefirered-daemons `0c6aa31d9` (context-content)
- **Design**: CodeMusic/DAEMONS `449a1ab9`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `bae9c4b26350beff5bf6131ad49526d5e9aa7a30` |
| `daemonsContext.gba` | CONTEXT | `7c1261c735d8587160896e322c104dbb3ec4fa0a` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `4f360da8cfa608af1b86970f081ecddee2d3827f` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `46ef276b171a487b5dc0a754dc6421fadfbe10ac` |

## The engine since v11.288.7

- `0c6aa31d9` The user's answers: credits (T-290), Ty (T-286, T-288), CRYSTAL's ratings (T-295), the Guide's shelf (T-297)

## The design and tools since v11.288.7

- `449a1ab9` Answers built: credits, Ty, CRYSTAL's ratings, FOLDS; T-297 (map hints) filed with its pilot, T-298 asked; port_vocab: an UPTIME, idioms across a line break
- `7ad1dd38` ROM release v11.288.7: CRYSTAL and AL in their own voices (drafts); USERBOXES

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
