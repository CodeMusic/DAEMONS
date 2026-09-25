# DAEMONS v11.287.5 — release notes

*Released 2026-09-25 15:49 · built against the design bible v11.287*

- **Engine**: CodeMusic/pokefirered-daemons `591eefd06` (context-content)
- **Design**: CodeMusic/DAEMONS `b921528c`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `13636d5950d364bc5f8aabf60db63b988836c7a1` |
| `daemonsContext.gba` | CONTEXT | `7761e585a66dc85ff12fefb581d6e20d71cba085` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `7be1ea4197309bd84a97e771b1bba076334d9a8d` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `d550dd8dd8290f7889474914dfd51545190eb5a6` |

## The engine since v11.287.4

- `591eefd06` T-282: the brain is drawn only on your own card -- a Cable Club partner's card lit with YOUR understanding
- `d81f3c856` T-281: the night tables carry the day's water and rods -- surfing and fishing on Routes 10 and 12 found nothing at night

## The design and tools since v11.287.4

- `b921528c` gbanight: the night tables copy the day's water, rods and rocks (T-281)
- `8ba4061a` T-281, T-282 closed (night water, the brain on your own card only); T-283 asks about DANGLING on Route 1 at night
- `f621ce08` gbabudget: the ROM has 6.8 MB free, not 1.3 -- the pinned graphics block's gap was counted as used; T-18 corrected
- `ced46edc` engine.md: the third day of driving the theatre (the doormat's centre, release addresses, a sound read from memory, a battler's species)
- `cf516bb8` T-274 heard in effect (the sound driver held SE_TOY_A on a Friday); CHANGELOG v11.287 carries the day's fixes
- `7046ccf0` ROM release: L refuses an entry the INDEX cannot open yet

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
