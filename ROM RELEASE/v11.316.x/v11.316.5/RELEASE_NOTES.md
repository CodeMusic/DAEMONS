# DAEMONS v11.316.5 — release notes

*Released 2026-10-28 15:14 · built against the design bible v11.316*

- **Engine**: CodeMusic/pokefirered-daemons `5510824f2` (context-content)
- **Design**: CodeMusic/DAEMONS `bcf7cae3`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `27aa8db003b72bb003b949018ba0f9fee4c04c18` |
| `daemonsContext.gba` | CONTEXT | `ffe6ff424fe17a557b8d76ee357c12016e0f76fc` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `d48f8312cc84b8674e32da5db3a3348c8800f74f` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `b102cd3c8fa5ce433cccc02d4ac60f49141cf63d` |

## The engine since v11.316.4

- `5510824f2` T-452 batch 17: HONEYTRAP to SHALLOWS (355-375, 20) in the new style, on the RECOMMENDED choices -- hand-drawn keys (HONEYTRAP's sweet drop, rose-red out of STEEL's hue trap; DATAGRAM's bundle, TRADEWIND's cloud puffs, FADING's faded hem, FORGETTING's trailing wraps, LACED's poison drop, DAYDREAM's and MINDWANDER's thought bubbles, TRANSFER's fruit, WRAPAROUND's wisp of breath, BIFURCATE's pearl, DEEPWELL's lure bulb), SHALLOWS's streak marks boxed onto its body, the type-hue trap fixed (STEEL, NORMAL, GRASS, WATER, FIGHTING greyed into the ramp), backs the front mirrored with the face out, frames and grounds off; grounding rows, icon palettes, follower art and palettes

## The design and tools since v11.316.4

- `bcf7cae3` TODO: T-452 batch 17 built (engine 5510824f2): 355-375 on the RECOMMENDED choices; questions in gfx/drafts/t452/v/questions.md
- `8fbf240a` T-452 batch 17 built (engine 5510824f2): HONEYTRAP to SHALLOWS (355-375, 20), on the RECOMMENDED choices (2026-10-28); drafts in gfx/drafts/t452/v, questions in v/questions.md (34 items), remaining.md (36 left, two batches) -- hand-drawn keys (HONEYTRAP's sweet drop, DATAGRAM's bundle, TRADEWIND's cloud puffs, FADING's faded hem, FORGETTING's trailing wraps, LACED's poison drop, DAYDREAM's and MINDWANDER's thought bubbles, TRANSFER's fruit, WRAPAROUND's wisp, BIFURCATE's pearl, DEEPWELL's lure bulb), the type-hue trap fixed, backs the front mirrored with the face out, frames and grounds off; scripts batch17.py, chain17.sh, prep17.py, hand_b17.py, recolour17.py, icons17.py, ba17.py, ba17.sh, view17.py, grid17.py, grp17.py, build17.py and the batch 17 subjects
- `f6287a64` TODO: T-473 struck -- released in v11.316.4 (engine e1f15ec1f), played in the theatre
- `32b021a1` qa: T-452 batch 16 sheets (v11.316.4)
- `b1e51a35` manual: rebuilt for v11.316.4
- `213d9707` ROM release v11.316.4: T-452 batch 16 (SINKHOLE to CATHODE); T-473 trading, the game's half (lock, LOAN, TRADED_IN, trade evolutions on arrival)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
