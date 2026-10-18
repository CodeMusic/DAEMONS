#!/usr/bin/env python3
"""THE SUBTLE LAYER, in the game and in the companion (T-423; docs/psychic-routines-notes.md D and D2).

    python3 tools/gensubtle.py                       # report: every entry measured, every rule checked
    python3 tools/gensubtle.py --write                # engineGba/src/data/subtle_layer.h and graphics/book/subtle/
    python3 tools/gensubtle.py --write --engine DIR   # the same, into another engine checkout (a worktree)

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
    lines = lines_of(e["text"], faint_paras=e["faint"])
    first = (BOTTOM - start) // PITCH
    per = (BOTTOM - TOP) // PITCH
    pages = [lines[:first]] + [lines[i:i + per] for i in range(first, len(lines), per)]
    return title, start, pages


def spreads(e):
    return 1 + -(-(len(layout(e)[2]) - 1) // 2)


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
                bad.append("%s: its last page holds %d line(s)" % (e["short"], len(pages[-1])))
            if e["sprite"] not in sp.SPRITES:
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
    plate = frames_of("seam")[0]
    d.rectangle((72, 44, 72 + plate.width + 3, 44 + plate.height + 3), outline=RGB8["C_RULE"])
    im.paste(plate, (74, 46))
    faint = RGB8["C_EDGE"]
    for k, fn in enumerate(sp.CLAIR_GLYPHS):
        x = 61 if k < 3 else 162
        fn(im, x, 52 + (k % 3) * 30, c=faint)
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


def pictures(sections):
    keys = []
    for s in sections:
        for e in s["entries"]:
            if e["sprite"] not in keys:
                keys.append(e["sprite"])
    return keys

# ---------------------------------------------------------------- the C the reader prints
def header(sections, keys, nframes):
    out = ["// Generated by DAEMONS tools/gensubtle.py from docs/subtle-layer.md -- edit those, not this.",
           "// T-423: THE SUBTLE LAYER. DRAFT WORDING, every string, until the user approves it on the private",
           "// field-test page. Its rules are in docs/subtle-layer.md's header.", ""]
    n = sum(len(s["entries"]) for s in sections)
    out += ["#define SUBTLE_SECTIONS %d" % len(sections), "#define SUBTLE_ENTRIES  %d" % n,
            "#define SUBTLE_PICTURES %d" % len(keys), "",
            "struct SubtleSection { const u8 *label; const u8 *heading; u8 first; u8 count; };",
            "struct SubtleEntry { const u8 *shortTitle; const u8 *title; const u8 *text; const u8 *caption; "
            "u8 picture; u16 faint; u16 folio; };",
            "struct SubtlePicture { const u32 *frame[3]; u8 w; u8 h; u8 frames; };", "",
            "static const u16 sSubtlePal[16] =", "{"]
    out += ["    [%s] = RGB(%d, %d, %d)," % (name, *c) for name, c in PALETTE]
    out += ["};", "", 'static const u32 sSubtleCover[] = INCBIN_U32("graphics/book/subtle/cover.4bpp");']
    for key in keys:
        for f in range(nframes[key]):
            out.append('static const u32 sSubtlePic_%s_%d[] = INCBIN_U32("graphics/book/subtle/%s_%d.4bpp");'
                       % (key, f, key, f))
    out += ["", "static const struct SubtlePicture sSubtlePictures[SUBTLE_PICTURES] =", "{"]
    for key in keys:
        fr = ["sSubtlePic_%s_%d" % (key, f) for f in range(nframes[key])] + ["NULL"] * (3 - nframes[key])
        out.append("    { { %s }, %d, %d, %d },   // %s" % (", ".join(fr), PIC_W, PIC_H, nframes[key], key))
    out += ["};", ""]
    k, folio = 0, 2
    rows = []
    for i, s in enumerate(sections):
        out.append('static const u8 sSubtleLabel_%d[] = _("%s");' % (i, g.c_string(s["label"])))
        out.append('static const u8 sSubtleHeading_%d[] = _("%s");' % (i, g.c_string(s["heading"])))
        for e in s["entries"]:
            out.append('static const u8 sSubtleShort_%d[] = _("%s");' % (k, g.c_string(e["short"])))
            out.append('static const u8 sSubtleTitle_%d[] = _("%s");' % (k, g.c_string(e["title"])))
            out.append('static const u8 sSubtleText_%d[] = _("%s");' % (k, g.c_string(e["text"])))
            out.append('static const u8 sSubtleCaption_%d[] = _("%s");' % (k, g.c_string(e["caption"])))
            mask = sum(1 << p for p in e["faint"])
            if mask >= 1 << 16:
                raise SystemExit("gensubtle: %s's asking voice reaches past paragraph 16" % e["short"])
            rows.append("    { sSubtleShort_%d, sSubtleTitle_%d, sSubtleText_%d, sSubtleCaption_%d, %d, 0x%04X, %d },"
                        % (k, k, k, k, keys.index(e["sprite"]), mask, folio))
            folio += 2 * spreads(e)
            k += 1
        out.append("")
    out += ["static const struct SubtleSection sSubtleSections[SUBTLE_SECTIONS] =", "{"]
    k = 0
    for i, s in enumerate(sections):
        out.append("    { sSubtleLabel_%d, sSubtleHeading_%d, %d, %d }," % (i, i, k, len(s["entries"])))
        k += len(s["entries"])
    out += ["};", "", "static const struct SubtleEntry sSubtleEntries[SUBTLE_ENTRIES] =", "{"] + rows + ["};"]
    return "\n".join(out) + "\n"

# ---------------------------------------------------------------- the companion's copy (tools/companion_export.py)
def subtle_book():
    """The book for the companion's library, in the game's order: each paragraph plain text, the asking voice marked,
    each entry's picture by key and its frame count (the phone cannot list the art). DRAFT, as in the game."""
    out = []
    for s in parse():
        out.append({"label": s["label"], "heading": s["heading"], "entries": [
            {"short": e["short"], "title": e["title"], "picture": e["sprite"],
             "frames": len(frames_of(e["sprite"], letters=False)), "caption": e["caption"],
             "paragraphs": [{"text": p, "voice": "asking" if k in e["faint"] else "telling"}
                            for k, p in enumerate(e["paras"])]}
            for e in s["entries"]]})
    return {"title": "THE SUBTLE LAYER", "subtitle": "a trainer's handbook", "draft": True, "sections": out}


def subtle_images():
    """{name: picture} for the companion: each picture as the game draws it (native size, RGB), its frames numbered,
    and the cover. RGB on purpose: the page colour is part of the picture. Nothing in them is set in the game's font
    (FireRed's): the cover's title and the week's note names are left for the app to set in its own type."""
    out = {}
    for key in pictures(parse()):
        for f, fr in enumerate(frames_of(key, letters=False)):
            out["subtle_%s_%d.png" % (key, f)] = fr
    out["subtle_cover.png"] = cover(letters=False)
    return out


# ---------------------------------------------------------------- report, or write
def main():
    sections = parse()
    bad = check(sections)
    keys = pictures(sections)
    nframes = {k: len(frames_of(k)) for k in keys}
    n = sum(len(s["entries"]) for s in sections)
    total = sum(spreads(e) for s in sections for e in s["entries"])
    print("gensubtle: %d sections, %d entries, %d pictures (%d frames), %d spreads"
          % (len(sections), n, len(keys), sum(nframes.values()), total))
    if bad:
        print("\n".join(bad))
        sys.exit(1)
    print("every line fits and every rule holds")
    if not WRITE:
        return
    gfx = os.path.join(ENGINE, "graphics/book/subtle")
    os.makedirs(gfx, exist_ok=True)
    for key in keys:
        for f, fr in enumerate(frames_of(key)):
            indexed(fr, PIC_W, PIC_H).save(os.path.join(gfx, "%s_%d.png" % (key, f)))
    indexed(cover(), 240, 160, fill="C_COVER").save(os.path.join(gfx, "cover.png"))
    indexed(icon(), 24, 24, fill="C_NONE").save(os.path.join(ENGINE, "graphics/items/icons/subtle_layer.png"))
    with open(os.path.join(ENGINE, "graphics/items/icon_palettes/subtle_layer.pal"), "w", newline="") as f:
        f.write("JASC-PAL\r\n0100\r\n16\r\n" + "".join("%d %d %d\r\n" % RGB8[n] for n, _ in PALETTE))
    with open(os.path.join(ENGINE, "src/data/subtle_layer.h"), "w", encoding="utf-8") as f:
        f.write(header(sections, keys, nframes))
    print("wrote src/data/subtle_layer.h, %d pictures, the cover and the icon into %s" % (sum(nframes.values()), ENGINE))


if __name__ == "__main__":
    main()
