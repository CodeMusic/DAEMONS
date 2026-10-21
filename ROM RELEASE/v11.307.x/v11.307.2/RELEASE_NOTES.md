# DAEMONS v11.307.2 — release notes

*Released 2026-10-20 20:40 · built against the design bible v11.307*

- **Engine**: CodeMusic/pokefirered-daemons `af8771e31` (context-content)
- **Design**: CodeMusic/DAEMONS `731d9026`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `3f87fd65c4161cf9114484a64b76dd274b6931b5` |
| `daemonsContext.gba` | CONTEXT | `7f7877832d60f6660bbbcce9a063cf2a28a13e2a` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `ab7e965f343d84a4195cb1a0e2e3a5e74fd7f4ed` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `3287fa14f991fbe4a97dc68aa015d306260354d6` |

## The engine since v11.307.1

- `af8771e31` T-18 P1: THE FOLLOWER walks and hides -- the lead (the first party daemon not an egg, HALTED or AWAY) walks a tile behind as its own party icon (no new art), 1x, in its TYPE colours (src/data/follower_palettes.h: the icon's shared palette remapped to the nearest colours of its front palette, by DAEMONS tools/gbafollowerpal.py, 14 KB), greyed by friendship (T-424's Saturation_ApplyToBuffer), in the field's light and weather; a 1 px hop mid-tile, flipped facing right. A SPRITE, not an object event: no object slot, blocks nothing, never saved or recorded. It replays the player's sprite path 16 px late (a ring of 16 pixel steps, IWRAM 72 B), so walk/run/bike/stairs/turn-back-swap come free and world pixels carry it across seams; a ledge's 32 px count as 16, so it waits above the ledge and jumps it on the next step. Hidden and snapped (walks out of the player after): surfing, forced movement, a FLASH-dark cave, a warp/door (the player's sprite hidden), a script moving the player (cut scenes) until it lets go. Absent: OPTIONS FOLLOWER OFF (new eighth row, DRAFT; FLAG_FOLLOWER_OFF 0x3E2 in SaveBlock2's filler, 0 B save), no lead, link rooms, the Continue recap, no free OBJ palette slot 12-15 or sprite. Comes back where it stood after a battle or menu (same map and tile), else on the player's tile. The party is read every 8 frames, not every frame. DEBUG -> GAME EVENTS -> FOLLOWER >: on/off, lead friendship 0/70/150/255.

## The design and tools since v11.307.1

- `731d9026` T-18 P1 built (engine af8771e31): tools/gbafollowerpal.py writes the follower's type palettes; tools/routes/follower-walk.json (11 stops, all pass); theatre_route.py learns keyitem and follower shown|hidden|absent, and its friendship step holds the follower's party reads off while its pokes land (one poke a frame left a checksum mismatch a per-frame read turned into a BAD EGG); companion_export.py leaves the DEBUG FOLLOWER page out of the PROFILE's events; TODO notes P1 on T-18's row
- `aa426942` qa: T-406 BOUND
- `e3cbb7e5` ROM release v11.307.1: the INDEX says how a daemon you hold came to you -- BOUND (T-406); THE SUBTLE LAYER's cover (T-423); seals v11.306.x

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
