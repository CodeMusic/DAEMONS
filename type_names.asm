; PROJECT: CONTEXT/CONTENT
; data/types/names.asm
;
; LENGTH LIMIT: 8 characters. Vanilla's longest are FIGHTING and ELECTRIC (8).
; Longer strings overflow the battle status box and the Dex type field.
;
;   CONTENT  7    STRATUM  7    ENTROPY  7
;   LOGIC    5    LEGACY   6    FLOW     4
;   VECTOR   6    SWARM    5    GROWTH   6
;   CORRUPT  7    LATENT   6    SIGNAL   6
;   CONTEXT  7                  FROZEN   6
;                               EMERGENT 8  <- exactly at the limit
;
; SUBSTRATE (9) was cut for this reason. STRATUM keeps the layer meaning.
;
; NOTE: the pointer list is CONTIGUOUS (16 entries) even though the type IDs
; are not. GetTypeName folds the $14+ block down to index 9. Verify the exact
; table shape against your checkout before pasting - it drifts between commits.

TypeNames:
	dw .Content
	dw .Logic
	dw .Vector
	dw .Corrupt
	dw .Stratum
	dw .Legacy
	dw .Bird     ; unused engine slot
	dw .Swarm
	dw .Latent
	dw .Entropy
	dw .Flow
	dw .Growth
	dw .Signal
	dw .Context
	dw .Frozen
	dw .Emergent

.Content:  db "CONTENT@"
.Logic:    db "LOGIC@"
.Vector:   db "VECTOR@"
.Corrupt:  db "CORRUPT@"
.Stratum:  db "STRATUM@"
.Legacy:   db "LEGACY@"
.Bird:     db "BIRD@"
.Swarm:    db "SWARM@"
.Latent:   db "LATENT@"
.Entropy:  db "ENTROPY@"
.Flow:     db "FLOW@"
.Growth:   db "GROWTH@"
.Signal:   db "SIGNAL@"
.Context:  db "CONTEXT@"
.Frozen:   db "FROZEN@"
.Emergent: db "EMERGENT@"
