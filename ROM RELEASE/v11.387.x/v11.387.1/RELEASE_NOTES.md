# DAEMONS v11.387.1 — release notes

*Released 2026-11-17 15:29 · built against the design bible v11.387*

- **Engine**: CodeMusic/pokefirered-daemons `ed754fb57` (context-content)
- **Design**: CodeMusic/DAEMONS `1c1b021c`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `2e92ba8de2c6e3664105345c97e444cc547dea67` |
| `daemonsContext.gba` | CONTEXT | `960f6fc97e10bf366056e44e0ebebe894a530441` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `33f4ddc6ad7c720c943347fb997d53ef3f1fdd7f` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `5b83eb90395b840b37a5bcc74839d6b13f65d08e` |

## The engine since v11.386.1

- `ed754fb57` T-578: KINDRED, the two cups -- with THE SUBTLE LAYER held, a badger in CELADON's condominiums (the TEA woman's room) pours two cups from one pot, hands the player one and goes with the other; the player drinks theirs. In LAVENDER TOWN the badger already knows: "You had the TEA. / I tasted water." FLAG_KINDRED_POURED, the badger's two hide flags set by each map's ON_TRANSITION. The user's pick A; the places and every word DRAFT.
- `2e3c8d00c` T-576: MOVE AND BURN -- at high VOLTAGE (4, as just after a party HALT) a WRITE (a CONTEXT routine with power that would land harder) now and then (25%) lands without an address: it misses, and the box says "Something moved. / Not the thing you meant." in the lean's purple; an ENTROPY lead at high VOLTAGE raises every routine's chance to burn by 10 points, on both sides of the field. The type chart untouched. gBattleStruct's last pad byte is noAddress. The user's pick A; the rates and the words DRAFT.
- `410682153` T-565 batch 5: the everyday overworld music, ours, in C (the harp and flute over the cartridge, as the fanfares and battle music) -- the main road, the coast road, Routes 24-25, the CHECKPOINT, the BENCHMARK, the gatehouses, THE UNDERTONE, cycling and surfing over pret's in place; and LURID and DOLDRUM split from MUS_FUCHSIA as vision 7.4 planned: MUS_DOLDRUM 386 (Poly and Fields) and MUS_LURID 387 (ScornSolutions Blues), their 14 maps re-pointed; DEBUG SOUND reaches MUS_LURID (the user's pick, DRAFT; DAEMONS tools/genoverworldmusic.py, port_music.py's MAP_MUSIC)
- `99ee830f0` T-575: TOUCH -- (1) a gift a person hands over (Std_ObtainItem), with a STRATUM daemon following, now and then brings "A read: this was held a long time / before it was given." (33%, fixed by the day, the place and the item); (2) a LATENT daemon following, once a night, the first step into DAEMON TOWER or the burned mansion: "A read: rain on stone. / It is dry in here." Both kept in THE LOG as TOUCH. The user's pick A; the places, the rate and every word DRAFT.
- `41bb1c6c9` T-577: RIPPLES -- at a still pond (VIRIDIAN CITY's, CELADON CITY's, ROUTE 22's: pond water under the two of them), stand ten seconds side by side with the follower and two rings spread from the two reflections and meet; then "A read: two ripples, one pond. / Where is the line?", kept in THE LOG (Daemons_GiveRead). The rings are the noticing's own ripple, scaled. The user's pick A; the ponds and every word DRAFT.
- `e574937ba` T-579: a read cannot be taken again -- every draw a read makes comes from its own generator seeded from the day and the map, so a reloaded save walks into the same read, true or not, in the same words; the same read twice running is kept once in THE LOG (the user's pick A, DRAFT). No words.
- `7ef7c1750` T-580: THE SUBTLE LAYER's last word -- after its LAST WORD page in the reader, back in the field the follower looks away a beat and turns to face the player; straight above or below, the turn is the flip (the user's pick A, DRAFT). No words.
- `81151f749` README: the release line names v11.386.1

## The design and tools since v11.386.1

- `1c1b021c` TODO: T-575..T-580 the SUBTLE LAYER's six scenes, confirmed as built (the user)
- `aaacb718` T-578 BUILT (engine ed754fb57): KINDRED, the two cups -- the route, the sheets, the row
- `a7df0394` T-576 BUILT (engine 2e3c8d00c): MOVE AND BURN, no address at high VOLTAGE -- the route, the sheets, the row
- `05433bda` qa: T-565 batch 5's overworld music as built, the sheet sent with the push (17Nov 20)
- `8d505ced` Tickets nightly 2026-11-17: the Redmine export (T-581)
- `ff55f6d1` T-565 batch 5: tools/genoverworldmusic.py, the everyday overworld music in voice C (engine 410682153); port_music.py points DOLDRUM's and LURID's maps at their own songs and no longer restores mus_pewter; song-status.md and T-565's row record it
- `d2da2dfa` T-575 BUILT (engine 99ee830f0): TOUCH, a gift's read and rain on stone -- the route, the sheets, the row
- `6ff940f9` T-581: the tickets in Redmine -- sync (files to Redmine, never deletes), mirror --from-redmine (refuses any lost ticket), export (every ticket's history for git), the Redmine set-up, and the nightly job that pushes the export
- `94965f39` T-577 BUILT (engine 41bb1c6c9): RIPPLES, two rings at a still pond -- the route, the sheets, the row
- `ea3a5450` T-579 BUILT (engine e574937ba): a read fixed by the day and the place -- the route, the sheets, the row
- `b92e4886` T-580 BUILT (engine 7ef7c1750): the follower turns after THE SUBTLE LAYER's LAST WORD -- the route, the sheet, the row
- `4e2de54b` Bible v11.387: the battle music and the battle sounds (T-565 batches 2 and 4, v11.386.1)
- `1bdc607e` qa: T-565 batch 2's battle music as built, the sheet sent with the push (17Nov 5)
- `be2ddc72` README and wiki Home name v11.386.1: every battle has music of its own
- `8995d388` ROM release v11.386.1: T-565 batch 2, the battle music -- all nine slots in C, the harp and flute over the cartridge as the fanfares (DRAFT); T-565 batch 4: the 24 battle sounds in C BOTH (DRAFT); seals v11.385.x

## The design bible's own entry for v11.387

### v11.387 — 2026-11-17

- Recorded from release v11.386.1 (8995d388, engine d74da2006 and aa19d5924), which sealed v11.385.x:
  - **The battle music** (T-565 batch 2, the Musical Instruments lane): all nine slots in voice C, over pret's in place. DRAFT.
  - **The battle sounds** (T-565 batch 4, the game lane): 24 sounds apart from moves, C BOTH. DRAFT. Both in 9.5, after the menus.
  - Also in the release, outside the bible: T-575 to T-580 filed (C-357's game half, the user's picks); T-581's first slice (tickets.py, a dry run); THE COMPANION recorded again.
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
