# CONTEXT / CONTENT — working agreement

A `pokered` total conversion where the creatures are daemons and the type chart
is an argument about consciousness. **Design is well ahead of implementation.**

## Always start here

- **`docs/vision.md`** is the design bible and the single source of truth. Read it
  before proposing anything. It carries a version (currently v1.8) and a decision
  log with a **Reversed** table — check that before re-suggesting something.
- **`docs/CHANGELOG.md`** is what moved and when.
- **`docs/lineage.md`** is where the ideas came from — three blogs, 2011–2026.
  Read it before writing anything about the theory.

## Layout — one session root, two repos

```
DAEMONS/            <- ALWAYS root sessions here (memory lives here)
  docs/             design bible, lineage, changelog, blog drafts
  patches/          published diffs against a clean pokered checkout
  gfx/ audio/       original assets
  engine/  ------>  symlink to ../pokered-daemons  (gitignored, never vendored)
```

`engine/` is **CodeMusic/pokered-daemons**, a fork of pret/pokered. `origin` is the
fork, `upstream` is pret — so `git pull upstream master` brings in their fixes.
It is kept out of this repo because `pokered/gfx/`
contains Nintendo-derived sprites and this repo promises not to distribute
copyrighted material. Work in it freely; just don't merge it in here.

## Build

From the repo root (a shim forwards into `engine/`):

```sh
make red            # -> engine/pokered.gbc
make blue           # -> engine/pokeblue.gbc
make                # all targets
make vanilla-check  # prove the toolchain
```

**Before diagnosing any build break:** `make vanilla-check` from the repo root.
It builds pristine `upstream/master` in a throwaway git worktree and checks the
hashes, without touching your branch. If vanilla matches, the toolchain is fine
and the break is ours.

Do **not** use `git stash` for this. Our changes are committed, so there is
nothing to stash and you would simply rebuild your own ROM and watch the
checksums "fail" correctly.

## Invariants — do not violate without an explicit decision

1. **Never say the thesis.** Craft rule 1 governs everything *inside* the game —
   dialogue, signs, Index entries. It does not govern these docs or blog posts.
2. **Name the process, not the pathology** (craft rule 3). Especially in 4.10.
3. **The type chart is byte-identical across both editions.** It is the argument;
   an argument that changes by cartridge is not one. See 8.4.
4. **Never paste `patches/type_constants.asm` or `type_names.asm` wholesale.**
   They are design documents, not drop-ins — master's structure is different and
   pasting either breaks the build. See 9.1.
5. **Greyscale is the design, not a limitation.** Colour appears once, at the
   Review Board. See 8.6.
6. **Renaming type constants is optional and expensive.** Only the *strings* in
   `data/types/names.asm` affect what the player reads. `ROCK` collides with
   `ROCK_SLIDE`, `FIRE` with `FIRE_BLAST`, `BUG` with the Bug Catcher class.

## Never put these in public writing

The game asks the player to work them out. A reader who knows them cannot un-know them.

- The Five Witnesses lock and its number
- Ty Clear's parentage
- The Corpus lobby engraving
- The order of the Quicksilver sequence (4.10) — the dating scheme exists so the
  player reconstructs it

## When you change the design

1. Edit `docs/vision.md` and bump the version line at the top
2. Add a `docs/CHANGELOG.md` entry
3. `./docs/build-pdf.sh <version>` and delete the superseded PDF
4. Update `docs/README.md`'s current-version row

## Scope discipline

Section 8 exists because *"the graveyard of ROM hacks is full of projects that
designed 151 creatures and shipped zero towns."* The vertical slice comes before
the bestiary. If a conversation has produced three design revisions and no build,
say so.
