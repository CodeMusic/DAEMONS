# DAEMONS v11.290.5 — release notes

*Released 2026-10-01 18:46 · built against the design bible v11.290*

- **Engine**: CodeMusic/pokefirered-daemons `f5ef4d327` (context-content)
- **Design**: CodeMusic/DAEMONS `e38d39eb`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `8b8e56bc04c46a1c48214ee9712a309bdcae03c9` |
| `daemonsContext.gba` | CONTEXT | `e41aff29a55229e8d6b36adead3439331951eb5d` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `f6f4cd9101e5ff6585c270a02a9fbea742e2d553` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `5f35e39bcdf1bea5723dac5826f610a25c63f05f` |

## The engine since v11.290.4

- `f5ef4d327` T-342, T-343: the GUIDE's shelf sparkles before REVEAL until taken; a sparkle seen without REVEAL is quieter, one beat in three
- `4403d6cb5` T-340, T-341: the READING ROOM attendant wishes she could read the GUIDE, hidden on an island -- and thanks you once you hold it (DRAFT)
- `5e00458c9` T-338, T-339: CRYSTAL says the INDEX can be more (one thing she is still working on, one at THE REPO, not for sale); the rival in the lab is eager to set out -- the mainland's machines, the islands' minds (DRAFT)

## The design and tools since v11.290.4

- `e38d39eb` TODO: T-338..T-343 closed with their engine commits
- `7c35d142` TODO: T-338..T-343 -- CRYSTAL hints at OPUS, TY eager in the lab, someone wishes for the GUIDE and thanks you, the GUIDE sparkles before REVEAL, quieter sparkles before REVEAL (the user)
- `73dbe093` ROM release v11.290.4: all fourteen grove doors carry the tell (T-337)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
