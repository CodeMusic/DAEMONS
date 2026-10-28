# DAEMONS v11.316.4 — release notes

*Released 2026-10-28 14:31 · built against the design bible v11.316*

- **Engine**: CodeMusic/pokefirered-daemons `589f9edf4` (context-content)
- **Design**: CodeMusic/DAEMONS `e6710892`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `0891567adc49667fc3968b5f293c17a211a5fc22` |
| `daemonsContext.gba` | CONTEXT | `1daf4639fb77a111b23bb431af1a4cc8a044d485` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `ed6e11efb3717def4a583b59f2832ad6204db7cc` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `c0da758aae2f1227f14539812e9c8aca0047ca28` |

## The engine since v11.316.3

- `589f9edf4` T-452 batch 16: SINKHOLE to CATHODE (332-354, 21) in the new style, on the RECOMMENDED choices -- hand-drawn keys (SINKHOLE's pincer jaws, DUSTDEVIL's dust funnel, CRACKLE's sparks, ARCFLASH's arc, PIXELBYTE's tail pixels, STOPGRAD's and STALEMATE's icicles, FEWSHOT's water drop, LOCKFILE's padlock, BREATHING's pearl, GUTFEEL's black pearl, ANODE's plus and CATHODE's minus on an ear), streak marks moved off DUSTDEVIL's chin and below GUTFEEL's pearl, the type-hue trap fixed (ICE blues, FIRE's brick, ELECTRIC's blue, PSYCHIC's pinks greyed into the ramp; CATHODE's ear indigo), backs the front mirrored with the face out, grounds off; grounding rows, icon palettes, follower art and palettes
- `e1f15ec1f` T-473 (C-219): trading between players, the game's half -- TRADING in byte 0x13 bit 3 (pokefirered's blockBoxRS): an AWAY daemon in a trade cannot be called home, by the app or the emergency way ("is in a trade", DRAFT); LOAN (bit 0) and TRADED_IN (bit 1, one-shot) in the u16 at 0x1E, bits 2-15 reserved, all sixteen through MON_DATA_ENCRYPT_SEPARATOR; a borrowed daemon is never released ("is borrowed", DRAFT), traded in-game or over the link, or trade-evolved; a TRADED_IN daemon is finished on load -- the INDEX, FIRST MET: A TRADE (a new FirstSeen kind, 0xFE), a trade evolution through GetEvolutionTargetSpecies(EVO_MODE_TRADE) on a copy (the EVERSTONE holds, EVO_TRADE_ITEM's item spent, only a default name follows, T-455's routines owed), "{name} arrived in a trade." (DRAFT); LOAN wins; an unfinishable slot clears the bit and logs it; DEBUG GAME EVENTS: A TRADE ARRIVES (HAUNTER) and A LOAN ARRIVES (KADABRA)

## The design and tools since v11.316.3

- `e6710892` qa: T-473 played in the theatre -- a trade arrives (HAUNTER -> GENGAR), a loan arrives (KADABRA, not evolved)
- `536a33c3` TODO: T-452 batch 16 built (engine 589f9edf4): 332-354 on the RECOMMENDED choices; questions in gfx/drafts/t452/u/questions.md
- `7ef261ab` T-452 batch 16 built (engine 589f9edf4): SINKHOLE to CATHODE (332-354, 21), on the RECOMMENDED choices (2026-10-28); drafts in gfx/drafts/t452/u, questions in u/questions.md (38 items), remaining.md (56 left, three batches) -- hand-drawn keys (SINKHOLE's pincer jaws, DUSTDEVIL's dust funnel, CRACKLE's sparks, ARCFLASH's arc, PIXELBYTE's tail pixels, STOPGRAD's and STALEMATE's icicles, FEWSHOT's water drop, LOCKFILE's padlock, BREATHING's pearl, GUTFEEL's black pearl, ANODE's plus and CATHODE's minus), streak marks moved on DUSTDEVIL and GUTFEEL, the type-hue trap fixed, backs the front mirrored with the face out; scripts batch16.py, chain16.sh, prep16.py, hand_b16.py, recolour16.py, icons16.py, ba16.py, ba16.sh, view16.py, grid16.py, grp16.py, build16.py and the batch 16 subjects
- `0cdb77d7` T-473 built (engine e1f15ec1f): the game's half of trading; companion_export reads the trade bits from struct BoxPokemon (trade_bits: trading_bit, trade_flags_offset, loan_mask, traded_in_mask) and leaves the two faked-trade debug rows out of the GAME EVENTS export; TODO records the user's loan ruling and the calls
- `5fcef267` qa: T-452 batch 15 sheets (v11.316.3)
- `72e60aca` manual: rebuilt for v11.316.3
- `18dd75e7` ROM release v11.316.3: T-452 batch 15 (PARTICLE to RIPTIDE, PENGUIN) on the recommended choices

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
