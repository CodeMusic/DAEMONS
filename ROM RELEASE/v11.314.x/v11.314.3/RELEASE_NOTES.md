# DAEMONS v11.314.3 — release notes

*Released 2026-10-27 22:24 · built against the design bible v11.314*

- **Engine**: CodeMusic/pokefirered-daemons `03a30f1be` (context-content)
- **Design**: CodeMusic/DAEMONS `7c52bede`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `b6a9c4d70b9353e9f3a4a541c650799a6ba02e59` |
| `daemonsContext.gba` | CONTEXT | `c62f464ddf2dd09d5f1780304fa526b3696a7a75` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `3969754d1eb9d53afe359d5993ba7e9a4d945510` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `28ff01750b4a1837a082a595f56315da0edb7011` |

## The engine since v11.314.2

- `03a30f1be` T-459 C: the lean -- before some turns, where "What will X do?" stood, a purple line about what the foe will do
- `786eff67c` T-452 batch 5 follow-ups: ACQUIRE's crab pincer, AXIOMKICK's kicking leg, ARCHIVER frosted, BREAKER bigger and cracked with sparks, CIRCULAR's headstand, BOOTSTRAP's six-egg back

## The design and tools since v11.314.2

- `7c52bede` T-459 C built (engine 03a30f1be): the lean in battle, in the book's purple where the question stood; counted, landed by what the foe did
- `a650e959` qa: T-452 batch 5 follow-ups sheets
- `860e7716` T-452 batch 5 follow-ups built (engine 786eff67c): ACQUIRE's pincer, AXIOMKICK's leg, ARCHIVER frosted, BREAKER bigger and cracked, CIRCULAR's headstand, BOOTSTRAP's six-egg back
- `5de571ba` TODO: T-452 batch 5 released (v11.314.2) and the user's six follow-ups
- `ca8af4d4` qa: T-452 batch 5 sheets (v11.314.2)
- `52ba0d87` ROM release v11.314.2: T-452 batch 5 -- HEATSINK to COREFILE and the PREMISE line, hand-drawn to their entries

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
