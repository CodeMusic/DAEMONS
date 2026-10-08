# DAEMONS v11.297.1 — release notes

*Released 2026-10-08 12:28 · built against the design bible v11.297*

- **Engine**: CodeMusic/pokefirered-daemons `c4d5edf8b` (context-content)
- **Design**: CodeMusic/DAEMONS `467f51f8`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `b4b584e820148c61a93cd907e99bbfa449798937` |
| `daemonsContext.gba` | CONTEXT | `68a23dc90a4eee3a15c022e49e4979d4338f02ea` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `ac47f8854942a2591579b9a46d054e8fca0dc37c` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `878f1dd9de6a3125bfc13622cd81d23330bc7390` |

## The engine since v11.296.3

- `c4d5edf8b` T-391 (DRAFT): the PLUGINs' last vanilla words -- 15 routine descriptions written for the game (PROTECT's firewall, SAFEGUARD's safe mode, DISTILL, HOMING, AMBIENT, RIPPLE, DISUSE and RAPPORT by trust, DISCHARGE, TRANSIENT, CARRIER, RADIATE, FLASHOVER, DEGRADED, LIFT) and UNLOAD's own (it printed EVICT's); the help's DRIVER page (holding the DRIVER is enough, not 'destroy an obstacle, fly, surf'), a swimmer's 'surfing type', and the water's 'dyed a deep blue'
- `ea05bf16f` T-388: TRAVERSE's ride is a manta ray -- six frames drawn by DAEMONS tools/gbamanta.py from a sprite-server draft (seed 3111), in the player's own palette; the wingtips lift on the second frame of each pair, the same wave as GOTO's ribbon

## The design and tools since v11.296.3

- `467f51f8` T-388 done (the manta, engine ea05bf16f) and T-391 done (DRAFT; the PLUGINs' last vanilla words, engine c4d5edf8b); T-393 filed: DESCEND never given, two LOCK ONs
- `eefa241c` bible v11.297: wisdom -- a MARK and its ROOT together (0.7): seven leaders paired with seven understandings, seven union routines on seven retired PLUGIN numbers, INSIGHT in the NOTEBOOK (rule 2 amended, never numbered); 9.24 amended for the splash's bits and notes; TRAVERSE becomes a manta (the user, 2026-10-08)
- `c9929aa8` T-388..T-392 filed: TRAVERSE's ride, the leaders and the ROOTS with their union PLUGINs, INSIGHT, the PLUGIN audit, the binary-and-music animations (the user, 2026-10-08)
- `fe681223` ROM release v11.296.3: GOTO is not a bird (T-387)

## The design bible's own entry for v11.297

### v11.297 — 2026-10-08

### Wisdom: a MARK and its ROOT together (2026-10-08)

- ***0.7, Wisdom (the user's decision, T-389, T-390)***: **intelligence and understanding together are wisdom.** *Seven
  leaders each pair with one understanding (five by the map, two by type; SCORN with none): talked to after the win,
  each says what the MARK taught and where to come back understanding, or, with it held, what the two make together,
  and gives that pair's union routine on a PLUGIN.* **Seven new routines on seven retired PLUGIN numbers** *(PRIOR,
  UNLOAD, INSTANCE, PAIR, AMBIENT, DISUSE, BIT ROT), because the TOOLKIT's slots are in the save.* **An insight arrives
  when both are held and is filed in a new NOTEBOOK section, INSIGHT** -- *rule 2 amended: it grows, never numbered.*
- ***9.24, amended (T-392)***: **routines may carry the splash's bits and notes**, *in their type's colour (binary on
  the CONTENT side, notes on the CONTEXT side); the seven union routines alone wear the splash's own colours.*
- ***TRAVERSE (T-388)***: *the water ride, still vanilla's shape, becomes a manta ray whose wings ripple like GOTO's
  wave (the user's pick).*

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
