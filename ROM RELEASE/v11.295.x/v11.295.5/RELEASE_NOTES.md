# DAEMONS v11.295.5 — release notes

*Released 2026-10-04 21:27 · built against the design bible v11.295*

- **Engine**: CodeMusic/pokefirered-daemons `b5dc7f8de` (context-content)
- **Design**: CodeMusic/DAEMONS `81eaa1e9`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `d7dc588f5265b57626fd7fe9be1cdd64d2807995` |
| `daemonsContext.gba` | CONTEXT | `6b0f0c9ff3044ad5d66d35e60dd48da612b3c343` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `cf20791336d3cb39d001fb2ac1359d6a144e67ba` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `8b128d66b3f4475633e6cfcf29e35ed4b1c79068` |

## The engine since v11.295.4

- `b5dc7f8de` T-350: CRYSTAL seen from behind -- the fox head and ruff on every throw frame, as approved
- `2fb8bde68` T-372: the trainer card shows a clock beside the day when the cartridge's real clock drives the time (the user's choice, A with a clock); nothing there when time comes from play

## The design and tools since v11.295.4

- `81eaa1e9` T-350 closed: CRYSTAL's back built in by genmentors.py (engine b5dc7f8de) and seen in the STREAM
- `76478435` T-350: CRYSTAL's back drafted -- the fox head and ruff from behind on every throw frame -- and shown for the user's approval
- `1d764d2c` T-372 closed: the clock beside the day on the trainer card
- `1f1cbc95` T-337: the singing fir's star seen twinkling on a screen (gold, the light, the glint), the last unseen piece of the 2026-10-02 evening goal
- `a992efcc` gitignore: T-350's drafts, drawn over the original's frames, stay local
- `b871c673` T-350 started: CRYSTAL's back redraw has its direction (drafts kept out of git: they were drawn over the original's frames)
- `509f2d00` T-372: the clock mark mocked on the real trainer card -- three options for the user (a symbol or a word beside the day, or a symbol on the TIME row)
- `c37c316f` T-369 closed: check_reach.py runs trap 17's registration check every time -- a palette tag registered in two slots that vanilla does not split fails, the player's forms and the daemon type tags excepted with why; proved on a planted split
- `b93d24a1` T-368 closed: the field-test page's 116 pictures are published files, the page 327KB (was 10.9MB)
- `49961c69` qa: the user's goal on the board (companion C-46, C-49)
- `21e3bbbe` ROM release v11.295.4: the game unchanged; the companion grew its goals of milestones, remotes and networks taught to the daemon, and its first iPhone app

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
