# DAEMONS v11.358.1 — release notes

*Released 2026-11-12 18:21 · built against the design bible v11.358*

- **Engine**: CodeMusic/pokefirered-daemons `78dbb3ae2` (context-content)
- **Design**: CodeMusic/DAEMONS `5bc9a2c4`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `b736ddb9fb276ed8406520463ed29cce3a00501d` |
| `daemonsContext.gba` | CONTEXT | `862b34166fef7f163aceace6e9491ab8d2570207` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `a416270c46f4ba36dc7b00fd64df3a5347f4aec6` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `7837c8b7e96d946fbb98a24f23b582c7630449f8` |

## A note on the book audio

A minor release, released with two recordings deferred (the user, 2026-11-12: "Release now, record after"): THE COMPANION's manual changed since its recording, and the new T-GLASSES book has not been recorded yet. Both are made after this release. The printed manuals are current.

## The engine since v11.356.1

- `78dbb3ae2` Merge T-547 THE BLANK TABLET (the Unity Book lane; the user approved the words 2026-11-12)
- `b9062d63a` T-445: KEEPALIVE PLANT's card exits as a CAVE card -- flash and nested rectangles, as MONEAN and DOLDRUM
- `80832812d` T-447 pair 7: the S.S. ANNE's wake wholly behind her hull (y 121), and the player in front of her funnel at the pier's end
- `38d8a4400` T-547 THE BLANK TABLET in BLANCHE and the old toad by the pond (DRAFT)
- `26cbfd1ae` README: the release line names v11.356.1

## The design and tools since v11.356.1

- `5bc9a2c4` T-540: the user's picks for every WALLED GARDEN line (85 of 85, by multiple choice in chat, 2026-11-12) -- docs/walled-garden-picks.json
- `62e62db3` THE COMPANION manual: THE CALENDAR, the fork and its bowl, and SETTINGS' THEME tab with the game's accents (C-349..C-355, C-341)
- `a79b6e51` qa: companion C-221 -- the link cable in the GAME tab (12Nov 29)
- `3f5b52c5` qa: companion C-221 -- the linked pair on roverbyteseer (12Nov 28)
- `51172251` qa: companion C-221 -- a TRADE CENTER trade between two linked games (12Nov 27)
- `5b0bb8dc` T-445 (engine b9062d63a): KEEPALIVE PLANT's card exits as a CAVE card, filmed; the popup after a CAVE card is vanilla's
- `a53953d2` T-447 pair 7 (engine 80832812d): the S.S. ANNE's wake behind her hull and the player in front of her funnel, filmed
- `8c37c1b3` THE COMPANION manual: the DREAM JOURNAL and the signs (C-356), from build 975's notes (C-341)
- `cea27f7d` TODO: T-548, T-549, T-550 picked by the user -- "Still me.", "A direction, not a verdict.", "A read: the room is thinking one thought." (half as often)
- `bc914bf4` qa: companion C-349..C-355 -- THE BLACKOUT accent, SETTINGS' THEME tab, the singing bowls, THE CALENDAR (12Nov 18-23)
- `a9c58d27` Route backlog_2026-11-12: film the 11/12 Nov backlog in the theatre -- the S.S. ANNE's departure burst, the KEEPALIVE PLANT, MONEAN and DOLDRUM cards (with and without the understanding), TANOBY's back walls, T-542 batch 4's three edges, and T-447 pair 6's AL CLEAR room and HALL OF FAME
- `9085499e` T-547 BUILT (engine branch t547-blank-tablet 38d8a4400; not released): THE BLANK TABLET by BLANCHE's north path and the old toad by the pond; tools/genblanktablet.py draws both and writes the words from docs/blank-tablet-draft.md; bible v11.358 (4.39); qa 12Nov T547 17 (DRAFT)
- `579ed653` qa: C-357 THE SUBTLE LAYER, lived, on the site (12Nov 16; companion 722dc55)
- `a6344c88` TODO: T-548 CONTAINER at evolving, T-549 SAY INSTEAD at naming, T-550 CHORUS in crowds -- THE SUBTLE LAYER's pages made play, drafts for the user's pick (the companion's half is C-357)
- `163d37b1` qa: C-356 the dream journal and its signs (companion fdb9cef)
- `9c752287` qa: C-190's card and C-337's THIS PHONE seen in the iOS app (Simulator)
- `55daf5a8` C-262: THE GLASSES, a manual for the T-Glass (12 pages, DRAFT) -- tools/manual.py's tenth book, read from the companion's glass firmware, its GLASSES card and wiki The T-Glass: first steps (fitting the picture, pairing by a three-second hold), the four screens, the care's moment and the morning's dream, the button, GLASSES in the app, the battery and trouble; two drawings; the glasses on its cover (manual_devices), its shelf cover, its own voice (bookaudio: near, picked by the user from three samples), releasedocs routes the glass firmware and card to it
- `369b34cc` Bible v11.357: THE BLACKOUT dark from the first line (T-546, v11.356.1); four stale lines from today's map of THE SUBTLE LAYER -- 51 entries, MOM's ship line ends when the ship sails (T-504), friendship saturation built (T-424), T-459 closed
- `2490fef6` qa: C-166, C-217, C-339 seen on the site; C-190's card acts (companion 6761f3b)
- `6bf7fe00` T-547 filed and drafted: THE BLANK TABLET in BLANCHE (night front, dawn back, both mended; a thirteenth line a face) and the old toad who says the lean (the user, 2026-11-12, by multiple choice; every word DRAFT)
- `68e2480e` README and wiki Home name v11.356.1
- `6da2df34` ROM release v11.356.1: THE BLACKOUT's dark through the field stage -- no lit scanlines at the top (T-546, engine 9b620f0d7); seals v11.355.x

## The design bible's own entry for v11.358

### v11.358 — 2026-11-12

- **4.39, the Blank Tablet built (T-547)**, from the user's picks by multiple choice:
  - The stone stands by BLANCHE's path north.
  - Each half of the third book reads one face: the night half the front, the dawn half the back, the mended book both.
  - Each face has its own thirteenth line, in its own hour, shown until read once.
  - The witch is an old toad by the pond, who says only the player's lean.
  - The words are in `docs/blank-tablet-draft.md`. DRAFT.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
