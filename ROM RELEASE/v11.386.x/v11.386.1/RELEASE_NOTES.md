# DAEMONS v11.386.1 — release notes

*Released 2026-11-17 12:36 · built against the design bible v11.386*

- **Engine**: CodeMusic/pokefirered-daemons `d74da2006` (context-content)
- **Design**: CodeMusic/DAEMONS `e7c5ead6`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `1407920d6784bcc2473d0cb316878c04f097edb7` |
| `daemonsContext.gba` | CONTEXT | `d735805304cd7eb82c13273423e257adf77dcb99` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `ac23b71e59aead3a2c9745dcf86d5d263acc8ba7` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `cc5d45acde6def7f9565096c8bf4ca82061abaf4` |

## The engine since v11.385.1

- `d74da2006` T-565 batch 2: the battle music, ours -- all nine slots in C, the harp and flute over the cartridge as the fanfares: VS_WILD, VS_TRAINER, VS_GYM_LEADER, VS_CHAMPION, VS_LEGEND, VS_MEWTWO (S.T.A.R.R.) and the three victories, over pret's in place on voicegroup195, which gains program 9, a plucked square 1 (the user's pick, DRAFT; DAEMONS tools/genbattlemusic.py)
- `aa19d5924` T-565 batch 4: the 24 battle sounds in C BOTH -- the hit's noise thud, super-effective's chord, faint falling to the tritone, the exp climb (the user's pick, DRAFT; tools/genuisounds.py --batch 4)
- `1cd5e785a` README: the release line names v11.385.1

## The design and tools since v11.385.1

- `e7c5ead6` T-581: tickets.py run bare (or with --write, as check_generators does) is the dry run, exit 0; it writes nothing
- `2fe7c646` T-565 batch 2: tools/genbattlemusic.py, the battle music -- all nine slots in voice C over pret's (engine d74da2006); genfanfares.py's voicegroup195 gains program 9, the arp's plucked square; T-565's row records it
- `281dfbcb` T-581 first slice: tools/tickets.py reads both TODO files into Redmine's payload and rebuilds them byte for byte (dry run, nothing sent)
- `8fba05a5` qa: the Cardputer Zero's GAMES (C-395) and RECEIVED (C-397), seen against a scratch companion
- `a6722737` T-565 batch 4: the battle sounds approved, C BOTH (the user, by ear)
- `1f3c2d8c` T-565 batch 4 drafted: the 24 battle sounds apart from moves in three styles (A TERMINAL, B HARP KEYS, C BOTH), APPROVED_4 empty
- `aff9b32a` qa: C-357's app four as built (PROCESSES, THE MASK, SAME DRIVE, RECOGNITION), on a scratch site (17Nov 1)
- `4c3f8193` T-575..T-580: C-357's game half as the user picked -- TOUCH, MOVE AND BURN, RIPPLES, KINDRED's two cups, a read fixed by the day and the place, the follower turning after the last page (all A, DRAFT)
- `50d686a9` THE COMPANION recorded again from its C-396 sources (friend, 75.5 min): every book's recording current
- `0193e8c1` Bible v11.386: the menu and UI sounds (T-565 batch 1, v11.385.1)
- `94bb6d89` README and wiki Home name v11.385.1
- `df3c0726` ROM release v11.385.1: T-565 batch 1, the 20 menu and UI sounds in C BOTH (DRAFT); C-396's MANUALS table; seals v11.384.x; THE COMPANION recorded after (the user)

## The design bible's own entry for v11.386

### v11.386 — 2026-11-17

- Recorded from release v11.385.1 (df3c0726, engine eeab33eec), which sealed v11.384.x:
  - **The menu and UI sounds** (T-565 batch 1), the user's pick "C Both": 20 sounds, a square click under the harp, the flute for held notes. DRAFT. In 9.5, after the fanfares.
  - Also in the release, outside the bible: THE COMPANION's manual names THE WATCH, THE GLASSES and THE CARDPUTERS (C-396), reprinted.
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
