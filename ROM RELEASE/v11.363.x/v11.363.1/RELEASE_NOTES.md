# DAEMONS v11.363.1 — release notes

*Released 2026-11-14 14:31 · built against the design bible v11.363*

- **Engine**: CodeMusic/pokefirered-daemons `e9a023b4b` (context-content)
- **Design**: CodeMusic/DAEMONS `ab81c0d8`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `e7e024b846a26eac1ef38d120dd7e9d9f2813ee6` |
| `daemonsContext.gba` | CONTEXT | `98854a4b6215a7cfc7b6681654a26631b433fef2` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `29808def279af336fd6cc6158ae5360bd20af0c0` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `d6634e4fc92c9b0c352bb49aa3a51638f6811d70` |

## A note on the book audio

A minor release, released with one recording deferred (the user, 2026-11-12: "Release now, record after"): the new T-GLASSES book has not been recorded yet.

## The engine since v11.362.1

- `e9a023b4b` T-548, T-549, T-550: THE SUBTLE LAYER at evolving, at naming, in crowds (DRAFT)
- `f1bcf2c86` README: the release line names v11.362.1

## The design and tools since v11.362.1

- `ab81c0d8` T-548, T-549, T-550 BUILT (engine e9a023b4b): "Still me." under an evolution, "A direction, not a verdict." on a daemon's naming screen, the crowd's read (DRAFT)
- `b92acb9f` companion_export: each species' gender split (genderRatio) for the companion, so a daemon is spoken of as the game has it -- he, she, or they (companion C-359; the user, 2026-11-14)
- `ea802646` qa: C-358 CREATIONS -- the household gallery, the record player, its spectrum, COMMUNITY
- `7d6196dc` THE COMPANION re-recorded (friend) with CREATIONS (bfe09406)
- `bfe09406` releasedocs STALE: THE COMPANION gains CREATIONS (C-358) -- MINE, HOUSEHOLD with its ✓ and Only what this phone does not have, COMMUNITY on THE COMMONS; download, share, let go; a sleep piece as a record, its night drawn round it, the spectrum; EXPORT as MP3, MP3 + DRIFT DOWN or PULSEENTRAIN; SLEEP SOUNDS' KEPT FROM OTHER NIGHTS is now CREATIONS; pages.json names Creations.tsx; reprinted (75 pages)
- `d096bd6b` Bible v11.363: THE WALLED GARDEN's art released -- C THE GLASSHOUSE, the GATEKEEPER's shelf, name card B over the wall; T-540 complete (v11.362.1)
- `ec1a5c5a` README and wiki Home name v11.362.1
- `4b15dfd2` ROM release v11.362.1: T-540's art -- THE WALLED GARDEN inside as C THE GLASSHOUSE, the GATEKEEPER's shelf to match, its name card B over the wall; T-540 complete (DRAFT); seals v11.361.x; T-GLASSES' recording deferred

## The design bible's own entry for v11.363

### v11.363 — 2026-11-14

- **3.11:** THE WALLED GARDEN's art, the user's picks, released in v11.362.1. With it, T-540 is complete.
  - **The interiors are THE GLASSHOUSE:** whitewashed panes that let the light in and show nothing.
  - **The GATEKEEPER's shelf** matches, with the old sign turned to the wall.
  - **The name card** shows the garden seen over its wall.
- A Settled entry in section 10. DRAFT.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
