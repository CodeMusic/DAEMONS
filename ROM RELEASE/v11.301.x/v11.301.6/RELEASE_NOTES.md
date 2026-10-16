# DAEMONS v11.301.6 — release notes

*Released 2026-10-15 22:58 · built against the design bible v11.301*

- **Engine**: CodeMusic/pokefirered-daemons `8ea66d0ea` (context-content)
- **Design**: CodeMusic/DAEMONS `0ef86f35`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `7a3a283534667815cc263ceceadef4985fab378e` |
| `daemonsContext.gba` | CONTEXT | `dd6cc16dfa2ee1b95af466fd45d5ebf8d6cd0da7` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `432267a3e64f3e9343587ca75a2b278bb8b0aab7` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `9afc03d463b45f802edb522a27d61d7b5a68eb01` |

## The engine since v11.301.5

- `8ea66d0ea` T-402 (the user, 2026-10-15): THE BAND'S SHEET ends on a code to The Painted Mirror's episode 4, Where Sound comes to Light, and Light comes to Sound

## The design and tools since v11.301.5

- `0ef86f35` companion_export.py, C-125 (companion 50fc085): each NOTEBOOK page's SEEN flag (T-403, so the phone marks it unread as the game does), the place it was found (notebook_notes.h's map, named from maps.json) and the song or post its QR code opens (T-402: sPageQr -> sQrCodes -> the URL above each code). check_generators: 131 clean; --check agrees.
- `d187a77c` qa: C-121 -- both Dials on the bench
- `d3c3df34` T-402 closed (engine 8ea66d0ea): THE BAND'S SHEET links The Painted Mirror's episode 4
- `f041d485` ROM release v11.301.5: every page from a public song ends on a QR code to it -- the user's nine links, fifteen more pages (T-402)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
