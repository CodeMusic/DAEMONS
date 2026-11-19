# DAEMONS v11.408.1 — release notes

*Released 2026-11-19 15:37 · built against the design bible v11.408*

- **Engine**: CodeMusic/pokefirered-daemons `719ad2dd5` (context-content)
- **Design**: CodeMusic/DAEMONS `b3227b0a`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `7ac446d6cabe45dc8119577ad8f40538d3f48476` |
| `daemonsContext.gba` | CONTEXT | `2d8a8f88fbfa570687843ec2a91f771fe04d38ea` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `2f627d046f69333ff6654935c798fa23ce8898c0` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `4124e5a15f2366cda94338300cb98e609fd47639` |

## The engine since v11.407.1

- `719ad2dd5` T-597: colour by song (DRAFT; the user: A grey until sung, song plus the two stories) -- a daemon's palette colours come in with the notes of its part they are tied to (sSongColourTies, 3.3 KB, gencolourbysong --write), carried colours never grey again; Saturation_SongToBuffer and the Mon* entries replace friendship at 30 call sites; friendship still scales over the song for AL's party and the Corpus (trainer classes as CreateNPCTrainerParty); the PC keeps a share per boxed daemon
- `51118cf94` README: latest is v11.407.1

## The design and tools since v11.407.1

- `b3227b0a` TODO: Redmine's mirror (T-597 closed, pokefirered-daemons@719ad2dd5)
- `df7530ca` T-597: gencolourbysong APPROVED, --write the engine's table, --verify-rom, the engine's integer maths (engine pokefirered-daemons@719ad2dd5, DRAFT)
- `c15fc6bc` qa: C-419 the INDEX sings, and ITS SONG on staves (companion 17034dc8, DRAFT)
- `ab705c25` qa: C-424's Kode Dot app in kode-sim -- ROUTINES, LODESTONE, READ MY TAG and back (review passed)
- `580be740` TODO: Redmine's mirror (a new ticket: later forms redrawn for colour by song)
- `e6bae1f5` qa: C-422's battles with friends' homes, seen on a scratch commons (DRAFT)
- `c07f87fe` qa: C-421's battle challenges, seen on a scratch companion (DRAFT)
- `3d302621` T-599: the quotations' styles, first slice (DRAFT, the user's to pick) -- each of the 18 types a style (A/B where uncertain: CONTENT, LOGIC, CORRUPT, CONTEXT, FROZEN, OPAQUE), 2-4 samples from real daemons of each, every one under 3 lines at 208px and clear of its SAID line, and six questions that shape all ~400
- `407d87aa` T-597 (draft): tools/gencolourbysong.py -- a daemon's palette at any share of its song (A grey until sung, B the key first, C the key's palette then A), census and contact sheets; nothing in the engine
- `d27e13cc` TODO: Redmine's mirror (T-603 closed, DAEMONS@b766e185)
- `b766e185` T-603: the tickets nightly honours a release hold for its whole length -- per-owner files in ~/.cache/daemons/release.hold.d/ as well as the shared one, checked again before each push (release_main.sh's exit trap had lifted v11.407.1's hold two minutes in, and 07f93547 went out inside it)
- `f5fdf8ca` Bible v11.408: the follower hums released (v11.407.1)
- `9c05f271` THE COMPANION's book audio re-recorded (friend, 76.2 min, sources e75ab71f) -- after v11.407.1, the user: release now, record after
- `a2d2eb13` qa: T-596 the follower hums (v11.407.1)
- `357479b6` engine.md: the budgets after v11.407.1
- `f4f84f1f` README, wiki: the newest release is v11.407.1
- `46088e05` ROM release v11.407.1: T-596 the follower hums, coloured notes from its mouth, and asks to sing (DRAFT); seals v11.405.x; THE COMPANION's book audio recorded after (the user)

## The design bible's own entry for v11.408

### v11.408 — 2026-11-19

- Recorded from release v11.407.1 (46088e05, engine b469aa716), which sealed v11.405.x:
  - **T-596, the wish to sing** (DRAFT): the follower hums with coloured notes from its mouth, and asks to sing after a won battle. In 9.36.
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
