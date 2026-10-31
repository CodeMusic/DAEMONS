# DAEMONS v11.334.1 — release notes

*Released 2026-10-31 16:05 · built against the design bible v11.334*

- **Engine**: CodeMusic/pokefirered-daemons `69d09218c` (context-content)
- **Design**: CodeMusic/DAEMONS `e79b619f`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `fe537679fbdc50a4e30d46439343d77a1de872d3` |
| `daemonsContext.gba` | CONTEXT | `ff1697fc8140e6f818d8d9530983e275547e46c1` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `d06ffccbf139421464fb6133e7e341c63a625d26` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `e1733352c74510325980742f3c24281f16174f18` |

## The engine since v11.333.3

- `69d09218c` T-505: the WAREHOUSE's admins are remnants who don't know what happened
- `ca737bf0f` T-503: BRAZEN's gym and THREE ISLAND's spoon-bender read and steer
- `0123e01fa` T-504: MOM's ship line ends when the ship sails; she says DAVID called, once
- `c5e4fc257` T-502: CRYSTAL's last words, in the lab once the eighth MARK is held
- `789ed43f2` T-500: OSRIC HATTER's name on his hat (DRAFT)
- `137062825` README: latest release v11.333.3

## The design and tools since v11.333.3

- `e79b619f` TODO: T-500, T-502..T-505 struck (built; release v11.334.1 next); generator_drift.json: port_dialogue must never --write SaffronGym (T-503)
- `f87256ed` T-502, T-503, T-504: t459d plays CRYSTAL in the lab and MOM after the ship; psychic notes corrected
- `47b1b970` Bible v11.334: the thin half-hour is 3:30 to 3:59 (T-501)
- `36014982` TODO: T-505 -- the admins become remnants (the user)
- `05d2e0aa` TODO: T-506, the third book's gate leaves the public writing (the user, by multiple choice)
- `6bae1e1d` README and wiki: the newest release is v11.333.3 (2026-10-31)
- `bb45443a` TODO: T-483 part 2, the SPELLBOOK, released v11.333.3
- `f818ec4a` manual: rebuilt for v11.333.3
- `414df2e8` ROM release v11.333.3: T-483 part 2 the SPELLBOOK and the gentle spells (AWAKENING, CONTRAST, PATTERN, LENS, FIELD); T-494 the card's line is the user's (all DRAFT)

## The design bible's own entry for v11.334

### v11.334 — 2026-10-31

- **4.39, the thin half-hour is 3:30 to 3:59 (T-501, the user, by multiple choice).** What is built already makes half past three the moment: OSRIC HATTER's clocks come right and the glitch peaks at :30. THE BOOK OF THIRTEEN's last spell, THE WITCHING HOUR, and the Blank Tablet's thirteenth line move from 3:00-3:30 to 3:30-3:59 to match. Nothing in the ROM changes; neither is built yet (T-483).
- A Settled entry in section 10.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | pret's byte-identical rebuild |
