# THE VERSES -- a line's song as one song, a quote a verse (T-613) -- DRAFT

*A proposal, its decisions taken by the user on 2026-11-23 (section 4). Nothing here is built yet. It rewrites how T-594's songs are made; the songs in
the game today stay until the new ones are built and heard.*

## 1. Is it true that daemons share their first seven notes?

**Yes.** Some forms' own parts open with the same first seven notes, in the same key, as another form's own part. The
game's summon (T-598) hears only the order of pitch classes, on the key wheel. It ignores octave and rhythm.

- **82 of the 400 forms are affected, in 37 groups** (the table is at the end).
- **74 of them are in different lines.** Only four groups are one line with itself (ROVERCUB and ROVERBYTE, for
  example).
- **The largest group is seven daemons**: HIBERNATE, DUALCORE, STAMPEDE, SUBSTRATE, ILLUSION, IMITATION and HASHCODE
  all open E G C G C G D in C major.
- **Counting octave and rhythm, only 4 forms would clash.** The clashes come from what the summon listens for, and
  from how the openings were made.

**Why, in the generator (`tools/gensongs.py`):**

1. **Every form of a line opens with the line's cry.** "Every form of a line opens alike" was a rule: a form's own
   part begins with the same turned motif, so ROVERBYTE's verse opens as ROVERCUB's does. You wanted the opposite: each
   form's verse starts with something its own.
2. **The cry is the type's motif, which is only two or three notes, repeated.** That is the G C G C G you can see all
   through the table. It gave every type a family sound, but it also gave the openings so little to tell them apart.
3. **CONTENT and CONTEXT are the same seven white keys.** C major and its relative minor are played on one wheel, and
   they are the two commonest types. 49 of the 82 are in C major or A minor.
4. **The tune after the opening is a walk.** Each word of the INDEX entry moves it a step or two, by its first letter.
   This is the "lacks soul" you hear: there are no phrases, no question and answer, no high point, no return.

Today's summon gets around clashes by lengthening the openings: 93 were lengthened (to as many as 13 notes) and one,
THENCASE, was left out. **None of that is needed if every verse is written to be unique from its first note.**

## 2. What you asked for, as a design

**A line's song is one song in verses.** Each form is a verse. ROVERCUB, ROVERSEER and ROVERBYTE are three verses that
sound like three songs and also like one song.

- **Every verse is whole on its own.** Its first seven notes, its HOOK, already feel nearly complete, the way a phrase
  ends on an open but restful note. By its last note the verse has come all the way home.
- **The verses complement each other.** They share the line's key, metre and tempo. The voice deepens with each stage,
  but the song stays one song.
- **A HIDDEN CHORUS, only where a line needs one.** It is short (two to four bars) and comes between the verses. It is
  heard only once the final form knows its whole song; until then the song goes verse to verse with nothing between.
  The chorus is where the family sound now lives, since the shared cry is no longer at the start of each verse. A line
  whose first type changes as it evolves (11 lines) turns to its new key in the chorus.
- **A quote a verse, and the chorus in italics.** Each verse has its own QUOTE, and its words appear as the verse sings
  them. Each quote is whole on its own, and a line's quotes, read in order, say something more together. Where they
  need joining, the chorus has a few words, in italics, shown between the quotes, every time the chorus is sung.
- **A summon is the verse's HOOK: its first seven notes, in its key.** You play the hook, and the daemon sings its
  whole song: every earlier verse, then its own, with the chorus between them once it is unlocked. *(As in the game
  you are thinking of, the snippet calls the whole song.)*
  - **The hook plays in the right shape, but the wrong key:** the summon answers ALMOST, with the same effect as the
    singing fir. Every hook gets its own shape, so the game can tell whose it almost was.
  - **A daemon you hold** answers once it knows its hook. It sings what it knows: its words are clear under the notes
    it has learned and scrambled under the static (C-485 draws this in the app; T-610 in the game).
  - **A daemon you don't hold** still comes (your answer just now). It sings as something not yet learned: static,
    scrambled words, a glimpse.
- **What a verse is drawn from**, in this order:
  - its **type**: the key, the mode, and the book's character for that type, which also sets the quote's style;
  - its **name**: the rhythm, and what the name means. TANGENT's verse rises along a slope, then leaves it on a
    straight line;
  - its **INDEX entry**, both editions: the CONTENT entry as the image the quote is written from, the CONTEXT entry as
    the bass under the tune (as today);
  - **its quote**. The verse's tune is set to the quote's words, a note a syllable, so the words appear exactly when
    they are sung. This is not lyrics, since nothing is sung; the words are set the way a hymn tune sets a text.

**What stays:**

- the key table (18 types, approved);
- the colours of the notes;
- the static, and the share learned from experience;
- each form's levels (a verse is learned over the same levels its part is now);
- the shiny's notes (T-602), re-derived from the new tunes;
- the hum (T-596);
- PLAY FREELY in the companion (C-419).

## 3. What has to change

| Where | What changes |
|---|---|
| **`tools/gensongs.py`** | A new composer. Each verse is built from phrases: the HOOK is seven notes that end open, and an ANSWER comes home. A verse has one high point, leaps are recovered by steps, and a motif is repeated and then varied. Each line gets a chorus. Each hook is checked against all 400: no two hooks share a shape, transposed or not, so none needs lengthening and the wrong key can say whose hook it almost was. The tune is set to its quote. It still writes the engine's tables, the summons and the companion's songs.json. |
| **The quotes (T-599, story lane)** | Each form's quote becomes its VERSE QUOTE: whole on its own, and part of its line's set. Each line that needs one gets a few CHORUS words. T-599's question 4 ("Do a line's quotations belong together?") is answered by this. It needs about 400 quotes and at most 146 choruses (one for each final form of a multi-stage line). |
| **The cry** | Each form's cry becomes its own HOOK, so the cry you hear in a battle is what you play to call the daemon. Today a line shares one cry. *(Recommended; see the decisions.)* |
| **The engine** | The summon listens for the hooks, which are all seven notes. A summon sings the whole song, chorus included once it is unlocked, with the quote's words appearing (T-610). The wrong key answers ALMOST. The chorus is unlocked when the final form's verse is perfect. An unlearned note is a detuned chord (T-611). New data: the chorus's notes, and the note each word appears on. |
| **The companion** | songs.json carries the chorus and the word timings. ITS SONG, the INDEX's SONG and a summon sing the same song (C-485). THE BOOK OF QUOTATIONS (T-600) prints a line as verses, with the chorus in italics between them. |
| **Re-derived, not redesigned** | T-597's palette colours (which notes bring each colour in), T-602's shiny notes, the companion's summons. |

## 4. Decided (the user, 2026-11-23, by multiple choice)

1. **A daemon with two types (175 of the 400):** the first type sets the key and the quote's style. The second type
   shades the verse: its motif colours the answer phrase, and its character colours the quote.
2. **One key and one tempo for a line:** every verse of a line shares its key, metre and tempo, and each stage sings
   lower. A line whose type changes turns to the new key in its chorus.
3. **The tune is set to the quote, a note a syllable:** the quote's rhythm shapes the tune, and each word appears on
   its own note. The quotes are written first, and the songs follow a batch behind.
4. **The cry is the hook:** each form's cry is its own verse's seven-note hook. Hear it in a battle, play it to call
   the daemon.
5. **The review:** by type, in 18 batches (the recommendation; not asked separately).
6. **Who comes (asked earlier the same day):** any daemon answers its hook. One you hold sings as far as it knows; one
   you don't hold sings as something not yet learned.

**And how a line is presented (the user, the same answer):**

- **The app** (C-491): a type's section shows each line's forms side by side, with an arrow between each pair. Under
  each sprite is its verse's music, and under that its verse quote. Under the whole set is the whole song, its notes
  coloured and moving as they do now.
  - As a verse plays, its daemon is lit and dances a little.
  - In the chorus, the arrow lights, and the daemon just sung fades to a glow it keeps. The next one lights with its
    verse.
  - After the song, every form keeps its glow.
  - Buttons: the music alone, the quote alone (a verse at a time), or the whole presentation: the whole song with its
    chorus and its quotes sung as lyrics (T-614).
- **The PDF** (T-600): the same layout, still.
- **The full book:** it opens once every daemon's song is unlocked. Until then it shows a riddle whose answer is found
  in the game. The answer downloads the full book's zip (from git), which holds the book and its recording. The
  recording plays the songs as well as reading the book.

## 5. The plan, about 400 daemons

| Step | What | Who | Size |
|---|---|---|---|
| 0 | ~~These decisions~~ (taken, section 4); the design goes into the bible (9.36) with the sampler | audio | with step 1 |
| 1 | **The composer** (gensongs v2), shown on six lines first: ROVERCUB's three verses, TANGENT, a single-stage daemon, a dual-type daemon, a line that changes type, a branch. Each comes as a sampler and a sheet, with placeholder quotes. | audio | a day |
| 2 | **The quotes.** About 400 verse quotes and up to 146 chorus lines, in T-599's styles, by type, with every line's set read together. | story | 18 batches |
| 3 | **The songs set to their quotes**, batch by batch as the quotes are picked; the hook-uniqueness check runs over all 400 every time | audio | 18 batches |
| 4 | **The engine**: a summon that sings the whole song, the words appearing, ALMOST in the wrong key, the chorus unlocked (T-610). The detuned chord (T-611). The cry becomes the hook. | audio, game | two or three days |
| 5 | **The companion**: songs.json's chorus and word timings, ITS SONG, the summon (C-485), and the book (T-600) | app | a day or two |
| 6 | **Re-derived**: colours (T-597), shiny notes (T-602), summons; then the push routine, with picture sheets and a sampler of every type | audio | a day |

**Step 1 drafted, 2026-11-23** (`tools/genverses.py --sampler`, `audio/drafts/t613_verses/`): six lines plus today's
ROVERCUB line for comparison, a sheet for each, and every hook alone. Every one of the 400 forms was given a hook (the
six lines' quotes, and each other form's INDEX entry standing in for its quote), and all 400 hooks are different. None
was lengthened, and none was left out.

**Built in the game and the companion, 2026-11-23** (the user: "Good, go on"):
- **Every daemon's song is now made of verses** (`tools/gensongs.py` builds from `tools/genverses.py`). Each verse uses
  its T-599 draft quotation where one exists. The sampler's placeholder words stand in for 7 forms, and the INDEX entry
  stands in for the other 342 until T-599 writes them.
- **Every summon is the form's seven-note hook.** All 400 are unique; none was lengthened and none was left out.
- **The hidden chorus** is sung between a final form's verses once a daemon the player holds knows its verse whole. In
  the game this is SHARE_CHORUS, from `sSongChorusParts`; in the companion it is `withChorus`. Only the five sampler
  lines have chorus words, all placeholders, so only they have a chorus yet.
- **A breath after each phrase:** a note sounds for at most 2.5 beats, and the rest of its length is silence.
- **A summoned daemon sings its whole song.** One the player holds sings it as far as it knows it; one nobody holds
  sings its own verse as static.
- **ALMOST:** a hook played in the wrong key comes back flat, followed by PLAY's own ALMOST line.
- **Re-derived from the new tunes:** the shiny notes (T-602) and the colour ties (T-597).

**Not built yet:**
- the quotation's words appearing as the daemon sings (T-610 and C-485, which wait on T-599);
- the cry becoming the hook (gencries);
- ALMOST in the companion's PLAY FREELY;
- the out-of-tune chord for an unlearned note (T-611).

Steps 1 and 2 can run side by side. Step 3 follows step 2 a batch behind, so the first types can be heard while the
last are still being written.

## Appendix: the forms whose own parts open alike today

The first seven notes of each form's own part, by pitch, ignoring octave and rhythm (as the summon hears them), on the
same key wheel. The black keys are spelled as on the piano, so E major's G-sharp is written A♭.

| The first 7 notes | The forms that open with them (their key) | One line? |
|---|---|---|
| E G C G C G D | HIBERNATE (C major), DUALCORE (C major), STAMPEDE (C major), SUBSTRATE (C major), ILLUSION (C major), IMITATION (C major), HASHCODE (C major) | 7 lines |
| D G C G C G D | BROADCAST (C major), BLINDSPOT (C major), LOOPBACK (C major) | 3 lines |
| E C G C G D C | COOKIE (C major), PENPHIN (A minor), ATTUNE (A minor) | 3 lines |
| E♭ F♯ A♭ E♭ A♭ A♭ F♯ | ROOTKIT (E major), IFTRUE (E major), IFFALSE (E major) | 2 lines |
| E A B♭ D F A C | BACKBONE (D minor), BIGENDIAN (D minor) | 2 lines |
| C E♭ F A♭ B♭ D♭ C | CAPSULE (A-flat major), SEEPAGE (A-flat major) | 2 lines |
| E♭ F♯ B♭ B B♭ E♭ F♯ | CINDER (E-flat minor), PHOENIX (E-flat minor) | 2 lines |
| A♭ D♭ B D♭ A♭ A D♭ | CRAWLER (E major), REAPER (E major) | 2 lines |
| G C G C G C D | DATAGRAM (C major), DAYDREAM (C major) | 2 lines |
| G C G C G C A | DEADLOCK (C major), RESENTMENT (A minor) | 2 lines |
| G B♭ B♭ B♭ F B♭ C | FIRMWARE (E-flat major), PAIRWISE (E-flat major) | 2 lines |
| E♭ F♯ F♯ D♭ A♭ F♯ F | FUSE (F-sharp major), ANODE (F-sharp major) | 2 lines |
| B♭ F♯ D♭ F♯ F♯ F♯ E♭ | HANDSHAKE (F-sharp major), COROUTINE (F-sharp major) | same line |
| B D G D G D A | HEARTBEAT (C major), SHIFTLEFT (C major) | 2 lines |
| A♭ B D♭ A♭ D♭ B A♭ | HOARDING (E major), HASHSEED (E major) | 2 lines |
| A♭ B D♭ A♭ D♭ D♭ B | HUDDLE (E major), STARTLE (E major) | 2 lines |
| A C F C G F E | HUNCH (A minor), MIME (A minor) | 2 lines |
| B♭ F G B♭ C E♭ C | ILLUMINED (A-flat major), SHALLOWS (A-flat major) | 2 lines |
| A F C F C C F | KAIROS (A minor), PROTEUS (A minor) | 2 lines |
| A G D G D A G | LOOKOUT (C major), BASTET (C major) | 2 lines |
| E C G C A G F | MOCK (C major), CACHE (C major) | 2 lines |
| E G C G C A G | NIBBLE (C major), COMFORT (C major) | 2 lines |
| A C G C G A C | OUTLIER (C major), KEEPER (C major) | 2 lines |
| E D G D G D A | OVERFLOW (C major), TRIPLECORE (C major) | 2 lines |
| C G C G C A G | PACKET (C major), UPTIME (C major) | 2 lines |
| F A D E♭ F A B♭ | REBUTTAL (G minor), CIRCULAR (G minor) | same line |
| B♭ D♭ F♯ F♯ F♯ E♭ D♭ | RELEASE (F-sharp major), CRACKLE (F-sharp major) | 2 lines |
| E C G C G C E | RESIDUAL (C major), MINDWANDER (C major) | 2 lines |
| A C A G F D D | ROVERCUB (F major), ROVERBYTE (F major) | same line |
| B D G D G B D | RUBRIC (C major), CRYWOLF (C major) | 2 lines |
| E G C G C G G | SHORTJUMP (C major), WRAPAROUND (C major) | 2 lines |
| E G C G C D G | STANDBY (C major), WARNING (C major) | 2 lines |
| B D G D G A D | SUSPEND (C major), CRAVING (C major) | 2 lines |
| C E♭ E♭ B♭ B♭ E♭ D | TALOS (E-flat major), ELPIS (E-flat major) | 2 lines |
| D♭ B D♭ A♭ D♭ B E♭ | THENCASE (E major), OTHERWISE (E major) | same line |
| D G C G C A G | VALENCE (C major), LOWBIT (C major) | 2 lines |
| B F C F C F D | VIGILANCE (A minor), GUESSWORK (A minor) | 2 lines |
