# DAEMONS v11.392.1 — release notes

*Released 2026-11-17 22:27 · built against the design bible v11.392*

- **Engine**: CodeMusic/pokefirered-daemons `02b44f853` (context-content)
- **Design**: CodeMusic/DAEMONS `be4e2cad`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `8fdcb210161ee194f7956ccc1552cf32ece3c671` |
| `daemonsContext.gba` | CONTEXT | `857dbb9e3734a6fbcfc5b124429cc88315fbab69` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `2d91f8c9ba6fc2a2b82b31b962ae20ee4e5c93a3` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `97108ef0e1ab1a05646c0df1ab09bafb17e2ccd4` |

## The engine since v11.391.1

- `02b44f853` T-565 batch 12: our own instruments under our older songs -- sixteen synthesized samples (piano, glockenspiel, xylophone, tubular bell, nylon guitar, two basses, pizzicato, timpani, strings, choir, trumpet, tuba, french horn, oboe, whistle) and PLAY's harp and flute in voicegroup191's nineteen played slots, envelopes unchanged; the dawn chorus's choir is ours too; no note and no bank moves (the user's pick, DRAFT; DAEMONS tools/genbank.py, gbavoices.py, genchorus.py)
- `561235063` README: the release line names v11.391.1

## The design and tools since v11.391.1

- `be4e2cad` T-565 batch 12: tools/genbank.py, our own instruments (engine 02b44f853); gbavoices.py points voicegroup191's played slots at them, genchorus.py its choir
- `fa758d73` Bible v11.392: the cries, A shaped by B (T-565 batch 11, v11.391.1)
- `c561f517` README and wiki Home name v11.391.1
- `ea54b57b` ROM release v11.391.1: T-565 batch 11, all 388 cries, A shaped by B -- the type's motif ordered by the name (DRAFT); seals v11.390.x

## The design bible's own entry for v11.392

### v11.392 — 2026-11-17

- Recorded from release v11.391.1 (ea54b57b, engine ba5c05d43), which sealed v11.390.x:
  - **The cries** (T-565 batch 11, the game lane): all 388, A shaped by B, the user's pick from four approaches. DRAFT. In 9.5, after THE MARGINS; the borrowed cries left for T-584.
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
