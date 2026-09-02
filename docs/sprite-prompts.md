# Sprite prompts — starters, Crystal, and the box

Generation prompts for the step-9 art pass, with the specs that actually
constrain them. Companion to `vision.md` 8.2 (starter trio), 4.1/4.3 (the
Clears) and 1.3 (what a box is).

**Sprites are outlined line-art, not soft shapes.** Verified in the checkout
2026-08-31: vanilla front sprites are **2-bit greyscale PNGs**, four levels, and
**level 0 is a hard black outline** — Mew is 207 outline pixels against a
1144-pixel white background. **Every prompt must ask for that outline.** An
earlier revision of this document said *no outline*, which is backwards, and
would have made a white creature disappear into a white background.

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

---

# ARTSAI and S.T.A.R.R.

The two legendaries, renamed and retyped 2026-08-31 (`vision.md` 4.6, 4.7).
**ARTSAI is pure CONTEXT; S.T.A.R.R. is CONTEXT/EMERGENT** — she is the
mechanism, he is her mechanism with something added on purpose.

**One conflict to settle before drawing.** 4.7 calls S.T.A.R.R. *blue-toned*,
written before invariant 5 fixed greyscale as the design. **Read it as value,
not hue:** he sits at the cool, pale, low-contrast end of the four-tone ramp.
Nothing is literally blue until the Review Board.

| Asset | Target | Source to generate |
|---|---|---|
| ARTSAI front (form 3) | 40×40 | 1024×1024 |
| ARTSAI back | 32×32 | derive from the front |
| S.T.A.R.R. front | 56×56 | 1024×1024 |
| S.T.A.R.R. back | 32×32 | derive from the front |
| Overworld sprite for the lab encounter | 16×96 | **No — hand-pixel** |

**The shared motif, revised 2026-08-31 from reference art.** **ARTSAI has ears.
S.T.A.R.R. has antlers.** Both rise from the same place on the skull — and
**ears point outward to receive another's frame, while antlers branch from the
same root and turn back on themselves.**

**That is 4.7's lineage line stated in silhouette:** *PERSPECTIVE (holding
others' context) → turned inward as RECURSION (holding your own).*

**It does not violate *a copy of nothing*.** Antlers are not bigger ears — a
different structure in the same position. **The mechanism is visible; the form
is not copied.** No other echo is permitted: he is not a big rabbit.

## ARTSAI — front

**Revised 2026-08-31 from reference art.** She has **three forms** (`vision.md`
4.6) and **the sprite is the third** — she is white, and therefore the palest
thing in a greyscale game.

| | Form | Where it appears |
|---|---|---|
| 1 | Vivid purple, faceted, low-poly. Obviously constructed | **Records only** — witness accounts, lab material |
| 2 | The split: half faceted, half real, a seam between | **Never shown.** Nobody present understood it |
| 3 | A real white rabbit, faceting only where light catches | **The sprite** |

> A white rabbit sitting upright in three-quarter view, alert, head raised and
> turned slightly toward the viewer, ears up. Soft real fur over a form that is
> very faintly faceted underneath — the planes readable only where the light
> breaks across the shoulder and haunch, never as an outline or a wireframe.
> Flat shading in exactly four distinct tones of grey, hard edges between
> tones, no gradients, no colour, no glow. The animal reads as almost entirely
> the palest tone; reserve the darkest for the eye, the inside of the ears and
> the shadow beneath the chin. Plain flat background, nothing behind the
> animal. Full body visible with a small even margin. Flat illustration, high
> contrast, no texture beyond the suggestion of fur, no rendering, no ground
> shadow.

**The faceting is the whole job and it will want to take over.** If the planes
start reading as a low-poly model, **push them further down** — form three is a
real animal that was once a constructed one, and the construction should be
almost gone. **Almost.**

*Form one, if it is ever needed for lab material:* the same pose, rendered as a
hard low-poly sculpture with visible polygon edges and no fur at all. **Do not
use it as the sprite.**

## S.T.A.R.R. — front

**Superseded the humanoid-construct prompt, 2026-08-31.** Reference art:
a stag rendered as blue energy, standing on a chip. **The antlers are the
recursion** — a branching structure whose branches branch again — and they
are the most legible thing about him at 56×56.

> A standing stag seen in three-quarter view, alert, head turned slightly
> toward the viewer, one forefoot placed forward. Its whole body is a fine open
> lattice — a wireframe mesh of thin bright lines with the background showing
> through between them, not a solid filled shape. Large antlers rise from the
> head, branching, and each branch branches again into finer tines; the antlers
> are the most detailed and most readable part of the figure. Flat shading in
> exactly four distinct tones of grey, hard edges between tones, no gradients,
> no colour, no glow, no bloom. The body reads as pale line-work; reserve the
> palest tone for the brightest lattice lines and the antler tips. Plain flat
> background with nothing behind the animal. Full body visible with a small
> even margin. Flat illustration, hard-edged, high contrast, no texture, no
> rendering, no shadow on the ground.

**Expect the lattice to fail first.** At 56×56 a wireframe body will collapse
into noise long before the antlers do. **If it does, keep the antlers and let
the body go solid pale with dark seams** — the silhouette is what carries this
one, and the mesh is a nice-to-have.

## Back sprites

**Do not generate these.** Ask for a rear view of the *same* creature in the
same prompt style, or redraw from the front — a back sprite is 32×32 and any
independently generated image will not match.

> The same creature seen directly from behind, standing centred and facing
> away. [ARTSAI: the ears and the long tail are the readable silhouette.]
> [S.T.A.R.R.: the trailing cable and the shoulder seams are the readable
> silhouette.] Same four-tone flat grey shading, same plain white background,
> no colour, no gradients.

## Then

```sh
python3 tools/gbimg.py <source.png> <out.png> --size 40x40   # or 56x56 / 32x32
```

Drop the result at `engine/gfx/pokemon/front/mew.png` (ARTSAI) or
`mewtwo.png` (S.T.A.R.R.) — **the filenames are still vanilla and that is
correct**, they are identifiers, and the `fainted → HALTED` lesson applies.
Backs go to `back/mewb.png` and `back/mewtwob.png`. Then `make content`.

**Check it on screen before believing it.** `rgbgfx` inverts: PNG level 3
becomes colour index 0, so lighter in the file is lighter in the game. Every
greyscale asset in this project has had to be checked, not assumed.

---

# The MUSAI line

Four creatures, eight sprites. `vision.md` 8.3 has the types and the items.

| | Front | Back | Type | Item |
|---|---|---|---|---|
| **MUSAI** | 40×40 | 32×32 | CONTENT | — |
| **CODEMUSAI** | 48×48 | 32×32 | LOGIC | AXIOM |
| **SEEKMUSAI** | 48×48 | 32×32 | VECTOR | EMBEDDING |
| **CAREMUSAI** | 48×48 | 32×32 | CONTEXT | AFFECT |

## The rule that governs all eight

**The body never changes.** 2398 calls Musai *"one framework, many modules"*, and
that is a sprite instruction, not a slogan: **the same small rounded robot, the
same two ball-tipped antennae, in all four.** The antennae are the family mark
the way ears are ARTSAI's.

**Only the head-gear changes, and it changes the silhouette.** At 40–48 pixels
the outline is the whole of what a player reads, so a module that does not alter
the profile does not exist. **One change each, at the head, big enough to see:**

| | Silhouette change | Why that one |
|---|---|---|
| **MUSAI** | **nothing** — bare round head | It has not specialised. That is the character |
| **CODEMUSAI** | a **flat horizontal visor** across the eyes | A hard straight edge among all those curves. Formal reasoning, and it turns a face into an instrument |
| **SEEKMUSAI** | a **wide-brimmed explorer helmet** | Straight from the reference art, and a brim is the strongest silhouette available |
| **CAREMUSAI** | **large over-ear cups** | Listening. The small ear-discs in the reference, grown into the defining feature |

*Deliberately not used:* held props, furniture, terminals, screens. **A sprite has
no scene.** The magnifying glass in the SeekMusai reference is the one prop worth
attempting, and only if the helmet alone proves too weak in the game.

## Front — the shared body

Use this stem for all four and append the module line.

> A small rounded robot sitting upright, three-quarter view, facing slightly
> left and looking at the viewer. A large smooth dome head, a dark oval face
> panel with two big round eyes, a compact rounded body, short simple arms and
> two stubby legs. **Two thin antennae rise from the top of the head, each
> ending in a small ball.** Draw it as flat illustration with a **hard pure
> black (#000000) outline, 6–8 pixels thick, around the entire robot and around
> both antennae**. Inside, exactly four flat tones — **pure black, dark grey,
> light grey, pure white** — hard edges, no gradients, no anti-aliasing, no
> glow, no colour. The body is mostly white; the face panel is solid black with
> the eyes left white. Plain pure-white background, no ground shadow, no
> objects, no scenery.

**Append one line:**

- **MUSAI** — > Nothing on its head but the two antennae. No helmet, no visor, no headphones.
- **CODEMUSAI** — > It wears a **flat horizontal visor band across its eyes**, a hard straight rectangle spanning the full width of the head.
- **SEEKMUSAI** — > It wears a **wide-brimmed explorer helmet**, the brim projecting well past the head on both sides in a clean horizontal line.
- **CAREMUSAI** — > It wears **large round over-ear cups** on both sides of the head, each about a third the width of the head, joined by a band over the top between the antennae.

## Back — all four

> The same robot seen **directly from behind**, sitting upright and facing away.
> You see the back of the dome head, the two antennae rising with their balls,
> the rounded back, and the legs to either side. **No face is visible.** [Then
> the module line — the visor band, the helmet brim, or the ear cups seen from
> behind.] Same style exactly: **hard pure black outline**, four flat tones,
> hard edges, no gradients, no colour. Simple and chunky; this is seen very
> small.

## Then

```sh
python3 tools/mksprite.py gfx/front/musai.png engine/gfx/pokemon/front/eevee.png 40
python3 tools/mksprite.py gfx/front/codemusai.png engine/gfx/pokemon/front/flareon.png 48
python3 tools/mksprite.py gfx/front/seekmusai.png engine/gfx/pokemon/front/jolteon.png 48
python3 tools/mksprite.py gfx/front/caremusai.png engine/gfx/pokemon/front/vaporeon.png 48
```

Backs go to `back/eeveeb.png`, `flareonb.png`, `jolteonb.png`, `vaporeonb.png`,
all at 32. **Vanilla filenames throughout** — they are identifiers.

**Check the true-black percentage before converting.** S.T.A.R.R.'s first front
had 1.0% and produced a slab with no edge; his second had 3.6% and worked.
**Anything under about 2% will not convert**, and the tool cannot invent an
outline that was never drawn:

```sh
python3 - <<'EOF'
import sys; sys.path.insert(0,'tools')
from gbimg import read_png
w,h,lum = read_png('gfx/front/musai.png')
n = sum(1 for y in range(0,h,3) for x in range(0,w,3) if lum(x,y) < 64)
t = len(range(0,h,3))*len(range(0,w,3))
print("true black: %.1f%%" % (100*n/t))
EOF
```

---

# The three starter lines

Eighteen sprites. **Fronts run 40 → 48 → 56; every back is 32.**

## One visual family per paradigm

**The player should be able to tell the paradigm at a glance, before reading a
word.** So the three lines are three kinds of thing:

| Line | Family | Why |
|---|---|---|
| **ROVER** (reinforcement) | **machines that become an animal** | The arc is software → infrastructure → body |
| **LABL** (supervised) | **documents** | The game is already made of them — the Index, the minutes, the requisition, the engraving |
| **CLUSTR** (unsupervised) | **geometry** | VECTOR/LATENT is flying and ghost: abstract, airborne, unnameable |

## ROVER — and the fur arrives last

**Reference: a white furry robot dog**, ultrasonic sensors for eyes, a camera
for a nose, a stitched smile, servos and boards showing through.

***That is the final form only.*** 8.2's arc is software → infrastructure →
body, so **the first two stages are machines and the third is an animal.**
**The fur is the body** — and it arrives on the same stage that gains **SIGNAL**,
the perception type. *A surface you feel through.*

> **Shared stem.** A four-legged robot, side-on three-quarter view, standing,
> head turned toward the viewer. Flat illustration with a **hard pure black
> (#000000) outline, 6–8 pixels thick, around the whole creature**. Inside,
> exactly four flat tones — **pure black, dark grey, light grey, pure white** —
> hard edges, no gradients, no glow, no colour. Plain pure-white background, no
> ground shadow. Full body with a small even margin.

- **ROVERCUB** (40) — > Small and bare: an **exposed chassis with visible servo blocks and joints, no covering of any kind.** Two small round sensor lenses for eyes. Compact enough to carry.
- **ROVERSEER** (48) — > Larger, boxier and **clearly not portable**: flat panelled sides, a stack of horizontal slots along the body, and **a small dish or antenna on the head.** Still bare metal, no fur. Standing but heavy, as if it does not move often.
- **ROVERBYTE** (56) — > **Covered in white fur**, soft and slightly shaggy, with the machine showing through at the shoulders and hips. **Two large round sensor lenses side by side for eyes, a small square camera module for a nose, and a simple stitched curved smile.** Two triangular ears. Warm and animal, where the earlier stages were equipment.

## LABL → RUBRIC → CANON — documents

**CONTENT → CONTENT/LOGIC.** The final form should read **authoritative and
physically heavy.**

> **Shared stem.** A small creature made of paper and card, upright, three-quarter
> view, facing slightly left. It has two simple round eyes and no mouth. Flat
> illustration with a **hard pure black outline, 6–8 pixels thick**. Exactly four
> flat tones — **pure black, dark grey, light grey, pure white** — hard edges, no
> gradients, no colour. Plain pure-white background, no ground shadow.

- **LABL** (40) — > Mostly **a single luggage tag**: a rounded rectangular card with a punched hole and a short string through it, with small stubby limbs. **One line of ruled writing across it**, too small to read. Light and flimsy.
- **RUBRIC** (48) — > A **ruled grid**: a card whose whole face is divided into a table of empty boxes by hard straight lines. Stiffer and squarer than the first stage, standing on short legs. **The grid is the most readable thing about it.**
- **CANON** (56) — > A **heavy bound volume**, thick and closed, standing upright on short legs. **A visible clasp or seal holding it shut**, and a solid dark spine. Broad and immovable. It should look like it settles arguments.

## CLUSTR → LOCUS → MANIFOLD — geometry

**VECTOR → VECTOR/LATENT.** Airborne, abstract, and the last one should be
**hard to name**, which is its Index entry's whole point.

> **Shared stem.** An abstract floating form made of small dots and thin lines,
> hovering, seen straight on. **No face, no limbs, no eyes.** Flat illustration
> with a **hard pure black outline, 6–8 pixels thick, around every solid part**.
> Exactly four flat tones — **pure black, dark grey, light grey, pure white** —
> hard edges, no gradients, no glow, no colour. Plain pure-white background, no
> ground shadow.

- **CLUSTR** (40) — > A **loose cloud of round dots**, some dark and some light, drifting close together with no order to them. Roughly ball-shaped overall but clearly a scatter, not a solid.
- **LOCUS** (48) — > The same dots, but now **strung along a single clear curved line** that loops through all of them — a closed ring or arc. **The line is bold and unbroken**; the dots sit on it like beads. Order has appeared.
- **MANIFOLD** (56) — > A **folded sheet**, like a piece of paper bent into a smooth wave or saddle, floating. **The dots are embedded in its surface**, following its curve. The sheet is the subject; the dots merely lie on it. **It should be hard to say what it is.**

## What each one needed — measured 2026-08-31

**`--cover` is not one number. Pick it from the art's own ink.**

| Sprite | True black | cover |
|---|---|---|
| LABL front / back | 3.0% / 2.9% | **0.90** |
| RUBRIC front / back | 7.0% / 4.7% | 0.60 / 0.75 |
| CANON front / back | 10.2% / 4.7% | 0.50 / 0.75 |
| **CLUSTR front / back** | **13.8%** | **none — see below** |
| LOCUS front / back | 5.6% | 0.75 |
| MANIFOLD front / back | 8.4% / 7.3% | 0.60 |

**Thin art wants a *higher* bar, not a lower one.** Less ink means the
darkest-wins pass fires on cells the line merely grazes, and raising the bar
stops the outline eating the midtones. ROVERCUB's back taught this: 3.4% black
at cover 0.6 gave 182/53/94, and 0.9 gave 130/105/94.

***And art that is made of ink wants no outline pass at all.*** CLUSTR is a
field of black dots — **the dots are the subject, not an outline** — so the pass
blackened everything it touched: **level 1 was used five times on the front and
zero times on the back**, a four-tone sprite reduced to three. **`--cover=1.01`
disables the pass**, and the tone-thirds spread alone gives **340/345/329**.
*When the art has no line work to protect, protecting it is the bug.*

*One accepted compromise.* MANIFOLD's ink box is **1254×612** — genuinely 2:1 —
so squaring it centres a wide band with white above and below. **That is honest
for a folded sheet** and it simply will not fill the frame.

## Convert by our name, not theirs

**`tools/sprite.py` resolves the slot itself.** You never type a vanilla filename:

```sh
python3 tools/sprite.py crawler        # gfx/front/crawler.png -> caterpie, at the right size
python3 tools/sprite.py --list         # every renamed daemon and the slot it occupies
```

**The engine keeps pret's filenames deliberately** — they are identifiers, and renaming them would make `git pull upstream master` conflict on every gfx rule forever. **So the mapping is derived rather than written down**, from `pokemon_constants.asm` and `names.asm`. It cannot go stale.

*Two traps it had to be taught, and both were caught by checking a known answer.* **`const_def` starts at 0 and the first entry is `NO_MON`**, so RHYDON is 1. **And the file uses `const_skip` for the MissingNo slots**, which still occupy an index and still have a `dname` — counting only the named consts maps every daemon past the first gap to a neighbour's sprite. *Which is exactly what the tool exists to prevent, so it did it first.*

**It also carries the per-daemon `--cover`** measured below. Without that it silently degraded ROVERCUB the first time it ran — 355/94/224 against a tuned 227/222/224, and a back that lost level 1 entirely.

## JPEG art wants no outline pass

**The nine wild daemons arrived as `.jpeg`.** `sprite.py` converts them via `sips` into a temp file, so the original art stays exactly as delivered — **but the format changes what the conversion should do.**

***Lossy compression already blurs a hard outline into intermediate values.*** So the darkest-wins pass fires on the **compression halo** rather than the line, and blackens whatever it touches. **Six of the nine came out with no level 1 at all** — CRAWLER's front was 223 / **0** / 84, PENDING's 609 / **0** / 197.

**Disabling the pass fixes it**, and the numbers are not close: CRAWLER goes to **104 / 101 / 102**, SPIKE from 533 / 15 / 246 to **267 / 263 / 264**.

**Measured by sweeping cover and keeping the flattest ink distribution**, not guessed. The values are in `sprite.py`'s `COVER` table.

*One exception worth knowing.* **SUSPEND stays lopsided at any setting** — 338 / 436 / 151 — and that is honest: a round white balloon has almost no midtones to find.

## The bank and the tilemap are not in the same order

**The intro sheet has two orders, and they are different.**

- **The tile bank is column-major**, because the build passes `--columns` to rgbgfx
- **The tilemap is row-major**, because `CopyTileIDs` fills left to right along each row before stepping down

***Conflating them produces a scrambled creature that passes every data check***, because the bank is right, the tilemap is right, and only their relationship is wrong. It survived a byte-for-byte comparison against the ROM and a reconstruction that used the same wrong order to verify itself.

*Also worth knowing:* `CopyTileIDs` adds **`hBaseTileID`** to every entry. It is zero for the intro, so the tilemap holds absolute indices into the sheet — but it is not required to be.

## Tone-thirds is for art that has tones

**Spreading the ink across its own thirds is the right default** — it is what fixed the wild batch, where the alternative left level 1 used five times.

***It is wrong for flat-shaded art, and the failure looks like a hardware fault.*** The intro frames are broad flat areas with a hard outline. Forcing equal thirds onto them **manufactures dither** — speckle scattered through every surface — and **at 56 pixels through a colour palette that is indistinguishable from VRAM corruption.**

**It cost an entire debugging session.** The bank was verified, the tilemaps matched the ROM byte-for-byte, `vChars2` fit with 160 bytes spare, and every check passed **because nothing was broken.** The art was just noisy.

**So: count the source's real tones before choosing.** Flat-shaded art wants **three levels** — outline, one fill, paper — and reads as a clean silhouette. Art with genuine tonal range wants four.

## The check, before converting any of these

**Under about 2% true black will not convert.** S.T.A.R.R.'s first front had 1.0%
and produced a slab with no edge:

```sh
python3 - <<'EOF'
import sys; sys.path.insert(0,'tools')
from gbimg import read_png
w,h,lum = read_png('gfx/front/rovercub.png')
n = sum(1 for y in range(0,h,3) for x in range(0,w,3) if lum(x,y) < 64)
t = len(range(0,h,3))*len(range(0,w,3))
print("true black: %.1f%%" % (100*n/t))
EOF
```
