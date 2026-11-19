# DAEMONS v11.405.1 — release notes

*Released 2026-11-19 01:57 · built against the design bible v11.405*

- **Engine**: CodeMusic/pokefirered-daemons `4e07515d8` (context-content)
- **Design**: CodeMusic/DAEMONS `21eef0ac`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `2892e2e64fbee9e12a6a3d94787a0e614ee58054` |
| `daemonsContext.gba` | CONTEXT | `6faabf23b1bfb800f2155a8ef2137e7465408019` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `a784c266deb2dd2efe42ef3ccd97677592b29f93` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `4f6839049dcf555656cb2856923e0f755a23b758` |

## The engine since v11.404.1

- `4e07515d8` T-595: songs in the engine (DRAFT) -- src/daemon_song.c sings a daemon's song through play.c's HARP (tune SE2, bass SE3), each unlearned note flickering toward its pitch over a tinted noise hiss (SE1) by the share learned from experience; the INDEX's START plays SONG, the party menu gains SING, and evolution sings the full part before the change, with an allusion where a next form waits; data from gensongs --write (398 parts, ~35 KB)
- `0edf6ad5f` README: latest is v11.404.1

## The design and tools since v11.404.1

- `21eef0acc` TODO: Redmine's mirror (T-595 closed, pokefirered-daemons@4e07515d8)
- `d6a9ab225` T-595: gensongs --write emits the engine's song table (APPROVED), reports its drift, and --engine-preview renders the engine's player offline (engine pokefirered-daemons@4e07515d8, DRAFT)
- `246da0094` Bible v11.405: TRAINER TOWER and THE SONG released (v11.404.1)
- `3c3148079` qa: T-438 TRAINER TOWER built (v11.404.1)
- `8fdfe7223` README, wiki: the newest release is v11.404.1
- `5aa44be75` ROM release v11.404.1: T-438 TRAINER TOWER in A PROGRESS (DRAFT art; T-438 closed) and T-594 THE SONG's draft generator; seals v11.403.x

## The design bible's own entry for v11.405

### v11.405 — 2026-11-19

- Recorded from release v11.404.1 (5aa44be7, engine 18c32d360), which sealed v11.403.x:
  - **T-438, TRAINER TOWER's interior** (DRAFT art): A PROGRESS, the user's AF -- floors and walls as progress bars, furniture as meters, the roof deck plain; its face kept vanilla for T-601. In 9.29.
  - **T-594, THE SONG** (DRAFT, not in the engine): every daemon's song from its name, type, INDEX entry and cry; SONG replaces CRY. New section 9.36.
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
