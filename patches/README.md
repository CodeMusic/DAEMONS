# patches/

Changes against a **clean `pret/pokered` checkout**. Nothing here is a complete
file from any commercial ROM, and nothing here builds on its own.

## Applied and building

| File | What | Status |
|---|---|---|
| [`0001-type-system.patch`](0001-type-system.patch) | The fifteen type names, and the two matchup deltas | **built clean, 2026-08-28** |

```sh
git clone https://github.com/pret/pokered.git
cd pokered
make && shasum -c roms.sha1      # confirm a byte-matching vanilla build FIRST
git checkout -b context-content
git am ../DAEMONS/patches/0001-type-system.patch
make red
```

Step 2 is the gate. If the vanilla checksums match, the toolchain is sound and
every later break is yours.

## Reference only — do NOT paste these

| File | Why not |
|---|---|
| `type_constants.asm` | Master wraps the list in `DEF PHYSICAL`, `DEF UNUSED_TYPES`/`_END`, `DEF SPECIAL` and `DEF NUM_TYPES`. `names.asm` depends on three of them; this file defines none. Pasting it breaks the build. |
| `type_names.asm` | Master uses `table_width 2`, a `REPT` block filling the ID gap, and `assert_table_length`. Nothing like this file. Change the **strings only**, in place. |

Both remain useful as the canonical statement of *what the fifteen types are and
why*. Treat them as design documents, not drop-ins. See vision.md 9.1.

## What the applied patch actually does

**Strings only** in `data/types/names.asm` — structure untouched:

CONTENT · LOGIC · VECTOR · CORRUPT · STRATUM · LEGACY · BIRD *(unused engine
slot, left alone)* · SWARM · LATENT · ENTROPY · FLOW · GROWTH · SIGNAL ·
CONTEXT · FROZEN · EMERGENT

**Two deltas** in `data/types/type_matchups.asm`:

```asm
; removed - the Gen 1 developer error
db GHOST,        PSYCHIC_TYPE, NO_EFFECT

; added - framing reaches what runs below the surface, and is destabilised by it
db PSYCHIC_TYPE, GHOST,        SUPER_EFFECTIVE
db GHOST,        PSYCHIC_TYPE, SUPER_EFFECTIVE
```

Every other line in the vanilla table carries over untouched and is already a
line in our chart. Kanto did the work.

## Not yet applied

- The two-edition build: rename `_RED`/`_BLUE` to `_CONTENT`/`_CONTEXT` in the
  Makefile. Cheap now, miserable to retrofit. See vision.md 8.4.
