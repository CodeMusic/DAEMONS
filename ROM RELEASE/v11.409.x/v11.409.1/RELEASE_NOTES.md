# DAEMONS v11.409.1 — release notes

*Released 2026-11-19 19:03 · built against the design bible v11.409*

- **Engine**: CodeMusic/pokefirered-daemons `958261282` (context-content)
- **Design**: CodeMusic/DAEMONS `d2d7b6d5`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `ebbfd3427f3ad1541a52662aa76cc09142fe82cb` |
| `daemonsContext.gba` | CONTEXT | `0f09b3081114520ffa26e3f93556cfe7a9dd4d93` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `5183758bbe37b55fc650d0cb709624bdba62c303` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `15e6b51e3411f1703d7a2552b933d1574e7d671d` |

## The engine since v11.408.1

- `958261282` T-598: play a daemon's song and it comes (DRAFT) -- DaemonSong_Listen (hooked after PLAY's SONGBOOK in Listen) matches the last notes, octave-blind, against each SEEN daemon's opening on its key's wheel (a minor song on its relative major, the user's pick); it flickers in near the player, sings its part with notes from its mouth, says its QUOTATION when T-599 writes one (sDaemonQuotations, all NULL: no words yet) and goes; never caught, never a battle; SaveBlock1.daemonsSummoned[64] (from questLogFreed after T-591's dream days); the INDEX shows a summoned daemon's quotation once one exists
- `65d0e3936` README: latest is v11.408.1

## The design and tools since v11.408.1

- `d2d7b6d5` TODO: Redmine's mirror (T-598 closed, pokefirered-daemons@958261282)
- `bef7a102` T-598: gensongs writes the summon openings (daemon_summons.h: 397 openings, lengthened past collisions, CORRUPT's sharp a wildcard; THENCASE cannot be told from OTHERWISE in 16 notes); film route t598 (engine pokefirered-daemons@958261282, DRAFT)
- `b77dd6d6` qa: C-426's Kode Dot den in kode-sim -- PIP, FEED and SLEEP on a scratch companion (review passed)
- `57804d74` Player's manual: Colour is the song (T-597, v11.408.1) -- a daemon's colours come in with the notes of its part, not with friendship; reprinted
- `22eec161` Bible v11.409: colour by song released (v11.408.1)
- `d88be332` qa: T-597 colour by song (v11.408.1)
- `00a04b62` engine.md: the budgets after v11.408.1
- `991e2464` README, wiki: the newest release is v11.408.1
- `9adefb20` ROM release v11.408.1: T-597 colour by song -- grey until sung, song plus AL's and the Corpus's friendship (DRAFT); seals v11.407.x

## The design bible's own entry for v11.409

### v11.409 — 2026-11-19

- Recorded from release v11.408.1 (9adefb20, engine 719ad2dd5), which sealed v11.407.x:
  - **T-597, colour by song** (DRAFT, the user's A): grey until sung, AL's party and the Corpus still by friendship; T-604 to redraw later forms. In 8.6a, 9.36 and the Reversed table.
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
