# DAEMONS v11.290.8 — release notes

*Released 2026-10-02 09:36 · built against the design bible v11.290*

- **Engine**: CodeMusic/pokefirered-daemons `60a50211d` (context-content)
- **Design**: CodeMusic/DAEMONS `38684b8d`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `6d1f7c5be68ad3dd3726b79febf4e0b50bc60df8` |
| `daemonsContext.gba` | CONTEXT | `6a476c657a3409158587be49f32aed76309412e5` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `2e00c042af20e3d7576cac5f4ae991fde4af9b5f` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `05db4766cc3744b3b7b57fca307ea3bbbb78d238` |

## The engine since v11.290.7

- `60a50211d` T-337 fixed: the grove tell moved out of the water animation's tiles (462/463 -> 626/637)
- `45d52c4d2` T-347: the CHECKPOINT attendant's dream, offered to a player who seems stuck (DRAFT)
- `138b1aaae` T-346: the leaders say each MARK's virtue aloud, ANNEAL points home, and CALLOW hears its BENCHMARK unlatch (DRAFT)

## The design and tools since v11.290.7

- `38684b8d` TODO: what the theatre saw on screen 2026-10-02 -- T-297, T-340..T-343 played; T-338/T-339 checked from the built text
- `c6121afd` T-317: three overworld-clarity designs mocked up on a real CALLOW frame, A recommended -- waiting on the user
- `d67f313a` T-337 fixed, engine.md trap 39: a tile no metatile uses can still be one an animation owns -- gbagrove's check_tell_tiles() refuses it
- `7f956ac7` T-346, T-347 built: the eighth door announced, and the CHECKPOINT attendant's dreams (tools/gbadreams.py, docs/attendant_dreams.json); T-319 kept current
- `ff4de037` T-344: every release proves its Rev 1 patches on the user's own carts, by SHA-1, and refuses to publish otherwise
- `62ce4a78` T-345: check_lexicon excuses the ROUTE 5-8 graffiti by file, sign and phrase -- a stale name painted beside it is still caught
- `d6ced8ef` TODO housekeeping: T-316, T-318, T-235, T-10 and T-221 closed (verified, nothing left open); T-252 narrowed to its one open question; answered waiting tags struck on T-224, T-210, T-120
- `0de830e0` TODO: T-344 the user's cart dumps are in (FireRed and LeafGreen Rev 1, both retail-exact); the test joins today's goal
- `fc1ec96a` TODO: T-346 the eighth door announced and the virtues said aloud; T-347 the CHECKPOINT attendant's dream for a stuck player (both approved 2026-10-02)
- `93299e85` TODO: the user's answers of 2026-10-02 -- T-210/T-120 all of it (with the user, not in a loop), T-317 a drafted overworld change, T-318 seven is enough; T-345 the graffiti check
- `1c3c9d68` tools/dreamfold.py: keep every session fold, and dream it
- `4fdbede5` qa/screenshots: every earlier review picture filed, named <day> - <ticket> - <what it shows> - <number>
- `411790fa` qa/: every review picture filed where GitHub shows it, private ones ignored; the handoff and the push routine in CLAUDE.md
- `274eba6c` ROM RELEASE/CART BACKUPS: a gitignored home for the user's cart dumps, and T-344 the patcher test
- `66b17671` ROM release v11.290.7: FOLDS' corner of paper -- every approved find has its hint (T-297)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
