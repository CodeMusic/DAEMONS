# DAEMONS v11.304.4 — release notes

*Released 2026-10-18 12:59 · built against the design bible v11.304*

- **Engine**: CodeMusic/pokefirered-daemons `f4d27dd0e` (context-content)
- **Design**: CodeMusic/DAEMONS `f5d472c9`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `9f473289ad5bff3adc310eff2dc13174617a7ecb` |
| `daemonsContext.gba` | CONTEXT | `91e19ac5e866efa170217886acf6235062eb4a9e` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `8058144528c9b3508205771a031f84579040953a` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `4bef5200ad51acfc993300abc7f66177e22188fd` |

## The engine since v11.304.3

- `f4d27dd0e` T-412 (approved by the user 2026-10-18): the DREAM LOG's titles, and HER DREAMS (DRAFT)
- `e736dc724` T-412 (the user, 2026-10-18): a dream opens with "I had a dream." (DRAFT)

## The design and tools since v11.304.3

- `f5d472c9` T-412: the DREAM LOG's titles, and HER DREAMS (engine f4d27dd0e, DRAFT; the user, 2026-10-18)
- `63f339f1` TODO: T-412, HER DREAMS' 24 titles chosen one by one (the user)
- `bb7c5541` T-423: the last calls -- hue C (the CONTEXT page), THE SUBTLE LAYER, VOLTAGE for CHARGE, CHORUS for RESONANCE for now, ATTUNEMENT and the Clairs hint kept
- `e721251e` TODO: T-412's 21 titles chosen one by one, and the attendant's half approved (the user)
- `79c11f5b` qa: C-162 -- the watch face mock-ups, the season behind and the weather in front
- `a2d80d4a` TODO: T-412 drafts written; T-424 after the casino (the user)
- `ca1af9ce` T-412: a dream opens with "I had a dream." (engine e736dc724, DRAFT; the user, 2026-10-18)
- `7b293d1b` qa: T-423 hue mock-ups -- the Guide's ROM page recoloured four ways (neutral, CONTEXT trim, CONTEXT page, plum)
- `0736d7b2` TODO: T-412's three answers (the user); T-424, saturation is friendship -- settled in 8.6, never built
- `b7e5033c` T-423: the user's calls on the psychic book (2026-10-18), the four checks, and lineage 3d
- `1d0e4d3b` qa: C-158 the casino dressed, THE HOUSE, own settings (site and Tab5), the drawn pieces
- `9fab34d5` ROM release v11.304.3: a MARK and its ROOT each say how the other balances it, the last note, the DREAM LOG's 21 dreams (T-410, T-411, T-412)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
