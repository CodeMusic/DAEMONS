# DAEMONS v11.290.1 — release notes

*Released 2026-10-01 16:46 · built against the design bible v11.290*

- **Engine**: CodeMusic/pokefirered-daemons `71b761513` (context-content)
- **Design**: CodeMusic/DAEMONS `6986beae`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `48f4b74ec6573c8ecb93ed3db1aa834dad0c2d58` |
| `daemonsContext.gba` | CONTEXT | `ded6d5aeab91f08a932f5f98d44ae530f1c0e425` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `32ba4197ef69cc0c8457fc0fdc32737284bd9dcb` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `42ca12759662d95c00bb416e57e00585fe4b0740` |

## The engine since v11.289.2

- `71b761513` T-333: 65 named daemons get INDEX categories of their own (DRAFT) -- OVERCALL, NIGHT WATCH, BANDWAGON, HARD STOP, KEEPALIVE, SHAPESHIFT ...; each line keeps the category it replaced
- `9d5a6e4a4` T-322: QUORUM's CONTENT entry takes the draft -- what a quorum is: none acts until enough of the others have seen the same thing (DRAFT)

## The design and tools since v11.289.2

- `6986beae` T-333 closed: check_lexicon fails on a renamed daemon under upstream's INDEX category; its vanilla-INDEX row fails the run again (a later check had overwritten its result)
- `8ab3e763` v11.290: QUORUM's CONTENT line redrawn (T-322, the user's choice) -- 4.25's quote follows; the INDEX's 65 categories in the changelog (engine 9d5a6e4a4, 71b761513)
- `0763ac9e` TODO: QUORUM answered -- take the draft (T-322), for the next goal pass
- `e4ab4fb6` ROM release v11.289.2: the dated documents (T-335) -- CORRESPONDENCE 1, PROSPECTUS 3 placed, the staff notice; lists and signatures on their own lines again

## The design bible's own entry for v11.290

### v11.290 — 2026-10-01

### QUORUM teaches its word, and the INDEX's categories catch up (2026-10-01)

- ***QUORUM's CONTENT line is redrawn*** (T-322, the user's choice): *"Three of them. None acts until enough of the others have seen the same thing. Two is enough. One never is." — the old line taught "three saw it", never the threshold. 4.25's quote follows; CONTEXT keeps its line.*
- ***65 named daemons get categories of their own*** (T-333, DRAFT): *ALARM is an OVERCALL DAEMON, BLISSEY's slot a KEEPALIVE, PROTEUS a SHAPESHIFT. `check_lexicon` now fails on any renamed daemon still under upstream's category — and its vanilla-INDEX row, which a later check had been silently overwriting, fails the run again.*
- ***The dated documents*** (T-335, released in v11.289.2): *the user's own dates on the NOTEBOOK's pages, under fable names; the record itself stays private.*

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
