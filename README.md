# CONTEXT / CONTENT

**A Pokémon Red total conversion where the creatures are AI daemons and the type chart is an argument about consciousness.**

Machines evolved into creatures. This is a Game Boy game about what happened next, and it makes its argument in damage numbers rather than dialogue.

---

## What this is

A total conversion built on [pret/pokered](https://github.com/pret/pokered), the reverse-engineered disassembly of Pokémon Red. Same engine, same 8-bit constraints, entirely different world.

**Two editions, one source tree.** The slash in the title is literal. `pokered` already builds Red *and* Blue from the same sources via two assembler defines, so **CONTENT** and **CONTEXT** cost three lines of Makefile. The type chart is byte-identical in both — it's the argument, and an argument that changes by cartridge isn't one. What differs is which daemons you meet, and what the Index says about them.

Creatures are **daemons** — background processes that run unattended, and the older sense too: the *daimon*, the voice that speaks to you from somewhere you don't control. They are not robots and nobody in the world calls them AI. They just live there.

## The idea

Gen 1 has no abilities, no held items, one Special stat, and fifteen type slots. That's a severe design space, and severity is the appeal: **the type chart ends up carrying the entire philosophy of the game.**

So the fifteen types are the vocabulary of thinking machines — CONTENT and CONTEXT, LOGIC and LATENT, ENTROPY, FLOW, GROWTH, SWARM. The matchups between them aren't decorative. Rules parse data brilliantly and fail at framing, and the combat math says so in every battle, without a single line of dialogue explaining it.

The rest follows the same principle. Kanto's towns were already named after colors and the original game never did anything with it, so this one finishes the job: every city is a word that means both a color and a feeling. Routes are named for what happens *between* colors — bleeding, fading, glazing, gloaming. The official map keeps its numbers. The people who live there use different names.

Nothing in the game explains any of this. That's the rule the whole project runs on.

There is also a rock opera bleeding into it, but that's a longer story.

## Design philosophy

A few rules the project holds itself to, in case they're useful to anyone building something similar:

- **Lessons must be mechanical.** If a gym's lesson can be skipped by grinding, it isn't a lesson.
- **Name the process, not the pathology.** Place names describe what happened to a place, never what a place supposedly *is*.
- **Never say the thesis.** The moment a character explains the theme, it stops being architecture and becomes a moral.
- **The antagonist is not wrong on purpose.** He's optimistic, likable, and optimizing a metric that was easy to measure instead of the one that mattered. That's most real harm, most of the time.

## Status

**Early.** Design is well ahead of implementation. Nothing is playable yet.

See [`docs/`](docs/) for the design bible, which is the honest picture of where this stands — including the decisions that were reversed and why.

Current focus is a vertical slice: three towns, one gym, twelve daemons, playable end to end. The 151-creature bestiary comes after that or not at all. Enough ROM hacks have died designing a full roster before shipping a single town.

## Building

You'll need [RGBDS](https://rgbds.gbdev.io/) and a copy of `pokered`. Follow pret's [install guide](https://github.com/pret/pokered/blob/master/INSTALL.md) first and **confirm you can produce a byte-matching vanilla build before applying anything here.** If the checksum matches, your toolchain is sound and every later break is yours.

```sh
git clone https://github.com/CodeMusic/DAEMONS.git
cd DAEMONS && ./setup.sh
make content
```

`setup.sh` clones the engine beside this repo, wires `upstream` to pret, and
creates the gitignored `engine/` symlink — because **a symlink does not survive
`git clone`**. It is idempotent; run it again whenever something looks off.

The engine is a **fork** of pokered, kept as a sibling repo rather than merged
in, so no Nintendo-derived asset ever enters this repository. The pattern, its
tradeoffs and the alternatives are written up in
[`docs/two-repo-pattern.md`](docs/two-repo-pattern.md).

**No ROMs, no commercial assets, and no copyrighted material are distributed in this repository, and none ever will be.** This is a personal project. Bring your own legally-obtained cartridge dump if you want something to compare against.

## Layout

```
docs/       vision.md — the living design bible, incl. the decision log
            versioned PDF snapshots, type-system build notes
patches/    drop-in files and diffs against a clean pokered checkout
gfx/        original sprite work (front/, back/, overworld/, ui/)
audio/      original music (music/, sfx/)
```

The bible is [`docs/vision.md`](docs/vision.md). It is the only document that
changes; the PDFs are periodic snapshots, kept because the project now has a
Reversed section and what it used to believe is part of the record.

## Credits

Enormous thanks to **[pret](https://github.com/pret)**, whose disassembly work makes projects like this possible at all, and to the **RGBDS** maintainers. Neither is affiliated with this project.

Pokémon is a trademark of Nintendo, Creatures Inc., and GAME FREAK Inc. This project is unaffiliated with and unendorsed by any of them.

## License

Original code, text, art, and music here are released under [choose one — MIT and CC BY-SA 4.0 are the usual pairing]. Nothing in this repository grants any rights to the underlying game.

---

*If you're here because you want to build something strange on an old engine: the constraints are the good part. Take fifteen slots and make them mean something.*
