# DAEMONS v11.289.2 — release notes

*Released 2026-10-01 16:25 · built against the design bible v11.289*

- **Engine**: CodeMusic/pokefirered-daemons `d0a2edbd8` (context-content)
- **Design**: CodeMusic/DAEMONS `91978a26`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `3d77c6ba3aaf22e77fc15de86b7df0320480eead` |
| `daemonsContext.gba` | CONTEXT | `33f10df91ea7da86d67c0c8cfb4bd9005cf00f61` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `cc91e989fa02fafd567b4bf992bb945857dc475d` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `ca7075491a4a8301b878b38bc4681ffd93700244` |

## The engine since v11.289.1

- `d0a2edbd8` T-335: the dated documents (DRAFT) -- CORRESPONDENCE 1 on 2F of the tower, PROSPECTUS 3 dated and placed, the minute, the errand page, the fitness letter, the nine items and the routing slip each carry their dates; a staff notice on the lab wall; every list item and signature on its own line again

## The design and tools since v11.289.1

- `91978a26` T-335 closed: the dated documents are in (engine d0a2edbd8); gbadocs keeps a single newline as a deliberate break, so lists and signatures stop running together; T-224 records PROSPECTUS 3 placed
- `5f834f50` TODO: T-335 the dated documents take their dates from the user's own record (private), T-336 a review of that record with the user
- `7dabd31b` TODO: T-334 trading past the first 151 is blocked (the user: leave it for now); T-333 scheduled for the next goal pass
- `6292ab5f` TODO: T-321 and T-327 closed -- the dialogue review is in (engine f44f0ffea), the 29 CONTEXT drafts and CRYWOLF are in (447796feb, 75f3ebda6); both released in v11.289.1
- `351abca1` ROM release v11.289.1: the brain fills lobe by lobe, two-column START menu, no INDEX gate, MOM's own lines, the poster, the three reviews applied; v11.288.x sealed

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
