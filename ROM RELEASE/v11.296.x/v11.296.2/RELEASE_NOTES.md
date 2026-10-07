# DAEMONS v11.296.2 — release notes

*Released 2026-10-07 11:45 · built against the design bible v11.296*

- **Engine**: CodeMusic/pokefirered-daemons `547ed6aec` (context-content)
- **Design**: CodeMusic/DAEMONS `a322921b`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `96eee892df1f5576c2e43139cf5741463ae45a85` |
| `daemonsContext.gba` | CONTEXT | `68dc898e62cdfe34d125db32f52d70a0963a6a9d` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `ad164a081de4c32fbba84f8b8dc1bee035a62728` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `be965eed12933bb4eda7f319c4ae76bd8fc53c9a` |

## The engine since v11.296.1

- `547ed6aec` T-385: the GUIDE's SECURITY page follows the Xenith week -- SUN chastity against lust ... THU forgiveness against wrath, FRI kindness against envy, SAT humility against pride (genguide.py from docs/guide.md)

## The design and tools since v11.296.1

- `a322921b` ai/README: points at the companion's voice -- n8n/ and stt/
- `ec6615c3` qa: the CC1101 running the companion's refactored firmware -- GAME ROUTINES, the battery and the DAY screen (companion C-68, C-63, C-73)
- `1548f328` T-385 done (engine 547ed6aec): the GUIDE follows the Xenith week -- docs/guide.md and the ROM's SECURITY page
- `c4faf039` companion_export: routines.json -- the game's move and type names, for the companion's GAME ROUTINES (companion C-68)
- `0611343c` T-385 answered: the GUIDE follows the Xenith week (to build in the day's release)
- `db4a9579` T-385 filed: the GUIDE's day table and the user's Xenith week disagree -- waits on the user
- `188b1300` ai: daemon/hear (speech to text alone, internal + relay); make_workflows.py writes the companion's workflows from one place; push.py tags every one daemons; the speech server on port 8770 (8000 is taken on roverbyteseer) -- companion C-83
- `c53f5ad8` ai/stt: an MLX Whisper speech-to-text server for roverbyteseer (OpenAI-compatible, port 8000) with its install and launch agent -- companion C-83
- `b2a33a71` companion_export: the user's Xenith week (Chastity cures Lust ... Humility cures Pride), companion C-73
- `c8d197fc` ai/n8n: push.py imports a workflow onto either n8n and switches it on; daemon/talk is live on both, asking LM Studio for gemma-3-4b by name (nothing stays loaded there) -- a spoken local turn about 14 s, a text turn through the public relay 1.3 s
- `a9cb752e` ai/n8n: daemon/talk -- the companion's push to talk (speech to text, the carried daemon in character on the local model or OpenRouter, the INDEX voice), internal and public relay (companion C-64, C-66)
- `c54f8dcc` companion_export: the Xenith week (the Guide's virtue over shadow, and the user's theme words, companion C-73) in place of RoverRadio's older table
- `258ed9a8` qa: AWAY end to end (work-day run item 4)
- `10fe71b3` T-378 closed: four routes played (scenes, t383, stillfall, field-test from stop 2); T-384 filed -- GOTO on the release ROM
- `1fe2e6fe` The walker crossed STILLFALL B1F's ice in the theatre -- ten moves, every slide stopping where the plan said (tools/routes/stillfall.json)
- `213b93dc` T-383: seen in the game
- `8624ab49` T-383 seen in the game (tools/routes/t383.json); T-378: a debug route wins any battle the walker meets, win takes a turn (A on DETACH never ends one), finish plays out a running script, says reads curly quotes as straight
- `9167f707` T-378: field-test.json passes stop by stop (2-18) -- the museum's fee marked paid, the museum left by its mat's middle, the Reading Room's door stepped onto once
- `95177098` T-367 closed (all seen but the NOTEBOOK pages, which wait on approval); T-378: music waits for a warp's song to settle; field-test.json -- the Reading Room's door and its inside as two stops, 1F's placard dropped in exam season; tools/routes/t383.json
- `e3aff7af` T-378: the runner refuses a theatre running another build (the song table in the emulator against the built ROM -- a text-only rebuild moved ROM addresses, so every music check read the wrong song), and never stands on a door to read the sign beside it
- `db4b6f72` qa: v11.296.1's pictures -- T-383's lines, PHLEGMATIC and SCORN (T-321), SLATE's MARK (T-346)
- `be8961cf` ROM release v11.296.1: T-383 (three lines the status sweep broke); seals v11.295.x

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
