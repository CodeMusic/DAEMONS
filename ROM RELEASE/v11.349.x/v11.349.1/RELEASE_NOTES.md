# DAEMONS v11.349.1 — release notes

*Released 2026-11-11 13:17 · built against the design bible v11.349*

- **Engine**: CodeMusic/pokefirered-daemons `714db52a1` (context-content)
- **Design**: CodeMusic/DAEMONS `d3dbb426`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `be3bc950124f9108b1e3833071a594250f4fc2ef` |
| `daemonsContext.gba` | CONTEXT | `d71c45409e2d84819740bb0316b67b7a263e80e4` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `358c23b73454f6cb84e0b69765aace0f56b703ee` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `5621df5b72bf75e37f3857b93665cd23f046a74a` |

## The engine since v11.348.2

- `714db52a1` T-519: THE UNITY BOOK's bag icon in the indigo board colour (gensubtle --write)
- `867208802` T-519: the third book's three covers regenerated (gensubtle --write, DAEMONS 0df91b92) -- the night half's tablet mirrored in a still pool, the dawn half's star over the fir with the lark, the mended cover holding both plates; UNITY_PALETTE's C_SLATE now indigo (8,7,18), cover and icon only (the user, 2026-11-11; DRAFT)
- `27a29b6f7` T-534: the MUSAI branch's followers, drawn from the finals -- all six forms in all four seasons, 24 looks (the user, 2026-11-11: "Yes, draw them"; DRAFT)

## The design and tools since v11.348.2

- `d3dbb426` T-447 pair 7 DRAFTED: the S.S. ANNE and its departure, three directions (A THE PACKET, B THE KEY, NO TUNE, C THE LIVERY)
- `397f6615` TODO: T-428 -- the playground's COMPANION tab is exported from the companion's committed HEAD only (playground 6e8ca37)
- `0df91b92` T-519: the third book's covers regenerated -- the night half's tablet mirrored in a still pool, the dawn half's Christmas star, the mended cover holding both on indigo boards (the user, 2026-11-11, by multiple choice; DRAFT; companion 58a98a2)
- `931e716b` T-534 the MUSAI followers BUILT (engine 27a29b6f7): all six forms in all four seasons, 24 looks drawn from the finals (gfx/drafts/t532_musai_seasons/followers/, scripts/draw.py), each vehicle redrawn to read at 1x; tools/gbafollower.py takes them as DRAWN in the form's own palette and tools/gbafollowerpal.py gives those 24 normal.pal and shiny.pal as they stand, so no write reverts them; qa 11Nov2026 T534 84; not released (DRAFT)
- `88a592dd` companion C-334: sleep sounds on roverbyteseer -- a keyed door (:4002, keys checked by LiteLLM) to ACE-Step 1.5, which makes the daemon's piece and hands it back made to loop without a seam (-23 LUFS); nothing kept there after the hub fetches it
- `d859d9f7` Bible v11.349: TULIKKO's sparks and THE UNITY BOOK's torn lines released (T-528 e, T-519, v11.348.2)
- `0f229a30` ROM release v11.348.2: TULIKKO's sparks (T-528 e, the conjugate light alone brings them) and THE UNITY BOOK's torn lines (T-519) (DRAFT)

## The design bible's own entry for v11.349

### v11.349 — 2026-11-11

- **4.40, released in v11.348.2:**
  - **TULIKKO's sparks (T-528 e).** Once the book is mended, sparks rise from the fox's tail on a night of light, in the edition's own colour. The conjugate light brings them on any night by itself, rising green and turning red, which is what the user chose.
  - **The torn lines (T-519).** The book now ends "...It will not be, and it always was. Look again, and you will see them both."
- A Settled entry in section 10. Every word is DRAFT.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
