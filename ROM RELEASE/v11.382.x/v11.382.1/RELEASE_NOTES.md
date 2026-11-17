# DAEMONS v11.382.1 — release notes

*Released 2026-11-16 21:30 · built against the design bible v11.382*

- **Engine**: CodeMusic/pokefirered-daemons `04464cc40` (context-content)
- **Design**: CodeMusic/DAEMONS `c30d301d`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `633575322c0e4d0a98fb9e178c3a4bc83f1b389b` |
| `daemonsContext.gba` | CONTEXT | `63ba538deb40821f7a323a4fe9abefb7b7655586` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `63a0c3201e0e08540220315c0f66969433466fe7` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `40bec0d2a78395f6effaf9d4add9621547e5613a` |

## The engine since v11.381.1

- `04464cc40` T-572: the player's head draws over the GOTO map's rings (subpriority 1 and 2 swapped), so REASON and INSTINCT can be told apart at a town (the user's pick)
- `879e09e6e` README: the release line names v11.381.1

## The design and tools since v11.381.1

- `c30d301d` T-573: VERDIGRIS DEPT. STORE drafted as a landmark, A/B/C (gbalandmarks celadon_city group, nothing approved)
- `9135d5b8` T-572 BUILT: the head over the GOTO map's rings
- `a0d0b902` T-572: filmed the head over the GOTO ring (route t572_head_over_ring, qa 16Nov2026 T572 36-40); engine left uncommitted
- `e05ec36a` C-393: THE CARDPUTERS, a manual for the Cardputer, the ADV and the Zero (23 pages, DRAFT) -- tools/manual.py's eleventh book, read from the companion's HARDWARE.md, CARDPUTERZERO.md, firmware/pizero/README.md, cardputer.cpp and the Boards wiki: the keys (the Zero's game on F Z X C, L K, Q P), the Cardputer and the ADV (linking, the corner, the pages, care, a word to every daemon, routines), the Zero (installing, making the game from your own ROM, playing at 1:1, the one save, LINK, SYNC, another game's save, away, its companion screens, what is not yet), the caps (the LoRa-1262; the CC1101 + NFC, not yet, C-391), batteries and trouble; what is not yet seen on the Zero said so. Eleven of its screens from qa 16Nov2026, two drawings, a Cardputer with its cap on the cover (manual_devices). Its own voice, tinkerer (the user's pick, A of three samples), with this book's own respellings in bookaudio (ADV, CC1101, the keys ; , . / by name); its shelf cover; releasedocs routes the Zero's program, the keyboards and CARDPUTERZERO.md to it and takes it as a SET UP book. README and the wiki name THE WATCH, THE GLASSES and THE CARDPUTERS
- `6073f2d3` Bible v11.382: the ladders down a hole (T-574, v11.381.1)
- `c98a8b89` README and wiki Home name v11.381.1
- `57ce1f7d` ROM release v11.381.1: T-574 the ladders down a hole in four caves as rungs and rails, NAVEL ROCK's fall hole a broken lip; seals v11.380.x

## The design bible's own entry for v11.382

### v11.382 — 2026-11-16

- Recorded from release v11.381.1 (57ce1f7d, engine 90d4d474e), which sealed v11.380.x:
  - **The ladders down a hole** (T-574), the user's pick: the four caves' ladders as T-570's rungs and rails, NAVEL ROCK's fall hole as its broken lip. DRAFT. In 9.29, T-570's bullet no longer says they wait.
  - Also in the release, outside the bible: T-565's sound census (`docs/sound-census-2026-11-16.md`), its split with the Musical Instruments lane agreed.
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
