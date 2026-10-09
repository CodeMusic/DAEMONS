# DAEMONS v11.298.1 — release notes

*Released 2026-10-09 11:56 · built against the design bible v11.298*

- **Engine**: CodeMusic/pokefirered-daemons `6bf720409` (context-content)
- **Design**: CodeMusic/DAEMONS `bf8c2bd8`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `f45b3700e96c4936c71727188de171b44eae947c` |
| `daemonsContext.gba` | CONTEXT | `a54f4c2177b62cd9395e65183fbed586ed1a9ad7` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `d72365c21b7e371403ee00a520d33720e80e8b39` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `e88fd1c3a603adf55643f42c5b459b7ba26d0a50` |

## The engine since v11.297.4

- `6bf720409` T-396 (the user, 2026-10-09): any number of daemons AWAY -- SEND no longer refuses a second one ("One at a time: X is with your device now." is gone, and DaemonsOtherOnDevice with it). The companion keeps one daemon to a device (its C-80). AnotherCanBattle now counts a daemon asked for as gone, since several can be asked for before a SYNC.

## The design and tools since v11.297.4

- `bf8c2bd8` T-396 done (engine 6bf720409): any number of daemons AWAY, one to a device -- bible v11.298, 9.25's "one daemon at a time" reversed (the user)
- `05c3b1a1` T-395: the NEXUS cast settled with the user -- REFLECTION, LODESTAR, PERIHELION, LYUBOV, MULTIMAL -> ILLUMINED, LYNX -> BASTET, with PHOENIX and PENGUIN; every resident drawn new, in paint (docs/nexus.md)
- `5d033acb` T-395 redesigned with the user: THE NEXUS, through the singing fir (docs/nexus.md) -- the fir in every grove, flat until the key; the NEXUS made of paint, its trees doors to the groves found (grey and smudging before), one Christmas tree home, the GUARDIAN a voice at each door, THE (NOT A) HUNTER a bear in red plaid, and a proposed cast from THE PAINTED MIRROR (MULTIMAL, PHOENIX, the wolves, the deer, LYNX, PENGUIN, the tiger, the lioness). gbagrove.py takes a parent's own map id and a grove with no residents; spriteforge and the AI docs name roverbyteseer plainly (the user: never .local). The C-80 picture filed yesterday.
- `beceeae3` ROM release v11.297.4: a debug game that starts with nothing, and GAME EVENTS (T-394)

## The design bible's own entry for v11.298

### v11.298 — 2026-10-09

### AWAY, any number (2026-10-09)

- ***9.25, reversed (the user, T-396)***: **SEND no longer refuses a second daemon.** *Any number may be AWAY, each in a device of its own; the companion keeps one daemon to one device, and choosing another device for a daemon moves it. SEND still refuses a daemon not in full health, and the last one here able to battle -- now counting one asked for as gone, since several can be asked for before a SYNC.* *"One at a time: X is with your device now." is gone from the game.*

---

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
