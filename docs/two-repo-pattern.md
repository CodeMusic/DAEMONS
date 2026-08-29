# The two-repo symlink pattern

Why this project is two git repositories joined by a symlink, what that buys,
what it costs, and how to apply it elsewhere.

---

## The problem

You are building on top of somebody else's large codebase. You need:

- **their tree**, buildable, and updatable when they fix things
- **your own material** — design docs, notes, drafts — versioned separately
- **one place to stand**, so a build command and an editor (and an AI session)
  can see everything at once

Those pull in opposite directions. Put everything in one repo and you inherit
their history, their size, and — often — their licensing exposure. Keep them
apart and every task spans two directories.

## The pattern

Two sibling repositories. One symlink. The link is **gitignored**, so it is
local scaffolding rather than tracked content.

```
~/Projects/
  DAEMONS/                    yours — docs, patches, assets
    engine ────────┐          gitignored symlink
    .gitignore     │            engine
    setup.sh       │          recreates the link after a clone
  pokered-daemons/ ◄┘         a fork of the upstream project
```

From inside `DAEMONS`, `engine/data/types/names.asm` resolves normally. Tools,
shells, editors and AI sessions all see one tree. Git sees two.

### The three moving parts

**1. The fork, with two remotes.**

```sh
git remote -v
origin      https://github.com/you/theirproject-yours.git    # your work
upstream    https://github.com/them/theirproject.git         # their fixes
```

`git pull upstream master` brings their changes in. `git push origin` sends
yours nowhere near them.

**2. The symlink, ignored.**

```sh
ln -sfn ../pokered-daemons engine
echo engine >> .gitignore
```

It is a signpost, not a copy — `stat -f %i engine/Makefile ../pokered-daemons/Makefile`
returns the same inode. Nothing is duplicated and nothing is committed.

**3. A setup script, because symlinks do not survive `git clone`.**

This is the tradeoff that decides everything else. A fresh clone of `DAEMONS`
has **no `engine/`**. Without a documented reconstruction step the pattern is
undiscoverable to anyone — including you, later. Hence [`setup.sh`](../setup.sh):
clone the engine if missing, add `upstream`, make the link, check the toolchain.

Make it **idempotent**. You will run it when something looks wrong, not only on
a fresh machine.

## When this beats the alternatives

| Approach | Gets you | Costs |
|---|---|---|
| **Symlink** *(this)* | Zero ceremony. Two clean histories. Their assets never enter your repo. | Does not survive a clone — needs `setup.sh` |
| **Submodule** | Survives cloning; pins their exact commit to yours | Detached HEADs, two-step commits, a long tail of confusion |
| **Subtree** | One repo, their history merged in, no setup step | Your repo now contains their code and their licence questions |
| **Vendoring** (copy it in) | Simplest possible | You have adopted their code and lost upstream updates |
| **Monorepo** | Everything together | Only sane if you own both sides |

**Choose symlink when their assets should not live in your repo.** That is the
deciding factor here: `pokered/gfx/` holds Nintendo-derived sprites, and this
project's README promises not to distribute copyrighted material. A submodule
would honour that too, but at higher friction for no gain on a solo project.

**Choose submodule when other people will clone it** and you need their engine
version pinned to your commit. If DAEMONS ever gains collaborators, this is the
upgrade path — and `setup.sh` is where you would make the switch.

## Gotchas, all of which we hit

**Name the directory after the repo, not the upstream.** We had `~/Projects/pokered`
alongside a fork called `pokered-daemons`, which made it genuinely unclear which
tree was authoritative. Renaming ended the confusion instantly.

**Fork before you rewire remotes.** `git remote add origin <url> && git push`
fails on a repo that does not exist yet, and the error you see may be about SSH
keys rather than the missing repo. Create the fork first.

**Match the transport you already use.** If you push other repos over HTTPS, use
HTTPS here. An `git@github.com: Permission denied (publickey)` is often just the
wrong protocol rather than a real key problem.

**`git stash` is not "check out their pristine version".** Stash only touches
*uncommitted* changes. If your work is committed, stash finds nothing, you
rebuild your own tree, and your checksums fail correctly while you conclude the
toolchain is broken. Use a throwaway worktree instead:

```sh
git worktree add --detach /tmp/pristine upstream/master
make -C /tmp/pristine && (cd /tmp/pristine && shasum -c hashes)
git worktree remove --force /tmp/pristine
```

**Two Makefiles means two sets of targets.** A shim at your root can forward
`build`/`clean` into theirs and add your own targets — but *your* targets only
exist at your root. Document which is which or you will run one from inside the
other and get `No rule to make target`.

**Gitignore the build artefacts on the far side too.** `engine/*.gbc` and
`engine/*.sav` are yours to ignore even though they land in their tree.

## For AI coding sessions specifically

Two extra reasons the single root matters:

**Memory and context are keyed to the session root.** Rooting a session in the
engine gives it a different memory store, and it will not know any of your
design decisions. **Always root at the docs repo** and reach into the engine
through the link.

**Put the contract in `CLAUDE.md` at that root.** Read-first order, the layout,
build commands, and the invariants that would cost hours to rediscover. That
file — not the directory structure — is what actually prevents design and
implementation drifting apart.

## Applying it to a new project

```sh
# 1. fork theirs, clone yours side by side
gh repo fork them/theirproject --clone=false --fork-name theirproject-mine
git clone https://github.com/you/theirproject-mine.git ~/Projects/theirproject-mine
git -C ~/Projects/theirproject-mine remote add upstream https://github.com/them/theirproject.git

# 2. link it into your repo, and ignore it
cd ~/Projects/myproject
ln -sfn ../theirproject-mine engine
printf 'engine\nengine/*.out\n' >> .gitignore

# 3. write setup.sh so step 1 and 2 are reproducible
# 4. write CLAUDE.md so the next session knows the shape
```

Then work in one directory, commit in two, and keep their code out of your
history.
