# DAEMONS v11.307.1 — release notes

*Released 2026-10-20 11:17 · built against the design bible v11.307*

- **Engine**: CodeMusic/pokefirered-daemons `97f28c455` (context-content)
- **Design**: CodeMusic/DAEMONS `568d3e25`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `3f50c869b03f10948c7986edf1ae2c65452b478b` |
| `daemonsContext.gba` | CONTEXT | `77b264b0f9552a35e8c94a92535430c38359c984` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `e2f148da4d75452f827a48f8b49beb3b1b0b7cc7` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `62718ba4565e82f182e4cf054f9e8d75056fc09a` |

## The engine since v11.306.10

- `97f28c455` T-406: BOUND -- the INDEX's workings (L, MORE) open with how the daemon you hold came to you: BOUND: <its met place>, BOUND: BY TRADE (METLOC_IN_GAME_TRADE or an OT that is not you), BOUND: FROM AN EGG (met level 0), BOUND: A GIFT (givemon, or a fateful encounter); the first held one is read, party then boxes, none held or reading in a battle says nothing (DRAFT). A gift is marked by ScriptGiveMon in substruct0's spare u16, bit 0 (MON_DATA_DAEMONS_GIFT 89); one given before this build reads as bound where it was given
- `4227f501d` T-423: THE SUBTLE LAYER's cover -- the plate narrowed so the six clair glyphs sit clear of it (the user chose cover A, 2026-10-20); DAEMONS tools/gensubtle.py

## The design and tools since v11.306.10

- `568d3e25` TODO: T-406 struck -- BOUND built (engine 97f28c455): the workings' first line says how the daemon you hold came to you (DRAFT)
- `491e20a9` T-423 done: the last three calls, made with the book in the game -- CHORUS kept, the Clairs hint kept, cover A with its plate narrowed (engine 4227f501d, companion 4467612)
- `6a106554` T-423: the cover's plate narrowed so the six clair glyphs sit clear of it (the user chose cover A, 2026-10-20; engine 4227f501d)
- `ea11e93f` TODO: T-319, invisible objects hidden from the model (the user)
- `4e1ca62d` T-319: the AI playtester kept current to 2026-10-20 (engineAi 8b3b1e0)
- `7605c077` TODO: T-18 planned; the user's four answers
- `548304a8` TODO: six finished tickets struck -- T-334, T-408, T-415, T-417, T-422, T-427 (the user)
- `98f2d9c2` Bible v11.307: CALLOW's own theme on the GBA build (T-05)
- `2d50f6f5` qa: T-406, T-05, T-422's cheer
- `92a6b928` ROM release v11.306.10: CALLOW's own theme (T-05), the GAME CORNER's crowd cheers (T-422), the INDEX says where you first met each daemon (T-406)

## The design bible's own entry for v11.307

### v11.307 — 2026-10-20

### CALLOW's own theme (T-05)

- ***7.4 (the user, by ear)***: **CALLOW plays The Christmas Cloak of Self** on the GBA build, *its houses and the school with it; THE BLEED keeps its tune, so the two no longer share.*

---

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
