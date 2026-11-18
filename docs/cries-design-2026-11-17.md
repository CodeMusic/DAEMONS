# The daemons' cries: a design question (T-565 batch 11)

*2026-11-17. Options for the user to choose from, by ear. **Nothing is built and nothing has gone into the engine.**
Every example below is a DRAFT.*

**Picked (the user, 2026-11-17): A, shaped by B** -- the type's motif, its order and rhythm from the name, a line
sharing a contour, lower and slower as it evolves. All 388 to be drafted by `tools/gencries.py`, DRAFT.

The census (`docs/sound-census-2026-11-16.md`) left the cries for last: **388 of them, every one still pret's**, heard
at least twice a battle, at every switch-in, on every INDEX page and party screen. A cry is the one sound that belongs
to a single daemon, so it is a design question before it is an audio one: *what does a daemon say when it arrives?*

## Drafted: all 388 (`tools/gencries.py`, DRAFT, not in the engine)

*A shaped by B, as picked.* **The type's motif turned by the line's first name, so a line shares its contour; lower
(0, a fourth, an octave) and slower (20% a stage) as it evolves; and the daemon's own name sets how many notes, their
rhythm and accents (a vowel long and soft, a consonant short and struck), a pickup from its initial and an approach
to the held note from its last letter.** Each within pret's length for the same species. `APPROVED` is empty, so
`--write --approved` writes nothing yet; `check_generators.py` runs it.

- **Bytes, built by wav2agb: 1,320,274 for the 388, against pret's 1,630,415** (242 s of cries against 300 s).
- **The three checks, every cry: 0 fail.** DOUBLES (20 frames: two notes at least, an eighth of the loudest energy),
  BACKWARD (the last 15 frames, which Growl plays first, not near-silent) and FAINT (3.6 semitones down: no note below
  E2, and inside the cry player's 140 frames). *They pass largely by construction* -- the register floor and the pace
  were set to meet them -- so they guard a later change more than they judge this one.
- **Said, not failed: in 127 of the 172 two-type cries, the second type's held note comes after the 20-frame cut**, so
  in a double battle those daemons are heard by their first type only.
- **One pair is still identical: HUNCH and MIME** (both CONTEXT, stage 1, which has no noise texture to tell them
  apart). The pickup from the initial separated the other four pairs a first pass made.
- **Eleven daemons borrow another's cry** (`SpeciesToCryId`: the NEXUS residents and the carried line), so each is
  heard in a cry shaped by the lender's name and type: REFLECTION in MIGHTYENA's, HANDSHAKE in PICHU's, and so on.

The clips, in `audio/drafts/t565_cries/all/`: **`sampler.mp3`** (30 cries, 35 s: three whole lines, a daemon of every
type and several grown up, the shortest and the longest; `SAMPLER.txt` lists them), `six_doubles_cut.mp3`,
`six_backwards.mp3`, `six_fainting.mp3` (the six above, in each mode), `cries/<id>_<daemon>.mp3` (all 388),
`CRIES.txt` (each cry's shaping, bytes and checks) and `sampler.png`.

## What the engine does with a cry (the facts)

- **The format.** Each cry is a recorded sample, `sound/direct_sound_samples/cries/<species>.wav`: **mono, 8-bit, 10512
  Hz** (all 388 at the same rate). `audio_rules.mk` builds it with `wav2agb -b -c -l 1 --no-pad` into a **DPCM-compressed**
  `.bin`: a block of 64 samples is one starting byte and 32 bytes of 4-bit steps from a fixed table of 16 (0, ±1, ±4,
  ±9 ... ±49, -64), so **33 bytes for 64 samples, about 0.52 bytes a sample, about 5.4 KB a second**. The steps are
  coarse, so every cry carries a hiss of its own; pret's noisy cries hide it, a pure tone shows it.
- **The tables.** `sound/direct_sound_data.inc` includes each `.bin` as `Cry_<Species>`; `sound/cry_tables.inc` holds
  `gCryTable` and `gCryTable_Reverse`, 388 entries each, the `cry` macro making a voice of type 0x20 (compressed
  DirectSound) at key 60, attack and sustain full. `SpeciesToCryId()` (`src/pokemon.c`) maps a species to its cry; the
  NEXUS residents and the carried line already borrow other species' cries through it (`sNexusCries`, `sCarriedCries`).
- **The player.** `PlayCryInternal()` (`src/sound.c`) builds a one-note song at run time from
  `gPokemonCrySongTemplate` (`src/m4a_tables.c`: tune, voice, volume, pan, a tie on key 60, a wait, the end) and plays it
  on one of two cry players (two, for double battles). **Pitch, length, release, chorus and reversal are set by the
  cry's MODE, never by the species**:

  | mode | when | what it does to the sample |
  |---|---|---|
  | NORMAL | most cries | key 60, untouched: the whole sample (length 140 frames, 2.3 s) |
  | DOUBLES | double battles | **cut after 20 frames (0.33 s)** and faded |
  | ENCOUNTER | static and aggressive encounters | up about a semitone, with chorus |
  | FAINT | a daemon fainting | **down 3.6 semitones** |
  | WEAK | an unhealthy daemon | down 1.4 semitones |
  | GROWL_1, ECHO_START | the moves Growl and Hyper Voice | **played backwards** (`gCryTable_Reverse`) |
  | ROAR, GROWL_2, HIGH_PITCH, ECHO_END | Roar, Growl, Howl, Hyper Voice | shortened, re-pitched, chorused |

  So any new cry must **say itself in its first third of a second** (doubles), **survive being lowered** (faint) and
  **survive being played backwards** (two moves).
- **The bytes.** The 388 `.bin` files take **1,630,415 bytes (1.55 MiB)**: on average 0.77 s and 4.2 KB a cry, from
  0.18 s (pidgey's, PACKET's) to 2.24 s (jynx's, COLDREAD's). The ROM uses **11.1 MB of 16** (`tools/gbabudget.py`,
  about 4.9 MB free; `docs/engine.md`). **Replacing every cry at no more than pret's length is byte-neutral or a saving**
  -- the budget is not the constraint, the length is.
- **Could a cry be a sequence instead (MIDI, or the square and noise channels)?** Not without an engine change. The cry
  player only ever plays one sampled note. A sequenced cry means `PlayCryInternal` starting a song of its own per
  species (388 songs, or a table beside the song table), and redoing what the modes do by hand: pitch by the player's
  pitch control, the doubles cut by a stop, chorus by a second track -- and **reversal cannot be done at all** without
  388 reversed sequences or Growl and Hyper Voice changed. A PSG cry would also **take the square and noise channels
  from the battle music while it sounds**, which a sampled cry never does. It would save most of the 1.5 MB, which the
  ROM does not need. *Not recommended now*; it is the one road here that changes `src/sound.c` and `m4a`.
- **A cheaper engine change exists, if one is ever wanted:** because pitch and length are already arguments to the cry
  song, **a per-species pitch and length table** (a byte or two per species, a few lines in `PlayCryInternal`) would
  let many daemons share one sample. That is what makes D below cheap, and it could let an evolution line share one
  sample in A.

## The six daemons in every example

Chosen across types and stages, each capped at **pret's own length for the same species**:

| daemon | pret's species | types | stage | pret's length | pret's bytes |
|---|---|---|---|---|---|
| HEAP | Geodude | LEGACY / STRATUM | 1 of 3 | 1.116 s | 6,067 |
| STACK | Graveler | LEGACY / STRATUM | 2 of 3 | 1.314 s | 7,141 |
| MONOLITH | Golem | LEGACY / STRATUM | 3 of 3 | 0.666 s | 3,625 |
| SPIKE | Pikachu | SIGNAL | middle of its line | 0.783 s | 4,262 |
| DANGLING | Gastly | LATENT / CORRUPT | 1 of 3 | 1.098 s | 5,966 |
| SINGULAR | Dragonite | EMERGENT / VECTOR | 3 of 3 | 0.896 s | 4,874 |

*Note what the cap does: pret's lengths do not grow along a line (Golem's is the shortest of its three), so "longer as
it evolves" cannot hold under them. The drafts grow by getting lower and slower instead.*

Every example was made as the cartridge would hold it -- 8-bit mono at 10512 Hz, through the engine's own `wav2agb`
with the cries' flags, so the bytes below are measured -- then **decoded back from that compressed `.bin`** and played
through one model of the mixer (13379 Hz). Pret's reference is rendered through the same model.

## The approaches

### A -- THE TYPE'S VOICE

**Each cry is its type's palette from batch 10, the move sounds' motif, played as a phrase**: the harp on the motif's
notes, a square click under each (C BOTH, the game's sound family), the type's noise texture, and for a daemon of two
types the **second type's last note held by the flute**. **The line shares a contour** (its first daemon's name picks
the motif's turn), and **each stage drops the register** (0, a fourth, an octave) and slows it.

- *What it says:* a daemon sounds like **what it is**. A player learns the chart by ear, the same way the move sounds
  already teach it. Kin sound like kin.
- *Cost:* **no engine change.** One generator in `tools/` writing 388 `.wav` files in place (species, types, stage and
  line all read from the engine). The six: **22,779 bytes against pret's 31,935.**
- *Risks:* a cry may blur with its own type's move sounds (they share a motif); seventeen palettes over 388 daemons means
  many near-twins within a type (CONTENT has the most) unless the shaping per species is richer than the drafts'; tonal
  harp shows the compression's hiss more than pret's noisy cries do.

### B -- THE NAME, PLAYED

**Each daemon's name turned into notes**: a letter is a degree of Blanche's C pentatonic (A, K, U the root; B, L, V the
second...), a vowel is **sung** by the flute and a consonant **plucked** by the harp, the last letter held; the octave is
the type's, lowered as the line evolves. *A cry is the daemon saying its name.*

- *What it says:* a daemon **is its name**, and it announces it. It is never explained; a player who spells one out
  will find it.
- *Cost:* **no engine change**; the simplest generator of the four (the names are in `species_names.h`). The six:
  **23,579 bytes.**
- *Risks:* the mapping is arbitrary, so the cries do not group by type or line -- kin do not sound like kin (HEAP, STACK
  and MONOLITH share nothing); a ten-letter name is squeezed and **doubles mode hears only its first three or four
  letters**; it reads as a melody more than a creature.

### C -- THE PROCESS HUMMING

**No melody: a machine sound per type**, synthesised -- a modem's handshake for SIGNAL, a disk seeking for STRATUM, a
stepper motor and its clunk for LEGACY, a fan spinning up for LATENT, a held-level glitch dropping out for CORRUPT,
oscillators drifting into one chord for EMERGENT, air rising for VECTOR (all seventeen are written). A second type is
layered under the first; a later stage is the same machine bigger -- lower and slower.

- *What it says:* a daemon is **the process running**; you hear it work, not speak.
- *Cost:* **no engine change**; a generator of seventeen small synthesisers. The six: **23,604 bytes.** Noise compresses
  well under DPCM, so it hides the hiss best.
- *Risks:* the least like a creature -- the daemons are machines that **became** creatures, and this keeps only the
  first half; harsh to hear twice a battle for forty hours; it will blur with the field and battle noises, which use the
  same textures.

### D -- ONE VOICE, MANY MOODS

**One shared voice -- a sung "ah"**, a buzz through three vowel formants -- and each daemon only a **pitch, a glide and a
length**: the line keeps a note, each stage sits lower, the name picks the glide.

- *What it says:* every daemon has **the same voice**, and only its pitch and breath differ; something almost human is
  speaking from each of them.
- *Cost, two ways:* **baked into 388 samples, no engine change** (the six: **22,868 bytes**); or **one sample (about 4.5
  KB) and a per-species pitch and length table**, a few lines in `PlayCryInternal` -- **about 1.5 MB freed**, the only
  approach that saves real space.
- *Risks:* monotony across 388; a human vowel is a strong statement about what a daemon is -- close to saying it outright
  -- and the uncanny reading may be the only one; a formant voice at 10 kHz with 4-bit steps sounds buzzy.

## Recommendation

**A, THE TYPE'S VOICE** -- with B's idea as its shaping. It is the only one that makes a cry carry the argument (the
type chart, by ear), it keeps the family every other replaced sound now belongs to (C BOTH, harp and flute over square
and noise), kin sound like kin, it needs no engine change and it costs fewer bytes than pret's. Its weakness is
near-twins within a type; the fix is to let the **name** order and accent the type's motif (B's letters choosing the
turn and the rhythm within A's palette), so each daemon is distinct and a line still shares its contour. C is the
strongest second, if the user wants the daemons to sound less alive; D's table is worth keeping in mind only if the
ROM ever runs short.

Whichever is chosen: check it **reversed** (Growl, Hyper Voice), **cut at 0.33 s** (doubles) and **lowered 3.6
semitones** (fainting) before writing any of the 388.

## The examples

Each approach: one clip of the six in a row (HEAP, STACK, MONOLITH, SPIKE, DANGLING, SINGULAR, about 8 s), then each
cry alone. All in `audio/drafts/t565_cries/`, DRAFT:

- `A_the_types_voice_six.mp3`, `A_the_types_voice_<daemon>.mp3`
- `B_the_name_played_six.mp3`, `B_the_name_played_<daemon>.mp3`
- `C_the_process_humming_six.mp3`, `C_the_process_humming_<daemon>.mp3`
- `D_one_voice_many_moods_six.mp3`, `D_one_voice_many_moods_<daemon>.mp3`

| | HEAP | STACK | MONOLITH | SPIKE | DANGLING | SINGULAR | the six |
|---|---|---|---|---|---|---|---|
| pret | 6,067 B | 7,141 | 3,625 | 4,262 | 5,966 | 4,874 | **31,935** |
| A | 3,518 | 4,149 | 3,359 | 2,235 | 5,107 | 4,411 | **22,779** |
| B | 3,428 | 4,031 | 3,214 | 3,627 | 5,075 | 4,204 | **23,579** |
| C | 3,949 | 5,359 | 3,082 | 3,200 | 3,869 | 4,145 | **23,604** |
| D | 3,199 | 3,531 | 3,607 | 3,526 | 4,508 | 4,497 | **22,868** |

**Pret's six, for comparing by ear, are retail audio and are never in git**: they were rendered beside the drafts,
outside the repository, by the same model. The drafts' generator also stays outside the repository until an approach
is chosen; the chosen one becomes a tool in `tools/` like `genuisounds.py`.
