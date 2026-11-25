# DAEMONS v11.418.2 — release notes

*Released 2026-11-25 02:13 · built against the design bible v11.418*

- **Engine**: CodeMusic/pokefirered-daemons `64e873566` (context-content)
- **Design**: CodeMusic/DAEMONS `beea054d`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `804bab13cd2c0cc1dc524565c411dad9119565cd` |
| `daemonsContext.gba` | CONTEXT | `09f6b4d496bb28194e6da22b6388ebcf4545e067` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `7e31c65e2e89f1fe059646c53b208cc2180b09fd` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `33b06c547e77c1905dc8b3a9772ad01751fb1291` |

## The engine since v11.418.1

- `64e873566` T-604: stage 13, the backs -- sixteen later forms given a region on the back to match the front's: LANDFILL's arms and legs in the sludge blues (13.0/0.0% -> 21.8/16.9% waits), SPIKE's ears pink behind, the belt, toes and back diamond lilac, the bolt tail in front (11.1/0.1% -> 16.1/17.0%), CRON's core back and every ray tip in the gem's aqua (12.0/0.4% -> 24.5/15.7%), SPINLOCK's gloves and arms green (11.1/0.4% -> 15.3/18.1%), RESPAWN's robe side drapes gold (20.6/4.0% -> 20.6/16.3%), BADSEED's seed heads pink in front, flaps and waist pink and stalks and leaves brown behind (10.4/4.7% -> 20.1/15.3%), OTHERWISE's hind wings tan and red (10.3/7.0% -> 18.3/15.2%), HONEYPOT's pot glaze honey (12.8/7.0% -> 15.3/17.0%), EMERGENCE's violet further up the tail (11.0/7.5% -> 19.8/17.9%), SUPERVISOR's outer wing feathers a pale blue in a new slot 10 (11.3/8.2% -> 19.4/18.1%), SEEKMUSAI's antennae, helmet band and suit in VECTOR's red (13.6/8.4% -> 18.7/19.9%), ENSEMBLE's palm leaves violet behind (16.9/8.5% -> 16.9/19.8%), CAPRICE's petals' fill a pale pink with slot 8 merged into 6, and the bud pink (10.1/8.9% -> 19.0/21.2%), BACKPRESS's mane down the neck (15.7/9.1% -> 15.7/17.9%), UPSTREAM's side fins and tail orange (13.3/9.3% -> 16.2/15.1%), SPYWARE's hind wings violet (22.3/9.7% -> 22.3/20.5%), DRAFT
- `069565df8` README: latest is v11.418.1

## The design and tools since v11.418.1

- `beea054d` qa: T-604 stage 13, the backs, built
- `e31ae951` TODO: Redmine's mirror
- `2e28e9f1` Book audio: THE COMPANION re-recorded for the v11.418 minor (friend, 82.5 min, sources 5e75cf86)
- `ea97d60b` T-604: stage 13, the backs -- sixteen forms (engine 916448c82), DRAFT
- `e85363be` T-604 (draft): stage 13, the backs -- sixteen later forms given a region on the BACK to match the front's
- `3af3b173` README and wiki: latest is v11.418.1
- `d2ab1835` ROM release v11.418.1: T-604 stage 12, a touch-up -- six earlier forms back over 15% (DRAFT); seals v11.416.x

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
