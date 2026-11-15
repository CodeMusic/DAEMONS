# DAEMONS v11.366.1 — release notes

*Released 2026-11-14 19:56 · built against the design bible v11.366*

- **Engine**: CodeMusic/pokefirered-daemons `9e489b46e` (context-content)
- **Design**: CodeMusic/DAEMONS `7112fdb5`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `c10d179ef87eb9b4de6853a6e4c50aa96ea9d0f9` |
| `daemonsContext.gba` | CONTEXT | `8257f43c5adbf6b6e3fc4c00af12a6eb33bdf67c` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `5f22ee23bb52212171e929b77d1291736ee656ed` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `02877afd14e937d92ebaa70e705984e66252a6ab` |

## A note on the book audio

A minor release, released with two recordings deferred (the user, 2026-11-14: "Release now, record after"): THE COMPANION's and the new T-GLASSES book's.

## The engine since v11.365.1

- `9e489b46e` T-561: the field overlays in the A TERMINAL family -- the trainers' emotes (SMALL SCREEN), the itemfinder (PROMPT CHEVRON), the quest log's frame and description bar, the START banner and the HELP screen
- `c7cb4fcf0` README: the release line names v11.365.1

## The design and tools since v11.365.1

- `7112fdb5` v11.365.1's release notes: the redaction commit's subject no longer quotes the phrase it redacted ([private: SECRETS §2]; check_secrets)
- `14bceacb` T-561 BUILT: the field overlays, the user's picks (engine 9e489b46e) -- APPROVED_561, drift report, check_generators ARGS, proof sheets
- `8d481c54` T-561 (DRAFT): the field overlays drawn in the A TERMINAL family -- gbamenus3.py --t561, APPROVED_561 empty
- `a9e01fa7` TODO: T-560's live run -- 15 turns on the Tiiny's 35B through the hub's mind, every call valid; the brief's name bug found and fixed (engineAi c99c539)
- `90484c1a` TODO: T-561 filed -- the field overlays, batch 2 of the 2026-11-14 re-census (the user's pick)
- `542d36d0` Bible v11.366: the Fifth Review in play (T-556, T-557, T-559) and the menus' leftovers in TERMINAL (T-554), released (v11.365.1)
- `e47cafba` T-552, T-553: the backs-and-icons batch frees the sprite server when it ends; its first 7 drawings
- `02ec7161` school.md: one line swept for a private item (the Fourth Review's flag; the user, 2026-11-14)
- `eafb06c6` spriteforge: unload ComfyUI's models when a batch's process exits and the queue is empty (POST /free, as the hub does) -- FLUX left loaded beside ACE-Step filled roverbyteseer's memory 2026-11-14; SPRITEFORGE_KEEP_LOADED=1 skips it
- `c620df63` TODO: T-560 moved into the open table (check_todo)
- `58e9b7ba` T-560: bindDaemons.sh --ai stops defaulting to the PAID model (or-muse-glimmer) -- the hub's mind or the dashboard's Mind card decides, --mind pins one (the engineAi session's patch, applied by the game lane); TODO T-560 filed
- `05ff8600` README and wiki Home name v11.365.1
- `63a4963b` ROM release v11.365.1: the Fifth Review in play -- DURABLE (T-556), the ending's two gates (T-557), the HARD CODED grunt and AL's fading party -- and T-554 the menu leftovers in TERMINAL (DRAFT); the first release run through check_secrets and check_todo; seals v11.363.x; two recordings deferred

## The design bible's own entry for v11.366

### v11.366 — 2026-11-14

- Recorded from release v11.365.1, the Fifth Review in play. Each section already says what was built:
  - **DURABLE** holds from full HP (T-556).
  - **The ending's two gates** (T-557).
  - **The hideout's grunt holds HARD CODED, and AL's party greys** (T-559).
- **T-554, the menus' last FireRed pieces in TERMINAL**, the user's picks: the standard window, the bag's frame, arrows and icons, the markings, the keypad glyphs and the PC's item frame.
- A Settled entry in section 10. DRAFT.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
