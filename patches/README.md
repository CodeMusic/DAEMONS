# patches/

Drop-in files and diffs against a **clean `pokered` checkout**. Nothing here is a
complete file from any commercial ROM, and nothing here builds on its own.

| File | Replaces | Notes |
|---|---|---|
| `type_constants.asm` | `constants/type_constants.asm` | Wholesale replacement. The `const_next $14` gap is the physical/special split and is not optional. |
| `type_names.asm` | `data/types/names.asm` | **Do not paste wholesale.** Table shape drifts between pokered commits — open yours, count the `dw` lines, replace only the strings. See vision.md 9.1. |

## Order

Per `docs/vision.md` 9.2. In short:

1. Confirm a **byte-matching vanilla build** first. If the checksum matches, the toolchain is sound and every later break is yours.
2. `type_constants.asm`
3. `type_names.asm` — strings only, structure untouched
4. The three-line patch to `data/types/type_matchups.asm`: delete `db GHOST, PSYCHIC, 00`, add the mutual `CONTEXT`/`LATENT` pair
5. `make`, then **stop and play.** Vanilla sprites, vanilla maps, your combat philosophy underneath.

Step 5 is the milestone that tells you whether the type system is fun, before a
single pixel is drawn.
