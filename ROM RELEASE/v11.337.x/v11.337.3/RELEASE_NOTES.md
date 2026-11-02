# DAEMONS v11.337.3 — release notes

*Released 2026-11-02 08:05 · built against the design bible v11.337*

- **Engine**: CodeMusic/pokefirered-daemons `b51e8e892` (context-content)
- **Design**: CodeMusic/DAEMONS `5c929f48`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `0f27fd45a491fa81fa76df9455de0fe51cde97f0` |
| `daemonsContext.gba` | CONTEXT | `21e3e897da1ca356bfbdc18204d225c794ee1a88` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `62696e00c4ba0f549b73e9723db271ceaceb154f` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `15a0d1a509dbdbfba2c4cc9848d4090a04ff500b` |

## The engine since v11.337.2

- `b51e8e892` T-515: the lioness's card home, filed in LOOSE PAGES as an echo of CORRESPONDENCE 7 (DRAFT)
- `83f3cb8cf` T-514: the USER card's bands light the GUIDE's centres -- each MARK the centre its virtue keeps in the week
- `8b126b2df` T-512: the INTERPRETER, once THE SUBTLE LAYER is taken: "Ask before you read anyone." (DRAFT)
- `ae6eb56d5` T-511: each read in THE LOG keeps its weekday, and reads come a little more often on a FRIDAY (DRAFT)
- `0c0fad1ba` T-510: CLOSURE rises one at a battle's start while the INSIGHT of today's virtue is held (the GUIDE's week)

## The design and tools since v11.337.2

- `5c929f48` TODO: T-510, T-511, T-512, T-514, T-515 done (engine 0c0fad1ba..b51e8e892); T-513 and T-516 drafted for the user
- `afa24639` T-510..T-515: THE SUBTLE LAYER's loose ends -- the CARD HOME's NOTEBOOK line, the route that films them, and the pictures
- `931a91a6` bookaudio.py: a compound says DAY-mon too (eudaemon, cacodaemon, agathodaemon keep their prefix); the counterbalance is sealed by default
- `adb8001a` TODO: T-518's commit is 1b507643 (6a8cb011 before the rebase)
- `d0ea573a` TODO: T-518 done for the three written books (6a8cb011); the counterbalance's half waits in "dawn" for its text
- `1b507643` T-518: the books read aloud again -- every daemon said DAY-mon, each book in its own voice
- `ca0b8789` ROM release v11.337.2: T-483 (5) FIELD's intent -- the foe telegraphs its routine by its type's colour and a motion

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
