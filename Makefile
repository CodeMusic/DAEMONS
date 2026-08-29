# CONTEXT / CONTENT — convenience shim.
# The real build lives in engine/ (a symlink to the pokered-daemons fork).
# See CLAUDE.md and docs/vision.md 8.4 and 9.2.

ENGINE  := engine
VANILLA := /tmp/pokered-vanilla

.PHONY: all content context clean play vanilla-check bible

all content context clean:
	$(MAKE) -C $(ENGINE) $@

## play — build the CONTENT edition and launch it
play: content
	./bindDaemons.sh

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

## bible — cut a PDF snapshot, e.g. make bible V=2.0
bible:
	./docs/build-pdf.sh $(V)
