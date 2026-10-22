# DAEMONS v11.309.2 — release notes

*Released 2026-10-22 00:17 · built against the design bible v11.309*

- **Engine**: CodeMusic/pokefirered-daemons `a9b165240` (context-content)
- **Design**: CodeMusic/DAEMONS `e01e253d`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `3cd9f46779b279d1f05f48eb9714807bd0833fdc` |
| `daemonsContext.gba` | CONTEXT | `b414c8dd4e9382af8458cfe220d1556348622716` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `adbac16980155c07db7a14b525394c0901db3fad` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `6c439a3b1214b56343772138e3363a055b9b13e0` |

## The engine since v11.309.1

- `a9b165240` T-435: a wooden boardwalk to the S.S. ANNE pier's fir, there whether the ship is in or gone (the user, 2026-10-21)
- `88a78263a` T-434: SIX ISLAND WATER PATH's grove door moves into the channel (the user, 2026-10-21)

## The design and tools since v11.309.1

- `e01e253d` T-434 and T-435 done (engine 88a78263a, a9b165240): the WATER PATH's grove door in the channel, the pier's boardwalk; check_reach walks the world
- `603d36ad` qa: T-431 the emoji and the slide; T-435 the bridge options
- `e1237041` ROM release v11.309.1: the daemon-emoji over your follower, built from its feelings; the feelings page slides like the others (T-431 P3, struck); seals v11.308.x

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
