# Sprite prompts — starters, Crystal, and the box

Generation prompts for the step-9 art pass, with the specs that actually
constrain them. Companion to `vision.md` 8.2 (starter trio), 4.1/4.3 (the
Clears) and 1.3 (what a box is).

**Workflow, proven.** Gemini generates large and clean; `tools/gbimg.py`
quantises and downsamples to the Game Boy target. This is how the DAEMONS
title logo was made and it worked first time. Do **not** ask Gemini for
pixel art at the final size — ask for a large flat-shaded image and let the
tool do the reduction.

---

## What can be generated, and what cannot

| Asset | Target | Generate? |
|---|---|---|
| Starter front sprites | 40×40 | **Yes** — 1024×1024 source |
| Crystal Clear battle portrait | 56×56 | **Yes** — 1024×1024 source |
| Player intro pic (holding a box) | 56×56 | **Yes** — 1024×1024 source |
| Title screen player | 40×56 | **Yes** — 1024×1434 source |
| Starter back sprites | 32×32 | Yes, but derive from the front instead |
| Overworld sprites (Crystal, player) | 16×16 per frame | **No — hand-pixel or code** |
| The box, overworld | 16×16 | **No — generate procedurally** |
| The box, battle frames | 8×8 × 4 | **No — generate procedurally** |

**Why the small ones are excluded.** At 16×16 a character has roughly three
pixels of head. Downsampling any generated image to that size produces mush,
and no prompt fixes it. The border episode is the precedent: generation gives
illustrations, and the Game Boy wants geometry. A 16×16 box with a status
light is *exactly* the kind of thing `genborder.py`-style code does perfectly
and generation does badly.

---

## The shared preamble

Put this at the top of every image prompt:

> Original creature/character design for a monochrome Game Boy game. **Flat
> shading in exactly four values: white, light grey, mid grey, near-black.**
> No gradients, no anti-aliasing, no texture, no colour. Bold black outline
> around every form. Pure white background, no shadow, no ground plane, no
> frame or border. The subject fills the canvas with a small even margin.
> Simple readable silhouette — it must survive being reduced to a 40-pixel
> image. Not pixel art; a clean flat vector-style illustration.

**Why four values.** The hardware has four, and 8.6 makes that the design
rather than a limitation. A generated image with soft shading quantises to
mud; one with four flat tones quantises to exactly itself.

---

## 1–3. The starters

8.2 fixes these as the three learning paradigms. **The designs below are
proposals** — the names are already flagged as placeholders (10, open items),
and nothing about the visual reading is settled.

The trio should be legible as *one* idea seen three ways: each is a small
process that learns, differing in how.

### Labl — Supervised (CONTENT), the Charmander slot

> A small neat quadruped creature, tidy and symmetrical, with a rectangular
> paper tag tied to it by a short cord — the tag is blank. Its body is made of
> clean straight-edged segments that fit together exactly, like something
> assembled to specification. Alert, upright posture, facing the viewer. It
> looks certain of itself.

*Reading:* it learns from labels, and it has one. **Strong early and rigid
late** should be visible in the geometry — everything squares up. Blank tag,
not a written one: 8.2's whole point is the label is imposed from outside.

### Clustr — Unsupervised (VECTOR), the Squirtle slot

> A small creature that has not finished resolving into one body: a dark
> compact core with five or six smaller rounded shapes orbiting close around
> it, held in place but not attached. The outline of the whole reads as a
> single creature at a glance and comes apart when looked at directly. Two
> simple eyes on the core. Soft, loose, slightly asymmetrical.

*Reading:* it finds structure without being told what to look for, so it
begins as several things that have not agreed yet. **Confusing early,
excellent late.**

### Nudgit — Reinforcement (GROWTH), the Bulbasaur slot

> A small creature leaning eagerly forward and slightly off-balance, reaching
> toward something just out of frame. A short thick tail curls up behind it in
> a closed loop that comes back to touch its own back. One ear up, one ear
> down. Its posture is all anticipation.

*Reading:* it learns by reward, so it is always mid-reach. The tail is a
literal feedback loop touching its own body. **Inconsistent, highest ceiling**
reads as the off-balance stance.

---

## 4. Crystal Clear — battle portrait, 56×56

4.1 already fixes her: *golden-amber fox, drawn from the SHC / iASHC
universe.* The sprite note says amber sits cleanly in the two mid greys.

> An anthropomorphic fox scientist, female, standing three-quarters to the
> viewer. Middle-aged and composed, not warm. A long open lab coat over plain
> clothes. Pointed fox ears, a distinct muzzle, and a full brush tail visible
> behind her. Her fur reads as **mid grey**, the coat as **white**, her
> outline and the darkest fur as **near-black**. She holds nothing and is not
> gesturing — her hands are at her sides or one is in a pocket. Her expression
> is measured and faintly tired. She is not presenting; she is being looked at.

**Why she holds nothing.** 4.1: *"She lets the daemon choose you — she would
never assign one."* A figure holding out a box would contradict the one beat
that defines her.

**The three foxes differ by value, not hue.** 4.3 wants family resemblance at
sprite level with zero text, and the game is greyscale — so **Crystal light-to-mid,
Ty dark, Al between**, and the same ear and muzzle geometry on all three. Ask
for the shade explicitly in each prompt; do not rely on "amber", "russet" and
"chestnut" surviving the conversion, because they will not.

---

## 5. The player — intro pic, 56×56

Vanilla's player holds a Poké Ball. Ours holds a box.

> A young trainer standing three-quarters to the viewer, cap and short jacket,
> one arm raised holding a **small hard-edged electronic unit** at chest
> height — roughly a cube, slightly wider than tall, with a narrow horizontal
> vent line across the front, a single small round indicator light in one
> corner, and a port on the side. It is a machine, not a container: no seam
> around the middle, no button, nothing that looks like it opens. Confident
> stance. Four flat values, bold outline, white background.

**This is the whole ball→box redesign in one object**, so it is worth getting
right here first and deriving the small versions from it. 1.3 is unambiguous:
*"A box is a machine… you are offering the daemon a host."* It should read as
something you would **ssh into** — a little server, not a crate and not a
cube. The failure mode to avoid is a cardboard box or a dice-like cube; both
say *container*, which is the reading 1.3 replaced.

## 6. Title screen player, 40×56

Same character and same box, framed for the title: full body, standing, box
held at the side rather than raised. Slightly taller-than-wide framing —
generate at **1024×1434**.

---

## The box, procedurally

`gfx/sprites/poke_ball.png` (16×16) and `gfx/battle/balls.png` (32×8, four
8×8 frames) are too small to generate and should be built in code, the way
the SGB borders were. The brief is fixed by the prompt above: a hard-edged
unit with a vent line and one indicator light.

The four battle frames are the throw animation, so they want to read as the
*same object rotating and opening* — which is geometry, not illustration.

**And the ladder is already named.** USERBOX → … → ROOTBOX (1.3, 1.4). The
tiers should differ the way Poké/Great/Ultra/Master do: same silhouette, more
indicator lights or a denser vent as privilege rises. That is a parameter in a
generator, not four separate drawings.

---

## After the images come back

```sh
python3 tools/gbimg.py            # helpers: read_png, resample, quantise, write_png
```

Each asset is: read → resample to target → quantise to 4 levels → write 2bpp
greyscale PNG. **Remember `rgbgfx` inverts**: PNG level 3 becomes colour index
0, so in the source PNG *higher value is lighter on screen*. `quantise()`
already produces that convention.

Front sprites are compressed into `.pic` at build time, so keep interiors flat
— large single-value regions compress well and busy dithering does not.
