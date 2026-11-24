# DAEMONS v11.416.3 — release notes

*Released 2026-11-24 18:35 · built against the design bible v11.416*

- **Engine**: CodeMusic/pokefirered-daemons `641be6567` (context-content)
- **Design**: CodeMusic/DAEMONS `b48d0c66`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `512e17d24de302647fe99a3bb72160864e54fee9` |
| `daemonsContext.gba` | CONTEXT | `19b605933167d48f3dfa877e1f0798dc6df61047` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `1ea830e8abef8a01ac6fbe7055ad2e90f637f05d` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `f5b5bbb143ca876ae743e76812398f325d612a94` |

## The engine since v11.416.2

- `641be6567` T-604: stage 11, the last -- sixteen later forms colour in as they learn their part: a region in the new part's colours (MENTALIZE's periwinkle gown, LOOKOUT's sable coat, STALEMATE's wing in frost-at-dusk lilac and violet, GUTFEEL's honey belly, MINDSIGHT's crown in CONTEXT, WRAPAROUND's lilac ears and feet, FEDERATED's steel-blue pods, CURRICULUM's saddle in blossom, MOMENTUM's dusk-violet back, RELEASE violet below the hood, ABANDON's crown of turning leaves, DEDUCTION's lilac waistcoat and violet paws, FIRMWARE's rusted saddle, EPIPHANY's lit gold wings, and the fossils MAINFRAME and PUNCHCARD in FLOW), DRAFT
- `932912534` README: latest is v11.416.2

## The design and tools since v11.416.2

- `b48d0c66` qa: T-604 stage 11, the last sixteen later forms, built
- `d2a4d89c` THE COMPANION manual: REVERIE's drifts on SLEEP SOUNDS -- THE DRIFT and its four kinds, the strong ones, the spirals in its eyes, and what it is not (companion C-551, C-555; DRAFT)
- `21b0e82a` TODO: Redmine's mirror
- `2810b655` T-604: stage 11, the last -- sixteen later forms colour in (engine 641be6567), DRAFT
- `cbe063ed` T-604 (draft): stage 11, the last -- the sixteen later forms still under 10% colour in as they learn their part: a region in the new part's colours (MENTALIZE's periwinkle gown, LOOKOUT's sable coat, STALEMATE's wing in frost-at-dusk lilac and violet, GUTFEEL's honey belly, MINDSIGHT's crown in CONTEXT, WRAPAROUND's lilac ears and feet, FEDERATED's steel-blue pods, CURRICULUM's saddle in blossom, MOMENTUM's dusk-violet back, RELEASE violet below the hood, ABANDON's crown of turning leaves, DEDUCTION's lilac waistcoat and violet paws, FIRMWARE's rusted saddle, EPIPHANY's lit gold wings, and the fossils MAINFRAME and PUNCHCARD in FLOW), DRAFT, nothing built
- `572892a5` README and wiki: latest is v11.416.2
- `f279e36e` ROM release v11.416.2: T-604 stage 10, fifteen more later forms colour in as they learn their part (DRAFT)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
