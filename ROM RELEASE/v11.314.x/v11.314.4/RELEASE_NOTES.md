# DAEMONS v11.314.4 — release notes

*Released 2026-10-27 23:35 · built against the design bible v11.314*

- **Engine**: CodeMusic/pokefirered-daemons `fca6b5251` (context-content)
- **Design**: CodeMusic/DAEMONS `482fbc8c`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `5a8b8890dfcf6981cc6d38fe977cbcbe4591207a` |
| `daemonsContext.gba` | CONTEXT | `2ab6b22462f01abe05f943abda0d28b13f891c22` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `6d0bbc68da9ef6e669450a02719239267603e434` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `203c8322a46e42b10558e5e91152c3b8d6a6cda8` |

## The engine since v11.314.3

- `fca6b5251` T-459 B: a read -- now and then, the first step on a map brings "A read: / something by the water." in the book's purple; the NOTEBOOK's READS -> THE LOG counts reads and leans
- `f7cbd87e6` T-452 batch 6: SLURP to COLDREAD (108-124) with HEARTBEAT, TURBULENCE, SIGKILL and TELL in the new style; grounding rows, icon palettes, overworld art, follower palettes

## The design and tools since v11.314.3

- `482fbc8c` T-459 B built (engine fca6b5251): a read on arrival in the book's purple, "A read:" (the user's word); the NOTEBOOK's READS -> THE LOG counts reads and leans
- `27ae2ce8` TODO: T-452 batch 6 built (engine f7cbd87e6) on the user's answers
- `78af106c` T-452 batch 6 built (engine f7cbd87e6): SLURP to COLDREAD with HEARTBEAT, TURBULENCE, SIGKILL and TELL as gbasprite's sources
- `e23f0474` ROM release v11.314.3: T-452 batch 5 follow-ups (ACQUIRE, AXIOMKICK, ARCHIVER, BREAKER, CIRCULAR, BOOTSTRAP); T-459 C the lean in battle

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
