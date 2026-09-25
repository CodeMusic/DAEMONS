# DAEMONS v11.284.1 — release notes

*Released 2026-09-25 03:01 · built against the design bible v11.284*

- **Engine**: CodeMusic/pokefirered-daemons `562cfff0b` (context-content)
- **Design**: CodeMusic/DAEMONS `8a5b205b`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `a1e70f78097443b6efe6372bbd4d0c14bf078502` |
| `daemonsContext.gba` | CONTEXT | `b5547d12d9d676022989a0d6d6fa00812e4b7c01` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `78560ccea5166e130c3e8d180c423a41278fade1` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `cedfb4e7cb7f923b6fbd04a7b3469072b5a4bc77` |

## The engine since v11.283.7

- `562cfff0b` T-267/T-268: read an entry in battle before binding; day and night
- `77f2585bc` T-266: the STREAM badge says STREAM again

## The design and tools since v11.283.7

- `8a5b205b` v11.284: day and night decided and built (9.21); reading is not keeping (4.2)
- `b4c92496` T-266 closed: the STREAM badge says STREAM again (tools/gbainkpaper.py maps the badge by role)
- `db89a507` ROM release v11.283.7: the terminal never repeats; the cartridge's clock

## The design bible's own entry for v11.284

### v11.284 — 2026-09-25

### The cartridge's clock, and what the user decided with it

- ***Day and night, built*** (9.21, T-268): **the real clock when the cartridge has one (T-265), play time when not** — *dusk, night and dawn tint the outdoor maps and the people on them, as each palette loads; HALFTONE stays grey.* ***On Routes 1, 8, 10 and 12 the day's bird sleeps and LATENT comes out*** — *DANGLING, and RESPAWN on 12, at the same levels and odds.* **OPAQUE waits for the GLOBAL INDEX**: *none of it is in the first 151.* ***DEBUG → WATCH*** *forces a watch, so night can be checked at noon.*
- ***Reading is not keeping*** (4.2, T-267): **in a battle, L reads the whole entry of the daemon in front of you, bound or not; the INDEX still shows ????? until you bind it.**
- ***The terminal never repeats itself, and reads the clock*** (T-264, T-265): *HELP and TUNE draw from every answer but the last; TIME shows CLOCK and the date, DRAFT. The game only reads the clock.*
- ***The STREAM's badge says STREAM again*** (T-266): *T-209's recolour had put its letters and its cloud on the same grey.*

---

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
