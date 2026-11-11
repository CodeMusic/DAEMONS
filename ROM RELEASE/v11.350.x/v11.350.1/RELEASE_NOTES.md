# DAEMONS v11.350.1 — release notes

*Released 2026-11-11 14:39 · built against the design bible v11.350*

- **Engine**: CodeMusic/pokefirered-daemons `b65ba5da7` (context-content)
- **Design**: CodeMusic/DAEMONS `48dc7f92`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `3a6b6864cba21351eae9bd6782d092e9a53b6aa9` |
| `daemonsContext.gba` | CONTEXT | `9a59fb77589a8f7ba8400934e7b103c8ba73edce` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `447bc3869d2ef1b10d02cba8399308a189230834` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `63ac802c3f21e2fb7bf1e6e3d0a858cdef869b3a` |

## The engine since v11.349.1

- `b65ba5da7` T-447 pair 7 BUILT: the S.S. ANNE in THE LIVERY, and the smoke over her funnel (DRAFT)

## The design and tools since v11.349.1

- `48dc7f92` T-447 pair 7 BUILT (engine b65ba5da7): the S.S. ANNE in C THE LIVERY, extended over the tiles its draft only recoloured, and the smoke moved over the funnel (DRAFT)
- `40024db6` ai/: the companion's part of the local cloud moved to daemons-companion seer/ (companion C-340) -- the Tiiny's voice stream, sleep sounds, Whisper, and n8n's daemon/talk and daemon/hear with make_workflows.py; their READMEs and CLAUDE.md point there. ai/ keeps the AI-play harness, its LiteLLM notes and its own workflows
- `b95cf5a1` Bible v11.350: the third book's covers and the MUSAI followers released (T-519, T-534, v11.349.1)
- `943313eb` TODO: T-544 struck through (459607fe, companion 46e7ad4); T-545, what its first run found (release_main.sh already switched to --audio-gate)
- `459607fe` T-544: releases bring the docs current from WHAT'S NEW -- tools/releasedocs.py lists what came since the last release (DAEMONS: the release record's commits; the companion: since the WHAT'S NEW build before the newest) and checks every README, wiki, manual and SET UP page against it; book audio regenerated on a major or minor release only (--audio-gate); the push routine's step 5
- `42f60b4a` ROM release v11.349.1: the MUSAI followers, all 24 seasonal looks (T-534) and the third book's three covers (T-519); v11.348.x sealed (DRAFT)

## The design bible's own entry for v11.350

### v11.350 — 2026-11-11

- **4.40:** THE UNITY BOOK's three covers, which the user chose and v11.349.1 released (T-519). The night half shows a tablet mirrored in a still pool. The dawn half shows a star over the fir, with the lark. The mended book has both plates on indigo boards.
- **9.34:** the MUSAI branch is built. All 24 seasonal forms are drawn, and v11.349.1 released their followers (T-534).
- A Settled entry in section 10. All of it is DRAFT.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
