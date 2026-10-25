"""T-452 roll-out: what each daemon IS, in words the model can draw -- its props and its shape, read off today's art
(gfx/daemons/) and its INDEX category. batch.py reads this; a later batch adds its twenty here.

    NAME: dict(props=..., front=..., back=..., icon=..., neg=...)

props  -- one line for the sheets: what must survive, and the INDEX category it stands for
front  -- the front subject (the prop named early: a prop named first is a prop drawn)
back   -- the back subject, "seen from behind" (image-to-image from today's back does the turning)
icon   -- a head-and-shoulders bust for the 32px party icon, drawn on its own
neg    -- extra negative for this one
icon2  -- optional: a second icon wording, for one whose bust became a face (batch.py's icon2 stage, the whole shape
          as the icon rather than a head)
"""

S = {
 # ---- batch 1 (2026-10-24) ----
 "roverseer": dict(
  props="a big four-legged robot hound, boxy metal body, antenna on its back (PREDICTIVE)",
  front="a large robot dog, a heavy four-legged robot hound with a long boxy grey metal body made of riveted plates, "
        "four thick jointed metal legs, a robot dog head with a dark muzzle and pointed metal ears, a small antenna "
        "with a round light on its back",
  back="a large four-legged robot dog seen from behind, rear view, facing away from the viewer, a boxy grey metal "
       "back panel with bolts, four thick jointed metal legs, a small antenna with a round light on top",
  icon="head and shoulders of a heavy robot dog, a boxy metal dog head with a dark muzzle and pointed metal ears",
  neg="humanoid, bipedal, standing upright, arms, gun, wings"),
 "roverbyte": dict(
  props="a fluffy robot puppy with floppy ears and jointed leg plates (EMBODIED)",
  front="a fluffy robot puppy, a plush round dog with floppy grey ears and a big friendly face, a sturdy round body, "
        "metal joint plates on its four legs, a small round lens on its chest",
  back="a fluffy robot puppy seen from behind, rear view, facing away from the viewer, the back of its round head and "
       "floppy grey ears, a sturdy round back, metal joint plates on its four legs, a short tail",
  icon="head and shoulders of a fluffy robot puppy with floppy grey ears and a big friendly face",
  neg="humanoid, bipedal, standing upright, arms, gun"),
 "label": dict(
  props="a paper luggage tag with a string loop on its head (EXAMPLE)",
  front="a paper luggage tag creature, a small rounded tag-shaped body with a hole and a loop of string tied on top of "
        "its head, two small dot eyes, two stubby little arms, two small feet",
  back="a paper luggage tag creature seen from behind, rear view, facing away from the viewer, a plain rounded "
       "tag-shaped back, a loop of string tied on top of its head, two stubby arms, two small feet",
  icon="head of a paper luggage tag creature with a loop of string on top and two small dot eyes",
  neg="ghost, penguin, bird, cat"),
 "rubric": dict(
  props="a square score sheet: a grid of ruled rows and columns for a body (CRITERION)",
  front="a square box creature made of a paper score sheet, a flat square body printed with a grid of ruled rows and "
        "columns like a marking table, two big eyes in the top row of the grid, four short stubby legs",
  back="a square box creature seen from behind, rear view, facing away from the viewer, the plain back of a square "
       "paper score sheet with faint ruled lines, four short stubby legs",
  icon="the top of a square paper score sheet creature, ruled grid lines, two big eyes in the top row",
  neg="robot, television, computer, arms"),
 "canon": dict(
  props="a steel filing cabinet, its drawer open on stacked papers (SETTLED)",
  front="a heavy steel filing cabinet creature, a square dark metal box with one drawer pulled half open showing "
        "stacked white papers, a drawer handle, two small stern eyes on its front, four short stubby legs",
  back="a heavy steel filing cabinet creature seen from behind, rear view, facing away from the viewer, the plain "
       "dark metal back of a square cabinet, a small keyhole, four short stubby legs",
  icon="the top of a dark steel filing cabinet creature, two small stern eyes, a drawer edge with white papers",
  neg="robot, television, computer, arms, safe dial"),
 "cluster": dict(
  props="a ball of many grey spheres packed together, one bright one among them (GROUPING)",
  front="a round cluster creature, a ball made of many grey and white spheres of different sizes packed tightly "
        "together, dark gaps between them, one small coloured sphere among them, two small eyes on the biggest sphere",
  back="a round cluster of many grey and white spheres of different sizes packed tightly together seen from behind, "
       "rear view, dark gaps between them, no face",
  icon="a round cluster of grey and white spheres packed together, two small eyes on the biggest sphere",
  icon2="a round ball of many small grey and white spheres packed tightly together, dark gaps between them, one small bright sphere, two tiny dot eyes",
  neg="grapes, berries, bubbles in water, frog eggs"),
 "locus": dict(
  props="a thick bent loop, a curved ring of tube (CONDITION)",
  front="a curved loop creature, a thick bent ring of smooth rounded tube like a bean-shaped donut, white and grey "
        "bands around it, a small calm face on the front of the loop",
  back="a curved loop creature seen from behind, rear view, a thick bent ring of smooth rounded tube like a "
       "bean-shaped donut, white and grey bands around it, no face",
  icon="a thick bent ring of smooth rounded tube with a small calm face",
  icon2="a thick bent loop of smooth grey rounded tube shaped like a bean or a bent ring, two tiny dot eyes on it",
  neg="snake, worm, legs, arms, food, bagel"),
 "manifold": dict(
  props="a flat folded sheet, a manta shape with fin wings and a long tail (SURFACE)",
  front="a manta ray creature whose body is a flat folded sheet, a smooth curved wave-shaped surface, two wide fin "
        "wings, a long thin tail, small eyes at the front edge, gliding",
  back="a manta ray creature seen from behind, rear view, a flat folded sheet body, the smooth top of a wave-shaped "
       "surface, two wide fin wings, a long thin tail pointing at the viewer, no face",
  icon="the front of a flat manta ray creature, a folded sheet body with two fin wings and small eyes",
  neg="whale, shark, fish scales, bird, legs"),
 "crawler": dict(
  props="a caterpillar of round segments, light and dark, a round white head (COLLECTOR)",
  front="a little caterpillar made of a row of round ball segments, alternating dark grey and light grey, a round "
        "white head with two big eyes, tiny legs underneath, a thin trailing thread behind it",
  back="a little caterpillar made of round ball segments seen from behind, rear view, facing away from the viewer, "
       "the segments stacked going away, the back of its round head, a thin thread trailing toward the viewer",
  icon="the round white head of a little caterpillar with two big eyes and the first dark round segment",
  neg="snake, worm without legs, butterfly, wings"),
 "pending": dict(
  props="a cocoon wrapped in dark cloth, a pale sleeping face peeking out (QUEUED)",
  front="an egg-shaped cocoon wrapped in dark grey cloth, a pale round sleepy face peeking out at the top with closed "
        "eyes, no limbs, sitting still",
  back="an egg-shaped cocoon wrapped in dark grey cloth seen from behind, rear view, a smooth wrapped back, no face, "
       "no limbs",
  icon="a pale round sleepy face with closed eyes peeking out of a dark grey cloth cocoon",
  neg="legs, arms, chick, baby"),
 "indexer": dict(
  props="a moth with wide wings of file-card panels, feathery antennae (FILING)",
  front="a moth with wide spread wings patterned in grey and white rectangular panels like file cards, a dark fuzzy "
        "body, two feathery antennae, small red eyes",
  back="a moth seen from behind, rear view, facing away from the viewer, wide spread wings patterned in grey and white "
       "rectangular panels like file cards, the back of its dark fuzzy body",
  icon="head and shoulders of a moth with two feathery antennae, small red eyes, the tops of its card-panel wings",
  neg="butterfly with colourful wings, bird, bat"),
 "scraper": dict(
  props="a banded grub with a dark sharp stinger at its tail (UNLICENSED)",
  front="a long striped grub larva, a horizontal body of grey and white bands, a round head with small eyes at one end, "
        "a dark sharp stinger spike at the tail end",
  back="a striped grub larva seen from behind, rear view, the round back end of its banded grey and white body facing "
       "the viewer, a dark sharp stinger spike pointing out",
  icon="the round head of a striped grub larva with small eyes and the first grey and white bands",
  icon2="the front end of a striped grub larva, round banded grey and white segments, a small round head with two small eyes, a dark stinger tip behind",
  neg="snake, worm without bands, butterfly, wings"),
 "buffer": dict(
  props="a hard oval pod, a shell with a slit and two small red eyes (HELD)",
  front="a smooth oval cocoon pod, a pale grey hard shell like a beetle's back, a narrow slit near the top with two "
        "small red eyes looking out, no limbs",
  back="a smooth oval cocoon pod seen from behind, rear view, a pale grey hard shell with a seam down the middle like "
       "a beetle's back, no face, no limbs",
  icon="the top of a pale grey oval shell pod with a narrow slit and two small red eyes looking out",
  neg="egg, legs, arms, face, mouth"),
 "injector": dict(
  props="a wasp with clear wings and a long needle stinger like a syringe (UNCHECKED)",
  front="a wasp with a striped grey and white body, thin clear wings, long thin legs, two small eyes, and a long sharp "
        "needle stinger like a syringe at its tail",
  back="a wasp seen from behind, rear view, facing away from the viewer, thin clear wings spread, the striped back of "
       "its body, a long needle stinger like a syringe pointing down",
  icon="head and shoulders of a wasp with two small eyes and antennae, thin clear wings behind",
  neg="bee with fuzzy body, butterfly, bird"),
 "relay": dict(
  props="a pigeon carrying an envelope tucked under its wing (HANDOFF)",
  front="a white envelope letter tucked under the wing of a grey pigeon, a grey pigeon with a white chest and a small "
        "round head, standing on two pink feet, a short tail",
  back="a grey pigeon seen from behind, rear view, facing away from the viewer, the back of its round head, folded "
       "grey wings, a short fanned tail pointing at the viewer, a white envelope corner peeking out beside it",
  icon="head and shoulders of a grey pigeon with a white chest and a white envelope under its wing",
  icon2="a grey pigeon with a big white envelope letter tucked under its wing, the envelope large and clearly visible",
  neg="owl, parrot, penguin, flying"),
 "broadcast": dict(
  props="a big dove with wide spread wings, sending to all (TO ALL)",
  front="a large grey dove with its wide wings spread fully open, a white head, a grey body, talons, beak open as if "
        "calling out",
  back="a large grey dove seen from behind, rear view, facing away from the viewer, wide wings spread fully open, the "
       "back of its white head, its tail pointing at the viewer",
  icon="head and shoulders of a grey dove with a white head, beak open as if calling out, wing tips raised behind",
  neg="eagle, owl, parrot, penguin"),
 "nibble": dict(
  props="a small plump rat, pink ear and nose, long thin tail (UNIT)",
  front="a small plump grey rat on four short legs, a round body, a small round pink ear, a pink nose, whiskers, a "
        "long thin pink tail",
  back="a small plump grey rat seen from behind, rear view, facing away from the viewer, a round rump, two round ears, "
       "a row of small light stripes down its back, a long thin tail pointing at the viewer",
  icon="head and shoulders of a small grey rat with a round pink ear, a pink nose and whiskers",
  neg="mouse with big ears, hamster, cat"),
 "overflow": dict(
  props="a big rat whose lumpy body bulges past itself, dark head, long tail (EXCEEDED)",
  front="a big rat with an overstuffed lumpy body bulging out in too many rounded grey lumps, a dark head with a pink "
        "nose, short legs, a long thin tail",
  back="a big rat with an overstuffed lumpy body seen from behind, rear view, facing away from the viewer, rounded "
       "grey lumps bulging out of its back, two round ears, a long thin tail pointing at the viewer",
  icon="head and shoulders of a big rat with a dark head, a pink nose and a lumpy bulging grey body behind",
  neg="hedgehog spikes, porcupine, cat"),
 "ping": dict(
  props="a hummingbird with a very long needle beak (DEMAND)",
  front="a hummingbird with a very long thin needle beak, a small grey body, wings raised up high, a short tail, "
        "hovering",
  back="a hummingbird seen from behind, rear view, facing away from the viewer, the round back of its small grey body, "
       "both wings raised up high, a short tail",
  icon="head and shoulders of a hummingbird with a very long thin needle beak",
  neg="eagle, owl, parrot, penguin"),
 "flood": dict(
  props="a diving bird with swept-back wings, long sharp beak and a crest (DENIAL)",
  front="a long-beaked bird diving forward with its wings swept back, a long sharp beak, a crest of feathers on its "
        "head, a grey body, talons",
  back="a long-beaked bird seen from behind, rear view, facing away from the viewer, wings spread up and back, a crest "
       "of feathers on its head, talons below",
  icon="head and shoulders of a bird with a long sharp beak and a crest of feathers on its head",
  neg="owl, parrot, penguin, duck"),
}

# ---- batch 1 redone for charm (the user, 2026-10-25: "more charm, accept drift") ----
#  batch.py's charm stages read these. key  -- the ONE prop or shape that must survive, named first in the prompt;
#  front -- the chibi subject that follows it (everything else may drift); icon -- a chibi bust or whole shape.
CHARM = {
 "roverseer": dict(key="a boxy riveted metal robot body with a small antenna and a round light on its back",
  front="a cute chubby robot hound puppy on four stubby jointed metal legs, a big round robot dog head with pointed metal ears and a dark muzzle",
  icon="a cute robot dog head with pointed metal ears, a dark muzzle and a small antenna"),
 "roverbyte": dict(key="big floppy dog ears and metal joint plates on its legs",
  front="a cute fluffy robot puppy sitting, a big round head with a happy face, a small round lens on its chest, four stubby legs",
  icon="a cute fluffy puppy head with big floppy ears and a small metal plate on its forehead"),
 "label": dict(key="a loop of string tied through a hole on top of its head",
  front="a cute little paper luggage tag creature, a rounded tag-shaped body, two stubby arms, two small feet",
  icon="a cute paper luggage tag creature with a loop of string on top of its head"),
 "rubric": dict(front2='a cute little square creature whose whole body is a sheet of graph paper, a clear grid of black ruled lines across its front, big happy eyes, four stubby legs',
  neg2='animal, cat, fur, ears',
  key="a ruled grid of rows and columns printed all over its square body",
  front="a cute little square paper score sheet creature, a flat square body, a happy face in the top row of the grid, four stubby legs",
  icon="a cute square paper sheet creature with a ruled grid on it and a happy face"),
 "canon": dict(front2='a cute little grey filing cabinet creature with its top drawer sticking far out, the open drawer full of stacked white paper sheets, big stern eyes on the front, four stubby legs',
  neg2='safe, fridge, closed drawers',
  key="one drawer pulled half open showing stacked white papers",
  front="a cute little steel filing cabinet creature, a square dark grey metal box, a drawer handle, a stern little face, four stubby legs",
  icon="a cute dark grey filing cabinet creature with a stern little face and an open drawer of white papers"),
 "cluster": dict(front2='a cute creature made of seven small round balls stuck together in a bumpy lump, each ball a different size, one ball has a happy face with big eyes, the balls clearly separate with dark lines between them',
  neg2='single sphere, one ball, gear, robot',
  key="a body made of many small round spheres packed tightly together like a ball",
  front="a cute round cluster creature, grey and white spheres of different sizes, a happy face on the biggest front sphere, one small coloured sphere among them",
  icon="a cute ball made of many small grey spheres packed together with a happy face on the front sphere"),
 "locus": dict(front2='a cute little creature shaped like a thick ring donut lying on its side, a big hole through the middle, smooth grey tube, big happy eyes on the front of the ring',
  neg2='cat, ears, fur, tail, paws',
  key="a body shaped like a thick bent loop, a ring of smooth tube curled around on itself like a donut",
  front="a cute little loop creature, smooth grey rounded tube with white bands, a happy face on the front of the loop, a hole through the middle",
  icon="a cute thick grey ring loop creature with a hole in the middle and a happy face"),
 "manifold": dict(front2='a cute little paper manta ray, a body folded from one flat sheet of paper like origami, two wide flat fin wings, a long thin whip tail, big friendly eyes',
  neg2='bat, ears, fur, leaf, plant',
  key="a flat folded sheet body with two wide fin wings and a long thin tail",
  front="a cute little manta ray creature gliding, a smooth curved wave-shaped body like folded paper, big friendly eyes at the front edge",
  icon="a cute little manta ray creature with two wide fin wings, big friendly eyes"),
 "crawler": dict(key="a body made of a row of round ball segments, alternating dark grey and light grey",
  front="a cute chubby caterpillar, a big round white head with large eyes, tiny legs underneath",
  icon="a cute caterpillar with a big round white head and large eyes, its round dark and light segments behind"),
 "pending": dict(key="an egg-shaped cocoon wrapped in dark grey cloth",
  front="a cute pale round sleepy face peeking out of the top of the cocoon, closed eyes, rosy cheeks, no limbs, sitting still",
  icon="a cute pale sleepy face with closed eyes peeking out of a dark grey cloth cocoon"),
 "indexer": dict(key="wide spread wings patterned with grey and white rectangular panels like file cards",
  front="a cute fuzzy little moth, a round dark fuzzy body, two feathery antennae, big eyes",
  icon="a cute fuzzy moth with feathery antennae and big eyes, card-panel wings"),
 "scraper": dict(front2='a cute chubby striped grub larva lying sideways, a body of grey and white bands, a big round head with big eyes, a large dark sharp stinger spike at the tail end',
  neg2='antennae, wings, horns',
  key="a dark sharp stinger spike at its tail and a body of grey and white bands",
  front="a cute chubby grub larva, a round head with big eyes, short stubby legs",
  icon="a cute chubby banded grub larva with a round head and big eyes, a dark stinger tip"),
 "buffer": dict(key="a smooth hard oval shell pod with a narrow slit near the top, two small red eyes peeking out of the slit",
  front="a cute pale grey oval pod creature, a seam like a beetle's back, no limbs, sitting still",
  icon="a cute pale grey oval shell pod with a narrow slit and two small red eyes peeking out"),
 "injector": dict(front2='a cute chubby little grey and white striped wasp with big eyes and clear wings, a very long thin sharp needle stinger like a medical syringe pointing out from its tail',
  neg2='ladybug, beetle, red body',
  key="a long thin needle stinger like a syringe at its tail",
  front="a cute chubby little wasp, a round striped grey and white body, thin clear wings, big eyes, small legs",
  icon="a cute chubby wasp with big eyes, antennae, clear wings and a needle stinger"),
 "relay": dict(front2='a cute plump little grey pigeon holding a big sealed white paper envelope letter in its beak, standing on two small pink feet, big eyes, folded wings',
  neg2='duck, chick, orange beak',
  key="a big white envelope letter tucked under its wing",
  front="a cute plump grey pigeon, a round white chest, a small round head with big eyes, two small pink feet",
  icon="a cute plump grey pigeon with big eyes holding a big white envelope letter"),
 "broadcast": dict(key="wide wings spread fully open",
  front="a cute plump dove with a round white head, beak open calling out happily, a round grey body, small feet",
  icon="a cute plump dove with a white head, beak open calling out, wings spread wide"),
 "nibble": dict(key="a long thin pink tail",
  front="a cute plump little grey rat, a round body, small round pink ears, a pink nose, whiskers, big eyes",
  icon="a cute little grey rat with small round pink ears, a pink nose and big eyes"),
 "overflow": dict(key="an overstuffed lumpy body bulging out in too many round grey lumps",
  front="a cute chubby rat with a dark grey head, a pink nose, big eyes, short stubby legs, a long thin tail",
  icon="a cute chubby rat with a dark grey head, a pink nose, its lumpy bulging grey body behind"),
 "ping": dict(key="a very long thin needle beak",
  front="a cute round little hummingbird hovering, wings raised up high, big eyes, a short tail",
  icon="a cute round hummingbird with big eyes and a very long thin needle beak"),
 "flood": dict(key="a crest of feathers on its head and a long sharp beak",
  front="a cute chubby diving bird with its wings swept back, big eyes, a round grey body, small talons",
  icon="a cute chubby bird with big eyes, a crest of feathers and a long sharp beak"),
}
