# T-452 SYMBOL's 28 forms -- questions (DRAFT art, not in the ROM)

**ANSWERED (the user, 2026-10-28): installed as drawn (1a 2a 3a 4a 5b); 6a followers for every letter at the player's size; 7a 'There are twenty-six' left alone. 8 still open.**

Sheet: `t452sym_sheet.png` (today's front | new front, back, icon, 1x and 2x; the shiny front).
Drafted 2026-10-28, seed 6800, dir y: each form image-to-image from a guide (the glyph in Arial Rounded Bold, thickened,
one big eye, two stubby feet) at 0.6 (6821) or 0.66 (6823), on the shared sprite server one job at a time. Every
form reads as its glyph. One palette for all 28 (CONTEXT's ramp, no accents), icons all in shared icon palette 1.
The **recommended** answer is first in each.

1. **The family look.** (a) **As drawn: the letter is the body, one big eye (today's one eye), two stubby feet** --
   (b) one more round for more charm: little arms and rounder, softer bodies drawn into the guide, at 0.66 -- (c) thinner
   strokes, nearer today's wire-thin Unown.
2. **Size.** The new forms stand about 40x45 against today's 24x40. (a) **As drawn** (the size of the other T-452
   daemons) -- (b) shrunk to about 75%: a symbol is a small thing.
3. **Backs.** (a) **The front mirrored, eye painted out -- from behind, the glyph reads reversed (R is Я, E is Ǝ)** --
   (b) not mirrored, eye out (the letter reads the right way round from behind) -- (c) backs turned by the model from
   each new front (56 more jobs; it usually draws a second front).
4. **The eye.** (a) **White and ink, no accent** (the 28 must share one palette; nothing for gbasprite's hue trap to
   rotate) -- (b) one shared iris colour for all 28, teal near hue 170 (outside CONTEXT's 40-degree trap round 312).
5. **G.** The draft drew G's eye as a big spiral filling its counter, so G's back keeps a pale crescent there.
   (a) **Hand-cut G's counter on the back (and front, outside the eye) so the ground shows through** -- (b) leave it.
6. **The follower.** A SYMBOL in the lead follows as its letter's party icon (GetIconSpecies), and the new icons are
   28px busts, so a lettered SYMBOL would walk larger than the player (T-464). (a) **Give the 27 letter species
   follower pictures too: gbafollower.py stops skipping SPECIES_UNOWN_* and makes each from its form's front** --
   (b) every letter follows as A's small picture.
7. **The INDEX entry** says "There are twenty-six"; there are 28 forms (26 letters, ! and ?). (a) **Leave it: the
   two marks are not letters, and the entry is the thing nobody has read** -- (b) "twenty-eight" (DRAFT word) --
   (c) a new line for the two marks (DRAFT, the user writes it).
8. **The companion.** It shows art from gfx/daemons/<name>_front.png, and SYMBOL's art stays in a subfolder (install
   plan, step 1), so the companion keeps no picture of it. (a) **companion_export.py reads gfx/daemons/symbol/a_front.png
   for SYMBOL** -- (b) leave SYMBOL without art in the companion.

Noticed, left as drawn: B's pupil is heart-shaped; I and ! are near twins (as today's); A's counter was a tiny
drawn 'A' and is cut as a real triangle by hand; seven counters (A B D O P Q R) were painted paper by the model and
are cut through.
