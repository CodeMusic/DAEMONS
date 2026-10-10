# DAEMONS v11.298.2 — release notes

*Released 2026-10-09 22:32 · built against the design bible v11.298*

- **Engine**: CodeMusic/pokefirered-daemons `2e4a96f2d` (context-content)
- **Design**: CodeMusic/DAEMONS `1e77e815`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `98823149350a164b0b58beb4ac9a3bf05db90024` |
| `daemonsContext.gba` | CONTEXT | `e9935a8db6414e35dc4f197bb52d807db78dcb31` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `e6f62eebc17a4780faab994f01ec83ce8041cac5` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `7fdcb29ab688fd2fb31d844b52df3b5a15b2056c` |

## The engine since v11.298.1

- `2e4a96f2d` T-395: the NEXUS residents -- eight new daemons in the unused slots OLD_UNOWN_C..J
- `2c64c15d0` T-397 (the user, 2026-10-09: "you always need one in your party"): the PORT and the DAY-CARE count a daemon asked for as gone, as SEND already does -- asking for one and then storing the other could have left the party empty at the next SYNC.

## The design and tools since v11.298.1

- `1e77e815` T-395: REFLECTION is both the NEXUS wolf and the stone LYNX grows by, on purpose (the user, 2026-10-09)
- `c022db45` qa: the NEXUS residents' sheets (T-395)
- `d5e79f35` T-395: the NEXUS residents in the game (engine 2e4a96f2d) -- tools/gbanexus.py writes the eight into the unused slots with their art, approved INDEX entries and OPUS's margins (DRAFT); their drawings also in gfx/daemons/ beside everyone else's. companion_export, reviewsheet and the item animation learnt a slot's second name (REFLECTION is OLD_UNOWN_C), and the export drops INDEX numbers past the save's 416 flag bits. still-vanilla.md marked stale. Waiting on the user: REFLECTION is already the MOON STONE's name.
- `f9f4189c` T-395: the NEXUS residents' back sprites -- drawn from behind on spriteforge, cleaned to 64x64; the fronts approved by the user (gfx/drafts/nexus/final64/README.md)
- `a40600d8` qa: the home-screen widget (C-100)
- `710c98fa` T-395: the NEXUS residents drawn on spriteforge (roverbyteseer) and cleaned to 64x64 -- REFLECTION with its black mirror, LODESTAR, PERIHELION with its cosmos, LYUBOV out of her oval, MULTIMAL with a light within, ILLUMINED, LYNX, BASTET; every drawing with its seed and prompt (gfx/drafts/nexus/final64/README.md). DRAFT, for approval.
- `fca35a8b` qa: the M5GO draws CAREMUSAI (C-97)
- `fcb3ad60` T-397 done (engine 2c64c15d0): one daemon always stays in the party -- the PORT and the DAY-CARE count one asked for as gone; the companion keeps the same rule at SYNC
- `9bd062b4` qa: T-396's picture
- `ec645bbc` ROM release v11.298.1: any number of daemons AWAY, one to a device (T-396)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
