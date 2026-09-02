# CONTEXT / CONTENT — convenience shim.
# The real build lives in engine/ (a symlink to the pokered-daemons fork).
# See CLAUDE.md and docs/vision.md 8.4 and 9.2.

ENGINE  := engine
VANILLA := /tmp/pokered-vanilla

.PHONY: all content context content-debug context-debug clean play play-debug vanilla-check verify-sprites bible

all content context content-debug context-debug clean:
	$(MAKE) -C $(ENGINE) $@

## play — build the CONTENT edition and launch it
play: content
	./bindDaemons.sh

## play-debug — the CONTENT edition with upstream's debug mode compiled in.
## SELECT on the title screen opens the debug menu; hold B to skip battles.
play-debug:
	./bindDaemons.sh content --debug

## vanilla-check — prove the toolchain, without disturbing your work.
## Builds pristine upstream in a throwaway worktree and checks the hashes.
## NOTE: `git stash` does NOT work for this — our changes are committed, so
## there is nothing to stash and you would just rebuild your own ROM.
vanilla-check:
	@git -C $(ENGINE) worktree remove --force $(VANILLA) 2>/dev/null || true
	@rm -rf $(VANILLA)
	git -C $(ENGINE) fetch upstream --quiet
	git -C $(ENGINE) worktree add --detach $(VANILLA) upstream/master
	$(MAKE) -C $(VANILLA)
	@cd $(VANILLA) && grep gbc roms.sha1 | shasum -c -
	@git -C $(ENGINE) worktree remove --force $(VANILLA)
	@echo "toolchain sound — any break is ours"

## verify-sprites — prove the built ROMs contain the art in gfx/.
## A .pic is an intermediate: make deletes it after linking, so a .pic left
## with a newer timestamp than its .png ships vanilla art in silence.
verify-sprites:
	@python3 tools/verify_sprites.py

## bible — cut a PDF snapshot, e.g. make bible V=2.0
bible:
	./docs/build-pdf.sh $(V)
