#!/usr/bin/env python3
"""THE SUBTLE LAYER, in the game and in the companion (T-423; docs/psychic-routines-notes.md D and D2).

    python3 tools/gensubtle.py                       # report: every entry measured, every rule checked
    python3 tools/gensubtle.py --write                # engineGba/src/data/subtle_layer.h and graphics/book/subtle/
    python3 tools/gensubtle.py --write --engine DIR   # the same, into another engine checkout (a worktree)
    python3 tools/gensubtle.py --book hermetic        # one book only (subtle, hermetic); without it, both

THE HERMETIC LAYER (T-483) is read by the same parser into the same open book: docs/hermetic-layer.md, written to
src/data/hermetic_layer.h and graphics/book/hermetic/. Its own rules are the four that file's header keeps (it is the
one exception to the rest); a paragraph opening '^ ' is an INSCRIPTION, printed in the tablet's emerald (C_RING, which
the reader breathes), and its pictures are not drawn yet -- every entry shows one plain placeholder frame.

WHAT IT IS. The user's own book, *Developing Psychic Routines*, rewritten for the game as a trainer's handbook
(docs/subtle-layer.md). It is read as an OPEN BOOK (the user, 2026-10-18): a contents spread, then each entry opens
with its picture on the left page and its text on the right, continuing over both pages -- book_reader.c's textbook
geometry, two 110px pages with a 94px column. Every line is measured against that column with genguide's own font
maths, and the book's rules are checked word by word, as the Guide's are.

ITS PICTURES are ink diagrams, one per entry (tools/subtle_sprites.py), each colour mapped to one of the reader's
sixteen palette roles and written as an indexed PNG the build turns into 4bpp. The palette is CONTEXT's hue on a dark
plum page, ON PURPOSE: the user chose colour carrying the argument for this book (D: hue C), so unlike the Guide's
cyan it is not measured away from the type hues. The seven centres and the heart are never given a hue.

THE COMPANION reads the same text through subtle_book() and subtle_art(), from tools/companion_export.py.
"""
import os, re, sys
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import genguide as g
import subtle_sprites as sp

ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "docs/subtle-layer.md")
WRITE = "--write" in sys.argv
ONLY = sys.argv[sys.argv.index("--book") + 1] if "--book" in sys.argv else None
BOOK = "subtle"
ENGINE = sys.argv[sys.argv.index("--engine") + 1] if "--engine" in sys.argv else os.path.join(ROOT, "engineGba")

# ---------------------------------------------------------------- the spread, as book_reader.c draws it
TW, PITCH, TOP, BOTTOM = 94, 13, 14, 135       # TB_TEXT_W; a line every 13px; a page's text from 14 to 135
PIC_W, PIC_H = 96, 88                           # the left page's picture box, whole tiles
CAPTION_LINES = 3

# ---------------------------------------------------------------- the rules (docs/subtle-layer.md's header)
RULES = [   # (name, pattern, case-sensitive, entries excused)
    ("practice, not cosmology", r"one awareness|panpsychi|figure of speech|is aware\b", False, ()),
    ("never names the two layers", r"content and context|context and content|called (content|context)", False, ()),
    ("only ever like", r"not just (a )?metaphor|mind is (a |the )?(machine|program|computer)", False, ()),
    ("no colour", r"\b(red|orange|yellow|green|blue|indigo|violet|purple|colou?rs?|hues?)\b|#[0-9a-f]{6}", False, ()),
    ("process, not pathology", r"anxi|depress|trauma|headache|fatigue|digest|disorder|diagnos|patholog|symptom|paraly"
                               r"|cancer|tumou?r|immun|oncolog|disease|\bvices?\b", False, ()),
    ("over, never cures (T-418)", r"\bcur(e|es|ed|ing)\b|\billness\b|\bsick\b", False, ("SPELLING", "THE SEVEN")),
    ("not the scientist (4.33)", r"one field|everything is one|never two things|same awareness", False, ()),
    ("the world does not know its name", r"\bDAEMONS\b|oldest sense", True, ()),
    ("never the thesis", r"are you present|running your life|a daemon is (not )?the", False, ()),
    ("no species, no fable explained", r"\bfox|\bpaws?\b|\bfur\b|\bowls?\b|were hatched|\bclothes|\bcoat\b|\bmart\b", False, ()),
    ("no device in the game's copy", r"\bdevice|\bscreen", False, ()),
    ("the kindred guard", r"share a name|same name|surname|family name|last name", False, ()),
    ("nobody's real name", r"christopher|\bchris\b|hicks|bannister|einstein|hortons", False, ()),
    ("left behind", r"hero gene|epigenet|left brain|right brain|faster than light|for a reason|superhero"
                    r"|conceive and believe|will be will be", False, ()),
    ("the decided names", r"(?<!in )\bcharge\b|resonance|\btheme\b|\bpassion\b", False, ()),
]

# ---------------------------------------------------------------- the sixteen colours, by the reader's roles (5-bit)
PALETTE = [
    ("C_NONE",        (0, 0, 0)),
    ("C_PAPER",       (7, 4, 6)),       # the page: a dark plum
    ("C_INK",         (30, 28, 29)),    # the text: a pinkish white
    ("C_SHADOW",      (2, 2, 2)),
    ("C_FAINT",       (20, 14, 18)),    # folios, captions, the asking voice
    ("C_RULE",        (22, 10, 19)),    # CONTEXT's hue (176 86 158), as the GBA can hold it
    ("C_MARGIN",      (29, 17, 26)),    # the hue, lit: a node, the next-page mark
    ("C_EDGE",        (10, 6, 9)),
    ("C_EDGE_DARK",   (4, 2, 4)),       # and the pictures' darkest shade
    ("C_HIGHLIGHT",   (12, 8, 11)),     # the cursor's bar, and the pictures' dim tone
    ("C_RING",        (22, 18, 21)),
    ("C_FRAME",       (1, 1, 1)),
    ("C_SLATE",       (9, 4, 8)),       # the cover's boards
    ("C_CHALK",       (31, 30, 30)),    # the cover's lettering
    ("C_CHALK_FAINT", (17, 12, 15)),
    ("C_COVER",       (3, 1, 3)),       # the backdrop
]
IDX = {name: i for i, (name, _) in enumerate(PALETTE)}
RGB8 = {name: tuple((c << 3) | (c >> 2) for c in v) for name, v in PALETTE}
SPRITE_ROLE = {sp.PAPER: "C_PAPER", sp.INK: "C_INK", sp.FAINT: "C_FAINT", sp.DIM: "C_HIGHLIGHT",
               sp.HUE: "C_RULE", sp.HUE_LIGHT: "C_MARGIN", sp.SHADE: "C_EDGE_DARK"}

# ---------------------------------------------------------------- T-483: THE HERMETIC LAYER, the one exception
# docs/hermetic-layer.md's header: what the book still keeps, word by word. The rest of THE SUBTLE LAYER's rules are
# the ones this book is allowed to break (bible 4.39); the four secrets are kept by the writer, not by a pattern here.
HERMETIC_RULES = [
    ("process, not pathology", RULES[4][1], False, ()),
    ("over, never cures (T-418)", r"\bcur(e|es|ed|ing)\b|\billness\b|\bsick\b", False, ()),
    ("reason and instinct (9.10)", r"\bintuition\b|\blogic and\b", False, ()),
    ("the world does not know its name", r"\bDAEMONS\b", True, ()),
    ("no device in the game's copy", r"\bdevice|\bscreen", False, ()),
    ("nobody's real name", RULES[12][1], False, ()),
]

# A night page; INSCRIPTIONS in the tablet's emerald (C_RING, which the reader breathes toward C_MARGIN, the emerald lit);
# the rules in THE SUBTLE LAYER's purple; the backdrop (C_COVER) is where the reader lays the pulse, about 30%.
HERMETIC_PALETTE = [
    ("C_NONE",        (0, 0, 0)),
    ("C_PAPER",       (4, 3, 6)),       # the page: a night
    ("C_INK",         (29, 28, 30)),
    ("C_SHADOW",      (1, 1, 2)),
    ("C_FAINT",       (17, 15, 20)),    # folios, captions, the asking voice
    ("C_RULE",        (22, 10, 19)),    # THE SUBTLE LAYER's purple: the pulse's middle
    ("C_MARGIN",      (10, 25, 15)),    # the emerald, lit (#50C878): the marks, and an inscription at its height
    ("C_EDGE",        (8, 6, 10)),
    ("C_EDGE_DARK",   (2, 1, 3)),
    ("C_HIGHLIGHT",   (9, 6, 12)),      # the cursor's bar
    ("C_RING",        (3, 17, 11)),     # an INSCRIPTION: the tablet's emerald (#1F8F5F), breathed by the reader
    ("C_FRAME",       (1, 1, 1)),
    ("C_SLATE",       (5, 3, 7)),       # the cover's boards
    ("C_CHALK",       (31, 30, 30)),    # the cover's lettering
    ("C_CHALK_FAINT", (16, 13, 18)),
    ("C_COVER",       (2, 1, 3)),       # the backdrop, pulsed
]
SUBTLE_RULES, SUBTLE_PALETTE = RULES, PALETTE
BOOKS = {
    "subtle":   {"src": "docs/subtle-layer.md", "prefix": "Subtle", "define": "SUBTLE", "header": "subtle_layer.h",
                 "gfx": "subtle", "icon": "subtle_layer", "title": "THE SUBTLE LAYER", "subtitle": "a trainer's handbook"},
    "hermetic": {"src": "docs/hermetic-layer.md", "prefix": "Hermetic", "define": "HERMETIC", "header": "hermetic_layer.h",
                 "gfx": "hermetic", "icon": "hermetic_layer", "title": "THE HERMETIC LAYER", "subtitle": "SPELLCRAFT"},
}


def use(book):
    """Point the module at one book: its text, its rules and its sixteen colours."""
    global BOOK, SRC, RULES, PALETTE, IDX, RGB8
    BOOK = book
    SRC = os.path.join(ROOT, BOOKS[book]["src"])
    RULES, PALETTE = (SUBTLE_RULES, SUBTLE_PALETTE) if book == "subtle" else (HERMETIC_RULES, HERMETIC_PALETTE)
    IDX = {name: i for i, (name, _) in enumerate(PALETTE)}
    RGB8 = {name: tuple((c << 3) | (c >> 2) for c in v) for name, v in PALETTE}


def inscribe(sections):
    """T-483: each entry's INSCRIPTIONS ('^ '), taken out of the text and kept as a set like the asking voice; 'voices'
    is both, which the reader does not indent. Not in parse(): companion_export reads the '^ ' itself."""
    for s in sections:
        for e in s["entries"]:
            e["inscribed"] = {k for k, q in enumerate(e["paras"]) if q.startswith("^ ")}
            e["paras"] = [q[2:] if k in e["inscribed"] else q for k, q in enumerate(e["paras"])]
            e["text"] = "\n\n".join(e["paras"])
            e["voices"] = e["faint"] | e["inscribed"]
    return sections

# ---------------------------------------------------------------- the text
def parse():
    """genguide's parse, with each entry's @@ SPRITE line taken out and its asking voice ('~ ') kept as a flag."""
    g.SRC = SRC
    sections = g.parse()
    for s in sections:
        for e in s["entries"]:
            paras, e["sprite"], e["caption"] = [], None, ""
            for p in e["text"].split("\n\n"):
                m = re.match(r"^@@ SPRITE \| (\w+) \| (.*)$", p)
                if m:
                    e["sprite"], e["caption"] = m.group(1), m.group(2).strip()
                else:
                    paras.append(p)
            if e["caption"] == "(to come)":
                e["caption"] = ""
            e["faint"] = {k for k, q in enumerate(paras) if q.startswith("~ ")}
            e["paras"] = [q[2:] if q.startswith("~ ") else q for q in paras]
            e["text"] = "\n\n".join(e["paras"])
    return sections


def lines_of(text, w=TW, faint_paras=()):
    """book_reader's Reflow for this book: words wrapped to W; every paragraph after the first opens indented, except
    in an entry with two voices, where each voice starts its own line. Each line keeps its paragraph's voice."""
    out = []
    for k, para in enumerate(text.split("\n\n")):
        faint = k in faint_paras
        line = "   " if (k and not faint_paras) else ""
        for word in para.split():
            cand = line + word if line.strip() == "" else line + " " + word
            if line.strip() and g.width(cand) > w:
                out.append((line, faint))
                line = word
            else:
                line = cand
        if line.strip():
            out.append((line, faint))
    return out


def layout(e):
    """Its pages: the opening spread's right page under the title, then left and right pages of nine lines."""
    title = g.reflow(e["title"], TW, small=True)
    start = 19 + len(title) * 10 + 9
    lines = lines_of(e["text"], faint_paras=e.get("voices", e["faint"]))
    first = (BOTTOM - start) // PITCH
    per = (BOTTOM - TOP) // PITCH
    pages = [lines[:first]] + [lines[i:i + per] for i in range(first, len(lines), per)]
    return title, start, pages


def spreads(e):
    return 1 + -(-(len(layout(e)[2]) - 1) // 2)


NOTES = []


def check(sections):
    saved, g.RULES = g.RULES, []
    bad = [b for b in g.check_text(sections) if "lines, the reader holds" not in b]
    g.RULES = saved
    if len(sections) > 10:
        bad.append("%d sections: the contents page holds 10" % len(sections))
    for s in sections:
        if len(s["entries"]) > 6:
            bad.append("section %s: %d entries, the contents page holds 6" % (s["label"], len(s["entries"])))
        for e in s["entries"]:
            title, start, pages = layout(e)
            if sum(len(p) for p in pages) > g.MAX_LINES:
                bad.append("%s: more lines than the reader holds (%d)" % (e["short"], g.MAX_LINES))
            if len(pages) > 1 and len(pages[-1]) <= 2:
                # T-483: THE HERMETIC LAYER's text is the companion lane's draft, so its short last pages are told,
                # not failed -- the writer fixes them in docs/hermetic-layer.md.
                (NOTES if BOOK == "hermetic" else bad).append("%s: its last page holds %d line(s)" % (e["short"], len(pages[-1])))
            if BOOK == "hermetic":
                if not e["sprite"]:
                    bad.append("%s: no @@ SPRITE line" % e["short"])
            elif e["sprite"] not in sp.SPRITES:
                bad.append("%s: no picture %r in subtle_sprites.py" % (e["short"], e["sprite"]))
            if len(g.reflow(e["caption"], TW, small=True)) > CAPTION_LINES:
                bad.append("%s: its caption takes more than %d small lines" % (e["short"], CAPTION_LINES))
            if len(g.c_string(e["text"]).encode("utf-8")) > 1000:
                bad.append("%s: its text is %d bytes; one game string holds 1024 (preproc), so split the entry"
                           % (e["short"], len(g.c_string(e["text"]).encode("utf-8"))))
            for ch in g.c_string(e["caption"]):
                if ch not in g.CM and ch != " ":
                    bad.append("%s: %r in its caption is not in the charmap" % (e["short"], ch))
            flat = " ".join([e["title"], e["text"], e["caption"]])
            for name, pat, cs, excused in RULES:
                if e["short"] in excused:
                    continue
                for m in re.finditer(pat, flat, 0 if cs else re.I):
                    bad.append("%s breaks %s: %r" % (e["short"], name, flat[max(0, m.start() - 25):m.end() + 25]))
    return bad

# ---------------------------------------------------------------- the pictures
FONT_N = FONT_S = None


def glyphs(img, s, x, y, small, fg):
    """Letters from the game's own font sheets, for the cover and the week's staircase."""
    global FONT_N, FONT_S
    if FONT_N is None:
        FONT_N = Image.open(os.path.join(ENGINE, "graphics/fonts/latin_normal.png"))
        FONT_S = Image.open(os.path.join(ENGINE, "graphics/fonts/latin_small.png"))
    sheet, cw, per, widths = (FONT_S, 8, 32, g.WS) if small else (FONT_N, 16, 16, g.WN)
    src = sheet.load()
    for ch in g.c_string(s):
        code = g.CM.get(ch)
        if code is None:
            continue
        cx, cy = (code % per) * cw, (code // per) * 16
        for gy in range(16):
            for gx in range(cw):
                if src[cx + gx, cy + gy] == 1:
                    sp.px(img, x + gx, y + gy, fg)
        x += widths[code]


def frames_of(key, letters=True):
    """A picture's frames. LETTERS=False leaves out anything set in the game's font (the week's note names): the
    companion holds nothing of Nintendo's, and the font is FireRed's."""
    fn = sp.SPRITES[key]
    if key == "stairs":
        return fn(text=lambda im, s, x, y, small, fg, shadow: glyphs(im, s, x, y, small, fg)) if letters else fn()
    return fn()


def indexed(rgb, w=None, h=None, fill="C_PAPER", role=None):
    """An RGB picture as palette roles, padded to whole tiles: the PNG the build turns into 4bpp."""
    role = role or {v: k for k, v in RGB8.items()}
    w = w or -(-rgb.width // 8) * 8
    h = h or -(-rgb.height // 8) * 8
    out = Image.new("P", (w, h), IDX[fill])
    out.putpalette([v for _, c in PALETTE for v in RGB8[_]] + [0] * (768 - 48))
    ox, oy = (w - rgb.width) // 2, (h - rgb.height) // 2
    src = rgb.load()
    for y in range(rgb.height):
        for x in range(rgb.width):
            c = src[x, y]
            name = SPRITE_ROLE.get(c) or role.get(c)
            if name is None:
                raise SystemExit("gensubtle: a picture uses %s, which is no palette role" % (c,))
            out.putpixel((ox + x, oy + y), IDX[name])
    return out


def cover(letters=True):
    """The cover (240x160, the whole window): the boards, the title in the game's font, the seam on a plate, and
    the six clair glyphs a shade off the boards -- there for a player who knows to look. No byline (the user)."""
    im = Image.new("RGB", (240, 160), RGB8["C_COVER"])
    d = ImageDraw.Draw(im)
    d.rectangle((50, 5, 191, 154), fill=RGB8["C_EDGE_DARK"])                 # the pages beneath
    d.rectangle((48, 4, 188, 152), fill=RGB8["C_SLATE"])                     # the boards
    d.rectangle((48, 4, 53, 152), fill=RGB8["C_EDGE_DARK"])                  # the spine
    d.rectangle((58, 8, 184, 148), outline=RGB8["C_RULE"])
    title, sub = "THE SUBTLE LAYER", "a trainer's handbook"
    if letters:                                   # the companion sets its own title: the font is FireRed's
        glyphs(im, title, 121 - g.width(title) // 2, 12, False, RGB8["C_CHALK"])
        glyphs(im, sub, 121 - g.width(sub, True) // 2, 27, True, RGB8["C_CHALK_FAINT"])
    plate = frames_of("seam")[0].crop((9, 0, 85, 84))   # narrowed (the user, 2026-10-20), so the glyphs sit clear of it
    d.rectangle((81, 44, 81 + plate.width + 3, 44 + plate.height + 3), outline=RGB8["C_RULE"])
    im.paste(plate, (83, 46))
    faint = RGB8["C_EDGE"]
    for k, fn in enumerate(sp.CLAIR_GLYPHS):
        x = 59 if k < 3 else 163
        fn(im, x, 50 + (k % 3) * 30, c=faint)
    return im


def icon():
    """The bag's icon (24x24): a closed book in the boards' colours, a line of the hue down its spine."""
    im = Image.new("RGB", (24, 24), RGB8["C_NONE"])
    d = ImageDraw.Draw(im)
    d.rectangle((5, 3, 19, 21), fill=RGB8["C_SLATE"], outline=RGB8["C_INK"])
    d.rectangle((5, 3, 7, 21), fill=RGB8["C_RULE"])
    d.line((10, 8, 16, 8), fill=RGB8["C_CHALK"])
    d.line((10, 11, 15, 11), fill=RGB8["C_CHALK_FAINT"])
    return im


def placeholder():
    """T-483: the one picture every HERMETIC LAYER entry shows until its own is drawn (51 are named, none drawn): an
    empty plate on the page, a hairline frame in the rule's purple and a small emerald mark at its heart. Plain on
    purpose -- it says a picture belongs here, not what it is."""
    im = Image.new("RGB", (PIC_W, PIC_H), RGB8["C_PAPER"])
    d = ImageDraw.Draw(im)
    d.rectangle((6, 4, PIC_W - 7, PIC_H - 5), outline=RGB8["C_RULE"])
    d.rectangle((8, 6, PIC_W - 9, PIC_H - 7), outline=RGB8["C_EDGE"])
    cx, cy = PIC_W // 2, PIC_H // 2
    d.polygon([(cx, cy - 6), (cx + 5, cy), (cx, cy + 6), (cx - 5, cy)], outline=RGB8["C_RING"])
    return im


def cover_hermetic(letters=True):
    """T-483: THE HERMETIC LAYER's cover (240x160): night boards, the title in the game's font, and a green tablet with
    two triangles on it, one pointing up and one down. No byline."""
    im = Image.new("RGB", (240, 160), RGB8["C_COVER"])
    d = ImageDraw.Draw(im)
    d.rectangle((50, 5, 191, 154), fill=RGB8["C_EDGE_DARK"])
    d.rectangle((48, 4, 188, 152), fill=RGB8["C_SLATE"])
    d.rectangle((48, 4, 53, 152), fill=RGB8["C_EDGE_DARK"])
    d.rectangle((58, 8, 184, 148), outline=RGB8["C_RULE"])
    title, sub = BOOKS["hermetic"]["title"], BOOKS["hermetic"]["subtitle"]
    if letters:
        glyphs(im, title, 121 - g.width(title) // 2, 12, False, RGB8["C_CHALK"])
        glyphs(im, sub, 121 - g.width(sub, True) // 2, 27, True, RGB8["C_CHALK_FAINT"])
    x0, y0, x1, y1 = 93, 50, 149, 138                    # the tablet, its head rounded off
    d.rectangle((x0, y0 + 6, x1, y1), fill=RGB8["C_EDGE_DARK"], outline=RGB8["C_RING"])
    d.pieslice((x0, y0, x1, y0 + 12), 180, 360, fill=RGB8["C_EDGE_DARK"], outline=RGB8["C_RING"])
    d.line((x0 + 1, y0 + 6, x1 - 1, y0 + 6), fill=RGB8["C_EDGE_DARK"])
    cx = (x0 + x1) // 2
    d.polygon([(cx, 66), (cx + 14, 90), (cx - 14, 90)], outline=RGB8["C_MARGIN"])     # above
    d.line((x0 + 8, 94, x1 - 8, 94), fill=RGB8["C_RING"])
    d.polygon([(cx, 122), (cx + 14, 98), (cx - 14, 98)], outline=RGB8["C_RING"])      # so below
    return im


def icon_hermetic():
    """The bag's icon (24x24): a closed book on the night boards, the tablet's emerald down its spine."""
    im = Image.new("RGB", (24, 24), RGB8["C_NONE"])
    d = ImageDraw.Draw(im)
    d.rectangle((5, 3, 19, 21), fill=RGB8["C_SLATE"], outline=RGB8["C_INK"])
    d.rectangle((5, 3, 7, 21), fill=RGB8["C_RING"])
    d.polygon([(13, 7), (16, 12), (10, 12)], outline=RGB8["C_MARGIN"])
    d.line((10, 15, 16, 15), fill=RGB8["C_CHALK_FAINT"])
    return im


def pictures(sections):
    if BOOK == "hermetic":
        return ["placeholder"]
    keys = []
    for s in sections:
        for e in s["entries"]:
            if e["sprite"] not in keys:
                keys.append(e["sprite"])
    return keys

# ---------------------------------------------------------------- the C the reader prints
def header(sections, keys, nframes):
    b = BOOKS[BOOK]
    P, D = b["prefix"], b["define"]
    out = ["// Generated by DAEMONS tools/gensubtle.py from %s -- edit those, not this." % b["src"],
           "// %s: %s. DRAFT WORDING, every string, until the user approves it on the private"
           % ("T-423" if BOOK == "subtle" else "T-483", b["title"]),
           "// field-test page. Its rules are in %s's header." % b["src"], ""]
    n = sum(len(s["entries"]) for s in sections)
    out += ["#define %s_SECTIONS %d" % (D, len(sections)), "#define %s_ENTRIES  %d" % (D, n),
            "#define %s_PICTURES %d" % (D, len(keys)), "",
            "#ifndef GUARD_LAYER_BOOK_TYPES   // one set of types for every book this tool writes (T-483)",
            "#define GUARD_LAYER_BOOK_TYPES",
            "struct SubtleSection { const u8 *label; const u8 *heading; u8 first; u8 count; };",
            "struct SubtleEntry { const u8 *shortTitle; const u8 *title; const u8 *text; const u8 *caption; "
            "u8 picture; u16 faint; u16 folio; u16 inscribed; };",
            "struct SubtlePicture { const u32 *frame[3]; u8 w; u8 h; u8 frames; };",
            "#endif", "",
            "static const u16 s%sPal[16] =" % P, "{"]
    out += ["    [%s] = RGB(%d, %d, %d)," % (name, *c) for name, c in PALETTE]
    out += ["};", "", 'static const u32 s%sCover[] = INCBIN_U32("graphics/book/%s/cover.4bpp");' % (P, b["gfx"])]
    for key in keys:
        for f in range(nframes[key]):
            out.append('static const u32 s%sPic_%s_%d[] = INCBIN_U32("graphics/book/%s/%s_%d.4bpp");'
                       % (P, key, f, b["gfx"], key, f))
    out += ["", "static const struct SubtlePicture s%sPictures[%s_PICTURES] =" % (P, D), "{"]
    for key in keys:
        fr = ["s%sPic_%s_%d" % (P, key, f) for f in range(nframes[key])] + ["NULL"] * (3 - nframes[key])
        out.append("    { { %s }, %d, %d, %d },   // %s" % (", ".join(fr), PIC_W, PIC_H, nframes[key], key))
    out += ["};", ""]
    k, folio = 0, 2
    rows = []
    for i, s in enumerate(sections):
        out.append('static const u8 s%sLabel_%d[] = _("%s");' % (P, i, g.c_string(s["label"])))
        out.append('static const u8 s%sHeading_%d[] = _("%s");' % (P, i, g.c_string(s["heading"])))
        for e in s["entries"]:
            out.append('static const u8 s%sShort_%d[] = _("%s");' % (P, k, g.c_string(e["short"])))
            out.append('static const u8 s%sTitle_%d[] = _("%s");' % (P, k, g.c_string(e["title"])))
            out.append('static const u8 s%sText_%d[] = _("%s");' % (P, k, g.c_string(e["text"])))
            out.append('static const u8 s%sCaption_%d[] = _("%s");' % (P, k, g.c_string(e["caption"])))
            mask = sum(1 << p for p in e["faint"])
            ins = sum(1 << p for p in e.get("inscribed", ()))
            if mask >= 1 << 16 or ins >= 1 << 16:
                raise SystemExit("gensubtle: %s's voices reach past paragraph 16" % e["short"])
            pic = 0 if BOOK == "hermetic" else keys.index(e["sprite"])
            row = "    { s%sShort_%d, s%sTitle_%d, s%sText_%d, s%sCaption_%d, %d, 0x%04X, %d" % (
                P, k, P, k, P, k, P, k, pic, mask, folio)
            rows.append(row + (", 0x%04X },   // %s" % (ins, e["sprite"]) if BOOK == "hermetic" else " },"))
            folio += 2 * spreads(e)
            k += 1
        out.append("")
    out += ["static const struct SubtleSection s%sSections[%s_SECTIONS] =" % (P, D), "{"]
    k = 0
    for i, s in enumerate(sections):
        out.append("    { s%sLabel_%d, s%sHeading_%d, %d, %d }," % (P, i, P, i, k, len(s["entries"])))
        k += len(s["entries"])
    out += ["};", "", "static const struct SubtleEntry s%sEntries[%s_ENTRIES] =" % (P, D), "{"] + rows + ["};"]
    return "\n".join(out) + "\n"

# ---------------------------------------------------------------- the companion's copy (tools/companion_export.py)
def subtle_book():
    """The book for the companion's library, in the game's order: each paragraph plain text, the asking voice marked,
    each entry's picture by key and its frame count (the phone cannot list the art), and as 'labels' the words
    the game letters onto a picture (the week's notes on its steps, C to B), since the art carries no font. DRAFT, as in the game."""
    use("subtle")
    out = []
    for s in parse():
        out.append({"label": s["label"], "heading": s["heading"], "entries": [
            {"short": e["short"], "title": e["title"], "picture": e["sprite"],
             "frames": len(frames_of(e["sprite"], letters=False)), "caption": e["caption"],
             "paragraphs": [{"text": p, "voice": "asking" if k in e["faint"] else "telling"}
                            for k, p in enumerate(e["paras"])],
             **({"labels": list("CDEFGAB")} if e["sprite"] == "stairs" else {})}
            for e in s["entries"]]})
    return {"title": "THE SUBTLE LAYER", "subtitle": "a trainer's handbook", "draft": True, "sections": out}


def subtle_images():
    """{name: picture} for the companion: each picture as the game draws it (native size, RGB), its frames numbered,
    and the cover. RGB on purpose: the page colour is part of the picture. Nothing in them is set in the game's font
    (FireRed's): the cover's title and the week's note names are left for the app to set in its own type."""
    use("subtle")
    out = {}
    for key in pictures(parse()):
        for f, fr in enumerate(frames_of(key, letters=False)):
            out["subtle_%s_%d.png" % (key, f)] = fr
    out["subtle_cover.png"] = cover(letters=False)
    return out


# ---------------------------------------------------------------- report, or write
def run(book):
    use(book)
    b = BOOKS[book]
    sections = parse()
    if book == "hermetic":
        inscribe(sections)
    bad = check(sections)
    keys = pictures(sections)
    nframes = {k: 1 for k in keys} if book == "hermetic" else {k: len(frames_of(k)) for k in keys}
    n = sum(len(s["entries"]) for s in sections)
    total = sum(spreads(e) for s in sections for e in s["entries"])
    print("gensubtle %s: %d sections, %d entries, %d pictures (%d frames), %d spreads"
          % (book, len(sections), n, len(keys), sum(nframes.values()), total))
    if book == "hermetic":
        named = {e["sprite"] for s in sections for e in s["entries"]}
        print("  %d pictures named, none drawn yet: every entry shows the placeholder frame" % len(named))
    for note in NOTES:
        print("  note: " + note)
    del NOTES[:]
    if bad:
        print("\n".join(bad))
        return False
    print("  every line fits and every rule holds")
    if not WRITE:
        return True
    gfx = os.path.join(ENGINE, "graphics/book", b["gfx"])
    os.makedirs(gfx, exist_ok=True)
    if book == "hermetic":
        indexed(placeholder(), PIC_W, PIC_H).save(os.path.join(gfx, "placeholder_0.png"))
        indexed(cover_hermetic(), 240, 160, fill="C_COVER").save(os.path.join(gfx, "cover.png"))
        ic = icon_hermetic()
    else:
        for key in keys:
            for f, fr in enumerate(frames_of(key)):
                indexed(fr, PIC_W, PIC_H).save(os.path.join(gfx, "%s_%d.png" % (key, f)))
        indexed(cover(), 240, 160, fill="C_COVER").save(os.path.join(gfx, "cover.png"))
        ic = icon()
    indexed(ic, 24, 24, fill="C_NONE").save(os.path.join(ENGINE, "graphics/items/icons/%s.png" % b["icon"]))
    with open(os.path.join(ENGINE, "graphics/items/icon_palettes/%s.pal" % b["icon"]), "w", newline="") as f:
        f.write("JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % RGB8[n] for n, _ in PALETTE))
    with open(os.path.join(ENGINE, "src/data", b["header"]), "w", encoding="utf-8") as f:
        f.write(header(sections, keys, nframes))
    print("  wrote src/data/%s, %d pictures, the cover and the icon into %s" % (b["header"], sum(nframes.values()), ENGINE))
    return True


def main():
    ok = True
    for book in ([ONLY] if ONLY else list(BOOKS)):
        ok = run(book) and ok
    use("subtle")
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
