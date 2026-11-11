#!/usr/bin/env python3
"""The game's three books as PDFs, to read away from the game (the user, 2026-10-30: "do all 3 of our books also have
PDF versions in the repo?? I think having them in a subfolder would be good -- like: /docs/books").

    python3 tools/bookpdf.py               # build each book's pages and say whether its file is current
    python3 tools/bookpdf.py --write       # print the books whose sources changed since they were printed
    python3 tools/bookpdf.py --write --force       # print them all
    python3 tools/bookpdf.py --html DIR    # the pages before printing, to look at in a browser
    python3 tools/bookpdf.py --review DIR  # T-519: the torn book's three readings, and all three side by side

WHAT IT WRITES, in docs/books/
  guide.pdf              THE PROGRAMMER'S GUIDE TO THE HUMAN MIND: docs/guide.md, read by genguide's own parse
  the-subtle-layer.pdf   THE SUBTLE LAYER: docs/subtle-layer.md, read by gensubtle's, each entry with its picture
  the-vault.zip          sealed (the user, 2026-10-30): a zip with a password, which may or may not hold the third book.
                         The key is its author's name as the book's own warning gives it, in title case with a space,
                         so it is written nowhere but in the book. docs/books/README.md tells the rumour, and the hint.
  the-second-vault.zip   sealed (the user, 2026-11-05: "seal them like the vault"): THE EUDAIMON LAYER, the torn book's
                         dawn half. Its key is its reader as its blessing names her, "The Lark".
  the-third-vault.zip    sealed the same day: THE UNITY BOOK, the book mended. Its key is both readers, as its
                         attestation names them, "Hatter and Lark".

REVIEW (T-519, the user, 2026-11-05: "the same book, written by different authors' view points"): --review DIR prints
THE HERMETIC LAYER, THE EUDAIMON LAYER and THE UNITY BOOK unsealed, and one-book-three-readings.pdf with the three side
by side, entry against entry, as the approved contents align them. Only into DIR -- docs/private/, never docs/books/,
where all three are sealed.

Each book is printed as the game prints it: its sections and entries in order, the asking voice faint, an inscription
in the tablet's emerald, every picture at whole-pixel scale. The covers carry no lettering of the game's (the font is
Nintendo's): the GUIDE and THE SUBTLE LAYER use the wiki's lettered covers (wiki/covers.py), and the third is lettered
here the same way. Every word is the game's DRAFT, and each book says so on its second page.

HOW IT PRINTS. Google Chrome prints the page on A5 (as tools/manual.py does), twice: the first print says which page
each entry landed on, the second puts those numbers in the contents. PyMuPDF then stamps the foot on every page but the
cover and keeps a hash of the page in the PDF's keywords (the vault's, in the zip's comment) -- which is how this
knows, without printing, whether a book on disk is current. Chrome's PDF and the zip's encryption are never byte-for-
byte the same twice, so a book is printed again only when its hash moves.
"""
import base64, html as H, hashlib, io, os, re, subprocess, sys, tempfile, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "docs/books")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PIC_SCALE = 3                     # nearest-neighbour, so no PDF reader smooths a pixel
VAULT_INSIDE = "sealed.pdf"       # the name a closed zip shows: it says nothing of what is inside

sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "wiki"))
import genguide                   # noqa: E402
import gensubtle                  # noqa: E402
import covers                     # noqa: E402  the wiki's cover lettering: Menlo, letter-spaced
from PIL import Image, ImageDraw  # noqa: E402

BOOKS = {
    "guide": {"file": "guide.pdf", "title": "The Programmer's Guide to the Human Mind", "by": "Christopher Art Hicks",
              "src": "docs/guide.md", "night": "#16212b", "accent": "#2f6f8f", "foot": "THE PROGRAMMER'S GUIDE"},
    "subtle": {"file": "the-subtle-layer.pdf", "title": "The Subtle Layer", "sub": "a USER's handbook",
               "src": "docs/subtle-layer.md", "night": "#1d1424", "accent": "#8a5cc8", "foot": "THE SUBTLE LAYER"},
    "hermetic": {"file": "the-vault.zip", "title": "The Hermetic Layer", "sub": "SPELLCRAFT",
                 "src": "docs/hermetic-layer.md", "night": "#0c1712", "accent": "#1f8f5f", "foot": "THE HERMETIC LAYER"},
    #  T-519: the torn book's other two readings, sealed as the night half is (the user, 2026-11-05)
    "eudaimon": {"file": "the-second-vault.zip", "review": "the-eudaimon-layer.pdf", "title": "The Eudaimon Layer",
                 "sub": "A BLESSING", "src": "docs/eudaimon-layer.md", "night": "#0f1d3a", "accent": "#2f62c8",
                 "foot": "THE EUDAIMON LAYER"},
    "unity": {"file": "the-third-vault.zip", "review": "the-unity-book.pdf", "title": "The Unity Book",
              "sub": "AN ATTESTATION", "src": "docs/unity-book.md", "night": "#1f1c18", "accent": "#a8842c",
              "foot": "THE UNITY BOOK"},
}
REVIEW = {k: BOOKS[k] for k in ("eudaimon", "unity")}  # the readings with no art of their own on the page yet
OPENS = ("hermetic", "eudaimon", "unity")       # each opens with its warning, blessing or attestation, before the contents


def meta(book):
    return BOOKS.get(book) or REVIEW[book]


def data_uri(im):
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def scaled(im, k=PIC_SCALE):
    return im.resize((im.width * k, im.height * k), Image.NEAREST)

# ---------------------------------------------------------------- the books, as sections of entries
def guide_book():
    sections = []
    for s in genguide.parse():
        sections.append({"label": s["label"], "heading": s["heading"], "entries": [
            {"short": e["short"], "title": e["title"], "picture": None, "caption": "",
             "paras": [(" ".join(p), "telling") for p in e["paras"] if p]} for e in s["entries"]]})
    import gbaqr                  # its last page is a QR code in the game; here, the link
    sections[-1]["entries"][-1]["link"] = dict(gbaqr.CODES)["Guide"]
    return sections


def layer_book(book):
    gensubtle.use("hermetic" if book in REVIEW else book)
    if book in REVIEW:
        gensubtle.SRC = os.path.join(ROOT, REVIEW[book]["src"])
    sections = gensubtle.parse()
    gensubtle.inscribe(sections)
    out = []
    for s in sections:
        entries = []
        for e in s["entries"]:
            pic = None
            if book == "subtle":
                pic = gensubtle.frames_of(e["sprite"], letters=False)[0]
            voice = lambda k: "asking" if k in e["faint"] else "inscription" if k in e["inscribed"] else "telling"
            paras = []
            for k, p in enumerate(e["paras"]):
                if p.startswith("% "):      # the observer's line: three wordings, by the lead daemon's SPIRITS
                    paras.append((" / ".join(w.strip() for w in p[2:].split(" | ")), "observer"))
                else:
                    paras.append((p, voice(k)))
            entries.append({"short": e["short"], "title": e["title"], "picture": pic, "caption": e["caption"],
                            "paras": paras})
        out.append({"label": s["label"], "heading": s["heading"], "entries": entries})
    return out


def vault_key(book, sections):
    """A vault's key, read from the book's own first page, so it is written nowhere else (title case, a space):
    the night half's, the name its warning gives ("OSRIC HATTER read it", T-519; it was "set it down"); the dawn
    half's, its reader as its blessing names her ("A LARK read it": "The Lark"); the mended book's, both readers as
    its attestation names them ("by a hatter, and one at first light by a lark": "Hatter and Lark")."""
    text = " ".join(p for p, _ in sections[0]["entries"][0]["paras"])
    if book == "origin":
        # T-533: THE ORIGIN OF A DAEMON's recording opens with the book's own last word, from its last page -- which a
        # device holds only once every chapter has come back (the companion's keyOfOrigin reads it the same way)
        last = " ".join(p for p, _ in sections[-1]["entries"][-1]["paras"])
        m = re.search(r"\bThat is how I (\w+)\.\s*$", last)
        if not m:
            raise SystemExit("bookpdf: THE ORIGIN OF A DAEMON's last line no longer ends its book; its recording has no key")
        return m.group(1).title()
    if book == "hermetic":
        m = re.search(r"\b([A-Z]{2,}) ([A-Z]{2,}) (?:set it down|read it)\b", text)
        key = m and "%s %s" % (m.group(1).title(), m.group(2).title())
    elif book == "eudaimon":
        m = re.search(r"\bA ([A-Z]{2,}) read it\b", text)
        key = m and "The %s" % m.group(1).title()
    else:
        m = re.search(r"\bby an? (\w+), and one [^.]*? by an? (\w+)\.", text)
        key = m and "%s and %s" % (m.group(1).title(), m.group(2).title())
    if not key:
        raise SystemExit("bookpdf: %s's first page no longer names its reader; its vault has no key" % book)
    return key


def cover(book):
    if book in ("guide", "subtle"):
        return Image.open(os.path.join(ROOT, "wiki/images/%s_cover.png" % book)).convert("RGB")
    gensubtle.use("hermetic")
    if book in REVIEW:              # no art yet: the book's own colour, lettered as the others are
        b = REVIEW[book]
        im = Image.new("RGB", (132 * covers.K, 160 * covers.K), b["night"])
        d = ImageDraw.Draw(im)
        covers.spaced(d, b["title"].upper(), covers.font(19), 34, im.width, "#f2efe8", 1.5)
        covers.spaced(d, b["sub"], covers.font(16, 2), 75, im.width, b["accent"], 2)
        return im
    im = scaled(gensubtle.cover_hermetic(letters=False).crop((54, 0, 186, 160)), covers.K)
    d = ImageDraw.Draw(im)
    c = gensubtle.RGB8
    covers.spaced(d, "THE HERMETIC LAYER", covers.font(19), 34, im.width, "#%02x%02x%02x" % c["C_CHALK"], 1.5)
    covers.spaced(d, "SPELLCRAFT", covers.font(16, 2), 75, im.width, "#%02x%02x%02x" % c["C_MARGIN"], 2)
    return im

# ---------------------------------------------------------------- the page
CSS = """
@page { size: 148mm 210mm; margin: 15mm 14mm 18mm 14mm; }
@page cover { margin: 0; }
:root { --ink: #17161b; --paper: #ffffff; --soft: #6a6874; --rule: #d9d6cd; --emerald: #1f8f5f; --pulse: #b0569e; }
html { font-size: 10pt; }
body { margin: 0; color: var(--ink); background: var(--paper); line-height: 1.5;
       font-family: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif;
       -webkit-print-color-adjust: exact; print-color-adjust: exact; }
h1, h2, .lab, .short, .toc, .front, .cap, .link { font-family: "Avenir Next", "Helvetica Neue", Helvetica, sans-serif; }
img { image-rendering: pixelated; }
a { color: inherit; }

.cover { page: cover; break-after: page; height: 210mm; background: var(--night); display: flex;
         align-items: center; justify-content: center; }
.cover img { width: 112mm; }

.front { break-after: page; padding-top: 40mm; text-align: center; }
.front .t { font-size: 19pt; font-weight: 700; letter-spacing: .02em; line-height: 1.2; }
.front .s { font: italic 12pt "Iowan Old Style", serif; color: var(--soft); margin-top: 2mm; }
.front .by { margin-top: 6mm; font-size: 10pt; letter-spacing: .12em; text-transform: uppercase; }
.front .from { margin-top: 30mm; font-size: 8.5pt; color: var(--soft); line-height: 1.6; }
.front .draft { margin-top: 5mm; font-size: 8pt; color: #9a3b3b; letter-spacing: .06em; }

.toc { break-after: page; }
.toc h1 { font-size: 17pt; margin: 0 0 5mm; color: var(--accent); }
.toc .sec { display: flex; font-weight: 700; font-size: 9pt; margin-top: 3mm; border-bottom: .6pt solid var(--ink);
            padding-bottom: .4mm; }
.toc .ent { display: flex; font-size: 8.4pt; padding-left: 5mm; color: #34333a; line-height: 1.45; }
.toc a { text-decoration: none; display: flex; width: 100%; }
.toc .n { flex: 1; }
.toc .pg { width: 9mm; text-align: right; color: var(--soft); }

.section { break-before: page; }
.lab { font-size: 8pt; font-weight: 600; letter-spacing: .3em; color: var(--accent); text-transform: uppercase; }
.section > h1 { font-size: 18pt; line-height: 1.2; margin: 1.5mm 0 7mm; padding-bottom: 3mm;
                border-bottom: 1.2pt solid var(--accent); }
.entry { margin-bottom: 8mm; }
.short { font-size: 7.5pt; letter-spacing: .22em; color: var(--soft); text-transform: uppercase;
         break-after: avoid; }
.entry h2 { font-size: 12.5pt; margin: .5mm 0 3mm; line-height: 1.25; break-after: avoid; }
figure { margin: 0 0 4mm; text-align: center; break-inside: avoid; }
figure img { width: 56mm; border-radius: 1.5mm; }
.cap { font-size: 7.8pt; color: var(--soft); font-style: italic; margin-top: 1.5mm; }
.epigraph { font-size: 8.5pt; color: var(--soft); font-style: italic; margin: -1mm 0 3mm; }
p { margin: 0 0 2.6mm; text-align: justify; hyphens: auto; orphans: 2; widows: 2; }
p.asking { color: var(--soft); font-style: italic; padding-left: 5mm; }
p.inscription { color: var(--emerald); text-align: center; font-family: "Avenir Next", sans-serif;
                font-weight: 600; font-size: 10.5pt; letter-spacing: .03em; margin: 4mm 6mm; }
.link { font-size: 8.5pt; margin-top: 3mm; }
p.observer { color: var(--accent); font-style: italic; text-align: center; font-size: 9pt; margin: 4mm 4mm; }
.warning { break-after: page; padding-top: 22mm; }
.warning h2 { color: var(--pulse); }
"""


def esc(s):
    return H.escape(s, quote=True)


def entry_html(e, eid):
    out = ['<div class="entry" id="%s"><div class="short">%s</div><h2>%s</h2>' % (eid, esc(e["short"]), esc(e["title"]))]
    if e["picture"] is not None:
        out.append('<figure><img src="%s" alt="">%s</figure>' % (
            data_uri(scaled(e["picture"])), '<div class="cap">%s</div>' % esc(e["caption"]) if e["caption"] else ""))
    elif e["caption"]:
        out.append('<div class="epigraph">%s</div>' % esc(e["caption"]))
    for text, voice in e["paras"]:
        out.append('<p class="%s">%s</p>' % (voice, esc(text)))
    if e.get("link"):
        out.append('<div class="link">Read it online: <a href="%s">%s</a></div>' % (esc(e["link"]), esc(e["link"])))
    out.append("</div>")
    return "".join(out)


def page_html(book, sections, cover_im, pages=None):
    b = meta(book)
    pages = pages or {}
    ids = {}
    k = 0
    for i, s in enumerate(sections):
        for e in s["entries"]:
            ids[id(e)] = "e%d" % k
            k += 1
    warning = sections[0]["entries"][0] if book in OPENS else None    # it opens with its warning (4.39, rule 4)
    toc = []
    for i, s in enumerate(sections):
        first = ids[id(s["entries"][0])]
        toc.append('<div class="sec"><a href="#%s"><span class="n">%s</span><span class="pg">%s</span></a></div>'
                   % (first, esc(s["heading"]), pages.get(first, "")))
        for e in s["entries"]:
            toc.append('<div class="ent"><a href="#%s"><span class="n">%s</span><span class="pg">%s</span></a></div>'
                       % (ids[id(e)], esc(e["title"]), pages.get(ids[id(e)], "")))
    body = []
    for i, s in enumerate(sections):
        entries = [e for e in s["entries"] if e is not warning]
        if not entries:
            continue
        body.append('<div class="section"><div class="lab">%s</div><h1>%s</h1>' % (esc(s["label"]), esc(s["heading"])))
        body += [entry_html(e, ids[id(e)]) for e in entries]
        body.append("</div>")
    front = ['<div class="front"><div class="t">%s</div>' % esc(b["title"])]
    if b.get("sub"):
        front.append('<div class="s">%s</div>' % esc(b["sub"]))
    if b.get("by"):
        front.append('<div class="by">%s</div>' % esc(b["by"]))
    front.append('<div class="from">A book from <b>DAEMONS: CONTEXT / CONTENT</b>,<br>as the game prints it.</div>'
                 '<div class="draft">DRAFT &middot; every word, until it is approved</div></div>')
    return """<!doctype html><html><head><meta charset="utf-8"><title>%s</title>
<style>:root { --night: %s; --accent: %s; }%s%s</style></head><body>
<div class="cover"><img src="%s" alt=""></div>
%s%s<div class="toc"><h1>Contents</h1>%s</div>
%s
</body></html>""" % (esc(b["title"]), b["night"], b["accent"], CSS,
                     ":root { --emerald: %s; --pulse: %s; }" % (b["accent"], b["accent"]) if book in REVIEW else "",
                     data_uri(cover_im),
                     "".join(front) if not warning else "",
                     '<div class="warning">%s</div>' % entry_html(warning, ids[id(warning)]) if warning else "",
                     "".join(toc), "".join(body))

# ---------------------------------------------------------------- printing
def chrome(html_path, pdf_path):
    if not os.path.exists(CHROME):
        raise SystemExit("bookpdf: Google Chrome is not at " + CHROME)
    r = subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer",
                        "--generate-pdf-document-outline", "--print-to-pdf=" + pdf_path, "file://" + html_path],
                       capture_output=True, text=True, timeout=300)
    if not os.path.exists(pdf_path):
        raise SystemExit("bookpdf: Chrome printed nothing\n" + r.stderr[-2000:])


def landing_pages(pdf_path):
    """{entry id: page number} from the contents' links in a first print."""
    import fitz
    out = {}
    with fitz.open(pdf_path) as doc:
        for p in range(min(8, len(doc))):
            for link in doc[p].get_links():
                if link.get("nameddest") and link.get("page", -1) >= 0:
                    out.setdefault(link["nameddest"], link["page"] + 1)
    return out


def stamp(pdf_path, out_path, book, digest):
    import fitz
    b = meta(book)
    doc = fitz.open(pdf_path)
    for i, page in enumerate(doc):
        if i == 0:
            continue
        r = page.rect
        y = r.height - 22
        page.insert_text((40, y), b["foot"], fontsize=6.5, fontname="helv", color=(0.45, 0.45, 0.5))
        num = str(i + 1)
        page.insert_text((r.width / 2 - fitz.get_text_length(num, "helv", 7.5) / 2, y), num, fontsize=7.5,
                         fontname="helv", color=(0.1, 0.1, 0.12))
        page.insert_text((r.width - 40 - fitz.get_text_length("DRAFT", "helv", 6.5), y), "DRAFT", fontsize=6.5,
                         fontname="helv", color=(0.45, 0.45, 0.5))
    doc.set_metadata({"title": b["title"], "author": b.get("by", "the DAEMONS project"),
                      "subject": "A book from DAEMONS: CONTEXT / CONTENT, as the game prints it. DRAFT.",
                      "keywords": "sources %s" % digest, "creator": "tools/bookpdf.py", "producer": "Chrome, PyMuPDF"})
    doc.save(out_path, garbage=3, deflate=True)
    doc.close()


def printed_digest(book):
    path = os.path.join(OUT, BOOKS[book]["file"])
    if not os.path.exists(path):
        return None
    if path.endswith(".zip"):
        with zipfile.ZipFile(path) as z:
            m = re.search(r"sources (\w+)", z.comment.decode("utf-8", "replace"))
    else:
        import fitz
        with fitz.open(path) as doc:
            m = re.search(r"sources (\w+)", doc.metadata.get("keywords") or "")
    return m.group(1) if m else None


def seal(pdf_path, zip_path, key, digest):
    """The vault: the book inside under a name that says nothing, the key the author's name, the hash in the comment."""
    with tempfile.TemporaryDirectory(prefix="daemons-vault-") as work:
        inside = os.path.join(work, VAULT_INSIDE)
        os.replace(pdf_path, inside)
        tmp = os.path.join(work, "vault.zip")
        r = subprocess.run(["zip", "-q", "-j", "-X", "-P", key, tmp, inside], capture_output=True, text=True)
        if r.returncode:
            raise SystemExit("bookpdf: zip failed\n" + r.stderr)
        subprocess.run(["zip", "-q", "-z", tmp], input="sources %s\n" % digest, text=True, check=True)
        with zipfile.ZipFile(tmp) as z:                 # it opens with the key, and with nothing else
            z.setpassword(key.encode())
            if z.read(VAULT_INSIDE)[:5] != b"%PDF-":
                raise SystemExit("bookpdf: the vault does not open with its key")
        os.replace(tmp, zip_path)


def build(book):
    sections = guide_book() if book == "guide" else layer_book(book)
    html = page_html(book, sections, cover(book))
    return sections, html, hashlib.sha256(html.encode()).hexdigest()[:16]


def print_book(book, sections, out_path, digest):
    """Two prints (the second with the contents' page numbers), then the foot stamped."""
    n = sum(len(s["entries"]) for s in sections)
    with tempfile.TemporaryDirectory(prefix="daemons-book-") as work:
        html_path = os.path.join(work, "book.html")
        open(html_path, "w", encoding="utf-8").write(page_html(book, sections, cover(book)))
        first = os.path.join(work, "first.pdf")
        chrome(html_path, first)
        pages = landing_pages(first)
        missing = [e for e in ("e%d" % k for k in range(n)) if e not in pages]
        if missing:
            raise SystemExit("bookpdf: %s's first print did not place %s" % (book, ", ".join(missing[:5])))
        open(html_path, "w", encoding="utf-8").write(page_html(book, sections, cover(book), pages))
        second = os.path.join(work, "second.pdf")
        chrome(html_path, second)
        stamp(second, out_path, book, digest)
    import fitz
    with fitz.open(out_path) as doc:
        return len(doc)

# ---------------------------------------------------------------- the three readings, side by side (T-519)
#  Where the mended book joined two entries into one (the approved contents), its one entry spans the halves' two rows.
JOINS = {"ONE": [0, 1, 2, 3, 4, 4], "FOLDS": [0, 1, 2, 3, 4, 4], "LOOP": [0, 1, 2, 2]}

COMPARE_CSS = """
@page { size: 297mm 210mm; margin: 11mm 10mm 13mm 10mm; }
html { font-size: 7.6pt; }
body { margin: 0; color: #17161b; line-height: 1.42; font-family: "Iowan Old Style", Palatino, Georgia, serif;
       -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.head, .sec, .short, .note, .lab { font-family: "Avenir Next", "Helvetica Neue", sans-serif; }
.title { text-align: center; padding-top: 50mm; break-after: page; }
.title h1 { font: 700 22pt "Avenir Next", sans-serif; margin: 0 0 4mm; }
.title p { font-size: 10pt; color: #6a6874; max-width: 170mm; margin: 2mm auto; }
table { width: 100%; border-collapse: collapse; table-layout: fixed; }
thead th { font: 600 8pt "Avenir Next", sans-serif; letter-spacing: .18em; text-transform: uppercase; color: #fff;
           padding: 1.6mm 2mm; }
th.h { background: #1f8f5f; } th.e { background: #2f62c8; } th.u { background: #a8842c; }
tr.sec td { font-weight: 700; font-size: 9.5pt; padding: 4mm 2mm 1mm; border-bottom: 1pt solid #17161b; }
tr.row { break-inside: avoid; }
td { vertical-align: top; padding: 2mm 2.2mm 2.4mm; border-bottom: .5pt solid #d9d6cd; }
td.h { background: #f2f8f4; } td.e { background: #f1f4fb; } td.u { background: #faf6ec; }
td.none { background: #f6f6f6; color: #9a98a2; font-style: italic; }
.short { font-size: 6.4pt; letter-spacing: .2em; color: #6a6874; text-transform: uppercase; }
h2 { font-size: 9pt; margin: .3mm 0 1.4mm; line-height: 1.2; }
p { margin: 0 0 1.4mm; }
p.asking { color: #6a6874; font-style: italic; padding-left: 3mm; }
p.inscription { font-family: "Avenir Next", sans-serif; font-weight: 600; }
td.h p.inscription { color: #1f8f5f; } td.e p.inscription { color: #2f62c8; } td.u p.inscription { color: #8a6a1c; }
p.observer { font-style: italic; color: #4a4852; border-left: 1.5pt solid #a8842c; padding-left: 2mm; }
.note { font-size: 7pt; color: #9a98a2; font-style: italic; }
"""


def compare_html(books):
    """books: {name: sections}; rows aligned section by section, the mended book's joins spanning two rows."""
    def cell(e, cls):
        out = ['<td class="%s"><div class="short">%s</div><h2>%s</h2>' % (cls, esc(e["short"]), esc(e["title"]))]
        out += ['<p class="%s">%s</p>' % (v, esc(t)) for t, v in e["paras"]]
        return "".join(out) + "</td>"
    halves = {s["key"]: s for s in books["hermetic"]}
    dawn = {s["key"]: s for s in books["eudaimon"]}
    rows = []
    for u in books["unity"]:
        k = u["key"]
        h, e = halves.get(k), dawn.get(k)
        rows.append('<tr class="sec"><td>%s</td><td>%s</td><td>%s</td></tr>' % (
            esc(h["heading"]) if h else "", esc(e["heading"]) if e else "", esc(u["heading"])))
        n = max(len(h["entries"]) if h else 0, len(u["entries"]))
        if h and e and len(h["entries"]) != len(e["entries"]):
            raise SystemExit("bookpdf: %s has %d entries in the night half and %d in the dawn half"
                             % (k, len(h["entries"]), len(e["entries"])))
        umap = JOINS.get(k, list(range(n)))
        if h and len(umap) != len(h["entries"]) or max(umap) != len(u["entries"]) - 1:
            raise SystemExit("bookpdf: %s's rows no longer line up with the mended book's contents" % k)
        for i in range(n):
            tds = [cell(h["entries"][i], "h"), cell(e["entries"][i], "e")] if h else \
                  ['<td class="none" colspan="2">Only in the mended book: BALANCE is written between the halves.</td>']
            j = umap[i]
            if i and umap[i - 1] == j:
                tds.append('<td class="u none">Joined into the entry above.</td>')
            else:
                tds.append(cell(u["entries"][j], "u"))
            rows.append('<tr class="row">%s</tr>' % "".join(tds))
    return """<!doctype html><html><head><meta charset="utf-8"><title>One Book, Three Readings</title>
<style>%s</style></head><body>
<div class="title"><h1>One Book, Three Readings</h1>
<p>THE HERMETIC LAYER, read at night; THE EUDAIMON LAYER, read at first light; THE UNITY BOOK, the two mended.</p>
<p>The same sections and the same thirteen spells, entry against entry. Where the mended book joins two entries, it says so.</p>
<p>DRAFT, every word.</p></div>
<table><thead><tr><th class="h">The Hermetic Layer</th><th class="e">The Eudaimon Layer</th><th class="u">The Unity Book</th></tr></thead>
<tbody>%s</tbody></table></body></html>""" % (COMPARE_CSS, "".join(rows))


def review(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    books = {}
    for book, name in (("hermetic", "the-hermetic-layer.pdf"), ("eudaimon", REVIEW["eudaimon"]["review"]),
                       ("unity", REVIEW["unity"]["review"])):
        gensubtle.use("hermetic" if book in REVIEW else book)
        if book in REVIEW:
            gensubtle.SRC = os.path.join(ROOT, REVIEW[book]["src"])
        keys = [s["key"] for s in gensubtle.parse()]
        sections = layer_book(book)
        for s, k in zip(sections, keys):
            s["key"] = k
        books[book] = sections
        n = print_book(book, sections, os.path.join(out_dir, name), "review")
        print("  %s: %d sections, %d entries -> %s (%d pages)" % (
            book, len(sections), sum(len(s["entries"]) for s in sections), os.path.join(out_dir, name), n))
    with tempfile.TemporaryDirectory(prefix="daemons-compare-") as work:
        html_path = os.path.join(work, "compare.html")
        open(html_path, "w", encoding="utf-8").write(compare_html(books))
        raw = os.path.join(work, "compare.pdf")
        chrome(html_path, raw)
        import fitz
        doc = fitz.open(raw)
        for i, page in enumerate(doc):
            if i:
                r = page.rect
                page.insert_text((r.width / 2 - 6, r.height - 16), str(i + 1), fontsize=7, fontname="helv",
                                 color=(0.3, 0.3, 0.35))
        out = os.path.join(out_dir, "one-book-three-readings.pdf")
        doc.save(out, garbage=3, deflate=True)
        print("  side by side -> %s (%d pages)" % (out, len(doc)))
        doc.close()
    return 0


def main():
    args = sys.argv[1:]
    if "--review" in args:
        return review(os.path.abspath(args[args.index("--review") + 1]))
    write, force = "--write" in args, "--force" in args
    html_dir = os.path.abspath(args[args.index("--html") + 1]) if "--html" in args else None
    for book in BOOKS:
        b = BOOKS[book]
        sections, html, digest = build(book)
        n = sum(len(s["entries"]) for s in sections)
        if html_dir:
            os.makedirs(html_dir, exist_ok=True)
            path = os.path.join(html_dir, os.path.splitext(b["file"])[0] + ".html")
            open(path, "w", encoding="utf-8").write(html)
            print("  %s: wrote %s" % (book, path))
            continue
        current = printed_digest(book) == digest
        where = "docs/books/" + b["file"]
        print("  %s: %d sections, %d entries, sources %s; %s is %s" % (
            book, len(sections), n, digest, where,
            "current" if current else "missing" if not os.path.exists(os.path.join(OUT, b["file"])) else "out of date"))
        if not write or (current and not force):
            continue
        with tempfile.TemporaryDirectory(prefix="daemons-book-") as work:
            html_path = os.path.join(work, "book.html")
            open(html_path, "w", encoding="utf-8").write(html)
            first = os.path.join(work, "first.pdf")
            chrome(html_path, first)
            pages = landing_pages(first)
            missing = [e for e in ("e%d" % k for k in range(n)) if e not in pages]
            if missing:
                raise SystemExit("bookpdf: %s's first print did not place %s" % (book, ", ".join(missing[:5])))
            open(html_path, "w", encoding="utf-8").write(page_html(book, sections, cover(book), pages))
            second = os.path.join(work, "second.pdf")
            chrome(html_path, second)
            if landing_pages(second) != pages:
                raise SystemExit("bookpdf: %s's page numbers moved between the two prints" % book)
            done = os.path.join(work, "book.pdf")
            stamp(second, done, book, digest)
            os.makedirs(OUT, exist_ok=True)
            if b["file"].endswith(".zip"):
                seal(done, os.path.join(OUT, b["file"]), vault_key(book, sections), digest)
            else:
                os.replace(done, os.path.join(OUT, b["file"]))
            import fitz
            with fitz.open(second) as doc:
                print("    printed %s: %d pages" % (where, len(doc)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
