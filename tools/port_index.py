#!/usr/bin/env python3
"""Carry the INDEX -- categories and entries -- into the GBA build.

    python3 tools/port_index.py [--write]

This one is not a substitution, it is a REFLOW. Gen 1 writes a dex entry as six
lines of about eighteen characters, split across two pages; Gen 3 writes it as
three lines of about forty-two, on one. So the words are the same and every
line break is wrong. The text is joined and re-wrapped, and anything that will
not fit in three lines is reported rather than truncated.

Only entries we actually changed are touched, so a half-ported Index is
obvious. Both editions get the same text: vanilla ships different dex entries
in FireRed and LeafGreen, and 8.4 fixed both of ours to the same story.
"""
import os, re, subprocess, sys, textwrap

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GB, GBA = os.path.join(ROOT, "engine"), os.path.join(ROOT, "engineGba")
WRITE = "--write" in sys.argv
WIDTH, LINES = 42, 3

def upstream(path):
    return subprocess.run(["git", "-C", GB, "show", "upstream/master:" + path],
                          capture_output=True, text=True).stdout

def categories(text):
    """{Species: CATEGORY} from dex_entries.asm."""
    out = {}
    for m in re.finditer(r'^(\w+)DexEntry:\s*\n\s*db "([^"]*)@"', text, re.M):
        out[m.group(1)] = m.group(2)
    return out

def entries(text):
    """{Species: [words]} from dex_text.asm, with the page break dissolved."""
    out = {}
    for blk in re.split(r'^_(\w+)DexEntry::', text, flags=re.M)[1:]:
        pass
    parts = re.split(r'^_(\w+)DexEntry::', text, flags=re.M)
    for name, body in zip(parts[1::2], parts[2::2]):
        words = " ".join(re.findall(r'(?:text|next|page)\s+"([^"]*)"', body)).split()
        out[name] = words
    return out

ours_cat, van_cat = categories(open(os.path.join(GB, "data/pokemon/dex_entries.asm")).read()), \
                    categories(upstream("data/pokemon/dex_entries.asm"))
ours_txt, van_txt = entries(open(os.path.join(GB, "data/pokemon/dex_text.asm")).read()), \
                    entries(upstream("data/pokemon/dex_text.asm"))

changed_cat = {k: v for k, v in ours_cat.items() if van_cat.get(k) != v}
changed_txt = {k: v for k, v in ours_txt.items() if van_txt.get(k) != v}
print("  %d categories changed, %d entries changed" % (len(changed_cat), len(changed_txt)))

rc = 0
# --- categories ------------------------------------------------------------
path = os.path.join(GBA, "src/data/pokemon/pokedex_entries.h")
text = open(path).read()
placed, missing = 0, []
for name, cat in sorted(changed_cat.items()):
    key = "NATIONAL_DEX_" + re.sub(r'(?<!^)(?=[A-Z])', '_', name).upper()
    pat = re.compile(r'(\[%s\]\s*=\s*\{\s*\.categoryName = _\(")[^"]*("\))' % re.escape(key))
    text, n = pat.subn(r'\g<1>%s\g<2>' % cat, text)
    if n: placed += n
    else: missing.append((name, key))
for name, key in missing:
    print("  !! category: no %s" % key); rc = 1
print("  categories: %d/%d" % (placed, len(changed_cat)))
if WRITE and not missing:
    open(path, "w").write(text)

# --- entries ---------------------------------------------------------------
for fname in ("pokedex_text_fr.h", "pokedex_text_lg.h"):
    path = os.path.join(GBA, "src/data/pokemon", fname)
    text = open(path).read()
    placed, missing, toolong = 0, [], []
    for name, words in sorted(changed_txt.items()):
        wrapped = textwrap.wrap(" ".join(words), WIDTH)
        if len(wrapped) > LINES:
            toolong.append((name, len(" ".join(words)))); continue
        body = "\n".join('    "%s%s"' % (l, "\\n" if i < len(wrapped) - 1 else "")
                         for i, l in enumerate(wrapped))
        sym = "g%sPokedexText" % name
        pat = re.compile(r'(const u8 %s\[\] = _\(\n).*?(\);)' % re.escape(sym), re.S)
        text, n = pat.subn(lambda m: m.group(1) + body + ");", text)
        if n: placed += n
        else: missing.append(sym)
    for s in missing:
        print("  !! entry: no %s in %s" % (s, fname)); rc = 1
    for name, n in toolong:
        print("  !! entry %s is %d chars, will not fit %d lines of %d" % (name, n, LINES, WIDTH)); rc = 1
    print("  %s: %d/%d" % (fname, placed, len(changed_txt) - len(toolong)))
    if WRITE and not missing and not toolong:
        open(path, "w").write(text)
if WRITE:
    print("  written" if rc == 0 else "  NOT written")
sys.exit(rc)
