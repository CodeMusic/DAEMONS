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

## Layout — one session root, three repos

```
DAEMONS/             <- ALWAYS root sessions here (memory lives here)
  docs/              design bible, lineage, changelog, blog drafts
  patches/           published diffs against a clean pokered checkout
  gfx/ audio/        original assets
  engine/    ----->  symlink to ../pokered-daemons       (Game Boy)
  engineGba/ ----->  symlink to ../pokefirered-daemons   (GBA, under evaluation)
```

Both symlinks are gitignored and neither fork is ever vendored: both carry
Nintendo-derived graphics and this repo promises not to distribute copyrighted
material. Work in them freely; just don't merge either one in here.

**After a fresh clone, run `./setup.sh`** — it clones both forks, sets their
`upstream` remotes, remakes the symlinks, and builds `agbcc` (which installs
*into* `engineGba/tools/` and so does not survive a fresh clone either). It is
idempotent.

### Two engines, and which one is real

`engine/` is **CodeMusic/pokered-daemons** and it is where the vertical slice
actually is — Benchmark 1, the type chart, 64 sprites, the music.

`engineGba/` is **CodeMusic/pokefirered-daemons**, forked 2026-09-02, and it is
a **spike, not a decision.** It exists to answer one question: are abilities,
item descriptions and a real scripting language worth rebuilding 334 files for?
See `docs/vision.md` 9.3. Until that is answered, **do not port work into it
and do not port work out of it.** Nothing about the design changes either way —
`docs/` is engine-independent and always has been.

The edition split survives the port unchanged, which is the first good sign:

| | CONTENT | CONTEXT |
|---|---|---|
| `engine/` | `_RED` | `_BLUE` |
| `engineGba/` | `firered` | `leafgreen` |

## Porting to the GBA build

Everything carried across so far went through a tool, and each one lives in
`tools/`. **Run them from the repo root; each takes `--write` and reports
without it.**

```sh
python3 tools/port_names.py --write      # species, items, moves, town names
python3 tools/port_index.py --write       # Index categories and entries
python3 tools/port_item_text.py --write   # item descriptions (new writing)
python3 tools/port_oak.py --write         # OAK -> CRYSTAL CLEAR, and her pronouns
python3 tools/port_vocab.py --write       # POKéMON -> DAEMON, and the rest of it
python3 tools/port_dialogue.py --write    # our WRITING, matched vanilla to vanilla
python3 tools/gbasprite.py --write        # 66 sprites, coloured by type
python3 tools/gbamarks.py --write         # the eight MARKS onto the trainer card
python3 tools/port_music.py --write       # our tracks, re-emitted as MIDI
python3 tools/gbastr.py CONTEXT USERBOX   # search a .gba through the charmap
```

Two habits worth keeping:

**`port_names.py` diffs, it does not zip.** It learns `{vanilla -> ours}` by
diffing our table against upstream's with `difflib`, which is the only way to
tell an **addition** from a **rename** — a positional zip read §2.5's added move
`CONSENSUS` as *"STRUGGLE was renamed to CONSENSUS"*, which would have renamed
Gen 3's Struggle.

**Edit the source, never the artifact.** `json_data_rules.mk` generates seven
headers — `items.h`, `region_map_entry_strings.h`, `region_map_entries.h`,
`wild_encounters.h`, `heal_locations.h` and two constants files — and every one
of them is **gitignored**. `port_names.py` wrote the sixteen town names into
`region_map_entry_strings.h` and they existed only in one working build: a
fresh clone would have built vanilla Kanto. Write the `.json`. And note that
renaming a mapsec renames a generated C symbol `src/region_map.c` refers to by
hand — the generator works on **bytes**, so `é` is two underscores and POKéMON
MANSION is `sMapsecName_POK__MON_MANSION`.

**An escape is two characters and the first is a letter.** In `\nPOKéMON` the
`n` sits against the `P`, so `\b` finds **no word boundary** and every word at
the start of a line is invisible to a pattern looking for it. This has now hidden
substitutions in three separate tools. Flatten before you match, and **re-run
every tool until it reports nothing** — that is what caught all three.

**`gbastr.py` is the GBA's `verify-sprites`.** Gen 3 encodes text through its
own `charmap.txt` exactly as Gen 1 does, so grepping a `.gba` for ASCII finds
nothing and proves nothing. Compiling is not evidence on this machine either.

## Build

`bindDaemons.sh` builds an edition and launches it. **It defaults to the GBA
spike, so `--classic` is how you reach the build that has a game in it.**

```sh
./bindDaemons.sh                    # CONTENT, GBA      -> mGBA
./bindDaemons.sh context            # CONTEXT, GBA
./bindDaemons.sh --classic          # CONTENT, Game Boy -> SameBoy
./bindDaemons.sh context --classic  # CONTEXT, Game Boy
./bindDaemons.sh --debug            # GBA testing build (ours)
./bindDaemons.sh --classic --debug  # Game Boy testing build (upstream's)
```

The `make` shim still forwards into `engine/` only — it is the classic build:

```sh
make content        # -> engine/daemonsContent.gbc
make context        # -> engine/daemonsContext.gbc
make verify-sprites # prove the ROMs contain the art in gfx/
make vanilla-check  # prove the classic toolchain against pristine upstream
```

For the GBA build, `make -C engineGba firered` (or `leafgreen`, or
`firered_debug`). **`shasum -c firered.sha1` now fails by design** — the ROM
carries our content. It proves the *toolchain* on a pristine `pret/pokefirered`
checkout, and it did still pass after the debug scaffolding went in, which was
the point at the time. It is not a regression check for this fork.

**pokefirered ships no debug build**, unlike pokeemerald, so `firered_debug`
is ours: `DAEMONS_DEBUG=1` suffixes `BUILD_NAME`, so it gets its own ROM file
and therefore its own save. A new game starts with six daemons picked for their
**abilities**, one of each **kind** of item so the description window can be
read, all eight badges and 999999; hold B to walk through grass. It is
scaffolding for the §9.3 spike rather than a general debug menu — those are the
two things being evaluated.

**Never filter a build for `error:`.** agbcc prints its diagnostics as
`warning:` lines and then fails with a bare `Error 1`, so `make … | grep -i
"error:"` reports a clean build while the ROM silently keeps the previous
binary. This has now caused two bugs in this project — the Route 1 music on the
Game Boy side and a stale debug ROM here. **Check the exit code**:

```sh
make -C engineGba firered_debug -j8 >/dev/null 2>&1; echo "exit=$?"
```

`bindDaemons.sh` gets this right already: it runs under `set -euo pipefail`, so
a failed build aborts the script rather than launching a stale ROM.

**GBA toolchain.** `arm-none-eabi-gcc` from Homebrew (no sudo), plus `agbcc`
built from source into `engineGba/tools/agbcc`. Homebrew's ARM gcc ships no
libc, so `MODERN=1` fails on `string.h`; agbcc brings its own headers and is
the path that works here.

`red` and `blue` still work in `engine/` as aliases. The `_RED`/`_BLUE`
assembler defines are **unchanged** — renaming those touches 47 asm files and
is deferred. Only the output names, make targets and cart titles moved.

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
