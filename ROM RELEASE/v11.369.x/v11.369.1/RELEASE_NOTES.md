# DAEMONS v11.369.1 — release notes

*Released 2026-11-15 11:34 · built against the design bible v11.369*

- **Engine**: CodeMusic/pokefirered-daemons `0aee7681c` (context-content)
- **Design**: CodeMusic/DAEMONS `c04fae5a`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `bb2991233f38d4d929a168e2d9ed4b4606c01580` |
| `daemonsContext.gba` | CONTEXT | `3575d28629755fb7f6e59725d5623d1c88d989bc` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `b010dc84bc82579f0d135b7d900676f6279ae8b4` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `30422021981ec2d5c3e35be52f2c27642a15f7d1` |

## A note on the book audio

A minor release, released with two recordings deferred (the user, 2026-11-14: "Release now, record after"): THE COMPANION's and the new T-GLASSES book's.

## The engine since v11.368.1

- `0aee7681c` T-563: the INDEX and the map in A TERMINAL -- the INDEX's own tiles, its mini card and AREA UNKNOWN's plate, the town map's head drawn from the player's own sprite, the SWITCH cursor, HEARSAY's cursor and ?
- `535094ec0` README: the release line names v11.368.1

## The design and tools since v11.368.1

- `c04fae5a` T-563 BUILT: the INDEX and the map, all A (engine 0aee7681c)
- `b0c95daf` T-563 DRAFT: the INDEX and the map -- A/B/C for the INDEX's tiles, mini card and ellipse, the town map's heads (from the player's own sprite) and switch cursor, HEARSAY's cursor and ?
- `97630631` TODO: T-563 filed -- the INDEX and the map, batch 4 of the 2026-11-14 re-census (the user's pick)
- `ca66b30f` Theatre verification of today's unseen builds: T-556, T-557, T-559, T-561, T-562
- `33c05622` qa: C-221 the link cable as video (companion fd7e7b7)
- `701cba74` Bible v11.369: the towns' last Nintendo tiles (T-562, v11.368.1)
- `24eec7b8` README and wiki Home name v11.368.1
- `fd158d6d` ROM release v11.368.1: T-562 the towns' last Nintendo tiles -- 309 in nine towns, LURID THE HUM, VERDIGRIS's store in BRONZE PANELS and its fountain as RINGS (DRAFT); seals v11.367.x; two recordings deferred

## The design bible's own entry for v11.369

### v11.369 — 2026-11-14

- Recorded from release v11.368.1 (fd158d6d, engine 0dabcb96e), which sealed v11.367.x:
  - **The towns' last Nintendo tiles** (T-562): 309 tiles in nine towns and VERDIGRIS's fountain, the user's picks. DRAFT. 9.29, beside the ground bullet.
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
