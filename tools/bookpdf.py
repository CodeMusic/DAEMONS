#!/usr/bin/env python3
"""The game's three books as PDFs, to read away from the game (the user, 2026-10-30: "do all 3 of our books also have
PDF versions in the repo?? I think having them in a subfolder would be good -- like: /docs/books").

    python3 tools/bookpdf.py               # build each book's pages and say whether its file is current
    python3 tools/bookpdf.py --write       # print the books whose sources changed since they were printed
    python3 tools/bookpdf.py --write --force       # print them all
    python3 tools/bookpdf.py --html DIR    # the pages before printing, to look at in a browser

WHAT IT WRITES, in docs/books/
  guide.pdf              THE PROGRAMMER'S GUIDE TO THE HUMAN MIND: docs/guide.md, read by genguide's own parse
  the-subtle-layer.pdf   THE SUBTLE LAYER: docs/subtle-layer.md, read by gensubtle's, each entry with its picture
  the-vault.zip          sealed (the user, 2026-10-30): a zip with a password, which may or may not hold the third book.
                         The key is its author's name as the book's own warning gives it, in title case with a space,
                         so it is written nowhere but in the book. docs/books/README.md tells the rumour, and the hint.

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
    "subtle": {"file": "the-subtle-layer.pdf", "title": "The Subtle Layer", "sub": "a trainer's handbook",
               "src": "docs/subtle-layer.md", "night": "#1d1424", "accent": "#8a5cc8", "foot": "THE SUBTLE LAYER"},
    "hermetic": {"file": "the-vault.zip", "title": "The Hermetic Layer", "sub": "SPELLCRAFT",
                 "src": "docs/hermetic-layer.md", "night": "#0c1712", "accent": "#1f8f5f", "foot": "THE HERMETIC LAYER"},
}


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
    gensubtle.use(book)
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
            entries.append({"short": e["short"], "title": e["title"], "picture": pic, "caption": e["caption"],
                            "paras": [(p, voice(k)) for k, p in enumerate(e["paras"])]})
        out.append({"label": s["label"], "heading": s["heading"], "entries": entries})
    return out


def author_of_hermetic(sections):
    """The vault's key: the author's name as the warning gives it ("OSRIC HATTER set it down"), in title case."""
    text = " ".join(p for p, _ in sections[0]["entries"][0]["paras"])
    m = re.search(r"\b([A-Z]{2,}) ([A-Z]{2,}) set it down\b", text)
    if not m:
        raise SystemExit("bookpdf: the third book's warning no longer names its author; the vault has no key")
    return "%s %s" % (m.group(1).title(), m.group(2).title())


def cover(book):
    if book in ("guide", "subtle"):
        return Image.open(os.path.join(ROOT, "wiki/images/%s_cover.png" % book)).convert("RGB")
    gensubtle.use("hermetic")
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
    b = BOOKS[book]
    pages = pages or {}
    ids = {}
    k = 0
    for i, s in enumerate(sections):
        for e in s["entries"]:
            ids[id(e)] = "e%d" % k
            k += 1
    warning = sections[0]["entries"][0] if book == "hermetic" else None    # it opens with its warning (4.39, rule 4)
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
<style>:root { --night: %s; --accent: %s; }%s</style></head><body>
<div class="cover"><img src="%s" alt=""></div>
%s%s<div class="toc"><h1>Contents</h1>%s</div>
%s
</body></html>""" % (esc(b["title"]), b["night"], b["accent"], CSS, data_uri(cover_im),
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
    b = BOOKS[book]
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


def main():
    args = sys.argv[1:]
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
            if book == "hermetic":
                seal(done, os.path.join(OUT, b["file"]), author_of_hermetic(sections), digest)
            else:
                os.replace(done, os.path.join(OUT, b["file"]))
            import fitz
            with fitz.open(second) as doc:
                print("    printed %s: %d pages" % (where, len(doc)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
