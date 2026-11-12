# DAEMONS v11.353.1 — release notes

*Released 2026-11-11 21:45 · built against the design bible v11.353*

- **Engine**: CodeMusic/pokefirered-daemons `676f4cb6b` (context-content)
- **Design**: CodeMusic/DAEMONS `bb1e2814`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `837c6b24225b3f318547f1a00f609bd92af02766` |
| `daemonsContext.gba` | CONTEXT | `04ddb2a1cb114487ec496c83311b8a942242b0d9` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `bd1207aabc110bee058b30927250d0ca0865e71f` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `de878beef3cf46dd404d30423eac0ba0a6248798` |

## A note on the book audio

A minor release, released with one recording deferred (the user, 2026-11-11: "Release now, record after"): THE COMPANION's manual changed since its recording, which trails it until it is re-recorded. The printed manual is current.

## The engine since v11.352.1

- `676f4cb6b` T-542 batch 4: the last three Nintendo edges in General -- the sand's corner (4), the forest path's edge (301), the cliff's foot (503) -- in B THE TRACE, the user's pick 2026-11-11 (gbaprimary --write --batch 4 --approved --pick B; DRAFT)
- `0b27e51fe` README: the release line names v11.352.1

## The design and tools since v11.352.1

- `bb1e2814` releasedocs STALE: THE COMPANION gains GUARDIAN (YOU) -- the grown-up's account, profiles named from two lists, their four controls, a one-time code to open one on a device, closing, removing, signing out and deleting; pages.json names screens/you/Guardian.tsx; reprinted (72 pages)
- `06ba6526` qa: T-542 batch 4 built (107)
- `3e21afab` T-542 batch 4 BUILT: the last three General edges (4, 301, 503) in B THE TRACE, the user's pick (engine 676f4cb6b); gbaprimary batch 4 (drafts A THE DITHER, B THE TRACE, C THE CUT STONE in gfx/drafts/t542_b4/, APPROVED_B4 {B}); check_generators runs --batch 4 --approved --pick B
- `39f9fbaa` Bible v11.353: the S.S. ANNE's wake at her waterline, released (T-447, v11.352.1)
- `d9857407` README and wiki Home name v11.352.1
- `8ab869b3` ROM release v11.352.1: the S.S. ANNE's departure wake at her waterline (T-447); seals v11.351.x

## The design bible's own entry for v11.353

### v11.353 — 2026-11-11

- **9.29:** the S.S. ANNE's departure wake now starts at her waterline, released in v11.352.1 (T-447, the user's pick). It had shown through the flagstaff's notch over the deck.
- A Settled entry in section 10. DRAFT.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
