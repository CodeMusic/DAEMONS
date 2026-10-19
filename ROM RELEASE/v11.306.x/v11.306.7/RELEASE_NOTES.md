# DAEMONS v11.306.7 — release notes

*Released 2026-10-19 15:25 · built against the design bible v11.306*

- **Engine**: CodeMusic/pokefirered-daemons `b4c215c59` (context-content)
- **Design**: CodeMusic/DAEMONS `500e3330`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `8625cba28e3a8cc00178e803752225d04dc13738` |
| `daemonsContext.gba` | CONTEXT | `d979decc020f316c6bd876c0f3b420221a59e9bd` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `a81a9255df53b3847694aae3bfb1e9e7c1331162` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `a2591a64ba559f3429ada9d09f51dc85ac993a6f` |

## The engine since v11.306.6

- `b4c215c59` INDEX: the cursor counts every daemon on a category page, seen or not (found by the field test's CONTEXT run)
- `2740469b5` T-334: the unseen legends found by walking into their place; the last two gates past 151 lifted; BELLOSSOM placed

## The design and tools since v11.306.6

- `500e3330` Field test: every feature since 2026-10-17 on the route, both editions -- CONTENT 40 stops, CONTEXT 13, all pass
- `bb5c21c9` T-334: legends found by walking in, tiles reached on foot, the last gates lifted, BELLOSSOM placed (engine 2740469b5); the INDEX's lookup fixed (engine b4c215c59)
- `dce59998` TODO: T-334 released; legends found by walking in, the last two gates lifted (the user)
- `c4bf480b` qa: T-334
- `3206b4c8` ROM release v11.306.6: the GLOBAL INDEX placed -- 128 daemons past #151 on the islands, 16 legendaries, trading past 151 open (T-334); the whole category on the INDEX (T-210)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
