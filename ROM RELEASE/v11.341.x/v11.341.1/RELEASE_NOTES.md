# DAEMONS v11.341.1 — release notes

*Released 2026-11-05 21:51 · built against the design bible v11.341*

- **Engine**: CodeMusic/pokefirered-daemons `4d40b097f` (context-content)
- **Design**: CodeMusic/DAEMONS `3bc67dcf`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `1b9db3f7126c6402892dceb26b961746f07e3f11` |
| `daemonsContext.gba` | CONTEXT | `6bf64df7e7a017b6bea0312052e3851f529714ee` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `f29ca57445b6c4e5562803329abbf6287a3787d9` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `bba401b5a91464c383215d73c2dca1d92a998881` |

## The engine since v11.340.3

- `4d40b097f` T-519: the third book's drawn art -- THE HERMETIC LAYER, THE EUDAIMON LAYER and THE UNITY BOOK each get the user's chosen cover (night V4, dawn V2, mended V2), a drawn frontispiece, the five opening-section pictures (handturning in two frames) and a drawn bag icon; every later entry shows its book's frontispiece until its own is drawn. The dawn half's boards are sapphire (C_SLATE, C_CHALK_FAINT, cover and icon only), and the night half's pictures keep C_EDGE_DARK apart from the breathed backdrop. Written by DAEMONS tools/gensubtle.py. DRAFT

## The design and tools since v11.340.3

- `3bc67dcf` TODO: T-519 the third book's art built (engine 4d40b097f)
- `92c987ba` qa: T-519 THE HERMETIC LAYER's drawn art, filmed (cover, WARNING, the frontispiece)
- `5a3eb6a0` T-522: every daemon's telling written -- 397 in docs/index-spoken.md, MISSINGNO has none (DRAFT)
- `f3c51c23` tools: gensubtle writes the third book's drawn art -- the chosen covers (bundled in tools/thirdbook_covers/), frontispieces, opening pictures and icons from thirdbook_art; the dawn half's boards sapphire (T-519, engine 4d40b097f)
- `6548bfdb` TODO: T-519 the books' art, the user's picks (night V4, dawn V2, mended V2)
- `68a5b7ac` T-519: THE UNITY BOOK approved as drafted (the user, 2026-11-05, after the three readings side by side)
- `4f708624` T-522: each daemon tells of itself, in the companion only -- 154 tellings, bible v11.341 (DRAFT)
- `c098565d` TODO: T-522 claimed -- each daemon's first-person telling, companion only (WIP)
- `be6b7d87` tools: thirdbook_art.py, draft covers, icons and pictures for the third book's three forms (T-519)
- `8553aa59` ROM release v11.340.3: the mended town vivid in THE CREATOR'S HOUR, and THE UNITY BOOK's cards (T-519, DRAFT)

## The design bible's own entry for v11.341

### v11.341 — 2026-11-05

- **4.2, the record says it and the daemon says I (T-522, the user, by multiple choice: "App only, spoken").** The game's INDEX stays in the third person: it is the instrument, and an entry that says "I" would hold the thing 4.2 says it cannot. In the companion, on its own page, a daemon tells of itself in its own voice (C-303, C-251): one telling per daemon, the same in both editions, written in `docs/index-spoken.md` and never built into a ROM. A telling says only what the daemon could know from inside, names no feeling, does not know there is a record, and does not accuse whoever carries it. MISSINGNO has none. Every word DRAFT.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
