# DAEMONS v11.335.3 — release notes

*Released 2026-10-31 22:18 · built against the design bible v11.335*

- **Engine**: CodeMusic/pokefirered-daemons `92375b5d9` (context-content)
- **Design**: CodeMusic/DAEMONS `1a792c5a`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `7b3c344693cf0f32e2723d1d0b72c1f466e0caed` |
| `daemonsContext.gba` | CONTEXT | `31ea89efacad8091fc46d8ff4034f32706987a48` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `5c7b923481c24ae6b1bebd8bf042a9cba02886d9` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `14f78594d9419fad0097bf0dfe83f6d1c99e66a7` |

## The engine since v11.335.2

- `92375b5d9` T-483 (5): THE ROOM and THE MIRROR in the SPELLBOOK

## The design and tools since v11.335.2

- `1a792c5a` qa: the companion's GLASSES card (C-262)
- `8e0c0785` TODO: T-483 (5) THE ROOM and THE MIRROR (engine 92375b5d9)
- `3edb544f` T-483 (5): theatre route t483_room_mirror (3/3) and qa 31Oct2026 T483 62-64 -- THE ROOM and THE MIRROR; t483_spellbook's and t483_pull's cursor counts for the two new rows (6/6, 3/3)
- `16e95a76` ROM release v11.335.2: T-483 (5) THE PULL and THE GREAT HAND in the SPELLBOOK

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
