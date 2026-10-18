# DAEMONS v11.303.3 — release notes

*Released 2026-10-18 06:42 · built against the design bible v11.303*

- **Engine**: CodeMusic/pokefirered-daemons `ef820ebf9` (context-content)
- **Design**: CodeMusic/DAEMONS `d327e2e8`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `2d8bab6070ae28db89cf0a498fd341b6f2505cf2` |
| `daemonsContext.gba` | CONTEXT | `38a7f96275fd3b88ebb4cb24287e69836b4ae030` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `f2b423600211b6a397437b9ab2890e988e231236` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `de0025c7280355f5b126ac2422a647145fc29e4c` |

## The engine since v11.303.2

- `ef820ebf9` T-416 HOLIDAYS P1+P2 (the user, 2026-10-17/18): the holiday lookup (clock, or play time's one watch), the month's note and colour on the day banner and the trainer card, LONGEST DAY/NIGHT's hours; the gifts at the CHECKPOINT, MOM and the sand, once per holiday per year; THE YEAR in the NOTEBOOK; DEBUG DATE and GAME EVENTS -> THE YEAR (DRAFT)
- `9f1e3f4f6` T-417 BREATHVERSE (the user, 2026-10-18): the islet rounded -- irregular, a small spit, the general set's shore pieces and inner corners (tools/gbabreathverse.py); and timeless: no season and no watch's light on it (DaemonsIsTimeless in fieldmap.c)

## The design and tools since v11.303.2

- `d327e2e8` genholidays --companion keeps the steps_off note at the top of holidays.json
- `0acda60a` T-416 HOLIDAYS P1+P2 built (engine ef820ebf9): genholidays drops the FIRST alias; THE YEAR's SEEN 69-80; companion_export writes holidays.json and THE YEAR (not run)
- `4ba1528c` T-417 BREATHVERSE: the islet rounded (tools/gbabreathverse.py: shore pieces and inner corners, a spit, 28x26) and timeless (engine 9f1e3f4f6)
- `34aac915` TODO: T-421's line lists from the review
- `c943c42c` T-421 (code-health review): check_lexicon's exit code counts every check -- the near-collisions' count was overwritten, the type copy and phantom places never reached it; port_pronoun.py refuses over T-391's later work (driftguard). TODO: T-419's row (never written), T-420 (STREAM and OPUS share flags), T-421
- `1a57eefe` TODO: T-410, T-411 (A) and T-412 approved as drafts (the user)
- `f3e2aeef` TODO: T-417 BREATHVERSE released; round the islet, keep it timeless (the user)
- `0746badb` qa: T-417 BREATHVERSE
- `ccf8b56e` ROM release v11.303.2: BREATHVERSE -- CONTEXT's FLUTE on an island grove through a palm on ROUTE 2; THE NEXUS its own section (T-417)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
