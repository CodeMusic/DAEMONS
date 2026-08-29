# CHANGELOG

Design-bible versions and what moved in each. `vision.md` is the living document;
the PDFs are snapshots cut with `./docs/build-pdf.sh <version>`.

---

## Session — 2026-08-29

### Title screen and SGB borders

- **DAEMONS logo** — `gfx/title/pokemon_logo.png` replaced, 128×56 2bpp, dimensions identical to vanilla so no title-screen code changed
- **CODEMUSIC** replaces GAME FREAK INC. on the title line; the year is deferred (needs glyphs that do not exist yet)
- **Version subtitles** — both editions ship at the same 10-tile width so the title code's contiguous tile run prints the whole word. The earlier 8-tile version rendered as "Con"
- **SGB borders generated, not drawn.** `red_border`/`blue_border` → `content_border`/`context_border`; `green_border` dropped. Three commissioned illustrations measured at **496 and 523 unique tiles against a budget of 96**; the generated versions cost **12 tiles** each
  - CONTENT — one dot grid, dots shrinking toward the screen
  - CONTEXT — the same cell over itself at an offset: the pattern is the relationship, not the marks
- Border palettes rewritten: index 0 is the light ground, index 3 the ink

### CONSENSUS — the SWARM fix (9.2 step 6)

- **Move `$A5`** — SWARM, 90 power, 100% accuracy, 15 PP, `NO_ADDITIONAL_EFFECT`. Verified by reading the move table back out of the built ROM
- **Inserted before STRUGGLE, not appended.** `engine/battle/core.asm` asserts `NUM_ATTACKS == STRUGGLE` — random numbers above STRUGGLE are treated as "not a move". STRUGGLE shifts `$A5` → `$A6`; every other move ID is untouched
- **Five tables, not the two 9.2 listed** — `move_constants.asm`, `moves.asm`, `names.asm`, `animations.asm`, `sfx.asm`, the last three because each asserts `table_length NUM_ATTACKS`
- Borrows PIN_MISSILE's animation and sound — converging projectiles
- **Not yet learnable.** Assigning it means naming species, which is steps 9 and 11

### Tools

- `tools/gbimg.py` — shared PNG helpers (`read_png`, `resample`, `quantise`, `write_png`) for any colour type and bit depth
- `tools/genborder.py` — generates a border from a repeating cell, asserts the tile budget and the 896-entry tilemap
- `tools/mkborder.py` — rewritten on `gbimg`; now the *measuring* tool for supplied art

### Format facts established against vanilla

- `rgbgfx` **inverts** greyscale: PNG level 3 → colour index 0, so higher PNG value is lighter on screen
- Tilemap entries are `(tile, attribute)`; palette is `(attr >> 2) & 7`, `$40` is X-flip
- Tile `$00` is reserved and flat — the centre 160×144 is covered by the Game Boy screen
- Colour index 0 is not transparent in a border; vanilla uses it as its lightest value

---

## Session — 2026-08-27 → 28

### Repository structure

- Created `docs/`, `patches/`, `gfx/` (front, back, overworld, ui), `audio/` (music, sfx) with a README in each
- Moved `vision.md`, the v1.0 PDF and the type-system notes into `docs/`
- Moved `type_constants.asm` and `type_names.asm` into `patches/`, with a README carrying the build order
- Added `.gitignore` for `.DS_Store`
- Root `README.md` layout block updated to match reality
- Added `docs/build-pdf.sh` + `docs/style.css` — pandoc + headless Chrome (v1.0 was cut with wkhtmltopdf, no longer installed). Takes a version *or* a filename: `./docs/build-pdf.sh 1.6` or `./docs/build-pdf.sh lineage.md`

### v1.1 — names interrogated, cast tightened

- **Gilt → Brazen.** Gilt implies a concealer and this story has no schemer; brass is honestly itself, and so is Scorn. Full argument in §3.1
- **Doldrum kept**, with a better reason: the doldrums are a *place*, and being becalmed is the failure state of gradient descent — the name *is* Benchmark 2's lesson
- **The Bleed kept.** Printing term first; the map already uses the body's colour words for what happens to surfaces (The Flush → Ardor)
- **BunnyArtsai35 → BunnyArtsai.** The number in her name gave away the Five Witnesses lock; relocated to a single Quicksilver terminal log
- **Ty → Ty Clear**, Crystal's son and Scorn's partner
- **The Goodhart engraving** — cast into the Corpus lobby floor, unattributed, adopted approvingly by Corpus
- **S.T.A.R.R. is a comprehension, not a clone** — the lab understood recursion and instantiated it
- New **§0.3 The loop underneath** (the CFM, named for the authors only) and **§4.9 Feedback, said sideways** (dialogue rules)
- §10 gains a **Reversed** table

### v1.2 — the Quicksilver inheritance, and the rival's name

- **§4.10** written: Corpus downstream of Quicksilver, with options A–E, guards and sanctioned surfaces
- **Craft rule 6: comedy is the cover.** Corpus is cheerful and absurd; the horror is what they are cheerful *about*
- **Rival naming prompt reversed** — keep vanilla's prompt, hard-code **CLEAR**. Crystal asks what you will *call* him, which is the route-sign device ninety seconds before Route 1 teaches it
- Ty's parentage is **never stated** — inferred from the surname, confirmed late by one line at Brazen

### v1.3 — the Quicksilver sequence

- **Corrected the uncaused fire.** Earlier draft had the island burn for no reason; theoretically tidy, dramatically inert
- The order settled: Crystal at Quicksilver → a fitness-for-work procedure removes her → Scorn assumes control, rebrands, **the metric changes** → pressure rises → the incident → Corpus inherits the people
- **Scorn caused the fire the way a metric causes a fire.** He signed a complete file about a person **he never met**
- The removal is **procedural, never medical** — craft rule 3 governs this beat harder than any other
- **Ty stayed.** His guilt is an absence of decision, not a betrayal
- **The Index is what Crystal did next** — her response to being denied being taken seriously
- **Dating scheme:** no date on the fire, dates on everything around it. The player reconstructs the order or does not
- **Brazen confirmed over Brass.** Brass is a colour and not a feeling — the only single-meaning name on a map built on double readings

### v1.4 — the two editions

- **§8.4.** The slash in the title is literal: **CONTENT** and **CONTEXT**, one source tree
- Verified against `pret/pokered` master: the repo already builds Red *and* Blue via `-D _RED` / `-D _BLUE` and `IF DEF(...)` blocks. Rename the defines and it is done
- Three tiers: encounter tables (free, zero extra sprites) → rosters that **lean**, so the editions are hard in different places → **Index entries that disagree** about the same daemon
- Trading becomes the structural argument: **you cannot complete the Index alone**
- **The type chart is byte-identical across editions.** It is the argument
- Build both targets on day one even while the ROMs are identical

### v1.5 — BINDING

- **Catching → BINDING.** `bind()`, *binding a daimon* (the literal ritual phrase), and a bond. CATCH was the only lexicon entry doing no double duty
- The test was not "is it nicer" but **"is it softer"** — it isn't; binding is darker than catching, so the player stays implicated
- Message register: **`LABL was BOUND.`** No exclamation, no congratulation
- ATTACH held in reserve if playtesters find BIND too dark

### v1.6 — not yet

- **§8.5.** Sprites and the **Gen1Recomp** question, recorded and deliberately undesigned
- The split that decides it: Gen1Recomp *imports data* and *hand-writes behaviour* — so ROM tables likely carry, `asm` almost certainly does not
- One afternoon answers it: build the step-5 milestone and drop it in the launcher

### v1.7 - the monochrome question
- Add 8.6. Greyscale is the design, not a limitation: the player is told
  these places are colours and shown grey, and supplies the rest
- Colorizing Halftone destroys Halftone - the town is dots that only look
  like grey, and that is a load-bearing wall
- Colour appears exactly once, at the Review Board, where four ancient
  people insist emotions are coloured fluids and are wrong
- Easier than full colorization: palette one map, greyscale ramp elsewhere

### v1.7 - the monochrome question
- Add 8.6. Greyscale is the design, not a limitation
- Colorizing Halftone destroys Halftone - a load-bearing wall
- Colour appears exactly once, at the Review Board

### v1.8 - step 5 shipped
- **A byte-matching vanilla build was verified, then patched, and it runs.**
  `engine/pokered.gbc` carries the fifteen type names and the two matchup deltas
- Correct 9.1: current master fills the ID gap with a `REPT` block, so there is
  no `$0B` fold. And the constants do not need renaming at all - only the
  strings in `data/types/names.asm` affect what the player reads
- Literals corrected by build: `PSYCHIC_TYPE`, not `PSYCHIC`; effects are named
  constants, not numbers
- Reclassify both files in `patches/` as reference-only; either would break the
  build if pasted
- Add `patches/0001-type-system.patch`, applied and building

### v1.9 - ORPHAN, and the RESOLVER
- Verified: 190 index slots, 151 species, **39 MissingNo.** - 36 bare
  `const_skip` holes and 3 already named (`FOSSIL_KABUTOPS`,
  `FOSSIL_AERODACTYL`, `MON_GHOST`), none with a dex number
- Add **ORPHAN** at Halftone Tower. CORRUPT/LATENT. The one daemon with a
  genuinely blank Index entry. An orphaned process is how a daemon is made,
  so the name is the mechanism
- Add the **RESOLVER** (Silph Scope): a linker resolves a symbol to a name;
  resolution is the town's subject. It exists because the Index is insufficient
- Keep `$B8` as the unresolved display state; ORPHAN is a real species in a free
  slot, so no engine surgery

### v2.1 - the Clears
- Vanilla's rival is Oak's *grandson*, and Ty was Scorn's partner before the
  rebrand - an adult with a career. He cannot be the boy who races you
- **Al Clear** becomes the rival and incumbent: Crystal's grandson, Ty's son
- **The transmission failure.** Ty understood through perspective thinking, but
  that understanding is context, and context does not transmit - only content
  does. Al received the method with none of the experience. The Index problem,
  inside a family
- It is also why the player wins: Al was taught, you were let loose
- **Ty P. Clear** relocates to the Quicksilver ruins. He could explain all of
  it and does not
- The Goodhart line moves to Al - "something my father used to say", delivered
  with no idea who said it first
- The family is named for three kinds of clarity: Crystal Clear (transparent,
  unfundable), Ty P. Clear (*type clear*, legible, understood by nobody),
  Al Clear (*all clear*, declared by the people who caused it)
- AL reads as AI in sans-serif type but not in the cartridge - Gen 1's I is
  serifed and L is not, verified against gfx/font/font.png. The double meaning
  lives where the theory lives, not where the game lives. Never lean on it

### v2.2 - default names
- Implemented per-edition name lists in constants/player_constants.asm,
  verified by decoding both ROMs
- Slot 1 **fixed** (PIP, AL - these are people), slot 2 **swapped** (the vanilla
  RED/BLUE gesture), slot 3 **differentiated** (so LUCID never floats out of the
  Clear family and into the player's list)
- Vanilla's wholesale mirror is not inherited: Red and Blue are symmetric
  positions, ours are not
- PIP is a dot, the smallest resolvable unit. CODE goes to CONTENT (literal
  instruction), SHARP to CONTEXT (perception). LUCID and CANDID are Clear-family
  clarity words

### v2.3 - PROF.OAK becomes CRYSTAL, with no title
- Crystal has no rank, deliberately. She built the Index to be taken seriously
  and was then processed out of her own lab; every other authority in the game
  has a role and she is just her name
- Vanilla split perfectly for it: OAK: (19x) -> CRYSTAL:, PROF.OAK (8x) ->
  CRYSTAL CLEAR. First name when spoken to, full name when spoken about
- One line had to be rewritten rather than renamed - the intro claims the title
  aloud, so "People call me the #MON PROF!" became "I study #MON."
- 43 player-visible strings changed, 21 blocks rewrapped. Vanilla's own widest
  line is 19 characters, which is the real ceiling
- ~267 code identifiers (OaksLab, OAKS_LAB, ProfOakName) left alone - internal,
  same category as the _RED/_BLUE defines

### v2.4 - MOCK, and PACKAGE
- OAK's PARCEL -> **PACKAGE**. A repo distributes packages, and CRYSTAL's PARCEL
  is 16 characters against a 12-character item limit
- **MOCK** (Ditto) is NORMAL/NORMAL, so CONTENT/CONTENT, and it learns Transform
  - therefore PERSPECTIVE. Perspective thinking was always in the wild;
  Quicksilver only noticed it
- The distinction costs nothing: MOCK takes another's frame freely because it has
  no frame of its own to lose. BunnyArtsai had a self, which is why she did not
  come back the same
- A mock object has the full interface and none of the behaviour - which rhymes
  with Al Clear receiving the form of his father's lesson, hollow

### v2.5 - the species rename, and colour settled
- POKeMON -> DAEMON / DAEMONS. Achieved by repointing ONE string:
  home/text.asm PlacePOKeText from "POKe@" to "DAE@", so all 650 #MON
  occurrences moved with no source edits and no rewrapping
- Widths cooperate: DAEMON is 6 rendered where POKeMON was 7, DAEMONS is 7.
  Singular gains room, plural is identical
- 54 non-species uses became literals first: #DEX -> INDEX (26),
  bare # -> POKe (23, all item prefixes split across a line break),
  #MANIAC -> POKeMANIAC (5)
- Grammatical number was the real job. 106 compounds are lexicon renames,
  123 marked plural, the rest read singular and needed no edit. English keeps
  attributive nouns singular, so the free default is also the correct one
- ~160 occurrences carry no strong evidence and want a human read at step 8
- **Colour settled at two sources**: Umbra (an obsolete answer, held still) and
  PERSPECTIVE (a glimpse, lost). MOCK makes the second reachable in ordinary
  play; BunnyArtsai is its most loaded firing, not a third source
- Verified: MEW appears in no wild encounter table in vanilla. There was never a
  designed way to reach it, which is why player culture invented one

### v2.6 - battle vocabulary, the boxes, the sleep cluster
- **RUNNER -> USER.** RUN was colliding with itself; vanilla's own text says
  "There's no running from a trainer battle" while the player is a RUNNER.
  USER is user-level privilege (and the first box is a USERBOX), someone who
  uses people (oPerson, 2011), and it frees RUN. Nothing lost - the verb moves:
  you are a USER, and you RUN daemons
- **WILD -> UNBOUND**, the exact antonym of BIND. The vocabulary now teaches
  itself: UNBOUND appears, you BIND it, it is BOUND
- Fainting -> **HALTED**. Fleeing -> **DETACHED**, which has no inverse on
  purpose: the process is still running, you stopped observing it
- Trainer battles are BENCHMARKS too - a scale distinction, as in ML. You
  benchmark constantly; THE BENCHMARKS are the eight that issue CERTs
- **A box is a machine** - sysadmin vernacular. You are not throwing a cage,
  you are offering a host. Catch rate by permission level becomes literal
- **The sleep cluster**: SNORLAX -> DEADLOCK, POKé FLUTE -> INTERRUPT,
  JIGGLYPUFF -> SUSPEND, WIGGLYTUFF -> HIBERNATE, SLEEP unchanged. INTERRUPT
  keeps the music: a tune is an abstract command that evokes a state
- The Underground Path is already a TUNNEL (networking), and the guard stays
  thirsty - the corporate checkpoint yields to a beverage. Inertia, not security
- 379 "trainer" occurrences deferred to the step-8 text pass

### v2.7 - step 7 and step 8 (part one)
- **Step 7: TRANSFORM -> PERSPECTIVE.** One string. Every Ditto in the game now
  runs the signature move of the theory
- **Step 8: the world renamed.** 14 map names, 143 references swept through
  dialogue, only 2 lines needed rewrapping - most new names are SHORTER than
  the old ones, the opposite of the OAK job
- Landmarks came too: VIRIDIAN FOREST -> THE UNDERTONE, ROCK TUNNEL -> THE
  BLACKOUT, VICTORY ROAD -> UMBRAL ASCENT, CINNABAR ISLAND -> QUICKSILVER IS.
- Routes deliberately untouched: the official map keeps its numbers (3.2). The
  local names are signpost content, which is new writing rather than a rename
- **Title subtitles built programmatically**: extracted clean e/o/n from the
  vanilla "Version" graphic, drew C/t/x to match its 2px stems, emitted valid
  1-bit greyscale PNGs at the exact canvas sizes. The title screen now reads
  Content / Context. No image model can produce these formats
- Still open in this pass: 379 "trainer" -> USER, and the route signposts

---

## Infrastructure

- `engine/` symlinks to `../pokered`, a fork kept separate because
  `pokered/gfx/` holds Nintendo-derived sprites and this repo promises not to
  distribute copyrighted material. Gitignored
- `CLAUDE.md` is the shared contract: read-first order, six invariants, the
  spoiler list, and the procedure for changing the design. One session root
  means one memory store and no design/implementation desync
- Top-level `Makefile` shim: `make red`, `make blue`, `make vanilla-check`

---

## Research

- **All three blogs read in full** — 95 posts, 78,136 words — and analysed in [`lineage.md`](lineage.md)
- **`psychologycode.com` recovered.** The site is gone; the Wayback capture of its RSS feed still carried all eight posts complete. Saved to [`archive/psychologycode/`](archive/psychologycode/). Three were never reposted anywhere
- Findings that changed the design: the thesis exists verbatim in 2011; craft rule 3 is the first post of the first blog; Scorn is a 2011 pseudocode snippet; §4.10 is a 2023 post about Rumpelstiltskin

## Drafts

- [`posts/2026-08-seeingsharp-announcement.md`](posts/2026-08-seeingsharp-announcement.md) — project announcement, ~2,300 words, **not published**
