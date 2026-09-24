# DAEMONS v11.282.1 — release notes

*Released 2026-09-24 09:29 · built against the design bible v11.282*

- **Engine**: CodeMusic/pokefirered-daemons `1716ca57b` (context-content)
- **Design**: CodeMusic/DAEMONS `fd63fc9b`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `6cc50fb754d064c5155e538df6d1d627e43e7edd` |
| `daemonsContext.gba` | CONTEXT | `300defc7c1f407d95992000fba4f0cacf0444c72` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `0a7d34f8c8390849b80bf8be55fff7943b096e7f` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `52c6ef532ae77d7df38ce57aa946c3881ead04cd` |

## The engine since v11.281.3

- *nothing: the same engine commit as the release before*

## The design and tools since v11.281.3

- `fd63fc9b` v11.282: a day of pushes, built
- `9e0a2946` T-221: where the groves could go, surveyed; four real lone trees, the rest to be planted
- `64ddde2e` ROM release v11.281.3: the INDEX's page, the readable stones, BPS patches

## The design bible's own entry for v11.282

### v11.282 — 2026-09-24

### A day of pushes, built

- ***OPUS's margins in two voices*** (T-188): **REASON's lines notice what you did, INSTINCT's what it was like** — *six written twice, DRAFT; the debug kit carries OPUS.*
- ***The send-out's colour flash, traced*** (T-254): **starting a fade copied the palette to the screen at once, past the drawing filter** — *found with the theatre's new `pburst`, which dumps palette RAM beside every frame.* ***engine.md trap 30.***
- ***The unresolved display is a latent before it is decoded*** (T-250): **the same seed stopped eleven steps in, inside the finished draft's outline** (`spriteforge.py --stop-at`, `gbaunresolved.py`).
- ***HALFTONE Tower's stones are encased screens, and can be read*** (T-249): **a headstone's housing, a dark screen of green marks; six lines, each an epitaph and a deletion record, DRAFT.**
- ***L turns an Index entry to its workings*** (T-189): **the line from its root and its routines by level, from the ROM's own tables** — *and SELECT's margin works on the family page's entries at last.*
- ***A MEME is explained, once*** (T-258): **at the CHECKPOINT, caught from another daemon and passed on** — *FireRed kept the check and never used it.* ***Memetics drafted*** *for INIT, his house and a MANSION log.*
- ***The INDEX writes a page about you*** (T-257): **CRYSTAL, home after the payload, lets it write; LAB NOTES keeps WHAT YOU CHOSE, rebuilt from the save** — *its words PLACEHOLDERS until approved.*
- ***ROM releases*** (T-259): **`tools/romrelease.py` files each build by version, seals a superseded version into one PDF, and makes BPS patches for all four retail ROMs** (`tools/bps.py`) — *ROMs and patches never in git; `ROM RELEASE/WHERES_THE_ROMS.md` says why.*
- ***Where the groves could go*** (T-221): **four real lone trees found; the rest to be planted, the user's to place.**

---

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
