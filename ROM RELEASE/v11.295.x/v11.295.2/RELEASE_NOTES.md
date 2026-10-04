# DAEMONS v11.295.2 — release notes

*Released 2026-10-04 15:38 · built against the design bible v11.295*

- **Engine**: CodeMusic/pokefirered-daemons `4a5895b45` (context-content)
- **Design**: CodeMusic/DAEMONS `6f574f33`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `f1766d0f0f2b372eabc6a19a32bb1d334e0bf305` |
| `daemonsContext.gba` | CONTEXT | `faf4f9d82cb3864928195647f4b766dfeb4d1ba8` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `26c120b42f6bc25829dce7c14f4b27a02a046182` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `47be5b3043fad594377ebd7d45324595a5c31c02` |

## The engine since v11.295.1

- `4a5895b45` T-374: only a daemon in full health goes AWAY, and an AWAY daemon is out of reach
- `7399b38ea` T-349: the catching lesson's old iguana reads as an iguana -- a spiked crest on the crown and a blunt snout (tools/genmentors.py)
- `2ae2997b1` T-371: a lemur on every CHECKPOINT's second floor tells you about the companion, and that it brings SEND
- `d1ab256d0` T-370: AWAY reshaped -- SEND only for a save the companion has synced, one daemon at a time, and an emergency way home

## The design and tools since v11.295.1

- `6f574f33` T-349, T-371, T-374 closed: the iguana that reads as one, the lemur on every second floor, and AWAY's health and reach rules
- `d4b5cd39` companion_export: items.json, for what an AWAY daemon holds (companion C-31); T-374 decided: AWAY needs a healthy daemon, and an AWAY daemon is out of reach
- `f1f92029` genmentors: the iguana's crest and snout (T-349); check_reach knows FLAG_COMPANION_LINKED is the app's to set (T-370)
- `b9add7cb` T-370 closed (engine d1ab256d0): AWAY reshaped; T-373 closed: the companion's words kept matching (companion_export --check in the push routine)
- `c106628f` ROM release v11.295.1: the OWL in CALLOW SCHOOL's colours (T-366)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
