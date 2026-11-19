# DAEMONS v11.407.1 — release notes

*Released 2026-11-19 08:40 · built against the design bible v11.407*

- **Engine**: CodeMusic/pokefirered-daemons `b469aa716` (context-content)
- **Design**: CodeMusic/DAEMONS `d14b13bc`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `97e021929b2e6e35c446096c800ee0e8a9408dd6` |
| `daemonsContext.gba` | CONTEXT | `ca6289593169ceec829e6dcfa5fad0e146aa8ceb` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `b6f33fe0c1e16f112265948605a04b9e5ee0826b` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `27919a8b3abe7a7863376b776f934f3dd4c3a86d` |

## The engine since v11.405.1

- `b469aa716` T-596: the wish to sing (DRAFT) -- a follower near its evolution hums a bar of its song as known (DaemonSong_Hum, under the music), each note an 8x8 sprite rising from its mouth in its pitch's colour (static ones flicker as the audio does; HUM_TAG palette, HALFTONE skips it); after a won battle it may ask "{STR_VAR_1} wants to sing." and sings on YES; DEBUG FOLLOWER rows to force both
- `1740b96a1` README: latest is v11.405.1

## The design and tools since v11.405.1

- `d14b13bc` TODO: Redmine's mirror (T-596 closed, pokefirered-daemons@b469aa716)
- `a9a183de` T-596: tools/genhumnotes.py draws the hum's note sprites; film route t596 (engine pokefirered-daemons@b469aa716); port_vocab keeps SING the song action from the move's rename to LULLABY
- `07f93547` Tickets nightly 2026-11-19: the Redmine export (T-581)
- `1bd97e09` The companion's manual: TRAIN sings (C-418), in Caring for it
- `db6c9f3f` qa: T-594 a line's song in its colours; C-418 TRAIN sings on the companion site
- `bf7d35a1` TODO: Redmine's mirror (T-594, C-417, C-418 closed; T-602 opened)
- `0d70c9f7` Bible v11.407: THE SONG's companion half and what is decided to build (9.36)
- `3c61231a` Bible v11.406: songs in the engine released (v11.405.1)
- `ce1ebcea` qa: T-595 songs in the engine (v11.405.1)
- `2a0574f0` engine.md: the budgets after v11.405.1
- `bfe19801` README, wiki: the newest release is v11.405.1
- `54c4e9fc` ROM release v11.405.1: T-595 songs in the engine -- SONG on the INDEX, SING in the party, evolving by song (DRAFT); seals v11.404.x

## The design bible's own entry for v11.407

### v11.407 — 2026-11-19

- **9.36 THE SONG, the rest of the design** (T-594, C-417, C-418; the user, 2026-11-18, in their words and by multiple choice):
  - **The keys**: the eighteen types' keys in a table, each tonic the note whose colour is nearest the type's own, CONTENT C major and CONTEXT its relative A minor, six spare (DRAFT, for the user's word).
  - **Where a part's levels come from**: its form's first level to its evolution level; a stone, trade or friendship 20 on; a final form as many levels as the form before it took; no line, 40 (DRAFT).
  - **In the companion, built** (C-418): TRAIN sings the part it is learning -- the forward pass in coloured notes, static a cloud of agreeing candidates, then green binary carried back, a group a note moved; two weeks of three a day makes a part whole; a whole part sends it home to SING, and it evolves in the companion only once AT HOME (bond 160, DRAFT). The widget too, and its FEED and DRINK animated as the app's (C-417).
  - **Decided, to build**: the wish to sing (T-596), colour is the song (T-597), a song played in its key summons its daemon (T-598), THE QUOTATIONS (T-599), their book (T-600), shiny songs (T-602).
- **Reversed**: 8.6a's "saturation is friendship" becomes "saturation is the song" (T-597, to build); logged, with Al's party and the Corpus open.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
