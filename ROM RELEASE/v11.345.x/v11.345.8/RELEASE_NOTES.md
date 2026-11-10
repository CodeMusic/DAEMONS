# DAEMONS v11.345.8 — release notes

*Released 2026-11-10 11:01 · built against the design bible v11.345*

- **Engine**: CodeMusic/pokefirered-daemons `ae8998672` (context-content)
- **Design**: CodeMusic/DAEMONS `b40a309f`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `84ec45a4c6ad6cc4444687f81a6099397d6ac5b9` |
| `daemonsContext.gba` | CONTEXT | `c1c7160dc130591f10c1dd2cfba495b5f544e7d5` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `8e2af7d4a706aebbc1a735e5fd30559dd82603b3` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `7555f51600b8dc667aabd20bda6f1bc623e79e46` |

## The engine since v11.345.7

- `ae8998672` T-538 batch 2: the teleporter door's frames redrawn from the WORKBENCH lab's closed block (gbadoors --write --approved; it fell behind the tileset)
- `32987f0ac` Merge origin/context-content (T-538 batch 1 from the game lane) into local (T-538 batch 2, T-539)
- `5b85fc3fc` T-538 batch 1, A HEARTH: the road houses, the COPYCAT's room and primary/building's 33 leftovers redrawn in place (DRAFT)
- `987ef11ad` T-539 A, PASSING: THE UNITY BOOK's LENS picture draws the Field as the FIELD page's passing daemons, not the old ')' marks (DRAFT)
- `b2046f01a` T-538 A HEARTH (batch 1) and A THE WORKBENCH (batch 2): the road houses, the house leftovers and the workrooms redrawn in place (DRAFT)

## The design and tools since v11.345.7

- `b40a309f` Merge T-539 (A PASSING, engine 987ef11ad) from claude/eloquent-euler-073d41
- `9079a166` Merge main (T-538 batch 1 built by the game lane, 5b85fc3fc) into T-538 batch 2: keep main's gbahomes, add gbaworkrooms; batch 2 sheets renumbered qa T538 16-21
- `b8a754ae` T-538 batch 1 built (engine 5b85fc3fc): A HEARTH -- the user, 2026-11-10: "A Hearth"; gbahomes APPROVED {A}, its report checks the engine; four ROMs exit 0, sheets qa 10Nov2026 T538 6-14, route t538_hearth (not filmed); DRAFT
- `a1645f37` T-539 built (engine 987ef11ad): A PASSING -- u_lens draws the FIELD's passing daemons, not the old ')' marks; four ROMs exit 0; not yet released or filmed (DRAFT)
- `1d818f50` T-538 built (engine b2046f01a): batch 1 A HEARTH, batch 2 A THE WORKBENCH -- the user, 2026-11-10; gbahomes/gbaworkrooms APPROVED {A}, reports check the engine, check_generators runs both writes; four ROMs exit 0, sheets qa 10Nov2026 T538 10-12; DRAFT
- `8db992da` TODO T-540: the user's answers -- line-by-line picks, RINGS count down 3..0, FIRST MET drops THE
- `4432afc2` TODO: T-533 -- the user's direction, 2026-11-10: nouns are verbs, matter a self-stable loop in the field, the physics told as the lore
- `7e015049` TODO: T-539 -- the user's pick, A PASSING (2026-11-10, by multiple choice); not yet built
- `c7b231a7` TODO: T-538 picks -- the user, 2026-11-10: batch 1 A HEARTH, batch 2 A THE WORKBENCH
- `d99b23a9` TODO: T-539 drafted (3f169445), waiting on the user's pick
- `3f169445` T-539 drafted: the mended LENS's ')' marks -- u_lens's field outside the lens in batch 4's language, three directions (A PASSING, B FIELD BELOW, C BENT GRASS), DRAFT; nothing in the engine before the pick
- `c65973be` T-538 drafted, batch 2: the workrooms -- bike shop, HOLT's SEA COTTAGE, the QUICKSILVER lab -- three directions (A THE WORKBENCH, B THE CLEAN ROOM, C THE SALVAGE YARD)
- `ca425231` T-540 drafted: THE WALLED GARDEN -- the SAFARI ZONE as a curated, walled platform run as a sandbox (DRAFT, nothing in the engine)
- `719736ad` T-538 drafted, batch 1: the road houses and the houses' leftovers -- three directions (A HEARTH, B THE WAYMARK, C FOUNDRY TOWN)
- `f79e318c` TODO: the user's answers 2026-11-10 -- T-437 rebuilt for judging, T-538 the other interiors, T-539 the mended LENS's marks
- `7e2e8574` ROM release v11.345.7: T-537 the desks and machines in A, FOUNDRY STOCK (DRAFT)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
