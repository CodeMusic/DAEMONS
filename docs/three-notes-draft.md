# A DAEMON'S THREE NOTES -- its type's key, its day and its month (T-612) -- DRAFT

*A proposal for the user's yes, written 2026-11-23 from the user's sketch (T-612): "each daemon has three notes and
colours" -- its type's key, its number mod 7 on the days' colours, its number mod 12 on the months'. It feeds C-490
(what a daemon makes in the companion, and DEVELOPER MODE's palette on its INDEX entry). Nothing here is built.
Every word DRAFT.*

## 1. Nothing new has to be invented

All three notes come from things already built and already approved:

- **The key** is 9.36's table (approved 2026-11-23). Each type has a tonic and a mode: CONTENT C major, CONTEXT
  A minor, LOGIC G minor, FLOW A-flat major, and so on. A type's tonic is the note whose colour is nearest the
  type's own.
- **The day** is the week's wheel in the companion's SYNESTHESIA (`server/src/psyche/synesthesia.ts`, C-385). It has
  seven days on the seven white keys and the seven colours of the bow: Sunday C red, Monday D orange, Tuesday
  E yellow, Wednesday F green, Thursday G blue, Friday A indigo, Saturday B violet. Each day holds a virtue over its
  shadow and a chakra (`data/week.json`).
- **The month** is the same file's year wheel. It has twelve months on the twelve notes of the octave: January C red,
  February C-sharp red into orange, and so on to November A-sharp indigo into violet and December B violet. A month
  on a black key is the blend of the two days either side of it. Each month holds a tone, from Renewal to Generosity,
  and a season, which flips with the edition's hemisphere.

That file already counts in colour: *"a day is 1..7 (Sunday 1), a month 1..12"*. **A daemon's three notes are its
first type's key, plus its INDEX number read on each wheel.**

## 2. The proposal

For a daemon with INDEX number *n* (the number the INDEX shows):

| | its note | its colour | what it carries |
|---|---|---|---|
| **KEY** | its first type's tonic, major or minor | the tonic's colour: **bright for a major key, dim for a minor** (the user's presumption) | **its kind**: what it shares with every daemon of its type |
| **DAY** | (*n* mod 7) + 1 on the week: always a white key | that day's colour | **what it practises**: the day's virtue over its shadow, and its chakra |
| **MONTH** | (*n* mod 12) + 1 on the year: any of the twelve | that month's colour, a blend on a black key | **what it brings**: the month's tone and its season |

The user's examples, worked:

| # | daemon | KEY | DAY | MONTH |
|---|---|---|---|---|
| 1 | ROVERCUB (GROWTH) | F major, green, bright | 2 Monday · D orange · TEMPERANCE over GLUTTONY, sacral | 2 February · C♯/D♭ red into orange · Love |
| 56 | PREEMPT (LOGIC) | G minor, blue, dim | 1 Sunday · C red · CHASTITY over LUST, root | 9 September · G♯/A♭ **blue into indigo** · Peace |
| 58 | SENTRY (ENTROPY) | E-flat minor, orange into yellow, dim | 3 Tuesday · E yellow · CHARITY over GREED, solar plexus | 11 November · A♯/B♭ indigo into violet · Remembrance |
| 59 | GUARDIAN (ENTROPY) | E-flat minor, orange into yellow, dim | 4 Wednesday · F green · DILIGENCE over SLOTH, heart | 12 December · B violet · Generosity |
| 60 | LOOP (FLOW) | A-flat major, blue into indigo, bright | 5 Thursday · G blue · FORGIVENESS over WRATH, throat | 1 January · C red · Renewal |
| 62 | MUTEX (FLOW, LOGIC) | A-flat major, blue into indigo, bright | 7 Saturday · B violet · HUMILITY over PRIDE, crown | 3 March · D orange · Balance |
| 151 | ARTSAI (CONTEXT) | A minor, indigo, dim | 5 Thursday · G blue | 8 August · G blue · Voice -- *its day and month are one note* |

**Two corrections to the sketch.** First, 56's month is 9, September, G♯/A♭. On the year's wheel that is **blue
into indigo, not yellow**; yellow is E, which is 5, May. Every other example works out as the sketch wrote it.
Second, **SENTRY has one type, ENTROPY: WATCHING is its INDEX category.** The question of two types still stands
for 175 daemons, MUTEX (FLOW and LOGIC) among them (section 5).

## 3. What the numbers say, across all 400 numbered daemons

- **Both wheels make 332 different sets of three notes; the week alone makes only 107.** The two wheels repeat
  together every 84 numbers (7 × 12), so a daemon numbered *n* and one numbered *n* + 84 share a day and a month.
  They share all three notes only when they also share a first type: that is 127 daemons in 59 sets. With the week
  alone, 377 of the 400 would share all their notes with another daemon. **This is the case for both wheels, beyond
  making music.**
- **Every CONTENT and CONTEXT daemon's DAY note is in its key**, because the week is CONTENT's scale: seven white
  keys and nothing added. For the other sixteen types it depends on the number.
- **Only 155 daemons have both of their other notes inside their key; 61 have neither.** VECTOR's five have none
  with both inside, and ENTROPY has 3 of 23. So the music has to decide what to do with a note outside the key
  (section 4).
- **Some daemons have only two different notes**: for 32 the day and the month are one note, for 34 the day is the
  tonic, and for 38 the month is.

## 4. What the music does with three notes

**The three notes are not a song.** A daemon's song stays as 9.36 has it: in its key, made from its name, its
INDEX entry and its cry. Summoning (T-610) and THE VERSES (T-613) do not change. The three notes are what a daemon
**makes with** in the companion (C-490): its EASEL art, the songs it makes and sings there, and its sleep and
meditation sounds.

The KEY note is home. For 245 daemons, at least one of the other two notes lies outside the key. The recommended
rule:

- ***Exact, and an outside note is its own accidental.*** **A note always sounds at its own pitch and is always
  drawn in its own colour**, so SYNESTHESIA stays true: a player who learns the colours can still play what they
  see. An outside note is the daemon's signature: a blue note **used in passing and resolved to the nearest note of
  its key, never held under the others**. In a sleep drone, only the notes inside the key are held, and the
  accidental sounds now and then and resolves.

The alternatives:

- ***Fitted*:** an outside note moves a semitone into the key, and its colour follows the note it becomes. This
  means a daemon's DAY colour is sometimes not its day's colour.
- ***Inside the key only*:** an outside note colours the daemon's art but never sounds.

## 5. A daemon with two types

**Recommended: its key is its first type's, as its song's is**, so the KEY note is the key its song is heard in.
The second type gives no note. DEVELOPER MODE's palette window (C-490) can still name it beside TYPE.

The alternatives:

- The first type's key as its KEY note, with the second type's tonic as a faint fourth colour, in the palette only.
- One KEY colour blended from both types' tonics, as a black key blends its neighbours. It would no longer match
  the key its song is in.

## 6. Where it shows

- **In the game: nowhere new** (craft rule 1). Its song is already in its key.
- **In the companion** (C-490): what it makes leans on its three notes and colours. With DEVELOPER MODE on, its INDEX
  entry shows a palette icon that opens TYPE, DAY and MONTH, each with its key or note and its colours, for example
  *DAY · TUESDAY · E · YELLOW*. The meanings are the wheels' own words, already on TODAY and THE CALENDAR.
  **Nothing new needs to be written.**

## 7. For the user

1. **Both wheels, or only the week?** Recommended: both (332 different sets against 107, and the user leans both
   "for making music").
2. **A note outside the key:** *exact, as its own accidental* (recommended), *fitted to the key*, or *colour only*.
3. **Two types:** *the first type's key only* (recommended), *a faint fourth colour*, or *a blend of the two*.
4. **What each colour means:** *the wheels' own meanings* (recommended: kind, practice, gift, as in section 2), or
   *colours only, no meaning*.

*Built once answered: the companion's SYNESTHESIA gains `Synesthesia.daemon(n, type)` returning the three qualia,
tested against this page's table; then C-490. The bible gets a short 9.36 entry when the user says yes.*
