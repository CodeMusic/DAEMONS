# DAEMONS v11.412.10 — release notes

*Released 2026-11-22 20:47 · built against the design bible v11.412*

- **Engine**: CodeMusic/pokefirered-daemons `954a6c817` (context-content)
- **Design**: CodeMusic/DAEMONS `968f829e`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `951886a02ca82420bde0c262dfd6a58afea8472c` |
| `daemonsContext.gba` | CONTEXT | `f2b5bcd97a3cb63186c8f5395827a032d56823ba` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `75ed32d21aca2c1236571c437d8403c8a7f7c05a` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `62334baa4fbe5e13fbd2cfab03f3a62d91961ffe` |

## The engine since v11.412.9

- `954a6c817` T-604: stage 3 -- fifteen more later forms colour in as they learn their part: a region in the new part's colours (TARPIT's resin-amber leaves, OVERDRIVE's blue-hot mane and tail, GUARDIAN's ember crest and tail, SPYWARE's orchid wing panels, CONJECTURE's gold tail and ears, MIGRATE's verdigris horn and spikes, ARCHIVER's FROZEN frost cap, fluke and sparkles, LEMMA MIND's gold fists, HAUNTPROC's teal belly and hem, SINGULAR's flame-orange VECTOR wings, horns and tail, EMERGENCE's violet tail, RESPAWN's amber hands, COREFILE's dusk-violet horns, THEOREM's indigo pauldrons, PREDICTOR's violet ears), DRAFT
- `740b79ae5` README: latest is v11.412.9

## The design and tools since v11.412.9

- `968f829e` T-604: stage 3 -- fifteen later forms colour in as they learn their part (engine 954a6c817), DRAFT
- `9fef0ca3` T-604 (draft): stage 3 -- fifteen more later forms get a region in their new part's colours, DRAFT, nothing built
- `0f339aa7` qa: T-604 stage 2, twelve later forms, built (v11.412.9)
- `03654a42` README and wiki: latest is v11.412.9
- `fa113292` ROM release v11.412.9: T-604 stage 2, twelve more later forms colour in as they learn their part (DRAFT)

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
