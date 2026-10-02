# DAEMONS v11.291.2 — release notes

*Released 2026-10-02 13:11 · built against the design bible v11.291*

- **Engine**: CodeMusic/pokefirered-daemons `33980cc15` (context-content)
- **Design**: CodeMusic/DAEMONS `8d116edd`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `0f4de3eff0a87b7523ac8b2335fb1967c159e912` |
| `daemonsContext.gba` | CONTEXT | `038f001bc611be99e9c9bbfa53a3c9e9fc607f4d` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `73c7c76925029d45afec93bb12fb80965cd1091a` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `874e848e314627bbb69581a14a2ebd803226f166` |

## The engine since v11.291.1

- `33980cc15` T-210 batch 1: the six starter lines of Johto and Hoenn named, written and drawn (approved by the user)

## The design and tools since v11.291.1

- `8d116edd` T-210 batch 1: the art (gfx/daemons, gfx/drafts/t210b1 with its scripts and picks) and the ticket
- `de15ddc8` engine.md trap 40: the theatre no longer opens in the user's emulator
- `abcff30a` T-210 batch 1 drafted: the six starter lines of Johto and Hoenn, named by their type's register (DRAFT, for the user)
- `b11e9ec7` T-210 started with the user: names by type, the legendaries last, the six starter lines first
- `f2e8a220` TODO: T-346 and T-347's drafts approved by the user
- `48a21d92` qa: T-317 played
- `6d7a9461` ROM release v11.291.1: the world's colours come back as you understand it (T-317) -- and v11.290.x sealed

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
