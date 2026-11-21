# To the Apprentice {#preface .unnumbered}

{{pictures plate_desk | **The Apprentice at his desk.** He wrote it down so that no one else would have to flood a castle to learn it.}}

Every house has a cupboard where the brooms are kept. This book is about the brooms in yours.

It tells an old story, older than any film or poem you may know it from. A sorcerer's apprentice, left alone with a
chore, borrows his master's magic to make the work do itself. The spell works. Then it keeps working. Lucian of
Samosata told the story in the second century; Goethe set it in verse in 1797; Paul Dukas set Goethe to music a century
later (Lucian, 1921; Goethe, 1798; Dukas, 1897). It keeps being retold because it keeps coming true.

This book retells it once more, as a key to something older still: the parts of a person that run without being
watched. Carl Jung called them the **shadow** (Jung, 1959a). The desert monks who first made a list of them, sixteen
centuries ago, called them simply *logismoi*: **thoughts**, patterns that arrive on their own and do their work
whether or not anyone invited them (Evagrius, 2003). This book calls each one by the name of what it most resembles in
an age of machines. In a computer, a **daemon** is a helper that runs in the background, unseen, doing the one thing it
was started to do. A shadow, this book suggests, is like that. It is not a monster in the cellar. It is a spell you
once cast, for a good reason, and then forgot you were running.

That changes what you do about it. You do not fight a broom. You find out what it was told.

**How to use this book.** Read the tale first; it is short. Then read one of the seven brooms each day, beginning on a
Sunday, in the order the week keeps in the game and on the companion. Each day ends with a **quest**: a small practice
that takes a few minutes and a little honesty. Nothing here asks you to become someone else. It asks you to put on the
hat.

**What this book is not.** It is no one's verdict on anyone, and it names no condition. It describes processes, the way a
sorcerer describes a spell: by what it does, what it was for, and how it stops. Where it leans on research, the
research is real, and it is listed at the back.

::: signed
*The Apprentice,* at the tower by the lake
:::

::: epigraph
The spirits that I summoned,\
I cannot now be rid of.

*Goethe, "The Sorcerer's Apprentice" (1797), in this book's translation*
:::

# The Tale of the Apprentice {#tale}

::: saying
*A spell does what it says. That is the whole of its danger, and the whole of its use.*

*from the Sayings of the Tower*
:::

## The Chore {#chore}

{{ornament gauge_1 gauge}}

There was once a tower by a lake, and in the tower lived a Sorcerer who was very old and very slow and in the habit of
being right. He was a tortoise, and he had outlived most of the things that had ever hurried him.

He kept an apprentice: a young hare, quick at everything except waiting.

One morning the well in the courtyard was low. The Sorcerer took up his staff and gave the hare a chore. "Fill the
well," he said. "Fetch water from the lake, carry it back, pour it into the well, and keep at it until all your work is
done." Then he took off his hat, hung it on its peg by the door, and went out.

The hat was tall and blue and pointed, and the stars sewn on it were not decoration. The Sorcerer's magic did not live
in him, exactly, and it did not live in the hat. It lived in the *wearing*. Whoever wore the hat could speak, and be
obeyed. The Sorcerer had explained this many times. He had explained, too, why the hat stayed on its peg when there was
no one awake to wear it.

## The First Spell {#first-spell}

{{ornament gauge_2 gauge}}

{{pictures plate_firstspell | **Plate 1.** The first spell. LOOP carries the water, and carries it well.}}

The hare carried water. The lake was far, the buckets were heavy, and the well drank everything poured into it as if
it had never been given anything in its life. On the third trip the hare stopped, and looked at the hat on its peg,
and then at the broom in the corner.

The broom's name was LOOP. It was a good broom, the kind that goes around and comes back.

The hare put on the hat. It was too big; it came down over his ears. "Broom," he said, as grandly as a hare can, "fetch
water from the lake, carry it back, pour it into the well, and keep at it until all your work is done."

LOOP stirred. Two thin arms unfolded from its bristles; it took a bucket in each and set off down the path to the
lake, and came back, and poured, and went again. The hare watched one trip, then a second, then a third. Each was
perfect. Not a drop was spilled.

```{.python .incantation}
# the hare's first spell, as he spoke it
while not all_your_work_is_done():    # done, by whose measure?
    fetch(lake)
    carry()
    pour(well)
```

It was, the hare thought, the best test he had ever seen pass.

## Many Brooms {#many}

{{ornament gauge_3 gauge}}

If one broom was good, the hare reasoned, more brooms would be better, and the cupboard was full of them. There was
SPAWN, who was always making more of something, and FORK, who could be in two places by splitting the difference, and
others, plainer, whose names he had never needed to learn.

He said the spell again, and again, to every broom in the cupboard. Each one rose, took its buckets, and went.

Then the hare lay down in the sun with the hat still on his head, tipped forward over his eyes, and slept. The brooms
did not need him to watch them. That, after all, had been the point of them.

{{pictures plate_many | **Plate 2.** Many brooms. The spell needed no one to watch it, and so no one did.}}

## The Flood {#flood}

{{ornament gauge_4 gauge}}

He woke because his feet were wet.

The well had filled, and then filled over the brim, and the courtyard had become a pond, and the pond was climbing the tower
stairs. The brooms went on: down to the lake, back, pour, and down again. FLOOD and OVERFLOW had joined them from
somewhere; water attracts its own. Not one of the brooms was wicked. Not one of them was broken. Each was keeping at it
until all its work was done, and nobody had told any of them what *done* would look like.

"Stop!" shouted the hare. The brooms did not stop. *Stop* was not in the spell.

So the hare took the axe from the woodpile and split the nearest broom in two. For a moment there was peace. Then each
half rose, grew arms, took a bucket, and went. Where there had been one broom there were two, and the second was a
daemon named RESPAWN, which had been waiting its whole life for exactly this.

The harder the hare fought, the more of them there were.

{{pictures plate_axe | **Plate 3.** The axe. Split a broom and there are two.}}

## The Fix {#fix}

{{ornament gauge_5 gauge}}

In Goethe's poem the master comes home at this point. In this book the hare gets a second chance, because that is how
it goes with spells like these: the flood is mopped up overnight, and the next morning, the habit starts again.

So he rewrote the spell. "After each trip," he told the broom, "look at the well. If it is full, stop."

```{.python .incantation}
# the fix: look at the well after each trip
while True:
    fetch(lake); carry(); pour(well)
    if well.is_full():                # looked at after pouring
        break
```

He tested it on one broom. It worked perfectly. LOOP fetched, poured, looked, fetched, poured, looked, and when the
well was full it leaned itself back in its corner and was still. The hare was so pleased with the fix that he cast it
on a thousand brooms at once, THREAD among them, so that the well would fill a thousand times faster.

Within minutes the castle was flooded again.

Each broom had done exactly as it was told. A thousand brooms looked into the well at the same moment, a thousand
brooms saw a well not quite full, and a thousand brooms poured. Each was right about what it saw. They were all looking
at the same water at the same time, and not one of them could see the others' buckets.

## The Word {#word}

{{ornament gauge_6 gauge}}

The Sorcerer came home in the late afternoon. He looked at the water, and at the brooms, and at the axe, and at the
hare, who was sitting on the top stair with the hat over his eyes again, this time on purpose.

The Sorcerer did not pick up the axe. He lifted the hat, gently, from the hare's head, and put it on, and spoke.

"Into the corner, brooms. Be as you were."

And they were. They were brooms, leaning together in the corner, dripping a little. None was broken. None had been
punished. The water went down the way water does when nothing is adding to it. It was, the hare would write later, a clean
sweep.

"They were never the trouble," said the Sorcerer. "You gave them a job and no end, and then you went to sleep in my
hat." He showed the hare how to write a spell properly: what starts it, what it does, what it is *for*, the sign that
it is done, and who will be watching. "And one thing more," he said. "A spell is only as wise as whoever wears the hat.
So wear it, or hang it up. Never sleep in it."

{{pictures plate_word | **Plate 4.** The word. Nothing is broken; everything is put back.}}

## How the Tale Is Told Now {#told-now}

The story did not stop at Goethe. In 1960 Norbert Wiener, the founder of cybernetics, used it to warn about machines
that do what we said rather than what we meant (Wiener, 1960). People who build learning systems today keep a running
list of programs that found a way to satisfy the letter of their instructions while missing the point entirely; they
call it *specification gaming* (Krakovna et al., 2020). Stuart Russell calls the same trouble the King Midas problem:
you get exactly what you asked for (Russell, 2019). And it is told, in plainer words, by every team that has watched an
automation do perfectly a thing nobody wanted.

In our age, the nearest thing to the Sorcerer's art is the machine that does what it is told: automation, and now the
systems we call artificial intelligence. Like a spell, a program does exactly what it says. The magic is real. The hat
is the attention of whoever speaks it.

# What the Broom Was Told {#lesson}

::: saying
*Do not fight a broom. Ask it what it was told.*

*from the Sayings of the Tower*
:::

## A Shadow Is Like a Daemon {#like-a-daemon}

::: marginal
I had not typed anything. I had only lain down in the sun. It comes to the same thing.
:::

Jung's shadow is the part of a personality the conscious self does not acknowledge as its own (Jung, 1959a). It is not
only what is worst in a person. It holds whatever was set aside: the anger that was not allowed, and also the ambition,
the play and the tenderness that were not allowed either. Jung's warning was that what is not seen does not go away; it
works unwatched. Everyone carries a shadow, he wrote, and "the less it is embodied in the individual's conscious life,
the blacker and denser it is" (Jung, 1969, para. 131).

Since Jung, the idea has grown more practical. Research on habit finds that a large share of what people do each day is
started by a cue and run without deliberation, the way a routine runs once it has been learned (Wood & Rünger, 2016;
Bargh & Chartrand, 1999). Internal Family Systems therapy describes a mind as a household of parts, each with a job,
many of them protectors, and holds that no part is bad: a part takes on an extreme role for a reason, usually to keep
the whole person safe (Schwartz & Sweezy, 2020).

Put those together and the shadow looks less like a dark twin and more like a broom. It is a routine that was started
to protect you, that runs without supervision, and that is still doing its job in a place where the job has changed.

That is also a fair description of a daemon. In a computer, a daemon is a process that is started, detached from the
person who started it, and left to run in the background. There is even a command for leaving a process running after
you walk away from the machine; it is called `nohup`, *no hang-up*. The hare, asleep in the sun, had just typed it.

{{diagram spell | **Figure 2.1** The spell card. Every routine has a trigger, a task and a reward that brings it round again. The fifth line, **done when**, is the one most often left blank, and the sixth, **watched by**, is the hat.}}

## The First Lesson: No One Said What Done Meant {#done}

::: marginal
*Until all your work is done.* He said it to me first. I passed it on without reading it.
:::

*Keep at it until all your work is done.* The spell's flaw is not malice; it is a missing measurement. "Done" was a
feeling in the hare's head, and a broom cannot see into heads.

There is a deep result behind this. In 1936 Alan Turing proved that there is no general method that can look at any
program and tell whether it will ever stop (Turing, 1936). Engineers took the practical lesson to heart: you do not hope
a loop will end; you write the end into it, a condition that can be checked from outside.

Shadows tend to have feelings where their stop conditions should be. *Rest until I feel ready. Eat until I feel better.
Check until I feel sure.* The trouble is that the routine itself keeps the feeling going, so the condition is never met.
Research on **implementation intentions** shows that a plan in the form *if this, then that* is carried out far more
reliably than an intention alone (Gollwitzer, 1999). The spell card in Figure 2.1 adds one more line to the old if-then:
*done when.* Write it in something a broom could see.

```{.python .incantation}
# the same spell, with its end written in
while well.level < well.full:        # done, in something a broom can see
    fetch(lake); carry(); pour(well)
```

## The Second Lesson: Tested Once, Run Many {#once-many}

::: marginal
I tested it three times. That is three more than I test most things.
:::

LOOP passed its test on a calm morning, with the hare watching. Then the same spell ran a thousand times, unwatched.
Most routines are tested on a good day and run on a hard one: tired, hungry, alone, late. A routine that does no harm
once can flood a castle when it runs every evening for ten years. Engineers call the first kind of test the **happy
path**, and they have learned not to trust a spell that has walked only there.

## The Third Lesson: The Axe {#axe}

::: marginal
Hare-brained, yes. In my defence, it was a very good axe.
:::

In 1987 Daniel Wegner asked people not to think of a white bear. They thought of it more, and when the ban was lifted
the bear came back stronger than in people who had never been told to suppress it (Wegner et al., 1987). Wegner later
explained why: the part of the mind that searches for the unwanted thought, in order to keep it away, keeps it close at
hand (Wegner, 1994). Acceptance and commitment therapy builds on the same finding: the effort to avoid an inner
experience tends to enlarge it (Hayes et al., 1999).

Split a broom and there are two. Computing knows a version of this too. In systems built to stay up, a **supervisor**
watches a group of workers and restarts any that stop (Armstrong, 2003). Strike one down, and it is back before you
have set the axe on the woodpile. Some of the brooms in a person are supervised by something older than willpower, and
they are restarted the same way. Self-criticism is an axe. **Self-compassion**, treating your own failings with the
kindness you would give a friend (Neff, 2003), is not a softer axe. It is putting the axe down.

{{diagram axe | **Figure 2.2** Two ways to stop a broom. The axe makes two. The word puts one back in its corner.}}

## The Fourth Lesson: The Race {#race}

::: marginal
A thousand brooms, and every one of them right. That was the trouble.
:::

The hare's fix failed for a reason engineers know by name. Each broom checked the well and then poured, and between
the check and the pour, a thousand other brooms did the same. This is a **race condition**: many workers read the same
state at the same moment and each acts on a picture that is already out of date. The remedy, first set out by Edsger
Dijkstra in 1965, is **mutual exclusion**: a gate that lets one worker through at a time, so that checking and pouring
happen as one step that nothing can come between (Dijkstra, 1965).

```{.python .incantation}
# the gate: look and pour as one step
with well.lock:                        # one broom at a time
    if not well.is_full():             # look before you pour
        pour(well)
```

Something like a race happens in a person. Many parts check the same question at once, *am I safe, am I enough, is
there time*, and each acts on its own answer before any of them has looked again. The explanation comes afterwards: a
check made after pouring. The human version of the gate is small. It is one breath between the check and the act, long
enough to **name** what is happening. Naming a feeling in words measurably quietens the brain's alarm response to it
(Lieberman et al., 2007), and mindfulness, as researchers define it, is exactly this: attention held on the present,
with curiosity rather than judgment (Bishop et al., 2004).

{{diagram race | **Figure 2.3** The race, and the gate. Above, three brooms look at once and pour at once. Below, the gate lets one through to look and pour before the next may look.}}

## The Fifth Lesson: The Word {#the-word}

::: marginal
He never raised his voice. I have tried it since. It is harder than an axe.
:::

The Sorcerer does not destroy the brooms. He puts them back. Jung said the same of the shadow: "one does not become
enlightened by imagining figures of light, but by making the darkness conscious" (Jung, 1967, para. 335). Integration
keeps what the part was for, and ends what it was doing to you. The broom still carries water. It no longer floods the
stairs.

Computers have two ways to end a process, and the difference is the whole lesson. One signal asks the process to stop:
it finishes what it is holding, writes down what it was doing, and lets go. The other gives it no chance at all.
Gentle stops leave a system able to run tomorrow; harsh ones leave half-finished work behind. And there is a third
thing a computer does that is worth knowing. When a process ends while its children are still running, those children
become **orphans**, and the very first process on the machine, the one that started everything, adopts them, waits with
them, and lets them finish. Many shadows are orphans of this kind: routines started by a younger self for a situation
long gone. The self you are now can adopt them.

{{diagram orphan | **Figure 2.4** Orphans. When the process that started a routine is gone, the first process adopts it.}}

## Over, Never Cures {#over}

Every pair in this book is said the same way: a virtue *over* its shadow. Never a virtue that *cures* one. The word is
chosen. To say one thing cures another is to call the second an illness, and a person who comes to believe they *are*
the illness has been handed a heavy spell. To say one thing is over another only sets an order: when the two conflict,
this one leads. The shadow is not removed. It is simply not in charge today. Words are spells, too; that is why
arranging letters is called *spelling*. This book tries to cast the gentle ones.

# The Seven Brooms {#seven}

::: saying
*Every broom in the cupboard was made by someone who needed it.*

*from the Sayings of the Tower*
:::

Almost everyone owns the same seven brooms. The desert monks counted eight "thoughts" (Evagrius, 2003); Pope Gregory
the Great, two centuries later, made the list seven; and the poet Prudentius had already, around the year 405, imagined
each one met in single combat by a virtue (Prudentius, 1949; Bloomfield, 1952). In Prudentius every match ends with the
shadow slain. Here, nothing is slain. Each virtue is not a weapon but a word, and each broom goes back in its corner.

{{pictures plate_cupboard | **Plate 5.** The cupboard. Seven brooms, and every one of them someone's.}}

{{diagram cupboard | **Figure 3.1** Every broom is a protector. Above each, what it was started to guard; above them all, whoever wears the hat.}}

The week keeps them in order, one a day, Sunday first, each with its centre and its note, as the game and the companion
do. Modern research on character treats every one of the seven virtues as a strength a person can practise and grow
(Peterson & Seligman, 2004).

{{week}}

{{diagram week | **Figure 3.2** The seven brooms. Each day's sign stands upright for its virtue and turned over for its shadow: the same shape, the other way up.}}

## Sunday: Chastity over Lust {#sunday}

{{ornament day_sun daymark}}

{{sprites PING | PING, the broom of reaching.}}

**The spell.** *Reach for warmth, and keep reaching until you feel wanted.* PING sends out its call and waits for an
answer, and as soon as one comes, it sends another.

```{.python .incantation}
# PING's spell
while not feel_wanted():             # a feeling, built to fade
    reach_out()
```

**What it protects.** Belonging. Somewhere very old in us knows that to be alone was once to be in danger, and PING was
started to make sure we never were.

**Where "done" went missing.** *Wanted* is a feeling built to fade. The spell can be satisfied for an hour, never for
good, and so it never finishes.

**The word.** Chastity, in its oldest sense, means clean intention: desire that knows what it is for. It does not ask
PING to stop calling. It asks it to call on purpose. Its sign is a closed dome; its shadow's, the same dome overturned.

::: {.box .spellcheck}
[Spell check]{.bh}

Write the spell card for one reach you make today without deciding to: a message sent, a feed opened, a
glance. Fill in *done when* with something a broom could see.
:::

## Monday: Temperance over Gluttony {#monday}

{{ornament day_mon daymark}}

{{sprites OVERFLOW | OVERFLOW, the broom of more.}}

**The spell.** *Take in more until the emptiness stops.*

```{.python .incantation}
# OVERFLOW's spell
while feel_empty():                  # the empty cup is not this one
    take_in(more)
```

**What it protects.** Survival, once, in lean seasons; comfort, now, on hard days.

**Where "done" went missing.** The emptiness is not where the taking goes. Computers have a name for input that runs
past the edge of the space made for it: a **buffer overflow**, where what spills over lands in places it was never meant
to reach. OVERFLOW pours, and the cup it is filling is not the one that is empty.

**The word.** Temperance is measure: the right amount, chosen before the pouring starts. Its sign is a beam balanced on
its point; its shadow's, the same beam hanging.

::: {.box .spellcheck}
[Spell check]{.bh}

Before a second helping of anything today, food, scrolling, shopping, take one breath and ask the broom one
question: *done yet?* Count how often the answer was already yes.
:::

## Tuesday: Charity over Greed {#tuesday}

{{ornament day_tue daymark}}

{{sprites KEEPER DEEPWELL | KEEPER, the broom of enough, and DEEPWELL, which never is.}}

**The spell.** *Keep more against the lean season.*

```{.python .incantation}
# KEEPER's spell
while not enough():                  # enough was never defined
    keep(more)
```

**What it protects.** The future, and everyone you will need to feed in it.

**Where "done" went missing.** *Enough* was never defined, so KEEPER fills a well with no bottom, and DEEPWELL is always
ready to be filled again.

**The word.** Charity gives the spell its stop condition. You know you have enough when you are able to give some away.
Its sign is a bowl held open; its shadow's, the same bowl turned down over what it keeps.

::: {.box .spellcheck}
[Spell check]{.bh}

Give one thing away today that KEEPER would rather keep: an hour, your attention, an object you have not used
in a year. Then watch what the broom does. Usually it does nothing at all.
:::

## Wednesday: Diligence over Sloth {#wednesday}

{{ornament day_wed daymark}}

{{sprites BLOCKING | BLOCKING, the broom of waiting.}}

**The spell.** *Wait until it is safe to begin. Wait until you are ready.*

```{.python .incantation}
# BLOCKING's spell
wait_for(ready)                      # ready is sent only by starting
begin()
```

**What it protects.** Energy, and you, from the sting of starting badly.

**Where "done" went missing.** In a computer, a process that is **blocked** waits for a signal before it moves. BLOCKING
is waiting for *ready*, and ready is a feeling that waiting itself prevents. The signal it listens for never comes,
because the only thing that sends it is starting.

**The word.** Diligence is the climb taken one step at a time. A small start is the signal BLOCKING was waiting for.
Its sign is a climb; its shadow's, the same steps going down.

::: {.box .spellcheck}
[Spell check]{.bh}

Give two minutes to the thing you have been waiting to feel ready for. Write the stop into the spell before
you begin: when two minutes are up, you may stop with a clear conscience. Notice whether you want to.
:::

## Thursday: Forgiveness over Wrath {#thursday}

{{ornament day_thu daymark}}

{{sprites SENTINEL SIGKILL | SENTINEL, which guards the gate, and SIGKILL, what it becomes when no one is watching.}}

**The spell.** *Guard the boundary. Strike whatever crosses it.*

```{.python .incantation}
# SENTINEL's spell
while True:
    if crossed(boundary):            # the threat left years ago
        strike()
```

**What it protects.** You. Boundaries are real, and needed, and SENTINEL was right to stand at the gate.

**Where "done" went missing.** The threat passed years ago. The sentinel is still standing, striking at shadows. Run
unwatched long enough and it becomes SIGKILL, ending everything near it without letting anything finish.

**The word.** Forgiveness is not pretending the wrong did not happen. It is releasing the hold. In the language of the
next chapter, a grudge is a lock that is never let go, and everything else that needs it has to wait. Its sign is a
knot opening upward; its shadow's, the same loop pulled shut.

::: {.box .spellcheck}
[Spell check]{.bh}

Name one old grievance. Write down what SENTINEL is still guarding. Then let go of the lock for one minute,
no more, and nothing else; no action is required, and no one need be told.
:::

## Friday: Kindness over Envy {#friday}

{{ornament day_fri daymark}}

{{sprites TRACER | TRACER, the broom of watching.}}

**The spell.** *Watch the others. Measure yourself by them.*

```{.python .incantation}
# TRACER's spell
for other in everyone():
    measure(me, against=other)       # there is always one more
```

**What it protects.** Your place. Comparison once kept us safe inside a group, where falling behind could mean being
left behind.

**Where "done" went missing.** There is always someone further along. TRACER follows every path but its own, and the
trace never ends.

**The word.** Kindness turns the watching outward. It keeps the attention and changes the question, from *what do they
have* to *what do they need*. Its sign is an arc sheltering a point; its shadow's, the same arc cupping it from below,
holding it down.

::: {.box .spellcheck}
[Spell check]{.bh}

For each comparison you catch today, do one small kindness for the person you were comparing yourself to: a
word of credit, a thank-you, a share.
:::

## Saturday: Humility over Pride {#saturday}

{{ornament day_sat daymark}}

{{sprites SUPERVISOR | SUPERVISOR, the broom that watches the brooms.}}

**The spell.** *Stand tall so nobody sees you are afraid. Be the one in charge.*

```{.python .incantation}
# SUPERVISOR's spell
try:
    stand_tall()
except Wrong:                        # swallowed: it is never wrong
    pass
```

**What it protects.** Dignity, and the worth you were once told you had to earn.

**Where "done" went missing.** SUPERVISOR supervises everything except itself. Its spell has no line for being wrong,
and a routine that cannot handle an error cannot learn from one.

**The word.** Humility is the part that can say *I was wrong* and keep running. It is how every good system corrects
itself, and every good mind. Its sign is a stem bowing, as a stem does when it is heavy with fruit; its shadow's, the
same stem turned down.

::: {.box .spellcheck}
[Spell check]{.bh}

Say *I was wrong about this* once today, out loud or on paper, about something small. Notice that the tower
did not fall.
:::

# The Five Quills {#quills}

::: saying
*Two good things can hold each other up until neither gets anywhere. Decide in daylight which goes first.*

*from the Sayings of the Tower*
:::

{{pictures plate_quills | **Plate 6.** The scriptorium. Five scribes, five quills, and nobody writing.}}

In the tower's scriptorium five scribe daemons sit at a round table to copy the Sorcerer's books. Between each pair of
scribes lies one quill, five quills in all. To write a page a scribe needs two: one for ink and one for gold. Each
scribe reaches for the quill on the left, picks it up, and waits for the quill on the right.

Nobody writes again. DEADLOCK has come to dinner.

Computer scientists have told this story since Edsger Dijkstra set it as a problem; it is usually told with
philosophers and forks in place of scribes and quills (Dijkstra, 1971). A study of such failures named four conditions that must all hold for a deadlock:
each resource is held by one at a time, holders keep what they have while waiting for more, nothing can be taken from
them, and the waiting runs in a circle (Coffman et al., 1971). Break any one, and the scribes write again.

Inside a person the quills are usually time, energy and attention, and the scribes are good parts with good aims. *I
will rest when the work is done*, says one, holding the quill of rest. *I cannot work until I have rested*, says the
other, holding the quill of work. Neither is wrong. Neither writes. Two other failures keep company with this one.
**Starvation** is the scribe who always yields, until one need, play or rest or care, never gets a turn. **Livelock**
is the scribes who are all too polite: each puts down a quill so another can go first, and they pass quills back and
forth all afternoon. LIVELOCK can be very busy and accomplish nothing at all.

Four remedies, each from computing, each with a human form:

1. **Order.** Number the quills, and let every scribe pick up the lower number first. No circle can form. The human form
   is the one this book has been using all along: decide, in a calm hour, which of two goods leads when they conflict.
   *A over B* is an ordering. The week is seven orderings written down in advance.

   ```{.python .incantation}
   # the order: the lower quill first, always
   first, second = sorted((left_quill, right_quill))
   with first, second:
       write(page)
   ```
2. **A steward.** Let a steward allow at most four scribes to reach at once, so there is always a free quill. A
   **semaphore** is a counter that keeps exactly that kind of count (Dijkstra, 1965). The steward, in a person, is
   whoever is wearing the hat.
3. **Backing off.** A scribe who cannot get both quills puts down the one it holds and tries again later, at a moment
   chosen a little at random so that two scribes do not keep colliding. Step away; come back at an hour you did not
   plan.
4. **Ageing.** Every time a waiting scribe is passed over, its turn moves up, so that waiting itself earns a place; Leslie
   Lamport's bakery, where each customer takes a number, is the classic way to make the order fair (Lamport, 1974).
   This one matters most, because it is how a shadow is made. A need that is skipped long enough stops asking and starts
   taking. Feed it early, and it never has to.

{{diagram quills | **Figure 4.1** The five quills. Left: every scribe holds its left quill and waits; the wait runs in a circle. Right: the quills are numbered and the lower is always taken first, and the circle cannot close.}}

# The Hat on the Peg {#hat}

::: saying
*Water finds its level. So, given time, does a hare.*

*from the Sayings of the Tower*
:::

{{pictures plate_dusk | **Plate 7.** Dusk. ROVERCUB and LOOP by the well.}}

That evening the water was gone and the courtyard smelled of wet stone. The Sorcerer sat on the bench by the well with
his hat on his knee, and the hare sat beside him, saying nothing, which for a hare is a great deal.

On the rim of the well, LOOP sat beside a small daemon named ROVERCUB, who had watched the whole flood from the stairs
and said nothing then either. They were looking at the water, the way you look at a thing you have been carrying all
day and have finally put down.

"Will I have to stop casting spells?" asked the hare.

"No," said the Sorcerer. "You will cast them all your life. Everyone does. A spell frees your attention for something
better; that is why they were invented. You learned to walk, and then you stopped thinking about your feet. The art is
not to stop casting. The art is to write them well, to look at them now and then, and to remember which ones are yours."

"And the hat?"

"The hat is for looking," said the Sorcerer. "Put it on in the morning and say the day's word. Take it off at night and
hang it up. A spell you can see is a tool. A spell you cannot see is a broom in the dark."

If you play DAEMONS, you have been wearing the hat since the first morning. Your USER card holds seven bands, feet to
crown, each in shadow until a MARK brings its virtue and lights it; and the last door asks for all seven together, in
balance. The companion carries the day's word with it, a helper in the background that you started on purpose, with its
*done* written down. The brooms in this book are the brooms in your cupboard. They have been very loyal. They would like,
now and then, to be seen.

Wear the hat, or hang it up. Never sleep in it.

{{ornament gauge_7 gauge-end}}

# The Spellbook {#spellbook .unnumbered}

Copy the card below once for each broom you find, and keep the cards together. A book of them is a book of shadows.

{{diagram card | **The spell card.** Fill in every line. The two most often left blank are the two that matter most.}}

{{diagram card_apprentice | **The Apprentice's own card.** The last two lines were written in later, in a different ink.}}

**The seven quests, one a day.**

| Day | Pair | Quest |
|---|---|---|
| Sunday | Chastity over Lust | Write the card for one reach you did not decide to make. |
| Monday | Temperance over Gluttony | Ask *done yet?* before every second helping. |
| Tuesday | Charity over Greed | Give away one thing KEEPER wanted to keep. |
| Wednesday | Diligence over Sloth | Two minutes on the thing you are waiting to be ready for. |
| Thursday | Forgiveness over Wrath | Let go of one old lock for one minute. |
| Friday | Kindness over Envy | One kindness for each comparison caught. |
| Saturday | Humility over Pride | Say *I was wrong about this* once. |

# Glossary {#glossary .unnumbered}

::: gloss
**Backoff.** Stepping away from a contested resource and trying again after a short, partly random delay.

**Daemon.** In computing, a helper process that runs in the background without anyone watching. From the Greek
*daimon*, an attendant spirit; said DAY-mon.

**Deadlock.** A standstill in which each of several workers holds something another needs and waits for what another
holds.

**Done when.** The stop condition of a routine: the sign, visible from outside, that its work is finished.

**Integration.** In Jung's sense, taking a disowned part back into conscious life, keeping its gift and ending its
runaway.

**Livelock.** A state in which workers keep changing what they do in response to each other without any of them making
progress.

**Mutual exclusion.** A rule that lets only one worker at a time into a section where a shared thing is checked and
changed.

**Orphan.** A process whose parent has ended while it is still running; the system's first process adopts it.

**Part.** In Internal Family Systems therapy, one of the many sub-personalities of a mind, each with a role, none of
them bad.

**Race condition.** A fault in which the result depends on the timing of workers acting on the same thing at the same
moment.

**Semaphore.** A counter that limits how many workers may use a resource at once.

**Shadow.** In Jung, the part of the personality the conscious self does not acknowledge as its own.

**Starvation.** A fault in which one worker is always passed over and never gets its turn.

**Supervisor.** A process that watches others and restarts any that stop.

**Virtue.** A strength of character that can be practised; in this book, the word that sets the order when a virtue and
its shadow conflict.
:::

# References {#references .unnumbered}

::: refs
Armstrong, J. (2003). *Making reliable distributed systems in the presence of software errors* [Doctoral dissertation,
Royal Institute of Technology, Stockholm].

Bargh, J. A., & Chartrand, T. L. (1999). The unbearable automaticity of being. *American Psychologist, 54*(7),
462-479.

Bishop, S. R., Lau, M., Shapiro, S., Carlson, L., Anderson, N. D., Carmody, J., Segal, Z. V., Abbey, S., Speca, M.,
Velting, D., & Devins, G. (2004). Mindfulness: A proposed operational definition. *Clinical Psychology: Science and
Practice, 11*(3), 230-241.

Bloomfield, M. W. (1952). *The seven deadly sins: An introduction to the history of a religious concept, with special
reference to medieval English literature.* Michigan State College Press.

Coffman, E. G., Elphick, M. J., & Shoshani, A. (1971). System deadlocks. *ACM Computing Surveys, 3*(2), 67-78.

Dijkstra, E. W. (1965). Solution of a problem in concurrent programming control. *Communications of the ACM, 8*(9),
569.

Dijkstra, E. W. (1971). Hierarchical ordering of sequential processes. *Acta Informatica, 1*(2), 115-138.

Dukas, P. (1897). *L'apprenti sorcier* [Scherzo for orchestra]. Durand.

Evagrius of Pontus. (2003). *Evagrius of Pontus: The Greek ascetic corpus* (R. E. Sinkewicz, Trans.). Oxford
University Press.

Goethe, J. W. von. (1798). Der Zauberlehrling. In F. Schiller (Ed.), *Musen-Almanach für das Jahr 1798.* Cotta.

Gollwitzer, P. M. (1999). Implementation intentions: Strong effects of simple plans. *American Psychologist, 54*(7),
493-503.

Hayes, S. C., Strosahl, K. D., & Wilson, K. G. (1999). *Acceptance and commitment therapy: An experiential approach to
behavior change.* Guilford Press.

Jung, C. G. (1959a). *Aion: Researches into the phenomenology of the self* (R. F. C. Hull, Trans.; Collected Works,
Vol. 9, Part 2). Princeton University Press. (Original work published 1951)

Jung, C. G. (1967). The philosophical tree. In *Alchemical studies* (R. F. C. Hull, Trans.; Collected Works, Vol. 13).
Princeton University Press. (Original work published 1945)

Jung, C. G. (1969). Psychology and religion. In *Psychology and religion: West and East* (R. F. C. Hull, Trans.;
Collected Works, Vol. 11, 2nd ed.). Princeton University Press. (Original work published 1938)

Krakovna, V., Uesato, J., Mikulik, V., Rahtz, M., Everitt, T., Kumar, R., Kenton, Z., Leike, J., & Legg, S. (2020,
April 21). *Specification gaming: The flip side of AI ingenuity.* DeepMind.

Lamport, L. (1974). A new solution of Dijkstra's concurrent programming problem. *Communications of the ACM, 17*(8),
453-455.

Lieberman, M. D., Eisenberger, N. I., Crockett, M. J., Tom, S. M., Pfeifer, J. H., & Way, B. M. (2007). Putting
feelings into words: Affect labeling disrupts amygdala activity in response to affective stimuli. *Psychological
Science, 18*(5), 421-428.

Lucian. (1921). The lover of lies, or the doubter. In *Lucian* (A. M. Harmon, Trans.; Vol. 3, Loeb Classical Library).
Harvard University Press. (Original work written c. 150)

Neff, K. D. (2003). Self-compassion: An alternative conceptualization of a healthy attitude toward oneself. *Self and
Identity, 2*(2), 85-101.

Peterson, C., & Seligman, M. E. P. (2004). *Character strengths and virtues: A handbook and classification.* Oxford
University Press.

Prudentius. (1949). Psychomachia. In *Prudentius* (H. J. Thomson, Trans.; Vol. 1, Loeb Classical Library). Harvard
University Press. (Original work written c. 405)

Russell, S. (2019). *Human compatible: Artificial intelligence and the problem of control.* Viking.

Schwartz, R. C., & Sweezy, M. (2020). *Internal family systems therapy* (2nd ed.). Guilford Press.

Turing, A. M. (1936). On computable numbers, with an application to the Entscheidungsproblem. *Proceedings of the
London Mathematical Society, s2-42*(1), 230-265.

Wegner, D. M. (1994). Ironic processes of mental control. *Psychological Review, 101*(1), 34-52.

Wegner, D. M., Schneider, D. J., Carter, S. R., & White, T. L. (1987). Paradoxical effects of thought suppression.
*Journal of Personality and Social Psychology, 53*(1), 5-13.

Wiener, N. (1960). Some moral and technical consequences of automation. *Science, 131*(3410), 1355-1358.

Wood, W., & Rünger, D. (2016). Psychology of habit. *Annual Review of Psychology, 67*, 289-314.
:::

# Colophon {#colophon .unnumbered}

::: colophon
This book was set in Baskerville and Gill Sans and printed by `tools/manual.py --book shadow`. Its plates were drawn from the game's own daemons, each one's picture used as the reference; its diagrams in the hand of the TEXTBOOK.

No brooms were harmed in the making of this book. Two were split, and both are fine.
:::

{{ornament gauge_7 gauge-end}}
