# DAEMONS v11.314.1 — release notes

*Released 2026-10-27 20:09 · built against the design bible v11.314*

- **Engine**: CodeMusic/pokefirered-daemons `8efc0d0de` (context-content)
- **Design**: CodeMusic/DAEMONS `a6945194`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `a57eda4c85b4a6b5ac10872c95f6e9f361d1de04` |
| `daemonsContext.gba` | CONTEXT | `074c8ffb1cc69dda5465ba8a4ee98685dd9f0694` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `f07a2a97d50666c52c27c726ea3990037b56f72e` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `a639ac423b479c4dca10d2a150c7fd1350c807e4` |

## The engine since v11.313.1

- `8efc0d0de` T-454: THE THREE wake with THE SUBTLE LAYER; tuning approved
- `0454701a2` T-454 follow-up: THE THREE's last line drops "they say" too -- "A daemon carries them as numbers it cannot see" (the user, 2026-10-27; gensubtle --write)
- `f020c9c9d` T-461: object sprites past 255 -- a 12-bit graphics id in bytes the save already had
- `edb60dfd8` T-454 follow-up: THE SUBTLE LAYER's THE THREE drops "Trainers say" -- the three values are the game's now (gensubtle --write)
- `3d9e706f6` T-454: THE THREE -- CLOSURE, ATTUNEMENT, VOLTAGE, per daemon, battle only (DRAFT tuning)
- `105492f9d` T-459 A: once THE SUBTLE LAYER is held, the follower notices first, in the book's purple
- `3d467a371` T-461: three object graphics ids freed for new sprites, no save touched
- `58ed63b7a` T-452 batch 4 follow-ups: LEMMA MIND's arms crossed in front, HONEYPOT a honey pot, STACK a boulder, QUORUM three pods
- `be0764027` T-460: the desk's props drawn 8px up, clear of the player's head (the user, 2026-10-27)
- `ea63fc73d` T-457, T-458, T-460: the SOUNDINGS words approved (the user, 2026-10-27, after the theatre run)
- `a6aa85764` T-452 batch 4: PROOF to TRIPLECORE (66-85) in the new style; grounding rows, icon palettes, overworld art, follower palettes
- `938341cd2` T-460: the arc around SOUNDINGS closes -- the card, the tag, the bench, the flowers (DRAFT)

## The design and tools since v11.313.1

- `a6945194` TODO: T-454 -- THE THREE wake with THE SUBTLE LAYER; tuning approved (engine 8efc0d0de)
- `afe2510c` T-454 follow-up (engine 0454701a2): THE THREE's last line drops "they say" too, the user's call
- `bc044bd0` T-461 phase 2 built (engine f020c9c9d): object sprites past 255; check_objgfx and gentowns take 256 up; the recap's stand-in
- `f6685042` T-454 follow-up (engine edb60dfd8): THE THREE drops "Trainers say"; companion_export leaves the DEBUG THE THREE page out (PG_THREE, a setting like FEELINGS)
- `31abafe3` check_generators: CHECK_GEN_LIMIT raises the per-tool limit on a busy machine
- `1e1bc311` TODO: T-454 built (engine 3d9e706f6) -- THE THREE, derived per battle, nothing saved; DRAFT tuning in include/daemons_three.h
- `83965935` T-459 A built (engine 105492f9d): the follower notices first, in the book's purple; {COLOR PURPLE}
- `346b4f05` T-461 (part): three object graphics ids freed; check_objgfx; gentowns takes FREE ids (engine 3d467a371)
- `d23dbcee` T-452 batch 4 follow-ups built (engine 58ed63b7a): LEMMA MIND's arms in front, HONEYPOT's lid and bands, STACK a boulder, QUORUM three pods
- `d921d748` T-451 and T-436 closed: played in the theatre; qa: the desk props and the surf check
- `454d97c9` TODO: T-461 room for more object sprites (the user's ask)
- `fcc9a06b` T-457, T-458, T-460: the SOUNDINGS words approved; the desk's props drawn up (engine ea63fc73d, be0764027)
- `bb2bb13d` Bible v11.314: the arc around SOUNDINGS closes (T-460), played through and approved
- `4f48331e` TODO: T-452 batch 4 follow-ups (the user's answers)
- `a9c47016` check_fresh_clone: a detached release worktree clones the origin branch at its tip
- `ad7bba26` theatre routes: SOUNDINGS played through (T-457, T-458); field-test-release stop 18 fixed
- `ed439b85` T-452 batch 4 built (engine a6aa85764): PROOF to TRIPLECORE as gbasprite's sources; LEMMA MIND's four arms and EDGECASE's stilt legs by hand
- `fab250c8` T-460: the arc around SOUNDINGS closes -- built (engine 938341cd2)
- `a20d9a14` qa: the companion on the iPad simulator -- the game beside it (C-189), the planner (C-191), SOUNDINGS (C-195)
- `17e4ec53` TODO: T-460 after T-459
- `ad908429` TODO: T-460 the arc around SOUNDINGS closes (the user's decision)
- `38e32af6` TODO: T-459 THE SUBTLE LAYER's intuitions in CONTEXT's purple (the user's decision); notes D4; qa mock-ups
- `a131c2f0` T-453 the planner's data: companion_export.py writes planner_story/maps/wild/trainers/curve.json
- `7eb6685d` TODO: T-451 built (3c9f762e), waiting on a real theatre run
- `3c9f762e` T-451: the theatre's warps fire where the game says, and nothing waits forever
- `64b37465` qa: v11.313.1's sheets (T-452 batch 3, T-458)
- `83072aac` ROM release v11.313.1: T-452 batch 3 (SKEW to CONJECTURE, the user's hand fixes); T-458 SOUNDINGS hears your daemon (DRAFT); v11.312.x sealed

## The design bible's own entry for v11.314

### v11.314 — 2026-10-27

### The arc around SOUNDINGS closes (T-460), and it is approved

- ***4.37 (the user, by multiple choice)***: **four small things join the arc** -- *CORRESPONDENCE 7 AT THE DOOR, a card of signatures on CRYSTAL's desk ("We never got to say it at the door."); an evidence tag on the receiver once THE FILE 4 is read; a half-built receiver on THE ANNEX's bench; flowers on her desk on OCT 3.* **The card closes the signatures motif: "Some are careful. Most are not."**
- ***Played through and approved (the user)***: **the SOUNDINGS route passes all 21 stops; every word of T-457, T-458 and T-460 is approved and the DRAFT marks come off.** *The desk props move so the player's hat no longer hides them. CELIO's name is "CELIO's machine" in a sentence and CELIO'S MACHINE on a letterhead, on purpose.*

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
