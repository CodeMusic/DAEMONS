# DAEMONS v11.343.1 — release notes

*Released 2026-11-07 13:04 · built against the design bible v11.343*

- **Engine**: CodeMusic/pokefirered-daemons `d3f239d57` (context-content)
- **Design**: CodeMusic/DAEMONS `2abdf657`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `171c2e3495c45224f2dbe19ce75469e72171a6e3` |
| `daemonsContext.gba` | CONTEXT | `33c4d7d1664515812200d34d515f003da8f32eb8` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `a01a88bf0ad485fbc76d51765ace3ea78532e280` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `512d4fe5a1483da5c1e43c38252ea1f545bdaec6` |

## The engine since v11.342.7

- `d3f239d57` T-527: the battle backgrounds in our own hand -- A OUR PLACE outdoors, B QUIET FIELD indoors (the user, 2026-11-07: "A outdoors, B indoors")

## The design and tools since v11.342.7

- `2abdf657` T-527 built (engine d3f239d57): the battle backgrounds in our own hand -- A outdoors, B indoors (the user, 2026-11-07)
- `b7f7fdd1` T-528, T-529: the aurora (the mended book lights the sky, red in CONTENT, green in CONTEXT, conjugate across the editions) and the mended book's lens (night, whole, dawn on every page) -- 4.40, v11.343 (the user, 2026-11-07, by multiple choice)
- `417b781f` T-527 draft: the battle backgrounds in our own hand -- nine terrains, A OUR PLACE and B QUIET FIELD (nothing in the engine)
- `617d0f13` THE SUBTLE LAYER: 'a USER's handbook' in the player's manual, docs/books and the wiki (the user, 2026-11-07; game and companion in v11.342.7)
- `44848518` ROM release v11.342.7: T-525 item icons batch 3 (57); T-526 26 item descriptions, a USER's handbook, THROTTLE TRAP's row whole

## The design bible's own entry for v11.343

### v11.343 — 2026-11-07

- **4.40, the aurora: the dawn that comes at night (T-528, the user, by multiple choice; brought by the game lane).** Once the book is mended, the light hangs over DAEMON TOWER every night: CONTENT in oxygen's red line, CONTEXT in its green. On some nights (about one in three, picked from the date) it shows beyond the tower, spreading grove by grove, and each mainland grove lights its conjugate grove on the islands. The mainland is the north wind's side and the islands the south's, in both editions. The dawn chorus plays in the groves at dawn after a night of light; TULIKKO, an arctic fox, sweeps the sparks up at STILLFALL CAVE. With a daemon from the other edition in the party the sky shows both lines, green below and red above, and PLAY gains a duet. The names were checked: Galileo's 1619 "boreale aurora", the Sámi guovssahas (its "heard" gloss popular, not settled), the Māori Tahu-nui-a-rangi (kept out of the game), the Finnish revontulet.
- **4.40, the mended book's lens (T-529, the user, by multiple choice).** Once mended, every page of THE UNITY BOOK turns between its night, whole and dawn readings in place, the tone turning with it; L and R in the game, a three-way switch in the companion.
- **Open log**: the aurora, entered and decided the same day.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
