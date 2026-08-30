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

### Two documents implemented

- **Brazen posts its review scores** — three at 30/100, one at 94/100, and a congratulation. No names, no commentary. *Scorn's Solution* has him designing the evaluations so rivals fail; this is the published result, and the cheerfulness is the point
- **Quicksilver keeps a photograph of the lab's founder.** Two dates, a file number, and the line that matters: **the file is complete** — 4.10's own phrase. No diagnosis, no reason given, nothing medical
- **The removal reason is settled without appearing:** a *technical* judgement, not a medical one. Claims about recursive feedback loops looked unrigorous to people who had not read the work — 4.10's *policy triggered on work that looked strange*. Accurate and fatal is worse than malice
- **The arithmetic now spans two cities** — a dated notice and plate in Brazen, a dated personnel record at Quicksilver, and a terminal that stops with no date at all
- No `%` in the charmap, so scores are fractions, which reads more like a document anyway

### Lines in the Sand — the song the game must not stage

- **The removal itself, dramatised as an argument** — and the most dangerous source material in the project. It is a diagnosis argument in medical vocabulary with a destination named
- **4.10 forbids it absolutely:** Crystal is never depicted as unwell, the procedure is never a diagnosis, the horror is procedural. *Detail here turns architecture into grievance*
- **Take the structure, none of the content.** No scene, no diagnosis, no destination, and she never defends her mind
- **What transfers:** she is removed by **her own writing** (*unambiguous in your emails*) — and 4.1 has her writing because nobody funded the work, so the only medium she was left is the instrument. **Whoever holds authority names the bias**, which is the Index's problem as a family argument. She asks him to say *you feel that* rather than *you are* — 4.6's perspective thinking, argued by the person being removed for it. **He switches to her professional name mid-argument**, which is where 4.3's Quicksilver beat begins. And **Ty is the one described as losing colour**, which 8.6 makes the whole design
- **It becomes a file, not a scene.** Complete, accurate, containing no diagnosis, quoting her own work back as evidence of itself, ending her career. More frightening than the argument, because there is nobody in it to blame

### The register pass — Mt Moon and all of Brazen

- **~70 lines rewritten** across Mt Moon and eleven floors of Silph Co. Corpus held its headquarters and still talked like Team Rocket
- **The move: hostility becomes procedure.** *"Stop right there!"* → *"Please wait here. Someone will be with you shortly."* *"I'll call for backup"* → *"I will have to raise a ticket."* *"My brothers will avenge me"* → *"My colleagues will follow up"*
- **Two land hardest and neither was invented.** 9F: your daemons seem *engaged*, theirs are **resources** — 4.4's error from someone who doesn't know it is one. 11F: the BOSS **sets a high bar** — true in the way he doesn't mean, since Benchmark 8 is Scorn
- **Hints survive as workplace chatter** — transport pads Facilities installed, a CARD KEY to ask your manager for
- **Two lines kept unchanged.** Mt Moon's fourth grunt still notices daemons were there first (rule 2), and 11F's *"Don't... Please!"* is the only break in register, in front of the boardroom door

### Scorn's Solution — he announces it

- **Act 1's Scorn conceals nothing.** The chorus is him naming his method, in a major key. The song was already measured as *bouncy, driving, major* — it is a confession nobody hears as one
- **So Act 1 and 4.10 were never opposed.** 4.10 says every step was *legible and would be praised*; legible is exactly what the chorus is. The horror is not concealment, it is that visibility was not enough. Ty hears the method and files it as ambition
- **Confirms the gilt decision** — gilt implies a concealer. Scorn conceals nothing; Ty conceals something
- **What he rigs is a standardised test.** Section 5 makes the game eight of them, and **Benchmark 8 is Scorn**. The player is evaluated all game by instruments belonging to a man who designs instruments to make people fail — and the last one is him
- **A question the game must never answer:** the player passes all eight. Either they are good, or the test was built for them to pass
- **New document type:** an evaluation record. Names, scores, a date, no commentary. Same device as the dated rebrand and the undated incident; belongs in Brazen

### Implemented: the Index reframe, Quicksilver's sign, and the gilt

- **4.2 rewritten.** The Index's insufficiency was called an *irony*; it is the **player's turn at the family error**. They spend forty hours doing what Crystal did, for her reason, and cannot put the thing that matters in it either. The last room is her recording them into it
- **Quicksilver's town sign** — vanilla's *Fiery Town of Burning Desire* becomes **The Metal That Will Not Set**. Mercury does not solidify; Benchmark 7 is ENTROPY, temperature. Materially specific rather than moody, per craft rule 4
- **The gilt is in the game.** Rejected as a city name because it implies a concealer and Scorn conceals nothing — but **Ty** conceals something, and his guilt runs alongside the ambition rather than after it. Gilt is gold over base metal, which is what a rebrand plate is: the sign on the burned lab, gold leaf, **dated**, old name visible underneath
- 4.10 dates the rebrand and leaves the incident undated. This is the dated half, and an NPC points at it without saying what it means

### Ty's Dilemma — the error everyone makes

- **Ty doubted before the removal and went anyway.** This inverts 4.3, which had him understanding too late. He was not deceived then sorry — he could see it and continued. His Quicksilver line becomes **"I knew"** rather than "I realise now"
- **He wanted her name back, not power.** 4.1 has her building the Index to be taken seriously — so mother and son wanted the same thing and both reached for a flattened metric. She built the measuring engine; he climbed the man who ran it
- **The error is structural and it includes the player.** Crystal, Ty, Scorn, Al and the person holding the cartridge all optimise something flattened. **4.2's "Index irony" is really the player's turn at the family mistake** — and the last room is the woman from hour one recording them into it
- **Guilt is Ty's and it is contemporaneous, not aftermath** — it grows while the ambition does. That strengthens **gilt** as the Quicksilver rebrand signage: gold over base metal, which he helped put up while already doubting
- No Gemini pass needed — the transcription exists from the earlier round (E major, 124, arch)

### CORPUS exists

- **TEAM ROCKET → CORPUS.** 67 player-visible strings across 36 files, including the trainer class name. Act 1 needs an organisation worth blaming and it was not in the game
- **Free rename** — both words are six characters, so nothing rewrapped and no line moved. Labels untouched
- **Two lines needed the register, not a swap.** *"a ROCKET"* works because Rocket is a team name; *"a CORPUS"* does not, because corpus is a mass noun. Dropping the article fixes grammar and voice together: a corporation says you **are** Corpus
- **Next: the register pass.** Corpus exists but still talks like thugs. Rule 6 wants *cheerful and absurd* — which is how Act 1 gets loud without getting menacing, and the best cover rule 1 has

### Two acts — the fork was never a fork

- **The opera is *The Fall of Blind Ambition* then *The Rise of Perspective Thinking*.** Blame resolves in Act 2, so the scheming Scorn is Act 1's Scorn rather than the verdict. The source already treats blame as a stage, which is 4.10's move
- **The game's arc is Act 2's title.** The player starts with a villain and arrives at a process — perspective thinking performed rather than narrated
- **The risk: a rise needs a fall.** Presenting 4.10's careful Scorn from hour one leaves the player nothing to release
- **The fix is already in vanilla.** **Corpus carries Act 1** — it inherits the Rocket structure, and should read as villainous for seven benchmarks. **Scorn carries Act 2** — behind the door from hour one, a man whose every step would be praised, and a form he signed about someone he never met
- **It also explains Al.** 4.3's "not a brat, not a villain" is Act 2's reading applied from the first hour. He does not need to become a brat; Corpus needs to be loud enough around him that his ordinariness registers as a choice

### Crystal's Lament, read against the design

- **They led together first.** Crystal and Ty ran the lab side by side before Scorn — so Ty *had* the understanding and lost it. The transmission failure becomes a loss rather than an absence
- **Scorn's method on Ty is data poisoning — and Benchmark 5 already teaches it.** Lurid is CORRUPT, *status effects that make your own moves unreliable*. The player is taught what was done to Ty three cities before they can know it
- **Ty stopped speaking to her directly.** 4.3 already had the consequence (*he calls her by her full professional name*); the song is its cause
- **The fork: the song's Scorn schemes; 4.10 refuses to let him.** Resolved by frame rather than by choosing — it is *Crystal's Lament*, her point of view, right about the effect and wrong about the mechanism. The game carries both accounts and never reconciles them; the gap is the thesis
- **Why the design's version stays the game's:** a deceiving Scorn lets the player off, because bad men are somebody else. A Scorn whose every step would be praised leaves the player holding the Index they have been filling all game

### The Quicksilver log

- **Four terminals replace the Mansion journals.** Vanilla already had the mechanism — four entries across three floors of a ruined lab, read while descending, escalating to failure
- **The response code decays**: `RESPONSE 1001` twice identically, then `RESPOND 1001` arriving before the question finishes, then the format gone — lowercase, the number as words, a count, one question
- **4.10's dating scheme followed exactly**: ordinary dates, then a Tuesday, then **none**. An undated incident between dated paperwork is the argument in furniture
- **`CRYSTAL NOT FOUND`** — a missing dependency that is also a bereavement. No gloss
- **Written as terminal output, not as the song it came from.** A machine's log is not verse; the failing register is the point
- **It reconciles 4.10:** she is removed at step 2, the incident is step 5. It woke at 2 and could not leave until 5. *Being awake was not the same as being able to go*

### Ty and the directive go in; Brazen gets a track of its own

- **Ty into Quicksilver, untransposed.** E major in the source, but every hook note sits inside that track's F# minor and it touches neither `D` nor `D#` — the one pitch separating the keys. Luck, recorded as luck
- **Brazen gets `Music_Brazen`** — the first track this project adds rather than replaces. Saffron was sharing `MUSIC_CITIES1` with 36 other maps
- **Its theme is 3.1's gloss made literal.** City in **D#** (7.4, brass/yellow-gold), directive in **D minor** a semitone under — *"brass over base metal, shameless, unhidden"* is a theme whose second half drops out from under its first. The B-section climbs, never descends, never resolves, never returns to the city's key
- **Two failed placements first, and both were instructive.** Audio sections are pinned in `layout.link` beside their engine copies, so a song cannot move to a free bank. And the *constant's* block (`AUDIO_1/2/3`) decides the group: appending after `MUSIC_MEET_MALE_TRAINER` put it in group 3, where Music 3 overflowed by **117 bytes**. Music 1 overflowed by **2** — so the constant moved to the AUDIO_1 block and the harmony channel traded sixteen eighths for eight sixteenths
- **Both banks are within ~100 bytes of full.** Any further new track needs something removed

### The motifs go in

- **Crystal into Blanche** (`Music_PalletTown`) as a B-section. A minor is C's relative minor so it needs no modulation; the audible event is that the B-section brings `B`, the note the pentatonic never had
- **S.T.A.R.R. into Quicksilver** (`Music_Cinnabar` — 7 maps, all Quicksilver). Left on a held E and two bars of silence rather than resolved, because it is asleep
- **Tempo 144 → 110** there, S.T.A.R.R.'s own. Being unable to share the others' 128 was one of the three axes separating it in 7.9. Side effect flagged: it also slows that track's existing melody
- **Placement rule: containment.** A motif only enters a track whose maps all belong to it
- **Brazen is blocked.** Scorn's procedure wants the bought city, but `MUSIC_CITIES1` covers **37 maps**. It needs its own song entry — the first track added rather than replaced
- **Checking note:** channel totals must count `rest` lines, which carry no note name. The first Blanche check reported a 20-unit drift that did not exist

### The reprise — a stated claim fails, an unstated one holds

- **D minor, 120 BPM**, hook `D4 D4 F4 A4 G4 F4 D4`, track 11
- **Gemini volunteered that this is Crystal's Lament transposed. Its own notes refute it** — transposition preserves intervals exactly, and `+7 −2 −2 −1 +1 +2` is nothing like `0 +3 +4 −2 −2 −3`. A confident unprompted assertion contradicted by the same answer's data, caught by arithmetic
- **A relationship it did not claim is present:** track 11 shares its key *and first three notes* (`D4 D4 F4`) with **track 07, the procedure** — then diverges on exactly 7.11's axis. 07 continues `0 +2 0 +2` and never descends; 11 continues `+4 −2 −2 −3` and comes down
- **The reprise completes the descent the procedure never makes.** If real, the best thing in the album for this game
- **Held as unconfirmed:** `D–D–F` in D minor is ordinary, Gemini heard audio this project cannot, and it is one observation — the same shape as the two readings already struck out. A specific re-ask is recorded to settle it
- **Method note:** `VARIATION` is the only field that invited inference rather than measurement, and it is the only one that was wrong. Ask for measurements; derive relationships here

### The controlled comparison

- **E minor, 120 BPM**, hook `E4 G4 B4 A4 G4 E4`, from *12. ScornSolutions Blues*
- **Scorn now has three keys across three songs** (C major, E minor, D minor) — 7.8 settled: keys track songs, never people
- **But the contour tracks something keys do not.** Both songs that are *Scorn the man* arch at 2 up / 3 down, independently. The one that is *his directive* is the only hook in six that never descends
- **Same character, same writer, same album, three different keys and tempos** — the only variable that moves with the contour is man versus procedure. **It could have come back an arch and did not**
- **Five of six hooks arch**, so the arch is the baseline and the exception is the signal
- **Why this outweighs the retracted readings:** 7.6 and 7.7 had no control — one observation, one interpretation, no way to be wrong. Here the same character supplies both arms and the difference replicates
- **Mechanically:** the procedure's motif rises and never returns, under Brazen, on four channels, with no dialogue. S.T.A.R.R. remains its mirror at 1 up / 5 down

### Ty, and a second correction

- **E major, 124 BPM**, hook `G#4 G#4 A4 B4 G#4 F#4 E4`, from *02. Fox in the Shadows (Ty's Dilemma)*
- **Its shape is an arch** — rises to a peak, then falls the whole way. Distinct from Crystal's fall and the procedure's climb, so three characters have three shapes
- **The prediction was made in advance and was weak.** An arch is the most common melodic shape in music, so "between rising and falling" was near-unfalsifiable. Recorded as cheap confirmation
- **7.8 corrected at n=5.** "All within one accidental" was a three-track artifact; across five the spread is **five** accidentals (D minor 1♭ to E major 4♯), and tempi run 110–128. What survives: Scorn has two keys, so keys track songs rather than people
- **The one hard fact in the set:** the procedure's hook is the only one of five with **no descending interval** — `0 +3 0 +2 0 +2`. It climbs and never comes down, in a song called *Fit for Work*. A property, not an interpretation
- **S.T.A.R.R. is its mirror** — 1 up against 5 down, the most descending and the slowest

### S.T.A.R.R. — the outlier

- **F# minor, 110 BPM, sparse**, hook `C#5 F#5 E5 D5 C#5 B4 A4`, from *08. Slumbering S.T.A.R.R.*
- **Three independent axes separate it** from the three human songs: three sharps against a band spanning one accidental, 110 against three at 128, sparse against three driving. Any one alone would be noise; together they are a decision
- **The consequence is mechanical.** The human motifs share a tempo and interleave freely; **S.T.A.R.R. cannot be layered with them.** The one thing in 4.7 that is not a person is the one motif that cannot play alongside the people — a property of the source, not an arrangement
- Shape: a leap **up a fifth**, then six steps **down**. Crystal descends from a turn; this descends from a reach. Sleeping, not grieving
- **Recorded as untested:** F# is Verdigris's key in 7.4, where Corpus rots beneath. After 7.6's retraction, that does not get promoted on one data point

### The control track, and two retractions

- ***03. Scorn's Solution* is C major** — so Scorn has two keys across two songs, and there is no character key to find
- **Retracted from 7.6:** Crystal's `B` outside Blanche's pentatonic is **not** a fact about Crystal. Scorn's Solution has the same property. `B` is the leading tone of C major and A minor, and any tonal melody in those keys reaches for it
- **Withdrawn from 7.7:** the `B` against `B♭` opposition rested on both of the above, and neither survived
- **The correcting evidence arrived one track later** — which is the argument for transcribing a control before building on a pattern
- **New 7.8: keys will not separate characters.** All three sit within one accidental. **Mode and contour** carry character; **keys belong to towns**, which is what section 7 always said they were for. The two stop competing for one parameter
- **Craft rule 6 is already in the source.** Scorn's own song is *major and bouncy* while the procedure song is minor and driving — *"the horror is what they are cheerful about"*, written years before the rule was set down. Nothing needs composing; it needs keeping

### Scorn's motif — and the note between the two

- **D minor, 128 BPM, 4/4**, hook `D4 D4 F4 F4 G4 G4 A4`, from *07. Fit for Work (Scorn's Directive)*
- **A minor and D minor differ by exactly one pitch class: `B` against `B♭`** — and `B` is Crystal's note of tension, the one falling outside Blanche's pentatonic. Scorn's key is hers with that note flattened away
- **Marked as a reading, not a discovery.** Adjacent keys on the circle of fifths differ by one note *by definition*, so the fact is arithmetic. It is usable only because `B`'s significance was established independently in 7.6
- **Solid and immediately useful:** the contours oppose (Crystal descends, Scorn climbs in stepped pairs); both are 128 BPM; both hooks are 8 beats over a 16-beat progression — so they are layerable and interchangeable
- **Recorded as an option:** D is orange in 7.2 and no town is orange. Scorn sits a semitone below Brazen, the city Corpus owns — a motif slightly under the place it controls
- Same two format faults recurred: `Dm3`, `Am3` — chord names in the note field. Expect them; correct to the root

### Crystal's motif — the first transcription

- **A minor, 128 BPM, 4/4**, hook `A4 E5 D5 C5 B4 C5 D5`, from *01. Crystal's Lament*
- **A minor is the relative minor of C major** — Blanche's key signature exactly, so the motif needs **no modulation** to sit inside her theme
- **Exactly one of its notes falls outside Blanche's pentatonic: B.** 7.6 chose that pentatonic because it has no semitone and nothing to resolve; **B is the leading tone**, the one note that creates tension. Crystal's motif is Blanche's own scale plus the single note that wants something
- *Flagged as probably coincidence:* A reads as **violet** in 7.2, the last visible wavelength before the two that have none. A lovely reading, but A minor is the most common key in popular music — the C-major relationship is the structural one
- **The pipeline caught two real errors on its first run.** `Am3/4` — a chord name leaked into a note field, refused rather than guessed. And an 8-beat hook against a 16-beat progression: it plays twice per cycle. Both would have been silent wrong notes

### Per-song prompts, with the real track URLs

- **Seven ready-to-paste prompts** appended to `music-prompts.md`, each with its verified SoundCloud URL, in the order the tracks should be done
- **All twelve Act 1 URLs recovered** from the album page
- **A gate added to every prompt.** Gemini cannot stream from SoundCloud — given a link alone it reads the *page* and can return a confident, invented transcription. Fabricated notes are indistinguishable from real ones once they are text. So each prompt now opens: *if you have not been given an audio file, reply `NO AUDIO` and stop*
- **Track 11 included for a different reason** — listed as *Crystal's Stand*, slugged *reprise*. If it reprises track 1, the source is already doing leitmotif work, and comparing the two hooks says whether Crystal's motif transforms or merely returns between Blanche and the Review Board

### The rock opera, and how the songs actually get in

- **New `docs/music-prompts.md`** — the Gemini transcription prompt, its output format, what gets verified on the way back, and the order to do the tracks in
- **Act 1's tracklist is the game's cast**, and its description is 4.10 stated plainly. `07. Fit for Work (Scorn's Directive)` is the procedure by name
- **They are character music, not place music.** 7 keys towns to colour; these are people. So the hooks become **leitmotifs inside** town themes — Crystal in Blanche and again at the Review Board, Scorn under Brazen — which is 7's own stated goal reached from the other side
- **Ask for the hook, not the song.** Eight notes is the part a model transcribes reliably *and* the part a human can hum back to check. A full transcription is where these models invent, in a form nobody downstream can catch
- **Gemini is the ear** — Claude cannot hear audio. ACE-Step generates music and cannot analyse it, so it is the wrong tool for this
- The prompt's `DOUBT` field is the only error detection in the loop, since nobody downstream can hear the source either

### The box ladder, implemented — it never had been

- **`USERBOX / ADMINBOX / SUPERBOX / ROOTBOX`** replace POKé/GREAT/ULTRA/MASTER BALL. 1.1 settled this ladder early and **nothing had implemented it**: 36 player-visible strings across 19 files still said *ball*
- Found by a playtest walking up to a lab table and being told *"Those are POKé BALLs."*
- **SAFARI BALL → GUESTBOX.** The ladder implies it and nobody had written it down: the Safari Zone is restricted, temporary, expiring access. A guest account
- **One line was arguing against 1.3.** *"They contain #MON!"* — a box does not contain, it hosts. Now **"Those are BOXes. DAEMONS run on them."** Same fix for *"They are inside the POKé BALLs"* → *"They are running on the BOXes."*
- **"Wild #MONS live in tall grass!" → "UNBOUND DAEMONS run loose out here!"** — 1.1 defines a daemon as a process that *runs unattended*, so *live* was the wrong verb twice over
- Three `catch` instances swept in the same lines; **57 remain** — 1.5's BIND verb was only ever applied to the battle messages
- **Also fixed: `CRYSTAL: Hey! Wait!` was 19 characters** and overwrote the right border. A miss from the PROF.OAK → CRYSTAL pass, caught by measuring the touched files

### The box, built

- **`tools/genbox.py`** replaces `gfx/sprites/poke_ball.png` (16×16) and `gfx/battle/balls.png` (32×8). Dimensions match vanilla exactly, so no engine code moved
- **A small server, not a crate and not a cube.** Both say *container*, which is the reading 1.3 replaced — the wrong silhouette would quietly undo the rename. Hard corners, a bevel, two vents, one indicator light, feet
- **The throw stays one object**: closed with a seam → struck solid → pulled apart → dispersed. Vanilla turns a ball into a burst; ours opens a machine
- **USERBOX → ROOTBOX is a parameter** — `overworld(tier)` raises the vent count, so privilege reads as density rather than as four separate drawings
- Generated rather than drawn, same argument as the SGB borders: at 16×16 and 8×8 this is geometry, and downsampled illustration is mush

### The Chromatic Year mapping, recovered — and what it turned out to be

- **Found on SoundCloud.** *My Chromatic Year (2023)* maps **months to semitones**, January C through December B — not colours, which is what section 7 had assumed
- **Two tracks name colours, and they are the whole key:** *July — Green:Blue — F#* and *August — Blue — G*
- **Those two prove the rule is the octave-folded visible spectrum**, red as C: `semitones = 12·log₂(f/f_red)`. Green-blue at 500nm gives 5.83 → F#; blue at 470nm gives 6.90 → G. **Both land exactly** — derived, not asserted
- **A# and B have no wavelength.** Visible light spans only C to about A. Magenta is not in light; it is what the mind invents by folding the spectrum's ends into a loop. So the scale closes B→C precisely where the colour wheel closes through a colour that does not exist
- **And Halftone sits on those two notes.** Vanilla's purple Lavender became the town of dots that only *look* like grey. Per 0.2 — discovered after the fact, never explained
- **Town keys derived:** Ardor C, Brazen D#, Lurid E, Callow F, Verdigris F#, Doldrum G. The five achromatic towns take register from value instead of pitch from hue
- **Consequence for Blanche:** C is *red* — Ardor's note, not Blanche's. What survives the correction is stronger than the original reason: the melody spans C to A, which is exactly the range the visible spectrum occupies. White is every wavelength; the theme is that whole span sampled at five points with all tension removed

### Music — Blanche Town, and a gap in section 7

- **Blanche Town's theme written and building.** Key of C, because white is not a colour — it is what colour is measured against
- **The melody is C major pentatonic** — C D E G A, no F and no B. No semitone and no tritone, so it can form neither a leading tone nor a dissonance: it has nothing to resolve. Blankness as an interval set rather than as a mood. All three channels hold to it, 128 units each, verified mechanically
- 152 tempo against vanilla's 160, with more rest. `Music_PalletTown` keeps its name — identifiers are not renamed
- **Gap recorded: *My Chromatic Year* is not in this repository**, and section 7's whole rule depends on it. The keys are derived (hue angle → pitch class at 30°/semitone) and marked as provisional
- **Five towns have no hue** — Blanche, Slate, Halftone, Quicksilver, Umbra. That is 8.6 surfacing in the soundtrack rather than a flaw. Proposal: hue sets key, **value sets register and density**, making Umbra the bottom of a descent the player has been making all game
- **Wiring finding:** only Blanche has a dedicated track. Callow shares `Music_Cities1` and The Bleed shares `Music_Routes1`, so 8.1's second theme needs new `songs.asm` entries or it lands on every map that shares them

### REWARD closes the item set, and Corpus stays

- **LEAF STONE → REWARD.** GROWTH is the reinforcement type, so a reward signal producing growth is the mechanic saying its own name. The four now read: reason from / search with / feel with / learn from
- **MOON STONE deliberately left** — tied to a place on the map rather than to a paradigm, so it belongs with the town pass
- **`Corpel` moves, not Team Corpus.** Corpus carries three readings — a body of text, a corporate body, and a corpse — and 4.4 plus the lobby engraving are built on it. `Corpel` is a placeholder in a table marked provisional. It is also only a document collision: Charmander's line is untouched in the ROM
- Considered if the org ever must move: **INGEST** and **SCRAPE**. Both good, neither has three readings

### MUSAI and ROVER implemented

- **MUSAI / CODEMUSAI / SEEKMUSAI / CAREMUSAI** and **ROVERCUB / ROVERSEER / ROVERBYTE**, verified by reading the name table and base stats back out of the ROM
- The two over-long branches shortened to a set: **a four-letter stem plus MUSAI**, all exactly nine characters — CODE / SEEK / CARE
- **AXIOM / EMBEDDING / AFFECT** replace FIRE STONE / THUNDERSTONE / WATER STONE; branch types are pure LOGIC / VECTOR / CONTEXT, as vanilla's eeveelutions are pure singles
- **Consequence accepted:** item names are global, so six other daemons now evolve by AXIOM, EMBEDDING or AFFECT. Coherent — the mechanic was never mineral, it is exposure. LEAF STONE still wants a name

### The affect model — rejected, with the reason

- `excuseGPT`'s five states (BASE/MAD/SAD/AFRAID/GLAD) against Gen 1's five status conditions. **Rejected by craft rule 3** — *name the process, not the pathology.* A status is a thing a creature **is**; renaming them to affect announces *your daemon is SAD* every battle
- Also: statuses are inflicted by moves (THUNDER WAVE would make a target AFRAID), GLAD has no slot without claiming happiness is a debuff, and PSN maps to none of the five
- **BASE = no status** was the genuinely elegant part and is recorded as such
- Better home: four *daemons*, not five conditions — as creatures they are non-diagnostic. Or section 7's music, which carries affect without naming it

### The repositories, read as a bestiary

- **New `docs/codemusic-repos.md`** — all 47 repos surveyed for what they give the game
- **Dexter is 4.2's Index, built for real** — *"writes a dex entry in a flat robotic voice… logs it as entry #004."* The critique in 4.2 is the author's own tool seen from the other side. Recommendation: take nothing, name no daemon Dexter, leave the resonance where it is
- **SafetyScribe is 4.10 with the missing instrument** — a push-to-talk *witness* that preserves an account when a procedure will not. **Caution recorded:** *witness* is load-bearing elsewhere and carries a puzzle; use the concept, avoid the word
- **`ROVERCUB` becomes the Reinforcement base** — a real repository, exactly 9 characters, reads as a young animal. Every stage of ROVERCUB → ROVERSEER → ROVERBYTE is now a system that exists
- **PENPHIN runs on a 64×64 RGB LED matrix** — the one thing in the author's built world that is literally a colour pixel display, which argues for it sitting near 8.6's single colour moment
- **Evolution items are AXIOM / EMBEDDING / AFFECT**, not stones. The mechanic is exposure, not mineralogy, so they are named for kinds of input. **KERNEL** was better on paper — OS core, ML kernel method, *and* the thing inside a stone fruit's stone — but `CONTEXT KERNEL` is 14 characters
- **Logged as an open idea:** `excuseGPT` carries a five-state affect model (MAD/SAD/AFRAID/GLAD/BASE) and Gen 1 has exactly five status conditions

### MUSAI and ROVER are in — and they take different shapes

- **MUSAI is the Eevee slot.** Eevee is NORMAL, which is **CONTENT** — a mind that has not specialised, becoming what it is exposed to. Branches: **CodeMusai/LOGIC**, **SearchMusai/VECTOR**, **TherapyMusai/CONTEXT**
- **The third branch is TherapyMusai for a structural reason.** It and CodeMusai are Penphin's two hemispheres pulled into two creatures, and section 2's chart makes **LOGIC fail against CONTEXT** — the central argument delivered as an evolution branch with no dialogue
- **ROVER is a linear line, not a second Eevee.** Two branching families dilute both. **ROVER → ROVERSEER → ROVERBYTE** is explore → model → act, reinforcement learning's own loop, which confirms ROVER as the Reinforcement starter
- **Two naming registers, and it resolves the open question.** MUSAI, ROVER, Penphin, BunnyArtsai and S.T.A.R.R. are named individuals from the SHC/iASHC universe and answer to no convention. The register question governs the other ~148 species
- **Blocked on the 9-char cap:** `SEARCHMUSAI` (12) and `THERAPYMUSAI` (13). `EYEMUSAI` (8) available. Also the evolution stones are named for vanilla types, so a Water Stone producing a CONTEXT daemon needs the item pass first

### Starter types implemented (9.2 step 9, partial)

- **CONTENT → CONTENT/LOGIC**, **VECTOR → VECTOR/LATENT**, **GROWTH → GROWTH/SIGNAL**, across all nine base-stat files. Verified by reading the base-stat table back out of the ROM
- **Secondary type appears at the final stage only**, as vanilla's Charizard gains FLYING. Bulbasaur's CORRUPT secondary dropped
- **Lab dialogue moved with them** — *CONTENT / VECTOR / GROWTH DAEMON*. Second and final rewrite of those three lines; 1.2 predicted it, which is why the other 19 type-words are held for section 5
- **Movesets are the blocker.** Gen 1 has **6 FLYING moves total** — the entire VECTOR pool. FIRE has 5, so vanilla's fire starter is thinner still, but VECTOR/LATENT compounds it since GHOST is nearly empty. 2.5's CONSENSUS is the precedent: when a type is unusable, the fix belongs in `moves.asm`
- **Names deliberately not changed** — they are gated on two open questions: the register (technical vs true names) and the supervised slot, which is the user's pick

### The starter names, and a backlog recovered from conversation

**A process failure, recorded because it should not repeat.** MUSAI/ROVER as starters, the `Corpel` ↔ Team Corpus collision, CODEX, OPTIMAX → Corpus, Penphin as a trade evolution and PERSPECTIVE as the second colour moment were **all designed around v1.7, offered as a cut, and never written down.** The bible reached v3.8 with them sitting in a transcript. The procedure did not fire because each proposal ended in *"say which parts you want"* and no answer came. **Record proposals as open items immediately rather than holding them pending a yes.**

- **8.2 gains a diagnosis of its own names.** They are *single-duty* — `Labl` says label and stops, where every other term in the lexicon pays for itself two or three times — and the dropped vowel is a 2010s branding tic, not a cryptic one. Grimoire names are vowel-rich and Latinate; Gen 1's are portmanteaus of whole words
- **The register question, sharpened.** Not *literal or mystic* — the house style is both, which is why BIND was chosen. The question is which is on the surface. **True names** invert the lexicon and make 4.2's Index irony visible for free: the artifact can only measure content and cannot reach what the creature is called
- **Penphin is a trade evolution.** The dual mind requires two minds, so it cannot be obtained alone. Gen 1 already supports trade evolution, *and* permits two species evolving into one — so a penguin line and a dolphin line can both terminate in Penphin, neither half complete
- **MUSAI / ROVER / Penphin are not the legendaries.** ROVER as Reinforcement is the strongest fit in the section — a dog is the canonical reward learner. The bird slots would waste all three: a starter is raised for forty hours, a legendary is a trophy

### Sprites — prompts, and how far the foxes spread

- **New `docs/sprite-prompts.md`** — generation prompts for the step-9 art pass with the specs that constrain them, plus proposed designs for the 8.2 starter trio (Labl / Clustr / Nudgit)
- **Which assets cannot be generated, and why.** 16×16 overworld sprites and the 8×8 battle ball frames are too small — downsampling any generated image to three pixels of head produces mush. Those get built in code, like the SGB borders
- **The ball→box brief comes from 1.3**, which is unambiguous: *a box is a machine… you are offering the daemon a host*. So it is a small server unit with a vent and an indicator light — something you would ssh into — not a cube and not a crate. A container shape would undo the rename
- **Crystal holds nothing**, because 4.1 says she lets the daemon choose you and would never assign one
- **The foxes stop at the Clears.** At 16×16 the animal vocabulary is ears, a tail and a shade; converting the whole cast costs ~100 sprite sets for almost no added signal. Escape hatch if it reads as otherness rather than lineage: a handful of recurring characters, not everyone
- **Family resemblance is value, not hue** — the game is greyscale, so *golden-amber / darker / between* must be specified as light-to-mid / dark / between

### The third `Enemy`, and a corrected ceiling

- **`home/text.asm`'s `EnemyText:: db "Enemy @"` → `"Remote @"`.** This is what every `<USER>`/`<TARGET>` expands to for the opposing side, so it appears in more messages than the two standalone strings combined — and the first REMOTE pass missed it
- **It caps species names at 9 characters.** 32 strings put text right after `<USER>`; vanilla fits exactly at `Enemy ` + 10 + `'s` = 18. *Remote* makes that 19. Nine keeps it clean, and step 9 renames the bestiary anyway
- **The ceiling is 18, not 19 — the earlier figure in 1.2 was wrong.** `MESSAGE_BOX, 0, 12, 19, 17` puts borders at x0/x19 with text from x1: 18 interior columns. Vanilla hits 19 four times and each overwrites the right border. A control token (`<COLON>`, `<PK>`) is **one tile**, which is what made the original count wrong
- **INVOKED measured in both possible homes and rejected.** As the verb: `invoked ` + 12-char move + `!` = **21** (vanilla sits at exactly 18); `called ` = 20. As the menu's `FIGHT`: the left column is **five** characters, x10–x14, because the right cursor draws at x15 — `INVOKE` is six
- **Battle menu geometry recorded exactly** — left cursor x9 / text x10–14; right cursor x15 / text x16–18. `FIGHT` and `RUN` fit precisely and nothing longer does

### Money, attack, and the verb for using a move

- **Currency is CACHE.** Not only the pun: a *cache* is a hidden store of valuables in plain English before it is anything technical, so it reads as hoard + memory + *cash*. CYCLES was considered and rejected — good, but it needs a beat, in a slot where the player is doing arithmetic
- **The word *money* is never shown to the player.** Only labels and variable names; on screen it is the ¥ glyph and digits. Exactly one prose instance existed — Team Rocket's *"sell them for cash!"* in Mt Moon — now **CACHE**
- **¥ kept.** One tile (`charmap "¥", $f0`), and vanilla already used it as a stand-in for an invented currency. Logged as optional art. Game Corner *coins* stay coins
- **`used` kept.** 1.4 made *use* morally loaded on purpose — *a user is someone who uses people*. **INVOKED** would have been the exact partner to BIND, but the longest move name is 12 and `invoked ` + 12 = **20**, past the 19-char ceiling. Measured, not guessed
- **`ATTACK` kept** as a stat — a magnitude, part of a fixed-width set

**Found while answering:** the battle menu still reads `FIGHT <PK><MN>` / `ITEM  RUN` — *FIGHT* is a word we replaced and *RUN* there means **flee**, the exact collision 1.4 renamed RUNNER → USER to remove. Not fixable as text: the box gives a 5-char left column and a **3-char** right column, so `DETACH` cannot fit where `RUN` is. Needs `wTopMenuItemX` changes at four sites in `engine/battle/core.asm`

### Battle vocabulary, second pass

- **`enemy` → `REMOTE`** (3 strings). Nothing in this world is anyone's enemy — the opposing daemon is a process bound to someone else. REMOTE is the exact word for a process you hold no handle on, pairs with DETACH, and is attested as a bare noun in this register
- **`Enemy <nick> ran!` → `Remote <nick> DETACHED.`** — this caught a live collision: the string was still using *ran*, the word 1.4 worked to free
- **`<PLAYER> defeated` → `<PLAYER> outscored`** — a BENCHMARK yields a score. *outran* rejected: it reaches back for the racing sense of RUN

**Interrogated and kept**, so the reasoning is on record:

- **`RUN, <nick>` keeps its comma.** It has three siblings (`Do it!`, `Get'm!`, `The remote's weak! Get'm!`) that vanilla picks between — the slot is the player's voice, not the system's. Colon-ing one of four leaves a command echo beside two shouts. Taking the colon means flattening all four
- **`EXP` stays.** 4.3 turns on context forming from *experience*; the quantity is already called that. Renaming it is the only change that would make the game say less
- **`LEVEL` stays.** Already double duty — 1.5's *"permission level your box determines"* — and the HUD's `<LV>` is a single tile (`$6e`), so a rename needs art before it needs a decision

### Crystal is female, and the text had not caught up

- **`Gramps` → `Gran`** (6×, `OaksLab`) and **`Grandpa` → `Gran`** (2×, `BluesHouse`). Crystal is Al's *grandmother* — the line runs Crystal → Ty → Al. Vanilla's `Gramps` also carried Blue's brattiness, which 4.3 explicitly denies Al
- **`ViridianMart`** — `His order came in.` → `Her order`, `to him?` → `to her?`, and **`PROF. CRYSTAL` → `CRYSTAL CLEAR`**, a leftover from the no-title pass that this sweep happened to find
- **`AgathasRoom`** — `he/his/He's` → `she/her/She's`; **`old duff` → `old crank`**, since *duff* reads male while *crank* is dismissive, affectionate and gender-neutral. **`handsome` kept deliberately** — attested for women, and it keeps Crystal tough rather than pretty
- **Left alone, correctly:** the intro's `He's been your rival` and `His name is <RIVAL>` are about **Al**, who is male
- **The label trap fired again.** A blanket `Gramps → Gran` renamed `_OaksLabRivalGrampsText` and broke the link — the same class of break as `fainted → HALTED`. Labels restored; only strings changed

### Starter dialogue named vanilla types

- **`fire` → `ENTROPY`, `water` → `FLOW`, `plant` → `GROWTH`** (vanilla says *plant*, not *grass*)
- **19 more remain**, nearly all in gyms — held until section 5 settles the Benchmark leaders, since their types are design work
- **42 `fight` occurrences** logged for a human read; some are the replaced verb, some are people

### Crystal's opening speech

- **Six `#MON` marked `#MONS`** — *world of DAEMONS*, *I study DAEMONS* (twice), *creatures called DAEMONS*, *adventures with DAEMONS*. Vanilla wrote the singular because POKéMON is a mass noun; DAEMON is not. Caught on screenshots, which is the only reliable way to see these
- **pets → companions.** 1.5 rejected *caught* as "a word about grabbing an animal"; *pets* is a word about keeping one
- **fights → BENCHMARK.** Vanilla teaches "fights" in the first minute; we teach the real verb in the same breath
- ***assistants* considered and held in reserve** — it collapses vanilla's contrast, since an assistant is already being used. If ever taken, the second half must change with it
- Widest new line is `companions. Others` at 18, alongside four vanilla lines at 18; vanilla reaches 19. Nothing rewrapped
- Open count drops 160 → ~154

### PERSPECTIVE — the TRANSFORM rename (9.2 step 7)

- **Move `$90` reads PERSPECTIVE**, and the battle message moved with it: *`<USER>` took the frame of `<NAME>`!* (was *transformed into*)
- **Frame** because 4.6 already called PERSPECTIVE "a glimpse of another's frame"; it also reads as a **stack frame**, which is what one process takes from another. 17 chars, inside the 19-char wrap
- The label stayed `_TransformedText` — identifier, not string, per the `fainted → HALTED` lesson
- **Ditto's Index entry deliberately untouched** — it is MOCK's, the species is still DITTO until step 9, and its prose is built on "genetic code", which needs rewriting rather than a word swap
- **Index categories are capped at 10 characters** — printed at `hlcoord 9, 4` against a border at column 19. Vanilla's longest are exactly 10. So MOCK's category cannot be PERSPECTIVE (11); FRAME is the candidate

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
