# Contributing

**Design is well ahead of implementation**, and the documents are where it lives. Read them before proposing
anything: most ideas have been considered, and some were tried and reversed, with the reason written down.

## The documents

| | |
|---|---|
| [`docs/vision.md`](https://github.com/CodeMusic/DAEMONS/blob/main/docs/vision.md) | **The design bible, and the single source of truth.** It carries a version and a decision log with a **Reversed** table -- check it before re-suggesting something |
| [`docs/CHANGELOG.md`](https://github.com/CodeMusic/DAEMONS/blob/main/docs/CHANGELOG.md) | what moved, and when |
| [`docs/TODO.md`](https://github.com/CodeMusic/DAEMONS/blob/main/docs/TODO.md) | work that has been **decided and not done**. The bible's Open log holds a *question*; TODO holds a *job*. Ids are permanent; a closed ticket is struck through with its commit, never deleted |
| [`docs/lineage.md`](https://github.com/CodeMusic/DAEMONS/blob/main/docs/lineage.md) | where the ideas came from: three blogs, 2011 to 2026. Read it before writing anything about the theory |
| [`docs/engine.md`](https://github.com/CodeMusic/DAEMONS/blob/main/docs/engine.md) | the hardware, not the design: the memory budgets, every fixed width, and the traps that have already cost the project time. Read it before adding a static, a name, or a line of text to a pane |
| [`docs/type-chart.pdf`](https://github.com/CodeMusic/DAEMONS/blob/main/docs/type-chart.pdf) | the chart on one sheet |

**Changing the design** means: edit `vision.md` and bump its version line, add a `CHANGELOG.md` entry, cut a new PDF
with `./docs/build-pdf.sh <version>`, and update `docs/README.md`.

## The craft rules

A few rules the writing holds itself to (bible section 0.1):

- **Never say the thesis.** No character, sign or INDEX entry explains what the game is about.
- **Name the process, not the pathology.** A place is named for what happened to it, never for what it supposedly is.
- **Lessons must be mechanical.** If a BENCHMARK's lesson can be skipped by grinding, it is not a lesson.
- **Colour carries the argument, never decorates it.** A daemon is coloured by its type.
- **The type chart is byte-identical across both editions.**
- **Scope discipline.** The vertical slice comes before the bestiary.

## Edit the source, never the artifact

Several of the engine's headers are **generated** from `.json` files and gitignored. A change written into a generated
header exists only in one working build; a fresh clone builds without it. **Write the `.json`** (or whatever the
generator reads), and let the build make the rest.

## The port tools

Everything carried from the Game Boy build to the GBA went through a tool in `tools/`. **Run them from the repository
root; each takes `--write` and only reports without it.**

```sh
python3 tools/port_names.py --write       # species, items, moves, town names
python3 tools/port_index.py --write       # INDEX categories and entries
python3 tools/port_item_text.py --write   # item descriptions
python3 tools/port_oak.py --write         # the professor, and her pronouns
python3 tools/port_vocab.py --write       # POKéMON -> DAEMON, and the rest of the vocabulary
python3 tools/port_dialogue.py --write FILE  # the writing, matched vanilla to vanilla -- name the file
python3 tools/gbasprite.py --write        # sprites, coloured by type
python3 tools/gbamarks.py --write         # the eight MARKS onto the trainer card
python3 tools/port_music.py --write       # the tracks, re-emitted as MIDI
python3 tools/gbastr.py CONTEXT USERBOX   # search a .gba through the charmap
```

Habits worth keeping:

- **`port_names.py` diffs, it does not zip.** It learns `{vanilla -> ours}` by diffing against upstream, which is the
  only way to tell an *addition* from a *rename*.
- **An escape is two characters.** In `\nPOKéMON` the `n` sits against the `P`, so `\b` finds no word boundary. Flatten
  text before you match, and **re-run every tool until it reports nothing.**
- **`gbastr.py` is how to search a ROM.** Gen 3 encodes text through its own charmap, so grepping a `.gba` for ASCII
  finds nothing and proves nothing.
- **A tool whose write would undo later hand work refuses to.** `tools/generator_drift.json` lists them and why;
  `--over-later-work` writes anyway, and then read `git diff`.

## The checks

```sh
python3 tools/check_generators.py   # every --write tool in report mode; fails if one crashes or would write (about 3.5 min)
python3 tools/check_reach.py        # after moving or adding anyone on a map
python3 tools/check_lexicon.py      # the vocabulary
python3 tools/check_agent_vocab.py  # the model harness's vocabulary
python3 tools/companion_export.py --check   # the companion holds the words the game is built from
```

- **`check_generators.py`** before committing: a generated file stays correct on disk long after the tool that wrote
  it has stopped working, and nothing else will tell you. `--writes` runs every tool's write in a sandbox.
- **`check_reach.py`** walks every map from where a player arrives and fails on anything made unreachable that
  vanilla could reach, a door that leads nowhere, a flag the story waits on that nothing sets, and more. A character
  standing in the only doorway once hid a whole stretch of the game for days while every other check passed.

And for any build: **check the exit code, never grep for `error:`** ([Building](Building)).

## Rules for anything public

- **No ROMs, ever**, and no Nintendo-derived assets in this repository. The engines stay as separate forks.
- **Every new in-game word is marked DRAFT** until it is approved.
- **Don't spoil.** Some things the game asks the player to work out are deliberately kept out of every public
  document, this wiki included. If you work one out, please keep it out of issues and pull requests too.
