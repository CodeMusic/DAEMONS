# DAEMONS v11.301.2 — release notes

*Released 2026-10-15 12:10 · built against the design bible v11.301*

- **Engine**: CodeMusic/pokefirered-daemons `15a6ba752` (context-content)
- **Design**: CodeMusic/DAEMONS `c31e1725`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `f50707edf7a50738edae851d83f74533ad713411` |
| `daemonsContext.gba` | CONTEXT | `75fedcef3e5c32baddd0981dfbd2706f73ab446a` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `321c23b821c90332f5596cfcea8e85251e5e317f` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `d0f68d5c8503426b131ce42e373696a8c2e5f1ff` |

## The engine since v11.301.1

- `15a6ba752` T-401 (2026-10-15): REST restored where the REST->IDLE move sweep reached plain English -- the SAFARI ZONE's four REST HOUSE signs (since 5baafcbcd, 2026-09-10) and the band's sheet, THE TUNE KNOWS THE REST (since bc7cba35f). DRAFT.
- `4dbb37611` Debug SOUND: SONG walks to the last appended song (MUS_CALLOW), not MUS_BRAZEN -- it could never play SLATE's or CALLOW's own (found recording T-05, 2026-10-15)

## The design and tools since v11.301.1

- `c31e1725` T-401 (engine 15a6ba752): REST HOUSE and THE TUNE KNOWS THE REST restored, and held in port_vocab and check_lexicon
- `ab127a85` qa: C-121 -- the Fire on the bench, the three buttons and five expressions
- `8040d4d0` T-392 filmed and T-05 recorded for the user's approval (engine 4dbb37611: the debug SOUND row reaches every song)
- `f3db30f4` ROM release v11.301.1: the loose pages say what they are about (T-401) and the song pages end on their songs (T-402); v11.300.x sealed into its notes PDF

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
