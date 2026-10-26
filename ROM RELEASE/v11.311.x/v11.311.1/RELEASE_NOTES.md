# DAEMONS v11.311.1 — release notes

*Released 2026-10-26 17:26 · built against the design bible v11.311*

- **Engine**: CodeMusic/pokefirered-daemons `462fa562c` (context-content)
- **Design**: CodeMusic/DAEMONS `00407fff`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `1956ffbb79d1a0e911e1e2ca54d12eba0dd3cd1e` |
| `daemonsContext.gba` | CONTEXT | `b3c61f156ea85ecc3305e7c88815764895483dc2` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `879c688994650f87a896b5ec856cd8539788b8f6` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `99082e776dad922ec8ffb0c1b0997e048f016d85` |

## The engine since v11.310.4

- `462fa562c` T-452 round two: batch 2 (WORM to SPRAWL) and MANIFOLD's folded-paper manta in the new style; ROVERCUB ungrounded, LOCUS's back turned, RELAY's and BUFFER's backs at 58 cells; every batch-1 icon redrawn by icon3; grounding rows, icon palettes, follower palettes
- `cc13f6633` T-457: the second joining -- mechanics with DRAFT placeholders (bible 4.37)
- `49eb0d574` T-445: CORPUS WAREHOUSE's name card
- `4f24d5d37` T-445: CORPUS HIDEOUT's name card
- `3e7dd26bc` T-445: the landmarks' name cards -- FOUNDRY CO., DAEMON TOWER, the MANSION

## The design and tools since v11.310.4

- `00407fff` T-452 round two built (engine 462fa562c): batch 2 and MANIFOLD A as gbasprite's sources, Part A, every batch-1 icon by icon3; FORK's tail, PREDICTOR's horn and OUTLIER's earless back by hand
- `20235fc2` T-457: the second joining's mechanics built (engine cc13f6633); gbadocs places PROSPECTUS_7/8, placeholders listed
- `c0f196cb` qa: C-187 the GAME tab on the iPhone, before a game
- `bb9c226f` T-445: CORPUS WAREHOUSE's card built (engine 49eb0d574)
- `bb1a18a3` TODO: T-445 WAREHOUSE card B approved (the user's answer)
- `f9ede049` qa: T-445 HIDEOUT card built; WAREHOUSE repaint candidates
- `b71d2260` T-445: CORPUS HIDEOUT's card built (engine 4f24d5d37); the WAREHOUSE's repainted with a bigger spin-tile floor (draft)
- `537bc279` TODO: T-452 round two approved (the user's answers)
- `a9ea324b` qa: T-452 round two draft sheet
- `424625a5` TODO: T-445 HIDEOUT approved, WAREHOUSE to repaint (the user's answers)
- `9f170b48` T-452 round two drafted: batch 1's notes fixed, MANIFOLD a third round, batch 2 (WORM to SPRAWL) by the charm recipe
- `9a708294` Bible v11.311: 4.37 the second joining (T-457)
- `9ebbf829` qa: T-445 name cards built; HIDEOUT and WAREHOUSE drafts
- `71aa5ecf` T-445: CORPUS HIDEOUT's and CORPUS WAREHOUSE's name cards drafted from the current maps (gbapreviews --landmarks, interiors; not approved)
- `ea915f32` TODO: T-457 the second joining -- CRYSTAL's work in THE MARGINS, and a merger that holds both
- `6bf91eb2` T-445: the landmarks' name cards built (engine 3e7dd26bc) -- LANDMARK_APPROVED names all three
- `0e8b99e1` TODO: T-445 the name cards approved (the user's answers); T-456 a card for the REVIEW BOARD
- `b709e1b4` qa: T-445 landmark name cards, draft sheet
- `50fda243` T-445: the landmarks' name cards drafted -- CORPUS's tower, DAEMON TOWER, the MANSION painted from T-447's buildings (gbapreviews --landmarks)
- `8b2b7865` qa: v11.310.4's sheets (T-447 pair 3, T-452)
- `89e1b721` ROM release v11.310.4: T-447 pair 3 (the REVIEW BOARD, ERRATA) and T-452's twenty-five daemons in the new style

## The design bible's own entry for v11.311

### v11.311 — 2026-10-26

### The second joining (T-457)

- ***4.37 (the user)***: **after THE ANNEX, CRYSTAL takes up the network in THE MARGINS the player helped finish, and her INDEX joins CELIO's machine side by side, neither on top** -- *the inverse of Brazen's gold leaf.* **Seeded in Act 2, paid off after:** *a receiver on her desk picking up one daemon far away, two undated PROSPECTUS papers, Brazen's board without scores, the CHECKPOINT keepers listening to someone not in the room; she hands over the GLOBAL INDEX almost silently.* **SCORN unchanged, the gold never repainted, nobody rescued.** *The name of her work, the Act 2 seed and the words are open; the user is writing some of them.*

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
