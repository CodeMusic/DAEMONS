# DAEMONS v11.288.23 — release notes

*Released 2026-10-01 14:02 · built against the design bible v11.288*

- **Engine**: CodeMusic/pokefirered-daemons `1b27b402f` (context-content)
- **Design**: CodeMusic/DAEMONS `1b25dac7`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `7afd5a50f0e2ea9bad0d6cbcc42a56e60aac378e` |
| `daemonsContext.gba` | CONTEXT | `6e92bd937a60a91b7e699f696a5fbf00b5e85dc1` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `a1de51bba7e80064a9db7bd9c2c0dda068a0f0d8` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `064b8642b1b92add285909cc265df42b822ec6a3` |

## The engine since v11.288.22

- `1b27b402f` T-221: grove back views redrawn to face away; GRADIENT, LIKELIHOOD and PAIRWISE re-rolled; FADING grows pale, not HALT
- `73e892a3a` TY's portrait gets the outline every other portrait has (gbaoutline --only ty; it was added after the pass ran)

## The design and tools since v11.288.22

- `1b25dac7` Grove back-view pass recorded; FADING's entry guarded against the vocabulary sweep (engine 1b27b402f)
- `bd2524ce` gbaowslots refuses a write that would delete TY, DAVID and the singing fir; TY's portrait outlined (engine 73e892a3a)
- `298541b3` TODO: T-313 and T-314 closed; T-319 kept current with the groves
- `c6316a81` Picture sheets of what changed, every push: tools/reviewsheet.py, and the rule in CLAUDE.md (the user, 2026-10-01)
- `8c78814a` ROM release v11.288.22: the fourteen groves, a gangway to the singing fir, a longer thank-you

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
