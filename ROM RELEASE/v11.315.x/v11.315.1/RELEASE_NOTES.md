# DAEMONS v11.315.1 — release notes

*Released 2026-10-28 04:52 · built against the design bible v11.315*

- **Engine**: CodeMusic/pokefirered-daemons `1cb1f2f3f` (context-content)
- **Design**: CodeMusic/DAEMONS `a340b392`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `0817767ad36b2e473fe81e1c2dac22ff58e640eb` |
| `daemonsContext.gba` | CONTEXT | `c50211e50ede8495196c42930321a12a8e127108` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `f7fef0bf74ff8353616a342435c3421c935e8a0e` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `a708e5f00922a3cdb586bbe814b8afb46c4e68d8` |

## The engine since v11.314.7

- `1cb1f2f3f` T-452 batch 9: ALARM to RELEASE (161-181) in the new style, on the user's answers -- RELEASE's amber lamp on its tail tip and amber cap, MULTICAST's four wings, BUILDUP's wool off and ball tail, PRESCIENCE's perch off, ENTRAPMENT a big-eyed spider in a web, PILOT today's dome, STATIC the plain mouse, the CONTENT hue trap re-hued (rose ears, chartreuse owl eyes); grounding rows, icon palettes, follower palettes

## The design and tools since v11.314.7

- `a340b392` qa: C-203 the watches' mock-up (reads, the ripple, a lean)
- `e57c28ac` companion_export: C-203 THE LOG's layout (the reads vars, the game's phrases and packing) for the companion; COMPANION_DATA writes a worktree's data/
- `e8c74e5f` TODO: T-452 batch 9 built (engine 1cb1f2f3f) on the user's answers
- `4dcb9686` T-452 batch 9 built (engine 1cb1f2f3f): ALARM to RELEASE (161-181) as gbasprite's sources, on the user's answers -- RELEASE's amber lamp on its tail tip and amber cap, MULTICAST's four wings, BUILDUP's wool off and ball tail, PRESCIENCE's perch off, ENTRAPMENT the big-eyed spider in a web, PILOT today's dome, STATIC the plain mouse; ALARM's and LOOKOUT's ears rose, POLL's and SUPERVISOR's eyes chartreuse (the CONTENT hue trap); mirrored backs; grounds off
- `983ba672` TODO: T-463 struck -- already done in engine ea63fc73d and be0764027 (v11.314.1)
- `eb94fba0` TODO: T-463 SOUNDINGS approved -- DRAFT marks off, desk props out from under the hat
- `4bff97f5` TODO: T-462 ITS DREAMS -- the companion's dreams reach the game (C-200, the user's answers)
- `dd036c68` Bible v11.315: 4.38 THE SUBTLE LAYER -- the book, THE THREE and what the player notices (T-423, T-454, T-459); engine.md budgets; wiki: the intuitions and SOUNDINGS
- `c657ff7b` sprites.md: the census as v11.314.7 counts it (two more object variants)
- `f88e4511` ROM release v11.314.7: T-459 D words under words (from The Subtle Layer)

## The design bible's own entry for v11.315

### v11.315 — 2026-10-28

### THE SUBTLE LAYER gets its section (T-423, T-454, T-459)

- ***4.38***: **the book had lived only in `docs/subtle-layer.md` and its notes; the bible now holds it** -- *a handbook of practice, found on an INTERPRETER's shelf in BRAZEN, in CONTEXT's hue; THE THREE values (CLOSURE, ATTUNEMENT, VOLTAGE), battle-only and unsaved, waking only once it is held; and what the player notices after: the daemon notices first, a read, a lean in battle, and words under words.* **The log decides: the NOTEBOOK counts what landed, and the game never vouches that intuition works** (4.33). *The four lines beneath, as the user chose them, are in a table.*
- ***Reports regenerated***: *`engine.md`'s budgets (the census was already current).*

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
