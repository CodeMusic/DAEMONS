# DAEMONS v11.410.1 — release notes

*Released 2026-11-20 00:02 · built against the design bible v11.410*

- **Engine**: CodeMusic/pokefirered-daemons `a4e3cff97` (context-content)
- **Design**: CodeMusic/DAEMONS `0e401380`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `23c849d1143414a5cc3d69e046cb11976780db3c` |
| `daemonsContext.gba` | CONTEXT | `72ed4b84a73868b12708efecc2d9d69e8ccf8a09` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `13762b2fa874172a08e3e36c874f962ba7a01f53` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `553aa778a4acd3fcf4797d983db2a85b4ebaad7e` |

## The engine since v11.409.1

- `a4e3cff97` T-601: TRAINER TOWER's face from its roof, AFT THE TIME POSTED (the user, 2026-11-19; DRAFT art) -- one storey bar per floor (8 floors), each window a stopwatch with its hand up; the side faces a storey tick and the green as glass a floor deep
- `2d7fc1bf8` T-598 follow-up: DaemonSong_Listen looks on past an unseen daemon's opening instead of returning, so it stays right even if a table ever lets one opening end another (the Musical Instruments lane's review)
- `a3a90327c` README: latest is v11.409.1

## The design and tools since v11.409.1

- `0e401380` TODO: Redmine's mirror (T-601 closed, pokefirered-daemons@a4e3cff97)
- `6d48383d` T-601: gbatownslast APPROVED_TOWER AFT, the face's time posted (engine pokefirered-daemons@a4e3cff97)
- `3923da60` T-601 (draft): TRAINER TOWER's face from its roof -- AFB2 STOREYS, AFF THE FILL, AFT THE TIME POSTED in gbatownslast --tower (DRAFT, nothing approved; one storey per 8-row tile row)
- `6ea31ce2` Bible v11.410: play a daemon's song and it comes, released (v11.409.1)
- `ca6f1dc9` THE PLAYER'S MANUAL's book audio re-recorded (adventure, 56.1 min, sources e9cf3ed8) -- after v11.409.1, the user: release now, record after
- `740011b1` qa: T-598 a song played, and it comes (v11.409.1)
- `8710c96a` engine.md: the budgets after v11.409.1
- `ce1e26e2` README, wiki: the newest release is v11.409.1
- `61bca9d1` ROM release v11.409.1: T-598 play a daemon's song and it comes (DRAFT; quotations wait for T-599); seals v11.408.x; THE PLAYER'S MANUAL recorded after (the user)

## The design bible's own entry for v11.410

### v11.410 — 2026-11-19

- Recorded from release v11.409.1 (61bca9d1, engine 958261282), which sealed v11.408.x:
  - **T-598, play a daemon's song and it comes** (DRAFT): matched against SEEN daemons' openings; it sings and goes; quotations wait for T-599. In 9.36.
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
