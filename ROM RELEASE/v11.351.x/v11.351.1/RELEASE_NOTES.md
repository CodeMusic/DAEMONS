# DAEMONS v11.351.1 — release notes

*Released 2026-11-11 16:55 · built against the design bible v11.351*

- **Engine**: CodeMusic/pokefirered-daemons `ba1c0ac79` (context-content)
- **Design**: CodeMusic/DAEMONS `33c89a9d`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `c54793ec76ee4f436e2cb8ccc414680c1c9d366a` |
| `daemonsContext.gba` | CONTEXT | `729cbc68da74b60279a1f53a3ca2071b7e667174` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `89415bec99a70b0eb56b894fbdd83aa305789c9d` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `8343b7994af47368fec77def12c4effee511fc84` |

## A note on the book audio

A minor release, released with three recordings deferred (the user, 2026-11-11: "Release now, record after"): THE COMPANION, PLAYING TOGETHER and THE WATCH were rewritten in `ecb4ff84` (T-545), and their recordings trail the manuals until the Releases lane re-records them. The printed manuals are current.

## The engine since v11.350.1

- `ba1c0ac79` T-445: TANOBY's card keeps MONEAN's rose pigment band, as drafted and picked (fc22a68da had painted it out by mistake; 334 tiles)
- `fc22a68da` T-445: two landmark name cards BUILT -- KEEPALIVE PLANT growing untended (A) and TANOBY's chambers carved, not lit (A), the user's picks 2026-11-11 (gbapreviews --cards --write --approved; DRAFT)
- `58eaa23d8` C-272: the eight redrafted HERMETIC LAYER faces in the game's arcana (port_arcana --write from companion arcana.json 3ccfa39) -- I BELOW DEDUCTION, II BELOW RECALL, VI ABOVE MULTIMAL, VIII BELOW WRAPAROUND, X ABOVE, XII BELOW STANDBY, XIII ABOVE, XXI BELOW POSTULATE (DRAFT)
- `fe069586a` README: the release line names v11.350.1 (DAEMONS T-545)

## The design and tools since v11.350.1

- `33c89a9d` check_generators: the T-445 comment names the cards by place, not by tileset folder (gbalandmarkrooms read 'power_plant' as an unknown tool writing that tileset and exited 1)
- `e8859a1e` qa: T-445's two landmark cards built (sheet 101)
- `2c5c74f8` T-445: the two landmark cards BUILT, PLANT A and TANOBY A (engine fc22a68da, ba1c0ac79); gbapreviews CARDS_APPROVED and CARDS_TAKEN, painted_path reads t445_landmarks under --cards; check_generators runs gbapreviews --cards --approved
- `8b5f5096` T-445: the landmarks' name cards re-censused and DRAFTED (gbapreviews.py --cards; gfx/drafts/t445_landmarks/) -- all ours but DOLDRUM CAVE; KEEPALIVE PLANT and TANOBY stale after T-447 pair 5, candidates for both, and the MANSION's rack hall and DAEMON TOWER's dot screen as alternatives; CARDS_APPROVED empty, nothing in the engine (DRAFT)
- `01091db8` TODO: T-545 struck through (ecb4ff84; companion ed09a9f, C-341)
- `ecb4ff84` T-545 (2): the manuals tell what WHAT'S NEW brought -- THE COMPANION: SLEEP SOUNDS, THE EASEL, THE ENGINE ROOM and a look inside its mind; THE WATCH: a book read in its own recording, kept on the card; PLAYING TOGETHER: IN DIALOGUE, BATTLE and THE ENGINE ROOM for the keeper; all three reprinted (DRAFT). releasedocs.py: the YOU tab's pages route to PLAYING TOGETHER, and an app page no chapter covers is STALE
- `a22d51e5` Bible v11.351: T-447 pair 7, the S.S. ANNE in THE LIVERY, released (v11.350.1); every landmark ours but USER TOWER and DOLDRUM CAVE
- `6c3ecfcf` T-545 (1): README and wiki Home name v11.350.1 (engine fe069586a)
- `0df51059` ROM release v11.350.1: T-447 pair 7, the S.S. ANNE in C THE LIVERY with the smoke over the funnel -- every landmark ours but USER TOWER and DOLDRUM CAVE; v11.349.x sealed (DRAFT)

## The design bible's own entry for v11.351

### v11.351 — 2026-11-11

- **9.29:** landmark pair 7 is built and released in v11.350.1 (T-447). The user chose THE LIVERY for the S.S. ANNE: the outside of the liner, which was already ours, carried into her rooms. Her departure smoke now sits over the funnel. Every landmark is now ours except USER TOWER (the user's) and DOLDRUM CAVE (waits on T-251).
- A Settled entry in section 10. All of it is DRAFT.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
