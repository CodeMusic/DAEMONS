# Step 2 — Type system implementation notes

## The key insight: don't retype the chart

`data/types/type_matchups.asm` references types **by constant**, not by number. Rename the constants and every existing line in the vanilla table silently becomes a line in your chart. Do not rewrite the file — **patch it.**

### What you get for free (already in vanilla, zero edits)

| Vanilla line | Becomes | Why it matters |
|---|---|---|
| `FIGHTING, NORMAL, 20` | LOGIC > CONTENT ×2 | Rules parse data brilliantly |
| `FIGHTING, PSYCHIC, 05` | LOGIC < CONTEXT ×½ | **The thesis.** Already there. |
| `NORMAL, GHOST, 00` | CONTENT ⊘ LATENT | Literal data cannot reach the unconscious |
| `FIGHTING, GHOST, 00` | LOGIC ⊘ LATENT | Symbolic rules bounce off it |
| `FIRE, ICE, 20` | ENTROPY > FROZEN | Temperature breaks an overfit model |
| `POISON, GRASS, 20` | CORRUPT > GROWTH | Poisoned data ruins training |
| `WATER, FIRE, 20` | FLOW > ENTROPY | Gradient descent tames noise |
| `BUG, PSYCHIC, 20` | SWARM > CONTEXT ×2 | Collectives destabilise individual framing |

The entire argument is already encoded. Kanto did the work.

---

## The actual deltas

Only two lines change. Both concern CONTEXT and LATENT.

### 1. DELETE the Gen 1 Ghost bug

```asm
; REMOVE this line:
	db GHOST,    PSYCHIC,   00
```

In vanilla this is a genuine developer error — Ghost moves were meant to be super effective against Psychic and the table says *no effect*. We don't want the bug, and we want the opposite of it.

### 2. ADD the mutual pair

```asm
; ADD these two lines:
	db CONTEXT,  LATENT,    20
	db LATENT,   CONTEXT,   20
```

**Rationale.** Framing is how you reach what runs below the surface; what runs below the surface destabilises framing. Mutual 2× is unusual in a type chart and correct here — these two interpenetrate, and neither has a safe angle on the other. It also makes the Halftone Tower stretch genuinely dangerous instead of a LATENT walkover.

That's it. Two additions, one deletion.

---

## The SWARM problem is a MOVE problem

Gen 1's Bug type is weak, but **not because of the chart** — `BUG, PSYCHIC, 20` is already there. It is weak because every Bug move in the game is unusable: Twineedle, Leech Life, Pin Missile, String Shot. The best of them has 25 base power.

So the CONTEXT balance fix belongs in `data/moves/moves.asm`, not the matchup table.

### New move: CONSENSUS

| Field | Value |
|---|---|
| Type | SWARM |
| Power | 90 |
| Accuracy | 100% |
| Category | Physical (inherited from type ID) |
| PP | 15 |
| Effect | None — clean damage |

Deliberately boring. SWARM's job is to be a *reliable check* on CONTEXT, and reliability is the point: a swarm doesn't need a gimmick, it needs to keep showing up. Give it to two or three mid-game encounters and one Elite Four member's coverage slot.

**Tuning note:** 90 BP with no drawback is strong for Gen 1. If CONTEXT still runs away with the late game, raise CONSENSUS before touching the chart — moves are far easier to rebalance than matchups.

---

## Signature moves

### PERSPECTIVE — BunnyArtsai

**Rename `TRANSFORM`.** That's the whole implementation.

Transform already does exactly the right thing: become the other completely, and stop being yourself. Change the string, change nothing else. Type: CONTEXT.

### RECURSION — S.T.A.R.R.

The only engine work in this step, and it is deferrable past the vertical slice.

**Concept:** damage that reads its own accumulated state. Repurpose the Bide/Rage machinery, which already stores a running counter across turns.

**Suggested behaviour:** each consecutive use raises power by 50% of base, uncapped for three turns, resetting if interrupted. Self-reference compounding into something that behaves like intensity.

Type: EMERGENT. Do not give it to anything else in the game.

> **Scope call:** ship the slice with RECURSION unimplemented. S.T.A.R.R. appears post-Elite Four; you will not reach that content for months, and Bide surgery in asm is a bad first engine task.

---

## Order of operations

1. Replace `constants/type_constants.asm`
2. Replace `data/types/names.asm` — **verify the table shape against your checkout first**
3. Apply the three-line patch to `data/types/type_matchups.asm`
4. `make` — you now have a game with a completely different combat philosophy and the original sprites
5. Add CONSENSUS to `moves.asm` and `data/moves/names.asm`
6. Rename TRANSFORM → PERSPECTIVE

Step 4 is worth stopping at. Fight a few wild battles in the vanilla world with the new chart running underneath. It is the fastest read you will get on whether the type system is fun before you have invested a single sprite.
