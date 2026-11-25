# DAEMONS v11.418.1 — release notes

*Released 2026-11-25 01:46 · built against the design bible v11.418*

- **Engine**: CodeMusic/pokefirered-daemons `190bd02cb` (context-content)
- **Design**: CodeMusic/DAEMONS `855eb854`

| ROM | edition | SHA-1 |
|---|---|---|
| `daemonsContent.gba` | CONTENT | `d69ba9913ba5fbf3ce69ab7eb9b9c58e74fd4492` |
| `daemonsContext.gba` | CONTEXT | `815856a8c12e27d87cb1bccb4f542bd39b18b65e` |
| `DEBUG/daemonsContent_debug.gba` | CONTENT (testing build) | `030a1e260f361a545de0793cb0f24e1e9de9e949` |
| `DEBUG/daemonsContext_debug.gba` | CONTEXT (testing build) | `3437904c6edb6ca85ca2bf735cb166172e8c30ea` |

## The engine since v11.416.3

- `190bd02cb` T-604: stage 12, a touch-up -- six earlier forms back over 15%: CONJECTURE's tail and ears a paler gold, and the ears' backs gold behind (3.4/3.4% -> 20.6/15.4% waits), LEMMA MIND's four fists gold whole with a dark amber shading and the gold a little deeper (9.6/13.0% -> 17.4/19.0%), SINGULAR's wings, both horns and the whole tail in flame orange with a peach belly (9.5/10.5% -> 22.3/20.5%), REBUTTAL's headguard in its gloves' oranges (9.6/9.0% -> 15.8/16.8%), CANOPY's blossom deepened to cerise (4.9/4.4% -> 16.8/16.4%), DELTA's gills and cheek re-tinted gold, orange and burnt orange (8.0/10.8% -> 18.3/17.6%), DRAFT
- `7aa34039f` README: latest is v11.416.3

## The design and tools since v11.416.3

- `855eb854` qa: T-604 stage 12, a touch-up of six, built
- `bb53300a` gencasino.py: read the companion's context.ts from server/src/psyche/ (C-428 moved it there), falling back to the old place
- `4acbe86a` README and wiki: daemons-embodied among the repositories (T-617; designed and reviewed, nothing built)
- `d70a741f` Tickets nightly 2026-11-25: the Redmine export (T-581)
- `e9990dc1` CLAUDE.md: add a repo to GitHub Desktop with open -a (the openLocalRepo link does nothing)
- `3a80f56f` CLAUDE.md: a new repo is cloned on both machines and added to GitHub Desktop on both (the user, 2026-11-25)
- `ac4f4cba` Tickets: a fourth Redmine project, embodied (B- for BODIES), and a twelfth lane, body -- mirrored into daemons-embodied's TODO.md; the repository in the layout, setup.sh and the nightly
- `22f8b7f6` T-604: stage 12, a touch-up -- six forms (engine 190bd02cb), DRAFT
- `fe826dd7` T-604 (draft): stage 12, a touch-up -- six earlier forms back over 15% waits on both sides, changed on the APPROVED art
- `cb8640d9` TODO: the mirror after C-492 closed
- `a82b6aa5` qa: C-492 the faces on the redrawn ROVER line and MUSAI branch, checked
- `2a0f341e` qa: C-447 ROLL CALL on the Zero over the air
- `66a7101d` T-634: EMBODIED's voice is workshop (the user's pick, A of three samples) -- tools/bookaudio.py's VOICES gains it; the book stays UNVOICED until it is recorded, so the audio gate passes
- `b0b0eb7f` TODO: Redmine's mirror (T-617 closed, T-634 opened; T-621 to T-633 from their lanes)
- `9f0da9c3` T-617: DAEMONS EMBODIED reviewed -- the user's answers to the design's twelve questions, and two additions of theirs, in the book and the bible (9.38, v11.418); nothing built
- `fa4eb1f1` T-622: the hardware's words in the bible (9.39, v11.417) -- DAEMICOM, FAMILIAR, SIGIL, WAND, QUILL, TALISMANS, SHEWSTONE, CIRCLE; EVOCATION, SCRYING, BINDING, INVOCATION; THRESHOLD, SANCTUM, LITANY, INCANTATION, DEPART -- the four open points answered; the four books' prompts and THE LORE OF THE DAEMICOM drafted, DRAFT
- `cb9da6a9` README and wiki: latest is v11.416.3
- `22218dc1` ROM release v11.416.3: T-604 stage 11, the last sixteen later forms colour in as they learn their part (DRAFT)

## The design bible's own entry for v11.418

### v11.418 — 2026-11-24

- **9.38 DAEMONS EMBODIED, reviewed** (T-617; the user, 2026-11-24, by multiple choice): the twelve questions answered -- braces; the first build a Pi Zero 2 W with an LLM630 Compute Kit as its brain; the body keeps a learned action; ROAM; no practice alone; one wake word of our own and a touch; tickets B- in a project and lane of their own, BODIES; THE BRAIN's interface to its own repository; the DESIGNS shelf, read aloud. **Two additions**: where a body thinks is a setting (ON BOARD, MESH, HYBRID, a frontier model only on request and approval), and a body learns to speak as it learns to move (words that start few and grow, each kept in its daemon's own voice). To EMBODY is 9.39's INVOCATION.
- **The book reprinted** with them (`docs/DAEMONS-embodied.pdf`, 62 pages): Part 9's four computers and the mind setting, Part 10's Learning to speak, Part 12's Zero and kit with five bench questions, phases A to L, Part 15 as what was decided and what is open.
- Section 10: one Settled entry; the twelve questions struck from Open, five smaller ones in their place.

## Patches

*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the ROM's CRC and refuses the wrong one. Step by step, with every checksum: `ROM RELEASE/HOW_TO_PATCH.md`.*

| patch | apply it to | that ROM's SHA-1 | tested on |
|---|---|---|---|
| `PATCHES/DAEMONS CONTENT for FireRed 1.0.bps` | Pokemon FireRed (USA) 1.0 | `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTENT for FireRed Rev 1.bps` | Pokemon FireRed (USA, Europe) Rev 1 | `dd5945db9b930750cb39d00c84da8571feebf417` | a real cart, dumped |
| `PATCHES/DAEMONS CONTEXT for LeafGreen 1.0.bps` | Pokemon LeafGreen (USA) 1.0 | `574fa542ffebb14be69902d1d36f1ec0a4afd71e` | pret's byte-identical rebuild |
| `PATCHES/DAEMONS CONTEXT for LeafGreen Rev 1.bps` | Pokemon LeafGreen (USA, Europe) Rev 1 | `7862c67bdecbe21d1d69ce082ce34327e1c6ed5e` | a real cart, dumped |
