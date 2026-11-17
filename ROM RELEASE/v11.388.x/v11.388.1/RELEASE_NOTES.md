# DAEMONS v11.388.1 — release notes

*Released 2026-11-17 17:51 · built against the design bible v11.388*

- **Engine**: CodeMusic/pokefirered-daemons `8fc425637` (context-content)
- **Design**: CodeMusic/DAEMONS `0a47a2ac`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `3e0d3af861ccd0ecfa2045a553dfd25be04e5967` |
| `daemonsContext.gba` | CONTEXT | `8948a6c8261222ba106a98d1709f7df635089d07` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `24cd3661e3742e8ddeeb232515eb9e5937e8d690` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `6ab2d11a5941bbb28907ef05331e7d39b200368c` |

## The engine since v11.387.1

- `8fc425637` T-565 batch 6: the 41 field sounds in C BOTH -- doors as a noise thud under a short square, rain as small noise ticks with harp drips, thunder rolling down the noise keys, warps and the PIN in the pentatonic (the user's pick, DRAFT; tools/genuisounds.py --batch 6)
- `586ed7e8b` T-565 batch 8: the story set-pieces, ours, in C (the harp and flute over the cartridge) -- CRYSTAL CLEAR's entrance (her Lament over the lament bass), her lab (her Reply), the new game's two, AL CLEAR's two (his champion figure), a leader's summons, the S.S. ANNE's waltz, the hideout, DAEMON TOWER, THE UMBRAL ASCENT, TRAINER TOWER, THE RECORD, BLANCHE slowed and the credits (a medley, her Lament to her Reply), over pret's in place; THE WALLED GARDEN's own song in an appended slot, MUS_WALLED_GARDEN 388, its nine maps re-pointed from MUS_EVOLUTION; DEBUG SOUND reaches it (the user's pick, DRAFT; DAEMONS tools/genstorymusic.py, port_music.py's MAP_MUSIC)
- `264705bd8` README: the release line names v11.387.1

## The design and tools since v11.387.1

- `0a47a2ac` T-565 batch 6: the field sounds approved, C BOTH (the user, by ear); the two batch-10 sketches stay out
- `d8a1bd00` T-565 batch 8: tools/genstorymusic.py, the story set-pieces in voice C (engine 586ed7e8b); port_music.py points THE WALLED GARDEN's nine maps at its own song; song-status.md records it (T-565's note is in Redmine)
- `10e73cff` T-581: no hand edit is lost after the cut-over -- the nightly carries any ticket row changed by hand since its last mirror into Redmine before mirroring (carry, mirror --save); sync --only
- `1b360437` T-581 closed in Redmine with its commits; T-582 opened (goal loops plan into Redmine) -- the first mirror written from Redmine
- `afa2df22` T-565 batch 6 drafted: the field sounds in three styles (genuisounds.py --batch 6; DRAFT)
- `f9fd168f` T-581: the tickets live in Redmine now -- the TODO files are its nightly mirror; sessions work as their lane through tools/tickets.py (mine, claim, new, close); the WIP mark and reserved id blocks are retired (the user, 2026-11-17: "Apply and switch")
- `71b78d27` T-581: ready for the cut-over -- tickets.py new (the next id, safe when sessions race: three at once got T-582..T-584), sync --create-only so a hand-written row becomes a ticket, check_todo.py checks the mirror once Redmine is the truth
- `d34f5b97` T-581: lanes in Redmine -- tickets.py --lane with show, mine, assign, and claim/close for after the cut-over; the nightly waits out a release; tools/redmine_lanes.rb (the eleven lane users)
- `5208ffde` Bible v11.388: THE SUBTLE LAYER's six scenes and the overworld music (T-575..T-580, T-565 batch 5, v11.387.1); 7.4's LURID and DOLDRUM rows
- `c9ea9430` README and wiki Home name v11.387.1
- `04363c24` ROM release v11.387.1: T-575..T-580 THE SUBTLE LAYER's six scenes (TOUCH, MOVE AND BURN, RIPPLES, KINDRED's two cups, a read fixed, the follower turns; DRAFT) and T-565 batch 5, the overworld music in C (MUS_DOLDRUM, MUS_LURID; the Musical Instruments lane's); seals v11.386.x

## The design bible's own entry for v11.388

### v11.388 — 2026-11-17

- Recorded from release v11.387.1 (04363c24, engine ed754fb57 and 410682153), which sealed v11.386.x:
  - **THE SUBTLE LAYER's six scenes** (T-575 to T-580, C-357's game half), the user's picks, all A, confirmed "keep as built": TOUCH, MOVE AND BURN, RIPPLES, KINDRED's two cups, a read fixed by the day and the place, the follower turning after the last page. DRAFT. In 4.38, after the three pages of T-548 to T-550.
  - **The overworld music** (T-565 batch 5, the Musical Instruments lane): the everyday roads, gatehouses, cycling and surfing in voice C; **LURID and DOLDRUM split from `MUS_FUCHSIA`**. DRAFT. 7.4's table no longer says the two share `Cities2` on the GBA, and a paragraph says so.
  - Also in the release, outside the bible: T-581, the tickets in Redmine (sync, mirror, export, a nightly job).
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
