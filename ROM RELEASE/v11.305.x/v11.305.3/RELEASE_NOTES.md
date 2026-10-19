# DAEMONS v11.305.3 — release notes

*Released 2026-10-18 21:36 · built against the design bible v11.305*

- **Engine**: CodeMusic/pokefirered-daemons `28184cef2` (context-content)
- **Design**: CodeMusic/DAEMONS `d00d053d`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `76d618fc731b642e7fb77c3743ab8cdd3c953f39` |
| `daemonsContext.gba` | CONTEXT | `ae87469d2115d2a05089372ee9f30f47b5d57596` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `99ff341cf119f003789da86a3689b119bed30818` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `b82308c0bc938240802ff3f94b84f170e1d54297` |

## The engine since v11.305.2

- `28184cef2` T-392 P2: every routine signed in the release ROMs, and every glyph outlined in true black (DRAFT)

## The design and tools since v11.305.2

- `d00d053d` T-392 P2: every routine signed in release, every glyph outlined (engine 28184cef2)
- `b4a8ed03` Wiki: Books -- THE PROGRAMMER'S GUIDE TO THE HUMAN MIND and THE SUBTLE LAYER: what each is, its cover, its chapters, and a link to the one file both the game and the companion are built from (never where they are found); in the sidebar, and linked from The companion
- `0794c1dc` T-423: the companion's book carries the week's note names as words (the staircase picture is unlettered: the game's font is Nintendo's)
- `02281373` TODO: T-392 P1 released; P2 and the glyph outline (the user)
- `4670b198` companion: the GUIDE's cover without its lettering (the game's font is Nintendo's; the app sets the title and author, now in guide.json) -- the user, 2026-10-18
- `d844cfc4` T-423: in the game (v11.305.2) and the companion's LIBRARY; the layout-order lesson recorded
- `de6980a2` T-423: companion_export writes THE SUBTLE LAYER for the LIBRARY -- subtle.json and art/subtle_*.png (the game lane's agreement: this function and its two outputs only)
- `15306f32` TODO: T-427, what the house keeps goes to CORPUS (the user, 2026-10-18; the companion's half is C-167)
- `efbe97aa` ROM release v11.305.2: THE SUBTLE LAYER (T-423, merged), its layout at the end so older saves open where they were

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
