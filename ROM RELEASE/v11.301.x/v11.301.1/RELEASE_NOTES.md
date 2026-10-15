# DAEMONS v11.301.1 — release notes

*Released 2026-10-15 09:49 · built against the design bible v11.301*

- **Engine**: CodeMusic/pokefirered-daemons `2fdd445e3` (context-content)
- **Design**: CodeMusic/DAEMONS `abe90152`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `ae9abcc3f7b5a1ca50ee7c5679fb99b9efb9a0a4` |
| `daemonsContext.gba` | CONTEXT | `6ec542a9ddd8c213c48f0c77dcaa47c2826a3f27` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `03e7c0d189091ed533cc82c119acd6dae6068ba6` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `e85852f64a37a2faf5865b2353475fa39c0ce1dd` |

## The engine since v11.300.1

- `2fdd445e3` T-402 (the user, 2026-10-15): every NOTEBOOK page from a song of the iASHC opera found public ends on a QR code to its track -- ten songs, sixteen pages; notebook.c's sPageQr says which page carries which code, and the codes' enum is generated beside them
- `56b932830` T-401 (the user, 2026-10-15): FOLDS names each fold -- AWARENESS, CHANGE, SPACE, MIRROR, PATTERN, RETURN -- because as only paper it read as paper; THE STONE says what nobody at home sees, and FIELDS no longer breaks a sentence across a page

## The design and tools since v11.300.1

- `abe90152` T-402 part (engine 2fdd445e3): ten songs' codes in tools/gbaqr.py, which now writes the enum too; TODO lists the songs still waiting on the user's links
- `3de5fb5c` T-401 part (engine 56b932830; the user, 2026-10-15): FOLDS names each fold, THE STONE and FIELDS made plainer. Bible v11.301 (4.33's paper-only FOLDS to Reversed; lineage 4.6), CHANGELOG, PDF cut, v11.300's removed.
- `6439bca8` TODO: T-401 (loose pages legible as what they transcribe; dialogue flow) and T-402 (a QR code after every blog- or book-based page) -- the user, 2026-10-15
- `fd9fb96f` ROM release v11.300.1: MIND READER is ANTICIPATE (T-393) and the AQUA admin is a tiger shark (T-120); v11.299.x sealed into its notes PDF

## The design bible's own entry for v11.301

### v11.301 — 2026-10-15

### The loose pages say what they are about (T-401)

- ***4.33 and LOOSE PAGES 7, reversed (the user)***: **FOLDS names each fold** -- *AWARENESS, CHANGE, SPACE, MIRROR, PATTERN, RETURN, the essay's own order -- because as only paper it read as paper ("it isnt clear that it is talking about awareness"). The essay's conclusions stay out (craft rule 1) and it still never mentions the scientist (NEVER ADJUDICATE). See Reversed.*
- ***LOOSE PAGES 1 and 3 (the user)***: **THE STONE** *now says what nobody at home sees ("they say I see things that are not there"; the rule "sat still long enough to copy down"), and is approved;* **FIELDS** *no longer breaks a sentence across a page, and ends "To me it is all one room."*

---

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
