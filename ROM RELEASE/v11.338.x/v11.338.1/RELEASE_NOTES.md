# DAEMONS v11.338.1 — release notes

*Released 2026-11-04 17:01 · built against the design bible v11.338*

- **Engine**: CodeMusic/pokefirered-daemons `f4bbae9f3` (context-content)
- **Design**: CodeMusic/DAEMONS `f4c717a3`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `735d4bba76aa7e974c7a6aa12db0e3ae526a2176` |
| `daemonsContext.gba` | CONTEXT | `98df3ec66dcc2dee3edc953d0997cd0d1973da8b` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `de881478ee854c6c28013c5b30ba92cf1aee1358` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `f6c8dc312e179629ab513f1ca8851d02e57fa388` |

## The engine since v11.337.4

- `f4bbae9f3` T-519 item 1: SPIRITS -- the refusal waits for A, as vanilla's "It won't have any effect." does (the party menu closed at once)
- `36f61046f` T-519 item 1: SPIRITS -- every daemon drifts between good spirits, as it is, and low spirits (DRAFT)
- `b30ee6d09` T-519 item 4: the catch-up begins on a CONTINUE with a recap too; the creator's hour's gold warmer, its motes given a palette
- `96a09f669` T-519 item 4: THE CREATOR'S HOUR reads as early dawn, not night -- the light eased toward dawn, more gold, gold motes
- `f710d2273` T-519 item 4: THE CREATOR'S HOUR's gold breath on the clock, as the companion's (C-237's rule)
- `9439a80e3` T-519 item 4 (3/3): the LARK by DAEMON TOWER in HALFTONE, and the hint (DRAFT)
- `66c67abed` T-519 item 4 (2/3): THE CREATOR'S HOUR -- light, not noise, every early morning
- `3ec8bf2b2` T-519 item 4 (1/3): the catch-up -- an hour's effects ease in when play begins inside it
- `6b99785d1` README and wiki: PRINCIPLES OF MIND (DAEMONS docs/DAEMONS-textbook.pdf, T-520), CALLOW SCHOOL's TEXTBOOK as a university textbook, beside THE OLD WORD

## The design and tools since v11.337.4

- `f4c717a3` TODO: T-519 the two hours and SPIRITS (engine 3ec8bf2b2..f4bbae9f3)
- `637c4259` companion_export: SPIRITS' class and lean bits in save_layout's trade block (T-519)
- `2aedd65d` qa: T-519 item 4 filmed -- THE CREATOR'S HOUR rising, at full, resolving, and the LARK; the route's reload and its finish step
- `c832e82f` T-519 item 1: SPIRITS filmed -- all six stops pass; the route plays out the load's dream first; six sheets filed
- `4e614d1e` T-519: THE EUDAIMON LAYER approved as drafted (the user, 2026-11-04); companion_export writes it as eudaimon.json
- `cba570c9` T-519 item 1: SPIRITS -- the route to film it (not yet run), and companion_export leaves its DEBUG page out
- `5db1cc34` T-519 item 4: the hint moves to HALFTONE's LARK by DAEMON TOWER (the user, 2026-11-04) -- its map sheet, and the route's last stop
- `bc313ded` TODO: T-519 the creator's hour's hint is the LARK near DAEMON TOWER (the user)
- `feef41df` companion_export: THE LOG's Saturday line for the companion (T-516 S1)
- `7fbdbb73` TODO: T-519 -- 11 sections fit the mended book, the hint is the LARK's, the companion's hours live (C-295)
- `6337e9bb` T-519 item 4: tools/routes/t519_hours.json (the two hours' film, not yet run: the theatre was down), and BLANCHE TOWN's baker on the map sheet
- `4eabd949` qa: C-295 / T-519, the creator's hour in the companion's den
- `ee4e448a` T-519: THE EUDAIMON LAYER, the dawn half, DRAFT -- the night half's ten sections read from the other side, the blessing, the gift-side spells, the observer's line
- `16509388` TODO: T-519 the creator's hour's hint, an early baker in BLANCHE TOWN (the user, by multiple choice)
- `3dfd6efb` CLAUDE.md: the companion's LAYOUT.md, read before adding or moving code there (companion C-292)
- `036d765e` qa: T-518 / companion C-277, LISTEN inside the books on the site
- `9f38dfbb` TODO: T-518 -- PRINCIPLES OF MIND read aloud (a5ae6299), and every recording plays inside its book (companion C-277)
- `a5ae6299` T-518: PRINCIPLES OF MIND read aloud by a professor; the sealed recording kept, not deflated, so the companion opens it
- `d3cac8d6` Fourth Review's words as docs/daemons-review-4.md beside the first three; press kit and social cards move to docs/marketing/
- `3ceb594b` The Fourth Review (v11.338): the game, the companion and its local AI read as one product; press kit and social cards beside it
- `aca909e4` Press kit (DRAFT) and tools/reviewpdf.py: the Fourth Review's companion PDF, twelve social cards as PNGs; review folder started
- `1f9f03cb` README and wiki: PRINCIPLES OF MIND (DAEMONS docs/DAEMONS-textbook.pdf, T-520), CALLOW SCHOOL's TEXTBOOK as a university textbook, beside THE OLD WORD
- `82fd8059` qa: T-520/C-276's two pictures
- `1728b55a` qa: T-520/C-276, PRINCIPLES OF MIND in the companion's CALLOW SCHOOL
- `da83c16c` TODO: T-520 PRINCIPLES OF MIND done (6c48adc9)
- `6c48adc9` T-520: CALLOW SCHOOL's TEXTBOOK as a university textbook -- PRINCIPLES OF MIND, An Introduction in Seven Floors
- `3e90682c` TODO: T-520 claimed -- CALLOW SCHOOL's TEXTBOOK as a real university textbook (the user, 2026-11-03)
- `d6bde063` TODO: T-519 -- the three contents approved (dawn titles mirrored, the Work backwards, Good Spell, the whole book plain)
- `44eb7fdb` v11.338: 4.40 THE UNITY BOOK -- the third book torn at the spine (night half, dawn half), mended at DAEMON TOWER with BALANCE; SPIRITS; DAEMONS said DAY-mons; T-519 filed
- `0a3a27d4` ROM release v11.337.4: T-513 Ty's 'Not yet.' and T-516 THE SUBTLE LAYER's four practices

## The design bible's own entry for v11.338

### v11.338 — 2026-11-02

- **4.40 THE UNITY BOOK (T-519, the user).** The third book is torn at the spine into THE HERMETIC LAYER and THE EUDAIMON LAYER. They are one book, read from the night side and the dawn side, opening with a warning, a blessing and an attestation. The thirteen spells are the same in both, and the dawn page names each cost as a gift. Only the thirteenth differs: THE WITCHING HOUR, THE CREATOR'S HOUR, THE HORIZON. The halves are mended at DAEMON TOWER, and BALANCE is written between them. OSRIC HATTER read the night half; a LARK read the dawn half.
- **4.40 SPIRITS.** Every daemon drifts between EUDAIMON, DAEMON and KAKODAIMON (in good spirits, as it is, in low spirits), nudged by four kinds of event (KEPT, BOND, WORK, PORTION) and stored in 4 bits. It shows in tone, never hue, with an evolution-like screen at each crossing.
- **Reversed: HALFTONE's town comes back into colour** once the book is mended, and greys again only in the night's hour.
- **1, said DAY-mons.** The frightening word is never written anywhere a reader sees, and whatever is spoken is respelled daymon(s) first (C-270).
- **0.1's exception** now names the torn book, not the gate. 4.39 points to 4.40.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
