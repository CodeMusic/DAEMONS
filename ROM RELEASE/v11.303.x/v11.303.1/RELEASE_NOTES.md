# DAEMONS v11.303.1 — release notes

*Released 2026-10-18 03:17 · built against the design bible v11.303*

- **Engine**: CodeMusic/pokefirered-daemons `45deb9ca3` (context-content)
- **Design**: CodeMusic/DAEMONS `210f2fca`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `09347cf8542c073e3dca3a6f2567a5c732c9ab9b` |
| `daemonsContext.gba` | CONTEXT | `8ab56bd60e4fa7f9a9f4c4613a9897a58c45d845` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `0c2d050b291ccba8e5f6c2093e83a07cae06dd9c` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `bf98b19ea23afab108cddf385217ebd670f0d1fc` |

## The engine since v11.302.4

- `45deb9ca3` T-417 P5 (the user, 2026-10-17): the ghosts, the gold join, the echo during the event, THE NEXUS kept lit (DRAFT)

## The design and tools since v11.302.4

- `210f2fca` TODO: T-417 P5 built (engine 45deb9ca3, engineAi c57230a) -- ghosts, the gold join, the echo during the event, THE NEXUS kept lit; every song and CONTEXT's FLUTE played in the theatre
- `f72087c0` TODO: T-417 -- BREATHVERSE, its palm on Route 2, the FLUTE beside the palm inside, rocks out of view (the user)
- `bfeb45e8` qa: C-149 -- the CASINO on the T-Watch S3; C-154 a word from another board as a notification
- `03f8e09a` qa: C-71 -- the T-Watch S3's face after the screen fix
- `3f8032b7` TODO: T-417 -- CONTEXT's FLUTE moves to a new island grove near CALLOW (the user)
- `264dd7f7` genholidays --companion: steps_off as the real name of the holiday it steps off (C-149's Row)
- `f35f747b` T-416 prepared: docs/holidays.json, the single source, and tools/genholidays.py (report; --write not yet run); the user's four answers applied
- `da1eae4c` TODO: T-416 prepared; the user's four answers
- `44023b97` qa: C-151 -- the CASINO's table on the T-Deck and the CC1101: a word, a jackpot called out and cheered
- `ff67309f` qa: C-151 -- the CASINO's table, first run on the T-Deck and the T-Embed
- `16f0ee0b` TODO: T-416 next after PLAY (the user)
- `1da34574` Bible v11.303: 3.5 PLAY, an instrument and a SONGBOOK (T-417); the groves' music (T-408)
- `40f0ee86` TODO: T-417 P4 released; the user's answers on the gate and the rhythm
- `d10fc9e8` companion_export: notebook.json's key_colours and outline, from genplaynotes (T-417)
- `dd317a30` qa: T-417 P4
- `5ed61f8f` ROM release v11.302.4: PLAY P4 -- the seven songs heard and learned (T-417); each grove its own music (T-408)

## The design bible's own entry for v11.303

### v11.303 — 2026-10-18

### PLAY, and the groves' music (T-417, T-408)

- ***3.5, new (the user)***: **an instrument and a SONGBOOK** -- *CONTENT's HARP from a LYREBIRD at CALLOW SCHOOL, CONTEXT's FLUTE under a palm on FINDERS BEACH; the band's sheet gives the key, then you play; a song counts only in its own key, with "Close" for the right shape in the wrong one; O CHRISTMAS TREE in B-flat opens a fir and lights THE NEXUS; seven songs from the user's albums, one per MARK and ROOT, each motif chosen by ear, heard at its understanding's place and learned by playing it back.* **A is INDIGO everywhere.**
- ***T-408 (the user)***: **each grove its own music**, *fourteen loops from the user's own songs, each universe its own band; the comparison by ear is T-419.*

---

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
