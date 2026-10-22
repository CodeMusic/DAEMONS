# DAEMONS v11.309.1 — release notes

*Released 2026-10-21 22:38 · built against the design bible v11.309*

- **Engine**: CodeMusic/pokefirered-daemons `659ce4ef7` (context-content)
- **Design**: CodeMusic/DAEMONS `53d7b623`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `5f4b75d28eb20d5d9c113ce1be829b66c0345ede` |
| `daemonsContext.gba` | CONTEXT | `20392e774c9b31ff76d6be52595242874c76fa56` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `01888562de80364f3fbd3a313b2e95e4e0685077` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `2a7dcecc58e93035318430c4be777d3de699b3f4` |

## The engine since v11.308.4

- `659ce4ef7` T-431 P2 (the user, 2026-10-21): the SUMMARY's fourth page slides in and out like the vanilla pages
- `3487137c8` T-431 P3: the daemon-emoji over the follower -- its face built from the lead's feelings, never named

## The design and tools since v11.308.4

- `53d7b623` TODO: T-435 traced; the user chose the wooden boardwalk, kept the ticket gate, wants a ship-in-port DEBUG jump
- `99282fd6` T-431 P3 built (engine 3487137c8) and the fourth page slides (engine 659ce4ef7): T-431 closed
- `35a6c084` TODO: T-435 the pier's fir on foot, and after the S.S. ANNE has gone (the user, 2026-10-21)
- `1e3b2ba6` TODO: T-434 traced -- SIX ISLAND WATER PATH's grove door is on outer sea; the user chose a channel rock
- `fa5bea89` TODO: T-434 a NEXUS door strands the player (the user, 2026-10-21)
- `4ebe2882` T-428: the game on an iPhone -- TAP TO PLAY when iOS holds its sound back, and a device's errors in the playground's log (daemons-playground d28f2e4); qa T-428
- `514389cf` qa: T-433 the items table
- `e71027bf` Bible v11.309: items and moments move feelings (4.9, T-433); TODO T-433 decided
- `e6dbe144` TODO: T-433 items move feelings and friendship (the user, 2026-10-21)
- `a0445872` qa: T-431 the feelings page
- `20379cbc` TODO: T-431 P2+P4 released v11.308.4; the user's answers (the page should slide)
- `83636350` ROM release v11.308.4: the SUMMARY's fourth page -- feelings drawn on an unlabelled grid, never named, with the 16 lines you approved (T-431 P2+P4, DRAFT); two DAEMON CENTER and two DAEMON MART leftovers now CHECKPOINT and THE REPO

## The design bible's own entry for v11.309

### v11.309 — 2026-10-21

### Items and moments move feelings (T-433)

- ***4.9 extended (the user)***: **items and moments push the feelings** -- potions and revives gladden by strength, the RARE CANDY angers a little (growth taken), bitter herbs and disliked berries rankle, a TM gladdens, the REMNANT unveiled frightens the party once; evolving, LEADERS and the HALL OF FAME gladden, a release saddens. *The whole table and its numbers are DRAFT and private to the plan.*

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
