#!/bin/bash
# T-210 babies, 2026-10-01: nine named daemons still on vanilla art, each drawn image-to-image from its parent's own
# redrawn sprite so the family holds (as T-327 did for LENSMUSAI). Fronts at denoise 0.8, backs at 0.65, seed 42.
cd "$(dirname "$0")/../../.."
SRC=gfx/drafts/t210babies/src
G="full body, greyscale, medium grey body with light grey highlights and dark grey shading, clean black outline, isolated on white, centered, small in the frame with empty space all around, no shadow, no text"
N="human, person, colored background, floor, ground, shadow, text, watermark, multiple creatures, scenery, photorealistic, blurry, cropped, border, white body, pale body"
draw() { # name parent "description"
  python3 tools/spriteforge.py i2i --seed 42 --denoise 0.8 --image $SRC/$2_front_512.png --out gfx/drafts/t210babies/$1_front \
    --prompt "pure white background, pixel art game sprite of a baby creature, $3, front view, facing the viewer, $G" \
    --negative "side view, rear view, adult, $N"
  python3 tools/spriteforge.py i2i --seed 42 --denoise 0.65 --image $SRC/$2_back_512.png --out gfx/drafts/t210babies/$1_back \
    --prompt "pure white background, pixel art game sprite of a baby creature, $3, rear view, facing away from the viewer, back of the head, $G" \
    --negative "face, eyes, front view, side view, adult, $N"
}
draw valence mood "a tiny round baby mouse, oversized head, short stubby limbs, a big round bouncy ball on the end of its tail"
draw residual anomaly "a tiny baby star-shaped creature, a five-pointed star body, two small curled horns, little stub wings, oversized head"
draw crank dynamo "a small chubby bear cub robot with a big wind-up key sticking out of its back, stubby limbs, oversized head"
draw standby suspend "a tiny round puffball, eyes half closed as if asleep, a small curl of fur on top, stubby feet"
draw cinder forge "a tiny smouldering lump of coal with little feet, an orange ember glowing in its cracks, oversized head"
draw static spike "a tiny fuzzy baby rat with big ears and a small zigzag lightning-bolt tail, oversized head, stubby limbs"
draw tell coldread "a tiny fluffy baby owl chick, a round owlet with huge eyes, stubby wings, orange feet"
draw premise axiomkick "a small young martial artist in a training stance, round head, stubby limbs, a headband"
draw rankle resentment "a tiny round grey blob with a small dome-shaped body, a sulky frown, stubby little arms"

# Second pass (2026-10-01), after the contact sheet: VALENCE's and CRANK's backs were not back views, TELL was the adult
# owl again, PREMISE came out a human boy, CINDER's back read as a lamp. Written as *_2; the first drafts stay.
redo() { # out source denoise "prompt" "extra negative"
  python3 tools/spriteforge.py i2i --seed 42 --denoise $3 --image $SRC/$2.png --out gfx/drafts/t210babies/$1 \
    --prompt "pure white background, pixel art game sprite of a baby creature, $4, $G" --negative "adult, $5, $N"
}
redo valence_back_2 mood_back_512 0.72 "a tiny round baby mouse seen from behind, rear view, facing away from the viewer, the back of its head and its round ears, a big round ball on the end of its tail" "face, eyes, front view, side view, lying down"
redo crank_back_2 dynamo_back_512 0.7 "a small chubby bear cub robot seen from behind, rear view, facing away from the viewer, round bear ears, a big wind-up key sticking out of the middle of its back" "face, eyes, front view, side view, antennae, insect"
redo tell_front_2 coldread_front_512 0.92 "a tiny round fluffy owlet chick covered in downy fluff, oversized round eyes, very small stubby wings, short orange feet, chubby and much smaller than an adult owl, front view, facing the viewer" "side view, rear view, long feathers, tall"
redo tell_back_2 coldread_back_512 0.85 "a tiny round fluffy owlet chick covered in downy fluff seen from behind, rear view, facing away from the viewer, the back of its round head, very small stubby wings, short orange feet" "face, eyes, beak, front view, side view, long feathers, tall"
redo premise_front_2 axiomkick_front_512 0.75 "a small round grey creature like a tiny ghostly blob wearing a headband, stubby fists raised in a fighting stance, front view, facing the viewer" "human, boy, child, person, hair, skin, clothes, side view, rear view"
redo cinder_back_2 forge_back_512 0.72 "a tiny smouldering lump of coal with little feet seen from behind, rear view, facing away from the viewer, an orange ember glowing in its cracks" "face, eyes, front view, side view, lamp, pedestal"

# Third pass: RANKLE's entry says it "smiles the whole time, so nobody thinks to ask" -- the first draft frowned.
redo rankle_front_3 resentment_front_512 0.8 "a tiny round grey blob with a small dome-shaped body and a wide fixed smile that never changes, stubby little arms, front view, facing the viewer" "frown, sad, angry, side view, rear view"
