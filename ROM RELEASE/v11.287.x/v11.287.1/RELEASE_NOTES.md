# DAEMONS v11.287.1 — release notes

*Released 2026-09-25 11:45 · built against the design bible v11.287*

- **Engine**: CodeMusic/pokefirered-daemons `baf9fbfc9` (context-content)
- **Design**: CodeMusic/DAEMONS `73615408`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `f831dc65aa15118bc6f88426902f416448dfbb8d` |
| `daemonsContext.gba` | CONTEXT | `b6f9d0660e9ee9bc740ccb954dfcdcc00e1f2ecf` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `446d7c1a8d93d3f6274fd3c691b909ff746b582b` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `46119a213be82895c1b31c0e1e2b4eef97b91a34` |

## The engine since v11.286.1

- `baf9fbfc9` T-272: R turns the USER card to its BENCHMARKS
- `cdd67c5cb` T-271: a brain on the USER card that lights once, and never counts
- `fe982a9af` T-304: an understanding writes itself into the Guide's margin

## The design and tools since v11.286.1

- `73615408` v11.287: the Guide's margins hold the understandings; the USER card's brain and BENCHMARKS
- `a67d047f` T-304 closed: the first understanding writes into the Guide's margin (DREAMS proposed; the chapter asked with T-252)
- `908de33a` ROM release: the week -- named, heard and coloured; v11.285.x sealed

## The design bible's own entry for v11.287

### v11.287 — 2026-09-25

### What the Guide opened, built

- ***The margins hold the understandings*** (4.36, T-304): *a note under the chapter an understanding concerns, in the Guide's cyan; DREAMS proposed, the words DRAFT, the chapter asked with T-252.*
- ***The USER card***: **a brain that lights once and never counts** (T-271), **and R for its BENCHMARKS** — *eight MARKS, each with what it certifies, DRAFT* (T-272). ***No UNDERSTANDINGS tab***, *by T-252's own rule.*

---

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
