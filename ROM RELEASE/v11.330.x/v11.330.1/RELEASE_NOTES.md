# DAEMONS v11.330.1 — release notes

*Released 2026-10-29 18:26 · built against the design bible v11.330*

- **Engine**: CodeMusic/pokefirered-daemons `7a607a7cd` (context-content)
- **Design**: CodeMusic/DAEMONS `cf21a9fa`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `13f6a0ec567473aadba2ff4a79c44034142e99ff` |
| `daemonsContext.gba` | CONTEXT | `87db655d9179494d3cdfde10526595207ee998f4` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `77f7288fddf0ebd0f789ee54eb359cdf3aaf9e7c` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `1fc824c9fc7987ebd84cc9bce4cdfe41d00e6da0` |

## The engine since v11.329.1

- `7a607a7cd` T-489 (DRAFT): ALIGN, the frame family's reverse -- a CONTEXT routine (382) whose foe takes the user's first type
- `297e3339d` T-491 (DRAFT): CONSENSUS grows with how far the party's streaks overlap, SLANT with how far they diverge
- `06d0f4858` README: latest release v11.329.1

## The design and tools since v11.329.1

- `cf21a9fa` engine.md: the numbers after ALIGN and CONSENSUS
- `e53c916a` qa: T-489 ALIGN in battle, T-491 CONSENSUS at high and low overlap (theatre, DEBUG build)
- `0fef4e24` Bible v11.330: 9.32 traded, lent and given (T-492's GIFT mark); 3.10's menus and field released (T-481 B+C)
- `7293bb80` animcensus: ALIGN (EFFECT_ALIGN) files under the COPY family -- T-489, the frame family's reverse
- `b1ba75c1` README and wiki: v11.329.1; the menus, the panes and the map's light keep the calendar too (T-481 B+C)
- `90112df2` TODO: T-481 struck (B+C released v11.329.1); T-489's answers; T-492 filed -- a daemon given, the game's half (the user: its own GIFT mark)
- `6109eb77` manual: rebuilt for v11.329.1
- `779211dd` ROM release v11.329.1: T-481 B+C the menus and the overworld keep the calendar; v11.328.x sealed

## The design bible's own entry for v11.330

### v11.330 — 2026-10-29

- **9.32, Traded, lent and given (new section).** It brings together the trading the companion does (T-473, C-219), loans and the PENPHIN pair, and it adds the gift (C-223, T-492; the user chose by multiple choice). A gift arrives with "[NAME] arrived as a gift." and FIRST MET: A GIFT, and it still trade-evolves. Both lines are DRAFT.
- **3.10:** all three surfaces now keep the calendar. The menus and the field were released in v11.329.1 (T-481 B, C).
- A Settled entry in section 10.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
