; PROJECT: CONTEXT/CONTENT
; constants/type_constants.asm
;
; Gen 1 determines physical vs. special by TYPE ID RANGE, not per-move:
;   $00-$08 -> PHYSICAL   (uses Attack / Defense)
;   $14-$1A -> SPECIAL    (uses Special / Special)
; The two blocks below are therefore a DESIGN DECISION, not a description.
; 8 physical slots and 7 special slots. That allocation is fixed by the engine.

	const_def

; --- PHYSICAL BLOCK ---
	const CONTENT   ; $00  tokens, symbols, literal data
	const LOGIC     ; $01  symbolic rules, brute force, proof
	const VECTOR    ; $02  embeddings, latent space, direction
	const CORRUPT   ; $03  bias, poisoned data, hallucination
	const STRATUM   ; $04  memory, storage, the physical layer
	const LEGACY    ; $05  silicon, deprecated hardware
	const BIRD      ; $06  UNUSED - engine leftover, do not repurpose
	const SWARM     ; $07  multi-agent, distributed (and bugs)
	const LATENT    ; $08  dormant processes, the unconscious

	const_next $14

; --- SPECIAL BLOCK ---
	const ENTROPY   ; $14  noise, temperature, exploration
	const FLOW      ; $15  gradients, backprop, descent
	const GROWTH    ; $16  training, reinforcement, fitting
	const SIGNAL    ; $17  raw input, sensors, current
	const CONTEXT   ; $18  framing, salience, affect
	const FROZEN    ; $19  overfit, brittle, hard-coded
	const EMERGENT  ; $1A  rare, unaccounted-for, AGI-tier
