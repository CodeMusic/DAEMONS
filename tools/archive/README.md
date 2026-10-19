# tools/archive/

Tools that have done their job and that no other tool, script, check or doc instruction runs or imports
(T-421, approved by the user 2026-10-19). They are kept, not deleted, because each one is the record of how a
change went into the build. `check_generators.py` scans only `tools/`, so nothing here is run by the checks.

Each tool's `ROOT` now points up from `tools/archive/` to the repo, so they still run from the repo root as they did.

| tool | what it did |
|---|---|
| `gbahouses.py` | T-59: redrew BLANCHE's two houses as two buildings. A one-shot migration: it asserts the vanilla rows it replaced, which are gone. |
| `gbamapedit.py` | T-71: the first ROUTE 1 edit (the pond). One-shot; asserts the grass it put the pond on. |
| `gbascholar.py` | the OWL's study in BRAZEN. One-shot; asserts the house it replaced. `gbaschoolfront.py` still describes its method. |
| `gen_sprite_prompts.py` | printed the per-daemon image prompts for the full-colour sprites from `gbasprite.py`'s types and hues. |
| `t210apply.py` | T-210: wrote each approved batch (`docs/drafts/t210_batch*.json`) into the species names, INDEX categories and both editions' entries. |
| `t210check.py` | T-210: checked a batch's words (name and category lengths, words already in use, entry width) before it went in. |

## Running T-210's two, if ever needed

Both read `docs/drafts/t210_batch*.json`. From the repo root:

```sh
python3 tools/archive/t210check.py                                # every batch: names, categories, entry widths
python3 tools/archive/t210check.py docs/drafts/t210_batch5.json   # one batch
python3 tools/archive/t210apply.py                                # report: every daemon the engine disagrees with
python3 tools/archive/t210apply.py --write                        # put the batches back into the engine
```

On 2026-10-19 both ran clean from here: every batch clear, and "7 batch(es), the engine agrees with every one".
**`t210apply.py --write` would undo any hand edit made to those names, categories or entries since a batch went
in** -- read its report first.
