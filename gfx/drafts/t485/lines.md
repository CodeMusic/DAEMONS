# T-485 -- OSRIC HATTER's lines (DRAFT, every word)

*Drafted 2026-10-29 for the user's sheet. Measured with `tools/fontwidth.py` (the message box's own glyph widths,
sFontNormalLatinGlyphWidths, apostrophe 3px): every line is at most 208px. A blank line between pairs is a `\p`
(a new box); the two lines of a pair are joined by `\n`. Every character is in charmap.txt.*

**Voice.** Courteous and odd, never menacing. He greets the player, then turns to the empty chairs and asks them;
he never gives an answer straight. Each riddle is turned from a saying of THE HERMETIC LAYER: (a) the Tablet of the
Hands (the fingertip and the palm), the Folds (one sheet, a crane), the Tablet of Gravity IX ("the whole earth,
asking you to stay"), the crease; (b) Hands VI, Gravity X (the apple and the earth), Hands VII ("from which fold am I
looking?"). The house is outside the book, so craft rule 1 holds: nothing says the thesis, and none of the four
private things is near it. No line names madness (craft rule 3): the book's warning does that, not him.

**When.** (a) anyone, one riddle per visit in turn, A1 -> A4 then round again (a var counts the visits, set when the
talk ends); (b) with THE HERMETIC LAYER held (`FLAG_GOT_HERMETIC_LAYER`), the visit's riddle is followed by B1 -> B3
in turn (or replaced by them -- questions.md Q3); (c) 3:30 AM by the clock, in his house: C instead of everything,
with `Glitch_Start` between its second and third boxes, once a save (T-486; window in questions.md Q2).

## (a) Anyone, one per visit in turn

### A1 the hands

```
Good evening. Sit anywhere but here;             203px
this one is taken. It is mine.                   160px

(to the chairs) A riddle, friends.               184px
It has five fingers and no palm                  172px

of its own, and it is sure it chose              190px
to reach. What is it?                            116px

...Nobody? Nor did I, for years.                 180px
More tea?                                         52px
```

### A2 the fold

```
Ah, you came back. The chairs said               194px
you would. They are seldom wrong.                190px

(to the chairs) What is folded into              192px
a crane, and a boat, and a hat,                  177px

and never stops being what it was?               190px
Don't tell me. I like not knowing.               183px
```

### A3 gravity

```
Half past three. It is always half               189px
past three in here. Tea stays hot.               190px

(to the chairs) What holds you with              196px
no hands at all, and asks you,                   168px

every moment, to stay?                           125px
The chairs know. They sit on it.                 176px
```

### A4 the crease

```
(to the chairs) Why is a clock                   167px
like a crease?                                    78px

...Because both keep the time                    164px
from coming apart. Or because                    164px

neither one ever moves. I change                 182px
the answer every Tuesday.                        143px
```

## (b) With THE HERMETIC LAYER held

### B1 book: the hands

```
Oh. You are carrying my book.                    165px
Mind the green words; they are loud.             203px

(to the chairs) The finger moves,                183px
and the hand moves. Neither lies.                184px

So tell me, friends:                             109px
which of us poured this cup?                     159px
```

### B2 book: the apple

```
(to the chairs) You have all read                187px
the half-saying. Then answer:                    161px

the apple falls to the earth.                    163px
What falls, very slightly, to it?                180px

...They never get it.                            116px
They are far too heavy.                          133px
```

### B3 book: which fold

```
(to the chairs) Do not ask which                 178px
is true. Ask from where you sit.                 176px

Chair seven taught me that.                      152px
Chair seven has never said a word.               191px

Thank you for reading it to the end.             201px
Most people stop at the warning.                 179px
```

## (c) At 3:30 AM, in his house (T-486)

### C 3:30 AM (then Glitch_Start)

```
Oh! Half past three, and for once                187px
every clock in the house is right.               188px

Hold your cup with both hands.                   171px
The fold is thin tonight.                        135px

[here the script calls Glitch_Start: 12 frames, never black; not printed]

There. Nothing broke.                            117px
It only showed you where it bends.               193px
```

*Answers the player may reach, never printed: A1 a glove (a hatter would say so) -- or a small hand, which is the riddle under it; A2 a sheet of paper; A3 the floor -- the
whole earth; A4 has none, which is the joke. B1 both of them; B2 the earth; B3 is not a riddle but his thanks.*
