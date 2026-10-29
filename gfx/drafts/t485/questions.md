# T-485 -- questions for the user (DRAFT sheet, 2026-10-29)

**The plot, as drafted.** The hat stands on QUICKSILVER's south sand at **(9..11, 11..13)**: the body 3x2 at
(9..11, 12..13), solid; the crown 2x1 at (9..10, 11), walk-behind like every vanilla roof's top row (collision 0, art
on the top layer); the door **(10,13)**, entered from (10,14), a non-animated door block as the MANSION's (8,3), so
gbadoors has nothing to redraw. Cell (11,11) is left empty: the old man stands there (LOOK_AROUND, never moves) and the
crown leans away from him. Nothing that exists moves.

*Why it is safe.* A land-only walk (stricter than check_reach's floor walk: elevation 3, open collision, round the
people who never move) from the POKeMON CENTER door reaches 149 cells before and 143 after -- exactly the six the hat
takes, nothing else lost -- and every warp's doorstep, all four signs, all four people, the north exit to ROUTE 21 and
the east shore by ROUTE 20 are reached before and after. SCORN's door (8,9) and its board (9..10, 9) are still reached
by column 8 and the crown row. BILL's scenes and the SEAGALLOP's run east of x 14. The cells are 11+ in from the top
edge and 12+ from the right, outside the seven-cell seam (trap 14). Every other spot on the island fails: the beach
under the pocket cuts SCORN's door off (only the old man's square would join it), and the east column is the island's
only land link north to south. **Budget:** 28 unique tiles of the 30 free (346..375, never 376..383), 8 new blocks (the door one of them) of
192/384, palette row 12 (unused: no block in either tileset draws it), 15 colours.

**The room** is LAYOUT_HOUSE1's 11x9 plan (its door mat and the warp at (4,7) kept): clocks along the back wall, the
table on (2..8, 4..5), chair backs along row 3 and seats along row 6 (solid), the foot chair (1,4), his tall chair at
(9,4) with him standing at it facing west; talked to from (9,5). New blocks go in generic_building_1's unused rows 9..10.

---

**Q1. The hat's size.** It is drawn 3 cells wide and 3 tall (48x48), smaller than SCORN or the CENTER beside it,
because the only open ground is three rows deep.
- **A. Keep it 3x3 at (9..11, 11..13)** -- a hat, not a house dressed as one; it reads as odd and small, which suits him. *(recommended)*
- B. Make it 4 tall by drawing the crown onto (9..10, 10) too, over the sand in front of SCORN's board (walk-behind; the board stays readable from (9,10) and (10,10), but the player vanishes behind the crown there).
- C. Move it to the wide south beach (15..17, 12..13), 3x2, a squat hat with no crown room.

**Q2. When is "3:30 AM"?**
- **A. 3:30 to 3:59 by the clock: his 3:30 line in that half-hour, the glitch once a save.** *(recommended: a player can find it without a stopwatch)*
- B. The minute 3:30 to 3:31 only.
- C. 3:00 to 3:59, the whole witching hour.

**Q3. With THE HERMETIC LAYER held, what does a visit say?**
- **A. The visit's riddle, then the next book riddle (B1 -> B3) in turn.** *(recommended: the book adds, it does not replace)*
- B. Only the book riddles, in turn, once the book is held.
- C. One book riddle once each, then back to the ordinary four.

**Q4. His colours.**
- **A. His own palette: QUICKSILVER's people's with the light blue and blue turned to the house's purple band.** *(recommended: he appears only in his house, so a tag of his own shares the special slot with no one -- T-365's repaint cannot happen there)*
- B. QUICKSILVER's people's palette as it is (a blue band), so he could stand outside one day with the gulls.
