# DAEMONS v11.376.1 — release notes

*Released 2026-11-16 10:33 · built against the design bible v11.376*

- **Engine**: CodeMusic/pokefirered-daemons `31adf3c19` (context-content)
- **Design**: CodeMusic/DAEMONS `14dc63c0`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `4c0774bf750a33f5aa2d166765bd3b3f4e045622` |
| `daemonsContext.gba` | CONTEXT | `0caf1ce9079ba991b7e1fbcc5bd047b0bd3f5612` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `96caa28b018d2bdb4186fe19bc9703b6d6c39ffc` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `9edcf96452b95b1e684eb2506d4d44e14a6710a6` |

## The engine since v11.375.1

- `31adf3c19` T-571: THE SUBTLE LAYER from its source -- USERS, and THE CONTAINER's last page back to three lines (two DRAFT words, The Subtle Layer's)
- `66503658b` README: the release line names v11.375.1

## The design and tools since v11.375.1

- `14dc63c0` T-570 drafted: the islands' and caves' last tiles drawn as shapes -- ladders, holes, slide ice, the rest (gbaislands.py --t570, A/B/C per kind, APPROVED_570 empty; nothing in the engine)
- `3f880958` qa: C-380 the Cardputer Zero's save reaching a scratch companion by itself
- `dbe657cb` qa: C-377 the Cardputer Zero program on the Mac -- the game made and played 1:1, HOME, MAKE THE GAME
- `05cd9260` Manuals: the game's own words after T-571 -- a trainer is a USER, the trainer card the USER CARD, the bag the POOL, the PC the PORT (PLAYER'S MANUAL, PLAYING TOGETHER, THE COMPANION); reprinted
- `864bd2c9` T-571: THE SUBTLE LAYER's source says USER, as engine 45cae5c3d's header does; THE CONTAINER gains "between them" (DRAFT) so its last page keeps three lines
- `c6432e77` Bible v11.376: the game's own words in newer writing (T-571, v11.375.1)
- `196851c7` T-571: the three layer books' sources say USER/USERS and POOL, as engine 45cae5c3d's headers do
- `7ae19bd6` README and wiki Home name v11.375.1
- `32bfa05e` ROM release v11.375.1: T-571 the game's own words in newer writing -- trainer is USER in the four books and the spellbook, POOL, PORT, DETACH, a bind; port_vocab guarded; seals v11.374.x; two recordings deferred

## The design bible's own entry for v11.376

### v11.376 — 2026-11-15

- Recorded from release v11.375.1 (32bfa05e, engine 45cae5c3d), which sealed v11.374.x:
  - **The game's own words in newer writing** (T-571), the user's ruling: USER, POOL, PORT, DETACH and bind applied by hand; stage names and idioms kept; port_vocab guarded. DRAFT. In 1.6, after its two habits.
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
