# DAEMONS v11.341.2 — release notes

*Released 2026-11-06 08:28 · built against the design bible v11.341*

- **Engine**: CodeMusic/pokefirered-daemons `4c0a300f8` (context-content)
- **Design**: CodeMusic/DAEMONS `e74591c5`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `0c7d78ca7bda9f867d323ec88c5fe9689c44a7a8` |
| `daemonsContext.gba` | CONTEXT | `e952359386d34c7e75e22c0c14d0d06572b95254` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `f4d3a0eab4da401f17dce36770ec2fa30a73eebd` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `5f0775fa6da933775ed3f76e4ac7115021b9c99b` |

## The engine since v11.341.1

- `4c0a300f8` T-519: the third book's pictures, batches 2 and 3 -- 76 more entries get their own picture: THE HERMETIC LAYER 24 (29 of 52 entries now drawn), THE EUDAIMON LAYER 24 (29 of 52) and THE UNITY BOOK 28 (33 of 55); the rest still show their book's frontispiece. EVERY FOLD, the dawn half's UPPER FOLDS and LET GO are redrawn before going in: small hands that read as hands, the opening hand as one hand, a palm-down hand letting go. Each picture is 96x88 in its book's own sixteen roles. ROM +315 KB (76 frames of 4224 bytes and their table rows). No RAM or save cost. Written by DAEMONS tools/gensubtle.py. DRAFT
- `20e9f8d42` T-519: SPIRITS' tone on the follower and the party icons -- a daemon in good spirits walks and sits in the party menu lighter (10/32 of the way to white over its own colours), one in low spirits darker (10/32 to black), never a change of hue. The follower's palette is toned after friendship's saturation and before the field's light, the weather and the hours (the creator's gold, the witching shimmer), which all reload it, so they go on over the tone; a crossing re-tones it within eight frames. A party icon shares its colour group's palette, so as AWAY's wash does, a toned one is pointed at a toned copy (one per group and tone, tags 56032+); AWAY's wash wins, and with no palette slot free the icon keeps its colour. The PC's box icons are left as they are: its sixteen OBJ palettes are spoken for. IWRAM +1 byte (sFollower), EWRAM 0, ROM +160 bytes of code. No save cost. DRAFT

## The design and tools since v11.341.1

- `e74591c5` TODO: T-519 the books' pictures, batches 2 and 3, in the game and the companion; SPIRITS on the follower (engine 20e9f8d42, 4c0a300f8)
- `1d64000a` T-519: the third book's pictures, batches 2 and 3, in tools/thirdbook_art.py's PICTURES (engine 4c0a300f8, not pushed)
- `fae53b89` qa: T-519 SPIRITS' tone on the follower and the party icons, filmed (engine 20e9f8d42, not pushed) -- as it is, lighter in good spirits, darker in low, the creator's hour's gold over the low tone, and the party menu with one in each state; route tools/routes/t519_spirits_tone2.json
- `6f2bd70b` T-519/C-299: the dawn half and THE UNITY BOOK recorded and sealed, each by its own book's key (the user, 2026-11-05)
- `a4f6f407` T-519: THE UNFOLDING's SPACE gets its own picture key, space (it shared room with THE WHEEL's ROOM; the game lane)
- `02a179d9` T-519: the dawn half and THE UNITY BOOK sealed in docs/books like the vault (the user, 2026-11-05)
- `71f03599` ai/n8n: daemon/talk is told how the daemon speaks of itself, after its INDEX entry (companion C-303, T-522; not pushed to n8n)
- `eaf16c90` ROM release v11.341.1: T-519 the third book's art -- the chosen covers, frontispieces, opening pictures and icons (DRAFT); v11.340.x sealed

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
