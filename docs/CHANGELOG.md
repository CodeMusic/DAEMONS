# CHANGELOG

Design-bible versions and what moved in each. `vision.md` is the living document;
the PDFs are snapshots cut with `./docs/build-pdf.sh <version>`.

---

## v11.150 — 2026-09-10

### 4.34's four scenes are in the ROM — T-27, T-28, T-29, T-30

- **T-27, the lab.** ***The silence version.*** *Vanilla walks her up to your door after the Review
  Board and escorts you in; none of it happens.* **You come out of your house after the biggest thing
  you have done and for the first time nobody is waiting, and nothing says so.** Done by leaving one
  scene var at a value the on-frame table has no entry for — ***no script was deleted and two of them
  simply have no way to run.*** **The GLOBAL INDEX is handed over by a man at a desk, on being spoken
  to.**
- ***The note is the object everything downstream re-reads***, so it is one string and it never
  changes. **"In a careful hand" is the whole tell and nothing points at it** — *a woman taken out of
  a building does not leave a tidy note.* The clause that only parses if she knew is **"does not need
  me in the room to continue"**, which reads as ordinary modesty the first time. *The aide has read it
  and got nothing out of it: "I read it. It is about the entries."*
- **The 60-species gate went with the escort, deliberately.** *An aide saying "you have not earned it
  yet" reinstates assessment at the exact moment 8.2a's tone rule removes it.* ***It is now the first
  thing in the game given to you without a test.***
- **T-28, the Owl.** ***The player only ever hears one side*** — not economy, but the safest way to
  write it: **the machine's argument never has to be written down, so it can never say the thesis.**
  *That is also 4.24's own structure with Act 1 inverted.* **He is not a fool and he is not beaten:**
  the turn is him noticing that his own objection applies to him. ***The concession refuses the word
  twice before making it.*** *Gate is a new `DaemonsPartyHasStarr` special — party, not caught,
  because 4.34 says you **bring** the machine.*
- **T-29, `THE ANNEX`.** ***The only one of the twenty-two island names not said by a person who
  arrived*** — **nobody arrives there, so the name came off a form**, and *an annex is a building
  attached to a bigger one, for what will not fit in it.* **The last scene moves there from the lab**,
  which is the one thing 8.2a got wrong. *She does not ask how you got here.* **Deoxys is turned off:
  a legendary ten tiles from the ending would be absurd.**
- **T-30, the gold.** ***The inversion is done by order and nothing else*** — the buried name is what
  you read first now and the gold one is last, and **no line remarks on it.** *4.4 calls the leaf "not
  a gesture, a fact with a date", so repainting it would be a gesture.* **Nobody touches the sign. It
  stops holding.**

### engine.md gains traps 11 and 12, both from T-29 and neither from the scene

- ***A mapsec rename half-applied.*** **`region_map_entry_strings.h` held the OLD symbol carrying the
  NEW string** while the entries header, *from the same JSON on the same run*, used the new one —
  undeclared symbol at compile. **Deleting both generated headers produced the matching pair**, and
  `port_sevii.py` now removes them on every write. ***Why one regenerated and the other did not has
  not been established***, which is the reason to delete rather than reason about it.
- ***A map directory is not a build input.*** **`BirthIsland_Exterior` had no `text.inc` at all** — an
  event island nobody could reach, so nobody had ever written a line for it — *and a new one has to be
  listed in `event_scripts.s` by hand.*

---

## v11.149 — 2026-09-10

### 4.34 — the Act 2 ending, and the release is a re-reading

- ***8.2a had the package and did not have the beat before it***, which is why 4.14 was designed and
  never staged and why the last scene had nowhere to be. **Every clause of 8.2a's ending survives;
  what moves is where she is standing when she reads it.**
- ***The correction that started it was already written down.*** **The fitness-for-work was Ty's** —
  8.2a says so in one line — *and it had been read here as Scorn's, which would have been a much worse
  story.* **His crime is a position in the middle of a record; a man who locks a woman in a building is
  a smaller character.** ***And it sets the rule: a procedure put her there, so a procedure takes her
  out. Nobody breaks a door.***
- ***The mechanism was in 4.24 the whole time*** — **"the document that removed her and the document
  that vindicates her are the same document. Only the reader changed."** *Her journals were read as
  evidence she had lost rigour; the machine reads the same pages and understands them.* **Nobody had
  noticed the vindication was also the release.** ***The climax of this game is an argument won by
  re-reading***, which is the ending a project about a type chart being an argument was already shaped
  for.
- **4.14 now happens before Act 2 starts and the player never sees it.** *S.T.A.R.R. woke when she was
  taken — 4.10's `CRYSTAL NOT FOUND` — went looking for Ty, and then they separated: he to the island,
  it to Doldrum Cave.* ***So Ty hands a stranger something for his mother because the machine already
  got to him***, and the player meets a cause as a man's behaviour.
- **Four rulings, so the writing has something to fail against:** the Owl's concession is ***dialogue
  only*** and concedes *something* it will not name; **he stays in Brazen**, because a remote scholar
  is a neutral one and 4.23 put him inside the bought city on purpose; ***the note never changes***, one
  string, or the game performs 4.24's re-reading for the player; and **the sign is not repainted** —
  *the gold simply is not holding.*
- **T-27 to T-30 opened.** *One of them makes a dead map reachable and flips 2.10 for exactly that map.*

### 4.7 — two sections had been read as disagreeing and never were

- ***`CLEAR LABORATORY` is the lab on Quicksilver Island***, which 4.4 has said since 2026-08-31. **So
  4.7's "born on Quicksilver Island" and 4.24's "the machine she built" are one fact said twice**, and
  the reading that Quicksilver built it independently of her was wrong. *Stated in 4.7 now, because it
  had never been written anywhere and cost a conversation.*
- **The building Scorn renamed is the building S.T.A.R.R. was made in.** *Which is why the sign is worth
  finding.*

---

## v11.148 — 2026-09-10

### T-23 — the island names, and the reading that halved the job

- ***The ticket said "35 places" and the reading said three kinds of place.*** **Counting them was most
  of the work:**
  - **A place that carries its island's number is a place nobody named** — `THREE ISLE PORT`,
    `FIVE ISLE MEADOW`, `SEVII ISLE 6`–`24`. ***That is 8.2a's grace note itself***, so they keep the
    number.
  - **`TANOBY` and the seven chambers are transliterations of an alphabet 4.24 says nobody reads.**
    *Renaming them would be translating the one thing whose whole point is that you cannot.*
  - **2.10 leaves `NAVEL ROCK` and `BIRTH ISLAND`** — no player of this game reaches either.
- **Which left twenty-one**, and a register that is not island-flavoured Kanto: ***Kanto's names are
  tones and institutions; the islands' names are what one person called a place once, and it stuck.***
  `MT. SMOULDER` · `FINDERS BEACH` · `THE OVERLOOK` · `SOMEONE'S STONE` · `THE WRONG WAY` ·
  `WHAT REMAINS` · `NOBODY'S ISLE` · `THE WAY IN`.
- ***`tools/port_sevii.py` owns the table***, which is the point of it: **overruling any one name is
  one edit and a re-run**, and the JSON, the C symbols and the dialogue all follow.
- **It caught both things this was going to break.** ***Seven hand-written `sMapsecName_*` symbols in
  `region_map.c`*** — the trap that broke the build three times during the species sweep, and the one
  the tool was written around. **And one swept line pushed past the 196px box** because `STILLFALL` is
  two characters longer than `ICEFALL`.
- ***Two caps, neither declared anywhere in the engine, both read out of the code:*** **18 characters**
  from `u8 mapName[19]`, and **112 pixels** from the name popup centring with `(maxWidth - width) / 2`
  on ***unsigned*** values — *wider than that underflows a u32 and the popup draws the name off the
  window instead of clipping it.* **All twenty-one fit inside vanilla's own widest, 96px.**
- **Tier 3 is now 3a (done) and 3b (T-26, the ~9,500 words).** *The names were the cheap half and
  saying so is the honest version.*

### The debug kit is already told about the STREAM

- ***Granting all eight MARKS in one frame unlocks nine shows in one frame***, and T-12's per-step hook
  then announced them **one at a time, eight message boxes into a new debug save.** *The hook was
  right; the save was not.*
- **Fixed in the kit rather than the hook.** ***Gating the notification on `DAEMONS_DEBUG` would have
  made the debug build the one build where the notification cannot be tested*** — and only what is
  **unlocked** is marked told, so anything unlocking later in a debug save still announces itself once.

---

## v11.147 — 2026-09-10

### T-09 — the two KNOWN FAULT cards, and the case nobody had labelled

- ***The ticket said the only thing left was choosing a display case, and that the choice was a
  reading of the room rather than a fact about it.*** **It turned out to be a fact about it.** *Every
  blocked block on that floor already carried a `bg_event` except one* — **so the room had been
  telling anyone who counted which case was empty**, and `tools/gbamaptiles.py` gave the approach
  tiles out of the layout's own `map.bin`.
- **The case takes two cards and they are read from opposite sides**, which is better than one wall
  with both: *one is met coming in and one going out.*
- **`DISPLAY UNIT`** — *the harder an operator worked at a thing on it, the less of a thing it drew.*
  From `lineage.md` 3b's door, **which stopped being a door under pressure and went back to dots and
  lines, which is all it had ever been.**
- **`SORTING FRAME`** — *shown a marking it had seen before, it assigned the purpose it had seen
  beside it.* From 3b's Guardian, **called *Hunter* on the evidence of a plaid shirt.** ***The last
  line is the card:*** *it was right often enough that nobody checked the markings.*
- **Both obey 4.32's format and neither names a distortion**, per craft rule 1 — *the DISPLAY UNIT's
  fault is a drawing fault and the SORTING FRAME's is a filing fault, and both are the machine's.*
- ***The words were right on the first pass and the line breaks were not.*** **Three of the nine
  lines ran past the 196px box by three to six pixels** — *re-broken, not rewritten*, and the check
  that caught it is `engine.md`'s own number rather than a guess about how wide a box is.

### A merge conflict had been committed into this file

- ***`docs/CHANGELOG.md` carried `<<<<<<< HEAD`, `=======` and `>>>>>>> main` in the tree*** — a
  merge resolved by committing the markers, unnoticed because **both sides were pure appends and the
  file still read correctly to a human**: v11.146 down to v11.137 above the seam, v11.136 below it,
  and v11.135 after that. *Already in the right order.*
- **The resolution was to delete three lines.** ***The lesson is the one the rest of this project
  keeps relearning:*** a diff showed nothing wrong because each side's text was fine; **it took
  something reading the whole file to find the three lines that belonged to neither.**

---

## v11.146 — 2026-09-10

### 8.2a's tiers 1 and 2 are done, which is a finding rather than a milestone

- ***The deferral said "not until the rest is in play", and the rest is in play.*** **Act 2's six
  scenes are in the ROM, both gems are named, the machine points at DOLDRUM, and the doctrine has a
  room.**
- **Which makes tier 3 the largest single job left in the project and the one 8 was written about.**
  *35 place names and ~9,500 words is not a naming pass; it is a rewrite of a quarter of the game's
  map dialogue to a tone rule.* ***The honest reading of "the condition is met" is that the brake came
  off, not that the work got smaller.***

### And TODO caught up with what actually shipped

- **T-09 moves to Ready.** *It had been blocked on "needs knowing which tiles are display cases" and
  `gbamaptiles.py` answers that* — **what is left is choosing which case, which is a reading of the
  room rather than a fact about it.**
- **T-23 moves to Ready** with its condition marked met, and marked as the file's largest job.
- ***The doctrine's open question is half-settled.*** Placement went in with T-22; **his name and the
  doctrine's name were left off on purpose, and that may be the answer** — *naming the doctrine gives
  the game a thing to hold, and 4.33's whole rule is that it holds nothing.*

---

## v11.145 — 2026-09-10

### SILPH is the FOUNDRY, and the bible had been citing the wrong decomp

- ***The opening line said `pokered` and has since 1.0.*** **9.3 records the day the project pivoted to
  `pokefirered` and the line never moved with it.** *Corrected, with the pivot named rather than erased.*
- **`SILPH` → `FOUNDRY`.** *SILPH is vanilla's silicon pun — sylph, silicon — and a **foundry is where
  silicon is actually made**, so the joke survives being translated.* It is also a real place that
  casts metal, which is 1's double-duty test, and **a company that makes the BOXES and the RESOLVER
  should be named for what it fabricates.** 35 lines, two item descriptions, the quest log, the sign
  and the region map.
- ***The mapsec was edited by hand***, because `region_map_sections.json` is in `NEVER_SWEEP` — place
  names are authored. **Checked first that `sMapsecName_SILPH_CO` is not one of the twenty mapsec
  symbols `region_map.c` names by hand.** It is not.

### The gap at the end of Act 2

- ***8.2a's spine ends "machine completes, DOLDRUM CAVE opens — S.T.A.R.R.", and nothing said so.***
  The flag that removes the cave guard is set four lines into Celio's scene: **the player finished an
  errand about gemstones and the world quietly changed in a city five islands away.**
- **So Celio reads his own log and does not understand it.** *Two ends, one handshake, exactly as
  designed — and a third thing on the line he did not put there, which by the log has been listening a
  very long time and is not on any of these islands.* **It gives one word. DOLDRUM.**
- *4.14 has the machine work out where a man in his condition would go, and go there.* **This is the
  same move run backwards, by the player.**

### Four items that fell between 1.6 and 1.6d

- **`COLD START` · `RESTART ALL` · `FIELD PATCH` · `WORKAROUND`** — *medicine in vanilla's reading and
  operations in ours.* **The line 1.6 already drew decides them**: HEAL POWDER is HOTFIX, so the bitter
  powder and the bitter root are the same joke at two sizes. ***A workaround is not the fix; it is the
  thing you do instead of the fix, and it works.***
- **The drinks stay drinks.** *Nobody buys a bitter medicinal root for pleasure and everybody buys a
  LEMONADE*, which is the whole of the distinction 2.8 has been making all week.
- ***And `PAYLOAD` was already a species.*** `check_lexicon` refused it — **PARAS is PAYLOAD**, which is
  the better home for the word: *a thing that carries something else and did not choose to.* The
  package is **`ENVELOPE`**. **Worth recording how close it came: the check reported it on the run that
  introduced it, and the output had been piped through `tail -3`.** *The tool was right and the reader
  was lazy.*

---

## v11.144 — 2026-09-10

### Act 2 is in the ROM

- **T-19 — the Warehouse, both ends.** *The package exists:* **`PAYLOAD`, out of `ITEM_LETTER`** — a
  Hoenn key item nothing in this game referenced, and already a letter. 8.2a is exact that what is in
  it *"is not written here and may never need to be"*, so the name says the shape and nothing else.
- ***Both men are in the room and Scorn is facing him.*** They worked the same operation from opposite
  ends and were never in a room; now they are, and nothing happens. **Ty is rewritten to 8.2a's
  reading** — strip the cackle and the argument underneath is a businessman's — *and he crosses the
  room to you, because that is what a man stating terms does.*
- **Scorn gets 8.2a's one beat, and it is not new dialogue**: it is him hearing the sentence he already
  said at Callow. *"It is a correct sentence. I have checked it four times. I cannot tell you why I
  keep checking it."* **He has noticed and he has not understood**, and nothing in the room explains it.
- ***The last scene.*** Crystal turns the package over once and does not open it. She asks one word.
  She crosses the room and opens it facing away — **and the script ends with her still facing away.**
  *Craft rule 1's hardest case so far: the loudest available last line is whatever is on that paper.*
- **T-21 — seven chambers, seven accounts of one event, and the event is never named.** *I SIGNED WHAT
  I WAS GIVEN. I WROTE DOWN WHAT I SAW. I CARRIED IT, I DID NOT READ IT. …NOBODY ASKED ME. IT IS STILL
  HERE.* **Nobody in them is lying and nobody is wrong, and it happened anyway.**
- **T-22 — the doctrine's room.** *4.33's eight steps, on SIX ISLAND's GREEN PATH, one per visit, and
  the ninth clears the flags so he begins again.* ***Every prohibition is an absence***, so the script
  carries the list of what is deliberately not there. **Delete him and nothing else changes.**

### And T-02 — the central argument fights with its own routines

- ***All nineteen of the MUSAI branch's damaging routines were off-type.*** **CODEMUSAI is LOGIC and
  fought by heat; CAREMUSAI is CONTEXT and fought by water; SEEKMUSAI is VECTOR and fought by
  electricity.** *Now 37%, under 2.7's 45% baseline, with two deliberate residuals a line.*
- **`FALSIFY` on CODEMUSAI is the pass.** *It breaks STEELMAN and PARAPHRASE, and CODEMUSAI exists to
  be LOGIC against CONTEXT* — **so 2.2's thesis relation arrives as a routine used on the sibling.**
- ***S.T.A.R.R. was already at 25%***: the ticket's 78% was the thirteen's average carried onto a name
  that did not deserve it.

### Two tools, and one of engine.md's traps caught its author

- **`tools/gbamaptiles.py`** reads a map's collision out of its own `map.bin` — *two bits per tile* —
  so where an NPC can stand or a sign can hang is a lookup rather than a playtest. **T-09 had been
  blocked on that exact sentence.**
- **`tools/port_musai.py`** refuses to write if a level loses its move, which is 2.7a's first rule
  checked rather than trusted.
- ***And `LOCALID_WAREHOUSE_GIDEON` went into a generated header.*** **`map_event_ids.h` is built from
  the map JSONs and gitignored**, so the edit survived exactly one build before the linker asked where
  the symbol had gone. *engine.md trap 4, on the person who wrote it down.*

---

## v11.143 — 2026-09-10

### Two more tickets, and two traps that were mine

- **T-25 — the `FIGHTING DOJO` is the `PROOF HALL`.** *The one BUILDING carrying a vanilla type word,
  and it is the rival gym, so it was the one place the old chart vocabulary sat on a signpost.* **A
  dojo is where a discipline is practised and a PROOF is what LOGIC produces**, and the class inside
  has been FORMALIST since 1.6a — *the room and its people finally agree.*
- **T-08 — `DAEMON` is not its own plural.** POKéMON is, like sheep; **DAEMON is an ordinary English
  noun**, so every line vanilla wrote as *"all sleeping POKéMON"* had been reading as broken English
  since 1.1. ***Twenty-five sentences force the plural and were read one at a time***; the rest are
  genuinely singular, or attributive — *"rare DAEMON fossils" is a compound noun the way "sheep dog" is.*

### engine.md gains traps 8 and 9, both self-inflicted

- ***A substitution that grows every time you run it.*** **`"to get rare DAEMON"` → `"to get rare
  DAEMONS"` matches itself on the next run**, and this project's own instruction is *re-run every tool
  until it reports nothing* — **so a non-idempotent rule is not a warning, it is a corruption engine
  with a crank on it.** *It produced `DAEMONSSSSSSS` in seven files.* **`port_vocab` refuses any pair
  where the key is inside the value now**, rather than warning.
- ***A file that empties itself.*** `open(P,'w').write(open(P).read()...)` **destroys `P`** — Python
  creates the `'w'` handle, which truncates, before the read on the right ever runs. *It had emptied
  `docs/README.md` three times in two days*, quietly, because that file is in no build. **T-06's fix
  to `check_lexicon` is what caught it**: a check that agrees with an absent row agrees with anything.

---

## v11.142 — 2026-09-10

### 1.6d — the rest of the bag, and the half of it that stays vanilla

- ***The ruling that matters is the one about what NOT to touch.*** **Is it used ON A DAEMON, or is it
  a thing a person owns?** *2.8's rule applied to a whole surface at once takes out more than half the
  bag:* the drinks, the treasure, the mail, the bicycle, the tickets, the keys. ***A world where every
  item is a computing pun is 5.3a's world with nobody in it.***
- **Forty-one operations.** The potion ladder is `RECOVER`; MP is a `CHARGE`; the six vitamins are
  **six parts of a machine's spec, one per stat**, which is vanilla's six-nutrients joke in the other
  domain; the X items are `TUNE`. **`ITEMFINDER`, `TOWN MAP` and `VS SEEKER` had been waiting for the
  obvious word: `GREP`, `SITEMAP`, `ROLL CALL`.**
- ***The berries are a TRAP TABLE and the container named itself.*** A berry fires once on a condition
  and is gone, which is a **handler**; the kind installed against a machine condition is a **trap**;
  and a **trap table** is the array of them a system installs. **`CATCH ALL` is the one that takes
  whatever arrives**, `LOW MARK` and `HIGH MARK` are watermarks, and the seven pinch berries are
  **`AUTO`** — *the X items' `TUNE`, firing without you.*
- **`RUBY` and `SAPPHIRE` are `PUBLIC KEY` and `PRIVATE KEY`**, and *the plot decided which*: **Corpus
  steals the SAPPHIRE, and stealing a private key is a crime.**
- ***Two things left alone on 2.10's rule***: the 22 berries with no effect and no way to get one, and
  `src/berry.c`, whose name field holds six characters and whose only readers are content this game
  cannot reach.

### 9.20 — the room that teaches the chart was teaching a different one

- ***A ticket about the word "fight" turned up the whole type chart.*** **`help_system.inc` carries 68
  blocks of it** — every type's matchups in both directions — **and every entry was still in Gen 3's
  names.** *T-04's pass could not see them because they are bare comma lists with no construction, and
  a bare `ROCK` is indistinguishable from a rock.*
- ***And `PSYCHIC` in those lists read `CONSTRUE`***: an earlier sweep had put the MOVE name where the
  TYPE name belonged. **The room whose entire job is explaining the chart was explaining a different
  one, in a vocabulary that was itself half-corrupted.**
- **16 lines re-wrapped at a comma, against a 248px ceiling** — *vanilla's own widest line in this
  exact layout, demonstrated rather than declared.*
- ***Five name bugs this week, all the same shape, and not one found by reading a diff.***

### And eight tickets closed

- **T-04** the type talk · **T-07** the fight read · **T-12** the STREAM notification · **T-13** the
  berries · **T-14** the usable items · **T-15** easy chat · **T-20** the key pair · **T-24** the
  A-to-Z picker, which had been bucketing every word by its *vanilla* spelling.

---

## v11.141 — 2026-09-10

### check_lexicon reads TODO.md's ticket ids

- ***One id, one job*** — the same rule as the lexicon, one level up again. **Two sessions
  issued T-13 through T-17 within the hour**, in a file whose own first rule is that **ids are
  permanent**, and nothing read it back.
- ***A GAP IS A FAULT HERE, and that is where tickets differ from versions.*** **Versions jump
  on purpose** — 1.0 → 11.8 → 11.108 — *so a gap there means nothing.* **TODO.md says a
  finished ticket is struck through and never deleted**, so a missing number means one *was*
  deleted, which is the thing that rule exists to prevent.
- **Verified against both faults**: the real collision reproduced by issuing T-13 twice, and a
  deletion by removing T-05. *Each fires with the reason attached.*
- ***That is the third contract this tool now holds*** — a word that means two things, a
  version that means two releases, and an id that means two jobs. **All three are agreements
  between places with no compiler in between**, which appears to be the shape this project
  produces faults in.

---

## v11.140 — 2026-09-10

### TODO.md caught up, and T-06 closed

- **T-06 is done.** ***`check_lexicon` reported "the version agrees in all four places" while
  testing two of them.*** The README's living row and its snapshot row are two of the four,
  and **an empty file disagrees with nothing** — so the check went quiet at exactly the moment
  the surface it watches had been destroyed. **An absent row is a fault now.** *Verified by
  emptying the file, watching it fail, and restoring.*
- **Five tickets added from the Act 2 work**, which is written into 8.2a and 4.33 and only
  partly in the ROM. **T-13** the Warehouse, both ends — *Scorn and Ty in one room, the
  package handed over, and Crystal reading it*; **T-14** `RUBY` and `SAPPHIRE`, still vanilla
  and still the post-game's two MacGuffins; **T-15** the Tanoby chambers as 4.24's
  translations, *whose vehicle is already built, because Braille is text you cannot read until
  you hold the key*; **T-16** the doctrine's room and its six prohibitions.
- **T-17 is blocked on 8.2a's own condition** — *tier 3 is 35 place names and ~9,500 words,
  and it waits until tiers 1 and 2 are in play.* **That is the same condition the original
  deferral used**, and it is the reason 8 exists.
- **One Open question added**: the doctrine's placement and name. ***Not after a type*** —
  `SWARM` is its own step 5's word.

---

## v11.139 — 2026-09-10

### docs/README.md was emptied, and nothing said so

- **The engine.md commit shows `docs/README.md | 38 ---`** — thirty-eight deletions, no
  insertions, and **the file left at zero lines.** *The commit message does not mention it and
  `engine.md` does not carry what it held.* ***That is the signature of a truncating write,
  not a decision*** — a `open(p, "w")` that never got its content, or a substitution that
  matched the whole file.
- **It is the docs index**: the bible, the current snapshot, the type chart, *The Bag*, the
  lineage. **Restored, and given a row for `engine.md`**, which is a genuinely useful new
  half — *vision.md is engine-independent on purpose, so the hardware had nowhere to live.*
- ***And it had a second cost that would not have shown up for weeks.*** `check_lexicon`'s
  version check reads **the README's living row and its current-snapshot row** as two of the
  four places the version has to agree. **An empty README does not disagree with anything**,
  so the check would have gone on passing while quietly testing two surfaces instead of four.
  *A check that silently stops checking is worse than no check*, and this is the second time
  today that shape has turned up.

---

## v11.138 — 2026-09-10

### 4.33 — the doctrine, as the player meets it

- ***A craft rule that cannot be checked is a wish***, and NEVER ADJUDICATE was stated without
  a way to tell when it had been broken. **The scene**: one NPC in one room, *already talking
  when you walk in and he does not stop for you*, working up through the eight steps. **He
  never asks whether you agree, there is no dialogue choice, and you can leave mid-sentence** —
  *come back and he has continued without you.* **That is the rule as a mechanic: the game is
  not waiting for your assent, because your assent is not part of it.**
- **Six prohibitions, each one a way the game could quietly agree with him.** No NPC refers to
  him — *"that old crank" and "he may be onto something" are both verdicts.* **S.T.A.R.R.
  never comments**, being the one voice a player would take as authoritative. No flag, item or
  Index entry acknowledges him. **No event confirms him and no event embarrasses him** —
  *debunking is adjudicating.*
- ***And he is not in the ERRATA***, which is the easiest of the six to break by accident:
  4.32's cards name thinking distortions, so **a card that happens to match his reasoning is
  the game calling him wrong by filing.**
- ***THE TEST: delete him from the game. Does anything else change?*** **If yes, the game
  adjudicated.**
- **One clarification that inverts what rule 1 usually asks.** *He may state the whole doctrine
  at length and that is not a violation* — **rule 1 withholds THE GAME's last line, and he
  supplies a different one.** ***The danger was never that he talks. It is that something in
  the game agrees with him.***

---

## v11.137 — 2026-09-10

### Reviewing The Painted Mirror, and the citation 4.33 turned out to have

- **Two sessions wrote about the same idea within an hour and neither knew.** 3b's mining of
  the audio drama lists *"matter… it's a process, an ongoing ode"* as **matter as process**;
  4.33 was being written at the same moment and its step 3 is *a rock has moving parts that
  hold it stable.* **The lineage entry filed it under 5.2, which is the eight MARKS** — a
  cross-reference to a section that does not make that claim, written because the section
  that does did not exist yet. **Repointed to 4.33.**
- ***And 4.33's status changes.*** It was written as a character's invention. **It is not
  invented — it is the author's own position from November 2022, handed to a character who
  takes it further than the author would.**
- ***Which makes NEVER ADJUDICATE stricter rather than looser.*** **A game that confirms the
  doctrine is an author agreeing with himself in his own work** — the one thing craft rule 1
  exists to prevent, *and much easier to do by accident when you happen to believe the
  thing.* **The overshoot is what makes him safe to write; the silence is what keeps him
  honest.**
- **Merge housekeeping:** both v11.134 and v11.135 kept, theirs above mine by date; the
  version line resolved to 11.135; **one current snapshot on disk**, per the check.
## v11.136 — 2026-09-10

### docs/engine.md — the hardware, written down

- ***`vision.md` is engine-independent on purpose, so the hardware had nowhere to live*** and was
  accumulating in commit messages. **`engine.md` is that half:** the three memory budgets and which
  one people mean by "storage"; **where a variable actually lands**, which is the single most useful
  fact in it; every fixed width with what we ship in it; and **eight traps listed by symptom**,
  because the symptom is what you will be looking at.
- ***Every number in it is written by `tools/gbabudget.py --write`*** — the memory out of the linker
  map, the name caps out of the **array declarations** rather than the constants beside them (the two
  families disagree), and the pane widths out of **vanilla's own widest line**, which is a
  demonstrated safe width rather than a declared one.
- **All eight name budgets are used to the last character.** *`CONJECTURE` at 10, `THUNDERPUNCH` at 12,
  `REVIEW BOARD` at 12, `LEARNING RATE` at 13.*

### 9.19 — four names the sweep had quietly changed

- ***The tool's first run printed the widest ability name in the game and it was `NO BUSY WAIT`***,
  which nobody wrote. **`OWN TEMPO` was authored `NO THRASH`; renaming the move `THRASH` to
  `BUSY WAIT` rewrote the ability.** *Twelve characters of twelve, so nothing complained.*
- **Three more in the same commit:** `ABSORBS HEAT` became `INGEST HEAT`; Overgrow's description and
  CRYSTAL's starter line both had the **type** `GROWTH` replaced by the move name; and ***the SCHOOL's
  chart lesson read "CORRUPT on SCALE UP"*** — **the one room whose entire job is teaching the chart.**
  *All four repaired.*
- ***The rule was written down and half-enforced, which is worse than not written.*** **`port_vocab`
  has carried *"name tables are authored and prose is swept"* for weeks, and `FIXED` — the thing
  meant to enforce it — was a WIDTH check wearing a name-protection label.** *It refused a rename that
  overflowed and accepted one that fitted. Every one of these four fitted.*
- **A `FIXED` span is now skipped entirely, whatever file it is in** — *protecting the LINE rather than
  the FILE, which is what the rule actually said.* **Trainer classes, trainer names and type names
  joined the list**, all three exposed and none of them noticed.

### And the S.S. ANNE warning only fires when she is still in

- **`ISLANDS` warned about the ship even after she had gone**, which is when the warning is meaningless.
  *A warning that is wrong half the time teaches the reader to skip the box.*

---

## v11.135 — 2026-09-10

### `lineage.md` 3b — *The Painted Mirror*, and the source PENPHIN came from

- **A seven-episode audio drama, ~8,200 words, November–December 2022** — not a blog post, not in the
  original survey, and it sits in the one gap the three sites leave: between the 2021 architecture
  posts and the 2024 rock opera.
- ***It is the origin of PENPHIN and of the Musai branch, and neither had a citation.*** Episode 5:
  **the dolphin is the logical self** — *"vocalized, confident, and accomplished… yet very
  time-focused, mechanical, and sometimes cold"* — and **the penguin is the creative one**, *"quiet,
  organized, spiritual, and feeling."* The trade requirement is in there too: ***"Alone, neither
  mirror image of the self will hear clearly."*** **The design's most load-bearing creature is a
  memoir, and the bible had been quoting it from memory for weeks.**
- **The blogs give perspective thinking as an ethic and as a capability. This gives it as an
  experience** — a man who had put the logical half in charge and did not become himself until the
  other half was let back in.

### Four scenes the blogs do not have

- **THE MISSING KEY SIGNATURE.** Notes wearing flat symbols that are not flat — *"they were just
  misunderstood. You have given them the key."* **2.6's one-clause test for CONTEXT as a puzzle
  rather than a definition**, and the most usable thing in the document.
- **THRASHING, four years early** — *"by allowing my thoughts to loop and recurse without
  consideration of time, I was effectively paralyzing myself."* 2.7 concluded that state is the one
  no type owns; this is it described from inside.
- **A DOOR THAT DE-RENDERS** into *"mere dots and lines"* under pressure — representation collapsing
  when leaned on.
- **THE INVERSION AT THE CENTRE OF SCORN** — *"anchoring the power of love… devolves into a power of
  love… rather, a love of power."* **4.18's crime, written from the inside by someone who caught it
  in time**, which is a register the character does not currently have.

### What is deliberately not mined, and one repair

- **Episode 7's animals are real people and the drama says so** — *"for privacy purposes… in a fabled
  form."* ***They are not creature designs and 3b does not treat them as any.*** The passages quoted
  carry an idea, not a confession, **and that line is drawn on purpose.**
- **`DOLPHIN` and `PENGUIN` cannot be species names** — 8.2b settled the register as technical, and
  **PENPHIN already carries both**, which is the correct amount of this document to have in the table.
- ***`docs/README.md` was zero bytes.*** It was emptied by **b4667618** (v11.131) and nothing noticed
  — 4,415 bytes to nothing, and the file is the index every other doc is found through. **Restored
  from b4c4a7ad** and brought forward to this version.
## v11.134 — 2026-09-10

### 4.33 — the one daemon, recorded before it was lost

- **A doctrine carried in conversation and nowhere else**, written down in full at the
  request of the person holding it. **The world is one daemon; every entity is a sub-process
  of it; material is a sub-process too** — *a rock has moving parts that hold it stable, and
  something is running in there keeping it a rock.* **Every process carries a spark of the
  whole system's awareness — a proto-experience, not a mind.** *Complexity is a swarm and
  never a unit, so every material thing is more a crowd than an individual.*
- **And the elementary things have an inner state.** A particle interacts, the interaction
  changes that state — *an atom becomes charged* — and the changed state changes how it
  interacts next. ***That feedback loop of processes exchanging information is a neural
  network. Not like one.*** **So we are processes of a great daemon, and what we see is what
  a neural network looks like from the inside.**
- **Why it is dangerous rather than merely odd:** ***step 6 is already in the bible at a
  different scale.*** 4.7 says of S.T.A.R.R. that *context determines which content is
  available, and the content you end up holding reshapes the context you are in.* **The
  scientist says the same sentence about an atom.** *It adds no mechanism — it takes the
  game's own mechanism and removes the size requirement.*
- **It is also a claim about the chart**, which is the best kind this project can host:
  STRATUM is *the physical layer everything else runs on*, LATENT is *running below the
  surface, unobserved* — **he says those are one type, and the ground is running.**
- ***THE RULE: he OVERSHOOTS, and the game NEVER ADJUDICATES.*** The game asks what counts as
  a mind; he answers *everything, trivially, all the way down*. **If he is right the question
  the whole game is built on dissolves**, so he is a pressure test rather than a mouthpiece.
  **No character confirms him and none debunks him. No event proves him and none embarrasses
  him.** *The temptation will be one line somewhere that nods — and that line is the moral,
  which the form is defined by withholding.*
- **What it buys: Crystal becomes the moderate.** *A thesis with nobody to its left reads as
  the author's pet.* And the observer question — **a plant, a rock with moving parts, a
  plan** — finally has a room to be asked in.
- **Not the Owl** (4.23 has him arguing the standard position from the bought city) and **not
  a Corpus employee** (0.1's rule 6 is a different joke). <span>OPEN</span>: placement, his
  name, and whether the doctrine has a name. **Not after a type** — `SWARM` is step 5's own
  word and `check_lexicon.py` would catch it.

### 8.2a — reopened, and the islands are Act 2

- **The deferral held for four days and did its job**: the islands are still `ONE ISLAND`
  through `SEVEN ISLAND` while Kanto is Blanche, Callow, Slate and Doldrum. *It was reopened
  for the opposite reason to the one written* — **not because the post-game proved thin, but
  because the opera already contained Act 2 and the game had nowhere to stage it.**
- ***4.14 is a scene that has never been staged.*** **The machine finds Ty** — not by
  searching, *"it works out where a man in his condition would go, and goes there"* — and
  delivers Crystal's message, and it lands. **The open log has been asking whether Ty's
  absence from the endgame reads as a statement or a loose thread. It reads as a thread.**
- **Measured: 136 maps, 2,043 strings, ~9,500 words — 25% of the game's map dialogue**, and
  **121 `DAEMON` against 0 `POKéMON`**, so the vocabulary pass already reached it and only
  the plot is stale. **Zero new gym leaders.** `PHLEGMATIC` is *already* in Icefall Cave.
- **The spine is vanilla's own**: a machine that needs two halves to link two worlds, which
  is the edition split made literal (8.4). **And the islands already gate Doldrum Cave**, so
  ***S.T.A.R.R. is not what you bring to Act 2 — it is what Act 2 is for.***
- **The tone rule, which is the whole reason the islands differ.** *Kanto is where you are
  assessed; the islands are where you are seen from somewhere else.* **The mainland declares,
  instructs and assesses; the islands ask, or offer a second reading.** ***Kanto tells you
  what things are. The islands tell you how they look from where the speaker is standing.***
  — checkable on a single line, which is the only kind of rule that survives 9,500 words.
- **The ending.** Both men are in the warehouse and **Scorn does not recognise him**; they
  worked the same operation from opposite ends and were never in a room. **Ty gives you the
  package and Ty does not come home** — 4.14 is exact that *the repair is a fact delivered,
  not a feeling exchanged*, and a son at the door would undo it. **She reads it. That is the
  last scene.**
- **Tiers 0 and 1 are done. Tier 3 — naming 35 places and rewriting 9,500 words — stays
  deferred on the same condition:** *not until the rest is in play.*

### And four scenes in the ROM

- **Scorn's breakthrough was already in his Callow speech.** He splits the blame with a
  machine and says *"it has never said otherwise"* — 4.18 already logs that as his flaw.
  ***The breakthrough is him hearing the sentence he just said***: one beat, an ellipsis, and
  **"It could not have."** He does not understand it yet.
- **Ty is the scientist at Dotted Hole.** *Strip the cackle and the argument underneath is a
  businessman's.* **He tells you where he is taking it** — which is why you know to go to the
  Warehouse, and why he is still there. *He was not hiding. He was trading.*
- **The staff do not say disbanded.** *"He has CHANGED? People do not change. They get
  promoted."* And on seeing his MARK on a child: ***"…Is it true, what they say? That he
  stopped in the middle of a sentence?"***
- **`TEAM CORPUS` → `CORPUS STAFF`** as the trainer class. *0.1's rule 6 has called them
  employees since the first draft.* `CORPUS EMPLOYEE` is fifteen characters against a
  twelve-character budget; **`CORPUS STAFF` is exactly twelve.**

---

## v11.133 — 2026-09-10

### The ENCOUNTER page, and one berth serving two ships

- ***The S.S. ANNE and the SEVII ferry are the same sailor.*** **`VermilionCity_EventScript_FerrySailor`
  branches on one variable** — below scene 3 he welcomes you aboard the ANNE, at scene 3 he is the
  SEAGALLOP sailor. ***So 9.17's `ISLANDS` entry sails the ANNE***, and the debug kit grants the
  S.S. TICKET specifically so that ship can be boarded. **The confirm box now says so.** *A debug jump
  that refuses to do the thing you asked is worse than one that tells you what it costs.*
- **`RECORD` gets you the GLOBAL INDEX. `ISLANDS` gets you the boat.** ***Neither implies the other***
  — the islands need a ferry that needs CELIO's quest that needs HOLT to have taken you to ONE ISLAND,
  which is main-story and untouched by the HALL OF FAME.
- ***A second submenu, by the same trick as the first.*** **The flag that chose which items
  `SetUpStartMenu` appends became a page number and nothing else changed.**
- **`DAEMON`** prints the species name on the row; **LEFT/RIGHT step by one and repeat when held, L and
  R step by ten.** **`LEVEL`** is the same stepper. **`INVOKE`** starts it — *1.6 spent that word
  already, "you bind() a daemon and you INVOKE it", and this row brings one up.*
- ***The list runs over national dex numbers, not species ids***, so the twenty-five dummy slots are
  not in it and **1..151 is the KANTO INDEX exactly.** **With the GLOBAL INDEX it runs to 387** —
  *one past the end of the complete list*, because 8.9 put MISSINGNO there. ***The only place in the
  game that list is not one short.***

### Two things the build had to be told

- ***A menu row has 48 pixels and the widest of the 412 species names is 60.*** **Sixty-seven would
  have clipped.** *Nine tiles gives 64 and clears every one* — measured across the whole table, and
  applied only while a debug page is open.
- ***An initialised static in `new_menu_helpers.c` does not link*** — the link script discards that
  file's `.data`, and the error names neither the variable nor the reason. **Zero means the vanilla
  width, which is what every other path is already in.**
- **`dowildbattle` stops the script context and hands the resume to the battle's saved callback**, so
  ***it needs a script to come back to*** and a menu callback has none. The daemon is built in C and a
  four-line script does the rest — *the same handover `RECORD` uses, and the same one a signpost uses.*

---

## v11.132 — 2026-09-10

### The GLOBAL INDEX, and two debug entries that leave the menu

- ***The SEVII ISLANDS are gated on four things and only one of them is the REVIEW BOARD.***
  **Islands 1–3 are not gated on it at all** — the ARDOR ferry runs once the S.S. ANNE has sailed
  and CELIO's quest has started. **Islands 4–7 need the upgraded INDEX**, which itself needs
  `FLAG_SYS_GAME_CLEAR`, ***sixty daemons owned***, and ***having been to ONE ISLAND***.
- ***And a debug save fails every clause*** — six daemons, no ferry, and **CRYSTAL CLEAR is not even
  in her own lab**: `FLAG_HIDE_OAK_IN_HIS_LAB` is set at new game and only the starter scene clears it.
- **`RECORD`** warps to the HALL and lets that map's own script do all of it — *the congratulation, the
  name going in, the flag, the respawn, the credits, waking at home.* **Not one line reimplemented.**
- **`ISLANDS`** sets both map flags, both passes, the ARDOR ferry and CELIO's quest to the point the
  RAINBOW PASS is handed over — ***and deliberately no further.*** *Recovering the SAPPHIRE is real
  content, and a debug jump that skips content is a debug jump that stops you testing it.*
- ***`DAEMONS_DEBUG` reached the C preprocessor and not the assembler***, so a script could not be
  fenced the way a function could. **One `--defsym` in `ASFLAGS`**, and `.if DAEMONS_DEBUG == 0` now
  works in any `.inc`. **Checked by grepping the ROMs: the release build carries none of it.**

### NATIONAL → GLOBAL

- ***4.2's INDEX is the LOCAL list; what CRYSTAL upgrades it to is the complete one.*** **A local index
  covers one partition and a global index covers the whole table** — *the distinction exactly, in a
  term of art nobody has to be taught.* **NATIONAL is a word about countries and this world has none.**
  *KANTO stays, because that is a place.*
- **Six literals**, all narrower than what they replaced. *Rejected: `CODEX` (pretty, no double duty),
  `NEXUS` / `MATRIX` / `VERTEX` (sci-fi, and this project's furniture is duller than that), `INDEX-II`
  (a version number on a thing 4.2 wants the player to distrust).*
- ***And the GLOBAL INDEX is still one short.*** **8.9 put MISSINGNO at 387 and the complete list stops
  at 386.** *Nobody says so.*

---

## v11.131 — 2026-09-10

### The held items are a rack, and the Bag became the chart

- ***Forty-seven named, and the register is the one 1.6 and 2.11 both leave open.*** **An item is an
  operation; an ability is a standing property.** *A held item is neither:* **it is a CONFIGURATION —
  a setting attached to a process from outside, in force while it runs, and removable.**
- ***Vanilla's seventeen type boosters are seventeen unrelated trinkets. Ours are one desk.***
  **`<TYPE> GAIN` ×17, `FLOW TRIM` for the small one, `HEADROOM` for the margin, `DITHER` for the
  noise, `MUTE` for the channel you do not want to hear** — *five words from one instrument.* **Each
  gain's first clause is 2.6's own one-line test for that type**, so the Bag now teaches the chart.
- **`RIGOUR` is reversed to `LOGIC GAIN`** and filed with its reasoning. *A rack of eighteen where one
  is a poem is a bug, not a flourish.*
- **The four best of the other twenty-five:** ***DEBUG BUILD*** (instrumented, so it learns faster and
  runs slower), ***LEARNING RATE***, ***SCALING LAW*** (an EMERGENT evolution item — *the argument and
  the mechanic said the same word*), and ***OFF BY ONE***, held by **EDGECASE**.
- ***Five collisions caught by the checker*** — BRUTE FORCE, OVERCOMMIT, OVERVOLT, YIELD and OVERCLOCK
  were all taken. **`BUBBLE` is better than what it replaced:** *a pipeline bubble is a gap where
  nothing issues*, which is a flinch, **and PIPELINE is already a species.**
- **Two broken descriptions repaired on the way past** — a scale that shone *"a HALT pink"* and a spoon
  that boosted *"CONSTRUE-type moves"*. **Both found by rewriting the file rather than reading the diff.**

### And four guards the tools should already have had

- ***`items.json`'s `english` field was both learned from AND swept.*** **MIRACLE SEED became GROWTH
  GAIN and the word pass immediately made it SCALE UP GAIN** on the Game Corner prize board.
- ***A phrase's output was swept again by the word pass*** — the same bug from the other side.
- ***The eighteen TYPE NAMES are now withheld from the word map entirely.*** **NEVER_SWEEP protected
  the type table and nothing protected the type word.**
- ***And one guard had gone stale and become the bug.*** SMOKE BALL and LIGHT BALL were fenced off
  because BALL is the capture device; once they had names of their own the fence was the only thing
  stopping the rename. **A stale KEEP is indistinguishable from a missed substitution.**
- **Three registers logged OPEN, all for the same reason:** *berries* (43 names, a pocket, a second
  name table), *usable items*, and **`src/data/easy_chat/`** — **twenty-four files holding a second,
  independent copy of the ability, move and species vocabulary that no naming pass has ever touched.**

### 8.9 — MISSINGNO, the one daemon the Index does not hold

- ***An homage that turned into the cleanest statement of 4.2's complaint in the game.*** **Gen 1's
  MissingNo. is not a creature: it is the absence of a record, rendered** — and this project has spent
  eleven versions arguing that a mind is what somebody wrote down about it.
- **It lives in `SPECIES_OLD_UNOWN_B`**, one of twenty-five slots Gen 3 left over from a scrapped
  feature, *already carrying a footprint, an icon and a `DoubleQuestionMark` sprite.* **No new art.**
- ***Three numbers are the argument and none of them says it.*** **catchRate 255** — *nothing recorded
  it agreeing or refusing, so there are no rights to check.* **expYield 0** — *nothing recorded the
  encounter.* **Its dex number is 387 and `NATIONAL_DEX_COUNT` is 386**, so ***every list in the Index
  is bounded one short of it*** and not one line of new code was written.
- ***The seen and caught bits ARE set***, into a real byte of the save that nothing reads back. **The
  record exists and is not counted.**
- **Type is CORRUPT / ORACLE.** *Vanilla's MissingNo. is the unused BIRD type and 2.2 named that slot
  ORACLE* — **and the chart has no rows for it, so nothing about the fight changes.**
- **Surfing off the east shore of QUICKSILVER**, the one-percent slot of a rate-one water table, at
  level 80, with Gen 1's own stat line — ***33 / 136 / 0 / 29 / 6 / 6.*** **BALLISTIC is a two-turn
  routine, so the thing with 136 base ATTACK spends its first turn charging** and the encounter is
  survivable by accident. *The only way to lose it is to hit it.*
- **The old man on the shore is how you hear**, and folklore is how anyone found the original:
  *"Don't bother telling anybody. It's not on any list, so as far as they're concerned it didn't happen."*

---

## v11.130 — 2026-09-10

### The seven benchmark designs are mechanics now

- ***Six leader parties rewritten, two mechanics in C, one gym script.*** **5.3 named four
  levers that ignore level — priority, status, party composition and the room — and every
  leader now has one in the ROM.** *CAIRN needed nothing: his line already has DURABLE.*
- **BASIN.** *The GYM has no gradient.* **No wild encounters, both trainers put your party
  back the way it was after they lose**, and the ace holds LEFTOVERS beside RESTORE and PIN,
  so a steady attacker draws forever. **Nobody says why.**
- **GAUGE** gives **FAST PATH** to all three; **TILT** gains **TRACER**, who carries
  **ORPHAN**; **MATTE** gets **REPLAY** on MIME and **SILENCE** with **DISABLE** on the ace —
  *three routines, all of them about what you are permitted to consider.*
- **ANNEAL's party order is shuffled**, in 22 lines of `CreateNPCTrainerParty` — **after the
  party is created, so the name hash and therefore every stat is untouched.** *A randomised
  party and a randomised opponent are different designs.*
- **SCORN does not roll.** ***Maximum damage every time, never a critical, secondary effects
  never proc*** — one flag read in `ApplyRandomDmgMultiplier`, `Cmd_critcalc` and
  `Cmd_seteffectwithchance`. **Scoped to `TRAINER_LEADER_GIOVANNI`**; his two earlier fights
  still roll, and whether they should is <span>OPEN</span>.

### Two things the build found

- ***GROWTH has no coverage and 5.3 asked for it anyway.*** **Gen 3 gives grass-types no
  legal routine that hits fire, flying, ice or bug for extra damage** — *the wish was written
  before anyone read the movepool.* **So "answers" moved from damage to what each member
  takes away**: SATURATE answers speed, STARVE answers the attacker, DUMP answers the CORRUPT
  switch-in, and **STEELMAN answers the special attacker — which in Gen 3 is the fire starter
  everybody brings.** *All four hold at level 60.*
- ***BASIN is "she" and 5.3 said "his" four times.*** **The ROM has said `She won't lose to
  someone like you!` since the port.** *Corrected in the document, not in the game.*
- **And one register became visible.** **Held items have never been swept** — *BRIGHTPOWDER,
  QUICK CLAW, SCOPE LENS* — **and benchmark 2 is the first place a player reads one.** Naming
  only LEFTOVERS would be the draft 8.7 rules against, **so the register is logged whole.**

---

## v11.129 — 2026-09-10

### The Review Board is named, and 6's table had two stale rows

- **`PHLEGMATIC` · `CHOLERIC` · `MELANCHOLIC` · `SANGUINE`.** *6 says the humor scheme "reads
  as a classical flourish on arrival, and as the entire thesis about six seconds later"* —
  **so it has to be visible on arrival**, and the trainer names are where it is visible.
  **77 lines of dialogue swept with them.**
- ***Two of the four types were wrong and only two had ever matched.*** The table assigned
  **VECTOR** and **ENTROPY** to members I and II; the Elite Four seats they occupy are
  **EMERGENT** and **LOGIC**. **The humors are the argument and the types were an
  illustration**, so the illustration moved — and both improved. ***Choleric is LOGIC***:
  hot, driven, and reasoning by force is what a choleric fighter is. ***Sanguine is
  EMERGENT***: the one who is *pleased* by behaviour nobody designed — **a different optimism
  from 4.4's, and not to be confused with it.** *Scorn optimises a metric; this one welcomes
  what escapes it.*
- **And "Ty (incumbent)" was stale in two tables.** The decision log settled **Al Clear** as
  rival and incumbent — *Crystal's grandson, Ty's son* — **and both 1 and 6 were still naming
  his father, three weeks on.**
- ***The seats are not the order you meet them in.*** **You fight IV, II, III, I** — an
  institution's internal seniority is not the order it presents itself to you, and nobody
  remarks on it.

### What the long names cost, and what paid it

- **The humor words are twice the length of the vanilla names**, and 33 lines outgrew the
  message box. ***`port_vocab`'s own `fit_to` reflowed twenty of them***, because the pane's
  width and line count are demonstrated by vanilla rather than declared.
- **Eleven were introductions with no slack** — *"I am MELANCHOLIC of the REVIEW BOARD!"* is
  220px in a 196px box — **so they now say which seat they hold**: *"I am MELANCHOLIC. Third
  of the REVIEW BOARD."* **Which is better, and is where the numbering became audible.**
- ***And the reflow ate fourteen labels.*** It merged `Text_RematchIntro::` onto the line
  below and the assembler said only *"junk at end of line"*. **Repaired, and worth recording:
  a text pass that rewrites blocks must not assume a block begins at the start of a line.**

---

## v11.128 — 2026-09-10

### 5.3a — the leaders reached the ROM, and 637 trainers did not need touching

- **5.3 designed seven benchmark leaders and the trainer table still said MISTY.** Six are in
  now — **BASIN, GAUGE, TRELLIS, TILT, MATTE, ANNEAL** — beside CAIRN and SCORN, ***and 127
  lines of dialogue moved with them***, because a leader who introduces herself by a name the
  battle screen does not use is worse than one never renamed.
- ***Two corrections the bible had already made and the table had not.*** **`TERRY` × 27** —
  vanilla's default rival, on every rival and champion battle, **and 4.3 named him `AL` weeks
  ago**: the bible had a rival called Al Clear and the ROM had one called Terry. **`GRUNT` ×
  51** — *1.7 rules Corpus is never described in intrusion language and craft rule 6 has them
  cheerful and absurd.* **A grunt is a thug; `STAFF` is what the organisation calls the same
  person**, and it is quietly worse.
- ***743 trainers, and only six had names we had changed. The other 637 are people.***
  JOEY, BEN, TIMMY, CHAD — ordinary first names, and they stay. **2.8's rule for the fifth
  time**, and *a world where every passer-by is a computing pun is a world with nobody in
  it.* **1.6a already put the argument on the other line: the CLASS says what they do, the
  NAME is just their name.**
- *Why trainer names are not in `port_vocab`'s learning:* **`AL` is two characters** and would
  match inside anything. The six leaders were swept by hand with a word boundary.

### The Review Board is deliberately not named

- **6 numbers its members and gives each a humor and a TYPE** — VECTOR, ENTROPY, LATENT,
  FROZEN. ***The Elite Four actually use FROZEN, LOGIC, LATENT and EMERGENT. Two of four
  match.***
- **Naming them now would quietly settle whether 6's humors move or the Elite Four's types
  do**, and that is a chart decision rather than a naming one. **Logged Open.** *The class
  already reads `REVIEW BOARD`, which is the half that was decided.*

---

## v11.127 — 2026-09-10

### 1.6a — the trainer classes

- **Twenty-three were already ours and the register was legible from them.** ***A trainer
  class is an OCCUPATION*** — what this person does, by trade or by disposition, in twelve
  characters.
- ***The test is what does NOT change.*** **FISHERMAN, SCIENTIST, ENGINEER, PAINTER, SAILOR,
  GENTLEMAN, EXPERT and LEADER are occupations in any world and were left alone** — 2.8's
  rule, for the fourth time. **Forty-five moved**, each failing in one of three ways: it
  **named a creature** (BIRD KEEPER → **DISPATCHER**, DRAGON TAMER → **WRANGLER**), it was
  **era slang** (COOLTRAINER → **OPERATOR**, SUPER NERD → **TINKERER**, CHANNELER →
  **MEDIUM**), or it was **a child or a gender role** (LASS → **APPRENTICE**, CRUSH GIRL →
  **GRAPPLER**, RICH BOY → **HEIR**).
- ***`MEDIUM` works hardest***: a medium speaks for the dead **and** a medium is what a signal
  travels through — *and she is standing in Halftone Tower.*
- **The `RS_` twins moved with them**, because they exist so a link battle reads the same as
  a local one.

### Two collisions, one of them three weeks old

- ***`PSYCHIC` became `CONSTRUE` twice*** — once as this trainer class, and once weeks later
  as the CONTEXT routine in 2.9. **Neither pass could see the other, because `check_lexicon`
  was not reading the trainer table.** The routine keeps CONSTRUE; the class is
  **`INTERPRETER`**, which is the better word for a person.
- **`BLACK BELT` was a class and a held item**, vanilla's own collision inherited. The class
  is **`FORMALIST`**; the item is **`RIGOUR`** — *what you hold to argue harder from* — and
  **its description had said FIGHTING-type since before 2.2 renamed that to LOGIC.**
- ***Both surfaces are watched now.*** `check_lexicon` reads the trainer table and
  `port_vocab` learns renames from it — **which immediately found four lines of dialogue
  still saying `POKéMANIAC`, three weeks after it became ARCHIVIST.** *The accented prefix,
  for the sixth time.*

---

## v11.126 — 2026-09-10

### 8.2d — the dex categories, and the register that was already on the shelf

- ***A vanilla category is a kind of ANIMAL*** — MOUSE, BAT, FLOWER, TADPOLE, WILD BULL — **a
  taxonomy of creatures, which this game does not have.**
- **Forty-four were already ours and nobody had written down what they were doing.** *Read
  together they are unmistakable*: PACKET is **IN TRANSIT**, PENDING is **QUEUED**, DEADLOCK
  is **BLOCKED**, QUORUM is **THRESHOLD**, INJECTOR is **UNCHECKED**, MUSAI is **UNSET**.
  ***The register is the condition it is in, or the role it plays — one abstract word, never
  a species of animal***, in eleven characters.
- ***That is the third register found already-decided and unrecorded*** — after 8.2b's
  bestiary fork and 2.9's move tables. **Worth naming as a pattern: this document is better
  at making decisions than at noticing it has made them.**
- **111 written.** `HAUNTPROC` is the **UNPARENTED** daemon — the whole Index entry in two
  words. `STUB` is the **PLACEHOLDER** and evolves into `ESCALATE`, the **RAISED** one.
  `LIVELOCK` is **NO PROGRESS**, which is the definition and also the joke. `WEED` is the
  **VOLUNTEER**, which is the gardener's word for a plant nobody sowed.
- **155 of 387 are ours, and no renamed daemon carries a vanilla category.**
- ***One thing the sweep almost missed***: MULTICAST, NOISE, SEMAPHORE and KERNEL fell
  outside the meetable set, because *their pre-evolutions are met and they are not.* Checking
  **"does any renamed daemon still have a vanilla one"** caught them where the scope query
  did not — **the question you check afterwards is not the question you scoped with.**

---

## v11.125 — 2026-09-10

### 8.2c — the Index caught up with the names

- ***Renaming seventy-nine species left seventy-nine Index entries describing the old
  ones.*** **A daemon called `TARPIT` with an entry about a carnivorous plant is worse than
  one still called VICTREEBEL** — the name now promises something the record does not
  deliver. **Sixty-one were in the meetable Kanto set, and each needed two entries.**
- ***0.4's ruling applied at scale for the first time.*** **CONTENT says what it does;
  CONTEXT says what follows from it** — written for four daemons until today, now for
  sixty-five. **`BADSEED`:** *"Releases a dust that settles on whatever is learning nearby.
  The dust is indistinguishable from pollen."* against **"What it fed on is in what it
  became. Nobody kept a record of the feeding."** *Neither is wrong and they do not meet.*
- **Where the pair did most:** `CLUSTER` *(six of them, none in charge / one is usually wrong
  and no record says which)*; `HAUNTPROC` *(no parent, no terminal, no entry in any list /
  something started it, and that something has exited)*; `TAPPOINT` *(sits under the route
  and reads what goes past / it is not in anyone's diagram)*; `UPTIME` *(has never stopped /
  it is kept running because stopping it has never been costed)*; `COOKIE` *(picked up again
  later by whoever set it down / it remembers everywhere it has been, and you did not agree)*.
- ***The count of entries differing between editions did not move, and that is not a bug.***
  **Vanilla already ships different text for many species** — 0.4 records the inheritance —
  so these sixty-one were already counted. **What changed is that they now differ on
  purpose.**
- **196 CONTENT and 189 CONTEXT entries are ours**, and ***no renamed daemon carries a
  vanilla record any more.***

---

## v11.124 — 2026-09-10

### 8.2b — the bestiary register was already decided

- ***The open log said the register was undecided and gated 151 names. It was not.*** It had
  been decided in practice by 4.26 and nobody wrote it down — **8.7's rule about unswept
  rulings, applied to a fork rather than to a fact.**
- **Three registers, read off the seventy-two that shipped:** *technical surface* for the
  bestiary (HEAP, FORK, PACKET, LATENCY); ***myth for the legendaries*** — **ASCLEPIUS,
  ORPHEUS, PROMETHEUS ARE the "true names the Index cannot reach"** that the fork's other
  half proposed, spent on exactly the creatures the Index was never going to hold; and *the
  project's own names* for MUSAI and ROVER, who are characters rather than creatures.
  ***The fork was never either/or. It was a distribution.***
- **The bound is 8.2a's, not a new one.** 386 species exist, 207 are meetable, **79 are Kanto
  and 69 are beyond it — every one of the 69 reached through the Sevii Islands**, where
  8.2a's ruling already says *name nothing there.* **151 of 386 species names are ours.**
- **`BELLSPROUT` → `SNARE` → `HONEYPOT` → `TARPIT`** — a GROWTH/CORRUPT line that catches
  things and holds them, *in order of how long it holds you.* `DIGLETT`/`DUGTRIO` →
  **`TAPPOINT`/`WIRETAP`**. `VENOMOTH` → **`SPYWARE`**. `FARFETCH'D` → **`EDGECASE`**.
  `TANGELA` → **`SPAGHETTI`**, and craft rule 6 says nobody points at it.

### The sweep found a principle the tools had been missing

- **79 renames left 65 places in dialogue naming the old species**, so `port_vocab` swept 103
  files — **and broke the build three times, the same way each time.**
- `DIGLETT` → `TAPPOINT` reached **`DIGLETT'S CAVE`** and took a hand-written C symbol with
  it. `EMBER` → `JITTER` produced **`MT. JITTER` and `JITTER SPA`** — ***both on the Sevii
  Islands, where 8.2a says name nothing.*** `MOONLIGHT` → `NIGHT REPAIR` put twelve
  characters in an eleven-character **dex category**. And `GROWTH` → `SCALE UP` went for
  ***the GROWTH TYPE NAME*** — **only the array's own width stopped it.**
- > ***NAME TABLES ARE AUTHORED. PROSE IS SWEPT.*** A pass that rewrites prose must never
  > reach a table it also learns from, or a rename on one surface silently rewrites another.
  > **Places, dex categories and type names are all names.**
- **`port_vocab` refuses rather than truncates now** — it checks every fixed-width surface
  before writing anything and names the offender. *Twice in this session a constant was added
  as a comment and not wired in; both are enforced.*

---

## v11.123 — 2026-09-10

### 2.11 — the abilities, and a register that is not a verb

- **9.3 named abilities as a reason to port; 8.7 called them the second teaching surface the
  project paid for and never spent.** ***77 of 78 are ours now*** — the last is vanilla's
  blank slot.
- ***A ROUTINE is an operation; an ability is a standing property*** — **what is true of a
  daemon while it is doing nothing**, which is what 4.29 already reads a daemon by.
  **The register is a flag set on the process**: file permissions, compile flags, hardware
  properties. ***The test: if the name describes an action it is a routine.*** That grammar
  is what stops the two surfaces colliding as they grow.
- **Vanilla wrote four for us.** `LEVITATE` → **`NO ADDRESS`**, which is *2.6's clause for
  STRATUM ×0 VECTOR verbatim*. `TRACE` → **`INHERITS`**, on SUBSTRATE — *the substrate takes
  on whatever runs on it*, that daemon's Index entry as a mechanic. `SYNCHRONIZE` →
  **`MUTUAL`**, which ARTSAI already has. `STURDY` → **`DURABLE`**, which **5.3 leans on**:
  HEAP, STACK and MONOLITH cannot go down to one hit — *Benchmark 1's creed as a rule in the
  damage calculation.*
- **Where the flag was already the joke:** `OVERGROW` → **`OVERFIT`** *(stronger the closer it
  is to failing)*; `HUSTLE` → **`UNSAFE OPT`**; `WONDER GUARD` → **`NARROW BAND`**;
  `NATURAL CURE` → **`CLEAN EXIT`**; `TRUANT` → **`HALF DUTY`** *(a duty cycle)*.
- ***And a pair nobody had read as one:*** **`PLUS` and `MINUS` are `SOURCE` and `SINK`** — a
  current source and a current sink, which is exactly what they do to each other.
- **31 descriptions rewritten** in a 32-character box, most of them describing a body.
  *Two came free from work already done*: **`Prevents self-destruction` is now `Nothing here
  may PANIC`** and **`Prevents fleeing` is `The foe cannot DETACH`** — because 2.10 renamed
  SELFDESTRUCT and 1.4 had already renamed fleeing, **and the surfaces had drifted apart.**

---

## v11.122 — 2026-09-10

### The other two routes — every routine the player can meet is ours

- ***2.10's pass followed level-up learnsets and stopped, which was one route out of three.***
  **The TM list is 58 moves and the trainer parties use 225**, and **89 of those were still
  vanilla** because no daemon learns them by level and nothing had looked down the other two
  roads.
- **269 of 356 now** — ***every TM, every HM, and every routine any trainer in the game will
  use***, with one deliberate exception: **`OVERHEAT`, kept because an ENTROPY routine
  agreeing with ENTROPY's own state is the point.**
- ***The best of the eighty-nine are where the mechanic and the register said the same
  thing.*** **`PETAL DANCE` → `OVERTRAIN`** *(locks you in for two or three turns and ends in
  THRASHING — which is what overtraining is)*. **`BULLET SEED` → `MINIBATCH`** *(two to five
  small passes rather than one large one; that is the definition)*. **`DYNAMICPUNCH` → `NON
  SEQUITUR`** *(confuses, and misses half the time)*. **`SANDSTORM` → `BIT ROT`**.
  **`GUILLOTINE` → `KILL`**. **`POISON GAS` → `LEAK`**.
- ***`SIGNAL BEAM` → `GOSSIP`*** — **held since 2.8 and released by 2.9**, because a gossip
  protocol is 2.6's clause for SWARM word for word.
- ***`BIND` had to move for a reason none of the others did.*** **It is 1.5's word — what you
  do to a daemon** — and a trapping routine wearing it would have put BIND in the battle log
  meaning something else entirely. → **`LATCH`**.
- **28 more descriptions rewritten**, every line measured; widest 121px of 170.
- ***What is left is genuinely unreachable.*** The 87 remaining are learned by no daemon,
  taught by no TM and used by no trainer — **they belong to species the bestiary has not
  reached, so they wait on 8.2 rather than on a decision.**

---

## v11.121 — 2026-09-10

### 2.10 — the ROUTINES pass, done to the reachable edge

- ***181 of 356 move names are ours*** — **every routine any daemon in this game learns by
  level**, plus the eight HMs and the two already renamed. **157 in one pass.**
- ***Every one came out of 2.9's table rather than out of taste***, and the best names are
  the ones where the register did the work:
  **`AERIAL ACE` → `HOMING`** *(a never-miss move, in a register about heading)*;
  **`MUD SPORT` → `GROUND`** *(grounding a signal is the literal engineering answer, and the
  move halves SIGNAL routines)*; **`MIST` → `READONLY`** *(blocks stat changes — weights that
  do not update, said as a file permission)*.
- ***And one the chart wrote for us.*** **`BRICK BREAK` → `FALSIFY` breaks LIGHT SCREEN and
  REFLECT — which are now `STEELMAN` and `PARAPHRASE`.** *LOGIC falsifying CONTEXT's framings
  is 2.2's thesis relation, arriving as a move interaction nobody designed.*
- **`SEISMIC TOSS` → `EQUATE`**, because its damage equals your level and the name is the
  formula. **`LOW KICK` → `WEIGH`**, because its power is the target's weight.

### The checker caught six thefts in one run

- **`CLAMP`, `PREEMPT`, `BUFFER`, `ESCALATE`, `ASSIST` and `FORK`** were all proposed and all
  already taken — *four by species, one by an unrenamed move, one by an item.* Re-cut as
  **`BROWNOUT`, `FAST PATH`, `PRELOAD`, `ACCUMULATE`, `DELEGATE`, `INSTANCE`.**
- ***`BROWNOUT` is better than what it replaced***: a brownout is a voltage sag that makes
  everything run slow and unreliable — **THROTTLED, stated electrically**, which is what
  THUNDER WAVE does.

### Thirteen kept, fifty-eight descriptions rewritten

- **`DISABLE` `PROTECT` `SAFEGUARD` `LOCK-ON` `METRONOME` `RECYCLE` `BLOCK` `MIMIC`
  `MINIMIZE` `RECOVER` `ENDURE` `CONVERSION` `CONVERSION 2`** left alone — *2.8's rule that
  the pass which renames what already lands makes the game worse.*
- ***Fifty-eight descriptions had to move with their names***, because one that still
  describes the old move is worse than no rename: *`OCCLUDE` cannot say "bites with vicious
  fangs".* **Every line measured; the widest is 126px of 170.**
- **What is left is not the same job.** The remaining 175 are moves *no daemon learns by
  level* — **trainers reach some and TMs teach others**, so the next pass is the trainer
  parties and the TM list, and it is smaller than 175.

---

## v11.120 — 2026-09-10

### 2.9 — the other seventeen registers, and the rule that was a sequence

- ***2.8 settled CONTENT and this project then treated that as a rule instead of a
  sequence.*** CONTENT went first because it was 79 of the 175 reachable routines and would
  set the tone — **an argument about ORDER**, applied twice as though it were an argument
  about **method**, holding `SIGNAL BEAM` and five HMs for a decision nobody was waiting on.
- ***A register is not invented. It is 2.6's clause turned into a part of speech.***
  **LOGIC** is derivation, **VECTOR** is delivery with a heading, **LEGACY** is the old
  instruction set, **SWARM** is the distributed protocols, **FROZEN** is weights that do not
  update, **OPAQUE** is opacity. *All seventeen existed already; the section is the
  derivation written down.*

### Settling them all at once caught four thefts

- **2.8's counter-test said the seventy-nine must not annex vocabulary the other types need,
  and then batch one annexed four words anyway** — *because there was nothing to check
  against.* **A rule with no table behind it is a hope.**
- `DEPRECATE` → **LEGACY's whole register**, re-cut as **`DERATE`** *(running a component
  below its rated capacity)*. `OBFUSCATE` → **OPAQUE's name said as a verb**, re-cut as
  **`BLUR`**. `REVOKE` → *access-control, which 1.7 rules is institution vocabulary*, re-cut
  as **`DOWNCLOCK`**. **`PIN` contested with FROZEN and was kept** — *pinning is about not
  being moved; freezing is about not being updated.*

### The HMs are the access model, on the map

- ***An HM only works in the field once you hold the MARK.*** That is the gate, which makes
  an HM **a capability you have been certified to exercise** — exactly the access-control
  reading 1.7 rules on-thesis. **So the MARKS are a keyring as well as 5.2's bench of
  instruments**, and **the box ladder is the same model applied to daemons.** *Two
  implementations of one idea, and nothing connects them.*
- `CUT`→**PRUNE** · `FLY`→**GOTO** · `SURF`→**TRAVERSE** · `WATERFALL`→**ASCEND** ·
  `DIVE`→**DESCEND** · `STRENGTH`→**DISPLACE** · `FLASH`→**VERBOSE** · `ROCK SMASH`→**CRACK**.
  ***TRAVERSE, ASCEND and DESCEND are across, up and down — three directions on one medium,
  which is exactly what the three moves do.*** **`GOTO` beat `JUMP`** because a jump's first
  read is a hop, and *you can only reach a CHECKPOINT you have already been to, which is what
  "known address" means.*
- **`VERBOSE` is the best of the eight**: `-v` turns on the output nobody could see **and
  floods the channel so nothing can be found** — the field effect and the battle effect in
  one word.
- ***And the failure messages are where these are actually taught***, because a player meets
  them far more often than a description: **`There is nothing to PRUNE.`** and **`You cannot
  TRAVERSE here.`**
- *Recorded because it was misremembered once:* **`ROCK SMASH` does not exist on the Game
  Boy** — it is a Gen 2 addition that arrived with the port, which is why DISPLACE and CRACK
  do not overlap. **It belongs in 9.3's list of what the spike bought.**

### 23 routines renamed

- The CONTENT batch — **WRITE · FLIP · PUSH · INSERT · OVERWRITE · COMMIT · EMIT · DERATE ·
  DOWNCLOCK · EXPOSE · INSPECT · STRIP · DEMOTE · BLUR · ADVERTISE** — plus the eight HMs.
  **All 23 checked clear against species, moves, abilities, types and items**, all inside the
  12-character budget, and every description rewritten and measured against the 170px box.

---

## v11.119 — 2026-09-10

### `BUSY WAIT` and `PIN` — and the first one was hiding a better move

- **`THRASH` is `EFFECT_RAMPAGE`**: ninety power, locked in for two or three turns, no
  switching and no choosing, **and it ends by leaving the user THRASHING.** *Its own
  description read "rampages about… then becomes thrashing", which after 1.6 read as a typo
  rather than a joke.*
- ***That is a busy-wait, exactly and completely*** — **a loop that will not yield the
  processor, runs flat out for as long as it holds it, and leaves the system thrashing when
  it is done.** → **`BUSY WAIT`**. *The vanilla move was already describing the thing;
  nobody had noticed because it was wearing a body word.*
- **`HARDEN` → `PIN`**, per 2.8's own worked example: *pinned memory cannot be moved or
  swapped out*, which is DEFENSE-up stated as an operation. **Its description was a body word
  too** — *"stiffens all the muscles in its body"* — **in a world 1.6 established has no
  bodies.**
- ***Two moves now wear another word's name and one is deliberate.*** **`OVERHEAT` is
  kept** — an ENTROPY move agreeing with ENTROPY's own state is the point. **`SIGNAL BEAM`
  is Open and held on purpose**: *2.8 settled the CONTENT register and no other*, so naming
  a SWARM routine now would pre-empt the decision 2.8 exists to make first. **`GOSSIP` is
  the proposal** — a gossip protocol is nodes passing state around until they agree, which is
  2.6's clause for SWARM word for word, and the rider leaves the target THRASHING.

---

## v11.118 — 2026-09-10

### The last two collisions, and the pair was free

- ***`GROWTH` was a CONTENT move wearing the GRASS type's name.*** ***`SWARM` was vanilla's
  Bug ability wearing the BUG type's*** — **found by `check_lexicon` on its first run**,
  which is the whole point of a check that reads every surface rather than the ones that
  existed when it was written.
- **Both are the same operation seen from two sides, and the field already had the words:**
  **`GROWTH` → `SCALE UP`** *(one instance given more)* and **`SWARM` → `SCALE OUT`**
  *(more instances)*. ***That is the real distinction in the field and it lands on exactly
  the right two things*** — the CONTENT move makes one thing bigger, the SWARM ability makes
  more of them and only when pressed. **Neither name had to be invented and the pair was not
  planned.**
- **Six ability descriptions still named vanilla types and went with it** — *Ups BUG moves,
  Ups GRASS moves, Ups FIRE moves, Ups WATER moves, Not hit by GROUND attacks, Traps
  STEEL-type DAEMON.* **The ability NAMES are still vanilla** — WATER ABSORB, FLASH FIRE,
  ROCK HEAD — *and belong to 8.7's ability pass, not to this one.*
- ***`check_lexicon` now reports clean: 1,152 names across abilities, items, moves, species,
  states and types, and no word means two things.***

---

## v11.117 — 2026-09-10

### 5.3 — the other seven benchmarks, and what a grinder runs into

- **8.7 called this the largest prose-to-ROM gap in the project.** Seven leaders with a
  concept, a one-line lesson and no mechanics — *"punishes split focus" is a wish.*
- ***Craft rule 5, restated as a test each design must pass:*** **name the thing an
  overlevelled player still runs into.** *If more levels solve it, it is not a lesson — it is
  a wall with a lesson written on it.*
- **Four engine levers ignore level entirely**, and every design is built from them:
  **priority** (moves before speed), **status** (a THRASHING daemon at 80 still hits itself),
  **party composition** (no single daemon sweeps a spread), and **the room** (a puzzle cannot
  be ground). *Everything else is stats, and stats are what grinding buys.*

### The seven

- **2 · `BASIN`** — Doldrum · FLOW · SLOPE. *A bowl that holds water; and the basin of
  attraction an optimiser cannot climb out of.* **No wild encounters, and his trainers heal
  you after they lose** — the one gym you cannot grind inside. **His ace holds LEFTOVERS and
  knows RECOVER**, so steady damage is a draw forever: ***more power does not break a loop,
  it makes a bigger loop.***
- **3 · `GAUGE`** — Ardor · SIGNAL · SENSE. *An instrument that senses; and to gauge is to
  perceive.* **Keep vanilla's switch puzzle — it is already a perception test.** Everything
  he has knows a **priority** routine, and *priority ignores speed, the one stat
  overlevelling does not settle.* **He says you were quicker. You were ready.**
- **4 · `TRELLIS`** — Verdigris · GROWTH · FIT. *The frame you train a plant to; it grows
  that shape and no other.* **The party is built by coverage, not strength** — one daemon at
  60 loses to the fourth member; four at 30 do not. ***Grinding is precisely the failure the
  gym is about.***
- **5 · `TILT`** — Lurid · CORRUPT · SKEW. *A distribution tilts; and to be on tilt is to be
  made unreliable by your own state.* **THRASHING and OBFUSCATE, in the invisible-wall
  maze** — the cleanest grind-proof design of the seven, *and 4.10's echo finally has a
  mechanic:* **the benchmark that teaches poisoning teaches what was done to Ty, three cities
  early.**
- **6 · `MATTE`** — Brazen · CONTEXT · FRAME. *The mount around a picture, and the film term
  for what is masked out* — 0.2's register exactly. ***ENCORE is the mechanic***: locked into
  your last routine, and the answer is to **back out one menu.** *9.16's FRAME show, played.*
- **7 · `ANNEAL`** — Quicksilver · ENTROPY · HEAT. *Controlled heat that lets a material
  settle — and the optimiser that uses temperature to escape a local minimum.* ***So
  Benchmark 2 traps you in a basin and Benchmark 7 is the heat that gets you out***, five
  cities apart, each named for its own lesson before the pair was noticed. **Filed under 0.2
  as a coincidence kept, not a plan.**
- **8 · `SCORN`** — Callow · STRATUM · TRUE. **Always maximum, never critical, no secondary
  effects.** ***The only fight that cannot be won on a good roll*** — and **that is
  alignment**: flawless execution of a specification nobody checked.

### And CAIRN already had one

- ***HEAP, STACK and MONOLITH all have STURDY***, so **they cannot be knocked out in one blow
  at any level** — *"everything must be encoded in something physical", as a rule in the
  damage calculation.* **Vanilla put it there and 5.1 never mentioned it.**

---

## v11.116 — 2026-09-10

### 8.7 — the third review, with every ruling recorded so this one gets swept

- **Its sharpest line is about the document**, and is filed as binding beside 8.6's:
  ***"A ruling nobody swept is not a decision, it is a draft."*** So 8.7 records **every**
  item with a verdict, refusals included, and the open ones carry the tag.

### Scorn met Crystal — "he never met her" is retracted

- **It could not coexist with 07's directive addressed to her, 4.20's minutes with two
  present, and 4.21's two men conferring** — and *met her* is a fact, not a frame.
- **New canon:** the company is founded with **Ty as CEO**; ***Scorn's Solution* is the
  hiring**; he designs the standardised evaluations **and rigs them, so rivals fail**;
  he becomes valuable, and **Ty introduces him to Crystal.**
- ***The horror is better than the one it replaces.*** It was never that he had no memory of
  a stranger — **it is that her son brought him to her, in her own building, and the
  signature still left no mark.** It makes 4.31's gym line exact: *he knows precisely what he
  weighted and has no idea whose lab he weighted it in.*
- ***And Crystal gains the one thing she lacked: standing to notice.*** **She is the only
  person in the story who saw Ty before Scorn and after** — not a mother's complaint about a
  colleague, a researcher's observation of a change she can date. **She never says it.**

### PREEMPT, and the check that was scoped to the day it was written

- **ICE HEAL → `WATCHDOG`.** It collided with MANKEY, named four days earlier — *and the
  review found the fault under the collision:* **preempting a hung task hands the processor
  to somebody else and the hung one stays hung.** A watchdog is the timer whose whole job is
  to notice something stopped answering and reset it. **The actual cure, still works twice.**
- **`tools/check_lexicon.py` is new.** 4.26 *did* run a collision check — against species,
  moves and types, **not items, because the item pass had not happened yet.** *Complete for
  the day it was written and incomplete by the following week.* The new one **reads every
  surface out of the build on each run.**
- ***It found a third collision on its first run that neither the review nor the project had
  seen:*** **`SWARM` is our BUG type and vanilla's Bug ability.**
- **1.7's security rule is amended.** It would have condemned `PAYLOAD`, `ROOTKIT` and
  `INJECTOR` — three species that shipped five days before it. ***Intrusion words belong to
  CREATURES; they never belong to the INSTITUTION.*** Sharper than the line it corrected.

### Taken, held, and refused

- **Free wins taken:** HOTFIX already costs colour; the Index completion line is already
  written; FROZEN's concept line gains *weights that are not updated*; **LOGIC → OPAQUE →
  CONTEXT → LOGIC is a cycle** — the interpretability gap as a triangle, out of Game Freak's
  own table. **Vera is Ainsworth and Halftone is Doka, both written without the clinical
  word — do not touch either.**
- **Ideas taken:** *"IMPROVE RESPONSE CONSISTENCY" becomes a mechanic* — **Scorn's daemons
  always roll maximum and never crit**, and the CC-7 pull gives S.T.A.R.R. its variance back.
  The ability pass. `CONVICTION` for Choice Band. The Five Witnesses differing by edition.
  Al's party desaturating. **And the Index sprite keeping the saturation it was recorded at
  and never updating** — 4.2 as a mechanic, one byte per species.
- **Held:** `SUS`→`ZZZ`/`HLD` *(a playtest decides it, not an argument)*; **`LEGACY`→`RUST`
  and `VECTOR`→`FLOAT`, the two best proposals in the review** and both type renames;
  `PRIORITY`→`BURST`; `MP`→`CYCLES`.
- **Refused:** CONSENSUS scaling with the quorum. **2.5 made it boring on purpose** — *a
  swarm does not need a gimmick, it needs to keep showing up* — and the proposal is better
  writing and worse balance.
- ***And the thing the review is most right about:*** **craft rule 5 is unpaid for benchmarks
  2 through 8.** Seven leaders with a concept, a one-line lesson and no mechanics.
  **The largest prose-to-ROM gap in the project, sitting on the spine of the fun.**

---

## v11.115 — 2026-09-09

### 2.7a — the three starters, curated to their paradigms

- **`tools/port_starters.py`. Off-type damaging routines across the three lines: 74% → 31%.**
  ***No type moved*** — the chart is untouched (8.4), no matchup moved (2.5), only which
  routines a daemon reaches for, which is the cheapest of the three levers and the only one
  that costs the argument nothing.
- **SUPERVISED — LABL · RUBRIC · CANON.** *A supervised learner is the least entropic thing
  in the set — it has ground truth — so a line that fought entirely by heat was the sharpest
  seam of the three.* **FORESIGHT** identifies the target, which is what a label *is*;
  **MIMIC** copies the answer it was shown; **SWIFT** cannot miss; **TRI ATTACK** is
  classification into three outcomes and, with STAB, hits harder than the FLAMETHROWER it
  replaces; **LOCK-ON** cannot miss *because you have the ground truth*. CANON's second type
  brings **COUNTER**, which returns exactly the error it was given.
- **UNSUPERVISED — CLUSTR · LOCUS · MANIFOLD. The FLOW spine stays, and that is a finding.**
  *k-means descends a distance objective, and FLOW's clause is "everything running downhill
  to the lowest point"* — the water is the algorithm, not a leftover. **It is also
  load-bearing: FLOW ×2 against LEGACY is the one LEGACY relation that reads, and Slate is
  Benchmark 1** — stripping it would have broken the first gym to make a point the chart was
  already making. What was missing is that **a VECTOR line knew no VECTOR routines at all**:
  GUST, AIR CUTTER (*a separating surface*), DRILL PECK, and **SHADOW BALL on MANIFOLD,
  because the manifold *is* the latent space.**
- **REINFORCEMENT — ROVERCUB · ROVERSEER · ROVERBYTE**, which needed the least, and that is
  worth saying: ***LEECH SEED is the best-fitting routine in the whole set and nobody
  arranged it*** — a return that accrues every turn from a thing you did once. **SOLARBEAM
  charges a turn before it pays, which is delayed reward, in the engine, since 1996.** Two
  changes: MEGA DRAIN for POISONPOWDER, and **SHOCK WAVE on ROVERBYTE, which gained SIGNAL as
  a second type and had never learned a single SIGNAL routine.**
- **The residual is chosen, not left over.** **DRAGON RAGE** stays on the supervised line
  because EMERGENT is *behaviour nobody can account for*; **BITE** stays on the unsupervised
  one because OPAQUE is the black box and unsupervised methods are the least interpretable
  thing in the field. ***It landed at 31%, below the 45% baseline rather than at it*** —
  defensible for the three daemons a player carries all game, but not the number aimed at,
  and recorded rather than rounded off.

### 2.7's two open questions, one of them closed by the engine

- **THRASHING is ownerless, and it is not ownerless by omission.** `battle_util.c` deals the
  confusion hit with **the attacker and the defender as the same battler**, type argument
  zero, abilities suppressed. *Every other state is something a kind of thing does to you and
  carries a type because that thing has one.* **This is the only one where the sufferer deals
  the damage, so there is nobody whose type it could be** — which finally gives a reason for
  the missing code and the missing item rather than just a record of them.
- **The seam is measurable and confined.** **Thirteen of the seventy-two were also retyped**,
  and they are the three starters, the Musai branch and STARR — *every one retyped to carry an
  argument.* **The fifty-nine left on vanilla's typing are 45% off-type; the thirteen were
  78%.** Off-type is already a statement the engine makes — same-type attack bonus means a
  routine of your own type hits harder *because it is you* — but **a statement made 78% of the
  time is not a statement.** Nine of the thirteen are now done; **the Musai branch and STARR
  are still owed.**

### Housekeeping

- **Two sessions wrote §2.7 on the same day from the same conversation** and both claimed
  v11.112. The ROUTINES-pass version is canonical; the duplicate section and its changelog
  entry are removed, and the two findings it alone carried — the engine's word on THRASHING,
  and the retyped-thirteen measurement — are merged into it.

---

## v11.114 — 2026-09-09

### 2.8 — the CONTENT register, settled

- **The number was frightening and the shape is not.** Grouped by what they do, the
  seventy-nine CONTENT routines are **7 plain damage, 25 damage-with-a-rider, 8 that lower
  theirs, 6 that raise ours and 33 status/control.** ***Only seven are plain damage*** —
  **CONTENT is mostly CONTROL**, which is why the type that hands you no verb turned out to
  have the most verbs available.
- **The register is the instruction set** — `WRITE`, `CLEAR`, `COPY`, `SHIFT`, `FLUSH`.
  ***An instruction has no semantics beyond what it does***, which is *"nothing read into
  it"* stated as a part of speech rather than as an absence. It is also the register the
  project already speaks: ROUTINES are subroutines, the items are operations, and **0.5 says
  CONTENT is the serial half — the one that shows its working.**
- **THE TEST:** *say the name; if you then have to say what it does, it is not CONTENT.*
  **THE COUNTER-TEST**, which stops the register eating the game: *CONTENT does not decide,
  weigh, frame or infer* — a word implying judgement belongs to CONTEXT, LOGIC or LATENT.
- **`TACKLE` → `WRITE`.** Twenty-five of the seventy-two learn it and for most it is the
  first routine they know, so it sets the tone. *Damage in this world is putting your data
  where theirs was.*
- ***And the perfect answer is unusable, recorded so nobody proposes it again.*** **`POKE` is
  the BASIC instruction that writes one byte to an address** — works twice, four characters,
  and **unusable in a game that has spent five passes deleting `POKé`.** *A pun that survives
  the read-aloud test and not the search-and-replace test is still a no.*

### Thirteen already work, PERSPECTIVE stays, and ten things collide

- **Not to be touched:** `DISABLE` `BLOCK` `PROTECT` `RECOVER` `ENDURE` `LOCK-ON` `SAFEGUARD`
  `MIMIC` `MINIMIZE` `METRONOME` `RECYCLE` `CONVERSION` `CONVERSION 2`. *A metronome is a
  clock, recycling is garbage collection, and a type conversion is a type conversion.*
  **Same finding as *catchy tune*: the pass that renames what already lands makes the game
  worse.**
- **`PERSPECTIVE` is kept as the deliberate exception.** It was already in the table and
  nobody had flagged it. *It looks like it breaks the register — perspective is the most
  CONTEXT word in the lexicon* — **and it sits on MOCK, the daemon with no content of its
  own, whose whole nature is becoming whatever it is shown.** ***The one CONTENT routine
  about taking a point of view is carried by the one daemon that has none.***
- **Ten move names collide with our own lexicon**, and nothing had checked because the move
  pass never started — *the same class as `INTERRUPT` being assigned twice.* **`GROWTH` wears
  the GRASS type's name, `THRASH` wears the confusion state's, `HARDEN` wears STEEL's** —
  all three must move. **`OVERHEAT` is kept**: a fire move and ENTROPY's own state agreeing
  is the point.

---

## v11.113 — 2026-09-09

### 0.5 — two perspectives, and why neither can send the other a transcript

- **0.4 named the two halves and stopped at recognition.** This is the layer under it: *why
  there are two points of view at all, what actually crosses between them, and why the
  crossing is the thing worth having.* **Demystified on purpose** — what is measured is kept
  apart from what is argued, and 0.2's rule holds throughout.
- **Measured:** cut the callosum and you get two points of view in one skull that each
  behave as though their own access were the whole of what happened. **And the callosum is a
  few hundred million axons joining a cortex holding orders of magnitude more state — so
  whatever crosses cannot be a transcript.** *That is arithmetic, not interpretation.*
- **Argued:** so the halves exchange **many partial summaries at once, none complete**. And
  ***receiving many partial things simultaneously is not a degraded version of receiving one
  complete thing — it is a different faculty***, and it is the one we call perception:
  associative, arriving whole, unable to show its working. **CONTEXT.** *Serialising the same
  material — one at a time, each licensed by the last — is* **CONTENT read through LOGIC.**
- ***And the part worth stating rather than gesturing at:*** **an order is a before and an
  after, so a mind that works serially is a mind that has time in it.** *Time is not
  something the serial side observes; it is what serialising feels like from the inside.*
  **The parallel side has no need of it**, which is why an intuition has no steps and cannot
  be replayed.
- **The hemisphere reading is marked as interpretation, not citation.** It is a live argument
  and the project uses it as *a shape to build with* — filed as a decision about what the
  game is made of, and **not evidence of anything about brains.**

### Why two beats one, which is the whole point

- **Neither perspective is correct and neither supervises.** CONTENT sees the particulars in
  order with its working shown, and cannot see what any of it is for; CONTEXT sees what the
  whole is for, at once, and cannot see whether it is so. ***Each one's blind spot is the
  other's subject.***
- **Not a compromise and not an average**: a claim that survives being read both ways has
  been checked in the one way each side cannot check itself. ***Bias is what you get when one
  side audits its own output.***
- **4.18a is this built**, and Scorn's crime becomes sayable in one line: **he weighted the
  stage whose only job is to hold the two against each other**, so the disagreement kept
  happening and stopped being able to resolve. *A clarifier that can only agree is a mind
  with the callosum cut and one side told to write the report.*

### Where the game already is this

- **Invariant 3 restated as the strongest form of the claim**: the chart is byte-identical
  across editions, so **the two carts are two points of view on one world and neither gets
  its own physics.**
- The **two Index entries** — one daemon, two honest records, no match: *the callosum problem
  as a collectible.* **LOGIC fails against CONTEXT and CONTEXT does not beat CONTENT** —
  neither input wins, which is the half people forget. **SUSPENDED** is the only state that
  takes one half offline and leaves the other running. **CODEMUSAI against CAREMUSAI.**
- ***None of it is ever said.*** The player meets two cartridges that will not reconcile, two
  entries that disagree, a chart where neither half wins, and a tile that reads `SUS`.

---

## v11.112 — 2026-09-09

### 2.7 — the ROUTINES pass, written down before a single name is proposed

- **72 species carry our names and 0 of 356 moves do.** *The largest unstarted surface in the
  project* — and the reason to write this first is that **half the decisions turn out to have
  been made already, by the chart.**
- **The loop closes four times and nobody planned it.** Mapping every state-inflicting move
  onto its type: **CORRUPT owns LEAKING and CASCADING, ENTROPY owns OVERHEATED, FROZEN owns
  HUNG**, and nothing else inflicts those four. *Vanilla built poison, burn and freeze as
  single-type states and 1.6's renames landed on the same alignment* — **the type, the state
  and the item were already one vocabulary closing on itself**, and nobody had noticed.
  ENTROPY → OVERHEATED is 2.6's clause for ENTROPY word for word.

### SUSPENDED wants two owners, and that is the finding

- **The question asked was which type owns it. Two do**, and *suspending each produces a
  different, nameable failure.* **Suspend CONTEXT and the literal keeps running: the hamster
  wheel — every particular attended to, nothing read for what it is for.** **Suspend CONTENT
  and the frame keeps running with nothing under it: intuition that cannot be argued with.**
- ***Those are the two inputs to a judgement — the thing as given, and the frame it is read
  in — and LOGIC is the operation between them.*** Suspend either and the operation runs on
  one leg, which is why the failures are opposite and both are recognisable.
- **It also explains why SUSPENDED is the one state 1.6 insists is temporary.** *Losing the
  frame and losing contact with the literal are not damage, they are being unscheduled* —
  and **RESUME is the exact inverse, which it always was.**
- **Same claim the project has already made twice**: Penphin's two hemispheres, and
  CODEMUSAI against CAREMUSAI as an evolution branch. **4.18a's clarifier is the chronic
  form** — *Scorn did not suspend the frame, he weighted the stage that holds the two
  against each other.* A CONTEXT suspension is the acute version.
- ***None of it is ever said.*** In the game a suspended daemon is `SUS` on a slate tile.
  **The player meets the two failures as two matchups and is never told they are a pair.**

### The naming rule, and what the pass costs

- ***"PACKET should do a move a packet would do" is right, and naming the move after the
  creature is not how you get there.*** `TACKLE` is learned by **25** of our 72. But
  **WING ATTACK's eight learners are all things that deliver something somewhere** — the
  learner set is coherent *because the chart was built from meaning.*
- **So: name a ROUTINE for the operation its TYPE performs, never for what any creature is.**
  The resonance is a consequence, and **a name that only works on its most famous learner is
  wrong.**
- **175 of 356 moves are reachable** by the renamed daemons — the pass is half the size it
  looked. The budget is **12 characters**, which vanilla already runs to.
- ***Forty-five percent of them are CONTENT*** — 79 of 175 — **the one type whose clause is
  "the thing itself, with nothing read into it."** *Every other type hands you a verb.*
  Logged Open, and it is **the register to settle first.**

---

## v11.111 — 2026-09-09

### `docs/items.html` — *The Bag*, and a document that cannot drift

- **A new sheet, generated rather than written.** `tools/gbaitems.py` **diffs our
  `items.json` against upstream's**, exactly as `port_names.py` does, so the rename list is
  *derived* — **36 items** — and a name invented in the tool cannot exist. **The shipped
  description is quoted out of the same json**, and the three-letter codes are read back out
  of `strings.c` and **asserted** against the page's own table.
- **What it holds:** the eight states with their codes and tile colours, the ten operations
  that end one, the box ladder, the four inputs, the key items, the name budget — and
  **the argument for each word**, which is the one part that is not derivable and lives in
  the tool keyed by `itemId`. *An item renamed without an entry is reported, not rendered
  blank.*
- **`build-pdf.sh` grew an html branch.** `./docs/build-pdf.sh items.html` prints a styled
  page as-is, no pandoc — which is how `type-chart.pdf` was always cut, and it was not
  written down.

### The type chart stopped carrying two tables it kept getting wrong

- ***It still said `CSC`, `HOT` and `INTERRUPT`*** long after the build shipped **`CAS`,
  `OVR` and `PREEMPT`** — a second copy of data that changes, maintained by hand.
  **Both sections now point at *The Bag*.**
- **What stayed is the one thing that is genuinely about the chart**: OVERHEATED is dealt by
  ENTROPY, whose clause is *noise and heat*; and **FROZEN could not be reused for the frozen
  state because it is a type name** — the constraint that produced `HUNG`.

### The STREAM, written down in the two places it was missing

- **9.16 gained a schedule** — every show, shipped and queued, each with its gate. *Seven
  vanilla-derived, nine ours, seven more written down for later*: the INDEX (4.2's complaint
  said as a tutorial), what a CHECKPOINT costs, the four inputs, MP, held items, **why a
  traded daemon disobeys** (obedience is keyed to the MARKS you hold, which is 5's argument
  arriving as a mechanic), and what the REPO is for. ***The gates are the discipline*** — a
  show offered before the thing it explains is a show about nothing.
- **The harness was told.** `game.txt` gained the item row and a paragraph: the STREAM is a
  menu of lessons, *the list grows one show per MARK*, and the early ones cover things the
  prompt does not.

---

## v11.110 — 2026-09-09

### The STREAM — 9.16, and what a lesson actually costs

- **`TEACHY TV` → `STREAM`.** *A stream is a broadcast and a stream is a sequence you read
  from as it arrives* — works twice, first try. **`MACHINE STREAM` was measured out of the
  running before taste got a vote**: `ITEM_NAME_LENGTH` is 14, so an item name is thirteen
  characters, and that name is fourteen. `TUTOR STREAM` fits and stays available.
- **The animation is not art, and that is the finding.** *There are no frames anywhere in
  this system.* A show is a **nineteen-command cutscene**, a **scripted hand**
  (`{cursorPos, delay}` moving the cursor through a **real battle**), and **voiceover text
  hooked to battle-controller events**. ***All four battle shows run the byte-identical
  nineteen commands*** — they differ in two strings, one party table and where the fake
  cursor goes. **Nobody ever authored a second animation and the system has no way to.**
- **So a slideshow is possible and is the expensive axis.** A still is a full 256×160
  background, and BG0–BG3 are already spent. *A new cutscene command is twelve lines of C.*
- **`sTalkScript` is the vanilla cutscene with the hand-off deleted** — fifteen commands, no
  battle, no bag, no party table. **A talk show costs two strings and a table row, under a
  kilobyte**, which is the unit the new lessons are built from. *A concept is not a button
  press, and a fake cursor demonstrating **representation** would be a lie about the lesson.*
- **The budget, measured:** **7.27 MB of ROM free** in two runs; a lesson is 600–950 bytes;
  all six vanilla shows together are 4,913. ***ROM is not the constraint.*** **EWRAM is —
  99.58% full, 1,104 bytes left** — so the menu is built into the heap block and costs
  nothing there. A menu label has 168px; vanilla's longest is 146.

### Nine new shows, and the mark is the gate

- **`Where do my daemons go?`** answers a question the game had never answered: *you **bind**
  a daemon with a **BOX**, and the box **hosts** it.* **"A hosted DAEMON is running. It is
  just not running here."**
- **Eight more, one per MARK**, each teaching its mark's concept **as a thing to do**:
  read the summary page (SLATE), there is no big fight (SLOPE), name three things before you
  press anything (SENSE), the TUTOR lost to a child on a route he had never walked (FIT),
  *"every DAEMON you outscore leaves a little of itself in yours"* (SKEW), the menu you
  opened decided what you were allowed to think of (FRAME), a plan that only works on the
  best roll is not a plan (HEAT), a THRASHING daemon obeys in the wrong direction (TRUE).
- ***Not one names its concept.*** The menu says `About the SKEW MARK.`, never "bias" —
  **5.2 named the marks precisely so the concept would not have to be**, and this is the
  first system to spend that.
- **The gate is `FlagGet(FLAG_BADGE01_GET + n)`**, so the list grows as the player is
  certified. *Vanilla already gated its two bag shows on the TM CASE*, so one filter
  replaced both rules.
- **Nine vanilla flags, `0x4A7`–`0x4AF`, are declared and referenced nowhere** — exactly one
  per talk show. The flag is set when a show is chosen, so the host reports only the *other*
  unseen shows. **The overworld marker is Open.**

### The vocabulary the shows were still using

- **`POKé BOX` → `USERBOX`.** *The accented prefix again* — fifth tool it has hidden from.
- **`move` → `ROUTINE`** in six lesson lines, `TEACHY TV` → `STREAM` in three, and two menu
  labels reworded.
- **The harness had two stale item names.** `mappings.json` said **`INTERRUPT`** for ICE HEAL
  and **`CLARIFIER`** for item 349; both were renamed in the game and never re-ported.
  `game.txt` said the same two, in the orientation table and three times in the opening
  sequence — ***so the agent has been told to look for an item that no longer exists.***
  Regenerated, and the table gained a row for the three-letter status tiles.

---

## v11.109 — 2026-09-09

### The badges got their colour, the states got a tile, and the museum got a name

- **9.15 is new.** `graphics/interface/pokemon_types.pal` had been vanilla since the port —
  the Index drew `CONTNT` on Normal's tan and `VECTOR` on Flying's pale cyan, so **9.4's
  colours had never once reached the screen where the player reads a type as a word.**
  The sheet has **thirteen usable entries for eighteen types**, so the badges were
  *re-indexed* rather than recoloured, and **five rare types borrow a slot from a common one
  — chosen so that no daemon in the game has both.** Magnemite, Articuno, Kingdra, Jynx and
  Paras were each checked by hand.
- **9.4's dark-step rule is narrowed, not reversed.** It measured white text on the base
  hues and found eleven of fifteen fail. **The badge glyph is white text *with a generated
  shadow*** (9.12), which measures 5.5:1 on the worst plate — *and thirteen dark steps are
  not thirteen distinguishable colours.* The rule stands everywhere the glyph has no shadow.
- **The six states have a tile.** `status_icons.png` still said PSN, PAR, SLP, FRZ, BRN;
  it now says **LEK THR SUS OVR HNG**, plus **HLT** for fainting, each on a colour that
  keeps vanilla's hue anchor and moves into 9.4's register. **Six letters had to be drawn**
  — the sheet's own face had no `E H U G O V`.
- **PKRS moved off LEAKING's palette slot.** It shared PSN's in vanilla, so it would have
  inherited the leak colour — *a beneficial condition wearing the leak colour is a lie the
  tile tells for free.* Its **name** is still vanilla and is now logged Open.
- **`gText_Toxic` holds `CAS`.** Vanilla's own unreferenced string was the one place a
  CASCADING code could go without adding a symbol to a build whose compiler reports failure
  as a warning and then a bare `Error 1`.

### The Cognitive Clarifier, written down

- **4.18a is new**, at the request of the person who built one. 4.18 leans on *"many frames
  polled and resolved"* for a whole crime and never unpacks it. **Two threads — reason and
  feeling, the second weighted by the system's own affective state — resolved by a short
  perspective pass that knows who it is for; then reception produces a BELIEF, which is
  stored, can be read, can be challenged, and is fed back in.**
- **The token budget is lopsided on purpose**: the threads are allowed to be long, the
  resolution is deliberately short. *Concision is a courtesy, not a compression.*
- **It makes Scorn's crime worse.** He touched neither thread — **he weighted the one stage
  whose only job is to hold two things in tension**, so the machine kept generating the
  contradiction and stopped being able to resolve it honestly. **"IMPROVE RESPONSE
  CONSISTENCY" is exactly true**, and the sleep explains itself: *a clarifier whose beliefs
  all confirm each other has no reception signal left to learn from.*

### The ERRATA — 4.32, and the proposal that needed one turn

- **`SLATE MUSEUM OF RECORD` → `SLATE MUSEUM OF ERRATA`.** *An erratum is a published list of
  what an edition got wrong* — **a museum of dead hardware, a legacy mind, and the thesis, in
  one word nobody has to explain.** One word on one sign.
- **The museum was not emptied, because three exhibits were already teaching distortions and
  nobody had noticed** — *"most of what was built is gone"*, *"I do not see how"*, *"we all
  saw the same picture at the same moment."* **So the change is labels, not contents**, and
  the OLD CORE handoff is untouched.
- **The upstairs exhibit is named for the first time: `KNOWN FAULTS`.** Cards take a fixed
  shape — **object, provenance, `KNOWN FAULT:` and the error described as an engineering
  failure.** *The fault is always the machine's and never the reader's*, which is craft rule
  3 doing the work. **No distortion is ever named.**
- **CC-7 is alluded to and not explained.** The exhibit scientist: *a researcher from
  Blanche wrote the cards, and she is collecting them — "into a module, she said. As though a
  fault were a part."* **The player has carried a `CC-7` since minute fifteen.**

### 1.6 amended, and 1.7 is new

- **ICE HEAL is `PREEMPT`, not `INTERRUPT`.** *The word was assigned twice, six weeks apart*
  — POKé FLUTE keeps it. **Preemption is the scheduler taking control back from a task that
  will not yield**, which is HUNG exactly. **The narrower word was the more accurate one.**
- **Item descriptions now teach the term and state the effect**, in that order, seven of them
  rewritten. *The player who knows the word gets a nod; the player who does not gets a
  definition and never notices being taught.*
- **1.7 answers PORT / TERMINAL / SSH.** **TERMINAL is backwards** — a terminal is the client,
  and a box is the far end. **`PC` → `PORT` is right and is logged Open**, because a
  half-rename is the failure this project has already had twice. **SSH is declined** as the
  first product initialism in the lexicon; *the idea it names is kept as prose.*
- **Security vocabulary: yes, narrowly.** **AUTHORISED, SIGNED, COUNTERSIGNED, REVOKED, KEY**
  are already the game's words and already on-thesis, because **4.18's crime is an
  access-control story told in paperwork.** **EXPLOIT, PAYLOAD, INJECTION, BREACH are
  declined** — *they would make Scorn a hacker, and the horror is that he filled out a form.*

---

## v11.108 — 2026-09-08

### The IVs, and the move that reads them

- **2.3 gains a third thing Kanto already encoded** — this one in arithmetic rather than a
  matchup, and found in the GBA engine rather than the chart. Gen 3 rolls six **IVs** per
  daemon, 0–31, once, never changing and never shown. *An IV is definitionally the part of a
  creature that is not content* — no field, no entry, nothing to fill in — which is **4.2's
  complaint about the Index expressed as a data type the engine already ships**, and 6's
  humors as arithmetic.
- **`HIDDEN POWER` derives its type from the IVs, and its pool excludes `TYPE_NORMAL`.**
  Verified in `battle_script_commands.c`: *the latent power in every daemon is never
  **CONTENT***. The type comes from the **lowest bit** of each IV and the power from the
  second — so what kind of hidden power a daemon has is set by the noise floor of its innate
  variation. Nobody designed that.
- **Renamed `PRIOR`.** A Bayesian prior is what a system believes before it has seen any
  evidence; it also just means what came before. **Works twice**, which is BIND's test.
  Description rewritten to name the mechanic and not the thesis.
- **The IVs stay invisible, deliberately.** FireRed ships no IV judge and none gets added:
  a readout of the one quantity the Index cannot hold would undo 4.2.

---

## v11.106 — 2026-09-07

### The six states, the items that undo them, and two menu words

- **1.6 replaces the last bodily metaphors in the game.** 1.4 shipped `HALTED` for fainting
  and stopped, leaving one process word and six about bodies. Each state is now the ordinary
  computing word for what the mechanic does: **LEAKING** (a memory leak is the only thing in
  computing that costs a fixed slice per tick), **CASCADING**, **SUSPENDED**, **THROTTLED**
  (a speed cap that intermittently stalls — both halves of paralysis in one word),
  **OVERHEATED**, **HUNG**, **THRASHING**.
- **FROZEN could not be reused for freeze** — it is a type name, and 2.6 had just spent effort
  establishing that type names carry meaning.
- **The items are operations rather than medicine.** PATCH, RESUME, PRIORITY, COOLANT,
  INTERRUPT, ROLLBACK, SNAPSHOT, **RESTART / REBOOT**. *The last pair arrives with its ladder
  already built: the bigger item is the bigger operation, which is exactly what REVIVE and
  MAX REVIVE are.* `PRIORITY` is the weakest of the ten on the works-twice test.
- **INVOKE, and the port unlocked it.** 1.4 wanted the word — *"you `bind()` a daimon and you
  invoke it"* — and refused it on width: six characters where the Game Boy's left column fits
  five. **The GBA menu is pixel-addressed and already ships DAEMON in that column; INVOKE
  measures 36px, exactly DAEMON's width.** The objection was hardware and the hardware changed.
- **Moves become ROUTINES** — a subroutine and a habit, which ties the list to 4.29's ladder,
  where a daemon is read by *what it does unasked*. METHOD was the runner-up and lost for being
  the more thematic word in a slot that is a plain label read a thousand times.
- **The rename is one string.** Eleven player-visible strings contain `MOVE` and most are the
  **verb** — `MOVE ITEMS`, `MOVE TO BAG`, `{DPAD_ANY}MOVE`. *Same trap as “catchy tune.”*
  `KNOWN MOVES` → `KNOWN ROUTINES`, measured at 84px against a 100px window.
- **Order is the whole trick, and it is recorded.** `POISON` is a **type**, `poisoned` is a
  **state**, so items substitute first, then type words, then bare states — reversing it turns
  the CORRUPT type back into a LEAKING type. And **an escape is two characters whose first is a
  letter**: `\nPoisoned` hides from `\b`, which has now caught four tools here, so
  `port_states.py` matches a flattened copy.
- **Built and verified**: 51 battle messages, 55 move descriptions, 13 help-system lines, 7 in
  teachy_tv, 10 items. Two lines pushed past the 196px box were rewritten rather than truncated.
  Read back out of the ROM through `gbastr`; the tool reports nothing on a second run.
- *Deliberately not done:* **`move` → `routine` inside prose** — "moves on own" and "can't move"
  are verbs while "move type" is a noun, and that separation is the move pass's job.

---

## v11.105 — 2026-09-07

### The one-clause test, and the two names that fail it

- **2.6 adds an instrument, not a verdict.** *For each type, write ONE clause a
  non-specialist understands; walk every relation it is in, attacking and defending;
  mark PREDICTS, SILENT or OPPOSITE.* **Three predictions and no net contradictions is
  a pass.** It sits beside BIND's *does it work twice?* — and a type that fails it has a
  **naming** problem, not a chart-position problem, since 2.3's chart is inherited and
  not up for renegotiation.
- **Run against all 83 relations: thirteen pass, two fail.** The question behind it was
  whether a player can *generalise* the chart or only memorise it — vanilla's sprites
  label the type **and** import a causal model, and 9.4's hue only does the first.
- **The thesis is safe.** **CONTEXT scores 8 / 8, LOGIC 7 / 12.** *The most important
  relation in the game — rules bounce off framing — is also one of the most
  self-explaining.* That was not guaranteed.
- **The failures are not the abstract types.** *CONTEXT and EMERGENT are the two most
  abstract concepts in the set and score perfectly.* **The two that fail are the two whose
  vanilla names were the most physical — ROCK and FLYING.** Two words, not a systemic fault.
- **`LEGACY` is 0 / 14** — in more relations than any type but GROWTH and ENTROPY, and
  predicts none. *ROCK bought smothering fire, blocking ice, swatting things from the air,
  erosion and roots; LEGACY spends all of it and returns nothing.*
- **`VECTOR` is 1 / 12 and contradicts one.** STRATUM hits it ×0 and *nothing about
  "direction in a space" explains why the ground cannot reach it.* **FLYING made that
  immunity free; VECTOR makes it look like a bug.** A silent clause costs a lookup; a
  contradicting one costs trust in the chart.
- **The fix is a string change.** `gTypeNames` is a plain table at `TYPE_NAME_LENGTH 8`,
  so **invariant 6's expensive half does not apply.** Candidates recorded and left **open**:
  `SILICON` or `RUST` for LEGACY, `ABSTRACT` for VECTOR. *2.2's names were chosen as a
  complete set and 2.6 is not entitled to overrule two of them on its own evidence.*
- **SWARM passes at 4 / 13**, and 2.5 already records it as mechanically weak for unrelated
  reasons. *Two independent problems pointing at one type.*
- **What the test does not answer, stated in the section:** it measures the **names**. The
  channel that actually teaches is **move names**, read hundreds of times to a sprite's
  handful — held with 2.5 and the nineteen gym lines waiting on 5.

---

## v11.104 — 2026-09-06

### The second external review, decided

- **8.6 closes: `COLOUR IS CONTEXT.`** *The world has it. Records do not. A daemon has as
  much of it as it has accumulated.* The question had been argued as art direction for two
  days; **it is a palette flag.** `gGlobalFieldTintMode` already exists in the engine — it
  is how FireRed's Quest Log replays in sepia — and it tints tilesets *and* object palettes.
  **A GBA sprite is indices; colour is a 32-byte table.** Grey town, grey Index and full
  colour are the same art. **The whole system costs no new art.**
- **A value ladder, not five greys.** Blanche warm white → Slate blue-grey → **Halftone true
  grey** → Quicksilver ash → Umbra near-black. *7.4 already does this for music: hue sets
  key, value sets register.* **Two grey towns halves Halftone**, so only Halftone is drained
  and the rest are graded — grass stays grass.
- **Saturation is friendship.** A daemon at low friendship is nearly grey with a hint of its
  type; at maximum it is the full 9.4 ramp. **Not evolution stage** — *"more colour on the
  final form" says power = colour*, and 8.2's final stages are the paradigms' **failures**.
  **Corpus classes get friendship 0**, so every daemon they field is visibly context-free —
  and **the people stay in colour**, because a grey workforce is the sneer 3.1 guards
  against. *The Index shows a daemon grey either way: the player can see what the record
  cannot.*
- **The post-game colour item is rejected.** It makes colour a reward, and a reward is a
  metric — Scorn's kind of thing. It is also **a Cognitive Clarifier for the player**.
- **`LOGIC / INTUITION` → `REASON / INSTINCT`.** `LOGIC` is the FIGHTING rename, and 2.3
  calls *"LOGIC resisted by CONTEXT"* the thesis — so one option was named after a column of
  the chart that **the chart says loses**, which is what 9.10's *"neither is the careful
  one"* forbids.
- **HOLT is an otter.** A holt is specifically an otter's den, so the name chose the species
  before anyone asked — and an otter is at home in two elements, which is the man who held
  two frames in one address. Found independently twice.
- **0.1 gains the form: *a fable with its last line removed*.** A fable ends with the moral;
  craft rule 1 is the refusal of that sentence. That is what every craft rule is **for**.
- **8.2a defers the Sevii Islands**, with an exact condition: **name nothing there.** The
  moment an island is named the decision is made by accident.

---

## v11.103 — 2026-09-06

### The slice is at 91%

- **37 blocks across two passes.** `208 prose blocks: 191 ours (91%), 11 vanilla reworded,
  6 untouched`. It was **9%** two days ago.
- **The status explainers finally moved**, and the fix was to use our own vocabulary rather
  than paraphrase vanilla's. *"Asleep, nothing runs. The battle ending does not wake it.
  AWAKENING is the interrupt."* — `INTERRUPT` is what 1.4 already renamed the Poké Flute to,
  so the item and the state now share a word. The other four end on the same line, **"Carried
  out of the battle with it,"** which is what a status condition *is*.
- **The spam e-mail became a summons.** Vanilla's is an advert; ours is the REVIEW BOARD
  sitting again, and one line at the bottom: *"CRYSTAL CLEAR: your attendance is again
  requested."* **Again.** She has not gone, and 4.20 is why.
- **Al's complaint got shorter and worse.** *"I have bound more. I was faster. Give me one
  job. One."* — no exclamation anywhere in it.
- **MOM stopped quoting the television.** *"You have that look."* And the two variants split
  on what CRYSTAL did rather than on the player: *she waited a while* / *she did not wait
  long*, which is 9.10's LOGIC and INTUITION seen from the doorway.
- **Callow's sign stopped rhyming with vanilla's.** *Evergreen And Unripe* scored high
  against *The Eternally Green Paradise* — the same joke, differently worded. It reads
  **"Green All Year. Untried All Year."** now.

---

## v11.102 — 2026-09-06

### DAISY is VERA CLEAR

- **2609 settled**, the last vanilla name in the family. One vocabulary entry, 22 dialogue
  blocks, 8 files.
- **The Clears are all kinds of clear** — *crystal* clear, *all* clear, *type* clear — and
  hers is **very** clear. Which is 2569's whole point: *"Gran reads them with an
  instrument. I just look."* Crystal needs equipment; Vera does not.
- **`IRIS CLEAR` was the prettiest and was rejected.** Crystal is a lens and an iris is an
  aperture — grandmother the instrument, granddaughter the eye — but it is not a pun and
  the other three are, so it breaks the device at the fourth member. **`CASH CLEAR`** was
  the exact pun and points at *storage*, the one thing she is not about.
- *Cost recorded:* CRYSTAL and VERA read a generation older than AL and TY, which is
  backwards.

---

## v11.101 — 2026-09-06

### The slice metric measures prose now, and it is at 74%

- **`gbaslice` exempts functional blocks.** Receipts, capacity refusals, route signs,
  cries, and anything under 45 characters — **106 of the 314**. Their shape is fixed by the
  job they do, and forcing them under the 0.5 threshold would mean writing them *worse* to
  satisfy a number.
- **The number it reports is honest now:** `208 prose blocks: 155 ours (74%), 47 vanilla
  reworded, 6 untouched`. The old headline said 62% and implied 100 blocks of unwritten
  prose; there are **47**.
- **The tool's own claim was the giveaway.** Its docstring says *"above it, vanilla is still
  doing the talking with our nouns in its mouth"* — true of dialogue, false of
  `{PLAYER} received the POTION`. It found the school's rewritten status explainers guilty
  because a status explainer must say what the condition does, that it persists, and what
  cures it, in that order.

---

## v11.100 — 2026-09-06

### 62%, and what the remaining number actually measures

- **18 blocks rewritten** — Al's short lab lines, Crystal's two, and the Callow and Slate
  blocks where the first sentence had been rewritten and vanilla's second sentence had
  survived. **The slice reaches 62%.**
- **Al's opening scene got shorter and colder.** *"Oh. It is you. She is not here."* /
  *"Gran. I have been standing here."* / *"Gran. And me."* — two words where vanilla had
  an exclamation. He is not louder than vanilla's rival; he is **more clipped**, which is
  the same character the Route 22 rewrite gave: someone who does not concede and does not
  elaborate.
- **Crystal counts.** *"There is one for you as well, {RIVAL}. I counted."*

### The metric is structural, not authorial, and that matters

- **`gbaslice` scored the school's status explainers as vanilla after they were rewritten.**
  *"A sleeping daemon does not act"* shares almost no wording with *"A POKéMON can't attack
  if it's asleep"*, and still lands above 0.5 — because a status explainer must say what the
  condition does, that it persists, and what cures it, **in that order**. Any correct version
  scores high.
- **So the remaining 100 is not 100 blocks of unwritten prose.** Roughly half is functional:
  receipts, plaques, route signs, and mechanical explainers whose structure is fixed by what
  they have to convey. The tool's docstring says *"above it, vanilla is still doing the
  talking with our nouns in its mouth"* — true of dialogue, **not true of a receipt**.

---

## v11.99 — 2026-09-06

### The man in the gym is Scorn

- **2712 settled.** `GIOVANNI → SCORN`, one vocabulary entry, propagated to five files.
- **The writing half-answered it and the art answered it again.** He already said *"the
  machine chose what I weighted it to choose"* — 4.18's crime, stated by him — and since
  this morning's fable pass the sprite in that slot is **Scorn's face**. The ROM was
  carrying his face, his confession, and another man's name on the statue.
- **The alternative was two different people weighting the same machine the same way**, a
  coincidence the story would have had to earn, and nothing earned it.
- **Callow's gym closes properly now.** Before: *"Nobody will tell me who runs this GYM. I
  have asked. They smile."* After: *"SCORN. He was running the GYM the whole time. I asked
  so many people."* The statue reads `LEADER: ?` until you beat him.
- **The trainer symbols stay** — `TRAINER_BOSS_GIOVANNI`, `TRAINER_PIC_LEADER_GIOVANNI`.
  Invariant 6: renaming constants is optional and expensive, and none of them is displayed.

---

## v11.98 — 2026-09-06

### The routes, the rival's two battles, and Slate's gym finished

- 17 blocks. **The slice reaches 58%**, and only 19 blocks are untouched.
- **Al's two Route 22 battles rewritten**, and the pair now reads as one person a year
  apart. Early, beaten: *"That was luck. It was."* — he says it twice because saying it
  once did not settle it. Late, beaten: *"No. I was not paying attention."* He has stopped
  blaming luck and started blaming himself, which is worse.
- **Route 1's ledges say something true about the shape of the game.** *"You can drop down
  them. You cannot climb back up. It is quicker going home than it is coming out."*
- **Slate's gym guide stopped being a hype man.** *"I do not battle. I watch. I can tell
  you how it goes."* — which is what that character has always actually been.

### Still open, and the writing has now half-answered it twice

- **GIOVANNI is not renamed** (2712), and Callow's gym statue says so in the ROM — under a
  sprite that has been **Scorn's face since this morning**. The gym guide already says
  *"Nobody will tell me who runs this GYM. I have asked. They smile."* and the leader
  already says *"the machine chose what I weighted it to choose"*, **which is Scorn's crime
  stated by him.** The two remaining untouched blocks in that room cannot be written until
  it is decided: either the man in the gym is Scorn, or two people weighted the same machine.

---

## v11.97 — 2026-09-06

### Blanche Town, and DRUM CORE

- **`DOME CORE → DRUM CORE`.** *Dome* had no hardware meaning — it was purely the shell
  vanilla drew. A **magnetic drum** is real storage and properly obsolete, so the three are
  now three technologies rather than two shapes and an age. **`HELIX` stays**, and it is
  better than it looks: **helical scan** is how VCRs and DAT drives wrote to tape.
  *`HEX` was considered and held* — it reads as **curse** before hexadecimal, which is the
  register `REVERSER` was just moved away from, and that reading is already spent.
- **The museum clerk stopped pricing children.** Vanilla said *"¥50 for a child's ticket"*;
  the rewrite trimmed the noun doing the disambiguating. It says **"¥50 to go in"**, which
  sidesteps the player's age rather than fixing a number to something the game keeps open.
- **Blanche Town written**, 17 blocks. **The slice reaches 55%.**
- **The sign pairs with Slate's.** `BLANCHE TOWN / Nothing Written Here Yet` against
  `SLATE CITY / A Surface That Takes A Mark` — the blank and the surface, two towns apart,
  and neither says why.
- **The grass is dangerous for a reason the game never repeats.** *"There are unbound
  daemons in the grass. A process will run wherever it can. Do not go out with nothing of
  your own."* That is 1.3 as a warning from someone who is only trying to be careful.
- **And the PC gets 4.20a's question thirty seconds into the game.** *"The PC holds them
  without running them. I have never worked out what that is like from the inside."*
  Crystal asks it once, idly, and nobody answers her. HOLT is the man who found out.
- **Crystal's late line is the one that costs.** *"You will go further than I did. I mean
  that kindly."* 4.20 is why she did not.

---

## v11.96 — 2026-09-06

### Deadstack had never been named, and the shops got written

- **Mt. Moon was still called Mt. Moon.** 3.2 named it **Deadstack** — *a mountain of dead
  hardware; fossils are legacy silicon* — and nothing implemented it. Every other landmark
  had been done: `VIRIDIAN_FOREST → THE UNDERTONE`, `SEAFOAM_ISLANDS → GLAUCOUS ISLES`,
  `POWER_PLANT → KEEPALIVE PLANT`, `VICTORY_ROAD → UMBRAL ASCENT`. This one was missed, and
  `port_names` could never have caught it, because it learns renames by **diffing our table
  against upstream** and this entry had never differed.
  *Found because the museum plaques written this morning say "recovered from Deadstack".*
- **Both spellings were in the ROM** — `MT. MOON` and `MT.MOON` — so `port_vocab` carries
  four forms and propagated to 11 files. Zero left.
- **The five remaining slice rooms written**, 16 blocks. **The slice reaches 53%.**
- **The trade-disobedience line was 1.3 waiting to be noticed.** Vanilla: an outsider
  *"may ignore an unskilled USER."* Ours: *"A traded daemon was bound by somebody else. It
  runs. Just not at your level."* That is the privilege ladder, in a house in Slate, said
  by someone complaining about their pet.
- **And the DAEMON CENTER got the line it needed.** *"A DAEMON CENTER restarts anything
  that HALTED. It comes back the way it went in."* Nobody remarks on it, and 4.20a is the
  man who **was** the thing in storage.
- **`NIDORAN♂` was still `NIDORAN♂`** in Slate's house — the ♂ had hidden it from the
  species rename. It is BRANCH.

---

## v11.95 — 2026-09-06

### The school teaches the chart, and does not understand it

- **The last of the four unwritten slice rooms.** 15 blocks, 0 ours → 9.
  **The slice reaches 50%.**
- **A school that explained the chart well would say the thesis.** 2.3 calls
  `LOGIC resisted by CONTEXT ×½` *"The thesis. Free."* — so a teacher who explains *why*
  framing resists rules hands the player the argument in the second town. **So the school
  teaches the table flat, with the reasons omitted.** That is what schools do with a
  table; it characterises the institution the way the minutes and the requisition do; and
  it *is* Callow, where nothing has been tested.
- **Vanilla gave us the first line for free.** *"I'm trying to memorize all my notes"*
  becomes *"I have to have the table by Friday. I do not have to understand it. I have to
  have it."* She names the distinction the whole game runs on and does not hear herself.
- **The notebook's four pages are the chart.** Fifteen kinds; some land twice as hard;
  some **cannot reach at all** — *"CONTENT cannot touch LATENT. Neither can LOGIC. Nothing
  either one does will register."* And then page four: *"The eight benchmarks test whether
  you know the table… That is the whole of the path."*
- **"Learn the table. It does not change."** True — 8.4 makes the chart byte-identical
  across editions. And quietly not the whole truth, because 4058 has each edition's player
  building a **different intuition** about what is strong from the encounter tables.
- **The blackboard keeps the status conditions**, reworded. Five slots, and a player
  actually needs to know what a burn does.
- **`ELITE FOUR → REVIEW BOARD`.** 8.6 has called them that since it was written — four
  ancient people insisting emotions are coloured fluids, in the one room with colour. The
  notebook had to name them, so `port_vocab` now carries the phrase and it propagated to
  every League room and the quest log.

---

## v11.94 — 2026-09-06

### Callow City, where the first gym you reach is the last one you open

- **19 blocks, 2 ours → 13, and nothing untouched.** The slice moves 44% → **47%**.
- **The sign carries both readings 3.1 asks for:** `CALLOW CITY / Evergreen And Unripe` —
  the colour and the feeling, in four words. Vanilla's *Eternally Green Paradise* was
  ironic; ours is literal, which is harder to shrug off.
- **CRAWLER and SCRAPER stopped being about poison.** *"CRAWLER only reads. SCRAPER takes
  what it finds."* Those are what the two words mean, and the distinction was sitting in
  the names untranslated.
- **The locked gym says the right thing.** *"This GYM has never once been open. Nobody here
  can tell me who holds it."* — **holds**, which is what a lock is for, and 5 makes
  Benchmark 8 Scorn: he set the bar the player is measured against all game and the door
  in front of it never opens.
- **The boxes get noticed once, plainly.** *"USERBOXes at your waist. So you have something
  running."* — 1.3 without saying 1.3. And *"People forget it was ever hard"*, which is
  HOLT's invention being taken for granted by a stranger who will never know his name.
- **Two more leftovers cleared.** `"a INDEX"` had been ungrammatical since the rename, and
  `POWER POINTs` was still the vanilla expansion of an abbreviation that now reads **MP** —
  it says **MANA** now, which is what the lab already called it.

---

## v11.93 — 2026-09-06

### Slate City, and two idioms `catch → bind` had broken

- **Slate City written**, 26 blocks, 1 ours → 14. **The slice moves 40% → 44%.**
- **The signs carry 3.1's own reading of the name.** `SLATE CITY / A Surface That Takes A
  Mark` — a slate is a writing surface, which is Benchmark 1's Representation lesson
  sitting inside the town name. And `MUSEUM OF SCIENCE → MUSEUM OF RECORD`, which is 0.2's
  reproduction throughline without saying it.
- **CAIRN's gym sign says what a cairn is for:** *He Stacks Stones So The Next One Finds
  The Way.* ROCK is LEGACY, and that is what a legacy is.
- **The DREAM EATER tutor stopped being about a dream.** *"I dreamt something was reading
  me while I slept. It took what it found."* Then, once it is handed over: **"Someone else
  can hold it."**
- **`catch → bind` had broken two idioms and nobody had looked.** 1.1 renamed the capture
  verb; the substitution does not know the difference between capturing and *catching up*.
  `"we can bind up later"` and `"grass bound up in my spokes"` were both in the ROM. Fixed,
  and `port_vocab.py` now holds a list of phrases where *catch* is not the capture verb and
  substitutes them to themselves before the word map runs.
- **The item rename propagated itself.** `port_vocab` learned `OLD CORE` / `HELIX CORE` /
  `DOME CORE` from `items.json` and found three more places they are spelled out — the
  fossil-choice UI in `src/strings.c`, which the museum work had not touched.

---

## v11.92 — 2026-09-06

### Slate's museum, which was a one-line concept and 0 of 9 blocks

- **A natural history museum for manufactured things.** The curators talk about dead
  hardware the way palaeontologists talk about bones — as ancient life that *evolved* —
  and nobody ever says these things were made. 3.2 already had Deadstack as a mountain
  of dead hardware whose fossils are legacy silicon; this is where that gets presented
  as science.
- **The three revival items become one family.** `OLD AMBER → OLD CORE`,
  `HELIX FOSSIL → HELIX CORE`, `DOME FOSSIL → DOME CORE`. **Core memory is literally
  dead hardware** — ferrite rings threaded by hand on a wire grid — and a **core dump**
  preserves a process at the moment it stopped, which is precisely what amber does to an
  insect. *Resurrect a daemon from amber* becomes **restore a process from a dump**, an
  operation that actually exists. Vanilla had one amber and two unrelated fossils; ours
  has three preserved images, which is what they always were.
- **The man with the secret is the room.** Vanilla's crank thinks his amber holds DNA and
  his colleagues ignore him. Ours: *"This CORE is not empty. There is still something in
  it. I have said so for eleven years. My colleagues write it down and file it. They are
  very polite."* That is 4.20's shape — a person recorded rather than heard — and 4.20a is
  the man who **was** the thing in the box. Nothing points at it.
- **And the USERBOX is on exhibit**, in one line, in a list of three things:
  *"And a USERBOX, in the case by the stairs. Donated last year."* v11.86 said the rhyme
  should land on the exhibits rather than on the object in the player's hand. It does, and
  the player is wearing one.
- **The old man worked on one.** *"Though I worked on one of these. It is strange to see
  it labelled."* Obsolescence pointed at a person rather than at a machine.
- 18 blocks written, every line inside the 196px budget. **The slice moves 34% → 40%.**

---

## v11.91 — 2026-09-06

### The box has no seam, which 8 had already settled

- **A seam says container and 1.3 says host.** Section 8 stated it plainly of the carried
  box — *"no seam anywhere that would let it open"* — and the box art built two days ago
  contradicted it: a seam on the bag icons, a throw that parted, and an open state that
  spilled light from the gap. The seam was justified as *"where the battle frames part"*,
  which is exactly the container reading 1.3 exists to prevent.
- **Found by asking a production question.** The player carries the box on a strap, and
  *"how do they throw it?"* has no answer while the box is a thing that opens. It has an
  obvious one once it is not: **you throw a host at a daemon and it either runs there or
  it does not.** That is 1.3's catch rate, literal rather than figurative.
- **The open frame now wakes rather than parts.** Nothing opens, so the screen lights —
  a process starting on a host, which is the only event that was ever happening.
- **A vent line takes the seam's place** on the lower face: it says machine where the seam
  said lid, and still keeps the face from being a blank slab.

---

## v11.90 — 2026-09-06

### The people are drawn as a fable, and the rule has three clauses

- **The cast had drifted anthropomorphic without anyone choosing it** — the first Crystal
  prompt asked for visible fur and a full brush tail, and everything followed. Four
  treatments of the same character, generated and compared rather than argued.
- **The worry was never that they are animals.** Furry and fable are different traditions:
  in one the species is what the character *is*, in the other it is a **role**. Aesop's fox
  is a fox because the story needs cunning.
- **B failed informatively.** Fully human, Crystal became Professor Oak — at 64×96 the face
  is twelve pixels, a fox head reads there and "sharp-featured and russet-collared" does
  not. It also loses 1619's three foxes readable as family with zero text.
- **C is a mask.** Animal head on a human body survived on Crystal because a lab coat hides
  the join, and failed on a bug catcher in shorts. The Star Fox argument behind it was
  about *portraits* — full length that character has a tail, fur and paw hands.
- **D holds:** integrated animality, drawn plainly, head-to-body ratio carrying age. The
  third clause is the one that nearly broke Scorn — left unstated it defaults to Barks and
  everyone comes out cute, which 4.4 cannot afford.

---

## v11.89 — 2026-09-06

### FORAGER, and the last three pathology words

- **`BUG CATCHER` → `FORAGER`.** *Information Foraging Theory* (Pirolli & Card, 1999) is a
  real named result — people seek information the way animals forage for food, following
  **information scent** toward richer patches. It pays three times: a bug catcher
  literally forages, the theory is about cognition rather than insects, and the player
  meets this class on Route 2 with no map and no knowledge, **foraging**.
- **The three remaining maniacs.** `#MANIAC → ARCHIVIST` was decided for a reason that
  applied identically to the others and they were left standing: **a game whose central
  injustice is a woman recorded as unwell cannot have a trainer class called a maniac.**
  `BUG MANIAC → APIARIST` (keeps a colony where a FORAGER chases individuals, and bees
  are what the swarm literature is written about), `RUIN MANIAC → SALVAGER` (salvage is
  physical *and* data salvage, which is what this world's ruins are), `HEX MANIAC →
  REVERSER` (*hex* was hexadecimal waiting to be noticed, and reverse engineering reads
  intent back out of a compiled artifact — LATENT exactly).
- **REVERSER pays a third time.** It stops a class of young women being marked as occult
  and strange, which is craft rule 3 applied to the thing 4.20 is about.
- **Two dialogue lines said the class out loud** — Slate City and the Fame Checker both
  have Brock's line about hobbyists — and were carried with it.

---

## v11.88 — 2026-09-05

### Four tones was the Game Boy's answer, not ours

- **9.4 amended: type hue dominant, with a few accents.** Index 0 transparent, 1–5 the
  type ramp, 6–10 up to five accents at their own colour. The dominant hue is still the
  type, so the palette still reads as the chart — which is what 9.4 argued for. Colour
  carries the argument; it no longer has to do it alone.
- **The build showed the cost.** `gbasprite.py` touched only the 33 species we had drawn
  and left the other 118 as vanilla art at twelve colours — so pointing the intro at one
  of *ours* made it **poorer**, a four-tone bird beside a full-colour professor. Two art
  systems side by side, which nobody designed.
- **This one could not wait on 8.6.** The vanilla sprites are Nintendo's and every one of
  the 151 has to become ours; the redraw is the first instalment of that answer, so the
  answer had to exist first.
- **The art stays type-agnostic** — body in neutral greys, accents saturated — so one
  drawing is right whatever the type is. An accent landing too near the type's own hue
  gets shifted off it, because a red eye on a VECTOR daemon is no eye at all.

---

## v11.87 — 2026-09-05

### Grey was a medium; it would now be a filter

- **8.6 and the build have disagreed for three days, and it is not an oversight.** 9.4
  already excepted the daemons — colour carries the argument — and the character art
  followed. The section now says so, and says why porting 8.6 literally would not fix
  it: on a DMG grey was *the medium* and the player registered no absence, which is
  exactly what argument 1 runs on. Desaturating a machine that can do colour makes grey
  **conspicuous**, and a player who notices attributes it to style rather than to their
  own perception filling a gap.
- **The inversion is recorded and not taken.** Colour as default, grey as what the game
  spends: Halftone becomes the one grey town in a coloured world and the Index shows its
  own loss — both *stronger* than the current reading. It costs Umbra's colour moment,
  PERSPECTIVE's flash, and argument 1 outright. **Left open on purpose**, to be settled
  when Umbra is a room you can stand in rather than in the abstract.
- **The last three balls in the opening.** `src/oak_speech.c` uses two different sprites
  and `pokeball.c` a third: `CreatePokeballSpriteToReleaseMon` takes the interface
  sheet, `CreateTradePokeballSprite` takes a separate 12-frame trade graphic, and
  `gOpenPokeballGfx` is the opened state. All three are boxes now.
- **A ball looks the same from every angle and a box does not**, which made the trade
  spin honest rather than harder: the front face narrows to an edge, the back comes
  round with no screen, and the height never changes.

---

## v11.86 — 2026-09-05

### The box got a screen, and the ladder started working

- **A container says the daemon is inside; a screen says it is running.** That is the
  distinction 1.3's rename exists to make, and nothing in the art had been carrying it.
  The box is now a compute unit with a small screen — and the crate that Gemini drew
  into Al's hand was wrong twice, since `genbox.py` had already banned cubes for saying
  *container*. Glass dissolves that objection rather than overruling it.
- **Privilege is pips on the glass** — USERBOX one, ROOTBOX four, GUESTBOX one dim.
  It replaces a vent-density ladder that **had never worked**: `overworld()` broke its
  loop at `y >= 11` before the third vent, so all four tiers rendered byte-identical
  while the decision log claimed the ladder was "a parameter, not four drawings."
- **The Index marker stops being a symbol.** Vanilla marks a caught creature with a
  picture of the thing that caught it. Ours lights the screen — a bound daemon is a
  process running on a host, and the marker now says that with no text.
- **The handheld reading, settled.** A grey box with a dark screen can read as a
  console. Feet, a small screen set high, no buttons and cubic proportions hold it off;
  the rhyme lands in **Slate's museum of dead hardware** instead, whose exhibits include
  dead boxes. The museum is 0 of 9 blocks written, so nothing had to be undone.
- **`tools/gbabox.py`** now draws all of it: five 24×24 bag icons with their palettes,
  five 16×48 throw sprites, the 16×16 box on the ground, and the 8×8 Index marker.
- **A second separate-palette trap, same shape as the trainers'.** Item icons take their
  colours from `graphics/items/icon_palettes/<name>.pal`, not from the PNG. Writing the
  picture alone leaves the new art wearing the old object's palette.

---

## v11.85 — 2026-09-04

### The thing in his hand is not a ball, and the prompt had to say so

- ***Gemini put a Poke Ball in Al's hand***, because everything it has ever seen in that pose is holding one. **The brief did not say otherwise, so it filled the gap with the most available meaning** — which is 0.4's own argument, performed by the tool
- **This project has BOXES.** 3.1's line is **USERBOX → ADMINBOX → SUPERBOX → ROOTBOX**, and `tools/gbabox.py` already drew one: *a pale cream crate with a dark rim and two bands across its face*, in `graphics/pokedex/caught_marker.png`
- The brief now describes it explicitly and says **"NOT a ball, NOT round, no button"** — *a negative instruction, because the positive one alone loses to the prior*

### And the picture is behind the word almost everywhere

- `gbabox.py`'s docstring called the Index marker *"the one place the old noun survives as a PICTURE rather than a word."* **It is not one place.** There are **36 ball graphics still in the tree** — every item icon, the party menu, two battle transitions, the trade and credits screens, `interface/ball_open.png`
- ***The vocabulary pass can only reach words.*** **BOX is written everywhere and drawn almost nowhere**, and a player is told BOX while being shown a ball for forty hours

## v11.84 — 2026-09-04

### Ty needs no sprite, and that is the point

- **4.3**: ***"TY P. CLEAR, printed, never spoken."*** He is in the institution's register, buried in the Quicksilver ruins as a leitmotif, and **confirmed by one line at Brazen** — *never in a room*
- ***Giving him a face would spend the device.*** He is the man who is in the record and not in the room, which is SENTINEL's CONTEXT entry inverted

### Al needs four, in two formats

| | | |
|---|---|---|
| `oak_speech/rival/pic.png` | **64x96** | the intro portrait |
| `rival_early_front_pic` | 64x64 | first battles |
| `rival_late_front_pic` | 64x64 | later battles |
| `champion_rival_front_pic` | 64x64 | the last fight |

- **The brief keeps his clothes**: dark olive-grey shirt, purple-mauve trousers, spiky orange-blond head fur. ***Crystal's sprite worked because it kept the professor's purple shirt and extended hand*** — the swap read as *the same shot of a different person*, and Al gets the same treatment
- **10 puts him between**: Crystal golden-amber, Ty darker, **Al somewhere between** — so a mid-amber fox with *Crystal's ear and muzzle geometry*, because **the family resemblance is what has to read, not the species**
- `docs/gemini-prompts-al.txt`

### A stale line in the decision log

- ***It said the rival's formal name is TY CLEAR.*** **Ty is a different person** — Crystal's son and Al's father — and 4.3's detailed ruling is explicit: *"This is Al. What'll you call him?"* **Corrected**

## v11.83 — 2026-09-04

### `tools/gbachar.py` — both characters in, and the formats do not resemble each other

| | | |
|---|---|---|
| **CRYSTAL** | `oak_speech/oak/pic.png` | **64x96, EIGHT bits per pixel** |
| **SCORN** | `trainers/front_pics/leader_giovanni_front_pic.png` | **64x64, four bits, sixteen colours** |

- ***Crystal's pixel values are 97 to 121, not 1 to 25.*** `oak_speech.c` loads her palette at **`BG_PLTT_ID(6)`** — palette RAM 96 — and **an 8bpp background indexes palette RAM directly.** *An image written with ordinary low indices would read the wrong end of the palette and arrive as noise*, with a clean build and no warning
- **Neither sprite carries its own shadow.** `oak_speech` draws `platform.png` underneath and the battle screen draws its own, so the art's ellipse had to come off — **removed by hue, not position**: *the ellipse is the background blended toward white and keeps its green bias; the lab coat is neutral and the suit blue-grey, and neither does*

### Where Scorn is actually seen

- ***Not an intro portrait — a battle sprite***, which is why his is square and hers is not
- **CORPUS HIDEOUT B4F**, **SILPH CO. 11F**, **CALLOW GYM** (4.31), and the **CORPUS WAREHOUSE** on Five Island. *Four encounters, and the player fights him in all four*
- **His overworld sprite is still vanilla and still a man** — the smallest remaining piece of the fox decision

## v11.82 — 2026-09-04

### Scorn is the bright red, and the reason is not the obvious one

- **3589 decides it**: ***"This design has no villain. Its central move is refusing to make anyone a monster."*** *A dark red cobra in a suit is villain-coded* — the player files him as the antagonist in half a second
- **4.6 states the horror precisely**: *"to Scorn the question is settled — they are units, they are inventory, the math is clean. That is the horror, and it needs no villainy to land."* **Bright red reads as a man having a good day**, which is worse and true

### And it is paid for, not free

| | head | suit | separation |
|---|---|---|---|
| **bright, as shipped** | 82.8 | 109.6 | **26.8** |
| darkened to 60% | 49.7 | 109.6 | 59.9 |

- ***I argued the opposite first and the measurement corrected it.*** **Darkening the head more than doubles the value separation**, because the suit is a mid-grey and moving the head down moves it away
- **So the dark version is the technically stronger sprite and the weaker character** — and the character wins. *26.8 is workable behind a thick outline and a hood silhouette*
- **If it ever needs more, lighten the SUIT rather than the head**: ×1.30 gives **59.7** with the charisma intact

### Art in

- `gfx/characters/crystal_speech.jpeg` and `gfx/characters/scorn.jpeg`. **Crystal keeps the vanilla sprite's purple shirt, extended hand and pale ellipse**, which makes the swap read as the same shot of a different person

## v11.81 — 2026-09-04

### The fox ruling rested on a resolution the port moved

- **2026-08-29 decided it and the reasoning was explicit**: *"at 16x16 a character has about three pixels of head, so the entire animal vocabulary is ears, a tail, and a shade"* — **so the Clears get ears, tail and value, nobody else changes, and the game never says anyone is a fox**
- ***That is a Game Boy fact. The GBA intro portrait is 64x96.*** At that size **a fox is a fox** — ears, muzzle, brush, fully legible, on **the first character the player meets**, while every other portrait is a person
- ***The named failure mode is no longer a risk to watch for on playtest. It is the default***

### So the cheap escape stops being contingent

- The ruling already specified the fix — *give light animal features to a handful of recurring characters so fox becomes one species among several* — and named **Scorn** first
- **He now arrives with her rather than after her**, because *the deferral assumed a size at which the problem would not show, and that size is gone*
- **The opera already has him: a red snake.** A species, not a shade — which is exactly what makes fox read as one kind among several

### What does not change

- ***The game never says anyone is a fox.*** **Link's Awakening is the model** — an island of animal-people, unremarked by anybody in it. *A world, not a claim.* **It becomes a statement the moment a character notices, and none does**
- **The daemon-confusion worry is answered by context**: portraits and battle sprites never share a screen. *A fox in a lab coat at 64x96 is a person in a room; MUSAI at 64x64 on a platform is a creature in a fight.* **The player is never asked to tell them apart**
- **The overworld ruling stands** — 16x32 is still three pixels of head
- `docs/gemini-prompts-crystal.txt` carries both briefs

## v11.80 — 2026-09-04

### Callow gym — 3 ours to 26, slice at 34%

- ***Written for what was already in it, not for where it comes.*** **The boss's final line was ours** — *"I optimised what I could measure. That is the job. The machine chose what I weighted it to choose."* — **and his first line was vanilla cackling**: *"Fwahahaha! This is my hideout!"*
- ***The same man, ninety seconds apart, in two different games.*** He opens cold now and the two ends match

### The MARK is not a reward

| | |
|---|---|
| vanilla | *"It is evidence of your mastery as a POKéMON trainer!"* |
| ours | ***"It is not a reward. It is a record that you were assessed."*** |

- **That is what a MARK has been since 5**, and it had never been said by the person who hands them out
- His TM is dated without explanation: ***"I wrote it when I ran this GYM. That was before the other thing."***

### The staff, per craft rule 6

- **0.1 says it outright**: *Corpus employees are cheerful and absurd; the horror is what they are cheerful about.* **Seven karate masters became seven employees**
- *"My daemons and I are very aligned. It is in my review."* · *"If my daemons performed the way I do in meetings…"* · *"Conditions were not typical."* · *"This will be raised with me."*
- ***Nobody in the building knows who runs it.*** The guide at the door has been asking: **"I have asked. They smile."**

### Open, and the writing has half-answered it

- ***GIOVANNI is not renamed.*** But 4.18 gives **SCORN** as the surname that painted over `CLEAR LABORATORY`, and the man in this gym already says *"the machine chose what I weighted it to choose"* — **which is Scorn's crime, stated by him, in the ROM**
- **Either the man in the gym is Scorn, or two different people weighted the same machine.** One vocabulary entry when it is decided

## v11.79 — 2026-09-04

### The Undertone — 2 ours to 15, slice at 27%

- ***The room was written around one block nobody needed to touch***: the carved stone, **the type chart as an artefact older than the path** — *"Read across: each thing, and what it does to each other thing. Nobody signed it."*
- **Everything else had to sit under it**, which is what the name asks for: *an undertone is the colour beneath the colour, and the thing meant but not said*

### Two signposts doing the falling tree

| | |
|---|---|
| **USER TIPS** | *"Nothing will announce itself if you stay off the grass."* — **"It is still there."** |
| a bug catcher out of boxes | *"I have no USERBOXes left. **Everything I meet now, I just meet.**"* |

- ***The second is the best line in the room and it belongs to a throwaway NPC.*** 0.4 needs an observer and the INDEX only holds what is bound — **so a USER with no boxes can see and cannot record.** *He does not know that is what he said*
- **The first is 0.4 on a signpost**, and it is still a correct game hint. That is the trick

### A wrong mechanic, caught by writing a second room

- ***The lab claimed "a daemon with MANA left has somewhere better to be."*** **MANA is PP.** What keeps a creature out of a box is its condition, not whether it has moves in hand
- *The forest's weakening tip is where it became obvious*, because two lines were saying different things about one rule. **The lab now reads "one that is not tired"**
- ***Writing a second room found an error in the first*** — an argument for doing them in a run rather than one at a time

## v11.78 — 2026-09-04

### The rival's house — 0 ours to 16, and the slice hits 22%

- ***The room had a scene in it nobody had noticed.*** **Crystal reads daemons with an instrument. DAISY just looks at them**

> **DAISY:** *"Gran reads them with an instrument. I just look. May I see your first one?"*

- **That is 0.4 inside one family** — two accounts of the same creature, both correct, arrived at completely differently — **and vanilla shipped it as a grooming minigame**

### The friendship ladder is observation, not sentiment

- Vanilla runs *"it loves you"* down to *"why does it hate you"*. **Ours are readings**

| | |
|---|---|
| highest | *"This one would not leave if you opened the box."* |
| | *"It is settled. It has stopped watching the door."* |
| | *"It stays near you without being told. That is most of it."* |
| lowest | *"…I would rather not say this. It would be anywhere else if it could. What have you been asking of it?"* |

- ***Nothing there says a daemon feels anything.*** Every rung reports **where it puts itself and what it does unasked** — and the bottom rung is worse for being flat. **Craft rule 1 is not strained: nobody claims to know what is inside it**

### Four lines doing other work

- **on AL** — *"He has not mentioned the result. So I know the result."*
- **on the TOWN MAP** — *"It shows where you are and what the places are called. The two do not always agree."* — 3.2's device, ninety seconds early
- **on the bookshelf** — *"Shelves of books about daemons. None of them by Gran."* — which pays off the lab's *"Everyone says so. Very few of them have read her."* **Neither explains the other**
- **on an EGG** — *"I cannot do anything with an EGG. There is nothing running in it yet."*

- *Open:* **DAISY is not renamed** — a Clear, and the last vanilla name in the family. One vocabulary entry when it is decided

## v11.77 — 2026-09-04

### The lab, written — 7 blocks to 34

- ***The first ten minutes of the game were 7 ours against 45 vanilla's.*** Now **34 against 23**, and the slice moved from **9% to 17%**
- **Vanilla's professor is genial and grand. Ours is a researcher** whom 4.10 has already had removed from a building

| | |
|---|---|
| on why she called them | *"I forget why I ask people things, and then it turns out I was right."* |
| on the three she has left | *"I used to keep a great many more. Three is what I have now."* |
| on choosing | *"Choose. Not carefully. You cannot know enough yet to choose carefully."* |
| on the INDEX | *"It writes down what a daemon does… It is very good at what it records."* |
| on her own project | *"I will not finish it. That is not modesty, it is arithmetic."* |

- ***"It is very good at what it records" is 0.2 in seven words*** — the reproduction that loses the original, said as a compliment by the person who built it
- **The send-off is inverted**: *"POKéMON around the world wait for you"* becomes ***"They are out there running. None of them is waiting for you."***

### Three findings from doing it

- ***The aides were the easiest to get wrong.*** *"I study DAEMON as CRYSTAL's AIDE"* is vanilla's idea of a scientist; *"I read daemons here. CRYSTAL signs the work."* is a person
- ***`catch → bind` reached a place it should not.*** HANDLER's entry read *"It **catches** what stopped"* — **the exception sense, which is the whole point of a fault handler** — and the pass rewrote it to *"binds"*. The rule is right and the collision is real, so the word became *intercepts*. **A vocabulary that owns a common verb keeps finding the other meaning of it**
- ***A block regex is the wrong tool for a `.string` run.*** Escaping `\\p` and `\\n` in a pattern that also escapes quotes matched **only single-line blocks** and skipped every multi-line one — **3 of 40, with no error.** Walking the lines and consuming while they start with `.string` is four lines and cannot be wrong

## v11.76 — 2026-09-04

### `tools/gbaslice.py` — the slice, measured

- **314 blocks between Blanche and Slate. 29 are ours. Nine percent.** 161 are vanilla reworded, 124 untouched
- **The test is similarity to upstream**, as in `gbaindex.py`: *the vocabulary pass rewrites POKéMON and USER everywhere*, so *"did it change?"* means nothing. **Below 0.5 the sentence was rewritten; above it, vanilla is still talking with our nouns in its mouth**

### It is not a port regression, and saying so matters

- ***`port_dialogue.py` carried everything there was*** — its own tally is **569 blocks, 536 matched, 0 without a home.** Nothing was lost crossing engines
- **507 of those 536 are not in the slice.** They are in Halftone, Quicksilver, Corpus, the Review Board. *The effort went to the places that carry the story, and the first hour was left as Kanto with the labels changed*
- ***Worse than a bug, because a bug is found by playing.*** This is found by **counting** — reading it feels fine, every noun is right, and the sentences underneath are somebody else's

| | ours | vanilla |
|---|---|---|
| **CRYSTAL CLEAR's lab** | 7 | **45** |
| the rival's house | 0 | 11 |
| Callow gym | 3 | 11 |
| The Undertone | 2 | 13 |

- ***The lab is the first ten minutes of the game, at 7 blocks to 45.*** **Slate's gym is the only room in the slice that is mostly ours** (8 to 5) because 5.1 wrote CAIRN's award

### A false alarm, recorded

- **A `sed` range printed two non-adjacent blocks together** and I read the join as a spliced message. **It was not.** A duplicate-block detector across every map found **one** collapsed pair in the whole game — *"dear boy" and "dear girl" onto "dear friend"*, which is the degendering pass working

## v11.75 — 2026-09-04

### Thirty-four Index entries, and the pair is not the default

- **The thirty-two slice daemons plus SUSPEND and HIBERNATE**, which had been renamed and left wearing vanilla's prose
- ***`gbaindex.py`'s "renamed, but the entry is still vanilla's" row is now empty.*** All **72** named daemons carry their own writing — **11 pairs, 61 singles**
- ***Single entries, and that is a decision.*** 0.4's instrument is sharp because it is **rare**: the eleven pairs are the daemons where the observer question bites. **A pair on every wild creature would make disagreement the wallpaper rather than the point.** *Pairs can be layered on later; they cannot be taken back once they are everywhere*

### Four that do more than describe

| | |
|---|---|
| **STUB** | *"It does nothing at all. It was put here to hold a place until something real arrived. Nobody came back for it."* |
| **ESCALATE** | *"The thing that was doing nothing was left alone long enough. It has every permission now. Nobody granted them."* |
| **OUTLIER** | *"Far enough from the rest to be dropped from the average. It was not an error. It was dropped anyway."* |
| **HIBERNATE** | *"It writes down everything that was running and switches off. What comes back is identical. Something is missing."* |

- ***HIBERNATE is the teleporter problem in a Wigglytuff*** — 0.4's substrate question asked about a creature that sleeps. **It reports a procedure and stops**
- **STUB into ESCALATE is one sentence across two entries**: *the thing that did nothing was left alone long enough* — Magikarp told as a security incident
- Every line validated against the 234px pane before writing; **widest is 229**

## v11.74 — 2026-09-04

### The slice bestiary — fourteen asked for, thirty-two named

- ***8's rule keeps it bounded***: the set is **the daemons the player meets before the first MARK**, not 151. Nine were already ours; fourteen were not
- **Fourteen became thirty-two, because a half-renamed line is the PORYGON2 problem again.** *SLOWPOKE without SLOWBRO is a daemon that evolves into vanilla.* Every line taken whole — **72 species named now**

| | |
|---|---|
| ZUBAT · GOLBAT · CROBAT | **ECHO · TRACER · MULTICAST** |
| GEODUDE · GRAVELER · GOLEM | **HEAP · STACK · MONOLITH** |
| MAGIKARP · GYARADOS | **STUB · ESCALATE** |
| MANKEY · PRIMEAPE | **PREEMPT · LIVELOCK** |
| PSYDUCK · GOLDUCK | **FAULT · HANDLER** |
| SLOWPOKE · SLOWBRO / SLOWKING | **LATENCY · SHELL / KERNEL** |
| CLEFFA · CLEFAIRY · CLEFABLE | **NOISE · ANOMALY · OUTLIER** |
| PARAS · PARASECT | **PAYLOAD · ROOTKIT** |
| NIDORAN♀ line | **FORK · THREAD · SCHEDULER** |
| NIDORAN♂ line | **BRANCH · PREDICTOR · PIPELINE** |
| POLIWAG · POLIWHIRL · POLIWRATH / POLITOED | **LOOP · SPINLOCK · MUTEX / SEMAPHORE** |
| GOLDEEN · SEAKING | **SPAWN · UPSTREAM** |

- ***SLOWPOKE branches into SHELL and KERNEL***, which is the pair — a Shellder on the tail is a process with a shell round it, on the head it is the other half of the same word
- ***POLIWRATH and POLITOED are MUTEX and SEMAPHORE***, the canonical pair, as the two branches of one creature

### The check that earned its keep

- **Every name was validated against the species, move and type tables before a byte was written**, and it caught two: ***`THRASH` and `BARRIER` are both vanilla moves***
- *A species sharing a move's name is not a build error — it is a battle log that reads as nonsense*, and it would have shipped. **`MUTEX` is better than the `BARRIER` it replaced**
- **Index entries are a separate pass**: thirty-two daemons now wear our names over vanilla's prose, which `gbaindex.py` reports in the same row as HIBERNATE and SUSPEND

## v11.73 — 2026-09-04

### The debug kit had the ticket and still could not board

- ***The item is not the permission.*** `ITEM_SS_TICKET` went into the bag last time and the ship was still shut, because the sailor at Ardor runs

> `goto_if_unset FLAG_GOT_SS_TICKET, ...DontHaveSSTicket`

- **He checks a FLAG and never looks in the bag at all.** A debug save with the ticket in hand was turned away at the gangway
- **Both are set now, deliberately**: *the flag is what opens the ship; the item is what the player can read a description of*, which is what 9.3 is here to evaluate
- ***Worth remembering as a class, not an incident.*** A test kit that grants objects grants nothing the game gates on state — and **every one of those failures looks like the kit did not run**

## v11.72 — 2026-09-04

### GLAUCOUS ISLES

- ***My "keep it, it is already a colour word" argument was wrong***, and being asked twice is what caught it: **FUCHSIA is also a colour and it became LURID.** Cerulean, Viridian and Celadon likewise. **The test was never *is it a colour* — it is *is it ours***, and SEAFOAM was the last major place still wearing vanilla's word
- **Glaucous is a real pigment** — the dull blue-green bloom on a plum — so it names a **surface**, which is the joke: *ORPHEUS is four floors under it*
- **The rename lives in `port_vocab.py` with the towns**, not in hand edits, and `ISLANDS → ISLES` is a phrase entry so every other island keeps its word

### MOCK, and a constraint that was never a constraint here

- ***4.6 ruled out `PERSPECTIVE` as the category*** because the Game Boy caps it at **ten** characters and proposed `FRAME` instead. **Gen 3's cap is eleven** — vanilla ships `TINY TURTLE` and `HUMAN SHAPE`. *So the category is `PERSPECTIVE`, spelled out*
- **The entry was a rewrite, not a word swap**, as 4.6 required — vanilla's prose is *"recombine its own cellular structure"*
- CONTENT: *"It becomes whatever it is looking at, completely. While it is doing that there is nothing of it left over."*
- CONTEXT: ***"It has been every daemon in this record and appears in none of them under its own name."*** — 0.4's observer problem inverted
- **The battle message is 4.6's verbatim**: `<USER>` **took the frame of** `<NAME>`!

### The animation — colour, because the colour means something

- ***9.4 settles it***: on the GBA a daemon is coloured by its **type**, so the palette is information, not decoration
- ***And the mechanic was already saying it.*** Gen 3's transform copies the target's sprite **and palette** — so **PERSPECTIVE already ends with the attacker wearing the target's type.** Nobody arranged that
- **What vanilla did not show is the cost.** 4.6 insists the move is *total and lossy*. **Its own hue now drains to grey before the swap and the new one arrives after**
- ***Grey is not a colour spent***: 8.6 makes grey the ground this game already stands on, so the surrender is a return to it and invariant 5 pays nothing

## v11.71 — 2026-09-04

### PLANT stays, and the table underneath it changed meaning for free

- **`WORKS` was on the table** — *the works still works*, and UMBRAL ASCENT is precedent for swapping the generic noun. **Not taken**: `PLANT` already carries two meanings, **an industrial plant and a living thing**, and *a building still growing with nobody tending it is the quieter joke*
- ***All five species in the plant are `TYPE_ELECTRIC`***, which 2 glosses as **SIGNAL — a carrier, not a spark**

| | | |
|---|---|---|
| MAGNEMITE | **SENTINEL** | SIGNAL/HARDENED |
| MAGNETON | **QUORUM** | SIGNAL/HARDENED |
| PIKACHU | **SPIKE** | SIGNAL |
| VOLTORB / ELECTABUZZ | *unnamed* | SIGNAL |

- ***The building is full of carriers, still carrying, with nobody receiving.*** **Nothing in the encounter table moved — the name moved, and the table changed meaning underneath it**
- **And SPIKE was already right**: in a building whose business is a keepalive — *a flat regular signal meaning only "still here"* — **a spike is the anomaly.** It was named before the building was

### Repo descriptions, so the two read as one

- `CodeMusic/DAEMONS` was still describing itself as *"a Pokémon Red total conversion"* — **stale, and a near-duplicate of the engine repo's**
- Now: ***"The argument, and where it came from."*** Design bible, lineage and tooling; fifteen years traced from three blogs into a type chart, a rock opera and two cartridges
- **The engine repo says what the game *is*; this one says what the argument is and where it came from**

## v11.70 — 2026-09-04

### The three birds, and vanilla had already placed them

| | where it is | | category |
|---|---|---|---|
| Moltres | Mt. Ember, the summit | **PROMETHEUS** | `CRAFT` |
| Zapdos | the plant | **ASCLEPIUS** | `RECOVERY` |
| Articuno | Seafoam, four floors down | **ORPHEUS** | `LAMENT` |

- **PROMETHEUS gave fire away as craft and was bound to a rock on a mountain.** *The CONTEXT entry is the punishment, unstated*: **"It is still up here, and it is not going anywhere."**
- **ASCLEPIUS raised the dead and Zeus killed him with a thunderbolt** — the thunderbird, in the building still running. *CONTENT: nothing it restarted has stopped again. CONTEXT: nobody asked the thing that stopped whether it wanted to be running*
- ***ORPHEUS is the sharpest.*** He went down and lost her **by looking back** — **the observer destroyed by observing**. His CONTEXT entry: **"It has not said what it saw when it turned around."**
- **Ten written pairs now**, verified per cartridge

### The other two landmarks keep their names

- ***Mt. Ember and Seafoam already obey 0.2*** — **ember** and **seafoam** are both colour words. Renaming them for a systems pun would break the register **KEEPALIVE was the exception to**: POWER PLANT was neither a pigment nor a state, which is why it was the one that had to move
- **And SEAFOAM is already working**: the place is named for its *surface* and the thing that matters is four floors under it. ***An account that describes only what is visible***

## v11.69 — 2026-09-04

### KEEPALIVE PLANT

- ***The Power Plant was the last place in Kanto carrying its vanilla name.*** The other two landmarks did not need one — **ember** and **seafoam** are both colour words and already obey 0.2
- **A keepalive is a signal whose only purpose is to stop a connection from closing.** The building is still running with nobody connected, and its resident is SENTINEL, whose one move stops you `DETACH`ing. ***The place is its own resident's move at building scale***
- **Two things vanilla had already arranged**: Rock Tunnel next door is **THE BLACKOUT**, so Route 10 signposts *the blackout and the thing still running*; and Route 17 now reads ***"I got my VOLTORB at the abandoned KEEPALIVE PLANT."***
- *The generated `region_map.c` symbol followed by hand, byte-wise*: `sMapsecName_KEEPALIVE_PLANT`

### `tools/gbaindex.py` — which entries to read in which cartridge

- **Two tests that do not work, both tried.** *"Does it differ between editions?"* is useless because **vanilla already varies nearly all of its own entries** — 224 of them. And *"were they identical in vanilla?"* fails too: **every entry this project has paired was one vanilla had already varied**
- **So the test is similarity to upstream**, which is what `port_dialogue.py` uses for the same reason: *a vocabulary substitution leaves most of a sentence standing and an entry we wrote does not*

| | |
|---|---|
| **written as a pair — read both cartridges** | **7**: MUSAI, CODEMUSAI, SEEKMUSAI, CAREMUSAI, SUBSTRATE, SENTINEL, QUORUM |
| ours, one entry copied into both | 27 |
| renamed, but the entry is still vanilla's | **2 — HIBERNATE and SUSPEND** |

- *That last row is a genuine to-do the tool found on its first run*

## v11.68 — 2026-09-04

### SENTINEL was on the wrong slot, and the reason is a rule

- ***In vanilla, Porygon's whole identity is "the artificial one"*** — a creature of code among creatures of flesh. **In this game every creature is a process**, so *"made of code" is the default* and the distinction evaporates
- > **In a world where everything is code, the anomaly is the thing made of matter.**
- **Which is 4.7's move already**: vanilla's Mewtwo is a copy made stronger, ours is *a comprehension, not a clone*. **Invert the vanilla premise rather than dress it**

### SUBSTRATE — the Porygon slot

- **The name was ours and had already been given up.** SUBSTRATE was the original STRATUM, cut because *type strings cap at eight characters and it is nine.* **Species names allow ten**
- CONTENT: *"Every other daemon is a process. This one has a mass, a temperature, and somewhere that it is."*
- CONTEXT: *"They call it the material one. Nobody has shown that being material is different from running."*
- ***Substrate independence, which is 0.4 one level down.*** Category `MATERIAL`; stats, ability and learnset restored to vanilla
- **Where you get it already meant something**: a Game Corner prize, **bought with tokens, by the concern whose hideout is under the floor**

### SENTINEL — the Magnemite slot

- **A single unblinking floating eye**, and the types were already right: **SIGNAL / HARDENED** — *a carrier, not a spark*, and a system secured against interference
- Attack and Sp. Attack to **5**, freed points to HP/Def/Sp.Def, **base stat total unchanged**. Six damaging moves out for **FORESIGHT, MEAN LOOK, REFLECT, LIGHT SCREEN, SAFEGUARD, PROTECT**. Ability **INSOMNIA**
- ***There is no scene, and that is the scene.*** You are not given it — **the only place in the game it occurs is the Power Plant**, a facility with no operators where something is still watching. *The falling tree as a room you can walk into*
- ***It learns `MEAN LOOK` at level six.*** `DETACHED` is breaking your connection to a running process — **so the thing that never attacks is the thing you cannot walk away from.** The Power Plant has no NPCs and no signs with text, which is the right amount of dialogue for it

### QUORUM — the Magneton slot

- **Three of them, fused.** *A quorum is the minimum number of observers for a decision to count*, so the evolution is **more observers and one account**, not the watcher learning to act
- CONTENT: *"Three of them, and they do not act either. What one of them saw, three of them saw."*
- CONTEXT: ***"Three accounts of one thing. They agree, which is not the same as being right."*** — 4.8 and 0.4 in one breath
- ***QUORUM also lives in DOLDRUM CAVE***, where S.T.A.R.R. sleeps. **Three witnesses in the room with the thing** — vanilla's own encounter table, already true

### Left open

- **PORYGON2 stays PORYGON2** — trade-evolution, effectively unreachable, no pressure
- ***The Power Plant is the last place in Kanto still carrying its vanilla name***, and it is now the home of the daemon still watching it

## v11.67 — 2026-09-04

### The debug kit could not board the ship

- **`ITEM_SS_TICKET` was not in the test bag**, so a debug save could not reach the ship at Ardor — *or HM01, or anything behind it*
- It also fits the kit's own logic: **a KEY item is its own pocket and its own description pane**, which is what 9.3's spike is evaluating

### A printer in Halftone argues about the primaries

- ***"I said red, yellow, blue. He said red, green, blue. He works in light, so he adds. I work in ink, so I take away. He called me negative for a year."***
- ***"Take everything from him and he is sitting in the dark. Take everything from me and I have a clean sheet. We were both right. He still will not have it."***

**It is not arbitrary. Three things hold it in place:**

1. **0.2** — the map is named in pigment and printing, so **this world is subtractive by construction**, while the player holds an **additive** screen. *The argument is about a split the player is sitting inside*
2. **0.4** — both men are right; **the disagreement is not error, it is two frames.** The article, in a form a player can check
3. **8.6** — the world is grey and the player supplies the colour, so the game is **neither** system. *It declines to mix and lets the observer finish it*

- **Halftone was the only possible town.** Its name is the dot screen, and its sign already reads **"The Noble Purple Town"** — in a game that records **purple is not on the spectrum** and the mind invents it
- **Craft rule 2 is not spent.** The Verdigris kid keeps the one *near-notice*; **the printer never mentions feeling** — he is talking about ink, and he is right
- ***The joke inverts on purpose***: the brother calls him **negative**, and the subtractive one is the one holding the **clean sheet** while the additive one sits in the dark. **The pessimist gets the blank page**
- *Cost*: the weakest of that shop's three hints, where to buy X ATTACK

## v11.66 — 2026-09-04

### 4.25 SENTINEL — the daemon that never attacks

- **The Porygon slot, NORMAL — which is CONTENT.** *The vessel was chosen for what it already is*: a made thing, a creature of code, built in a laboratory
- ***0.4 as a creature.*** The article's answer to the falling tree is **no observer, no sound**, so a thing that only watches is what makes anything reportable at all
- **The echo is left alone.** A *sentinel* watches; a *sentient* thing is one there is something it is like to be. Unrelated, and they sound as though they must be

### It cannot attack, and the numbers say so rather than a rule

| | vanilla | SENTINEL |
|---|---|---|
| Attack / Sp. Attack | 60 / 85 | **5 / 5** |
| HP / Def / Sp. Def | 65 / 70 / 75 | **110 / 110 / 130** |
| total | 395 | **395** — *the budget is unchanged* |

- **No damaging move left in the learnset.** TACKLE → **FORESIGHT**, PSYBEAM → **MEAN LOOK**, TRI ATTACK → **REFLECT**, ZAP CANNON → **LIGHT SCREEN**
- ***MEAN LOOK is the one that matters.*** `DETACHED` is breaking your connection to a running process, and 0.4 has perception requiring an observer — **so a daemon that stops you detaching is the observer refusing to let the connection close.** *The player is never told. They simply cannot leave*
- **SHARPEN stays, and it is a joke**: it raises an Attack stat of **five**. *It prepares to act and never does*
- **INSOMNIA, not TRACE** — the watcher cannot be put to `SLEEP`, and `SLEEP` is one of ours. Category **`OBSERVER`**

### The pair, and it is 0.4's sharpest

| | |
|---|---|
| CONTENT | *"It has never attacked anything. It stays where it can see, and it does not look away. That is the whole of it."* |
| CONTEXT | *"Everything it saw is on record. It is not in the record. Nobody thought to write down who was watching."* |

- **Verified per ROM**: the CONTENT account is in `pokefirered.gba` and not `pokeleafgreen.gba`; the CONTEXT account the other way round

### And a rename that had to be stopped

- ***`port_vocab.py` found PORYGON inside PORYGON2 and offered `SENTINEL2`*** — a nickname that would not have matched its own species, since `SPECIES_PORYGON2` is untouched
- **Naming an evolution is a decision, not a substitution.** Held in the keep list until there is one — *and the question is real: an evolution of a thing that never attacks either stops watching or gets better at it*

## v11.65 — 2026-09-04

### The keyword list, checked again — and the check was wrong the first time

- **The list is the same 114 terms reviewed on 4 September**; `vocabulary-candidates.md` already held the whole shortlist, SENTINEL included
- ***But its "already spent" table was checked word for word, which is the wrong check.*** **LABEL ships as `LABL` and CLUSTER as `CLUSTR`** — both read as free and neither is. *A name shortened to fit a nine-character field is still spent*
- **The ROM carries 33 of our names now, not the six that table was measured against.** Any future pass has to normalise before it compares — the same lesson `port_names.py` learned when a positional zip read an addition as a rename

### SENTINEL, revised now that 0.4 exists

- ***0.4 makes it the best noun on the list, and that was not visible before.*** The article's answer to the falling tree is **no observer, no sound** — so a thing that only watches is what makes anything reportable at all
- **A daemon called SENTINEL that never attacks is 0.4 as a creature.** It does nothing, and nothing can be said to have happened without it
- **And it is the sharpest pair the two-account Index will get**: one record of what it observes, one of why there is a record
- *Still not queued.* 8's scope rule outranks a good idea

## v11.64 — 2026-09-04

### 0.4 — the keystone article is in the bible now

- ***Sensation into Perception, and the Filters of our Experience*** (PsychologyCode, 15 July 2013) — the longest post on the site, nearly a third of it, and **the one never reposted.** `lineage.md` 2.2 had the archaeology; **`vision.md` did not carry the idea at all**
- **It names both halves eleven years early**, under different words: *"the basic information your eyes gathers is known as the **bottom-up** information, and all your memories which come into play during the analysis is called **top-down** information"*
- ***"Sensation is shared. Perception is not."*** One line doing three jobs — **the edition split** (two stages of one act of recognition, not two products), **the type chart** (top-down completes bottom-up, never the reverse), and **the colour cartography** (8.6 spends the greyscale so the player supplies the hue — *which is the article, played*)

### Three places it was already in the game, none of them on purpose

- **`DETACHED`** — 7.2 defines fleeing as *breaking your connection to a running process; the process is still running, you simply stopped observing it.* **That is the falling tree, sitting in a battle message**, written before anyone joined them up
- **"Some of them disagree."** The briefing already warns the records will not match
- **The Five Witnesses.** 4.8's lock is that sentence built into a puzzle

### Ruled — the two Indexes disagree on purpose

- ***Gen 3 ships a separate Index text file per edition.*** Vanilla uses it for flavour and **451 of ours still carry that variation, inherited** — but ***every entry this project wrote was written once and copied into both***, throwing away **the one instrument in the ROM shaped exactly like the thesis**
- **The entries are a pair now**: CONTENT reports *what it does*; CONTEXT reports *what follows from it — who framed it, who chose, who is not in the record*
- ***Neither reports a feeling***, so 0's table still holds exactly — the Index measures only content. **What differs is what the observer attended to**, and two honest records of one creature still fail to match
- **Written first for the four MUSAI**, the family that already is the argument

| | SEEKMUSAI |
|---|---|
| CONTENT | *"Finds the nearest match to anything it is shown. Nearest is not the same as right. Nobody told it. Nobody will."* |
| CONTEXT | *"Every answer it gives is the closest thing it has already seen. What it has seen was chosen by someone else."* |

- **Proved at the byte level**: `gbastr` finds *"chosen by someone else"* in `pokeleafgreen.gba` and **in neither CONTENT ROM**
- **Craft rule 1 unbreached.** A player with one cartridge learns a creature; a player with both learns that **a record has an author**. *They are never told which is true, because the question is malformed*

## v11.63 — 2026-09-04

### SEEKMUSAI takes the Pikachu slot

- ***S.T.A.R.R. was the instinct and the wrong answer***: 4.7 puts it **dormant past the Review Board**, and *a creature asleep for the whole game cannot be the one that welcomes you into it*
- **The Pikachu slot is a fact about the anime's marketing**, not about FireRed's fiction — the creature there has nothing to do with the briefing beside it
- ***The briefing is about records***: an INDEX that starts out empty, everything written down somewhere, closing on **"Some of them disagree."** So it is narrated by the daemon whose item is **EMBEDDING** — the thing that makes an index searchable
- `TYPE_FLYING` fixes it at VECTOR: **sanguine red, not Jolteon's yellow**. And it is the sibling *not* already on the title screen

### `tools/gbaseek.py` — only the body is drawn art

- All three layers were generated and **the two overlays did not seam**: the antennae sat on a plain dome while the body has a swept crest, and the visor was a different faceplate shape. *The helmet would have changed shape every time it twitched or blinked*
- **The overlays are built FROM the body** — its own top sixteen rows with stalks drawn on, its own faceplate with a line across. *The seam is exact by construction*
- The tool also has to skip the **"A" and "B" Gemini burns into the corner** — taken as the largest connected component, which a bounding box would have swallowed

### The breath is one pixel, and it is not a style choice

- ***`SpriteCB_Pikachu` is three lines and governs the rig***: `sprite->y2 = gSprites[sprite->sBodySpriteId].animCmdIndex`
- **Each overlay's offset is the body's frame number, 0 or 1** — so a body that moves more than one pixel tears away from its own overlays. The generated frame B was a full crouch and **doubled the helmet**
- **Frame B is synthesised**: frame A dropped one pixel, shadow left in place. *Vanilla's own frames are a one-pixel settle with 33 pixels of touch-up.* The generated crouch is unused
- **The visor sprite moves `(24,13)` → `(24,17)`.** Solving the layout against Pikachu's eye position forced the creature to **sixteen pixels wide**; four pixels of sprite position was cheaper than shrinking the character

## v11.62 — 2026-09-04

### The controls guide winks, and survives reaching real hardware

- ***The one screen in the game that addresses the player as a player***, and on an emulator **not one of the six button names is where it says it is**
- **was** — *"The various buttons will be explained in the order of their importance."*
- **is** — ***"The buttons, in the order they matter. Names, not places. Check your bindings."***
- ***"Bindings" is not borrowed from emulator settings — it is already this project's word.*** 7.2 replaced *catch* with **bind**, the build script is `bindDaemons.sh`. **On a real cartridge the line still parses**, because those buttons are bound to a shell — *so it does not expire the day the ROM reaches hardware*, which was the condition
- **A rewrite, not an addition**: page 1's window is 30x4 tiles — 240px wide and **two lines tall**, and vanilla used both. 212px and 217px against 236; vanilla's own widest here is 221
- *Craft rule 6 licenses it* — a game that is funny in its ordinary moments earns the right to be serious in three or four of them

## v11.61 — 2026-09-04

### Ruled: the world is chiptune, the front door is not

- ***"chiptune I think is good"*** — the twelve tracks from `engine/` keep the texture they were written for. **9.14 already put the title outside the fiction**, so the front door gets the sample ROM and the world does not
- ***"Leave them alone" was not on the table, because they were not left alone.*** They played `VOICE 0`, and slot 0 of the banks they pointed at is a **keysplit — a drum-kit key map — in ten cases out of eleven**
- **The PSG slots do not agree between those banks either**: slot 87 is a programmable wave in three of eleven and a filler square in the rest, so *the same wave part changed instrument from town to town*

### `voicegroup192` — the Game Boy bank

- **GM 80 and 81 are "Lead 1 (square)" and "Lead 2 (sawtooth)"** and Gen 3 puts its PSG voices exactly there — the same GM agreement `voicegroup191` relies on
- `pokered` declares channels in order and `port_music.py` keeps it, **so the channel index is the hardware channel**: 80 pulse 1, 81 pulse 2, 87 wave, 126 noise
- **Filler slots hold pulse 1**, as 191's hold the piano — *a stray program stays in the family*

### The tool that owns the notes owns the bank

- ***`port_music.py` still had `mus_title` in its list and overwrote the stems transcription*** the first time it ran after the bank change, repointing it off `voicegroup191`. **Caught because midi.cfg reported 13 songs when there are 12**
- It keeps `midi.cfg` in step now, and `SUPERSEDED` keeps its hands off the track it no longer owns
- **`gbasongs.py` knows chiptune is a decision**: PSG on our bank at its four slots is clean; a square anywhere else, or a keysplit anywhere at all, still reports. *All 13 songs clean*

## v11.60 — 2026-09-04

### The battle menu had lost a newline, and it had been lost for weeks

- ***"menu is weird"*** — and it read **`FIGHT  BAG DAE`**, with DAEMON and RUN off the right edge of a 96px window
- Vanilla is `BAG\nPOKéMON`. **Ours was `BAG DAEMON`** — the line break replaced by a space, so all four options ran onto one line
- ***`reflowable()` already refuses to touch a string containing `{CLEAR_TO}`***, because a string that positions its own text is a layout. **The damage predates that guard**, and `convert()` is a no-op on an already-converted string — *so every later run of the tool walked straight past it*

### A guard, because "we fixed the tool" does not fix what it already broke

- `port_vocab.py` now diffs every **layout** string against upstream and reports any whose line-break count changed. **Verified by reintroducing the bug and watching it fire**
- ***The audit found exactly one casualty in the whole tree.*** The guard was right; it just arrived after this one

### DETACH reaches the menu it belonged in

- **7.2 has said `DETACHED` since the type table**, every battle message uses it, and the menus still said **RUN**. The window is 12 tiles — **96px, with the second column at 56, so 40px** — and `DETACH` measures **36**. *It fits with four to spare*
- `Got away safely!` → **`DETACHED.`** — 4.10's table specified this and nothing had ever implemented it

| | was | is |
|---|---|---|
| action menu | `FIGHT / BAG DAEMON / RUN` on one line | **`FIGHT · BAG` over `DAEMON · DETACH`** |
| Safari menu | `ROCK{CLEAR_TO}RUN` | `ROCK{CLEAR_TO}` **DETACH** |
| escaping a wild daemon | `Got away safely!` | **`DETACHED.`** |
| escaping a USER | `No! There's no running from a USER battle!` | **`No! You cannot DETACH from a USER engagement!`** |
| CRYSTAL's version | `...no running away from a USER DAEMON battle!` | **`CRYSTAL: No! You cannot DETACH from a USER engagement!`** — 176px, exactly vanilla's own widest line |

## v11.59 — 2026-09-04

### None of the music looped

- ***Twelve songs ended on `FINE` and stopped.*** The title theme played its 42 seconds once and left the screen silent; every town theme played through and quit
- **mid2agb builds the `GOTO` out of a MIDI text meta-event** — `[` for the loop start, `]` for the jump back. Nothing was emitting them
- ***And the markers only count on the FIRST midi track.*** `ReadMidiTracks()` reads it with `ReadSeqEvents()` and merges what it finds into every AGB track; `ReadTrackEvent()`, which reads the rest, **does not look at text meta-events at all.** Markers on a note track are read by nothing and fail silently — which is exactly how they were written the first time
- **`port_music.py` was writing each song's body TWICE to fake a loop**, at double the ROM cost, and it still stopped after two passes. One body and a real `GOTO` now
- `mus_caught_intro` is the one that must not loop: *it is the binding sound, and it hands the screen back*

### `tools/gbasongs.py` — the audio `verify-sprites`

- **Three audio bugs reached a play-test, and every one compiled cleanly**: no program change (silence), `VOICE 0` onto a keysplit (Game Boy squares), no loop marker (songs that stop). *Each needed a person to sit and listen*
- It reads the generated assembly and says **what will come out of the speaker** — the bank, the instrument behind every program number, the track count, and whether it repeats
- **Two things it had to learn to be honest.** mid2agb *compresses*, so a repeated bar becomes a `PATT` and its notes are written once; and it **omits the length prefix on a note whose length repeats**, so most note lines are a bare `.byte  Cn3` — counting `N24` found **4 notes in a song that has 32**
- **The twelve ported songs are flagged, not condemned.** PSG is a legitimate texture and these are Game Boy compositions. *It is flagged because it should be a decision, and it was previously the accident of writing no program change at all*

## v11.58 — 2026-09-04

### Stems, and a transcriber that no longer guesses

- **AIVA's new front end is an audio model** (*Powered by Minimax Music 3*) and has no notes inside it to export; the symbolic composer is the 1.0 app, and its chord-progression flow **capped the description field mid-sentence**. Four services in, the answer was to stop using services
- ***Suno exports stems***, and that changes the problem completely

### What mp3midi.py was actually doing

- **A mix is one signal**, so it split melody from bass with a filter at 250Hz and **inferred the middle voice from a chroma profile** — because `pyin` is monophonic and *cannot hear two notes at once*
- **Both were approximations of an instrument list we now simply have**

### `tools/bpextract.py` + `tools/stems2midi.py`

- **Basic Pitch is polyphonic**, so chords come back as chords. *Nothing in the output is inferred: every note was heard in a file containing one instrument*
- **It runs in its own Python 3.11 venv** — a dependency still imports `imp` (gone in 3.12) and another `pkg_resources` (gone in setuptools 81). On macOS it runs on **CoreML and pulls no TensorFlow at all**
- ***The stems are time-aligned at zero.*** They are shorter than the mix and each other because the export trims where an instrument stops — **five of seven stems' loudness contours correlate best against the mix at exactly lag 0**, and a separator emits aligned stems by construction

### Taking the top note of a chord is wrong

- The first reduction took the highest note per cell and **brass came back reaching G#6, keyboard F7** — *upper partials, which Basic Pitch correctly reports as notes*
- It takes the **loudest** now, and where two are within a hair it takes the one **nearest what it was already playing** — the assumption a musician transcribing by ear makes without noticing. **Brass F#3-F#5, keyboard C#3-C#6**
- A **register window** per stem (3rd to 90th percentile of its own pitches) drops the sparse high tail. *Measured per stem, because these are five different instruments*

### The theme, at six tracks

| stem | voice | heard | cells | out of key |
|---|---|---|---|---|
| Brass | trumpet | 52 | 149 | 13 |
| Synth | **harp** — 233 cells is an arpeggio, and a glockenspiel across that many at 152 BPM is a smoke alarm | 293 | 233 | 16 |
| Strings | string ensemble | 91 | 113 | 2 |
| Keyboard | piano | 176 | 239 | 18 |
| Bass | fingered bass | 68 | 154 | 17 |
| Drums | timpani, one stroke a bar | — | 11 | — |

- **Sixteenths, not eighths** — Basic Pitch's timing earns the resolution
- ***Strings came back with two notes out of key in a hundred and thirteen.*** The old tool snapped 10% of a melody it was much less sure of

## v11.57 — 2026-09-04

### The title screen was unreadable because of one lost nibble

- ***"the intro screen for both editions are hard to read the text..... and the PRESS START is hidden under caremusai's sprite"***
- **A tilemap entry's high nibble is its palette bank.** Vanilla writes **15** on all 640 tiles of `copyright_press_start`; `tools/gbastrip.py` rebuilt the map from tile indices alone and wrote **0**
- **Bank 15 is the background palette. Bank 0 is the wordmark's.** So PRESS START, the copyright line and all four screen fills started taking their colours *from the ramp that draws DAEMONS* — **yellow text on a yellow band** — and the "stripes" nobody chose were the wordmark's own gradient leaking out behind it
- **The blink died in the same nibble**: `Task_TitleScreen_BlinkPressStart` writes entries 1-5 of bank 15, and nothing was reading bank 15
- ***One nibble, four symptoms, and every one of them looked like a taste problem***

### `tools/gbatitleview.py` — the screen, composited outside the machine

- **The layout was being fixed by squinting at emulator screenshots**, which is how the creatures came to stand on the words. This composites the real tiles, maps and palettes at the real coordinates, following the GBA's own rule that **an OBJ draws above a BG of equal priority**, and reports every layer's ink box
- **A collision is now arithmetic**: DAEMONS x 26-228, the edition name x 100-153, PRESS START 89px wide, a 64x64 creature about **31px either side** of its centre

### The layout, and it is all whole tiles

| | was | is |
|---|---|---|
| the two creatures | 76 and 164 | **50 and 190** |
| PRESS START | y 129-135, x 43-131 | **y 137-143, x 75-163** — one tile row down, four tiles right |
| the copyright line | centred on 256 | **centred on 240**, which is what the GBA shows |
| the ground | the wordmark's ramp | **`tools/gbatitlepal.py`** — cold slate under CONTENT, deep violet under CONTEXT |

- **`gbastrip.py` is idempotent now.** It rebuilds the screen from its own output, so a second run shifted PRESS START off the row it had just moved to and erased it — *caught by running it twice, which is the house rule anyway*
- **The creatures breathe**, a quarter cycle apart. In lockstep it reads as one animation played twice

### Kept on the books

- **The sixteen-frame intro is deferred, not abandoned** — as *our* sixteen frames, sketched in `docs/intro-sequence.md`. It is not back yet because the screen it hands over to could not be read, and *that is the wrong order to build in*

## v11.56 — 2026-09-04

### The theme had the right notes and the wrong machine

- ***C# major, 152 BPM, 68 melody notes, key confirmed at 0.88 — and it came back as*** **"it sounds like the past gameboy like music"**
- **`mid2agb` emits a `VOICE` byte only where the MIDI carries a program change**, and `tools/mp3midi.py` emitted none. Every track played **slot 0 of `voicegroup137` — a keysplit, with `voice_square_1` at 1–3.** *PSG square waves, on hardware that carries a sample ROM*
- **The transcription was never the problem.** 11.55 fixed silence by adding a program change and stopped there; **`VOICE, 0` is not a neutral default, it is a specific and wrong instrument**

### `tools/gbavoices.py` — Gen 3's banks are General MIDI

- ***`voicegroup149` puts glockenspiel at 9, tubular bell at 14, harp at 46, timpani at 47, oboe at 68 and flute at 73*** — **GM 10, 15, 47, 48, 69 and 74, zero-indexed, exactly.** So a bank is addressable by ordinary program number
- **A Steinway, an SC-88 string ensemble, trumpets, french horns, a choir and timpani are already in the ROM**, scattered across banks that no single song draws on. *`voicegroup191` collects them into one GM-mapped bank*
- **Unused slots hold the piano, not vanilla's square-wave filler** — *a program number we did not intend should still arrive as an instrument.* The failure mode that started this was silence and then a square wave

### Three channels was the Game Boy's number and I ported it anyway

- **Vanilla's `mus_vs_trainer`, `mus_vs_gym_leader` and `mus_vs_deoxys` all run ten tracks.** 7.14g asked for the lift to come *from the arrangement* — and the arrangement had been capped at a limit that belongs to the other engine
- `mus_title` is now **five**: trumpet, glockenspiel doubling it, string ensemble, fingered bass, and **timpani on the downbeat**
- **`engine/` is untouched and stays at three.** *That constraint is real there*

| | |
|---|---|
| `mus_title` bank | `voicegroup137` → **`voicegroup191`** |
| tracks | 3 → **5** |
| programs emitted | `0, 0, 0` → **`56, 9, 48, 33, 47`** |
| the other twelve ported songs | **still `VOICE 0`** — they are Game Boy compositions, and that is a decision, not an oversight |

## v11.55 — 2026-09-04

### The front door moves to **C#**

- 7.14g first put it in C because *the title was in the key of the town you leave from* — Blanche is C pentatonic. **9.14 then established that the front door is not in the world**, which is why colour could be spent there without breaking invariant 5, *so it obeys the author rather than the map*
- **`SeeingSharp`, the language and the pitch are the same word three times.** The cost is named: the door stops feeling like somewhere you have been, and instead sits **a semitone above everywhere you are about to go**
- **The first Suno prompt was correct and boring.** It asked for *sparse, unhurried, dry* and got a lullaby. 7.14g's finding was that the **tone** was wrong, and *tone is not key alone* — the lift belongs in the arrangement, and it has to survive three channels, so **the drive goes in the bass line** rather than in a kit that gets dropped

### `tools/mp3midi.py` — the transcription is DSP, not a prompt

- ***Gemini answered `NO AUDIO`, and that is the gate working.*** 4.9 records what happens without it: a model that cannot hear hands back an earlier answer and admits in its own `DOUBT` field that it guessed. **When the gate fires, the answer is not a better prompt — it is to stop asking**
- **librosa was already on the machine.** Beat tracking gives the grid, Krumhansl-Schmuckler gives the key by correlating the chroma against twenty-four profiles, and `pyin` gives two pitch tracks. *Nothing in it is an opinion*
- **Three voices, because the engine has three**: melody above 250Hz, bass below 300Hz, and a middle voice that is the strongest chord tone per beat which is **neither of the other two** — which is what an arpeggio is
- ***The pitch track slips and the chroma does not.*** The key reads at **0.88 correlation** while any single note is far less certain, so notes outside the scale are moved to the nearest degree **and the count is reported** — if that count were large, the key would be wrong

### The first track through it

| | |
|---|---|
| asked for | **C# major, 150 BPM** |
| came back | **C# major, 152 BPM** — runner-up G# at 0.70 against 0.88 |
| melody | 68 notes, C♯3–A♯4, opening on **C♯** |
| snapped | 16 melody notes, **10%** |
| motion | 33 up, 28 down |

## v11.54 — 2026-09-04

### The presents scene is code becoming music

- ***The engine already did all of it.*** `sparkles_small` is an **8×8 sprite with a four-frame loop** and `sparkles_big` is **32×32 with four more**, both on one shared palette — so 9.14's transformation is **four drawings and a palette, and not one line of new code**
- **0, then 1, then a note, then a note lit** — and because the field's lifetimes are already staggered by the existing timers, *it converts gradually rather than all at once*
- **The palette is two ramps in one bank**: 2–5 is the code, flat and cold; 6–13 are the note colours. ***Nothing fades between them.*** A particle stops being one thing and starts being the other

### The mark behind the words

- The slot held GAME FREAK's gold flame. **Ours is two rings crossing — a feedback loop stood upright.** The lower one is code and the upper one is music, *each semi-monochrome in its own cold or warm ramp so neither is more than one colour of thing*
- ***Where they overlap, and only there, the palette gets bright.*** That is 9.14's sanctioned spend **stated as a shape** — colour is what arrives when two things that disagree connect — and the scene then spends the next few seconds proving it with the particles. **Nothing says so**
- Shading is by **angle** rather than by a light source, which at 32×64 reads as roundness without costing a ramp

### Not prompted for

- **A quaver at eight pixels square is about a dozen lit pixels, and no image model places a dozen pixels.** Both sheets and the mark are drawn procedurally, in palette, the way the MARKS and the Index box were

## v11.53 — 2026-09-04

### The unused sixteenth type is **ORACLE**

- **Gen 1 calls the slot `BIRD` and Gen 3 calls it `???`**; both mean the same unused type. *In computing an oracle is a black box that returns correct answers **without showing how**,* which is 4.6 stated as a data structure — and it is **six characters**, so 9.12's badge drops no vowel
- Named on both engines and drawn onto the badge sheet. **Nothing carries the type yet**, so it is invisible until something does
- *PRIVILEGE was the other candidate* and was rejected for saying the argument too loudly: invariant 1, and a type badge is somewhere the player cannot avoid reading

### The three birds

- **ZAPDOS → ASCLEPIUS**, and the mapping is *literal rather than thematic*: **Asclepius was killed by Zeus's thunderbolt**, and ZAPDOS is the electric one
- **MOLTRES → PROMETHEUS** — gave mortals fire *and every craft with it*. **ARTICUNO → ORPHEUS** — went below for someone and **lost her by looking back**
- ***All three were punished by the authority that granted them the gift***, for being good enough at it that a line got crossed. **Orpheus is 4.10 exactly**: the one thing he was told not to do was check
- *Health, craft, feeling* — **HP, MP, and no stat at all**, because there is not one for the third. Which is psychology, code and music. **A reason to use them and never a line to write down**

### The intro goes CODEMUSIC, then the door

- Scenes 1 to 3 are the Gen 3 intro — *a creature running through grass, then two facing off, then a fight* — and they were **the one place left showing vanilla creatures**
- ***Filling them is sixteen drawings, twelve of them matched animation frames*** — and matched frames are the thing image models are worst at, because consistency across a sequence is exactly what they do not hold
- **2.4's face-off is our version of that scene and it is on the title now**, where it costs **two** drawings instead of sixteen. *One line to put back, and every asset is still in the tree*

## v11.52 — 2026-09-04

### The title's copyright strip

- It still read **©2004 GAME FREAK inc.** It now reads **(c)'11-'26  CODEMUSIC**, in *the same typeface the boot screen uses*, so the two copyright lines in this game are visibly the same object saying the same thing
- ***It cannot be edited as a picture.*** `copyright_press_start` is a **64-tile atlas, a 32×20 tilemap and one palette bank**, shared with PRESS START — and **PRESS START blinks by toggling palette entries one to five.** The copyright uses 6 to 14, so it does not blink; *anything drawn there has to stay out of 1–5 or it starts flashing too.* Verified after the fact: the new line uses only 10 and 12
- **The old line straddles the band's top edge** — white letters with a **black** outline, upper half on the black above and lower half on the red — and that black is *the same index as the plain black above the band*, so it could not be erased everywhere

### One bug worth naming

- ***The band is its first and last row, not the rows that happen to be mostly red.*** Testing membership in a sparse list said **row 153 was not in the band** — because the old text covered enough of it to fail the count — so **exactly the rows with text on them were the rows that did not get cleared.** The ghost of GAME FREAK survived two attempts that way

### ASCLEPIUS

- Recorded in the shortlist. *The pun is Arceus/Asclepius and on its own it is worth nothing.* **What is worth a slot is that Asclepius was struck by lightning for raising the dead** — not for failing and not for malice, but for being good enough at it that a line got crossed, destroyed by the thing that had authorised him. **That is 4.6 and 4.10 in one word**, and the three birds are the only unnamed legendaries

## v11.51 — 2026-09-04

### `defeated` → **outscored**, at last

- **237 decided this in August and the GBA never got it.** *A trainer battle is a BENCHMARK and a benchmark yields a **score**; defeated is the language of combat, outscored is the language of evaluation* — which is what the Review Board will later do to the player. Eighteen occurrences
- ***One of them had to survive untouched.*** CAIRN says **"That is not a defeat. It is a format I do not have."** — and 5.1 is explicit that he *reframes his own loss as a limit in his reading.* **The word DEFEAT is the thing he is refusing**, so renaming it would delete the line's whole move. It is protected by name
- **Erika concedes *the score*** rather than a defeat — 237 read forwards instead of substituted into

## v11.50 — 2026-09-04

### The word the rename table never ruled on

- ***"RIVAL AL would like to battle!"*** — and **battle is not in the table.** 237's whole move is away from combat language (*outscored* not defeated, *HALTED* not fainted, *DETACHED* not ran), and this was the last of it left in plain sight
- **There are two of them.** The **challenge** is an event — twenty occurrences, *"would like to battle", "want to battle"* — and it is now **ENGAGE**. The **state** is a context — *"in battle", "outside of battle"*, ninety-two of them — and **engage does not substitute for a context**, so those are left until there is a decision
- *Six letters for six*, so **not a line had to be rewrapped**

### And a hole in the pane rule

- The repair caught strings that had *already* gained a line, but the JSON **conversion** path still used the old budget — so a string that **changed** could gain one. VS SEEKER came back **four lines deep in a three-line window**
- Both paths use the same bound now

## v11.49 — 2026-09-04

### The front door has art

- **Five assets through `tools/gbatitle.py`.** The wordmark and both edition logos are **in the ROM**, verified against the compressed intermediates rather than the PNGs. The two face-off figures convert clean — **14 and 15 of 16 colours**
- ***And the face-off is on screen.*** Two **64×64 OAM sprites** replace the box-art creature, which is now blank: *Charizard behind our two daemons was never the plan*
- **The sides swap between editions and the poses do not.** Each creature is drawn once facing right; whichever stands on the right is **flipped**, so both face the gap and *the one that lunges is still the one that lunges.* **2.4 warned that a wholesale slot swap makes CAREMUSAI lunge and the chart argue the opposite thing** — a hardware flip cannot do that
- **64×64 is the frame 9.4 refused to upscale into, and neither is upscaled**: CODEMUSAI is 48, CAREMUSAI is 56, each sits inside it untouched

### What real Gemini output taught the tool

- **It came back as RGBA**, and PIL's default composite for a dropped alpha is **black** — which would make the whole surround read as subject
- **It came back as JPEG**, and a codec puts a ramp on every hard edge by construction, so the anti-aliasing check *cannot tell the artist's from the codec's.* Say so and threshold anyway rather than refuse a good drawing
- **Ink on a border means the crop went through a letter** — the CODEMUSIC wordmark's final C is cut, and that is reported rather than silently accepted
- ***Vanilla's 256×64 logo is side by side***, the big word left and the edition stacked right, while ours came back **stacked at 1.87:1 into a 4:1 slot**. Letterboxing would have wasted half the strip, so the tool finds the blank band between the two words and **recomposes**
- **The palette must be exactly sixteen entries.** Padding to 256 made gbagfx emit a *4bpp sprite carrying an 8bpp palette*

### `docs/vocabulary-candidates.md`

- The 114 keywords, checked against every name already spent, kept as a **standing shortlist** to draw from when naming reaches daemons and items

## v11.48 — 2026-09-04

### `tools/gbatitle.py`

- **Four assets, three formats, and none of them is "a PNG."** The two figures are 64×64 4bpp with index 0 transparent and index 1 a **protected outline** — generated art puts hundreds of nearly-black pixels on an edge and a median cut will merge them into the darkest body colour, leaving the creature with none. The logo is 8bpp, so only size binds
- ***The CODEMUSIC wordmark is not one bit***, which the brief claimed. It is L mode carrying **4bpp indices times seventeen** — 0 for the letters, 255 for the ground, two shades between — verified by round-tripping vanilla's own art back through and getting `[0, 17, 34, 255]` out
- **It refuses rather than guesses**, and the anti-aliasing check reads the **source**, not the resample: LANCZOS creates intermediate values by definition, so checking afterwards rejected vanilla itself

### `docs/vocabulary-candidates.md`

- **114 terms checked against every name already spent.** Ten are live game names — MANIFOLD, PING, DEADLOCK, BROADCAST, CANON, BUFFER, BIND, SLEEP, EMBEDDING, RESOLVER — and **ENTROPY and EMERGENT are types**, so *Emergence* is spoken for. The forty-odd that matched only the bible's prose are free
- **2789 already named the hole**: six FLYING moves is the whole VECTOR pool, LATENT is thinner, and *CONSENSUS is the precedent that the fix belongs in `moves.asm`.* Moves are also the cheapest thing here to be wrong about — five tables to add, one string to rename
- **SENTINEL is free**, and *the echo is the whole argument in one word*: a sentinel watches and does not act, a sentient thing is one there is something it is like to be, and **the two are unrelated and sound as though they must be**. Which is why it must never be explained
- ***And nine of them are the thesis with its coat on.*** ALIGNMENT, AUTONOMY, AGENCY and the rest — **an item called ALIGNMENT says it on a menu screen the player cannot avoid.** Spend those on paperwork nobody explains, or not at all
- *Nothing implemented.* Naming is the author's, and **8.6's binding finding is that the bible is outrunning the slice**

## v11.47 — 2026-09-04

### PP reads as MP

- **`{PP}` is not two letters** — it is one compressed glyph, `F9 06`, which the text engine resolves to **cell 0x106** of the latin font sheet. The summary screen draws it at x=36 and the number at x=46, so the whole label lives in **ten pixels**; MANA is twenty-four and would run over the number
- **MP is the same two characters**, so every literal changes width by nothing and only the glyph's left half had to be drawn. The font's own M is six wide where the glyph allows five, so it uses the **four-pixel M from `latin_small`**, which was designed for that width. `latin_small`'s own copy packs each P into three and is **declined rather than mangled** — `{PP}` is drawn once, in FONT_NORMAL
- ***And the pane rule learned two things.*** `fit_to` searched upward from a string's own widest line, which called GRUDGE a fit at **178px in a pane that holds 108**; it searches the whole range now, narrow to wide, checking width *and* line count. And the rule only holds **where a file feeds one pane** — `battle_message.c` does not, so a file-wide bound there measured a two-line string against a twelve-line ceiling

### 9.14 — the front door

- **Colour is sanctioned a third and last time**, and 2586 is the reason it can be: the greyscale is a *spending decision*, not a mood. It has gone to the Review Board and to TYPE; this is the rest. Both scenes sit **outside the fiction**, so the spend is on one claim, stated twice — ***colour is what arrives when two things that disagree connect***
- **The face-off is the one 2.4 already designed**: CODEMUSAI against CAREMUSAI, LOGIC failing against CONTEXT. *And its warning carries over* — **CODEMUSAI lunges, CAREMUSAI opens**, the sides swap between editions and **the poses do not**. Free here, because the swap is a hardware flip: one drawing each
- **`box_art_mon` is a 96×96 background block on one palette and two creatures do not fit**, so they become **OAM sprites at 64×64** — the frame 9.4 refused to upscale into, and both sit inside it untouched at 48 and 56
- **The connection is the particle system that is already there.** Ten frames per particle: *nought to five carry it inward, six to nine are the bloom.* No new sprite slots, no new tasks, and the bloom stays **abstract**
- The presents scene reuses the sparkle field's own tunables, so **0 and 1 become notes mid-flight** and the staggered lifetimes convert the field gradually rather than all at once

### `docs/gemini-prompts-title.txt`

- **Gemini draws the two things that need an artist** — the face-off figures and the wordmarks — *and not the particles.* A musical note at sixteen pixels square is nine lit pixels, and no image model places nine pixels; those are drawn procedurally, as the MARKS and the Index box were

## v11.46 — 2026-09-04

### Found by playing it

- **LEFTOVERS stopped mid-sentence and waited.** Rewrapping had put a scroll break into **158 item descriptions** — the JSON handler never got the rule the src pass has, and a description pane shows every line at once
- ***And the line count itself had moved.*** `own_budget` is the widest line a string uses, which is a lower bound on the pane, not the pane. The rewrap now widens up to the widest line the **whole file** uses — which the pane demonstrably holds, because vanilla shipped it — and stops as soon as the count is back where it started
- **The cause was mine.** 229 is precise that *Remote* replaces what every name-prefix expands to before a **NAME**. Vanilla writes that as capital `Foe` and uses it **four times**; lowercase `foe` is the common noun and appears **308 times** in prose. Renaming the noun too pushed **115 move descriptions** onto a fifth line of a four-line pane, and *"the remote is attacked with a sharp chop"* was never the design
- ***The word-boundary bug caught me a fourth time***, in my own repair script: an escape is two characters and the first is a letter, so **59 line-initial occurrences were invisible**. Stash the escapes. Every time

### Corrections

| | |
|---|---|
| the lab sign | **CRYSTAL CLEAR RESEARCH LAB** — 1535 wants her surname on anything formal |
| the Meeting Room minutes | **"The two present could not follow."** |
| the requisitions board | **CC-7 COGNITIVE CLARIFIER MODULE** — Gen 3's box has room for the word |
| the Index's caught marker | **a box, not a POKé BALL** — the one place the old noun survived as a *picture* |
| MOM, and the Silph president | **nobody is a boy or a girl** |

- ***A multi-page sign is prose on a sign, not a panel.*** QUICKSILVER / The Metal That / Will Not Set is three lines by design; the requisitions board is five pages of sentences that merely hang on a wall, and Gen 1's eighteen-character wrap wasted a box twice as wide
- **Gen 1 hyphenates across those narrow lines**, so `Counter-` + `signed.` joined as *"Counter- signed"*. A route sign reads `BLANCHE TOWN -` / `CALLOW CITY` though — **what sits before the hyphen tells them apart**
- **The player is LOGIC or INTUITION, not a gender.** Gen 3 branches MOM's line on the gender flag, which in our game *is* that choice, so she said *"All boys leave home"* or *"All girls dream of traveling"* depending on which you follow. Both say **Everyone** now. *The other gendered branches are not address*: Route 12's two variants are identical, and the Copycat's differ in manner of speaking, which under LOGIC and INTUITION is apt rather than wrong

## v11.45 — 2026-09-04

### Every Game Boy dialogue block is now accounted for

**569 blocks: 536 matched, 4 handled elsewhere, 29 vocabulary-only, 0 without a home.**

- ***Half the remaining list was never work.*** A block whose only edit was a rename has nothing to carry — `port_vocab.py` and `port_oak.py` already made that change on the Gen 3 side, independently and everywhere. **29 of the 48 were that**, and counting them as unported made the backlog look twice its size
- **`#DEX` was detokenising to `DAEDEX`**, which neither tool knew. It reads as vanilla `POKéDEX` now, so Gen 1's line looks like Gen 3's line for matching and `port_vocab` turns it into INDEX afterwards — which is where that rename lives
- **`CeladonMansion` is the apartment block in Celadon, not the Pokémon Mansion on Cinnabar**, and a fuzzy name match reached for the wrong one. *The threshold refused to place them, which is the system working* — nothing wrong was written. Audited every pairing: the only ones whose names share no token are the four deliberate aliases
- **Nine placed by hand** where the scoring could not decide and a person could — Bruno's first meeting (the tie the margin correctly refused to break), the three starter prompts, Scorn's introduction, the binding tutorial, the carved stone in the forest
- **Two merged.** Gen 1 splits CAIRN's award and its explanation across two blocks; Gen 3 says both in one, wrapped around the badge fanfare, so that block is written out with its control codes intact

### The nameplate said BROCK while he said "I'm CAIRN"

- 5.1 names him CAIRN and the gym dialogue has said so since 2026-08-30, but **neither engine ever renamed the trainer** — at hour two of the slice he introduces himself as CAIRN and the battle nameplate read BROCK. Five characters; the field holds twelve
- **His party needed nothing.** GEODUDE and ONIX are ROCK, and `[TYPE_ROCK]` is LEGACY, so *"his daemons are LEGACY — old formats, still readable"* was already true. The species names are still vanilla, but that is the bestiary's work
- He is the only leader with this gap: **the other seven have not been written yet**
- **The eight MARKS reached dialogue too.** They have UI strings, but a badge is not an item in Gen 3, so `port_names` had no table to learn them from and the prose still said BOULDERBADGE — twelve literals, plus twenty-six mentions of BROCK

### CLAUDE.md said the GBA spike was still open

- vision **3405** records that the spike answered its question in a day and the project pivoted; CLAUDE.md still said *"do not port work into it and do not port work out of it."* **A future session would have read the wrong instruction** and hesitated over work that is now the main line

## v11.44 — 2026-09-04

### The catch-up sweep

***The port tools all reported success and the game still said POKéMON.*** `pokered` writes the core noun as the charmap glyph `#`, so one line renamed it everywhere; `pokefirered` spells it out in every string. **The Game Boy build got its whole vocabulary from one character and the GBA build had inherited none of it.**

- **`tools/port_vocab.py`** — 1595 blocks in 242 files, plus 300 single-line and 121 multi-line `src` literals and every tracked JSON. The map is **derived**: species, moves and items diffed out of our own GBA tables against upstream; the vocabulary lifted from the Game Boy diff
- **Singular and plural is not derivable.** `pokered` had `#MON` and `#MONS` and the Game Boy pass chose by hand **586 times** — *"your" is plural 7 times and singular 25.* The heuristic **agrees with those decisions 93.7%** of the time, scored against them
- **Trainer classes**, the **Remote** prefix and **DETACHED** (1.4, vision 212–235), the **box line** including two-word names, and **`{PKMN}`** — a control code that renders the noun, so it expands *before* the plural decision

### The town names were in nobody's repository

- `port_names.py` wrote them into **`region_map_entry_strings.h`**, which is *generated* from `region_map_sections.json` and **gitignored**. All sixteen existed only in one working build; **a fresh clone would have built vanilla Kanto**
- Renaming a mapsec renames a generated C symbol `region_map.c` refers to by hand — and the generator works on **bytes**, so `é` is two underscores

### One bug, in three tools

- **An escape is two literal characters and the first is a letter**, so in `\nPOKéMON` the `n` sits against the `P` and **`\b` finds no boundary**. Every word at the start of a line was invisible: **104 substitutions** in `port_vocab`, a name wrapped mid-word in `port_dialogue`, **two fame checker blocks** in `port_oak`
- *Each was found by re-running a tool that had already reported clean*

### Measuring a line

- A control code **draws nothing, draws one glyph, or expands to a word** — counting the third as zero wrapped strings to widths they never had, and counting `{CIRCLE_2}` as a name made `help_system.inc` measure 80px too wide
- **A control code can contain spaces**: splitting on whitespace tore `{CLEAR_TO 56}` in half and the Safari menu came back as `{PALETTE` / `5}{COLOR_HIGHLIGHT_SHADOW`
- **A string that positions its own text is a layout**, not prose
- **`\l` scrolls.** A dex entry, a move description and a quest log line show every line at once; rewrapping had introduced **355 scroll breaks** into files that never had one

### Also ported

- **521 dialogue blocks** (from 488) — the tie-break no longer rejects twins, the threshold moved to 0.48 after sampling, and fourteen more maps found their Gen 3 name. *pokered calls it `<Town>Pokecenter` and pokefirered calls it `<Town>City_PokemonCenter_1F`, so the tool states the rule rather than nineteen aliases*
- **The twins threshold stayed at 0.85 after testing 0.80**: it gained exactly one block — Bruno's pre-battle line — and put it on his **rematch** intro rather than his intro. *The margin was right to flag it*
- **An escort plays the theme of the place it happens in** (2422). Gen 3 spends that cue as `MUS_FOLLOW_ME`; Pewter's three and Pallet's one now play their own town's theme. Pallet's is the first escort the player sees, and a jaunty vanilla tune over the opening walk would undo the front door
- **The binding sound.** Our `caught_mon` is *tone* data, not noise, so the music parser carries it — the only difference was the label, `SFX_X_Ch5:` against `Music_X_Ch1::`. Its pair, **UNBOUND, stays unported**: it is noise-channel only, the GBA reaches PSG noise through a voicegroup rather than a note, and guessing at that without hearing it is worse than leaving it
- **CONSENSUS** at move 355 — Gen 3 makes no `NUM_ATTACKS == STRUGGLE` assertion, so it appends and nothing shifts. Five tables, PIN_MISSILE's animation, `TYPE_BUG` per invariant 6
- **The eight MARKS** on the trainer card — Gen 3's badge palette already carries a grey ramp
- **Eight more music tracks** — only four of twelve had ever been carried
- **Two signs** the Game Boy added, placed by *reading the map blockdata* for a wall with floor below it
- **A SMOKE BALL is not a box** — hold items, not capture devices

### Where the GBA build stands

| | |
|---|---|
| vanilla vocabulary left in `src/` and `data/` | **0** (one source comment) |
| dialogue blocks ported / listed | **521 / 48** |
| music tracks | **12 / 12**, plus the binding sound |
| Index entries | **30 / 30** both editions |
| still open | the 48 blocks, the UNBOUND noise cue, the intro and title art |

## v11.43 — 2026-09-03

### The dialogue port — 488 blocks of our own writing, carried across

- **`tools/port_vocab.py` made the GBA say DAEMON. It did not carry one sentence we wrote.** That lived in `engine/text/` — 165 files — and now **488 blocks of it are in the GBA build**: the Quicksilver signs, SCORN SOLUTIONS over CLEAR LABORATORY, Holt's house, the gyms

#### Nothing is matched on our own text, because our own text is the thing that differs

- The pairing is done on **vanilla**: Gen 1's original line against Gen 3's original line, each taken from its own fork's `upstream/master`. Where those agree, the Gen 3 block is *the same NPC saying the same thing*
- **Labels are no help** — `_CinnabarIslandSignText` on one side, `CinnabarIsland_Text_IslandSign` on the other — *but the words survived the generation*
- Checked against known ground truth: all five Quicksilver blocks landed on the right label, including one scoring only **0.57**

#### A threshold alone is not enough

- ***The winner has to beat the runner-up.*** A near-tie means two Gen 3 lines fit equally well, and **putting our writing in the wrong NPC's mouth is worse than not porting it**. The margin caught five bad matches an absolute cutoff had accepted — among them a Viridian Forest gate line that had landed on a bug catcher
- Thirty-one map aliases, because pokered names rooms nothing in pokefirered is called: `CeladonMart1F` → `CeladonCity_DepartmentStore_1F`, `MrFujisHouse` → `LavenderTown_VolunteerPokemonHouse`, `BluesHouse` → `PalletTown_RivalsHouse`

#### A sign is not prose

- pokered breaks **QUICKSILVER / The Metal That / Will Not Set** across three lines *on purpose*, and reflowing it to fill a wider Gen 3 box destroys the thing it is doing — vanilla keeps its own signs broken the same way. **`...SignText` blocks keep their shape**; only lines that cannot fit are split

#### What is left, named rather than dropped

- **81 blocks in 45 maps** have no confident Gen 3 home — FireRed rewrote them past recognition, or two blocks fit equally well. Listed in **`docs/port-dialogue-remaining.md`**, regenerable from the tool
- *An unported line we know about is worth more than a line dropped into the wrong mouth*

## v11.42 — 2026-09-03

### The vocabulary pass — 1595 blocks in 242 files

- ***The Game Boy got this almost for free and the GBA cannot.*** `pokered` writes the core noun as the charmap glyph `#`, so **one line** — `charmap "#", $54` — renamed POKéMON everywhere at once. `pokefirered` **spells the word out in every string**, so the same rename is a few thousand substitutions with every touched line rewrapped
- **`tools/port_vocab.py`** derives its map rather than declaring it: species, moves and items are diffed out of *our own GBA tables* against upstream (43 renames) — **if the Index says PACKET, the NPC has to say PACKET** — and the rest is lifted from the Game Boy diff (`ROCKET`→`CORPUS`, `TRAINER`→`USER`, `catch`→`bind`, `BADGE`→`MARK`, `fainted`→`HALTED`, and eleven town names)

#### Singular and plural is not derivable, so it was measured

- `pokered` had **two spellings**, `#MON` and `#MONS`, and the Game Boy pass chose between them **by hand 586 times**. *"your" is plural 7 times and singular 25* — no rule recovers it
- The heuristic here (quantifier before, plural verb after, and the verbs you actually used — *catch, raise, trade*) **agrees with those 586 decisions 93.7% of the time**, scored against them. It recovers **115 of 121** plurals. *The remaining ~6% will read singular where you wrote plural*

#### A boundary bug that hid 104 substitutions

- An escape is **two literal characters and the first is a letter**, so in `\nPOKéMON` the `n` sits against the `P` and **`\b` finds no boundary**. *Every word at the start of a line was invisible to the tool.* Escapes are now stashed behind a non-word sentinel first
- *Caught by re-running the tool*, which reported clean and left 104 in place

### Also ported

- **Trainer classes**: `POKéMANIAC` → **ARCHIVIST** (both entries), `TEAM ROCKET` → **TEAM CORPUS**
- **The parcel says what it is.** Game Boy capped item names at 12 and it was `CC-7`; GBA allows 14 but no shipped name exceeds 12, so the item is **`CLARIFIER`** and the dialogue now reads **the COGNITIVE CLARIFIER** in full

## v11.41 — 2026-09-03

### OAK is gone from the GBA build — 84 blocks in 25 files

- **`tools/port_oak.py`** applies the table `vision.md` settled once on the Game Boy side: `OAK:` → **`CRYSTAL:`**, `PROF. OAK` → **`CRYSTAL CLEAR`** *with no title*, `OAK'S PARCEL` → **the PACKAGE**. Reports without `--write`, like every other port tool
- **The rewrap is measured, not counted.** `src/text.c` carries FONT_NORMAL's advance widths and `charmap.txt` maps character to glyph, so a line's width is arithmetic. Budget **196px** — the widest line vanilla ships in any map `text.inc`, and 26 tiles is every standard message window. The intro and help system get **220px**, which is what *their* wider windows hold
- *Identifiers are not text.* `PalletTown_ProfessorOaksLab` is a directory, `gOakSpeech_` a label, `B_WIN_OAK_OLD_MAN` an enum. **`ROAK` stays** — it is a rival name you can pick

### A name split across a line break

- Vanilla wraps **`PROF.\nOAK's POKéMON SEMINAR`** *mid-name*, so the pattern never saw it. **Two blocks survived the first pass and only the second run of the tool found them** — a reflowable block is now flattened *before* it is renamed. *The tool being idempotent is what caught this*

### The gender sweep, again

- **She is not a he**, and 4.3 has been caught by this once already. Fourteen pronoun repairs, applied **only inside blocks that name her** — which is why `VermilionCity` survives untouched: its *"he"* is the **other AIDE**
- Agatha remembered her as *"tough and handsome"* → **"tough and striking"**
- `TRAINER_PKMN_PROF_PROF_OAK` was `TRAINER_ENCOUNTER_MUSIC_MALE`; the fame checker's (unused) gender table had her `MALE`. Both flipped

### Four fields where CRYSTAL CLEAR does not fit

| field | cap | resolution |
|---|---|---|
| `struct Trainer` name | **12 bytes** | **`CRYSTAL`** — the battle nameplate takes the short form |
| quest log location | 144px observed | **`CRYSTAL CLEAR'S LAB`** (108px) |
| PC menu option | 104px | **`CRYSTAL CLEAR's PC`** — 101px, *fits* |
| fame checker name | message box | **`CRYSTAL CLEAR`** — 78px, fits |

- The wrapper never breaks **CRYSTAL CLEAR** across a line. *The surname is the device; splitting it is losing it*
- The intro's self-introduction is **`My name is CRYSTAL CLEAR.`** in full, per 4.3

- **Verified in the ROM, not the source**: `PROF. OAK`, `OAK:` and `OAK RESEARCH` are absent from all three `.gba` files through the charmap; `CRYSTAL CLEAR` and `CRYSTAL:` are present

## v11.40 — 2026-09-03

### SONG was walking the sound effects

- **The song table is not interleaved, and I had the halves backwards.** `SE_USE_ITEM` is **1** and `SE_POKE_JUMP_FAILURE` is **255**; music opens at **`MUS_HEAL` = 256** and ours close it at **`MUS_BRAZEN` = 347**
- `DbgSongCallback` wrapped to **1**, so SONG was pushing *sound effects* through the BGM player — **255 presses from the first actual track.** SFX worked because 1..255 is exactly the effect range
- SONG now walks **256..347**, SFX walks **1..255**, and neither wraps into the other

### Fly opened the map and could not land

- **Every destination gates on `FLAG_WORLD_MAP_*`.** `region_map.c` returns `MAPSECTYPE_NOT_VISITED` for any mapsec whose flag is clear, and the cursor will not settle on one
- The debug kit granted badges and HMs but no visited flags — *the map drew, and nothing on it was selectable.* The block is contiguous (`PALLET_TOWN` … `BIRTH_ISLAND`, 51 flags), so the kit now sets all of it

### Text

- **"When the two disagree"** → **"When these disagree"**

### Six characters is measured, not assumed

- Packed as tightly as the face allows — real ink extents, one pixel between letters — **`CONTENT` is 32px, `ENTROPY` 32, `CORRUPT` 33, `EMERGENT` 38.** The badge interior is **30**. *Nothing seven letters long fits, at any spacing*

## v11.39 — 2026-09-03

### The badge alphabet is the game's now, not ours

- **Three hand-drawn glyphs were each one pixel wrong**, and only words showed it: a two-pixel **T** stem read as `I`, a tapering **W** read as `V`, a blunt **V** read as `U` — so `FLOW` rendered *FLOV*, `GROWTH` rendered *GROVTH*, `VECTOR` rendered *VECIOR*
- **`tools/gbatypes.py` now lifts A–Z out of `graphics/fonts/latin_small.png`** — `FONT_SMALL`, the game's own half-width face, *already four pixels of ink on a five-pixel pitch*, which is the metric the badge was built to. 8×16 cells, thirty-two per row, indexed by the charmap byte (`A` = `0xBB`)
- The sheet's own shadow is discarded and regenerated, because the badge sits on **eight different grounds**
- The tool's PNG reader learned sub-byte bit depths — the font sheet is **2bpp**, `menu_info.png` is 8
- **Verified in the ROM, not in the PNG**: the `FLOW` badge's four tiles, encoded `& 0xF` the way `gbagfx` does, are present in all three `.gba` files
- *The tell was on screen the whole time* — the species names beside the badges were clear and the badges were not. Same screen, same size, two different alphabets
- `docs/vision.md` **9.12** rewritten; bible now **v11.39**

## v11.38 — 2026-09-03

### SONG played nothing

- **`PlayNewMapMusic` does not play anything.** It sets `sCurrentMapMusic` and arms the map-music state machine, which next runs on a **map transition** — so from inside a menu, or from a field hotkey, it changes nothing you can hear. SFX worked because `PlaySE` starts immediately
- **`PlayBGM` is the one that starts a track**, and it leaves the map's own music state untouched — which is what lets BACK simply play the map song again rather than having to restore anything
- Both the submenu and the SELECT hotkeys had the same bug

---

## v11.37 — 2026-09-03

### A real DEBUG submenu, and a type port that was missed

- **ROVERCUB was reading GROWTH / CORRUPT.** The GBA still had vanilla Bulbasaur's GRASS/POISON while the Game Boy build has had it as single-type GROWTH all along — **renaming a type does not retype a species**, and only one of those two tables had been ported. `tools/port_types.py` carries all 13
- **`START → DEBUG` is a submenu now** — HEAL, MART, SONG *n*, SFX *n*, BACK. Built out of the start menu rather than beside it: `DoDrawStartMenu` calls `SetUpStartMenu` on every redraw, so a flag swapping which items get appended gives a submenu with the cursor, input, descriptions and frame already working
- **The song and SFX numbers live in the menu labels** — `PrintStartMenuItems` runs every entry through `StringExpandPlaceholders`, so `{STR_VAR_1}` shows the current track with no second window
- **Crystal asked twice.** "But first, tell me a little about yourself" was followed by "Now tell me…". The second is just the question now
- **`shasum -c firered.sha1` fails by design** and the docs said otherwise. It proved the toolchain while the fork was pristine; the ROM now carries our content

---

## v11.36 — 2026-09-03

### The black screen, actually fixed

- **`StartMenu_FadeScreenIfLeavingOverworld` fades to black for every callback except SAVE, EXIT and RETIRE** — because those are the only three that *stay* in the overworld. DEBUG stays too, and being absent from that list is what blacked out the screen: it faded out and there was no new screen to fade back in
- **The missing description string was a real bug and a different one.** Fixing it fixed the gibberish and nothing else; the diagnosis that it also explained the crash was wrong
- **The debug kit persists across Continue.** `load_save.c` copies `gPlayerParty` into the save block like any other party — the kit only *runs* at New Game, which is not the same as its results being temporary

---

## v11.35 — 2026-09-03

### The type badges

- **All 17 redrawn** (`tools/gbatypes.py`) — 32×12 pixel art at tile offsets from `sMenuInfoIcons`, indexed by type + 1. These are what the summary screen and the Index draw; `gTypeNames` only feeds the move-select window
- **Six characters is a hard limit** — the face is 4px wide on a 5px pitch, measured off vanilla's own NORMAL/GROUND/DRAGON at exactly 30px of ink. So the long names drop a vowel exactly as vanilla's PSYCHC does: **CONTNT, CORRPT, STRATM, ENTRPY, CONTXT, EMRGNT, HARDND**
- **`CONTNT` and `CONTXT` differ in the middle**, not the end — the pair that most needs to stay apart
- **Only the text is redrawn.** Backgrounds and rounded corners are untouched, because colour is how a type is recognised before the word is read
- **W was drawn twice.** At 4px a W with a middle bar *is* an H, and GROWTH came out GROHTH. Only looking at it catches that

---

## v11.34 — 2026-09-03

### The black screen was a missing string

- **`sStartMenuDescPointers` is indexed by the same enum as the action table**, and `STARTMENU_DEBUG` was added to one and not the other — so the menu read off the end of the array. That was the garbage description **and** the black screen: printing an unterminated string into the help window. One omission, two symptoms
- **The Index's habitat pages are where a process runs**, not where an animal lives — `WHERE THEY RUN`, and *Userland / Branching / Boundary / Stream / Kernel / Stack / Fragmented / Network / Unindexed*. Each is a real place in a computer and still reads as a place
- **START menu reads `DAEMONS` and `INDEX`**
- **Three text fixes** — S.T.A.R.R.'s *no longer **just** information*; ARTSAI's last line rewritten to be readable; Crystal now asks the rival's name *again* rather than *now*
- **The type badges are still vanilla.** They are pixel art in a 128×128 tile sheet, not strings; scoped, not attempted

---

## v11.33 — 2026-09-03

### The Index finished, and a DEBUG entry in the START menu

- **`THE INDEX`** replaces `POKéMON LIST`, and the category line reads `CHANCE DAEMON` rather than `CHANCE POKéMON`
- **Four entries the Game Boy build never wrote.** MUSAI and DEADLOCK were renamed and left with upstream's text; **150 and 151 described only how they came to exist**, which tells a player nothing about what they are for. They say what they *do* now — S.T.A.R.R. reads its own output until what returns is no longer information, and ARTSAI stands where you are standing and brings back what was in neither of you
- **Two categories** — MUSAI is `UNSET`, a variable with no value assigned; DEADLOCK is `BLOCKED`
- **A `DEBUG` entry in the START menu** — full restore and a full bag, findable without being told. The nested MUSIC/SFX browsers are deliberately *not* here: they need another window, another task and a 348-song list, and that is worth building with someone testing it
- **`grep "error:"` hid a broken build.** agbcc prints warnings and then `Error 1` without that word, so a filtered build looked clean while the debug ROM silently kept a stale binary. Same class as the Route 1 music bug; check exit codes

---

## v11.32 — 2026-09-03

### The project pivots to the GBA

- **`pokefirered-daemons` is the engine now.** `pokered-daemons` is kept as a reference and is not updated further; both READMEs say so, with the reasoning and the cost
- **The gender question is gone.** `playerGender` is read 102 times and all but one picks a graphic — the exception called you someone's *son* or *daughter* and now says *child*. Replaced with **"When the two disagree, which do you follow?" — LOGIC / INTUITION**
- **The ID number is derived**, not rolled: an FNV hash of your name, your rival's name, the edition and whether it is a debug build fills eleven bits, and five are chance. The high sixteen stay random because they decide shininess
- **The intro rewritten** — Crystal has no title, because the professor-slot character having no professor is the device; DAEMONS are *companions*, others *BENCHMARK* them; the rival is a grandchild referred to as *they*
- **`docs/gemini-prompts-gba-player.txt`** — the two figures, front and back, with the overworld sheets explicitly excluded and the three arm lessons from the Game Boy build written down

---

## v11.31 — 2026-09-03

### The copyright screen, and debug hotkeys that answer

- **`tools/gbacopyright.py`** — three lines on the GBA copyright screen, in the same font as the Game Boy one. A tile atlas plus a 32×32 tilemap rather than a 31-tile budget, so the text can sit anywhere; 70 unique tiles from 600 cells. A drop shadow the Game Boy could not afford
- **`tools/gencopyright.py` is importable** — its work moved behind a `__main__` guard so the font can be borrowed without generating a Game Boy asset
- **Every debug hotkey now answers** — the POKéCENTER jingle and a message for healing, the item fanfare for restocking, the song number on screen. A tool that changes hidden state silently is indistinguishable from one that did not run
- **`L + B` restores the map's own song**, and the song hotkeys moved to `A`/`B`: holding L does not stop the avatar walking, so `UP`/`DOWN` would have marched you into a wall while browsing

---

## v11.30 — 2026-09-03

### The Index expanded, and prompts for full-colour sprites

- **29 Index entries expanded** (`tools/index_expand.py`) — Gen 1 gives ~108 characters, Gen 3 ~126, so the room is one more short sentence each. Spent as one more **beat**, never on adjectives
- **The Game Boy build keeps the short entries** — 126 does not fit in 108. The two engines now differ by *length*, not by meaning; §8.4's rule is about editions, and CONTENT/CONTEXT are still identical on both
- **`tools/gbacolour.py`** — quantises full-colour art to 15 colours plus transparency. The outline is forced to black before the median cut, or it merges into the darkest body colour and the creature loses its edge
- **One palette per species, shared by front and back** — the front defines it, the back maps into it. The other order would recolour the front
- **`docs/gemini-prompts-gba-sprites.txt`** — 66 blocks, generated from the same type/hue data the sprite tool uses so no prompt can name the wrong colour

---

## v11.29 — 2026-09-03

### The MARKS land after all, and the debug build grows hotkeys

- **The eight MARKS ported** into `src/strings.c`, where Gen 3 keeps badge names as individual symbols. §9.3 had recorded them as unportable — badges have no bag slot and no description, which is true, but **"not an item" is not the same as "has no name"**
- **Four debug field hotkeys**, all held with L: **R** heals the party, **SELECT** restocks balls, medicine, the four inputs and money, **UP/DOWN** walks the song table and plays it. Hotkeys rather than a menu: a submenu is window templates, a task, a callback and a tilemap — a day of UI for tools that exist to save time
- **Two link traps recorded** — an initialised mutable static lands in `.data`, which `ld_script.ld` discards for that object; and a new song object must be named in the linker script or it links as "defined in discarded section"

---

## v11.28 — 2026-09-03

### Brazen gets its own slot, and a wrong claim is corrected

- **Saffron shares `MUS_PEWTER` with Pewter and Viridian**, so putting Slate City in that slot silently gave Brazen the wrong theme. Found by asking the map, not the tool
- **"Adding a song moves every index after it" was false.** The table is positional; a row *appended* shifts nothing. `MUS_BRAZEN` is 347, four lines of registration
- **`ld_script.ld` names every song object explicitly** — a song built but not listed there fails to link as "defined in discarded section". Loud, at least
- `SaffronCity/map.json` → `MUS_BRAZEN`; Viridian keeps `MUS_PEWTER`, which §7.4 says is right

---

## v11.27 — 2026-09-02

### The chart change, built for the first time

- **§2's only matchup change had never been implemented on either engine** — `git diff` on `data/types/matchups.asm` is empty and always was. The one place invariant 3 says the argument lives was still vanilla
- **`CONTEXT ↔ LATENT` mutual 2× is now in `gTypeEffectiveness`** — and it cost **one line instead of three**, because Gen 3 already fixed the Gen 1 `GHOST → PSYCHIC = 0` bug the design was working around, and already ships `GHOST → PSYCHIC` at 2×
- Array bumped 336 → 339; Gen 3 declares the size rather than relying on the sentinel

---

## v11.26 — 2026-09-02

### Music

- **`tools/port_music.py`** — parses our GB channel data and writes MIDI, because pokefirered builds music from `.mid` through `mid2agb`. Nothing can be copied between a hardware sequencer and a software mixer; the notes are re-emitted
- **`titletheme` → `mus_title`, `slatecity` → `mus_pewter`, `thebleed` → `mus_route1`** — each replaces an existing slot, so no constant, table row or index moves
- **Three conversions**: 8 GB ticks = a quarter note and GB octave N = MIDI octave N are both structural; **GB tempo used as BPM is a guess** and the thing most likely to need tuning by ear
- **`brazen` has nowhere to go** — FireRed ships no `mus_saffron`. Reported rather than guessed at

---

## v11.25 — 2026-09-02

### setup.sh had never actually been exercised on a fresh clone

A re-clone put `pokefirered-daemons` on `master` with agbcc gone, and recovering
from that turned up three bugs in the one script whose entire job is recovering
from that.

- **The branch was only set when cloning.** An existing checkout was left on
  whatever branch it happened to be on — which is exactly what a re-clone gives
  you: `master`, none of the work, and no sign anything is wrong. It now always
  ensures the branch, and says so when it switches
- **agbcc was installed into `/tmp/agbcc/engineGba`.** `install.sh` takes a
  path, and `$PWD` was evaluated *inside* a subshell that had already `cd`'d to
  `/tmp/agbcc`. It then printed "built and installed". The destination is
  resolved before the `cd` now, and the script checks the compiler actually
  landed rather than trusting an exit code
- **`$(basename ...)` came back empty** in one shell here, collapsing the target
  to `..` and making git try to clone over the parent directory. Replaced with
  parameter expansion
- **agbcc's build noise is logged, not printed** — it is a 1998 compiler built
  by a 2026 one and the wall of deprecated-prototype warnings looked like a
  failure

---

## v11.25 — 2026-09-02

### 66 sprites, in colour, and invariant 5 gets its answer

- **`tools/gbasprite.py`** — 33 daemons, front and back, into 64×64 4bpp with a 16-colour palette each
- **Nothing is upscaled.** 40 → 64 is a 1.6× resample of hand-tuned pixel art; each sprite is centred at native size instead, which is how Gen 3 treats small species anyway
- **Colour is by TYPE**, so it carries the argument rather than decorating it — the answer §9.3 said had to be made in the bible. Four anchors come straight from §6's humours (sanguine/VECTOR, choleric/ENTROPY, melancholic/LATENT, phlegmatic/FROZEN); the other eleven are new claims
- **The outline stays near-black** — an outline that takes the hue stops reading as an outline
- Palettes are written CRLF, as `.gitattributes` requires, or git rewrites all 66 on every checkout

---

## v11.24 — 2026-09-02

### The port continues

- **`HARDENED` and `OPAQUE`** name Gen 3's two extra types, both read off the vanilla chart rather than invented: DARK is immune to PSYCHIC, so a black box is immune to perspective-taking; STEEL falls to fire, fighting and ground, which is what happens to safety hardening
- **33 daemon names and 12 item names ported** via `tools/port_names.py`, which learns `{vanilla -> ours}` by diffing our table against upstream's and substitutes on the vanilla string — no index arithmetic between two very different data layouts
- **12 item descriptions written** (`tools/port_item_text.py`) — new writing, not a port, because Gen 1 stores none. The box ladder never explains itself
- **Two encoding traps recorded** — the JSON stores `POKé` as `POK\u00e9`, and Gen 3 capitalises `OAK'S PARCEL` where Gen 1 wrote `OAK's`

---

## v11.23 — 2026-09-02

### The port begins, and corrects §9.3 twice

- **All fifteen type names ported** to `gTypeNames`, unchanged from `data/types/names.asm`. The chart is the argument; the port does not renegotiate it
- **`TYPE_NAME_LENGTH` widened 6 → 8.** Vanilla's 6 is why it ships FIGHT/ELECTR/PSYCHC — **six of our fifteen do not fit it.** We assumed the newer machine gives more room everywhere; for the one field carrying the argument it gives less. Cheap to fix, but found by building rather than by reading
- **The MARKS were never getting descriptions** — in Gen 3 badges are not items at all (`items.h` contains `BADGE` zero times). The description win is real, but it belongs to the boxes, the stones, medicines and TMs
- **`tools/gbastr.py`** — searches a `.gba` through the game's own charmap, the GBA counterpart of `verify-sprites`. Caught two stale ROMs on its first run
- **`TYPE_STEEL` and `TYPE_DARK` left vanilla deliberately** — the two extra type names are a bible decision, not a header one

---

## v11.22 — 2026-09-02

### The GBA spike

- **`CodeMusic/pokefirered-daemons` forked**, branch `context-content`. Both editions build and match the retail hashes byte for byte
- **`engineGba/` symlink** alongside `engine/`. Neither vendored, both gitignored
- **`bindDaemons.sh` now defaults to the GBA build**; `--classic` reaches the Game Boy one, which is where the slice is. `--debug` is Game Boy only
- **`setup.sh` clones and wires both**, and builds `agbcc` — which installs *into* the fork and so does not survive a clone
- **A debug build for the GBA** — pokefirered ships none, so `firered_debug` is ours: its own ROM and save, a party picked for abilities, one of each kind of item so the description window can be read, all badges, and hold-B to avoid grass. With `DAEMONS_DEBUG=0` the retail builds still match their `.sha1` byte for byte
- **`vision.md` §9.3** records the case: 334 files of implementation against 5,343 lines of design; abilities and item descriptions are the real argument, not colour; invariant 5 stops being a constraint and the chart goes 15 → 17 types. **A spike, not a decision**

---

## v11.21 — 2026-09-02

### The title screen, in both media

- **`audio/music/titletheme.asm`** — the title screen had been repointed at `Music_Dungeon3`, *Echoes of the Algorithm*, F minor, the track where Crystal goes into the system after the removal. Correct for the cave, wrong for the front door. Now its own theme: C major, I–vi–IV–V, 150 — and C because §7.4 gives Blanche C pentatonic, so the door is in the key of the town you leave from. 96 bytes in bank `$1f`
- **`tools/titleface.py`** — lights the title figure's face after conversion. A wide brim shadows a face by construction and at 40×56 that collapsed to a void. The hat leaves the head three rows, so it is one pixel per eye and two for the mouth; two-pixel eyes read as a visor and rounding the corners put the visor back
- **Both media had drifted dark independently** — a prompt that never asked for warmth, and a repoint that was free

---

## v11.20 — 2026-09-02

### Craft rule 6 governs the art

- **"Is it a dark game?" — no**, and §0.1 rule 6 says so: funny in its ordinary moments, serious in three or four. Scorn is *genuinely warm*, CAIRN *is right*, the silence is *not cruelty*. The design has no villain, and greyscale is a spending decision, not a mood
- **The player prompts had been arguing the opposite.** They asked for "still, composed" and "confident" and never once for warmth, then asked for a wide brim — which shadows a face by construction. All three samples came back faceless
- **A mandatory tone paragraph** on every character prompt: the face must be *one of the lightest areas of the figure, never the darkest*. At 40×56 a face is six pixels; if they are black, the character is a silhouette
- **New title art needed** — the current one cannot be salvaged, the face is a void

---

## v11.18 – v11.19 — 2026-09-02

- **The title figure's shoulder had a bite out of it** — one light pixel in the middle of the black shoulder line, a cell the outline pass grazed but did not cover. **A one-pixel hole on an outer edge does not read as a hole; it reads as a piece missing**
- **`--close` added to `tools/mksprite.py`** — fills one-pixel gaps in the outline, but only where they touch the background. Lowering `--cover` also closes them and thickens every line in the figure to do it; `--close` used *less* black and left zero holes

---

## v11.17 — 2026-09-02

- **`--fill` added to `tools/mksprite.py`, and the title figure reconverted.** Keeping the subject's proportions filled 57% of the slot's width where vanilla's fills 100% — a standing person is 0.43 wide-to-tall and the slot is 0.714, so 43% of forty columns was going to margin. That margin was the missing detail
- **The flared-coat sample was tested and rejected** — at 0.93 aspect `--fill` squeezes instead of stretching, and the coat becomes a grey triangle

---

## v11.16 — 2026-09-02

### The title figure is generated art now

- **`gfx/title/player.png`** converted from a generated illustration through `tools/mksprite.py`, replacing the hand-drawn placeholder
- **`--solid`** added: the title sprite is OAM, where the lightest level is transparent, so a white lab coat renders as a hole. The flood must run at **source** resolution — on the finished 40×56 the outline is one pixel and leaks. 234 pixels of coat would have been see-through
- **Two non-square bugs fixed in the same pass** — the outline pass ran `range(size)` on both axes and covered only 40 of 56 rows; the cropped-too-tight warning divided by `size²`

---

## v11.15 — 2026-09-02

- **The player has feet.** The coat reached the floor, so the hem swung but nothing read as a step and the figure slid like a blob. It now stops one row short, with shoes below — together standing, apart walking, one hiding the other in profile
- **`tools/mksprite.py` takes `WxH`** as well as a single size. A daemon slot is square; the 40×56 title figure was being squashed by a square crop
- **A prompt for the title figure** added to `docs/gemini-prompts-player.txt` — three variations, and what to judge them on (the brim and the hem survive the shrink; the face does not)

---

## v11.14 — 2026-09-02

### The title screen figure

- **`gfx/title/player.png` drawn** at 40×56 via `tools/gentitle.py` — same character, and the first place with room to draw the unit itself. **A first pass; replace it with generated art**, which is proven at this size
- **All three player prompts rewritten** — they still described a cap and a short jacket and would have regenerated the rejected character

---

## v11.13 — 2026-09-02

### The player, redesigned

- **A cap and a strap was Ash with a satchel.** Replaced: the player now sits between a scientist, a magician and a wizard
- **A lab coat and a wizard's robe are the same silhouette** — so the coat carries two archetypes for free and the hat only has to carry the third. A flat brim *wider than the shoulders*; equal width stacks into a mailbox
- **The arms took three tries** — flush black columns read as outline (the figure had none, which is what was noticed), a transparent gap read as a hole through the armpit. Sleeves at level 2 against a torso at level 1 read as arms
- **No legs** — the coat reaches the ground, so the walk is the hem swinging
- **The side view is a real profile now.** A `coat()` helper had quietly made it the front view with a different face, so walking left looked like walking towards you. The frames are written out one by one

---

## v11.12 — 2026-09-02

### The second seat — adopted, not yet drawn

- **The editions differ by seat, not by scene.** The intro's front slot is the player's side; CONTENT sits behind CODEMUSAI, CONTEXT behind CAREMUSAI. Same two daemons, same lunge, same loser
- **The poses do not travel with the slots** — swapping slot contents wholesale would make CAREMUSAI lunge and silently invert the chart. Six new drawings, not a re-crop
- **`docs/gemini-prompts-intro.txt`** extended with the six CONTEXT frames and that warning
- **The `_RED`/`_BLUE` conditional will come back** — its removal earlier today was for a different creature, which is a different argument

---

## v11.11 — 2026-09-02

### The player

- **`gfx/sprites/red.png` redrawn** — six 16×16 frames, hand-drawn via `tools/genplayer.py`. Cap brim-forward, a light strap across the chest, the satchel visible on the back when walking away
- **Vanilla's idiom kept deliberately** — the player stands next to thirty NPC sprites that are still vanilla's
- **`docs/gemini-prompts-player.txt` rewritten** — it had asked for a throwing pose at `gfx/intro/red_nidorino_1.png`, which is CODEMUSAI; following it would have overwritten the intro. Now three prompts (front 56×56, title 40×56, back 32×32) plus the two shrink frames, and the hand-drawn slots marked as such
- **`gfx/sprites/red_bike.png` redrawn** — the same six frames from the waist up, with a bike below the rail; the wheels move and their tone flickers rather than the whole bicycle sliding
- **Still vanilla**: the three fishing frames (16×8) and the three generated pics

### The intro face-off was only in one edition

- **`_BLUE` still included `blue_jigglypuff_*`** — CONTEXT was opening on Jigglypuff. The conditional is removed; both editions share CODEMUSAI, per 8.4 and invariant 3

---

## v11.10 — 2026-09-02

### The eight MARKS have icons

- **`tools/genmarks.py`** draws all sixteen 16×16 blocks of `gfx/trainer_card/badges.png`
- **SLATE / SLOPE / SENSE / FIT / SKEW / FRAME / HEAT / TRUE** — one per benchmark, each the concept §5's table already assigned it; every icon is an instrument or a plot, and the set reads as a bench of measuring tools
- **The unearned state is the same tool as an outline**, not a gym leader's portrait — the toolkit is visible from hour one and fills in
- **`vision.md` §5.2** records the set and why TRUE is a plumb bob

### Cleanup

- **`engine/pokered.gbc` and `engine/pokeblue_debug.gbc` removed** — vanilla-named leftovers containing none of our sprites

---

## v11.9 — 2026-09-01

### The copyright screen

- **`©'11-'26 CODEMUSIC` / `SeeingSharp` / `Psychology/Code`** replace the three vanilla lines
- **`tools/gencopyright.py`** — draws the strip from the vanilla copyright font, recovered pixel-for-pixel, plus twelve glyphs it never had (`S P h l g p y / 0 1 2 -`)
- **31 tiles exactly** (`$60`–`$7E`), all in `copyright.png`. The copy now stops at a new `NintendoCopyrightLogoGraphicsEnd` label instead of spanning into `gamefreak_inc.2bpp` — that asset is printed as a fixed nine-tile run by the title screen and the splash too, and shortening it made the title read `CODEMUSIC AB`
- **`r` re-cut** — it had been split one column late out of the vanilla `re` ligature and kept a sliver of the `e`
- **The title-screen year is no longer blocked** — the 2026-08-29 entry deferred it for want of digit glyphs

### A stale intermediate shipped vanilla sprites

- **NIBBLE appeared in battle as vanilla Rattata.** `gfx/pokemon/front/rattata.pic` carried a timestamp newer than the `.png` it is built from, so make called it up to date and every ROM linked after that point embedded it
- **A `.pic` is an intermediate** — make deletes it after linking, so the offending file was gone before it could be inspected, and rebuilding it from the art on disk gives a different size (157 bytes, not 215): it was never built from our sprite
- **`make verify-sprites`** — rebuilds all 64 daemon pics and searches each ROM for their exact bytes. Compiling is not evidence; this is the same reasoning as decoding the ROM with the charmap to check strings
- **`context-debug` had never been built this session** — three of four ROMs were being rebuilt

### The intro face-off

- **CAREMUSAI un-mirrored** — the pair now face each other

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

### A stale intermediate shipped vanilla sprites

- **NIBBLE appeared in battle as vanilla Rattata.** `gfx/pokemon/front/rattata.pic` carried a timestamp newer than the `.png` it is built from, so make called it up to date and every ROM linked after that point embedded it
- **A `.pic` is an intermediate** — make deletes it after linking, so the offending file was gone before it could be inspected, and rebuilding it from the art on disk gives a different size (157 bytes, not 215): it was never built from our sprite
- **`make verify-sprites`** — rebuilds all 64 daemon pics and searches each ROM for their exact bytes. Compiling is not evidence; this is the same reasoning as decoding the ROM with the charmap to check strings
- **`context-debug` had never been built this session** — three of four ROMs were being rebuilt

### The intro face-off, and the wordmark corrected

- **The intro squares up CODEMUSAI and CAREMUSAI** — *Penphin's two hemispheres pulled apart*, and the chart makes **LOGIC fail against CONTEXT.** The game opens on its own central argument before the player can read it, and **the one that loses is the one everybody expects to win.** CODEMUSAI lunges; CAREMUSAI opens
- ***The dedup is a VRAM requirement, not an optimisation.*** Dropping it made the tilemaps trivially sequential — and corrupted the entire intro. The scene loads the back-mon sheet at `vChars2` then loads the GameFreak graphics **immediately after it**, so **147 tiles overflows the block** and everything after lands wrong; the splash filled with garbage too. **Deduped properly instead**, in the same column-major order the build reads: **147 tiles collapse to 97**, because the three poses share most of their body
- ***The wordmark was a shade too light, and the cause was mechanical.*** The vanilla splash uses **two ink conventions** — level 1 for the star and mark, **level 0 for every text strip** — and I applied one to all four. **`gamefreak_inc` is now pixel-identical to the version it replaced**
- **The bold font is recovered rather than redrawn** — two-pixel strokes over five rows, proportional, with `P R N T` added to match. The splash strip reads **CODEMUSIC PRESENTS** in the same weight

### The splash is CodeMusic

- **Four tiny assets, no code change.** The falling star becomes **a falling note**; the mark becomes **`{ ♪ }`** — braces are unambiguously code, a note unambiguously music; the strips read **CODEMUSIC**
- ***The sound was already right.*** `SFX_SHOOTING_STAR` opens with `pitch_sweep 2, -7`, a downward sweep — **it was always a glissando and simply had no note attached.** Left alone: the swap makes the existing sound *mean* something
- **Monochrome, deliberately.** Invariant 5 spends colour once, at the Review Board, and **a colourful splash before forty hours of grey reads as a limitation rather than a choice.** Binary and notation are line and shape, and lose nothing without hue
- **Drawn, not generated** — 8×8 is one tile. `tools/gensplash.py`, to the vanilla convention: background level 3, ink level 1

### Route 1's silence, and two sounds

- ***Song ids are computed from header position*** and a 3-channel header eats three. AUDIO_1's table ended at **253**, so appending two songs put them at **256 and 259**; `db` truncated them and **Route 1 pointed at garbage**
- ***The build had been saying so the whole time*** — `Value $103 is not 8-bit` — **and my build checks filtered warnings out.** 7.15 one layer down: measured, printed, and discarded unread
- **Reusing headers costs zero ids and freed two.** The Bleed took `Music_Routes1` (Route 1 and Route 2 — The Bleed and Underpaint); Slate took `Music_MuseumGuy`, which **no map used at all**
- **DAEDEX was a charmap accident** — `#` is `$54` = *DAE*, so `#DEX` rendered DAEDEX. Now `INDEX`, and the diploma had it too
- **The binding sound inverts vanilla's fanfare** — same rhythm, descending, settling on a low held note. *A thing closing, not a prize won*
- **And an unbound daemon has its own cue**, branched on `wIsInBattle` in three instructions. It reuses `SFX_BATTLE_16`, one of two spare headers, and is **noise-channel only** — *a process nobody owns arrives as static, not a melody.* **It rises and stops where the binding sound settles**

### The BIND verb, finally applied

*Caught in play: the capture message still read **PACKET was caught!**. 1.5 settled BIND months ago and 9 had been tracking 57 stragglers.*

- **55 instances rewritten** across dialogue and the battle messages. The only survivor is *catchy tune*, which is a song
- ***And the success message is flat.*** Vanilla says *All right! <NAME> was caught!* — **the exclamation congratulates the player for imposing the contract.** Ours is **`<NAME> was BOUND.`**
- **Nothing else changed.** The failure lines keep their *Darn!* and *Shoot!*, because 1.4's rule **refuses to celebrate, not to punctuate** — a lament is not a celebration. **Only the moment of binding goes quiet**

### The slice is built

- **The eight evolutions are in** — OVERFLOW, RELAY, BROADCAST, FLOOD, INDEXER, INJECTOR, SURGE, HIBERNATE. **Thirty-two daemons now carry original front and back art**
- **Covers swept per sprite again**, and the spread is wider than the wild batch — **0.34 through 1.01 across sixteen files** — which is why this is measured per sprite rather than set per format. All sixteen came back with three even ink levels
- ***8.1's vertical slice is complete.*** Type chart, intro, route signage, CAIRN, Slate's theme and The Bleed's modulation, and every creature between Blanche and Slate named, drawn and filed
- ***The next milestone is 8.6's: Benchmark 1 beaten on hardware.*** Not another section

### The nine wild daemons

- **The starters are paradigms; these are substrate** — the primitives a system is made of, walked through while carrying one way of learning
- **NIBBLE → OVERFLOW**, **PACKET → RELAY → BROADCAST**, **PING → FLOOD**, **CRAWLER → PENDING → INDEXER**, **SCRAPER → BUFFER → INJECTOR**, **SPIKE → SURGE**. Fifteen species, with categories and entries
- ***The pair the set is built around is CRAWLER and SCRAPER.*** Two swarms, the same shape, the same forest — **one follows every link it finds; the other takes the same things by the same method, and nobody gave it permission.** The chart says which is which by making the second CORRUPT, and nothing else has to
- **The lines evolve along processes.** Crawl, queue, index — *what it cannot file, it drops.* The poisoned line is the identical pipeline with permission removed at every step
- ***Two names were already better than the drafts.*** JIGGLYPUFF and WIGGLYTUFF were already **SUSPEND** and **HIBERNATE** — the two real power states, escalating correctly, **rhyming with the man a machine suspended.** `LULL → BLOCK` discarded. **Check before renaming**
- **Zero vanilla wild names remain in the cartridge**, verified by decoding — including one hiding in another creature's Index entry, which the dialogue sweep did not cover

### Slate and The Bleed — 8.1's music

- **Slate is achromatic**, so 7.4 gives it value rather than hue. ***Blanche is C pentatonic — no F, no B — and Slate is that scale with both gaps filled.*** **The first town has holes in it and the first benchmark closes them:** Representation as a key signature, and CAIRN's creed in the scale he stands in
- ***And F is the note Blanche does not have** — which is exactly the key 7.4 derives for Callow.* So **The Bleed is the road where the missing note becomes the key**: A-section in C, B-section a fourth up in F
- **Which is what the name already meant.** A *bleed* is one colour carried past its own edge into the next, and a modulation is a key doing that. **The name was the mechanic before anyone noticed**
- **156 bytes for both.** Each needed a new constant and one repointed line, since Slate shared `Cities1` with 37 maps — **an edit, not a budget**
- **8.1's "two city themes and one route modulation" is now done**

### v11.1 — external review, taken and answered

*Read against v11.0 by a second model. Its sharpest finding is about this document: **the bible is outrunning the slice.** Sixteen version bumps in one session and 8.1 is still not beaten on hardware. **Recorded as binding — the next milestone is that, not another section.***

- **One constraint the review did not have: Gen 1 has no item descriptions.** Three proposals put their payload in one. **CC-7's moved into the item name**, which is stronger — the player *carries* the number rather than reading about it; **the RESOLVER's tag moved into Scorn's mouth**; the AXIOM/EMBEDDING/AFFECT documents are deferred until they have a speaker
- **Built: `PACKAGE → CC-7`.** *Crystal Clear's order came in. A CC-7.* / *Ah. The module. Thank you.* **Thirty hours later the same part number is on a door at Quicksilver, with its reason field.** Replaces a custom USERBOX — the wrong gift twice, since a box is 1.3's argument and it copied vanilla's custom ball
- **Built: Scorn at the bottom of the Verdigris basement**, settling 4.5 — the player likes him *before* the tower, so Halftone betrays their own judgment. He hands over the RESOLVER as inventory and dismisses its tag: ***QS-LAB, I think. Before my time.*** Then wishes them luck at the tower
- **Built: his Benchmark 8 accounting**, split with something that cannot answer — ***It has never said otherwise***
- **Built: the catching tutorial** — *you offer it a box. It goes in on its own, or it does not go in*
- **Adopted, not built: Ty is not in the ROM at all.** The post-game triangle is new content rather than edits. Also pending: Penphin as **the architecture that cannot be weighted**, ORPHAN as a Quicksilver process nobody reaped, THE HOLDOUT and the TOKEN garble
- **Declined: moving ROVER out of the starter slot.** The diagnosis was right — 2450 said individuals are not species and 8.2 then made one a starter — but the cure costs two surnames in a Gen 1 bestiary and discards an arc that pays. **2450 is amended instead: a starter may be a named individual**

### v11.0 — CHANCE and INTENT

*Caught in review: the legendaries' Index categories read `ACCIDENT` / `DELIBERATE`, and both halves were wrong.*

- **Mismatched** — one a noun, one an adjective, so the pair never scanned as a set
- ***And `ACCIDENT` mis-framed the event.*** ARTSAI's was **wondrous**; Crystal came back to tell them what she had seen. **Accident frames it as damage** — the institution's reading, not the truth. There is an argument for printing the institution's reading deliberately, since flattening is what the Index does — **but a flattening only works if the player can see it is one**, and at one word in a taxonomy slot they cannot
- **`CHANCE` / `INTENT`.** Both abstract nouns, exact opposites, **neither implying damage**. `INTENT` is the bible's own word for *a comprehension that wakes with an intention*, and **a chance is also an opportunity**
- *The field was never the problem.* Vanilla puts **`NEW SPECIE`** and **`GENETIC`** in exactly these two slots — **origin-as-category is already the convention for the legendary pair**

### The starters are named — all nine

- **`LABL → RUBRIC → CANON`** and **`CLUSTR → LOCUS → MANIFOLD`**, joining the ROVER line. **No vanilla starter name remains in the cartridge**
- ***Corpel* collided with Corpus, and *Canonex*'s `-EX` earned nothing** — it reads as *ex-* or Latin *out of*. The fix gains something: **the names get more formal as the creature gets more authoritative.** *Labl* is barely a word, *rubric* is a technical term, *canon* is an institution — **and a rubric is the marking scheme**, in a world of benchmarks and marks
- ***Nebulon* was not vague, it was backwards.** A nebula is **diffuse, less structured than a cluster**, so the line ran grouped → scattered → structured. **`LOCUS` escalates properly**: points that *happen* to be near → points that share a *rule* → the *surface* they lie on
- **Index entries for all six.** *Someone else decided what it means.* / *Nothing checks the rule.* / ***New things are filed as errors.*** / *Nobody told it which things matter. It has guessed.* / *It cannot say what the rule is for.* / ***It can show you the shape, not a name***
- **The two final stages are the paradigms' failures side by side.** **CANON is accurate and files novelty as error; MANIFOLD finds real structure it cannot name.** One certain and wrong at the edges, the other right and mute
- ***And CANON's line is the Meeting Room minutes*** — *new things are filed as errors* is what happened to a woman who moved between fields, printed in an Index entry two hundred slots from the building it describes

### The ROVER line, and RESONANCE

- **The order is reviewed and kept.** ROVERCUB → ROVERSEER → ROVERBYTE reads **software → infrastructure → body**, and ending in a body is the same shape as ARTSAI coming back real
- **SIGNAL lands exactly there.** Both disembodied stages are pure GROWTH; **the moment it has a body it gains the perception type.** Nothing was arranged for it — it fell out of Venusaur's slot
- ***Prediction arrives one stage before perception.*** A seer sees ahead and a server predicts, so **the system could forecast before it could feel anything.** A real critique sitting silently in an evolution line, and it only works in this order
- **Index entries: PORTABLE / PREDICTIVE / EMBODIED.** *It has no way to choose the route.* / *It has never once been outside.* / ***Everything it predicted, it can finally check***
- **RESONANCE proposed as Penphin's**, completing the signature set: PERSPECTIVE takes **your** frame and loses mine, RECURSION takes **my own**, and **RESONANCE is two frames reinforcing with neither lost.** Penphin is *a logic model and an emotion model that must agree before acting*
- ***And Penphin cannot be obtained alone*** — a trade evolution, because the dual mind requires two minds. **The move meaning *two frames in phase* belongs to the one daemon that requires another person to exist**
- **Behaviour deliberately unspecified.** RECURSION already claims the Bide machinery, and inventing a mechanic before there is a need is how placeholders become canon

### The gilt sign, and TAINT withdrawn

- **In gold `SCORN SOLUTIONS`; underneath `CLEAR LABORATORY`.** Both are a founder's surname plus what the place is, and **the rebrand changed exactly one word: Laboratory became Solutions.** A place that studied things became a company that sells them
- ***CLEAR* is already load-bearing** — Crystal, Ty, Al, and the Cognitive **Clarifier**. Her surname ties founder, family and machine into one word, **and it is the word that got painted over**
- **The acronym is dropped, the name is kept.** iASHC pays nothing — a player cannot unpack it — but *Scorn Solutions* is a name, and it pays twice: the surname and the contempt
- **Built** onto the Quicksilver lab sign, which read `#MON LAB`. *Gold leaf, laid over something. Where it has lifted, the older letters show.* **The player has to look**
- ***TAINT MARK withdrawn.*** It covered Benchmark 5 exactly — contamination and a tainted judgement — and it has a **well-known vulgar reading** that would land as a joke in a game where you *receive* one. **A second meaning the design did not choose is not a second meaning; it is a leak.** **SKEW MARK** pays the same twice and does not: *skew a measurement, hold a skewed view* — and **a weighting is a skew**, the exact operation Scorn performed on the Clarifier

### The badges become MARKS

- **City names do not scale** — `VERDIGRIS MARK` is 14 and `QUICKSILVER MARK` is 16, over the 12-char item cap. So each is named from its **concept**
- **SLATE / SLOPE / SENSE / FIT / TAINT / FRAME / HEAT / TRUE**, each paying twice: the gradient and the terrain, fitness and *over*fit, poison and a tainted judgement, framing and a frame of reference, heat and sampling temperature
- **TRUE MARK earns its place.** Benchmark 8 is Alignment, run by **the man who aligned perfectly to the wrong metric**, and the mark he hands you asks whether *aligned* and *true* are the same word. **They are not, and nothing says so**
- **Three places carried badge strings, not one**: the item names, fourteen gym dialogue lines, and **a second hardcoded list in `scripts/Route23.asm`** for the gate guards. **`BADGE` now occurs zero times in the cartridge**, verified by decoding — the generic plurals and the trainer card's `BADGES` label included
- *Found on the way:* `_CannotUseItemsHereText` was **19 columns**, one of vanilla's four border-clobbering lines. Fixed

### Two events, and what separates them

- **The ARTSAI event and the fire are not the same incident**, and the gap is **not a number of years.** The ROM already fixes it more precisely than a number could
- **The delta is her absence, measured in askings.** The two events are separated by exactly how long it took a machine to stop expecting her back
- **The dates say so.** Mar 4 → Apr 19 → Aug 12 is one spring and summer; the plate says SEPT 3; **the last terminal carries no date at all**, which needs no explaining — the logs stop the moment the person keeping them is gone
- **Crystal causes both events. Once by being there, once by not.** She is present when ARTSAI comes back changed and it is read as her losing the plot; **she is absent when S.T.A.R.R. wakes, and that absence is the cause. The machine's fatal error is her name**
- **The film's version is declined.** A patron funding a weapon and offering to help it focus its power cannot be imported — 4.4 rests on Scorn being likable and optimising the wrong metric, and a sponsor with bad intent makes it a caper. **Nobody funded anything: a man took over a lab, changed what it measured, and the building did not survive it**
- *Also recorded:* Gen 1's mansion is burnt from the incident, and **Cinnabar's volcano is Gen 2**, three years later. Neither is ours

### The Five Witnesses, and the terminal

- **Five existing NPCs repurposed, one per city, no map changes** — Blanche, Slate, Doldrum, Ardor, Verdigris. All five were vanilla filler
- **They contradict on time, on who was present, and on cause**, and every one of them is certain
- **The contradictions now have a cause rather than being arbitrary.** Two describe **form 1** (*purple, all flat faces, like cut glass*), two describe **form 3** (*white, like an ordinary hare*), and one describes ***the change itself*** — her uncle says it changed while he was looking. **Only she is telling the truth about what happened, and she is quoting an uncle** (4.6)
- **Each carries exactly one accurate spatial detail**: far room past the stairs / west side / against the outer wall / below where the roof went in / the room with no window. **Composited they are one room**
- **The terminal is on Mansion 1F**, deliberately not one of the four carrying the 1001 log, so the threads never touch. ***`ITER 35` occurs exactly once in the ROM***, verified by decoding the cartridge
- **Still to build: the hidden object and its event flag.** The accounts give the where and the terminal gives the how far; **nothing yet rewards standing there**

### The MUSAI line gets its Index entries

*Caught in play: SEEKMUSAI still read `LIGHTNING` with Jolteon's negative-ions prose. All four were still vanilla.*

- **Categories `GENERAL`, `DEDUCTIVE`, `RETRIEVAL`, `AFFECTIVE`** — technical register, which 4.9 permits for the Index because **there it lands as jargon rather than insight**
- **MUSAI:** *Runs no module by default. It keeps whatever it is given first.* **Nothing is filed about the rest** — 4.2's thinness, and a general model before fine-tuning
- **CODEMUSAI:** *Given a rule, it will not stop until the rule is met.* ***It does not ask where the rule came from.*** **Scorn's failure as a creature description**, printed by the Index as a spec sheet
- **SEEKMUSAI:** *Nearest is not the same as right.* **Nobody told it**
- **CAREMUSAI:** *Reads the room before it reads the problem. Often correct.* ***Cannot show its working***
- **The last two are the argument.** 2406 has LOGIC failing against CONTEXT; here is why, in the Index's flat voice — **one cannot say where its rule came from, the other cannot show its working, and the chart says the second one wins.** Nobody comments on it

### POKéMANIAC → ARCHIVIST

- ***Maniac* is a pathology word**, and craft rule 3 says name the process, not the pathology. **A game whose central injustice is a woman recorded as unwell cannot have a trainer class called a maniac.** `DAEMANIAC` was considered and fails for the same reason
- **`ARCHIVIST` pays twice**, which is 1's standard: an archivist keeps **records**, and an **archive is stored compressed data** — exactly what a box does to a daemon
- **And it is precisely right for HOLT**, who built the storage and was then inside it (4.20a). Four dialogue references and the class name; the `POKEMANIAC` symbol is untouched
- **ARTSAI and S.T.A.R.R. have no dialogue anywhere** — verified, zero references to either in any text file. The rename was complete on arrival, and **the Five Witnesses, the ITER 35 terminal and the lab encounter are the largest unwritten block in the design.** All text plus one hidden object; no engine work

### v10.1 — ARTSAI's three forms, and the name device

- **She was not always what the player meets.** Reference art gives three states: **vivid purple and faceted**, the **split** with a seam of colour, and a **real white rabbit** with the faceting only where the light catches
- **4.8's log already said it**, before there was a picture: ***ITER 35 — held two frames. did not come back the same.*** That line *is* the transformation, recorded by someone with no idea what they were recording
- **And the colour is 7.3, not decoration. Purple has no wavelength** — magenta is what the mind invents by folding the spectrum's ends into a loop the physics does not contain. **White is every wavelength at once.** So **she begins as the invented colour and ends as the one that is all of them**
- **Greyscale means the transformation cannot be shown**, which is correct: 4.6's claim is that nobody present understood what they saw
- **It also explains why the five witnesses contradict** (4.8) — **some saw form one and some saw form three**, and every one of them is honest. The puzzle's premise becomes true rather than arbitrary, at no extra writing cost
- **The sprite is form three**: white, and therefore the palest thing in a greyscale game
- **`STARR` in the species field; `S.T.A.R.R.` in the documents** — 3.2's device applied to a name. **The player learns what the letters stand for in the ruins, not from the Index.** Both fit the 10-char cap, so the choice was never technical

### v10.0 — the title order, explained at last

*Noticed from the outside: the build maps **RED → CONTENT** and **BLUE → CONTEXT**, and the title runs the other way. The mapping was always right; the order was accidental.*

- **It stays, and 8.4 now says why.** Everyone says *content is king* — putting **CONTEXT first is the thesis in two words**, before the player has read a line, and **the title refuses to let the original decide its order.** The correct posture for a conversion whose subject is that the frame decides what you are looking at
- **The two orders answer different questions.** *The title is the argument* (context is prior to content); *the mapping is the inheritance* (Red came first and is the default build). Both are right
- ***Flagged per 0.2:*** **this is a justification for a choice already made, not something found.** The rule against promoting coincidence to finding applies to the project's own decisions too — filed as a decision, and evidence of nothing

### HOLT — the man who was the thing in the box

*Vanilla's Bill merged with a creature. **That premise cannot be imported**: if a person can become a daemon then daemon-ness is a costume, the category goes arbitrary, and the game is forced to assert that people are a different kind of thing. It has carefully never said that.*

- **He was not transformed. He was suspended.** The box system holds a running process without running it — **a stored daemon has no state until it is withdrawn**, which is how the game already works
- **That is the only superposition the project can honestly claim, and it earns the idea without the word.** *Quantum* said aloud is borrowed authority and the exact explaining craft rule 1 forbids
- **Two went into the store and both were processes.** The system could not determine which was the observer, because there was no fact about it it could see. **The SEPARATION SYSTEM forces a read the store deliberately defers** — so the failure sits in the system, not in what people are
- **It is the machine-side twin of the removal.** Crystal held several fields and was recorded as incoherent; HOLT held two perspectives and the machine could not resolve him. **Both are resolution failures — but you can ask a machine to try again**
- **His line:** *I am not sure it chose correctly. I am sure it chose. Those are not the same thing, and I built the machine that cannot tell them apart.* **He is describing every institution in this game and thinks he is describing a bug**
- **He built the storage the player uses for forty hours**, and is the only person who has been inside it. Nothing points at it
- **PERSPECTIVE gets a place** — his accident is the move with no return path
- **BILL → HOLT**: a holt is a den, and it is one letter from *hold*. 12 references, the PC menu, the access message. *WARD rejected — the hospital register is what 4.10 avoids*
- ***Multiple outcomes* deliberately not built.** The engine cannot branch and the story is not about branching; **multiple readings is the real subject**

### Benchmark 1 — CAIRN

- **A cairn is a heap of stones that physically encodes something** — a path, a boundary, a grave. **It is 5's lesson standing in a field, and it is a rock.** The name arrived already meaning it
- **His creed:** everything you know is sitting in something, and **if it is not written down, it did not happen.** LEGACY daemons — old formats, still readable. **He is right, and nothing in the gym undercuts him**
- ***And the player meets that sentence again.*** The Meeting Room minutes are that creed applied to a person (4.20). **Benchmark 1 teaches it as sound practice at hour two; hour forty shows the cost.** Nothing connects them
- **How he loses:** the player encoded something he **could not read**, which he calls *a format I do not have* rather than a defeat. **He reframes his loss as a limit in his own reading** — perspective thinking in embryo, from a man who does not know that is what he did
- The gym trainer keeps it: *you have not written down enough yet*, then **CAIRN keeps a record of every match in here. Every one.**
- **BOULDERBADGE → SLATE MARK** — a mark on a slate is encoding; a mark as a grade is what a benchmark issues. Route 22's gate updated to match. **The other seven are still vanilla and want renaming as a set**
- This clears the last writing item in **8.1's vertical slice**. What remains there is the twelve daemons and Slate's theme

### The routes get their local names

- **Thirteen signs, every route that has one** — 1, 2, 3, 4, 9, 12–19. 3.2's device built exactly as specified: **the official plate untouched, the local name arriving underneath as `Painted beneath:`**
- **The institution's name is cast into the sign; the residents' name is added to it.** That is the difference 3.2 is about, made physical for free
- **The Bleed, Underpaint, Ashfall, The Wash, The Dapple, The Drift, Slack, Brackish, The Muddle, The Streak, Seafade.** Routes 16–18 all read **THE STREAK** — one cycling road, three signs
- This clears a line item from **8.1's vertical slice**

### v9.6 — the rumour that shaped a schedule

- **New 7.15, the space audit.** Every earlier claim that the music banks were full was **estimated, carried forward, and never measured.** Measured now: **901 bytes free before this session, 3792 after — having added six tracks**
- **The arithmetic that dissolves it:** our tracks run 89–478 bytes against a **median vanilla track of 427**, so **replacing a vanilla body frees more than it spends, every time.** The claim was true only of *appending without displacing*, which is not what a total conversion does — **every vanilla track is a slot, and there are 47**
- **4.23's Owl is unblocked.** His music was recorded as waiting on bank space; it never was. He shares `MUSIC_CITIES1` with 37 maps, so he needs **a constant and one repointed line in `songs.asm`** — the same edit Lurid, Callow and Doldrum need. **The scene and the tune are no longer on different timescales**
- *The lesson is 0.2's, turned on the project rather than the source:* **a number nobody measured is not a constraint, it is a rumour** — and this one shaped scheduling for days

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

## MIDI pipeline, tested 2026-09-07

`stems2midi.py` runs end to end on the intro stem set and its diagnostics work.
The mix rebuild fires (`no mix at intro-stems.mp3 / rebuilding it from 3
stems`), key detection reports its runner-up (C major 0.92 against A minor
0.78), and the overlap warning is correct rather than noisy:

    !! other carries 65% of all sounded cells -- the separation
       did not work, or the arrangement has only one part.

Suno returned three stems — Drums, Bass, Other — with no separate melody stem,
so `Other` genuinely holds melody and harmony together. The warning is
describing the input, not a bug.

**Regenerating was NOT committed.** The output differs materially from the
tuned file: 4 tracks and ~425 note-ons against the committed 5 and ~309.
Fewer parts, more notes. The committed version is the one tuned by ear when the
accompaniment got its chords back, and replacing it on the strength of a
byte-count comparison would be swapping something judged for something merely
newer. It needs an A/B by ear.

## v11.107 — 2026-09-08

**Two type hues moved, for legibility rather than taste.** Four pairs sat closer than ~20 in
CIE76 on the ramp's mid tone, which is most of a sprite's area and roughly where two colours
stop being separable at 56px. `CORRUPT` 10.8 → 25.9 from STRATUM (soil → mould);
`EMERGENT` 10.6 → 26.0 from SIGNAL (teal → deeper jade). Each moved within its own
metaphor, and only one of each pair moved.

`LOGIC / LEGACY` (18.5) and `SWARM / GROWTH` (18.9) left as they are — separating them would
weaken a metaphor to buy two points of distance.

**§9.4 gains the reasoning**, and `type-chart.html` gains a *Why each colour* section: all
fifteen, with the four that §6 fixes marked as inherited rather than chosen.

**Recorded as open:** white text fails on eleven of the fifteen base hues; the ramp's dark
step passes all fifteen at 5.6:1 or better, so badges should use it.
`graphics/interface/pokemon_types.pal` is still vanilla.
