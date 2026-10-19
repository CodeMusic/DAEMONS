"""The engine's own glyph widths, keyed by character -- one reader for every tool that measures a line (T-421).

    from fontwidth import font, charmap, glyph_widths

Six tools carried their own copy of this, and five read charmap.txt's apostrophe line, `'\\'' = B4`, as a key four
characters long: the apostrophe was not in their map and measured 0px, so every 208px check was blind to it. The
engine draws it 3px wide (sFontNormalLatinGlyphWidths[0xB4]). Nothing here imports a tool, so importing it runs
nothing.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")

#  charmap.txt writes a quote that cannot sit between quotes as an escape
_ESCAPED = {"'\\''": "'", '"\\""': '"', "'\\\\'": "\\"}


def charmap(gba=GBA):
    """{character: byte} for every single-character entry in charmap.txt, the last entry winning (as the tools
    that measured before this did). A string entry ("...") of one character counts too; multi-byte values keep
    their first byte."""
    cm = {}
    for line in open(os.path.join(gba, "charmap.txt"), encoding="utf-8"):
        line = line.split("@")[0].strip()
        if "=" not in line:
            continue
        k, v = (p.strip() for p in line.split("=", 1))
        if k in _ESCAPED:
            k = _ESCAPED[k]
        elif len(k) == 3 and k[0] == k[2] == "'":
            k = k[1]
        elif len(k) > 1 and k[0] == k[-1] == '"':
            k = k[1:-1]
        try:
            cm[k] = int(v.split()[0], 16)
        except (ValueError, IndexError):
            pass
    return cm


def glyph_widths(table="sFontNormalLatinGlyphWidths", gba=GBA):
    """One of src/text.c's width tables, as a list indexed by byte."""
    src = open(os.path.join(gba, "src/text.c"), encoding="utf-8").read()
    body = re.search(r"%s\[\]\s*=\s*\{(.*?)\};" % re.escape(table), src, re.S).group(1)
    return [int(x) for x in re.findall(r"\d+", body)]


def all_glyph_widths(gba=GBA):
    """{table name: widths} for every sFont*LatinGlyphWidths table in src/text.c."""
    src = open(os.path.join(gba, "src/text.c"), encoding="utf-8").read()
    return {n: [int(x) for x in re.findall(r"\d+", b)] for n, b in
            re.findall(r"(sFont\w*LatinGlyphWidths)\[\]\s*=\s*\{(.*?)\};", src, re.S)}


def font(gba=GBA):
    """(widths, charmap) for the message box's font -- what the tools called _font()."""
    return glyph_widths(gba=gba), charmap(gba)


if __name__ == "__main__":
    w, cm = font()
    print("  apostrophe: byte 0x%02X, %dpx" % (cm["'"], w[cm["'"]]))
