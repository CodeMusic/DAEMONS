# DAEMONS v11.288.1 — release notes

*Released 2026-09-25 18:00 · built against the design bible v11.288*

- **Engine**: CodeMusic/pokefirered-daemons `c38b70e32` (context-content)
- **Design**: CodeMusic/DAEMONS `75c5d3ac`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `47cd2fb887d105922852d4df6fe27e8a338bc0d7` |
| `daemonsContext.gba` | CONTEXT | `d90e4766794e29d1af3e6af4ea46fd545884eb45` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `c88299735fc2b4fd2960cf242da6361d49eaf105` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `838687f933527b4eaa3f116200eee4e4c4968aa9` |

## The engine since v11.287.7

- *nothing: the same engine commit as the release before*

## The design and tools since v11.287.7

- `75c5d3ac` v11.288: The Folds of Awareness cited as 4.33's second source; FOLDS placed (T-285); Scorn's doorway (T-284); Ty's approach asked (T-286); engine.md trap 33
- `b7450208` ROM release v11.287.7: Scorn out of the warehouse doorway; LOOSE PAGES 7 (DRAFT)

## The design bible's own entry for v11.288

### v11.288 — 2026-09-25

### *The Folds of Awareness*, and a door nobody could walk through

- ***A second source for the one daemon*** (4.33; `lineage.md` 5, 4.6): **the user's essay *The Folds of Awareness* (Seeing Sharp, September 2025)** *— one sheet of awareness folded and never cut, a great hand and many small ones, and free will left unanswered, which is 4.33's own rule.* **Its order is what is new**: *change (time) before space, a binding fold, the mirror, pattern, the return.* *Where it already sits in the game — the watches and the week, BIND, PERSPECTIVE, DOLDRUM read and unread, T-188's choice — is written down, and none of it was placed on purpose.*
- ***LOOSE PAGES 7, FOLDS*** (DRAFT, T-285): **folding instructions pinned where the Condominiums 3F's lower painting hangs**, *six steps and a half, every one only paper; not the scientist's, so THE TEST in 4.33 still holds.*
- ***Scorn stood in the only doorway to Ty's room*** (T-284): *placed 2026-09-10 "five tiles from Ty and facing him", on the one tile into the Rocket Warehouse's last room, so the PAYLOAD — and CRYSTAL's ending after it — could not be reached in play for fifteen days.* **He now stands on Ty's own row, five tiles off and facing him, in the room's alcove.** ***Found by `tools/check_reach.py`***, *new: it walks every map from where a player arrives and reports what we made unreachable against a pristine upstream. It also moved CORRESPONDENCE 2's reserved spot off a wall the CONDOMINIUMS 3F's Designer seals off, to the roof room's bookshelf.*
- ***Ty's approach walks onto the player*** (T-286, **asked**): *after the battle he steps down into the only tile you can talk to him from.*

---

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
