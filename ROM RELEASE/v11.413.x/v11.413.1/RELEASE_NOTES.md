# DAEMONS v11.413.1 — release notes

*Released 2026-11-23 14:38 · built against the design bible v11.413*

- **Engine**: CodeMusic/pokefirered-daemons `39093823d` (context-content)
- **Design**: CodeMusic/DAEMONS `0f12b477`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `4cbfca39dd372ac84331455f6335296aad9de440` |
| `daemonsContext.gba` | CONTEXT | `f17f73382ba4f3fae431fa230ad6342369555e6a` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `1cc6316f40e319f4eeb10040aaad944c536d54c3` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `e89a9ab73c12e6ebca68f43b95fc77cbbe0500e5` |

## The engine since v11.412.10

- `39093823d` T-604: stage 4 -- fifteen more later forms colour in as they learn their part: a region in the new part's colours (BACKPRESS's sea-green crest and fins, DRAGNET's moon-jelly violet bell, UPSTREAM's goldfish-orange fins and tail, HANDLER's violet speculum, TRACKER's ginger ears, tail and tabby marks, PARTITION's rust armour plates, LIVELOCK's violet trunks, OUTBREAK's plum hood, QUORUM's brass eyes and spheres, BREAKER's violet cap, BUSYWAIT's gold ears and flank, ROOTKIT's amber cap, INFERENCE's gold ears and tail, ENSEMBLE's coconut side heads, REBUTTAL's orange gloves), DRAFT
- `b2aa2cc02` README: latest is v11.412.10

## The design and tools since v11.412.10

- `0f12b477` qa: T-604 stage 4, fifteen later forms, built
- `17373b52` qa C-482: a shiny's ITS SONG in a scratch companion (DRAFT)
- `7b6e8a30` C-482: gensongs exports T-602's shiny notes into the companion's songs.json (shiny: a form's [note index, MIDI]; companion 587e30f2)
- `d4cc7e61` The Fifth Review: where it stands at v11.412 -- items 3, 4 and 7 done, 1, 2 and 5 still the author's
- `bdc0d058` T-604: stage 4 -- fifteen later forms colour in (engine 39093823d), DRAFT
- `143841b0` T-604 (draft): stage 4 -- fifteen more later forms get a region in their new part's colours, DRAFT, nothing built
- `e4228402` qa: C-476's captions in the day's README
- `8bba8516` Bible v11.413: the eighteen type keys approved (T-594, the user's yes)
- `ff5972a0` qa: C-476 STATES OF YOUR OWN in MINE, a BUGS space (DRAFT)
- `efac78c8` qa: C-474 THE SPELL LEFT RUNNING on the LIBRARY shelf (DRAFT)
- `3d06e491` C-474: THE SPELL LEFT RUNNING exported for the companion's LIBRARY -- gensubtle shadow_book()/shadow_images(), companion_export's shadow.json and plates, shelfcovers' cover (companion 37936d50)
- `97406d2f` qa: T-604 stage 3, fifteen later forms, built (v11.412.10)
- `486a2d13` README and wiki: latest is v11.412.10
- `d4da548c` ROM release v11.412.10: T-604 stage 3, fifteen more later forms colour in as they learn their part (DRAFT)

## The design bible's own entry for v11.413

### v11.413 — 2026-11-23

- **9.36 THE SONG -- the keys approved** (T-594; the user, 2026-11-23): the eighteen types' keys as drafted in v11.407 -- each tonic the note whose colour is nearest the type's own, CONTENT C major, CONTEXT its relative A minor, six spare -- are the user's now, no longer DRAFT. Nothing rebuilt: every song is already in them.
- Section 10: one Settled entry.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
