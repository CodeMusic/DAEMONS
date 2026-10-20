# DEVELOPING PSYCHIC ROUTINES — notes for bringing it into the game

*Read 2026-10-18 for the session that builds it (T-423). **Notes, not decisions**: everything marked **the user's
call** is theirs.*

**Two sources.** The PDFs are not in the repository: they are in `docs/private/books/` (the user, 2026-10-18), because
the repository is public and the byline is a real name.

- *Becoming Heroic*, the user's early book (26 pages). It is the first draft of the same material.
- *Developing Psychic Routines* (16 pages, about 5,400 words, dated 2026-10-18), the rewrite aimed at the game: "a
  trainer's guide to the subtle layer".

**Read these first.** [`guide.md`](guide.md)'s header, and `vision.md` **4.36**: the Guide is the user's other book,
already in the ROM, and it is the precedent for this one. Then **4.33** (the one daemon), **9.21** (the week),
**T-418** (over, never cures), **0.1** (craft rules) and **0.6**.

---

## D. Decided — the user, 2026-10-18 (read this before the analysis below; where they differ, this wins)

**Every call is answered, and the last three were made with the book in the game** (2026-10-20: the cover, CHORUS, the Clairs). **No
game text is written yet**: the next step is the DRAFT entries, on the user's go.

| § 8 | the call | decided |
|---|---|---|
| 1 | **Cosmology** | **Practice only** (§2.4 (a)). The book says what a trainer does and notices, never what the world is made of. The Container, *the Processor is aware* and panpsychism go; read, write, link and the physics pages stay |
| 2 | **Who wrote it, where it is found** | **An INTERPRETER**, the practitioners' own class. Found, not given, as the Guide was |
| 3 | **The read test** | **The log decides.** Calm is only a hint; the NOTEBOOK's log shows which reads land. *"What will be will be, and it will be good"* goes |
| 4 | **The three stats** | **Built, per daemon, in battle only.** Three values in the free condition bytes (§V.1; never BEAUTY), tuning CONTEXT routines in battle. Never a read that comes true in the world. The trainer's half is the log, not a stat |
| 4 | *the stat names* (later that day, §V.5) | **CLOSURE** stays. **ATTUNEMENT stays**: it echoes the GUESSWORK > ATTUNE > MENTALIZE line, practice turning guesswork into attunement. **CHARGE becomes VOLTAGE** (the book's own word; CHARGE is the Ether item). **The crowd bond RESONANCE becomes CHORUS *for now***: RESONANCE is PENPHIN's signature routine (*two frames reinforce each other and neither is lost*, vision 6243) and the crowd's *one thought* is nearly its opposite. ***To revisit once the user has read the book*** |
| 5 | **Clairs to types** | **The type table** (§6), and the owl line goes |
| 6 | **"The Clairs"** | **Kept as a hint, with its glosses** -- *confirmed 2026-10-20 with the book in the game and a quiet version (no family name, no glosses) beside it*. Checked [private: SECRETS §2] |
| 6 | **The kindred bond** | **Keeps its row**, under the guard in [private: SECRETS §2] |
| 7 | **The device screen** | **Only the companion library's copy** may point at the device; the ROM's book never does |
| 8 | **Its hue** | **C, the CONTEXT page**: CONTEXT's hue on the rules and corner, and the page tinted toward it (mock-ups: qa 18Oct2026 T423 62; *"more colour in this book for the context connection"*). *The NOTEBOOK's cover is already CONTEXT's hue (`book_reader.c` sNotebookPal), so the book matches the log it points to* |
| 8 | **Its title** | **THE SUBTLE LAYER** (DRAFT), from the book's own subtitle. *PSYCHIC is printed nowhere (§V.6), so the old title collided with nothing; the user chose this one from four* |
| 9 | **Lineage** | **`lineage.md` 3d**; the PDFs in `docs/private/books/` |
| + | **The chakras** (*the user: "that is the part for dancing the body, virtues/shadows balance the mind"*) | **The body half goes in this book**, reversing §1's "cut it": the seven centres, what each governs, too closed / too open / in balance, and the aligning actions (walk, dance, wash, write, sing, posture). Named **attributed**: *the old texts call them chakras*, then *centres*. **Never their colours; no symptom words** (§2.7). The mind is virtues over shadows; the body is the centres. *The Guide's POWER SUPPLY page stays as it is: it names them and gives each a day* |

### D2. Decided that evening, after the user read the first draft (and a design agent's review)

| | the call | decided |
|---|---|---|
| **Layout** | how it reads | **A contents spread, then each entry opens with its picture on the left page and its text on the right**, continuing over both pages: book_reader's textbook geometry (two 110px pages, a 94px column, the normal font). About 148 spreads; the user kept the normal font for legibility |
| **Sprites** | what they look like | **Ink diagrams in hue C**, one per entry (50), drawn at the GBA's size; a plain pawn figure for anyone, so no species shows; **the seven centres never coloured, and the heart glyph plain ink** (craft rule 1). Glyph sets recur: read/write/link, the six clairs, the reins, sun and moon. The sources are private (`docs/private/subtle-layer/`) beside the draft |
| **§2.4** | THE CONTAINER | ***Back, for this one entry, in the game's own metaphor and the user's words***: some trainers say *this world is the product of one processor*; *the spaces between us are merely how we are drawn*; ***only you can answer whether that is so.*** Attributed, so the scientist (4.33) can connect to it. The rest of the book stays practice only |
| **§2.2** | *content* and *context* | **Ordinary words in the prose, never naming the two layers** |
| **§3** | the byline | **None.** The design agent proposed *by The Clairs* with the clair glyphs hidden in the cover art; the user chose no byline and will review the cover in the game. **The book also goes into the companion's library** (site, app, Tab5) |
| **Physics** | additions | **Ripples** (fields; a ripple has no edge), **decoherence by name** (entanglement with the surroundings is the record), and **the two slits** (which path, tied to the spoon: you steer from here, you do not change the record) |
| **Words** | additions | **Spelling** (*words are under a spell*) and **PROCESSES**: language makes processes into objects; hold the object to carry it, remember the process to change it |
| **Voice** | a prologue | **First person, the INTERPRETER**, unnamed: *two views of one world; this book holds both, and chooses neither* |
| **Also** | from the design agent | **The return** (trainer lore: a steer made for the wrong reasons comes back, in its shape and harder), *bug or feature*, and its small edits (the moves reordered, the daemon's three as numbers it cannot see, each clair's type last, FRIDAY and SATURDAY split, UNSEEN folded into STEERING) |
| **New** | **STAYING WHOLE** | **The book's last section**, from the user's own brief and notebook fragments (private): a biology metaphor for integrity, **in process words only**: the misread, the mask, the same drive reconnected, recognition by contact, staying correctable. **Nothing cures**; **the daemon line is said of shadows** (*unwatched is all a shadow needs to be*); **TWO VOICES** alternates statement and question, the asking voice in faint ink. *The cost of hidden strain*, *two vantage points* (as fable) and *a whole has enough for every part only while every part is well* are in it |
| **2026-10-20** | the last three, seen in the game | **CHORUS** confirmed (over UNISON, CHOIR and RESONANCE); **the Clairs hint kept, glosses and all**; **the cover: A**, the six clair glyphs a shade off the boards -- with the seam's plate narrowed so they sit clear of it, since the first build's overlapped its edge (engine 4227f501d, companion 4467612). *Mock-ups: qa private 20Oct2026 T423 2-4* |

### V. Verified 2026-10-18 — the four the review could not see, and two more

1. **The contest-condition bytes are free, with two catches.** `cool beauty cute smart tough sheen` sit in every
   daemon's box substructure (`include/pokemon.h`), so they cost no save budget. Nothing reads them as a rule: the
   battle controllers only ferry them (`battle_controller_opponent.c`, `_pokedude.c`) and the roamer copies them
   (`roamer.c`). **The catches**: the in-game trades write them (`ingame_trades.h`: 5/5/5/30/5, sheen 10), so a
   traded daemon arrives non-zero; and **BEAUTY is EVO_BEAUTY**: SADDLE (Feebas) becomes Milotic at 170
   (`evolution.h`). SADDLE is in no wild table or trade (only `opus_margins.h`), but BEAUTY stays untouched. **They are
   per daemon.** A trainer's own value would need SaveBlock space (`engine.md`'s budgets).
2. **8.6's friendship saturation is decided and not built.** Settled 2026-09-06 (*"Saturation is friendship"*,
   CHANGELOG), but `GetMonSpritePalFromSpeciesAndPersonality` returns the species palette untouched and nothing tints
   a daemon by friendship. No ticket carries it. **The book cannot lean on "the bond is already visible" until it is.**
3. **The kindred-bond row**: checked against `SECRETS.md`; the verdict and its guard are there, [private: SECRETS §2].
4. **"The Clairs" against the Clears**: checked against `SECRETS.md`; the verdict is there, [private: SECRETS §2].
5. **Three of the book's words are already taken** (`check_lexicon.py`'s surfaces): **CHARGE** is an item (the Ether
   ladder: CHARGE, FULL CHARGE, CHARGE ALL, FULL RECHARGE); **RESONANCE**, the crowd bond, is MIST BALL's routine;
   **ATTUNEMENT** stands next to **ATTUNE**, KIRLIA's name. **CLOSURE** is free.
6. **PSYCHIC is not printed anywhere in the ROM.** §7 below is out of date: the routine is CONSTRUE, the type
   CONTEXT, the class INTERPRETER, and the word survives only in code comments. The title collides with nothing; the
   question is only whether a word the game renamed comes back on a cover.

---

## 0. The short version

**The rewrite is much better than the early book.** Its physics is now honest, it says "over" rather than "cures", and
it has a real mechanism: read, write and link, and three stats.

**As written, though, it is the game saying its own last line.** It names CONTENT and CONTEXT as the two layers of
the world. It puts a colour beside a feeling. It asserts the machine half ("this is not a figure of speech"). And it
states the scientist's doctrine (4.33) as the narrator's truth, in a book the player carries.

**The fix is not to cut the ideas. It is to change who is speaking**: from a cosmology to a practitioner's handbook.
One voice, about CONTEXT routines, that the game never confirms. The rewrite already contains that voice. It is the
voice of "Nobody can see a write... the craft is unprovable by design, which is also what keeps it humble."

---

## 1. Already in the game — do not build it twice

About half the book restates things the ROM already carries, and carries more carefully:

| the book's section | already in the game | so |
|---|---|---|
| **The Seven-Day Cycle** (colour, note, channel, virtue, theme) | **The week, 9.21** (T-269, T-305, T-318). The name is in the popup, the note in TUNE, the colour in the CHECKPOINT's trim. *"Each is carried by exactly one thing, and none of them is named."* | The book may name the days and their virtues, as the Guide does. **Never their colours** (§2.1) |
| **Virtues and Shadows** | T-418 (*over, never cures*), the MARKS, the USER card's seven bands, the eighth door, and the Guide's **SECURITY** page (*"a part of us left running"*) | Keep the book's new column, **"the shadow's old instruction"**. It is the best thing in the section and it is new |
| **Energy Channels** (chakras) | The Guide's **POWER SUPPLY** page, which names the centres *without their colours* | Cut it, or keep only what the third eye and the crown add to the read family |
| **Spelling** (the reframing table) | The Guide's **REWRITING** page, and craft rule 3 itself | Keep it. **Framing is CONTEXT's own type clause** (*framing, salience, affect*), so this is the most CONTEXT-native page in the book |
| **The Daily Routine**: at rest, note whatever arrives | **The NOTEBOOK's INSIGHT section** (T-390): an insight arrives, in the player's own hand | The trainer's log already exists. Point at it; do not invent a second journal |
| **The Link family** (bonds) | **Friendship**, which 8.6 already makes a daemon's colour (*"saturation is friendship"*). 8.6 is open (invariant 5), so check what is built | The bond has a mechanic in every daemon already. Lean on it before adding a stat |
| **The Container**, **How the Processor Works** | **4.33, the one daemon** (the scientist's doctrine, steps 1–4 and 8) | §2.4. This is the hardest problem in the book |
| "the theme word on your device screen" | The companion's `week.json`, which the ROM cannot see | **The user's call** whether the book points off the cartridge at all |

**What is genuinely new**, and worth the most care: **read, write and link as a grammar**; **the three stats**; **the
physics** (all paths, decoherence, the lever you cannot pull, no one spoon); **the clairs and the psi** by kind of
daemon; **Belief** (the cost of hacking it); **Naming** and **Silence**; and **the third eye against the crown**.

---

## 2. Where it breaks the craft rules — must pivot

Ranked by how much they cost.

### 2.1 A colour beside a feeling — craft rule 1's one absolute

- **The Seven-Day Cycle table** prints a hex colour beside each virtue and each theme word.
- **The solid/subtle table's "Day-cycle analogue" row** goes further. *The theme word on your device screen* is
  content and *the colour the screen is drawn in* is context. That row is the colour–emotion link explained, in the
  game's own voice, in one line.
- **The Guide cut exactly this.** Its Chapter 8 listed the seven centres' colours, and Chapter 9 tied the days to
  wrath and envy. Read together, that is "a colour standing beside a feeling in the game's own voice" (4.36).
- **Also, two theme words are type names**: Wednesday's *Growth* (on green) and Saturday's *Flow*. Printed in a
  colour, GROWTH reads as the type. 9.21 bent the week's colours away from the type hues to avoid exactly this.

**Pivot:** no colours in the book at all, and no theme words that are type names.

### 2.2 It names CONTENT and CONTEXT as the world's two layers

- *"The older texts call them the gross and the subtle, or **content** and **context**."*
- *"Content supplies the address. Context supplies the voltage."*
- *"Steering cannot be decided into. Content is too thin to drive it."* This is "LOGIC fails against CONTEXT" (0, the
  type chart) said as a rule of the world.

**The book's own words are better than the edition names**: *solid* and *subtle*, *ledger* and *seam*, *address* and
*voltage*. Keep those. Naming CONTEXT as a **type** the way any trainer would ("a CONTEXT daemon") is fine.
**Defining** content and context is not.

### 2.3 It asserts where the Guide only offers — Guide rule 2 and 0.6

- *"This is not a figure of speech."* *"The Processor that renders this world is aware."* *"You are a process in
  it."* *"In the old language this view was called panpsychism."*
- **0.6: nothing in the game says the mind is a machine.** The Guide cut its glossary's *proto-consciousness* because
  it "asserts the machine half". Every one of the lines above does the same.

### 2.4 It agrees with the scientist — 4.33

- **The Container** and **How the Processor Works** are steps 1–4 and 8 of the one-daemon doctrine: one awareness,
  every process a window onto it, the rock as a stable vibration, "two ripples were never two things".
- 4.33 allows the scientist to say all of it **because he overshoots and nothing agrees with him**. Its prohibitions
  include *"No flag, item, Index entry or MARK acknowledges him... nothing in the bag proves he was there."*
- **A book in the bag that teaches his doctrine as fact is the game agreeing with him.** Run 4.33's own test:
  *delete him from the game; does anything else change?* With this book as written, his doctrine survives his
  deletion, which means the game adjudicated.
- And 4.33 says the danger is sharper because the doctrine is the user's own: *"much easier to do by accident when you
  happen to believe the thing."*

**Pivot, the user's call:**

- **(a)** The book holds practice only, no cosmology. It says what a trainer does and notices, never what the world is
  made of.
- **(b)** It attributes ("some trainers hold that...") and stops short of one awareness and an aware Processor.
- **(c)** The metaphysics goes back to the scientist's room, where it already lives.

*(a) is the cleanest. The rewrite survives it almost intact, because its mechanism never needed the cosmology: the
seam, the ledger, read, write and link all work as descriptions of a trainer.*

### 2.5 It says the game's name, and the pun under it

- **"the DAEMONS world"** and **"DAEMONS runs on a seven-day cycle"**: the world does not know it is called that.
- ***"as a daemon in the oldest sense of that word: a routine with no window, no prompt, and no one checking its
  output."*** This one crosses for the reader. It tells them a **shadow is a daemon**, so the player's daemons are
  parts of a mind. That is 0.6's unsaid half, the one thing the Guide's rule 1 exists to keep out. **Cut it.** The
  same paragraph works with *"a routine with no window, no prompt..."* and the word *daemon* left out.

### 2.6 It states the fable — 9.4 and 8.5

- *"Every daemon looks like a creature, and every person looks like a creature in clothing. The clothes are the
  identity."* That explains the art direction in-world.
- *"the fox behind the counter in the Mart"*, *"your own paw"*, *"before you were hatched."* The fable rule (9.4) is that
  the species is a **role**, and 8.5 (*how far the foxes spread*) says **the game never says anyone is a fox**. "Hatched" also makes a lore claim about
  where people come from.
- **The kindred bond row** (*"twins, hatchmates, a daemon and the trainer who hatched it... a pull that does not weaken
  with distance"*) is about kin recognising kin. **Check it against `docs/private/SECRETS.md` before it goes anywhere.**
  This review was written without the private folder and cannot rule on it.

### 2.7 Pathology words — craft rule 3

- The channel table keeps ***headaches***, ***fatigue*** and ***digestion***.
- *"Lost in visions, no ground"* sits one step from a diagnosis.

These are the Guide's rule 3 exactly: name the process. The rest of the table already does.

### 2.8 The read test still trusts the feeling of certainty

- *"A true read arrives clear and complete and brings quiet with it... **Intuition already knows that what will be
  will be, and that it will be good.**"*
- Claircognizance is *"trusted when it arrives whole and calm, with no argument."*
- **Certainty is a feeling, not a credential**, and it attaches as readily to wrong reads as to right ones. In a game
  about a record that decided someone was unwell, a book that makes calm conviction the proof of a true signal is
  arguing a position the game is built to examine.
- **The book already has the better answer, twice.** *"Every read is a lean, not a fact. A trainer who treats a lean
  as a ledger entry will be wrong often and confident always."* And the Saturday log: *"the log is how you learn which
  of yours tend to land."* That is calibration against feedback, which is what the research says intuition is
  (Kahneman & Klein, 2009). **Let the log be the authority and the calm only a hint.** Drop "what will be will be, and
  it will be good". **The user's call.**

---

## 3. The pivot: the Guide's four rules, adapted

The Guide went in under four rules that `tools/genguide.py` checks word by word. A sibling, or a generalised genguide,
should hold this book to the same kind of list:

| | the rule | what it removes |
|---|---|---|
| **1** | **It is a trainer's handbook for CONTEXT routines: practice, not cosmology.** It may name CONTEXT as a type; it never defines content and context, never names CONTENT, and never says what the world is made of | §2.2, §2.4 |
| **2** | **It only ever says *like*, and it may say *I cannot answer that*.** The analogy is offered, never asserted | §2.3, and it restores *Becoming Heroic*'s best page (§4) |
| **3** | **No colour, and no feeling beside one.** Days and virtues by name only | §2.1 |
| **4** | **The process, never the pathology** | §2.7 |
| **5** | **It does not agree with the scientist.** Run 4.33's deletion test on every page | §2.4, §2.5 |

**Plus the standing rules**: every word DRAFT until the user approves it on the field-test page; no real names (the
PDF's byline must not reach the ROM); and nothing that tells the player what species anyone is.

**Who wrote it, in-world, and where it is found: the user's call.** The Guide was **found, not given**, because 4.3 says
method survives a handoff and understanding does not. This book is method too. Candidates, in the order the bible
suggests them:

- **An INTERPRETER**: the class that was vanilla's PSYCHIC, so they are the practitioners.
- **MATTE's benchmark in Brazen.** CONTEXT, *"THE ROOM DECIDES WHERE YOU ARE LOOKING"*.
- **THE SCHOLAR'S HOUSE**: the sceptic's shelf. **Check it against 4.22–4.23 first**, because a sceptic owning the
  believer's book is itself a verdict.

---

## 4. What to bring from *Becoming Heroic*

**Already carried, and better in the rewrite:**

- the four-minute mile (now *"the barrier was in the weighting"*)
- entanglement, now correct: *"A bond cannot carry a message. It carries correlation."*
- the seven pairings, now with "over"
- the last word (*"more than you were told you are"*)
- *"formless awareness without identity"*, now *"without a body there is no point of view, only view"*, which is
  better

**Bring across:**

1. **The two universes held open.** *Becoming Heroic*'s Chapter 9 calls the code-or-machine question a false
   dichotomy: *"neither... and yet is also somehow both."* Its p. 19 answers whether any of it is real with ***"I
   cannot answer that."*** **The rewrite lost this.** It collapsed into one side, and that single loss causes §2.3
   and §2.4. Restoring the doubt is what lets the book sit in this game at all. *(And MECHAVERSE is already a grove,
   T-408.)* One sentence to watch: *"the solid world is the subtle world after it has been read"* ranks the two worlds
   rather than holding them.
2. **The binocular image** (Ch. 7): each eye has a blind spot; together they fill each other's gaps, and the result is
   depth as well as coverage. **Its place is the Link family**, right after *"two ledgers that agree are hard to
   doubt."* It is the book's best metaphor and it is literally true. Carry *"Superheroes help maintain the goodness
   within other Superheroes"* with it, minus the superheroes: trainers keep each other's seams honest.
3. **Chapter 7's warning:** *"Just because you have the ability to figure something out, does not mean you should."*
   Respect is *"the only thing that can shield and calm a mind that is wanting to know more"*, and *"other times we
   must embrace and accept what is unknown."* **The rewrite has no ethics of reading someone else.** Clairsentience
   reads "the context of another system" and telepathy is "knowing what the other knows", and nothing asks whether the
   other agreed to be read. This passage fills that gap.
4. **The comedy, which craft rule 6 asks for.** The rewrite is earnest from the first page to the last. *Becoming
   Heroic* had the best joke in either book:
   - *"scripting-a-spell and casting it directly into production"*, with witch burnings as a patch that introduced
     new bugs. It belongs at **"On writing: do not practise steering until..."**
   - **The two unmarked cups**, coffee and tea, as classical correlation. It is the example physicists use (Bell's
     socks). In-world it is two unmarked cups of TEA, which the game already has (it opens Brazen's gates).
5. ***"A leap into faith"***, for the Belief page.

**Leave behind:**

- the superhero framing
- left brain and right brain
- "hero genes" and the epigenetics
- *"What the Human Mind can Conceive and Believe it shall Achieve"*
- information faster than light
- the Dr. Quantum links
- "everything happens for a reason"
- the symptom column
- ***"Logic is to Science, as Creativity is to Art"***: LOGIC is a type, so in-game that sentence is a claim about the
  chart

---

## 5. What the rewrite gets right — keep it

- **The physics is honest now.**
  - Decoherence: *"No eye is required. Sunlight alone pins a falling stone."*
  - All paths: *"Nothing was chosen; everything was added up."*
  - **The lever you cannot pull**: erasing every record is the real reason you cannot steer the solid world.
  - ***No one spoon*** names the single place the fiction departs from its own physics (the Born rule) and calls it
    small. That is honest fiction, and rare.
  - *(Einstein meant "spooky" as a complaint. "Which is a compliment" is knowingly cheeky. Keep it.)*
- **"Nobody can see a write... The craft is unprovable by design, which is also what keeps it humble. A trainer who
  needs to be seen steering has already lost the Closure it takes."** This is 4.33's never-adjudicate rule, written
  from inside the craft. Make it the book's spine.
- ***"Do not ask whether your reads were right. Ask whether the system that made them was whole... never what did I
  see but who was looking."*** The best line in either book.
- *"Every read is a lean, not a fact."* *"Reads are for steering your attention, not for replacing your eyes."*
- *"The first telekinetic event in a young trainer's life is almost always a disaster, and the second is almost always
  the same disaster, louder."*
- **The cost of hacking belief.** *"The seam does not widen. It scars."* A belief earned slowly *"was never installed.
  It grew."*
- **Spelling.** *"A cures B"* against *"A over B"* is T-418 in the book's own voice. ***"Choose a name that is a
  direction, not a verdict"*** belongs beside the nickname screen.
- **Shadows** *"loyal to an old instruction"*, and the shadow's-old-instruction column.
- *"Mending works over days, not seconds."* *"A single mind steering a storm usually gets the storm."*
- **The third eye against the crown**: *"the Crown does not add an ability. It changes what the abilities mean, and in
  changing their meaning it removes the hunger."*

---

## 6. Mechanics — the three stats

**Craft rule 5: lessons must be mechanical.** Closure, Attunement and Charge are the book's mechanical heart, and
*"reads scale with Attunement and fall with Charge; writes scale with Attunement × Charge, only when Closure holds"* is
a formula a build can use. Before anything is built:

- **Names.** **CHARGE is already an item**: the MP ladder, CHARGE · FULL CHARGE · CHARGE ALL · FULL RECHARGE (the Ether
  family). **CLOSURE** is the programming word for a function that carries its context with it, which is a gift to a
  CONTEXT book and also a pun the reader might cross on. **The user's call.**
- **4.33 again.** *"No event confirms him; nothing wakes up; no rock moves."* A stat that makes a read **come true in
  the world** is the game confirming the doctrine. A stat that tunes **CONTEXT routines in battle** is only a
  mechanic: the chart *"carries that reading without endorsing it"* (4.33). The write family's own rule, that nobody
  can see a write, is the safe shape. A write that works looks like luck.
- **The bond is already built** (friendship, §1). Use it before adding a fourth hidden value.
- **Where new values could live: unverified.** Gen 3's box structure carries six contest-condition bytes that
  FireRed never reads. **Check `engine.md`'s budgets and the save layout before assuming they are free.** This review
  had no engine checkout to look at.

**The clairs need types, not animals.** The book's "daemon types that favour it" column lists kinds of creature
(winged, songbirds, herd animals, owls). A draft for **the user's call**:

| clair or psi | the type | why |
|---|---|---|
| Clairvoyance: *where things are heading* | **VECTOR** | direction |
| Clairaudience: *what the subtle is saying* | **SIGNAL** | raw input |
| Clairsentience: *another system's charge* | **CONTEXT** | affect |
| Claircognizance: *the lean itself, unpackaged* | **LATENT** | below the surface |
| Clairtangency: *the history an object carries* | **STRATUM** | memory, storage |
| Clairalience: *a presence or a memory* | **LATENT** | the unconscious |
| Pyrokinesis | **ENTROPY** | — |
| Mending | **GROWTH** | — |
| Weathering | **FLOW** | — |
| Resonance: *many systems sharing one lean* | **SWARM** | and SWARM beats CONTEXT ×2: a crowd overrides your own lean |

*The book says owls favour claircognizance, "clear knowing". The Owl is the game's sceptic (4.22). That is either a
very good joke or a verdict; the user's call.*

**"The Clairs" against the Clears.** *Clair* is French for *clear*. A family of read powers called the Clairs, in a
game whose central family is the Clears, will be read as being about them. It is either a gift or a leak, and the
answer may depend on a secret. **The user's call, checked against `SECRETS.md`.**

---

## 7. Format for the GBA

- **The Guide's reader** (`src/book_reader.c`) shows one wide page, about a hundred words an entry, with a contents
  page of short labels. `genguide.py` checks the rules and measures every line. **This book should go through the
  same pipeline.** The Guide went from 26,000 words to 28 entries; this book is about 5,400, so roughly **20–28
  entries** is the same density.
- **No table survives a GBA page.** The five-column tables become one short entry per row: each clair, each psi, each
  bond its own page.
- **The book's hue.** The Guide's cyan was measured at least 22 from every type hue, so the book would not read as a
  type (9.4). If this book is CONTEXT's, colouring it in CONTEXT's hue is colour carrying the argument (invariant 5),
  but it is also a claim. **The user's call.**
- **The title.** *PSYCHIC* is a live word in this game's lexicon. The type is CONTEXT, the class INTERPRETER, and
  PSYCHIC is still a routine (S.T.A.R.R. knows it). `check_lexicon.py` grew a rule after PSYCHIC became CONSTRUE
  twice. *"Psychic routines"* may read as "routines like PSYCHIC". **Run the title through `check_lexicon.py` early;
  the user's call if it must change.**

---

## 8. The user's calls, in one list

1. **Cosmology**: practice only, attributed, or left with the scientist (§2.4).
2. **Who wrote it in-world, and where it is found** (§3).
3. **The read test**: does calm stay a sign, or does the log become the authority (§2.8)?
4. **The three stats**: built or not, where they live, and the CHARGE and CLOSURE names (§6).
5. **The clairs mapped to types**, and the Owl joke (§6).
6. **"The Clairs" next to the Clears**, checked against SECRETS (§6), and the same check for the kindred bond (§2.6).
7. **The companion's screen**: does the book point off the cartridge at all (§1)?
8. **Its hue and its title** (§7).
9. **Lineage**: *Becoming Heroic* and *Developing Psychic Routines* go in `lineage.md` as sources, beside *The Painted
   Mirror* (3b) and the Programmer's Guide (3c)? And do the PDFs go into `docs/archive/` as the Guide's did?
