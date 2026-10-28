# DAEMONS v11.316.6 — release notes

*Released 2026-10-28 17:15 · built against the design bible v11.316*

- **Engine**: CodeMusic/pokefirered-daemons `be3388f75` (context-content)
- **Design**: CodeMusic/DAEMONS `0d93bab5`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `861dd0d7fe64a3bc274a835e98fd727bdca96b91` |
| `daemonsContext.gba` | CONTEXT | `737e2285f949177cabd99fa562bc0eb5e7815d67` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `7717fd41679819eaceb1743757594fbdf5863644` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `94bca16cd32ee110c9d5383c0a96c70824515e41` |

## The engine since v11.316.5

- `be3388f75` T-452 batch 18: OVERLOADED's art into CASTFORM's normal form -- the build makes castform/front.4bpp, back.4bpp and the palettes by joining normal/, sunny/, rainy/ and snowy/ (graphics_file_rules.mk), so castform/front.png (what gbasprite writes) never reached the ROM and OVERLOADED drew as vanilla's normal form; the written front, back and palettes copied into normal/. The sunny, rainy and snowy forms are still vanilla's.
- `b9b2dc5eb` T-452 batch 18: REDACTED to EPIPHANY (376-397, 22) in the new style, on the RECOMMENDED choices -- hand-drawn keys (REDACTED's black bar over its eyes, SUBTEXT's zipped mouth and a stitch line, FORGERY's pen-nib tail tip, PRISTINE's monocle, OVERLOADED's sun, snowflake and raindrop, SYN's and ACK's cyan tail lights, MENTALIZE's chest gem), the type-hue trap fixed (STEEL, NORMAL, ROCK, PSYCHIC, DRAGON greyed into the ramp; the sun pale, the lights and gem cyan), backs the front mirrored with the face out, grounds and a frame off; grounding rows, icon palettes, follower art and palettes
- `7e6f68651` README and wiki: the player's manual near the top (DAEMONS docs/DAEMONS-manual.pdf); latest release v11.316.5; about 349 daemons in the new style

## The design and tools since v11.316.5

- `0d93bab5` TODO: T-452 batch 18 -- OVERLOADED (CASTFORM) never reached the ROM; its normal form now carries the art (engine be3388f75), its three weather forms a question
- `ecfc38f4` TODO: T-452 batch 18 built (engine b9b2dc5eb): 376-397 on the RECOMMENDED choices; questions in gfx/drafts/t452/w/questions.md
- `7ba16d52` T-452 batch 18 built (engine b9b2dc5eb): REDACTED to EPIPHANY (376-397, 22), on the RECOMMENDED choices (2026-10-28); drafts in gfx/drafts/t452/w, questions in w/questions.md (26 items), remaining.md (14 left, one batch) -- hand-drawn keys (REDACTED's black bar, SUBTEXT's zipped mouth, FORGERY's pen-nib tail, PRISTINE's monocle, OVERLOADED's sun, snowflake and raindrop, SYN's and ACK's tail lights, MENTALIZE's chest gem), the type-hue trap fixed, backs the front mirrored with the face out, grounds and a frame off; scripts batch18.py, chain18.sh, prep18.py, hand_b18.py, recolour18.py, icons18.py, ba18.py, ba18.sh, view18.py, grid18.py, grp18.py, build18.py and the batch 18 subjects
- `35b7de3f` TODO: T-452 -- the user: MISSINGNO keeps its question marks; SYMBOL's 28 forms redrawn
- `e5b2f47a` README and wiki: the player's manual near the start, and from the wiki's home, PLAYING and sidebar; trading between players through the companion (T-473); v11.316.5; about 349 daemons in the new style (engine README and wiki 'player's manual', playground too)
- `b55d7dc2` qa: T-452 batch 17 sheets (v11.316.5)
- `2b505737` manual: rebuilt for v11.316.5
- `86427668` ROM release v11.316.5: T-452 batch 17 (HONEYTRAP to SHALLOWS) on the recommended choices

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
