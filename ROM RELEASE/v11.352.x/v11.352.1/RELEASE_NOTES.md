# DAEMONS v11.352.1 — release notes

*Released 2026-11-11 18:41 · built against the design bible v11.352*

- **Engine**: CodeMusic/pokefirered-daemons `569037e2d` (context-content)
- **Design**: CodeMusic/DAEMONS `77e500dc`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `6d3a859beabaf709e0ec519ef50253e78789ed1c` |
| `daemonsContext.gba` | CONTEXT | `57da5ee2fd844bb93b2630b902a6c9c83b116b66` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `902309a5b022a6c6567572d9dbb18eb9b647874d` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `8b31dfe0f9f1b78c0050a4a421834be8b9ce7ce7` |

## The engine since v11.351.1

- `569037e2d` T-447: the S.S. ANNE's departure wake to her waterline -- +76, y 113 (was +80, y 109, which showed through the flagstaff's notch over the deck); the user's pick 2026-11-11
- `a682d40e1` README: the release line names v11.351.1

## The design and tools since v11.351.1

- `77e500dc` T-447: the S.S. ANNE's wake to her waterline (engine 569037e2d); gbalandmarkrooms' departure sheet reads the wake from ss_anne.c (wake_at) and draws it behind the ship; qa 106
- `9b3c06af` qa: C-296, SPIRITS' tone and THE MIND's SPIRITS card (companion dca02e7)
- `8fe99710` T-545: the three recordings made after v11.351.1, as the user chose ("Release now, record after") -- THE COMPANION (62 min), PLAYING TOGETHER (17 min) and THE WATCH (25 min), each in its own voice, from the manuals of ecb4ff84
- `349b7cb1` Bible v11.352: T-445's two landmark cards and C-272's eight HERMETIC LAYER faces, released (v11.351.1)
- `ba8c8ad2` T-544: releasedocs.py --defer-audio -- a minor or major release the user chose to record after (v11.351.1, "Release now, record after") passes the audio gate with the plan printed; a book with no voice still fails
- `f4d710f0` qa: C-273, THE HERMETIC LAYER's cards on the site (companion f94226e)
- `c07143db` README and wiki Home name v11.351.1 (engine README too)
- `981c22cd` ROM release v11.351.1: T-445's two landmark cards (KEEPALIVE PLANT A, TANOBY A) and C-272's eight redrafted HERMETIC LAYER faces; seals v11.350.x; three book recordings deferred (the user: release now, record after)

## The design bible's own entry for v11.352

### v11.352 — 2026-11-11

- **9.29:** the landmarks' name cards follow their buildings, released in v11.351.1 (T-445). The KEEPALIVE PLANT's card is growing untended, and TANOBY's chambers are carved, not lit. Every place card is now ours except DOLDRUM CAVE's.
- **4.39:** eight of THE HERMETIC LAYER's faces were redrafted in the companion and carried into the game's deck (C-272, v11.351.1).
- A Settled entry in section 10. All of it is DRAFT.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
