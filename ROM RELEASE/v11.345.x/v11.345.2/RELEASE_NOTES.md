# DAEMONS v11.345.2 — release notes

*Released 2026-11-09 15:17 · built against the design bible v11.345*

- **Engine**: CodeMusic/pokefirered-daemons `850ec7286` (context-content)
- **Design**: CodeMusic/DAEMONS `f22b5c17`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `9b23f8f91550660a3f8b586c4a9acf7e193a32b1` |
| `daemonsContext.gba` | CONTEXT | `8fe0d1b32f57d9166dd3489befc46ccf7eeee6a5` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `d4e90eea73bfe10b6114063bd921854565936f44` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `79610927a69d8e50f5a1bca6597feabc6002c4f0` |

## The engine since v11.345.1

- `850ec7286` T-525 batch 4: 47 more item icons drawn by hand in code (the valuables, shards, MOOMOO MILK, LAVA COOKIE, five MAILs, four scarves, PEER REVIEW, ENVELOPE, METEORITE, POWDER JAR and the 20 berries on the TRAP TABLE's plank), each its own d_<item> files, its row repointed

## The design and tools since v11.345.1

- `f22b5c17` T-525 batch 4 built (engine 850ec7286): the user, "Build all" and "Keep all 20" -- ICONS4 in APPROVED, --all writes all four batches (192 icons), check_generators' report exits 1 on drift; four ROMs exit 0, filmed qa 9Nov2026 T525 9-12 (DRAFT)
- `6504e635` TODO: T-533 THE ORIGIN OF A DAEMON (a private outline first) and T-534 the MUSAI branch with grace (words first), both drafted in docs/private
- `18749c23` qa C309 5-6: the voice module in a book's look (THE SUBTLE LAYER, PRINCIPLES OF MIND)
- `fdc9f402` T-525: batch 4 of the item icons drafted -- 47 drawn by hand in code (the valuables, shards, MAIL, scarves, four key items, the berries on the TRAP TABLE's plank), nothing in the engine (DRAFT)
- `922cf2bf` port_index: a whole-tree --write refuses (driftguard), the report names every row it would change, and check_generators runs it
- `cf8375b2` ROM release v11.345.1: T-532 the MUSAI branch's seasons -- six daemons in four seasonal forms each, following the edition's season; CODEMUSAI's CRYPTOPHASIA; 24 INDEX entries; seals v11.344.x

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
