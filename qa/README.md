# QA and testing

What the build looked like when it was checked: the evidence, kept beside the code so anyone reading the repository
can see the game without building it.

```
qa/
  screenshots/
    2026-10-01/          one folder a day; its README.md is the gallery, captions and pictures
      t297_folds_tell.png    <ticket>_<name>.png
    private/             GITIGNORED -- anything not ready to be public (below)
```

**Every picture sent for review is filed here** (CLAUDE.md, *Showing the user what changed*), with the same caption:

```sh
python3 tools/qashot.py --ticket T-297 --caption "FOLDS' corner of paper, before and after" sheet.png
python3 tools/qashot.py --ticket T-335 --caption "the dated pages" --private pages.png
python3 tools/qashot.py --list
```

**Most of these are not screenshots of a running game.** They are review sheets decoded from the built ROM's own
data -- sprites, maps, text in the game's font -- by `tools/reviewsheet.py` and its kin, because that is what can be
checked on every push without an emulator. A caption says when a picture was played on a screen instead.

**What goes in `private/`.** Anything that shows a NOTEBOOK page; anything drawn from `docs/private/`; any of the four
things the game asks the player to work out (CLAUDE.md, *Never put these in public writing*). **When in doubt,
private**: a picture can be moved out later, and never taken back once pushed. `qashot.py` refuses a public filing
that sounds private unless told it was looked at.

**Every word in a picture is a DRAFT** until the ticket it belongs to says it was approved.
