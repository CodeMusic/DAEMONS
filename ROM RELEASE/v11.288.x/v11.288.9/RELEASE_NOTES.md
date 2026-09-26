# DAEMONS v11.288.9 — release notes

*Released 2026-09-26 11:22 · built against the design bible v11.288*

- **Engine**: CodeMusic/pokefirered-daemons `4d9962bce` (context-content)
- **Design**: CodeMusic/DAEMONS `fad14426`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `a142e0675e2d48649ece0f6396b68e82da5125d5` |
| `daemonsContext.gba` | CONTEXT | `ba1e07202e54bd38d4fd68fb4cbe219cd1653bf3` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `628184d3f2fc84a3f47d375f3e7054fa87af2426` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `16bab104f2cf0e8acf3771968b945566e023cebe` |

## The engine since v11.288.8

- `4d9962bce` The Guide out in the world: DOLDRUM's dream sign (T-309), five case studies as islanders (T-310), the Board's torn copy (T-311); Ty's Act 2 voice (T-316) -- DRAFT lines, all played
- `f31398b29` The family (T-313) and DAEMON Designers (T-314): two credits pages; MOM's ship, DAD's initials, DAVID's note (DRAFT)
- `aa31082e5` T-299, T-312, T-258: AL comes in by the door; the REPO's door is clear and OPUS has its golden ticket; HALFTONE ORPHAN HOUSE

## The design and tools since v11.288.8

- `fad14426` T-309, T-310, T-311 closed; T-316 drafted
- `01e631e3` T-313, T-314 built (DRAFT lines, played); changelog for T-299, T-312
- `fa58b0cb` T-299, T-312, T-258 closed; tools/gbarepoopus.py
- `1f7f3d51` The user's thirty answers, logged (2026-09-26): T-299, T-312 to T-319 opened; T-05, T-10, T-18, T-50, T-120, T-210, T-221, T-234, T-235, T-252, T-256, T-258, T-269, T-271, T-297, T-298, T-301, T-309, T-310, T-311 answered
- `bbd3103c` ROM release v11.288.8: the credits, Ty, CRYSTAL's ratings, the Guide's shelf

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
