#!/usr/bin/env python3
"""THE PROGRAMMER'S GUIDE TO THE HUMAN MIND, in the game (T-300..T-302; vision.md 4.36).

    python3 tools/genguide.py            # report: every entry measured, every rule checked
    python3 tools/genguide.py --write     # engineGba/src/data/guide.h and graphics/book/guide_cover.png

WHAT IT IS. The user's own book (docs/archive/, 137 pages), which the game lets you find on THE MARGINS and read: its
text is docs/guide.md, compressed to 28 entries under four rules, and this turns that into the C the reader prints
(src/book_reader.c). Every line is measured against the page it will be printed on, and the rules the text must keep
are checked word by word -- the book says outright what the game never does, so the checks are the point.

ITS LOOK is its own cover (T-302): the cover image is read out of the PDF itself, the brain is cropped from it and
reduced to the book's sixteen colours, and the lettering is set in the game's own font -- HUMAN MIND at twice the size,
as the cover has it. The sixteen colours are the reader's palette roles (C_PAPER, C_INK, ...) for this book: charcoal
boards and pages, white and silver, and one cyan, MEASURED against every type hue because a UI colour may not be a
type's (9.4). The cover's own cyan is 22.7 from SIGNAL; this one is 29.6 from the nearest.
"""
import io, os, re, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
SRC = os.path.join(ROOT, "docs/guide.md")
PDF = os.path.join(ROOT, "docs/archive/The Programmers Guide to the Human Mind.pdf")
OUT_H = os.path.join(GBA, "src/data/guide.h")
OUT_COVER = os.path.join(GBA, "graphics/book/guide_cover.png")
WRITE = "--write" in sys.argv

# ---------------------------------------------------------------- the page, as book_reader.c draws it
PAGE_TEXT_W = 94            # TB_TEXT_W: the text column on either page
LEFT_LINES, RIGHT_LINES = 7, 9
MAX_LINES = 96              # GB_MAX_LINES in the reader
SHORT_W = 100               # a contents entry on the right page
LABEL_W = 86                # a section on the left page
TITLE_LINES = 4             # the full title, FONT_SMALL, over at most four lines at the head of the left page

# ---------------------------------------------------------------- the four rules (docs/guide.md, vision.md 4.36)
#  1: about people -- nothing of the game's own vocabulary, and no colour beside a feeling
RULE1 = [r"\bdaemons?\b", r"\bcontent\b", r"\bcontext\w*\b", r"\bcolou?rs?\b", r"\btypes?\b", r"\bindex\b"]
#  2: the analogy offered, never asserted
RULE2 = [r"\bmind is (a |the )?(software|machine|computer|program)", r"\bnot just (a )?metaphor", r"more than (just )?a metaphor"]
#  3: the process, never the pathology
RULE3 = [r"\banxi", r"\bdepress", r"\btrauma", r"\bptsd\b", r"\baddict", r"\bphobi", r"\bdisorder", r"\bdiagnos", r"\bpatholog"]
#  4: no substance named
RULE4 = [r"\bpsychedel", r"\blsd\b", r"\bpsilocybin", r"\bdmt\b", r"\bmushroom", r"\bdrugs?\b"]
RULES = [("1: about people", RULE1), ("2: only ever LIKE", RULE2), ("3: process, not pathology", RULE3),
         ("4: no substance", RULE4)]

# ---------------------------------------------------------------- the sixteen colours, by the reader's roles
PALETTE = [
    ("C_NONE",        (0, 0, 0)),
    ("C_PAPER",       (40, 42, 46)),      # a page: charcoal, a shade up from the boards
    ("C_INK",         (230, 234, 238)),   # the text: near-white
    ("C_SHADOW",      (18, 19, 22)),      # its shadow, below the page
    ("C_FAINT",       (120, 128, 138)),   # folios, headings, a section's part number
    ("C_RULE",        (0, 150, 205)),     # the traces and rules: the cyan, dimmed
    ("C_MARGIN",      (0, 200, 255)),     # the cyan itself: a node, the cursor's edge
    ("C_EDGE",        (62, 64, 70)),      # the leaves beneath
    ("C_EDGE_DARK",   (30, 31, 35)),
    ("C_HIGHLIGHT",   (78, 82, 90)),      # the cursor's bar: a grey, so it is nobody's hue
    ("C_RING",        (178, 186, 194)),   # silver
    ("C_FRAME",       (12, 12, 14)),      # the spine, the gutter
    ("C_SLATE",       (48, 46, 46)),      # the boards
    ("C_CHALK",       (250, 250, 250)),   # the cover's lettering
    ("C_CHALK_FAINT", (104, 110, 118)),   # silver in shadow
    ("C_COVER",       (22, 22, 24)),      # the backdrop around the book
]
IDX = {name: i for i, (name, _) in enumerate(PALETTE)}


def lab(c):
    def f(u):
        u /= 255
        return ((u + 0.055) / 1.055) ** 2.4 if u > 0.04045 else u / 12.92
    r, g, b = map(f, c)
    X = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    Y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    Z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    t = lambda v: v ** (1 / 3) if v > 0.008856 else 7.787 * v + 16 / 116
    return (116 * t(Y) - 16, 500 * (t(X) - t(Y)), 200 * (t(Y) - t(Z)))


def type_hues():
    src = open(os.path.join(ROOT, "tools/gbasprite.py"), encoding="utf-8").read()
    return {k: tuple(map(int, v.split(","))) for k, v in re.findall(r'"(\w+)":\s*\(\s*([\d,\s]+?)\)', src)}


def check_palette():
    """A colour that has a hue must be 20 or more (CIE76) from every type's -- 9.4's own separability line."""
    bad, hues = [], type_hues()
    for name, c in PALETTE[1:]:
        if max(c) - min(c) < 24:
            continue                     # a neutral: the house ramp's greys are nobody's type
        d, t = min((sum((a - b) ** 2 for a, b in zip(lab(c), lab(v))) ** .5, k) for k, v in hues.items())
        if d < 20:
            bad.append("%s %s is %.1f from %s's hue" % (name, c, d, t))
    return bad

# ---------------------------------------------------------------- the font, from the engine
def load_font():
    src = open(os.path.join(GBA, "src/text.c"), encoding="utf-8").read()
    def widths(name):
        return [int(x) for x in re.findall(r"\d+", re.search(name + r"\[\]\s*=\s*\{(.*?)\};", src, re.S).group(1))]
    cm = {}
    for line in open(os.path.join(GBA, "charmap.txt"), encoding="utf-8"):
        line = line.split("@")[0].strip()
        if "=" not in line:
            continue
        k, v = (p.strip() for p in line.split("=", 1))
        if k == "'\\''":
            k = "'"
        elif len(k) == 3 and k[0] == k[2] == "'":
            k = k[1]
        else:
            continue
        try:
            cm.setdefault(k, int(v.split()[0], 16))
        except ValueError:
            pass
    return widths("sFontNormalLatinGlyphWidths"), widths("sFontSmallLatinGlyphWidths"), cm


WN, WS, CM = load_font()


def width(s, small=False):
    w = WS if small else WN
    return sum(w[CM[c]] for c in c_string(s).replace("\\p", "") if c in CM)


def reflow(text, w, small=False):
    """book_reader.c's Reflow: words wrapped to W; a paragraph starts a new line."""
    lines = []
    for para in text.split("\n\n"):
        line = ""
        for word in para.split():
            cand = word if not line else line + " " + word
            if line and width(cand, small) > w:
                lines.append(line)
                line = word
            else:
                line = cand
        if line:
            lines.append(line)
    return lines

# ---------------------------------------------------------------- the text
def parse():
    sections, cur, entry = [], None, None
    body = open(SRC, encoding="utf-8").read().split("\n## ", 1)[1]
    for raw in ("## " + body).split("\n"):
        line = raw.rstrip()
        m = re.match(r"^## (\w+) \| (.+?) \| (.+)$", line)
        if m:
            cur = {"key": m.group(1), "label": m.group(2), "heading": m.group(3), "entries": []}
            sections.append(cur)
            entry = None
            continue
        m = re.match(r"^### (.+?) \| (.+)$", line)
        if m:
            entry = {"short": m.group(1), "title": m.group(2), "paras": [[]]}
            cur["entries"].append(entry)
            continue
        if entry is None:
            continue
        if line.strip():
            entry["paras"][-1].append(line.strip())
        elif entry["paras"][-1]:
            entry["paras"].append([])
    for s in sections:
        for e in s["entries"]:
            e["text"] = "\n\n".join(" ".join(p) for p in e["paras"] if p)
    return sections


def c_string(s):
    """For _("..."): straight quotes become the game's curly pair, a paragraph becomes \\p."""
    out, opened = [], False
    for ch in s:
        if ch == '"':
            out.append("”" if opened else "“")
            opened = not opened
        else:
            out.append(ch)
    return "".join(out).replace("\n\n", "\\p")


def check_text(sections):
    bad = []
    for s in sections:
        if len(reflow(s["heading"], PAGE_TEXT_W, small=True)) > 2:
            bad.append("section %s: its heading takes more than the right page's two small lines" % s["label"])
        if width(s["label"]) > LABEL_W:
            bad.append("section %s: %dpx, the left page takes %d" % (s["label"], width(s["label"]), LABEL_W))
        for e in s["entries"]:
            for field in ("short", "title", "text"):
                for ch in c_string(e[field]).replace("\\p", ""):
                    if ch not in CM and ch != " ":
                        bad.append("%s: %r is not in the charmap" % (e["short"], ch))
            if width(e["short"]) > SHORT_W:
                bad.append("%s: %dpx on the contents page, which takes %d" % (e["short"], width(e["short"]), SHORT_W))
            if len(reflow(e["title"], PAGE_TEXT_W, small=True)) > TITLE_LINES:
                bad.append("%s: its full title takes %d small lines, the head of the page has %d"
                           % (e["short"], len(reflow(e["title"], PAGE_TEXT_W, small=True)), TITLE_LINES))
            n = len(reflow(e["text"], PAGE_TEXT_W))
            if n > MAX_LINES:
                bad.append("%s: %d lines, the reader holds %d" % (e["short"], n, MAX_LINES))
            flat = " ".join([e["title"], e["text"]]).lower()
            for rule, pats in RULES:
                for p in pats:
                    for m in re.finditer(p, flat):
                        bad.append("%s breaks rule %s: %r" % (e["short"], rule, flat[max(0, m.start() - 20):m.end() + 20]))
    return bad


def spreads(e):
    n = len(reflow(e["text"], PAGE_TEXT_W))
    return max(1, -(-n // (LEFT_LINES + RIGHT_LINES)))


def header(sections):
    out = ["// Generated by DAEMONS tools/genguide.py from docs/guide.md -- edit those, not this.",
           "// T-300/T-301: THE PROGRAMMER'S GUIDE TO THE HUMAN MIND. DRAFT WORDING, every string, until the user",
           "// approves it on the private field-test page. The four rules it keeps are in vision.md 4.36.", ""]
    n = sum(len(s["entries"]) for s in sections)
    out.append("#define GUIDE_SECTIONS %d" % len(sections))
    out.append("#define GUIDE_ENTRIES  %d" % n)
    out.append("")
    k = 0
    for i, s in enumerate(sections):
        out.append('static const u8 sGuideLabel_%d[] = _("%s");' % (i, c_string(s["label"])))
        out.append('static const u8 sGuideHeading_%d[] = _("%s");' % (i, c_string(s["heading"])))
        for e in s["entries"]:
            out.append('static const u8 sGuideShort_%d[] = _("%s");' % (k, c_string(e["short"])))
            out.append('static const u8 sGuideTitle_%d[] = _("%s");' % (k, c_string(e["title"])))
            out.append('static const u8 sGuideText_%d[] = _("%s");' % (k, c_string(e["text"])))
            k += 1
        out.append("")
    out.append("static const struct GuideSection sGuideSections[GUIDE_SECTIONS] =\n{")
    k = 0
    for i, s in enumerate(sections):
        out.append("    { sGuideLabel_%d, sGuideHeading_%d, %d, %d }," % (i, i, k, len(s["entries"])))
        k += len(s["entries"])
    out.append("};\n")
    out.append("static const struct GuideEntry sGuideEntries[GUIDE_ENTRIES] =\n{")
    for i in range(n):
        out.append("    { sGuideShort_%d, sGuideTitle_%d, sGuideText_%d }," % (i, i, i))
    out.append("};")
    return "\n".join(out) + "\n"

# ---------------------------------------------------------------- the cover
COVER_X, COVER_W = 56, 128


def cover_source():
    import fitz
    d = fitz.open(PDF)
    xref = d[0].get_images()[0][0]
    return Image.open(io.BytesIO(d.extract_image(xref)["image"])).convert("RGB")


def glyphs(text, small=False, scale=1):
    """TEXT in the game's own font, as (x, y) of each lit pixel -- the glyph's ink, not its shadow."""
    img = Image.open(os.path.join(GBA, "graphics/fonts/latin_small.png" if small else "graphics/fonts/latin_normal.png"))
    cw, per_row, w = (8, 32, WS) if small else (16, 16, WN)
    px, x = [], 0
    for ch in text:
        g = CM[ch]
        ox, oy = (g % per_row) * cw, (g // per_row) * 16
        for yy in range(16):
            for xx in range(w[g]):
                if img.getpixel((ox + xx, oy + yy)) == 1:
                    for sy in range(scale):
                        for sx in range(scale):
                            px.append((x + xx * scale + sx, yy * scale + sy))
        x += w[g] * scale
    return px, x


def nearest(c, roles):
    return min(roles, key=lambda r: sum((a - b) ** 2 for a, b in zip(PALETTE[IDX[r]][1], c)))


def build_cover():
    W, H = 240, 160
    pix = [[IDX["C_COVER"]] * W for _ in range(H)]

    def rect(role, x, y, w, h):
        for yy in range(max(0, y), min(H, y + h)):
            for xx in range(max(0, x), min(W, x + w)):
                pix[yy][xx] = IDX[role]

    def text(s, y, role, small=False, scale=1):
        pts, tw = glyphs(s, small, scale)
        x0 = COVER_X + 4 + (COVER_W - 4 - tw) // 2
        for (x, yy) in pts:
            if 0 <= y + yy < H:
                pix[y + yy][x0 + x] = IDX[role]

    rect("C_FRAME", COVER_X - 2, 1, COVER_W + 4, 159)                   # the book's edge on the backdrop
    rect("C_SLATE", COVER_X, 2, COVER_W, 157)                           # the boards
    rect("C_FRAME", COVER_X, 2, 4, 157)                                 # the spine
    rect("C_MARGIN", COVER_X, 150, 2, 7)                                # the cover's one blue mark, low on the spine
    text("THE PROGRAMMER'S", 3, "C_CHALK", small=True)
    text("GUIDE TO THE", 12, "C_CHALK", small=True)
    text("HUMAN MIND", 20, "C_CHALK", scale=2)
    rect("C_RULE", COVER_X + 10, 50, COVER_W - 16, 1)                   # the two rules around the subtitle
    rect("C_RULE", COVER_X + 10, 54, COVER_W - 16, 1)

    # the brain, from the cover itself: cropped, reduced, and every pixel given the nearest of the book's colours
    src = cover_source()
    w, h = src.size
    brain = src.crop((int(w * 0.13), int(h * 0.17), int(w * 0.87), int(h * 0.84)))
    bw, bh = 96, 88
    brain = brain.resize((bw, bh), Image.LANCZOS)
    roles = ["C_SLATE", "C_FRAME", "C_EDGE_DARK", "C_EDGE", "C_CHALK_FAINT", "C_RING", "C_CHALK", "C_RULE",
             "C_MARGIN", "C_HIGHLIGHT"]
    bx, by = COVER_X + 4 + (COVER_W - 4 - bw) // 2, 58
    for y in range(bh):
        for x in range(bw):
            c = brain.getpixel((x, y))
            #  the cover's own dark ground becomes the boards, so the brain stands on the book and not in a box
            dark = (c[0] * 77 + c[1] * 150 + c[2] * 29) >> 8 < 58 and max(c) - min(c) < 40
            pix[by + y][bx + x] = IDX["C_SLATE" if dark else nearest(c, roles)]

    text("CHRISTOPHER ART HICKS", 147, "C_CHALK", small=True)
    img = Image.new("P", (W, H))
    img.putpalette([v for _, c in PALETTE for v in c] + [0] * (768 - 48))
    img.putdata([v for row in pix for v in row])
    return img

# ---------------------------------------------------------------- the bag's icon
OUT_ICON = os.path.join(GBA, "graphics/items/icons/guide.png")
OUT_ICON_PAL = os.path.join(GBA, "graphics/items/icon_palettes/guide.pal")
ICON_KEY = (180, 180, 180)      # index 0, the bag's transparent colour, as every icon's


def build_icon():
    """24x24: the book standing, its two white title bars and cyan rules, and the cover's brain the size of a thumb."""
    icon = [[0] * 24 for _ in range(24)]
    roles = ["C_FRAME", "C_SLATE", "C_EDGE", "C_RING", "C_CHALK", "C_RULE", "C_MARGIN", "C_CHALK_FAINT"]
    pal = [ICON_KEY] + [PALETTE[IDX[r]][1] for r in roles]
    ix = {r: i + 1 for i, r in enumerate(roles)}
    for y in range(1, 23):
        for x in range(4, 20):
            icon[y][x] = ix["C_FRAME"] if x in (4, 19) or y in (1, 22) else ix["C_SLATE"]
    for y in range(2, 22):
        icon[y][5] = ix["C_FRAME"]                                   # the spine
    icon[19][5] = icon[20][5] = ix["C_MARGIN"]                       # its one blue mark
    for x in range(8, 17):
        icon[3][x] = ix["C_CHALK"]                                   # the title, as two bars
    for x in range(7, 18):
        icon[5][x] = ix["C_CHALK"]
        icon[7][x] = ix["C_RULE"]
    #  the brain, drawn: at this size the cover's own reduces to a grey smudge (tried, 2026-09-25)
    brain = ["..RRR.RRR..",
             ".R..sRs..R.",
             "R.c..R..c.R",
             "R.ss.R.ss.R",
             "R..s.R.s..R",
             ".R..sRs..R.",
             "..RR.R.RR..",
             "....RRR...."]
    key = {"R": "C_RING", "s": "C_CHALK_FAINT", "c": "C_MARGIN"}
    for y, row in enumerate(brain):
        for x, ch in enumerate(row):
            if ch in key:
                icon[10 + y][7 + x] = ix[key[ch]]
    img = Image.new("P", (24, 24))
    img.putpalette([v for c in pal for v in c] + [0] * (768 - 3 * len(pal)))
    img.putdata([v for row in icon for v in row])
    return img, pal + [(0, 0, 0)] * (16 - len(pal))

# ---------------------------------------------------------------- report / write
def main():
    sections = parse()
    bad = check_palette() + check_text(sections)
    n = sum(len(s["entries"]) for s in sections)
    words = sum(len(e["text"].split()) for s in sections for e in s["entries"])
    print("  %d sections, %d entries, %d words (the book: about 26,000)" % (len(sections), n, words))
    for s in sections:
        print("    %-12s %s" % (s["label"], "  ".join("%s(%d)" % (e["short"], spreads(e)) for e in s["entries"])))
    for b in bad:
        print("  !! " + b)
    if bad:
        return 1
    h = header(sections)
    cover = build_cover()
    same_h = os.path.exists(OUT_H) and open(OUT_H, encoding="utf-8").read() == h
    same_c = os.path.exists(OUT_COVER) and list(Image.open(OUT_COVER).getdata()) == list(cover.getdata()) \
        and Image.open(OUT_COVER).getpalette()[:48] == cover.getpalette()[:48]
    print("  src/data/guide.h %s; graphics/book/guide_cover.png %s"
          % ("already written" if same_h else "to write", "already drawn" if same_c else "to draw"))
    if os.environ.get("SCRATCH"):
        cover.convert("RGB").resize((720, 480), Image.NEAREST).save(os.path.join(os.environ["SCRATCH"], "guide_cover.png"))
    icon, icon_pal = build_icon()
    pal_text = "JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % c for c in icon_pal)
    same_i = os.path.exists(OUT_ICON) and list(Image.open(OUT_ICON).getdata()) == list(icon.getdata()) \
        and os.path.exists(OUT_ICON_PAL) and open(OUT_ICON_PAL, newline="").read() == pal_text
    print("  graphics/items/icons/guide.png %s" % ("already drawn" if same_i else "to draw"))
    if os.environ.get("SCRATCH"):
        icon.convert("RGB").resize((96, 96), Image.NEAREST).save(os.path.join(os.environ["SCRATCH"], "guide_icon.png"))
    if WRITE:
        if not same_i:
            icon.save(OUT_ICON)
            open(OUT_ICON_PAL, "w", newline="").write(pal_text)
        if not same_h:
            open(OUT_H, "w", encoding="utf-8").write(h)
        if not same_c:
            cover.save(OUT_COVER)
        print("  written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
