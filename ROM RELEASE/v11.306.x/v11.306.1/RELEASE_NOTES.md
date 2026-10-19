# DAEMONS v11.306.1 — release notes

*Released 2026-10-18 23:01 · built against the design bible v11.306*

- **Engine**: CodeMusic/pokefirered-daemons `9916ce1d2` (context-content)
- **Design**: CodeMusic/DAEMONS `d19d2443`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `06529bea23befa2437a6859a29c9c2cc292824d6` |
| `daemonsContext.gba` | CONTEXT | `5648683c328632ccc4213e9dec1623af6c87672f` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `62080a168baaa51a7704f093ccb16eb715641679` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `e9a9541f0b142c1ce62732081f0fed12f6f2794a` |

## The engine since v11.305.3

- `9916ce1d2` T-392: no cap, the union scripts released, and P3's holiday looks (DRAFT)

## The design and tools since v11.305.3

- `d19d2443` Bible v11.306: 9.24 amended -- every routine signed, the holidays' one allowance (T-392)
- `b8202d50` T-392 P3: holiday looks from holidays.json (genholidays sHolidayRoutineLooks, gensignature's lane sheet), no cap; TODO note (engine 9916ce1d2)
- `a99b70d7` qa: C-167 THE HOUSE KEEPS on the site (the test server, a copy of the save)
- `18742d7f` TODO: T-392 P2 released; no cap, the union scripts released (the user)
- `5aacad9d` qa: T-392 P2
- `9f2d0715` ROM release v11.305.3: every routine signed, every glyph outlined in true black (T-392 P2)

## The design bible's own entry for v11.306

### v11.306 — 2026-10-18

### Every routine signed (T-392)

- ***9.24, amended (the user)***: **all 363 routines carry a signature of their own** -- *nine glyphs of bits and a three-note figure in the type's key, unique by construction, outlined in true black, run in full; the union routines' own scripts released.* **A third exception to clause 3**: *on a holiday a routine may wear the holiday's look on its signature only, in the twelve month colours; a QUIET holiday plays soft.*

---

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
