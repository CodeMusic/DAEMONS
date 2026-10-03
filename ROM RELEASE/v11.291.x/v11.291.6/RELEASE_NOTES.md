# DAEMONS v11.291.6 — release notes

*Released 2026-10-02 23:00 · built against the design bible v11.291*

- **Engine**: CodeMusic/pokefirered-daemons `b037ad549` (context-content)
- **Design**: CodeMusic/DAEMONS `a1bf12d7`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `815d42ddd0618447eebd13cad2ab77d75749742f` |
| `daemonsContext.gba` | CONTEXT | `739c2c7c3c594628cb65ba97e36d10b56a30b636` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `426ac3961561346a1971e6bdd3b83cbcfe52ad68` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `7305dcd7b54e4a85f2606ee99bab07b542394ceb` |

## The engine since v11.291.5

- `b037ad549` T-210 batch 5: the early Hoenn routes named, written and drawn (DRAFT)

## The design and tools since v11.291.5

- `a1bf12d7` T-210 batch 5: drafts, art and picks (engine b037ad549)
- `967dd3d5` tools/t210check.py: a T-210 batch's words checked before they go in
- `4f15e9d0` T-210: batch 5 is the early Hoenn routes, as a goal loop (the user)
- `1b93910b` qa: T-210 batch 4 as built
- `ea3ab76d` ROM release v11.291.5: UNROLL, and the dragons and fossils named, written and drawn (T-210 batch 4)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
