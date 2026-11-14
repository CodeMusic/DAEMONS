# DAEMONS v11.360.1 — release notes

*Released 2026-11-14 10:14 · built against the design bible v11.360*

- **Engine**: CodeMusic/pokefirered-daemons `ce345c195` (context-content)
- **Design**: CodeMusic/DAEMONS `c6ea43ba`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `caa5e3e46738e512b3d4c31acd6c83bdb8125bc5` |
| `daemonsContext.gba` | CONTEXT | `97cf533bd089ec6e518bf3533c438090408dd2c8` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `aa050ea05c1036a4cf0e1e6e24f6386a10742971` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `eb58d9531dc29fb7f4282204d514cedcb60ae2c2` |

## A note on the book audio

A minor release, released with one recording deferred (the user, 2026-11-12: "Release now, record after"): the new T-GLASSES book has not been recorded yet. It is made after this release.

## The engine since v11.358.1

- `ce345c195` T-540: THE WALLED GARDEN -- the SAFARI ZONE's every line set to the user's pick (85 labels, 2026-11-12), DRAFT
- `f90dd5f99` README: the release line names v11.358.1

## The design and tools since v11.358.1

- `c6ea43ba` docs README: the bible row names v11.360
- `a8952a1b` Bible v11.360: 3.11 THE WALLED GARDEN (T-540) -- the SAFARI ZONE as a walled platform run as a sandbox, its 85 lines picked by the user and built (DRAFT)
- `a99aaaa7` T-540: THE WALLED GARDEN's words built (engine ce345c195) -- the tools, the lexicon's two old names, the route, the sheets
- `19526da3` THE COMPANION re-recorded (friend) with THE DAY'S TENDING, the LINK CABLE and C-357's lines (cc5628a0) -- the recording v11.358.1 deferred
- `0a2f0a38` qa: C-357, THE COMPANION manual's new pages
- `cc5628a0` releasedocs STALE: THE COMPANION gains THE DAY'S TENDING (TODAY) and the LINK CABLE (Playing), and C-357's lines where their screens have chapters -- READS calm or argued, a lean Landed or A misread, the tally; THE SUBTLE LAYER's PAST / PRESENT / FUTURE kept for the day, only the FUTURE drawn again; a goal's weathered mark; Still me. after a change of form; pages.json names Tending.tsx and Link.tsx; reprinted (74 pages)
- `4aab80cc` Bible v11.359: v11.358.1 recorded -- THE BLANK TABLET released (T-547), the S.S. ANNE's wake behind her hull and the player before her funnel (T-447), the KEEPALIVE PLANT's card exits as a cave's (T-445)
- `7e3b2a81` TODO: T-547 released in v11.358.1 (engine 78dbb3ae2, release 49bd3417); not filmed yet
- `4c6cd758` README and wiki Home name v11.358.1
- `49bd3417` ROM release v11.358.1: T-547 THE BLANK TABLET (the Unity Book lane) and the filmed fixes -- the S.S. ANNE's wake behind her hull, the player before her funnel, KEEPALIVE PLANT's card exit; seals v11.356.x; two recordings deferred (the user)

## The design bible's own entry for v11.360

### v11.360 — 2026-11-12

- **3.11, THE WALLED GARDEN (T-540)**: the SAFARI ZONE becomes a curated, walled platform run as a sandbox (the user, 2026-11-10); its 85 lines picked one by one by the user (2026-11-12) and built, DRAFT. The RINGS count down, the menu reads SIGN OUT, SAFARI ZONE survives only as an old name, remembered.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
