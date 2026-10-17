# DAEMONS v11.302.1 — release notes

*Released 2026-10-17 19:53 · built against the design bible v11.302*

- **Engine**: CodeMusic/pokefirered-daemons `cf0dad98b` (context-content)
- **Design**: CodeMusic/DAEMONS `8416340d`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `6f82abc3d35409cfb9a73f64d9303a9971292066` |
| `daemonsContext.gba` | CONTEXT | `6101ede7e30684c9cded98f55497f25c1785684e` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `a440c590819ad9d8c50f7b56a330e5c016d51e73` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `ea0169ab0d1339ba764323086054f631bd0f9065` |

## The engine since v11.301.11

- `cf0dad98b` T-415 (the user, 2026-10-17): outdoor fog a light haze under the watch's light; WIND lifts VECTOR, no sandstorm; rain twice as heavy
- `b2d8cfb64` T-415 phase 1 (the user, 2026-10-17): WEATHER by season -- Ruby's unused overworld weather, drawn from the date
- `0c16670da` T-418 (approved by the user 2026-10-17): the GUIDE's SECURITY page says shadows -- "Virtues and Shadows: Securing the System", each virtue OVER its shadow, and a scan on a schedule where the patch was (DRAFT)
- `2540fa94e` STREAM's description: "lectures, one per MARK and more." (the user, 2026-10-17; DRAFT) -- the understandings' lectures joined them (T-405)

## The design and tools since v11.301.11

- `8416340d` qa: T-415 weather on Route 1
- `b9e24efa` TODO: T-415 decisions on phase 1 (the user, 2026-10-17) built -- fog a light haze, WIND lifts VECTOR, rain heavier (engine cf0dad98b)
- `aa995a00` qa: T-418, the GUIDE's SECURITY page in the ROM, both pages (played in the theatre)
- `bc6f5ddb` TODO: T-417's design decided (the user, 2026-10-17, by phone)
- `2192aea9` T-418 (engine 0c16670da, companion 8b255aa): the GUIDE's SECURITY page says shadows -- "Virtues and Shadows: Securing the System" (approved by the user 2026-10-17; DRAFT)
- `5dd7788f` TODO: T-415 phase 1 built (engine b2d8cfb64); tools/skyodds.py replays the weather's odds
- `6e3f550e` qa: T-418, the GUIDE's SECURITY page with shadows, drafted (a mock, not in the build)
- `fc5dac35` TODO: T-417 decided (HARP in CONTENT outside CALLOW SCHOOL, FLUTE in CONTEXT under a beach palm; the sheet gives the key; songs from the two albums; priority); T-416's last three answers
- `33a953d5` v11.302: a virtue is said OVER its shadow, never as its cure (T-418, the user 2026-10-17)
- `124c5e0c` companion_export.py (companion ea6e6d8): the week's cue is "<virtue> over <shadow>", never "cures" (T-418, the user 2026-10-17)
- `6d55bf2c` TODO: T-416 holidays decided in part (in-world names, the picks, a note a month); T-417 the instrument and SONGBOOK, planning
- `2fc20938` TODO: T-415 weather decided (the user, 2026-10-17); T-416 holidays and month colours, planning
- `8d6ba7aa` companion_export.py (companion 1640a9e): the GUIDE cover as drawn, with the author's name (the user, 2026-10-17)
- `8952fd4f` qa: T-405 on STREAM, played
- `8f85c7cb` ROM release v11.301.11: the understandings' STREAM lectures (T-405) and their names in the debug menu (T-252)

## The design bible's own entry for v11.302

### v11.302 — 2026-10-17

### Over, never cures (T-418)

- ***9.21, the week (the user)***: **a virtue is said over its shadow -- "CHARITY / over GREED." -- never as its cure.** *"Cures" makes the shadow an illness, and someone who takes in that they are the illness is harmed by the word: craft rule 3 reaching the week. "Shadow" is the structure (Jung's shadow work: lit and balanced, not removed) and the seven old names are the ground, so the MARKS print neither "vice" nor "sin".* ***Built***: *the ROM already said "over"; the companion's day cue now does too (`tools/companion_export.py`, week.json).* ***And the GUIDE (approved the same day)***: *its SECURITY page is now "Virtues and Shadows: Securing the System" -- a shadow "is not an intruder", each virtue over its shadow, a scan on a schedule where the patch was -- which also retires the old page's EXPLOIT, an intrusion word for a person (1.7). DRAFT.*
- ***10, Settled***: **Over, never cures.**

---

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
