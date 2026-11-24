# DAEMONS v11.416.2 — release notes

*Released 2026-11-24 09:36 · built against the design bible v11.416*

- **Engine**: CodeMusic/pokefirered-daemons `2635975c3` (context-content)
- **Design**: CodeMusic/DAEMONS `dc6ddb12`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `55ca0c330da6978d084a1fd820b250bfa23e6612` |
| `daemonsContext.gba` | CONTEXT | `57d371b2e3ccbc54e979e47f2026238a627f113d` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `cfa67b459593cc882b0de8076d55398534efd4bc` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `4096be9ec6bd6bc346cdf8cf10fffe6959e2a22d` |

## The engine since v11.416.1

- `2635975c3` T-604: stage 10 -- fifteen more later forms colour in as they learn their part: a region in the new part's colours (CYCLICAL's straw sombrero, CLINGING's head flushing blush and violet, BOOSTING's crown in blossom, LONGJUMP's indigo crest and sky-blue wings, DEEPWELL's deep-sea glow on its back and tail, FORGE's lit firebox, FLOCKING's gold forewings banded in VECTOR, WARMSTART's petals warming to gold and apricot, GATHERING's VECTOR ladybird wing cases, TORPOR's STRATUM mud on belly, hands and feet, OVERLAY's tinted glass dome, ALLUVIUM's STRATUM-silted fins, UNBRANCHED's tan and chestnut coat, JACOBIAN's dusk-violet wing, AQUIFER's geode shell in rose quartz and amethyst), DRAFT
- `8e915008d` README: latest is v11.416.1

## The design and tools since v11.416.1

- `dc6ddb12` qa: T-604 stage 10, fifteen later forms, built
- `6be1a393` qa: C-447 ROLL CALL with a pretend cap
- `25756302` TODO: Redmine's mirror
- `3fc371b1` T-604: stage 10 -- fifteen later forms colour in (engine 2635975c3), DRAFT
- `7ea1a5b7` T-604 (draft): stage 10 -- fifteen more later forms colour in as they learn their part: a region in the new part's colours (CYCLICAL's straw sombrero, CLINGING's head flushing blush and violet, BOOSTING's crown in blossom, LONGJUMP's indigo crest and sky-blue wings, DEEPWELL's deep-sea glow on its back and tail, FORGE's lit firebox, FLOCKING's gold forewings banded in VECTOR, WARMSTART's petals warming to gold and apricot, GATHERING's VECTOR ladybird wing cases, TORPOR's STRATUM mud on belly, hands and feet, OVERLAY's tinted glass dome, ALLUVIUM's STRATUM-silted fins, UNBRANCHED's tan and chestnut coat, JACOBIAN's dusk-violet wing, AQUIFER's geode shell in rose quartz and amethyst), DRAFT, nothing built
- `b544403e` C-518: THE BRAIN, night 3 -- tools/ai_models.py's BRAIN: line (none: it writes LiteLLM's model table, no fallbacks)
- `636e5a3c` Tickets nightly 2026-11-24: the Redmine export (T-581)
- `cc738796` C-518: THE BRAIN, night 2 (approved 2026-11-24) -- DAEMONS' ai/: the BRAIN: line in airun.sh, inplay_beat.py and LiteLLM's config.yaml (each none: a launcher, a presence beat, a proxy with no fallback), and a BRAIN column in the n8n README (health brainstem, look and sprite visual, voice motor, chat none, talk moved); reviewed cold, GO with changes
- `6a3fb9b4` README and wiki: latest is v11.416.1
- `690d1f2d` ROM release v11.416.1: T-604 stage 9, fifteen more later forms colour in as they learn their part (DRAFT); seals v11.415.x

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
