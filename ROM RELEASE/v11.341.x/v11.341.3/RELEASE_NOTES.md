# DAEMONS v11.341.3 — release notes

*Released 2026-11-06 10:46 · built against the design bible v11.341*

- **Engine**: CodeMusic/pokefirered-daemons `ca744f3d6` (context-content)
- **Design**: CodeMusic/DAEMONS `d0a51f44`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `4c282b7f7af8078ab9380b5f5d6590df9e8de5f3` |
| `daemonsContext.gba` | CONTEXT | `d52eed6a7e87b95c4acfe22e7850453345a6ce5f` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `efa90b7592342fdbaf348786f94fdd938b5a3969` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `7e94ca186a22999aa39ba8779e21d37981c795f3` |

## The engine since v11.341.2

- `ca744f3d6` T-519: the third book's pictures, batch 4 -- the last 68 entries get their own picture: THE HERMETIC LAYER 23 (52 of 52 entries now drawn), THE EUDAIMON LAYER 23 (52 of 52) and THE UNITY BOOK 22 (55 of 55); no entry shows the frontispiece in its place any more. Nineteen were redrawn before going in: OLD WORK, OLD WORDS and PHILOSOPHY as four large objects on two shelves; ROOM's arch upright and stepped aside, the mended one with an animal bowing; CONTRAST (dawn and mended) as a clock face at rest and two halves sewn together; WHAT IT DOES as a cupped hand; KINSHIP's small hands; the mended VOWS tied in a bow; THE VERB's hand reaching down; SEAM's scissors; BOTH WAYS' rain cloud; the dawn LAST WORD's dusk sky; CREATOR's sleeping lark; FIELD's passing daemons in all three; the mended SMALL HAND on the gate. Each picture is 96x88 in its book's own sixteen roles. ROM +288,320 bytes (68 frames of 4224 bytes and their table rows), the same in all four builds. No RAM or save cost. Written by DAEMONS tools/gensubtle.py. DRAFT

## The design and tools since v11.341.2

- `d0a51f44` TODO: T-519 every picture in the third book drawn (engine ca744f3d6)
- `dc2bb1f9` T-519: the third book's pictures, batch 4, in tools/thirdbook_art.py's PICTURES (engine ca744f3d6, not pushed) -- the last 68 entries (23 night, 23 dawn, 22 mended), nineteen of them redrawn first, so every entry of all three books has its own picture; gensubtle reports how many still show the frontispiece (none)
- `4a2dd7b0` ROM release v11.341.2: SPIRITS on the follower and party icons, and 76 more of the third book's pictures (T-519, DRAFT)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
