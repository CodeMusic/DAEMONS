# DAEMONS v11.315.2 — release notes

*Released 2026-10-28 05:23 · built against the design bible v11.315*

- **Engine**: CodeMusic/pokefirered-daemons `6d04ef3df` (context-content)
- **Design**: CodeMusic/DAEMONS `e8ea0f7d`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `84d2a40d3ded5987a165cb6a94a57a9ac46d1d25` |
| `daemonsContext.gba` | CONTEXT | `5fbd1998023821809ad8e384b0e26b1e652b225a` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `8ddb76a81fb4ca5f63457ad35f1fb436c9a51b0d` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `92d4b8fe9070379a8e5d1c85db9c6f48eec434a2` |

## The engine since v11.315.1

- `6d04ef3df` T-462 ITS DREAMS (DRAFT): the companion's dreams reach the game -- a third DREAM LOG part beside YOUR DREAMS and HER DREAMS

## The design and tools since v11.315.1

- `e8ea0f7d` TODO: T-462 ITS DREAMS built as a DRAFT (engine 6d04ef3df) for the user's review on the device
- `1ba0d885` T-462 ITS DREAMS (DRAFT, engine 6d04ef3df): docs/its_dreams.json -- sixteen dreams, a title each, an opening and a broken/quiet/vivid ending -- and tools/gbaitsdreams.py, which checks every width (208px lines, 130px titles), no counting, no sleep, and writes src/data/its_dreams.h; companion_export: profile_layout's its_dreams (the vars' save offsets, the filed flags, the titles) and notebook's its_dream pages
- `a3af7d99` qa: T-452 batch 9 sheets (v11.315.1)
- `b65d5dfe` ROM release v11.315.1: T-452 batch 9 (ALARM to RELEASE) on the user's answers; v11.314.x sealed

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
