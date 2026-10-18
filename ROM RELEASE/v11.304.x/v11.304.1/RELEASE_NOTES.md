# DAEMONS v11.304.1 — release notes

*Released 2026-10-18 09:27 · built against the design bible v11.304*

- **Engine**: CodeMusic/pokefirered-daemons `1555a7ec7` (context-content)
- **Design**: CodeMusic/DAEMONS `4a603fbf`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `4ef91f62d9f26a009b6e8c9033fdec65fe72bed4` |
| `daemonsContext.gba` | CONTEXT | `7dd93395f2cd3a8a89a07b7c0ef35807d8c78ab2` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `61d7ff48a2d7e88807a89402a2d4d1c5e3efdbc2` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `6df1cdd8d69136467b087f83c7e65ca766f7020a` |

## The engine since v11.303.4

- `1555a7ec7` T-416 HOLIDAYS P3+P4 (the user, 2026-10-17/18): a holiday's daemons, its light, sky, fir glow, VIOLET BLOOM and fireworks; the givers no script called; DEN DAY reads either type (DRAFT)

## The design and tools since v11.303.4

- `4a603fbf` Bible v11.304: 3.6 HOLIDAYS (T-416); 3.5's FLUTE is found in BREATHVERSE (T-417)
- `fcea2643` T-416 P3/P4 built (engine 1555a7ec7): DEN DAY reads either type in holidays.json and genholidays' comments; TODO note
- `063ee0ef` qa: T-420
- `e656168c` ROM release v11.303.4: the STREAM's MARK shows no longer take OPUS off the shelf; old saves repaired on load (T-420)

## The design bible's own entry for v11.304

### v11.304 — 2026-10-18

### HOLIDAYS, and the FLUTE moved (T-416, T-417)

- ***3.6, new (the user)***: **the real calendar, a note and a colour for each month** -- *thirty-six holidays, three a month by edition, in-world names in the game; the banner plays the month's note; gifts once a year; THE YEAR in the NOTEBOOK; quiet days kept quiet.*
- ***3.5 (the user)***: **CONTEXT's FLUTE is found in BREATHVERSE**, *an island grove through a palm on ROUTE 2, so both editions get their instrument at the start.*

---

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
