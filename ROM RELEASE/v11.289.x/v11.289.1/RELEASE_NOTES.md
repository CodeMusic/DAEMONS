# DAEMONS v11.289.1 — release notes

*Released 2026-10-01 14:53 · built against the design bible v11.289*

- **Engine**: CodeMusic/pokefirered-daemons `f44f0ffea` (context-content)
- **Design**: CodeMusic/DAEMONS `805affb9`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `3607028aefc791af8adec1b3223875a620d599b1` |
| `daemonsContext.gba` | CONTEXT | `e884ff1bf927ea21692bd6050a3f74540afdb01c` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `79eeadd7140ee3c96865e805695a95fbcd570415` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `b4327b1df2751b2672b18dfbbe9400f03e3e600b` |

## The engine since v11.288.23

- `f44f0ffea` T-321: the dialogue review applied -- nine teaching lines rewritten in their speakers' voices (PHLEGMATIC, the SLATE curator, SCORN to the PRESIDENT, the Owl, CAIRN, VERA, Anthony), CORPUS no longer calls itself evil (T-101), typos and the help's POKé BOX fixed (DRAFT)
- `6cb36f9ed` T-322: three categories that contradicted their entries -- LENSMUSAI FOCUS, MASKMUSAI COVER (vanilla's SUN and MOONLIGHT), SLURP BULK READ (DRAFT)
- `72217932c` T-327: MASKMUSAI redrawn as a grey robot behind a mask -- the white draft's body could not be told from the paper
- `447796feb` T-322, T-327: the INDEX review applied -- 61 entries for 54 daemons (THEOREM/LEMMA MIND, BOTTLENECK, BREAKER, SLURP and the weak ones), and CONTEXT's own line for the 26 reached by evolving; OVERRUN's margin follows (DRAFT)
- `3b03ec68d` T-324: the signs -- 114 blocks redrafted (vanilla wording replaced, six of ours eased), lost header breaks restored, SEVAULT's half-rename and Gen 1 tips fixed; the sign lady copies the new tip (DRAFT)
- `45b6666df` T-332: declare SetStartMenuWindowWidth in every build (the release ROM did not compile without it)
- `7916ee330` T-332: the START menu is two columns -- twice as wide, a divider down the middle; up/down within a column, left/right across
- `77c031fb0` T-331: the brain on the USER card fills one lobe per understanding, each in its type's colour; the halo when all seven are held
- `3722435dc` T-323: the bedroom poster is the annotated map, and it sparkles until read -- beacons twinkle from the start, REVEAL or not (DRAFT words)
- `abb91e1d8` T-326: MOM's own -- over twenty years on ships, and 'go on your journey, then come back and look again'; after the eighth MARK she asks how home looks now (DRAFT)
- `75f3ebda6` T-327: GRANBULL is CRYWOLF (the user's name) -- FALSE ALARM, both entries and its sprite (DRAFT)
- `1225e90dc` T-329: no national-INDEX gate -- every daemon's page shows, its number counts and every evolution happens from the start

## The design and tools since v11.288.23

- `805affb9` v11.289: the brain fills lobe by lobe (T-271 reversed by T-331); goal run 2 recorded -- T-321..T-332 (engine 1225e90dc..f44f0ffea)
- `02acf4ca` TODO: the user's answers recorded (T-188, T-221, T-224, T-321..T-327); T-329 INDEX gate, T-330 AI harness, T-331 brain lobes, T-332 two-column START menu
- `278c2995` ROM release v11.288.23: the grove daemons face away, three re-rolled, TY outlined

## The design bible's own entry for v11.289

### v11.289 — 2026-10-01

### The brain shows each understanding, and the user's answers built (2026-10-01)

- ***Reversed (T-271 → T-331)***: **the USER card's brain fills one lobe per understanding, each in its type's colour, with a halo at seven** — *the user could not tell how the single glow changed. Recorded in the Reversed table.*
- ***No national-INDEX gate*** (T-329): *every daemon's page shows and every evolution happens from the start; trading past the first 151 still waits for the GLOBAL INDEX.*
- ***The START menu is two columns*** (T-332): *up/down within a column, left/right across; it no longer runs off the screen.*
- ***MOM's own lines*** (T-326), ***the bedroom poster that sparkles until read*** (T-323), ***CRYWOLF*** (T-327), ***MASKMUSAI redrawn***.
- ***The three reviews applied*** (T-321, T-322, T-324): *114 sign blocks, 61 INDEX entries, nine teaching lines and the CORPUS self-descriptions; all DRAFT.*
- ***The AI harness caught up*** (T-330). *New: T-333, 65 named daemons still under vanilla's INDEX category.*

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 |
|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` |
