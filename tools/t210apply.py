#!/usr/bin/env python3
"""T-210: put each approved batch's names, INDEX categories and entries into the GBA build.

    python3 tools/t210apply.py            # report: every daemon in docs/drafts/t210_batch*.json the engine disagrees with
    python3 tools/t210apply.py --write    # write them

The batches are drafted with the user, one JSON each (docs/drafts/t210_batch1.json ...): the vanilla species, our name,
the INDEX category, and the CONTENT (firered, pokedex_text_fr.h) and CONTEXT (leafgreen, pokedex_text_lg.h) entries.
This keeps all four places in step with them -- species_names.h, pokedex_entries.h's categoryName and both editions'
text -- so a batch written once cannot drift, and running it twice changes nothing. Art is gbasprite.py's (from
gfx/daemons/<name>_front/_back.png); routines are move_names.h, by hand, once the user has approved them.
"""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv
FILES = {"names": "src/data/text/species_names.h", "cat": "src/data/pokemon/pokedex_entries.h",
         "content": "src/data/pokemon/pokedex_text_fr.h", "context": "src/data/pokemon/pokedex_text_lg.h"}


def text_body(lines):
    return "\n".join('    "%s%s"' % (l, "\\n" if i < len(lines) - 1 else "") for i, l in enumerate(lines))


def main():
    src = {k: open(os.path.join(GBA, f), encoding="utf-8").read() for k, f in FILES.items()}
    new = dict(src)
    changed, batches = [], sorted(glob.glob(os.path.join(ROOT, "docs/drafts/t210_batch*.json")))
    for b in batches:
        for x in json.load(open(b))["daemons"]:
            sp, cap = x["species"], x["species"].capitalize()
            edits = (
                ("names", r'(\[SPECIES_%s\]\s*=\s*_\(")[^"]*("\))' % sp, x["name"]),
                ("cat", r'(\[NATIONAL_DEX_%s\]\s*=\s*\{\s*\.categoryName\s*=\s*_\(")[^"]*("\))' % sp, x["category"]),
            )
            for k, pat, val in edits:
                if len(re.findall(pat, new[k])) != 1:
                    raise SystemExit("  refused: %s not found once in %s" % (sp, FILES[k]))
                new[k] = re.sub(pat, lambda m: m.group(1) + val + m.group(2), new[k])
            for k in ("content", "context"):
                pat = r'(const u8 g%sPokedexText\[\] = _\(\n)(.*?)(\);\n)' % cap
                if len(re.findall(pat, new[k], re.S)) != 1:
                    raise SystemExit("  refused: %s's entry not found once in %s" % (sp, FILES[k]))
                new[k] = re.sub(pat, lambda m: m.group(1) + text_body(x[k]) + m.group(3), new[k], flags=re.S)
    for k in FILES:
        if new[k] != src[k]:
            changed.append(FILES[k])
    print("  %d batch(es), %s" % (len(batches), "the engine agrees with every one" if not changed
                                  else "would change: " + ", ".join(changed)))
    if changed and WRITE:
        for k in FILES:
            if new[k] != src[k]:
                open(os.path.join(GBA, FILES[k]), "w", encoding="utf-8").write(new[k])
        print("  written")
    elif changed:
        print("  report only; pass --write")


if __name__ == "__main__":
    main()
