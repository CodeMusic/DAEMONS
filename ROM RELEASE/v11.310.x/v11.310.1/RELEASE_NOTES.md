# DAEMONS v11.310.1 — release notes

*Released 2026-10-24 19:29 · built against the design bible v11.310*

- **Engine**: CodeMusic/pokefirered-daemons `2d8265ba1` (context-content)
- **Design**: CodeMusic/DAEMONS `d2040d85`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `c65bbb9d2e5b447ed86560cfe0b667ab69d25237` |
| `daemonsContext.gba` | CONTEXT | `8f04a31565d814604d2a85c765d72756844ee48b` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `fbb3a84a36819cc21edccb8d4db8166424064a0e` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `ca1e25789551cdbefd81cc178c764884a42a7809` |

## The engine since v11.309.14

- `2d8265ba1` T-455: a daemon the companion evolved is offered its new species' routines on return
- `cf4454491` T-447: SCORN SOLUTIONS and the MANSION drawn from the story (the first pair, the user 2026-10-24)
- `888b17299` T-448: the load-time finish -- a daemon the companion grew or delivered is finished on Continue
- `5d9a9e16d` T-450: the carried line -- HANDSHAKE, TETHERING, COROUTINE in OLD_UNOWN_K/L/M (INDEX 395-397, MISSINGNO to 398)
- `b3751fe01` T-423: THE SUBTLE LAYER's text after the user's review (2026-10-24) -- the three values as trainer lore until T-454, a virtue at the wrong size casts a shadow, the last word in the author's voice, the lever page corrected; DAEMONS tools/gensubtle.py

## The design and tools since v11.309.14

- `d2040d85` T-447 first pair built (engine cf4454491); T-455 built and struck (engine 2d8265ba1)
- `d4e29b8b` TODO: T-450 struck -- built (engine 5d9a9e16d) and in the bible (9.27, v11.310)
- `11540dc7` Bible v11.310: a daemon carried can evolve away (9.26, C-184/T-448/T-455); HANDSHAKE, TETHERING, COROUTINE, the line that grows only while carried (9.27, C-185/T-450); one app, iPad first (9.28, T-453); the landmarks drawn from the story (9.29, T-447)
- `7631d0d2` T-454: the condition bytes are T-431's feelings now -- the three values need another home (the game lane, 2026-10-24)
- `41aa65a5` TODO: the user's answers on T-447, T-452, T-450; T-455 moves on return
- `e84184f6` companion_export: marks.json keeps where each understanding is found out of the public companion (the user, 2026-10-24)
- `a629af02` T-452 round two drafted: the six redrawn to the user's answers, props in the prompt, accents capped (gfx/drafts/t452/b)
- `606b0722` TODO: T-448 built (engine 888b17299) and struck; T-450 built (engine 5d9a9e16d), its bible entry still owed
- `aa0f824b` T-450: tools/gbacarried.py writes the carried line into engineGba (5d9a9e16d); its art cleaned into gfx/daemons; rear drafts; companion_export judges CARRIED; gbanexus leaves the INDEX count to it
- `e559d4eb` T-447 draft 2: SCORN's steel door and its red light, the form in six big boxes, the MANSION's one stain and rib cage (not written)
- `07e90485` qa: batch H built; T-449, T-447, T-452 drafts
- `6522aa31` T-423: the user's review of THE SUBTLE LAYER (2026-10-24) -- British kept, the three values softened and T-454 filed, a virtue at the wrong size, the last word in first person, the lever page fixed (engine above)
- `0de56ef3` TODO: the user's answers on T-452's pilot and T-447's first pair
- `c44f538e` companion_export: index cards keep where an understanding is found out of the public companion
- `56e04a1a` TODO: T-453 card colour decided (type match); planner data next
- `951e15a8` ROM release v11.309.14: LURID in acid and neon, the islands' weathered boards and drying nets, SOMEONE'S STONE's cairn, DENSE WOOD, THE SAME BUSH in salt scrub; the landmarks kept for their own art (T-438 batch F/H)
- `ee34966e` T-447 draft: gbalandmarks.py, SCORN SOLUTIONS and the MANSION drawn into their footprints (not written)
- `b7668ffb` T-452: the last PACKET back attempt (seed 4523, drew a front like the rest)
- `1ab88480` T-452 pilot drafted: six daemons in the sprite-server style, reduced to 64x64 by type (gfx/drafts/t452)

## The design bible's own entry for v11.310

### v11.310 — 2026-10-24

### A daemon carried can evolve away (C-184, T-448, T-455)

- ***9.26 (the user)***: **a daemon on the companion evolves there by the game's own rules for level, friendship, the hour and WURMPLE's split** -- *never items or trades.* **The game finds it evolved and finishes it on load**: *stats, INDEX, ability, and the routines its new species learns offered the first time it is seen.*

### The line that grows only while carried (C-185, T-450)

- ***9.27 (the user)***: **HANDSHAKE → TETHERING → COROUTINE, a sugar glider; SIGNAL, SIGNAL, SIGNAL/STRATUM; stats 250/360/485.** *bond = steps/1000 (20 000 a day at most) + days carried × 5 + cares + goals together × 3; `EVO_CARRIED` at 60 and 160, never met on the cart; the first from the companion on the first goal finished while carrying, one per save; Gen 3's unused slots, INDEX 395–397, MISSINGNO to 398 (3.4 amended).*

### One app, iPad first (T-453)

- ***9.28 (the user)***: **one self-contained iOS app -- the game patched on the device from the player's own ROM and never bundled, the companion, the LIBRARY and the NOTEBOOK**; *INDEX cards coloured by type match with the understandings held.*

### The landmarks drawn from the story (T-447)

- ***9.29 (the user)***: **the buildings the story turns on get art of their own, inferred from the story, rather than a retint of vanilla** -- *two at a time, a sheet and a yes before each pair.*

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
