#!/bin/bash
# T-174 round 2, 2026-09-20. Round 1 failed the same way for eight of the nine, and the way is diagnosable:
#   * a LIGHT GARMENT ON LIGHT FUR dissolves -- AL's cream shirt came back as a bare chest in three of four poses;
#   * a SMALL HELD OBJECT dissolves -- CAIRN's slate and AL's monitor;
#   * and the fur SATURATES -- HOLT's brown otter came back orange, which is the Clears' colour, not his.
# So: denoise 0.32 rather than 0.45 (keep more of the drawing), and a negative that names each failure.
cd /Users/christopherhicks/Projects/DAEMONS
export SPRITEFORGE_HOST=${SPRITEFORGE_HOST:-http://100.67.234.4:8008}
S=gfx/drafts/t174
N="bare chest, shirtless, open shirt, unbuttoned, naked, human, human face, hair, person, man, woman, anime, grey background, colored background, floor, scenery, frame, border, drop shadow, text, watermark, blurry, photorealistic"
while IFS='|' read -r name body; do
  python3 tools/spriteforge.py i2i --image $S/src2/${name}_hi.png --denoise 0.32 --seed 1917 --out $S/alt2/${name}_r2 \
    --prompt "pure white background, pixel art game sprite of a single anthropomorphic $body, full body, clean black outline, isolated on white, centered" \
    --negative "$N" 2>&1 | tail -1
done <<'LIST'
holt|dark brown river otter engineer with an otter head and a thick tapering tail, brown fur not orange, in buttoned blue-grey work coveralls and a tool belt, holding a coil of cable
vera|red fox woman with a fox head and a bushy tail, in a full cream apron with a clear outline over a pale long-sleeved dress, hands together at her waist
init|basset hound with long drooping ears and a dark heavy muzzle, in a plain beige robe with a clear outline and sandals, standing still
cairn|green tortoise with a domed shell, in a buttoned white shirt and a dark work apron and brown boots, both hands holding a flat dark slate tablet
scorn|red cobra with a hooded snake head and a long coiled tail, in a buttoned grey business suit with a red tie, one hand held out
al_speech|young red fox in a BUTTONED cream collared shirt with sleeves, purple trousers, brown boots, a satchel at his side, one hand on his hip
al_early|young red fox in a BUTTONED cream collared shirt with sleeves, purple trousers, brown boots, carrying a small grey computer under one arm
al_late|young red fox in a BUTTONED cream collared shirt with sleeves, purple trousers, brown boots, one arm raised
al_champion|young red fox in a BUTTONED cream collared shirt with sleeves, purple trousers, brown boots, one arm out with the palm forward
LIST
