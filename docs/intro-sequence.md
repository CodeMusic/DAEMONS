# The intro sequence — a sketch

**Drafted 2026-09-04.** The Gen 3 intro was cut because filling it meant
sixteen drawings, twelve of them matched animation frames, and matched frames
are the one thing image models cannot hold.

***This does not need any of them.***

## What we already have

| | |
|---|---|
| **CODEMUSAI**, lunging, 64×64 | drawn, in the ROM, on the title |
| **CAREMUSAI**, opening, 64×64 | drawn, in the ROM, on the title |
| **code motes** — 0 and 1, cold, 3 frames | drawn |
| **note motes** — warm, 3 frames | drawn |
| **the bloom** — 4 frames, ends | drawn |
| sprite movement, h-flip, palette fades | *free, in code* |

**A face-off is movement and light.** The creatures do not need to be redrawn
in sixteen poses; they need to *arrive*, *hold*, and *not change each other*.

## The sixteen beats

| | | costs |
|---|---|---|
| 1 | Black. One `0`. Then one `1`. | a sprite |
| 2 | The field fills with code motes, **all drifting the same way** | the spawner |
| 3 | **CODEMUSAI** slides in from the left, mid-lunge | a sprite, moving |
| 4 | It holds. The motes gather *toward* it | spawn direction |
| 5 | The cold light drops. **Notes appear** — warm, and *not in step with each other* | anim 1 |
| 6 | **CAREMUSAI** slides in from the right, open | a sprite, moving |
| 7 | Both fields on screen at once. ***Neither changes the other*** | nothing |
| 8 | The two figures move toward the middle | movement |
| 9 | The gap narrows. Motes begin **crossing** it | the title's own callback |
| 10 | First arrivals — **single blooms**, one at a time | anim 2 |
| 11 | More. The blooms begin to **overlap** | spawn rate |
| 12 | The screen goes bright — *a palette flash, not a drawing* | `BlendPalettes` |
| 13 | White | — |
| 14 | The white recedes. Both figures, **still, facing each other** | the title's own layout |
| 15 | Colour arrives **in the background**, where there was none | palette |
| 16 | Cut to the title, which is already this picture | — |

***Not one new creature drawing.***

## Why it is the right scene and not just the affordable one

**7 is the whole design.** Two fields, on screen together, and *neither converts
the other* — 2's chart is that LOGIC fails against CONTEXT, and the way it
fails is by not landing, not by losing a fight.

**And 12 is 9.14, third time.** The presents scene says *colour is what arrives
when two things that disagree connect*; the mark behind the words says it as a
shape; this says it as an event. **Three scenes, one sentence, none of them
speaking it.**

*The vanilla intro ends with one creature knocking the other down.* **Ours ends
with both still standing and the room lit.** That difference is the entire
project, and it is made by cutting a fight rather than animating one.

## What it costs in code

A fourth `IntroCB_` in the existing chain — the callbacks are already a state
machine and beats map onto states one to one. It reuses:

- `sSpriteTemplate_FaceOffCode` / `_FaceOffCare`, already loaded on the title
- the crossing-particle spawner and callback, **already written**, with the
  spawn points moved and the convergence turned on later
- `BlendPalettes`, which the scene already uses for its fades

**The risk is timing, not capability** — every beat is a state and a frame
count, and those want tuning by eye rather than by design.

## The one open question

**Does the player skip it?** Vanilla lets A, START or SELECT jump to the title
at any point, and that is still wired. *If beat 7 is the argument*, a player who
skips never sees it — which is either a problem or exactly right, since the game
does not explain itself to people who are not looking.
