# THE SPELL LEFT RUNNING — the book's architecture

*T-606. The user, 2026-11-21: "a prestige [book] like the callow school book ... a gamified psychology book which makes
use of computer science too ... Carl Jung's teachings about the Shadow Self ... a shadow part of you is like a daemon.
It runs in the background, and without awareness to it ... it needs the light of your awareness ... the charismatic /
poetic / subtle-puns / subtle magick ... diagrams ... [the] sorcerer's apprentice ... a shadow is like the broom, an
automation that was made and left running ... it itself is not bad, it just needs the light of consciousness to
integrate ... and this then maps to the 7 daily habits." Then, the ticket read: "continue to produce the architecture
of the book, the context, and the diagrams, and the look & feel (the added subtleness which gives it its identity)."*

**Every word, plate and diagram is a DRAFT** until the user keeps it. This file is the book's plan; `manual.md` is the
book. `python3 tools/manual.py --book shadow --write` prints it (in a worktree, point `companion` at a clone first:
the printer's last step redraws the companion's shelf covers).

## 1. What the book is

**One sentence.** A shadow is like a daemon: a spell you once cast, for a good reason, that kept running after you
stopped watching; you do not fight it, you find out what it was told, and you put it back in its corner.

**Its place among the game's books.** The GUIDE *reasons*; THE SUBTLE LAYER *notices*; THE HERMETIC LAYER works
*spells*; the TEXTBOOK *teaches*. THE SPELL LEFT RUNNING **debugs**. It is the one book that treats the reader as
the author of their own routines, and it hands them the tools to read one: the spell card.

**Three voices, kept apart on the page.**

| voice | who | where it speaks | how it is set |
|---|---|---|---|
| the Sorcerer | an old tortoise, slow and right | the chapter epigraphs (*Sayings of the Tower*), the Word, the last scene | italic Baskerville, centred |
| the Apprentice | a young hare, quick, honest about it | the tale, the preface (signed), and notes in the margins of the lessons | the body face; marginalia in a hand-lettered face, ink-brown |
| the lesson | no one in particular | the five lessons, the seven brooms, the five quills | the TEXTBOOK's scholarly voice, every claim cited |

The book is *set down by the Apprentice, from the Sorcerer's teaching* (the title page). That is why the hare can be
candid in the margins: it is his book, and his flood.

## 2. The identity: the subtle things

None of these is announced. Each is there for the reader who notices, the way the game's own details are.

1. **The water gauge.** Each scene of the tale opens with a small drawing of the well and its level: low, rising,
   brimming, over, flooded, flooded again, and at the Word, *full, and no more*. A reader who flips the chapter sees the
   tale told by the water alone. The last page of the book carries the gauge once more, at full and no more.
2. **Incantations.** Every spell in the book is also written out as a short incantation in the book's *spell hand*:
   a code block on parchment, its comments set as whispers. The tale's spell is `while not done` with no `done`; the
   fix adds the line in gold. Each broom of the week has its own incantation. Readers who code will read it as code;
   readers who do not will read it as a charm. Both are right.
3. **The Apprentice's margins.** Short notes in the margin of the lessons, in his hand: confessions and small jokes
   (*"I tested it three times. That is three more than I test most things."*). Never more than one a section; never a
   lesson the body has not already made.
4. **The seven lights.** Each day of the week carries a row of seven small lights with its own lit, Sunday's first,
   Saturday's last: the cover's seven brooms each with a light above. The game's USER card lights seven bands; the
   book never says they are the same lights, and does not need to.
5. **The day signs.** Each day's section heading wears its sign in gold, upright for the virtue, and the same sign
   turned over in grey for its shadow: the dome, the beam, the bowl, the climb, the knot, the arc, the stem (vision
   9.21's week table).
6. **The hat as the book's mark.** A small hat sits over every chapter number; a single broom is the scene break; the
   press's mark is the hat in a circle. The hat is attention, and the book is always wearing it.
7. **SPELL CHECK.** Every quest is set in a box headed SPELL CHECK. The pun is the point: checking a spell is the whole
   practice.
8. **Sayings of the Tower.** Every chapter opens with one saying, the Sorcerer's own, short enough to remember; the
   book's only real epigraph is Goethe's line, in this book's own translation, on the first page.
9. **Subtle magick.** It is never explained and never dropped: words are spells (*spelling*); the round table is a
   circle; the daemons are, in older magic's word, familiars; a book of spell cards is a book of shadows; the stars on
   the hat are not decoration. Nothing in the book claims magic is real. Everything in it treats attention as if it
   were.
10. **The puns stay small.** *A clean sweep; over the brim; the well is not well; swept up in it; hare-brained* (the
    hare says it of himself, once). One a chapter, at most, and never in a lesson's key sentence.
11. **The colophon winks.** Set in Baskerville and Gill Sans. *No brooms were harmed in the making of this book. Two
    were split, and both are fine.*
12. **The Apprentice's own card.** The Spellbook closes with the hare's own spell card, filled in, for the nap: its
    *done when* first left blank and then written in, in a different ink.

## 3. The architecture

| part | what it does | the devices it carries |
|---|---|---|
| **Cover** | the hat on its peg over seven brooms with seven lights, water at the foot | the hat, the lights, the water |
| **Frontispiece** | a map of the tower's grounds: the lake, the path, the well, the bench, the door and its peg, the cupboard, the scriptorium | the hat as the compass's north |
| **Title, copyright, dedication** | *set down by the Apprentice*; the sources of the tale; *for every broom that only ever did as it was told* | the colophon's wink |
| **To the Apprentice** (preface) | what a shadow is like; how to read the book, a broom a day | Goethe's lines; signed by the hare |
| **1. The Tale of the Apprentice** | the story, in six scenes and a coda | the gauge at every scene; four plates; the first incantation |
| **2. What the Broom Was Told** | five lessons and *Over, never cures* | four diagrams; incantations; the margins |
| **3. The Seven Brooms** | a broom a day, Sunday first | the cupboard plate; the signs, the lights, an incantation and a SPELL CHECK each day |
| **4. The Five Quills** | when two good parts need one thing: deadlock, starvation, livelock, four remedies | a plate; the quills diagram |
| **5. The Hat on the Peg** | the evening; the moral; the game, said once and lightly | the dusk plate; the last gauge |
| **The Spellbook** | the blank spell card, the Apprentice's own, the week's quests | the card |
| **Glossary, References, Colophon** | the words and the sources | the wink |

**A day's anatomy** (chapter 3), the same seven times so the reader always knows where to look: the sign and the
lights; the daemon; *the spell* in a line and as an incantation; *what it protects*; *where "done" went missing*;
*the word*, with the sign said in words; SPELL CHECK.

**A lesson's anatomy** (chapter 2): the tale's moment it comes from; the research, cited; the computing idea, said
plainly; the human form of it; at most one note in the margin; a diagram where one helps.

**Length.** About 6,000 words before the back matter: 35 to 45 minutes read aloud, the user's measure.

## 4. The cast

| role | daemon | why that one |
|---|---|---|
| the first broom | **LOOP** | it goes around and comes back |
| the many | **SPAWN**, **FORK** | making more of something; being in two places |
| the flood | **FLOOD**, **OVERFLOW** | water attracts its own |
| the axe's answer | **RESPAWN** | split it and it returns |
| the race | **THREAD** | a thousand at once |
| the well | **DEEPWELL** | a well that is never full (Tuesday) |
| Sunday's broom | **PING** | sends its call and waits for an answer |
| Monday's | **OVERFLOW** | input past the edge of its space |
| Tuesday's | **KEEPER** | keeps more against the lean season |
| Wednesday's | **BLOCKING** | waits for a signal that never comes |
| Thursday's | **SENTINEL**, and **SIGKILL** | the guard, and what it becomes unwatched |
| Friday's | **TRACER** | follows every path but its own |
| Saturday's | **SUPERVISOR** | supervises everything but itself |
| the scribes | **DEADLOCK**, **LIVELOCK**, **MUTEX**, **SEMAPHORE**, **SCHEDULER** | the five quills' failures and remedies |
| the companion at dusk | **ROVERCUB** | watched the flood from the stairs and said nothing |
| the shadow, named | **HAUNTPROC** | a process that haunts; on the cover's list, never cast in a scene |

The Apprentice (a young hare) and the Sorcerer (an old tortoise) are animals under the fable rule; the daemons are the
brooms and the familiars. The hare is an Aesop echo: the one who naps.

## 5. The plates

Drawn by `tools/spriteforge.py` (klein4b with the pixel-art LoRA, 512x512, each daemon's own front picture as a
`--reference`), filed in `art/drafts/` with the record that remakes each one exactly.

| plate | where | who | state |
|---|---|---|---|
| the first spell | ch. 1 | LOOP, the hat on its peg | drafted |
| many brooms | ch. 1 | the hare asleep in the hat, SPAWN, FORK | drafted (redrawn once: the first try drew people) |
| the axe | ch. 1 | the hare, RESPAWN | drafted |
| the word | ch. 1 | the Sorcerer, LOOP and the brooms, the hare on the stairs | drafted |
| the cupboard | ch. 3 | the week's brooms, crowded and shy | first draft, **to redraw**: charming, but generic animals rather than PING, OVERFLOW, KEEPER, BLOCKING, SENTINEL, TRACER and SUPERVISOR (the redraw timed out while roverbyteseer was busy) |
| the scriptorium | ch. 4 | DEADLOCK, LIVELOCK, MUTEX with SEMAPHORE's flag | drafted (redrawn once) |
| dusk | ch. 5 | ROVERCUB and LOOP on the well's rim | drafted |
| the Apprentice at his desk | the preface | the hare, LOOP | drafted 2026-11-21 |

## 6. The diagrams

Drawn in PRINCIPLES OF MIND's hand (Gill Sans; ink, grey, the hat's night blue, the virtues' gold, the water's blue).

| figure | shows |
|---|---|
| frontispiece | the map of the tower's grounds |
| 2.1 the spell card | a routine's loop, its blank *done when*, its watcher |
| 2.2 the axe and the word | suppression makes two; the word puts one back |
| 2.3 the race, and the gate | check-then-act at scale, and mutual exclusion |
| 2.4 orphans | a routine from a younger self, adopted by the first process |
| 3.1 the cupboard | every broom a protector: what each of the seven guards |
| 3.2 the seven signs | upright for the virtue, turned over for the shadow |
| 4.1 the five quills | the circular wait, and the ordering that breaks it |
| the spell card | to copy; and the Apprentice's own, filled in |
| the gauges | seven small wells, low to flooded to *full and no more* |

## 7. Into the game, the companion and a voice

*The user's own rule: every book reaches both the GBA reader and the app's book pages, and every book has its own
voice.*

- **The game's reader.** *Drafted 2026-11-21:* `docs/shadow-book.md`, twenty-four entries in seven sections (FIRST, THE
  TALE, THE LESSONS, SUN TO WED, THU TO SAT, THE QUILLS, THE HAT), read by `tools/gensubtle.py --book shadow` as the
  sixth open book beside THE SUBTLE LAYER, the third book and ORIGIN: every line measured against the reader's 94px
  column, nine lines a page, 72 spreads, no entry ending on a stranded line, and its rules checked word by word -- the
  game's craft rules whole, and a fable world's (nobody real named: the PDF's references stay in the PDF). Its page is
  the PDF's parchment with the hat's night for ink and the virtues' gold for the marks; each section opens with a
  Saying of the Tower in faint ink. **Still to do**: its twenty-four pictures, drawn for the reader's sixteen colours
  (the plates, the daemons, and the diagrams redrawn small); its cover and bag icon; then `BOOK_SHADOW` in
  `book_reader.c` and its item -- until then its `--write` refuses.
- **Where it is found.** *Open, the user's call.* The tale is set in a tower, and the game has DAEMON TOWER, where the
  books are mended; it could also be the book that arrives once all seven virtues are held, or the one the GUIDE's
  margin points to.
- **The companion.** The book on the LIBRARY shelf (its cover by `shelfcovers.py` once it is on `PDFS`), its pages
  exported like the other books. The day's SPELL CHECK beside the day's word on TODAY. And the gamified part not yet
  built: **spell cards in the companion** -- the user writes a card for a routine of their own (trigger, task, *for*,
  *done when*, *watched by*), and the companion's nudges become the hat. That is a ticket of its own, to file when the
  user wants it.
- **Its voice.** Chosen with the user from samples (T-543). The book wants one voice that can be both the slow
  Sorcerer and the quick Apprentice: unhurried, warm, a little amused.

## 8. Research, and the rules it keeps

- **The research is real.** Every study, date and finding is in the References, in the TEXTBOOK's style. Before the
  book is final, each is checked against its source, as the TEXTBOOK's were.
- **Quotation.** Jung is quoted twice, briefly, with paragraph numbers; everything else is said in the book's own
  words. Goethe's lines are this book's own translation. Lucian, Goethe and Dukas are the tale's only sources; nothing
  of any film is used, named or drawn.
- **The game's craft rules.** Never the thesis (only ever *like*); the process, never the pathology (no condition
  named, no verdict on anyone); a virtue *over* its shadow, never its cure (T-418); wrath answered by forgiveness
  (T-498); never the frightening word the game's name is taken for; nothing personal, nothing from `docs/private/`.

## 9. Open, for the user

1. The title: *The Spell Left Running: A Book of Shadows, in Seven Brooms*, or another.
2. The hare and the tortoise, or other animals.
3. Which plates stay, and which are redrawn.
4. Where the book is found in the game.
5. Its voice, from samples.
6. Whether spell cards become a companion feature (a C- ticket).
