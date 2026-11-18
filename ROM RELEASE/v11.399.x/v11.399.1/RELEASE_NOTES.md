# DAEMONS v11.399.1 — release notes

*Released 2026-11-18 12:03 · built against the design bible v11.399*

- **Engine**: CodeMusic/pokefirered-daemons `08fcde731` (context-content)
- **Design**: CodeMusic/DAEMONS `151bdf65`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `9d2ecc4df187399347fc7f009871d30c69d842e7` |
| `daemonsContext.gba` | CONTEXT | `1f2f4cc2757e35ba842bc756b1ea7c75c8455478` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `33353408d3ab104568980fbf012c1a9ead4b888a` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `b019055fa5735eb589eafe05b4574a6565205f5d` |

## The engine since v11.398.1

- `08fcde731` T-589: the stat arrow by type (DRAFT) -- B_ANIM_STATS_CHANGE's high byte carries the causing move's type + 1 (StatArrowCause at SetMoveEffect's stat cases, setgraphicalstatchangevalues, playstatchangeanimation; 0 for Intimidate, Speed Boost, berries); General_StatsChange plays roles RISE, RISE2, FALL through playtypesewithpan, CONTENT's sound when no move caused it
- `679bad280` README: latest is v11.398.1

## The design and tools since v11.398.1

- `151bdf65` TODO: Redmine's mirror (T-589 closed, pokefirered-daemons@08fcde731)
- `1d19d10a` TODO: Redmine's mirror (T-591 opened)
- `d0f937a1` T-589: the stat arrow by type (engine pokefirered-daemons@08fcde731, DRAFT) -- genuisounds' ROLES_10 gains RISE, RISE2, FALL (only General_StatsChange, capped at 30 frames, rise never borrows a fall); genanims --type-sounds and genstates emit the role lines
- `dfbe7d27` Book audio: THE GLASSES (11.7 min, near) and THE PLAYER'S MANUAL (55.9 min, adventure) read whole after T-590, THE CARDPUTERS (26.6 min, tinkerer) after C-398's reprint -- the user: "Record them now"; every recording current
- `186040ad` T-531: the day symbol drawn for a build (DRAFT) -- tools/gendaysymbol.py draws the seven, ring and horizon, from the paths approved 2026-11-08 into the companion's server/data/art/daysymbol (light and dark pages); DREAMS shows each dream's day symbol (companion C-407 faeb7265); qa 18Nov2026 T531 23
- `a49867b7` TODO mirror: C-328 closed (and T-590 from Redmine)
- `085650c9` qa C-328: a battle between two players, seen on the site at phone width -- the request from another companion, a turn, ROVER outscored KIT! and the experience
- `98c07ef7` T-590: bookaudio says the first row of a table with an empty header -- only a line with dashes is the separator, so THE GLASSES' 'a tap' and nine of THE PLAYER'S MANUAL's tables are read whole; both recordings now behind (no other book moved)
- `f15974d7` README and wiki: THE COMPANION is 76 pages, THE CARDPUTERS 24
- `6961839f` C-398: THE CARDPUTERS caught up with the Zero's first days (24 pages, DRAFT) -- GAMES (C-395) in place of MAKE THE GAME and NEW RELEASE, both editions and their TESTING builds; the one save (C-397); a daemon sent from the game and RECEIVED; the install as measured (17 minutes, about five after); 2.4 GHz Wi-Fi only; more than twice the speed the game needs; M5Stack's own cap apps; shut down in software before the slide switch. The keys and the sound stay not yet seen. Two new screens from qa 17Nov2026
- `6162f209` TODO mirror: T-565 closed in Redmine with both lanes' commits (all twelve batches released)
- `faf2b04c` Sound census: the move sounds still pret's are fourteen, two of them battle's on purpose
- `5738a57a` Sound census brought current: the twelve T-565 batches, where each was released, and the 23 songs and 43 sounds still pret's
- `c4517102` engine.md trap 45: a fresh clone compared with a build that was not this commit's -- check_fresh_clone's DIFFERS after a peer's engine push was this machine's stale ROM (T-565); CLAUDE.md counts forty-five
- `4ae5dd1a` qa: C-358, a DAEMONS sleep piece's .imedx opened and played in PulseEntrain
- `d2fb9511` T-581: the nightly's carry takes only real hand edits -- a row that matches Redmine is a session's own mirror, not an edit; a carried edit keeps the ticket's place
- `e422444d` TODO: Redmine's mirror (a new ticket: the stat arrow by type)
- `07bfb313` Tickets nightly 2026-11-18: the Redmine export (T-581)
- `d9dd5252` TODO: Redmine's mirror (T-588 closed, DAEMONS@8bb6ee46)
- `8bb6ee46` T-588: check_generators --writes' five new drifts settled -- gencries' voice() makes the harp/flute samples with wav2agb -b (the sandbox had no gitignored .bin, so every cry drifted; no cry changes); gentowns keeps T-578's KINDRED badger; gbacivictown's drift entry names celadon_city's later redraws (T-438 F, T-562, T-573); gbatowns out of generator_drift.json; engine.md and sprites.md tables current
- `fe8f0958` TODO: Redmine's mirror (a new ticket: check_generators --writes' five new drifts)
- `8e93c66c` Bible v11.399: the shared move sounds by type, the sound census closed (T-583, v11.398.1)
- `4c6f3540` qa: T-583 each type's own move sounds (v11.398.1)
- `e020dee8` README, wiki: the newest release is v11.398.1
- `90849e70` ROM release v11.398.1: T-583 shared move sounds true to each type (DRAFT); seals v11.397.x

## The design bible's own entry for v11.399

### v11.399 — 2026-11-18

- Recorded from release v11.398.1 (4c6f3540, engine 8a6d96dc8), which sealed v11.397.x:
  - **The shared move sounds by type** (T-583): the three shared sounds play each type's own. DRAFT. In 9.5.
  - **The sound census is closed** (T-565, from 2026-11-16): every song, sound effect, cry and instrument the game plays is the project's own. 9.5 says so.
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
