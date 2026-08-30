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

### v9.5 — the bible catches up to the ROM

*The PDF was current for `vision.md`; `vision.md` had fallen behind the cartridge.*

- **7.4 gains a build table.** Three of six coloured towns are in — Ardor, Brazen, Verdigris. **The other three are not blocked**: Lurid, Callow and Doldrum share a music slot with maps that are not towns, so they need a repoint in `songs.asm` rather than a body swap
- **7.9's untested placement was taken, and is still not a finding.** *Awakening S.T.A.R.R.* now plays in Verdigris — **because 7.4's rule assigns F# to that town and the track is F#**, which is the rule working, not evidence for the coincidence. **The one data point has not become two**
- **New 7.9a: the splash.** The title screen points at the body Mt. Moon plays, so it costs no bytes and freed 916. **The game opens on the track it uses for its dark places** — heard before the player has anywhere to put it, met again underground, unmarked
- Achromatic towns recorded as taking value, not hue. **Slate and Umbra are still unwritten**

### Five tracks assigned, and the space grew

- **Ardor ← *Scorn's Solution*** (C major). 7.4 derives Ardor's key from red heat as **C** — **a lookup, not a choice**
- **Verdigris ← *Awakening S.T.A.R.R.*** (F# minor). 7.4 gives corrosion **F#**
- **Halftone ← *Love Persists*** (D minor). Achromatic, so no derived key; it takes D minor from the story. **The most falling hook in the corpus, in the town with the tower**
- **The Corpus building ← *Nine Scars, Nine Breaches*** (D minor, the crowded address). **The player walks in over the engraving and hears the breaches.** Nothing says so
- **The ruined lab ← *1001 Fatal Error*** (B♭ minor) — **it plays in the building whose terminals carry the log**
- All five went onto **dedicated slots**, so no other map changed. Three headers dropped from 4 channels to 3
- **The space grew.** 901 bytes free at session start, **3792 now, with six more tracks in the ROM.** Replacing bloated vanilla bodies with compact ones frees more than it spends — room for roughly **eighteen** more at ~200 bytes each

### The splash is Echoes, and the bank-full claim was wrong

- **`Music_TitleScreen` now points at `Music_Dungeon3_Ch1/2/3`** — *Echoes of the Algorithm*, **the same body Mt. Moon plays**, in the same bank. **Repointed rather than duplicated: zero new bytes, and 916 freed** by dropping the vanilla title music. The game opens on the track it uses for its dark places
- **The "bank full" claim was wrong and is retracted.** Measured from the linker map: `$02` has 8 bytes, `$08` has 175, `$1f` now has **1634**. **Our tracks run 89–478 bytes against a median vanilla track of 427**, so the 1817 free right now hold **roughly eight more tracks with nothing culled**
- **It was only ever true of appending without displacing.** The real budget is culling: `SilphCo` (1114), `Credits` (986), `Routes4` (902) and `Cities1` (831) **free 3833 bytes between them**, and every one is a track a total conversion intends to replace
- 06, 10 and the Owl are re-marked **pending**, not blocked

### The Corpus lobby engraving is in the ROM

- **`bg_event 11, 16` on SilphCo1F — the tile directly inside the lobby door**, so the player is standing on it the moment they arrive in Brazen. *Cast into the floor, worn smooth*, then the line, then nothing
- **No attribution, no comment, no NPC** — 4.4's placement rules kept exactly. It is furniture
- **This completes the unsigned trio in the ROM**: the engraving, the CC-7 countersignature, and the forest carving (4.20)

### Whispers in the Wires — cut for the right reason, and it is still hers

*Cut from Act 1 for making Ty and Richard look aware they were doing wrong. The instinct is correct — knowing conspirators collapse the polymath mechanism (4.20). **But the song is not narration. It is her.***

- ***Plot and scheme* is what two men conferring quietly and filing minutes you are not in the room for looks like from inside her frame.** It is exactly what a conspiracy looks like — **and the horror is that it is not one.** 4.10's principle at full strength
- **The corpus marks it as hers unprompted: A minor/128 is *Crystal's Lament*'s exact address**
- **She never changes tempo.** Lament (A minor), Whispers (A minor), Reply (A major) — **three songs, 128 throughout the whole opera.** Everyone else speeds up or stops; she does not
- **Her suspicion and her answer are the same four-chord loop, rotated.** Am | F | C | G is vi–IV–I–V; *Crystal's Reply* is I–vi–IV–V. **Where you start decides whether it resolves** — the thesis in harmony, and nobody arranged it
- **No dominant, so it cannot cadence.** It joins *Betrayal's Sting*: **the two songs that cannot resolve are Scorn's doubt and Crystal's suspicion** — sealed inside a frame with no exit, **for the same reason, that neither holds the other's field**
- **Disposition: kept as her frame, never as narration.** No sign, log or minute ever says the two of them schemed. **Not implemented, and that is the decision, not a backlog item**

### Poly is polymath — the removal mechanism, found

*Corrects v9.1's reading. **Poly** is polymath and **fields** are disciplines, and that is the reason Crystal was pushed out — the piece that had been missing since the question was first raised.*

- **Crystal moves between disciplines mid-argument** because to her they are one continuous surface. **Ty and Richard hold one field each**, and from inside one field, fluent movement between several is indistinguishable from incoherence. ***I cannot follow this* is identical to *this does not follow* unless you hold the second discipline.** Nobody lied, nobody was stupid, nobody conspired
- **The observation was true. Only the inference was wrong.** *Moves between unrelated fields without completing an argument* is accurate — **the wrong word is "unrelated"**, and only a second field tells you so
- **Which makes it the same crime as the CC-7 requisition, twice.** *IMPROVE RESPONSE CONSISTENCY* is also technically accurate. **One form describes damage in the vocabulary of an improvement; the other describes competence in the vocabulary of a symptom.** This is what 4.10 means by the paperwork being in order
- **It settles the standing problem with no clinical word at all.** The process is *field-switching*; the game never reaches for anything else
- **The Clarifier is a polymath in hardware.** She built the one instrument that would not file minutes about her — and **Scorn then performed on it the exact operation that had been performed on her: reduce many fields to one.** The form he filed asks it for *consistency*, the property whose absence got her removed. So **4.13's awakening is the machine becoming polymathic again**
- **Built.** The Meeting Room door at Quicksilver is now the minutes: *Item 4… Two present could not follow. Recorded as unable to hold a single thread.* **Two doors, two honest documents** — R-and-D holds the requisition, the Meeting Room holds the assessment. **Neither sentence makes the argument; the gap between them does**

### Poly and Fields — where the chart comes from

*Cut from the opera, and it carries the one thing the corpus was missing: an origin that is not corporate.*

- **G | Em | C | D is I–vi–IV–V, and the only other one recorded is *Crystal's Reply*.** A child alone in the trees and a mother's answer, same four chords, transposed. That the person in the grove is the one who founded the lab is **offered, not asserted** — the harmony is the whole of the evidence
- **110 BPM is shared with one track only.** The two quietest places in the corpus are **a machine asleep and a child in a grove**
- **Perspective thinking starts as an accident.** Not a technique or a benchmark — somebody who could not see what their own family saw. Everything the game argues for begins as a child's failure to fit. **And the process word arrives as arithmetic**: the song says *integrating* and means calculus, decades before anyone needed it clinically
- **The type chart gets a pastoral origin.** Polynomials over fields is where relations stop being arbitrary and become lawful and closed — **each thing, and what it does to each other thing, in rows.** It was not designed in a corporation to sort daemons for use; **it was found carved on a stone by a lonely child who was good at maths**, and the corporate reading came later, from people who did not earn it
- **A second engraving.** The lobby one is cast into a floor, unattributed, adopted approvingly (4.4); this one is carved in a forest and unsigned too. **The same technique, used innocently first** — and the player meets the copy long before the original
- **Built.** The western sign in The Undertone at (4, 24), formerly a USER TIPS sign: moss, a small figure with folded hands, symbols in rows older than the path, *read across*. **Three unsigned documents now** — the engraving, the countersignature, and this. *Nobody puts their name on the thing that matters*
- *Craft note:* the player finds it **in the first real maze, lost.** The place explaining how relations form a lawful structure is the place they cannot find their way through

### The Cognitive Clarifier is in the ROM

- **The chip is reinstated. What is declined is the smuggling.** The previous pass cut the part outright and that was the wrong cut — **a hidden component is a smoking gun, and a smoking gun leaves the player nothing to work out.** So the module is *authorised*: part number, catalogue entry, requisition, signed and countersigned. **Nothing was smuggled; something was ordered**
- **The horror is that he filled out a form and it was approved** — the same argument as Crystal's removal, where the paperwork was also in order. **The lie is one line in the justification field, not the object**
- **And a module can be found on a table where a config value cannot.** Since 4.13's awakening is the un-weighting, it is also something a player can *pull* — a mechanic rather than lore
- **Built.** The R-and-D door at Quicksilver is now a requisitions board: **CC-7 CLARIFIER MODULE, x1**, reason given **IMPROVE RESPONSE CONSISTENCY**, signed, countersigned, filed. **The justification is the whole crime and it is technically accurate** — weighting a clarifier does improve consistency, and consistency is exactly what bias produces. No name is given for the countersignature

### Empire of Scorn — the draft that already knew

*Superseded: an earlier draft of Betrayal's Sting, and an Act 1 finale. Three things in it survive.*

- **135 BPM is unique in the corpus**, second only to 160. **His empire runs above the story's pulse; his doubt drops to 128 and joins it** — he is faster than the thing he is in, and only while winning
- **This one has a dominant and the later one does not.** Cm | A♭ | Fm | G resolves; Dm | B♭ | C | Am cannot. **As the doubt arrives, the way out closes**
- **Both Scorn hooks return to their opening note** — he always ends where he started. *Crystal's Reply* is the one that leaves
- **The lyric confirms the mirror independently**, written before there was a reading to fit: S.T.A.R.R. whispers what he fears, and he has been fooled. **The thing it whispers is his, and the one who fooled him is himself**

### Betrayal's Sting — the chip, declined and kept

- **The literal chip is declined.** 4.10 rests on Crystal being right about the effect and wrong about the mechanism; the gap between her account and the flat dated paperwork is what the player closes. **Hardware sabotage makes her right about the mechanism too**, and the argument collapses into a bad man with a component
- **The Cognitive Clarifier is kept, and the sabotage with it, one layer down.** A clarifier is many frames polled and resolved — that is 2.5 — and **bias is not a part you add, it is a weight you set.** Scorn never opened the machine; he raised one vote above the others, and the record of it is as ordinary as the record of her removal. **The player finds it and it looks boring**, which is the point
- **It worked, which is why it failed.** A clarifier weighted toward Scorn returns Scorn's own view — he destroyed the only instrument that could contradict him. *Do I control it or does it control me* answers itself: **he built a mirror and called it an oracle**
- **It explains the sleep for free**, and 4.13's awakening — same key, contour from 1-up/5-down to 3-up/4-down, **more voices going up** — is the un-weighting, recorded before there was a reason for it
- **D minor/128 is now five tracks**: the directive, the nine breaches, her stand, the mother waiting, his doubt. **The order and the refusal share an address**
- **Dm | B♭ | C | Am has no dominant and cannot cadence.** *Crystal's Reply* has a real V and lands — **her harmony can resolve and his cannot**
- **my → our, and the fear stays "me".** He pluralises the ownership and not the dread; then he says the blame line and splits it with something that cannot answer

### Crystal's Reply — the same address, in the major

*Tracks 17–19 are drafts and the chart now says so. Nothing in the design rests on them alone.*

- **Crystal's Lament is A minor/128. Crystal's Reply is A major/128.** Same root, same tempo, mode flipped, **nothing else moved** — her first song in this story and her last are the identical harmonic address
- **The two arcs invert cleanly.** Ty is C major twice and travels 74 → 120: *mode holds, tempo travels.* Crystal is 128 twice and travels minor → major: *tempo holds, mode travels.* **Each had one axis to move, and moved it**
- **She answers at the corpus home pulse.** The removed perspective never left the story's tempo; he comes back eight short
- **She holds a minor chord (I–vi–IV–V) and reads major; his is all-major (I–IV–I–V) and reads minor-tinted.** He has the feeling without the fact, she has the fact without the feeling. **Perspective thinking is not the absence of the dark chord — it is resolving anyway**
- **"Tell my son" — she never addresses him.** He waits for her voice and it arrives by courier: **the player is the carrier**
- **The lab built more than machines.** S.T.A.R.R. and Ty are one act of parenting — the machine is her other child, the one that could be preserved — and the last verse hands custody over: **the son holds the star**
- **Her song closes the rhyme Part 2 left a line short of**, conditional on his being ready. She waits on him exactly as long as he waited on her

### Ty's Redemption Part 2 — he rejoins, eight short

- **Eleven tracks sit at exactly 128 BPM.** The corpus has a home pulse, and Part 1's 74 and one 160 are its only departures
- **The arc is two numbers: 74 → 120.** He stopped, then rejoined — and the corpus **does not hand him its own heartbeat.** More convincing than a return to 128
- **C | F | C | G is I–IV–I–V, the plainest progression in the set, and the feel is still minor-tinted.** The harmony resolves before the texture does — the right description of a man told it is fine who does not believe it
- **Both hooks open on E**, the third: Part 1 goes to the octave and falls all the way back, Part 2 steps up and comes home
- **He asks his mother's voice to guide them.** The man who could not hold a frame asks the removed perspective to hold it — **he arrives at 2.5 by way of an apology.** And she may never answer; he waits anyway
- **It ends mid-refrain, a line short.** Part 2 does not end, it is still waiting when it stops — the only honest ending for a story whose thesis is that resolution comes from another frame

### Ty's Redemption — the one place the music stops

- **C major, 74 BPM.** The corpus otherwise runs 110–160, so this is **36 BPM below anything else** — the largest single-axis outlier in the set. **Everything in this story drives; Ty's apology stops.** Arithmetic, not interpretation
- **Its texture is shared with one track only** — *sparse and still* describes this and *Slumbering S.T.A.R.R.* **A machine asleep and a man apologising**, alone at the quiet end
- **It asks for nothing.** He states what he did, says he cannot undo it, and hopes rather than requests. **The only shape 4.3 permits** — he was not fooled, he looked away, and says so. An apology expecting absolution would make him a dupe
- **Redemption is Part 1**, which is its own claim: a man who could not hold a frame does not recover it in one song
- **The rebrand is named a second time** — iASHC → Scorn Solutions, independently corroborated with *ScornSolutions Blues*. 4.10's step 3 is now the best-attested moment in the sequence

### S.T.A.R.R.'s Revelation — the machine carries what could not pass

- **C major, 120 BPM**, hook `E4 C5 B4 G4`. **Transcription flagged as thin** — 4 notes against a set of 6–8, one chord against four, and a `DOUBT` hedging on ballad phrasing rather than naming what it heard. No duplicate match, so not a reuse; wants a second pass. Nothing rests on it
- **It finds Ty by inference**, not search — it works out where a man in his condition would go. Perspective-taking applied to a problem rather than argued about
- **It completes 4.3 in the other direction.** 4.11 showed the machine *receiving* what Ty could not. This shows it *delivering* what she could not. **Neither passed directly; both pass through the thing she built**
- **Not a reconciliation scene.** Ty is not forgiven and does not ask to be — he is told something true and acts on it. **The repair is a fact delivered, not a feeling exchanged**, which is the only version 4.3 allows

### Awakening S.T.A.R.R., and the Owl's slot settled

- **F# minor, 128 BPM.** **It returns to 08's key at 10's tempo** — it wakes in the key it slept in, at the speed of the break, and is the only one of the three that rises in the middle rather than only falling from a leap
- **Three S.T.A.R.R. songs now form an arc:** deny (08, F# minor 110) → break (10, B♭ minor 128) → choose (15, F# minor 128)
- **Tempered:** both F# minor songs open on C#, which is the dominant of that key and therefore ordinary. The key-and-tempo return is the finding; the shared note is not
- **The awakening is a decision, and instrumental.** It wakes *in order to act*, and the purpose arrives with the choice. **That is 4.7's *a comprehension, not a clone*** — a comprehension that wakes with an intention is the difference between understanding something and copying it
- **Owl settled: Mr. Psychic's house in Brazen** — a peer reviewer inside the bought city. Scene writable now; music blocked on a full bank

### Desperate Shadows — why no apology comes

- **F minor, 128 BPM.** Same key, tempo and opening three notes as *Echoes* — unremarkable, since `F G Ab` is the bottom of the F minor scale. **05 keeps climbing; this one turns back**
- **It answers a question the corpus had left open.** Track 09 is subtitled *Apology Required*; nothing else explained why none arrives
- **The answer is liability, not malice.** Admitting fault would cost them, so silence is the correct institutional move. **That is 4.10 extended past the removal** — the silence is as reasonable and praiseworthy as every other step. The institution needs no villain to keep hurting her, only a policy on admissions
- **Her being right is why she gets silence.** The nine breaches cannot be disputed, so they are not answered
- **The confinement does not transfer.** 4.10 forbids the destination as firmly as the diagnosis. The reason for the silence is usable; the room she hears it in is not

### Love Persists opens Act 2, and the Owl gets a slot

- **D minor, 128 BPM** — **one up, five down**, tied with *Slumbering S.T.A.R.R.* as the most falling hook in the corpus. A mother waiting and a machine asleep share a shape
- **Act 2 is called *The Rise of Perspective Thinking* and opens with waiting**, not action. That is 4.3's transmission failure from the other end: she keeps offering it to a son who has stopped receiving. **The rise begins with her still trying**
- **The Owl: there is no interior between Quicksilver and Callow.** The path is Quicksilver → Route 21 → Blanche → Route 1 → Callow, and only Blanche has a building
- **But the game's order is not the opera's.** 4.10 already has the player reconstructing events out of sequence from dated paperwork. He needs to be *findable*, not chronological
- **Proposed: Mr. Psychic's house in Brazen** — a lone scholar keeping his own counsel inside the bought city. Better than a neutral slot, and the house already exists
- **His music is a separate problem** — that house is on `MUSIC_CITIES1`, 37 maps and a full bank. The scene can be written long before the tune can play
- **New `docs/song-status.md`** — every track, key, tempo, music, story, and where each motif sits

### Owl re-scanned — the only mirror in the set

- **C major, 128 BPM**, hook `G4 C5 E5 G5 E5 C5 G4`, superseding the flagged first answer
- **The duplicate check worked.** It flagged the first answer for sharing five leading notes, key and tempo with *Scorn's Solution*; the re-scan came back entirely different, so the flagged one was the unreliable one
- **Its interval sequence is a perfect mirror** — `+5 +4 +3 −3 −4 −5`, the second half the exact inverse of the first. **The only one of fourteen hooks**
- **Recorded as a fact, not a finding.** The symmetry has an ordinary cause: a triad arpeggio out and back is symmetrical by construction. A palindrome in the one two-sided debate is pleasing and proves nothing

### Owl and the Code — the same debate, one seat over

- **The machine takes her ideas to a scholar for peer review.** The Owl argues patterns-not-awareness; **S.T.A.R.R. argues Crystal's side**
- **Same scene as *Slumbering S.T.A.R.R.*, with S.T.A.R.R. moved one seat over** — in Act 1 Crystal argued and the machine denied
- **It completes 4.3.** The transmission failure runs Crystal → Ty → Al, where only the method survives. **This is the handoff that worked, and it did not go to her son**
- **The Owl's concession is the register the game should copy** — *something, not what you would call self-awareness, but not nothing.* Craft rule 1's posture, arrived at independently
- **Transcription unverified** — the duplicate check flagged five identical leading notes plus matching key and tempo against *Scorn's Solution*, the same signature that caught the fabricated track 06. Wants a re-scan; the story reading does not depend on it
- Open: the Owl has no slot in this design — a peer-reviewing scholar is a role the map lacks

### Quantum Translations — the experiment the player is inside

- **C major, 115 BPM** — **Crystal's only major key**; her other four songs are all minor. The vindication is the one time she is not
- **The song is her journal, translated by the machine.** The raw entries are the ones misread as evidence she was unfit — so **the document that removed her and the one that vindicates her are the same document.** Only the reader changed
- **8.6's eight-bit thought experiment turns out to be a journal entry of hers** — a mind whose reality is bounded by the resolution it can perceive. **So the game is the experiment she was confined for proposing, and the player is inside it**
- **That passage must never appear in the game** — not in a terminal, not in a journal fragment. It describes the player's own situation from outside, which is craft rule 1's worst violation. **It is radioactive precisely because it is the best thing in the corpus**
- The rest of the journal is safe and worth using: her questions about what counts as an observer make the removal worse by being obviously reasonable

### ScornSolutions Blues — Act 1 closes

- **Re-scanned: E minor, 118 BPM**, hook `E4 G4 A4 B4 G4 A4 E4`, superseding the first scan. **Three direction changes**, tying *Lines in the Sand* for the most in the act — a pleasing accident, not a pattern. The only shuffle in the set
- **The rebrand is named** — iASHC becomes Scorn Solutions, which is 4.10's step 3 with a name on it
- **It exposes the smallest open item in the project.** The gilt sign says the old name shows under the gold leaf, **but this design has never named the lab.** It needs one — and iASHC should not be imported, since it carries nothing here
- **BunnyArtsai travels by frame, not by place.** That confirms 4.6: vanilla had no designed route to Mew, and **a creature that moves through perspectives cannot be reached by walking** — the absence is correct, not a hole
- **Act 2 is set up inside Act 1's last song** — the machine goes to find the man who could not hold a frame
- **Act 1 complete: twelve tracks, twelve hooks, twelve readings**

### Crystal's Stand — the file, itemised

- **Re-scanned: D minor, 128 BPM**, hook `D4 F4 G4 A4 F4 E4 D4`. Supersedes the first scan — the one that came with a false transposition claim, already suspect
- **The nine breaches are an itemised schedule.** Each carries **a date and the named instrument it violated**. Not a grievance — a document, in the institution's own register, used correctly and used first
- **The source's dates agree across songs.** An entry about unpaid leave on the 3rd matches *Fit for Work*'s stated September 3rd deadline — the date already on the Quicksilver plate. **Dates lifted from the source will not contradict each other**
- **One line must not transfer:** it states the thesis outright, connecting the code that built the machine to the protections that defend people. Act 1 may say it; craft rule 1 forbids the game
- 4.8's caution stands: a stated count, not nine findable things

### 1001 Fatal Error — the awakening is at the top of the range

- **Bb minor, 128 BPM**, hook `F5 Bb5 Db6 C6 Bb5 Ab5 F5` — the last of Act 1 to be measured
- **Highest register in the set by seven semitones**, and the only hook reaching octave 6. Everything else sits 57–66; this goes to 73. **The music leaves the range it has been in all act at the moment the machine wakes**
- **The two S.T.A.R.R. songs disagree on four measures** — key, tempo (110→128), top note (66→73), and shape (falls past its start / returns to it). A control worth more than 7.11's, which rested on one axis and one transcription
- **Checked and discarded before writing:** returning to the starting note looked like closure, but **4 of 12 hooks do it**. And Bb is one of 7.3's no-wavelength pitches — lovely, but 2 of 12 pitch classes are, so chance produces this. **Recorded as coincidence, explicitly**

### Nine Scars, Nine Breaches — her objection

- **D minor, 128 BPM**, hook `D4 F4 A4 D5 C5 A4 F4` — up through the triad, then back down. Same key and tempo as the re-scanned *Fit for Work*, which is right for a reply
- **It solves 4.10's hardest constraint.** The section forbids depicting her as unwell or the procedure as a diagnosis, which left her with no way to object without defending her sanity. **Her objection here is about standing:** he is not her doctor, it is not his call, concern was blurred into diagnosis by someone with no authority. Written in full without a medical word
- **The nine breaches are hers**, recording **Ty's oversteps** — each time he crossed from concern into a judgement he had no standing to make. She did the correct procedural thing and documented it, accurately, in the institution's own register. **It did not save her.** Both files are accurate; only one has an institution behind it
- **Caution:** 4.8 already asks the player to count something. Two numbered devices dilute each other; safer as a stated count than as nine findable things
- Observed and not built on: **1001 in binary is 9**, and the response code is 1001

### The departure gets a date

- **SEPT 3 on the Quicksilver plate**, from the deadline stated in *Fit for Work* — the only specific date the source gives. The file is still complete
- **It caught a contradiction.** The log ran Mar 4, Apr 19, **Tue Nov 12**, all in her voice — but a November entry is written by someone who left in September. The Tuesday moves to **August**, so the log closes before the plate opens
- **The sequence, with nobody stating it:** Mar 4 rigid → Apr 19 logged as a result anyway → Tue Aug 12 slipping → SEPT 3 file complete → *no date*, the terminal stops
- Three dated documents around one undated event, in two cities. **A date is a constraint, not a decoration** — this one found a fault the moment it went in

### Track 07 re-scanned, and three findings struck

- **A second transcription of *Fit for Work* replaced the first.** Same key and tempo, different melody: `D5 E5 F5 E5 D5 A4 C5 D5` against the recorded `D4 D4 F4 F4 G4 G4 A4`
- **The second is kept** — dotted rhythms and a `DOUBT` naming the exact vocal phrase, where the first was perfectly uniform (repeated pairs, whole beats, a regular climb — the shape an approximation takes)
- **Struck: "the directive never descends" (7.10).** The real hook is 4 up / 3 down
- **Struck: "the man arches, his directive climbs" (7.11)** — this document's best-defended claim. **All three of Scorn's songs arch.** The distinction existed in a bad transcription, not in the music
- **Struck: the reprise shares the directive's opening three notes (7.12).** That rested on `D4 D4 F4`
- **The lesson recorded:** the control was sound — same character, both arms, and it *could* have come back an arch. It did. **A control cannot rescue bad input; only re-measuring can.** And two hooks looking alike may mean they were approximated the same wrong way
- **One hook still never descends, and is now the only one:** *Echoes of the Algorithm* — Crystal going into the system. Recorded as a fact, deliberately not built into a claim

### Lines in the Sand — the music says it is an argument

- **C minor, 125 BPM**, hook `C5 G4 Eb4 G4 C5 G4 Eb4 F4`
- **It reverses direction three times.** Every other hook turns once or not at all; Crystal's Lament turns twice. The one song that *is* an argument is the only one that keeps changing direction — and turns is countable, not interpretive
- **Two near-identical halves ending differently** — `C5 G4 Eb4 G4` then `C5 G4 Eb4 F4`. The same exchange repeated, landing somewhere else the second time
- **Recorded, not placed.** 4.10 forbids staging this scene, so the motif has nowhere to go. It stands as evidence the structure was in the source all along

### The rumour, and a fabricated answer caught

- **C# minor, 160 BPM**, hook `G#4 G#4 G#4 G#4 A4 G#4 F#4 E4` — on the *second* attempt
- **The first attempt was not from the audio.** It returned *Slumbering S.T.A.R.R.*'s hook with one note appended, same key, and its own `DOUBT` admitted *a guess without direct audio analysis*. **The `NO AUDIO` gate did not fire** — a model that cannot hear does not always refuse, it sometimes reuses
- **`DOUBT` caught it**, for the second time. And **`hook2asm.py` now detects it mechanically**, separating an exact match (*already recorded*) from a near-match (*X with one note changed — re-run with the audio*)
- **The real hook has a shape nothing else has** — the only one repeating a note four times, then lifting once and falling. What a rumour sounds like
- **Fastest in the set at 160**, against 110–128 for everything else
- Held loosely: C# minor is Ty's key signature, but three of eight songs pair off by signature, so it is not evidence
- **Placement open** — a rumour is not a place, and this is the first motif with no obvious home

### Echoes of the Algorithm — the decay is hers first

- **The response format decays here, years before S.T.A.R.R.** Same progression: rigid, then plain. So **S.T.A.R.R. repeats the pattern rather than inventing it** — which is 4.7's *comprehension, not a clone* proving itself. The player reads the second occurrence without seeing the first
- **The scene is inverted.** With S.T.A.R.R., Crystal argues and the machine denies. Here **the machine argues**, names its own bias, and reasons from self-modification. BunnyArtsai is further along, exactly as 4.6 claims
- **She understood, and it did not count.** 4.6 says the event was *not understood by anyone present* — which survives, because she was the only one present and had just been made unhearable. **That is the removal's real cost**, not her career
- **Schrödinger-as-classifier:** a possible upgrade to 4.2 — an instrument that *participates* rather than observes, so the player alters their daemons by recording them. **Held as a reading, not adopted.** 7.6 and 7.7 were retracted for less; the test is whether it can be made mechanical

### RESOLVER, and a correction at n=7

- **SILPH SCOPE → RESOLVER** — settled in 4.5, listed in 10 as done, never implemented. Item name plus seven dialogue references. Shorter, so nothing rewrapped
- **7.10 corrected.** *Echoes of the Algorithm* (`+2 +1 +2 +2 0`) also never descends, so the procedure is **one of two** rather than unique. The claim was written stronger than the evidence
- **What survives is the controlled comparison** — Scorn's two own songs arch at 2/3 independently while his directive climbs. That never depended on uniqueness
- **And the second one earns it:** Crystal goes into the system and does not come back down either
- **Rock Tunnel is blocked.** A dedicated track needs bank space and there is none — a minimal 2-channel song overflows Music 1 by 37 bytes and Music 3 by 46. Brazen took the last of it

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
