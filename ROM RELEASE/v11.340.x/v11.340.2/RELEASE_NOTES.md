# DAEMONS v11.340.2 — release notes

*Released 2026-11-05 11:02 · built against the design bible v11.340*

- **Engine**: CodeMusic/pokefirered-daemons `3e7697468` (context-content)
- **Design**: CodeMusic/DAEMONS `3fd177ff`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `853f6af64e325fbd9f0ad2618eb405ad87d3f160` |
| `daemonsContext.gba` | CONTEXT | `a0e62ec4b21ec492caa6beec373c0eb5ae4f980d` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `5dc972196486a2a9bbe834290c68dfbc2da50346` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `677cd426447e368b122b283f5baff04c94d1a116` |

## The engine since v11.340.1

- `3e7697468` T-519 item 3: the deepening's and the burst's colours as a table by brightness, built once a frame -- worked out per entry they overran the vblank's pass and starved the main loop (filmed: a frame a minute); and each step's splash after the mending stronger (150 of 256)
- `00085e73d` T-519 item 3 (6/6): DEBUG -> GAME EVENTS -> MENDED (on: both halves found and mended at once, THE UNITY BOOK in the bag; off: unmended, the halves back) and THE HORIZON SAID (on: its once spent; off: unsaid, with the twelve marked cast so it can be said again)
- `15ad62eda` T-519 item 3 (5/6): THE HORIZON, the mended book's thirteenth -- listed once THE UNITY BOOK is mended and the twelve are cast, in either thin hour (the SPELLBOOK opens for it in the creator's hour), once a playthrough (VAR_SPELLS_CAST bit 14, its own). The two thirteenths together: every cost THE WITCHING HOUR lifts is lifted (nothing owed), THE RETURN said under it is not spent (nothing lost), and it lasts from the cast to the end of the creator's hour that morning. RAM only, as the witching hour. DRAFT
- `49a8d728b` T-519 item 3 (4/6): the mending -- at DAEMON TOWER with both halves held, the first step inside (or a half opened there): the burst, the tower's tone turning through every colour into its own; the halves leave the bag and THE UNITY BOOK (ITEM_UNITY_BOOK, was ITEM_0FA) comes in, their flags kept. Its reader: 11 sections at an 11px contents pitch (the others keep 12), the ATTESTATION's observer line by the lead daemon's SPIRITS, any hour, its folds letting the night half's spells off the page. Leaving the tower the town comes back into colour over 20 steps, a splash at each. DRAFT
- `5802a82e4` T-519 item 3 (3/6): a half at DAEMON TOWER before the mending -- opened from the bag on any floor, its tint deepens for a moment (deep emerald for the night half, deep sapphire for the dawn half; over a floor's own colours where it is back in colour) and settles, and its last page ends torn mid-sentence at the spine. DRAFT
- `7b85f8a09` T-519 item 3 (2/6): THE UNITY BOOK generated -- DAEMONS tools/gensubtle.py --book unity writes src/data/unity_layer.h (11 sections, BALANCE at the crease; 55 entries; the ATTESTATION's observer line by SPIRITS), a placeholder cover with both spines, picture and bag icon; each half's header gains its last page torn mid-sentence at the spine (HERMETIC_TORN_ENTRY, EUDAIMON_TORN_ENTRY). DRAFT
- `601cf9105` T-519 item 3 (1/6): HALFTONE's tone follows the halves held -- greyscale with neither, emerald sepia with the night half, sapphire (a cyanotype) with the dawn half, both unmended by the hour (emerald at night, sapphire by day); each tone a 32-step ramp of exact brightness so a settled frame stays one compare an entry. Mended (FLAG_UNITY_MENDED, was vanilla's unused FLAG_0x4BD): the town and every tower floor in colour, grey only in the witching half-hour, extra vivid in THE CREATOR'S HOUR (a negative print fade as the palettes load, four steps, relit as it moves). The deepening, burst and step-by-step spread the later commits drive. DRAFT

## The design and tools since v11.340.1

- `3fd177ff` TODO: T-519 the mending (engine 601cf9105..3e7697468)
- `5b2b0fdd` T-519 item 3: THE UNITY BOOK for the companion (companion_export: unity.json, the item, the GAME EVENTS row; THE HORIZON's debug reset left out), theatre_route's open SPELLBOOK, and the book's pages filed (qa 5Nov2026 T519 25). DRAFT
- `53b08f75` qa: C-298 JOURNEY's JOURNAL and its printed page
- `d0aa45f9` T-519 item 3: gensubtle --book unity -- THE UNITY BOOK from docs/unity-book.md into src/data/unity_layer.h (11 sections, BALANCE at the crease, 55 entries; the ATTESTATION's observer line by SPIRITS; a placeholder cover with both spines and its bag icon); each half's header gains its last page torn mid-sentence at the spine (TORN, measured as a reading). DRAFT
- `151a63b3` ROM release v11.340.1: T-445 the forests' and the SAFARI's place previews; v11.338.x sealed

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
