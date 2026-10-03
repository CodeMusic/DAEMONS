# DAEMONS v11.292.1 — release notes

*Released 2026-10-03 09:22 · built against the design bible v11.292*

- **Engine**: CodeMusic/pokefirered-daemons `6d31db3ce` (context-content)
- **Design**: CodeMusic/DAEMONS `53ca9ef8`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `20c920f4425caff480883554929f2a25ec7254b3` |
| `daemonsContext.gba` | CONTEXT | `f1e5b846f23552d8b12231c8871bdc0ee42a2af4` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `3f2803d9ff239988356889567e3fd410add09cec` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `a514627198fe375124a9e5110ed559ecab27b61f` |

## The engine since v11.291.10

- `6d31db3ce` T-348: the first shop clerk spoken to while holding OPUS notices it (the user; DRAFT)

## The design and tools since v11.291.10

- `53ca9ef8` T-348: a shop clerk notices OPUS -- reversed by the user; bible v11.292 (engine 6d31db3ce)
- `d9ff4066` ROM release v11.291.9: the weekday from the date, not the clock chip's register (T-265)

## The design bible's own entry for v11.292

### v11.292 — 2026-10-03

### A shop clerk notices OPUS (2026-10-03)

- ***Reversed by the user (T-348)***: *"Nobody remarks on it, then or ever" no longer holds. The first shop clerk spoken to while the player holds OPUS notices it, says it writes a line under some INDEX entries and that SELECT turns the page, and hopes they enjoy it -- once, at whichever shop comes first. Who left it is still never answered. Built and released the same day.*
- *Since v11.291, all released: T-210's six batches (95 daemons named by type, written and drawn), the routines they brought in, EPIPHANY's line redrawn as a real animal, the 13 legendaries' myth names approved; T-265's weekday read from the date.*

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
