# DAEMONS v11.313.1 — release notes

*Released 2026-10-27 13:49 · built against the design bible v11.313*

- **Engine**: CodeMusic/pokefirered-daemons `64fc90970` (context-content)
- **Design**: CodeMusic/DAEMONS `cbbc9c69`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `de92aad9c4ae6963fcef0fa3c658ed8e22089d65` |
| `daemonsContext.gba` | CONTEXT | `fb4aaecdd008e5ee29e33f2211d34c7b13fa4fd2` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `6ab53db21fd52ec1d6e14ebd4ee0a7e893ef9515` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `4ac303a10d4c9eb4928edeccf6a134eb354d738b` |

## The engine since v11.312.1

- `64fc90970` T-452 batch 3: SKEW to CONJECTURE (44-65) in the new style; grounding rows, icon palettes, overworld art, follower palettes
- `45321b45b` T-458: SOUNDINGS hears your daemon -- the receiver and the keepers name the AWAY daemon, by its signal

## The design and tools since v11.312.1

- `cbbc9c69` T-452 batch 3 built (engine 64fc90970): SKEW to CONJECTURE as gbasprite's sources; RESIDENT's rings, SPYWARE's eye spots, SPINLOCK's spiral, TAPPOINT's hole by hand
- `00d03b36` TODO: T-458 built (engine 45321b45b) -- SOUNDINGS hears your daemon; companion_export exports sounding_shift 6 (C-195)
- `c56c9a0c` Bible v11.313: SOUNDINGS (4.37 settled, 9.30 new; T-457, T-458, C-195)
- `d2b8f504` TODO: T-458 SOUNDINGS hears your daemon (the user's decision)
- `37ea66c9` TODO: T-452 batch 3 approved with hand fixes (the user's answers)
- `88aae388` T-452 batch 3 drafted: SKEW to CONJECTURE (44-65) by the charm recipe, icons by icon3, grounds off ten (gfx/drafts/t452/f)
- `8ff13f26` qa: v11.312.1's sheets (T-456)
- `69923fbf` ROM release v11.312.1: the REVIEW BOARD's name card (T-456); T-457 in the user's words (DRAFT) -- SOUNDINGS, the receiver and its sprite, CRYSTAL's line at the receiver; v11.311.x sealed

## The design bible's own entry for v11.313

### v11.313 — 2026-10-27

### SOUNDINGS (T-457, T-458, C-195)

- ***4.37 settled (the user)***: **CRYSTAL's work is SOUNDINGS**, *the Act 2 seed a sign on ONE ISLAND, and every word approved as DRAFT* -- **PROSPECTUS 8 answers PROSPECTUS 3 line for line.**
- ***9.30 (the user, by multiple choice)***: **SOUNDINGS hears your daemon** -- *the receiver and the keepers name the player's AWAY daemon; the companion writes a four-level signal into the flags byte's two spare bits at each SYNC (doing well, fine, quiet today, no signal yet), one `sounding_shift` key serving both sides; the app gets a SOUNDINGS view, heard and never ranked.*

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
