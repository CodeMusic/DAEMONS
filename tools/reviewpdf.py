#!/usr/bin/env python3
"""The external reviews and the press kit, as PDFs in the manual's look (the user, 2026-11-03: "a comprehensive pdf
report (that has a similar look and feel of the other daemon pdfs found in docs) ... and also a marketing section as a
seperate pdf ... some of the pages I could take on their own for social media").

    python3 tools/reviewpdf.py review            # report: what would be printed
    python3 tools/reviewpdf.py review --write    # docs/The-Fourth-Review.pdf
    python3 tools/reviewpdf.py press --write     # docs/DAEMONS-press-kit.pdf, and its social cards as PNGs

Each book is a folder: `review.md` (pandoc markdown, fenced divs for callouts), `book.css` (laid over the manual's
own `docs/manual/manual.css`), and `cover.html`. In the words, `{{sprite NAME ...}}` puts daemons in a row, drawn
from engineGba's own front sprites at a whole-number scale, and `{{frame NAME ...}}` puts game screens from
`docs/manual/frames/`, so the pictures are the build's and never redrawn.

A page with class `card` is a social card: square (1080 x 1080 px at 2x). The press kit prints them inside the PDF
and, with --write, also as PNGs in `docs/press-kit/cards/`, one file each, ready to post.

HOW IT PRINTS. pandoc turns the words into HTML; Chrome prints it; PyMuPDF stamps a running foot on every page but
the cover and the cards. Chrome is found on macOS or Linux.
"""
import glob
import html as H
import os
import re
import shutil
import subprocess
import sys
import tempfile

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
BOOKS = {
    "review": {"src": "docs/review-4", "out": "docs/The-Fourth-Review.pdf",
               "title": "DAEMONS: The Fourth Review", "foot": "THE FOURTH REVIEW"},
    "press": {"src": "docs/press-kit", "out": "docs/DAEMONS-press-kit.pdf",
              "title": "DAEMONS: press kit", "foot": "PRESS KIT", "cards": "docs/press-kit/cards"},
}
CHROMES = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "/usr/bin/google-chrome",
           "/usr/bin/chromium", "/opt/pw-browsers/chromium"]
TYPE_HUE = {  # tools/gbasprite.py TYPE_COLOR, by our names (a chapter band is coloured by the type it argues)
    "CONTENT": (198, 188, 168), "LOGIC": (96, 122, 158), "CORRUPT": (84, 92, 52), "STRATUM": (158, 122, 78),
    "LEGACY": (130, 130, 138), "SWARM": (128, 148, 72), "FLOW": (70, 106, 176), "GROWTH": (92, 158, 96),
    "SIGNAL": (86, 190, 190), "CONTEXT": (176, 86, 158), "VECTOR": (206, 70, 70), "ENTROPY": (222, 158, 46),
    "LATENT": (92, 70, 118), "FROZEN": (166, 206, 222), "HARDENED": (196, 170, 96), "OPAQUE": (40, 40, 46),
}


def chrome_path():
    for c in CHROMES:
        if os.path.exists(c):
            return c
    raise SystemExit("reviewpdf: no Chrome found (looked in %s)" % ", ".join(CHROMES))


# -- the build's own pictures ----------------------------------------------------------------------------------------

def species_slots():
    txt = open(os.path.join(GBA, "src/data/text/species_names.h"), encoding="utf-8").read()
    return {m.group(2): m.group(1).lower() for m in re.finditer(r'\[SPECIES_(\w+)\] = _\("([^"]*)"\)', txt)}


def sprite(slot):
    base = os.path.join(GBA, "graphics/pokemon", slot)
    if not os.path.isdir(base):
        base = os.path.join(GBA, "graphics/pokemon", "nexus_" + slot)
    im = Image.open(os.path.join(base, "front.png"))
    lines = [ln for ln in open(os.path.join(base, "normal.pal"), encoding="utf-8").read().split("\n")[3:] if ln.strip()]
    cols = [tuple(int(x) for x in ln.split()) for ln in lines]
    if im.mode != "P":
        im = im.convert("P")
    im.putpalette([c for col in cols for c in col] + [0] * (768 - 3 * len(cols)))
    rgba = im.convert("RGBA").crop((0, 0, 64, 64))
    px = rgba.load()
    for y in range(64):
        for x in range(64):
            if px[x, y][:3] == cols[0]:
                px[x, y] = (0, 0, 0, 0)
    return rgba.resize((512, 512), Image.NEAREST)


class Pictures:
    def __init__(self, work):
        self.work, self.slots, self.made = work, species_slots(), {}

    def daemon(self, name):
        if name not in self.made:
            out = "spr_%s.png" % re.sub(r"\W", "_", name)
            sprite(self.slots[name]).save(os.path.join(self.work, out))
            self.made[name] = out
        return self.made[name]

    def frame(self, name):
        src = os.path.join(ROOT, "docs/manual/frames", name + ".png")
        if not os.path.exists(src):
            src = os.path.join(ROOT, "docs/manual-social/frames", name + ".png")
        im = Image.open(src).convert("RGB")
        out = "frm_%s.png" % name
        im.resize((im.width * 4, im.height * 4), Image.NEAREST).save(os.path.join(self.work, out))
        return out

    def expand(self, md):
        def spr(m):
            names = m.group(2).split()
            cls = m.group(1) or ""
            imgs = "".join('<span class="sp"><img src="%s" alt="%s"><span>%s</span></span>'
                           % (self.daemon(n), n, n if "named" in cls else "") for n in names)
            return '<div class="sprites %s">%s</div>' % (cls.strip("."), imgs)

        def frm(m):
            items = re.findall(r'(\S+?)(?:\|"([^"]*)")?(?=\s|$)', m.group(1).strip())
            cells = "".join('<figure class="scr"><img src="%s" alt=""><figcaption>%s</figcaption></figure>'
                            % (self.frame(n), H.escape(c or "")) for n, c in items if n)
            return '<div class="screens n%d"><div class="row">%s</div></div>' % (len(items), cells)

        md = re.sub(r"\{\{sprite(\.[\w.]+)?\s+([^}]*)\}\}", spr, md)
        md = re.sub(r"\{\{frame\s+([^}]*)\}\}", frm, md)
        return md


# -- the page --------------------------------------------------------------------------------------------------------

def pandoc(md):
    r = subprocess.run(["pandoc", "--from=markdown+fenced_divs+bracketed_spans+pipe_tables-smart", "--to=html5",
                        "--section-divs", "--toc", "--toc-depth=2", "--standalone", "--template", TEMPLATE],
                       input=md, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr)
    toc, body = r.stdout.split("\n@@BODY@@\n", 1)
    return toc, body


def bands():
    out = []
    for t, (r, g, b) in TYPE_HUE.items():
        ink = "#16161a" if (0.299 * r + 0.587 * g + 0.114 * b) > 150 else "#fff"
        out.append(".t-%s{--tc:rgb(%d,%d,%d);--tink:%s}" % (t, r, g, b, ink))
    return "\n".join(out)


def chapters(body):
    n = [0]

    def h1(m):
        attrs, title = m.group(1), m.group(2)
        if "unnumbered" in attrs:
            return "<h1%s>%s</h1>" % (attrs, title)
        n[0] += 1
        return '<div class="chapnum">PART %d</div><h1%s>%s</h1>' % (n[0], attrs, title)
    return re.sub(r"<h1([^>]*)>(.*?)</h1>", h1, body, flags=re.S)


def section_types(body):
    """pandoc puts a heading's classes on its <section>: copy a t-TYPE class onto the heading's chapnum too."""
    return re.sub(r'(<section[^>]*class="[^"]*\b(t-[A-Z]+)\b[^"]*"[^>]*>\s*)<div class="chapnum">',
                  r'\1<div class="chapnum \2">', body)


TEMPLATE = os.path.join(tempfile.gettempdir(), "reviewpdf.template.html")
open(TEMPLATE, "w").write("$toc$\n@@BODY@@\n$body$\n")


def build(key, write):
    book = BOOKS[key]
    src = os.path.join(ROOT, book["src"])
    work = tempfile.mkdtemp(prefix="reviewpdf_")
    pics = Pictures(work)
    md = pics.expand(open(os.path.join(src, "review.md"), encoding="utf-8").read())
    toc, body = pandoc(md)
    body = section_types(chapters(body))
    css = open(os.path.join(ROOT, "docs/manual/manual.css"), encoding="utf-8").read()
    css += "\n" + open(os.path.join(src, "book.css"), encoding="utf-8").read() + "\n" + bands()
    cover = open(os.path.join(src, "cover.html"), encoding="utf-8").read()
    cover = pics.expand(cover)
    for f in glob.glob(os.path.join(src, "pictures", "*")):
        shutil.copy(f, work)
    html_path = os.path.join(work, "book.html")
    raw = os.path.join(work, "raw.pdf")
    import fitz

    def print_once(pages):
        t = re.sub(r'href="#([^"]+)"([^>]*)>(.*?)</a>',
                   lambda m: '<a href="#%s"%s><span class="tt">%s</span><span class="tp">%s</span></a>'
                   % (m.group(1), m.group(2), m.group(3), pages.get(m.group(1), "")), toc, flags=re.S)
        toc_html = ('<section class="toc"><div class="tochead t-CONTEXT">Contents</div>%s</section>' % t) if toc else ""
        page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>%s</title><style>%s</style></head>'
                '<body>%s%s%s</body></html>' % (H.escape(book["title"]), css, cover, toc_html, body))
        open(html_path, "w", encoding="utf-8").write(page)
        if os.path.exists(raw):
            os.remove(raw)
        r = subprocess.run([chrome_path(), "--headless", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer",
                            "--generate-pdf-document-outline", "--print-to-pdf=" + raw, "file://" + html_path],
                           capture_output=True, text=True, timeout=300)
        if not os.path.exists(raw):
            raise SystemExit("reviewpdf: Chrome printed nothing\n" + r.stderr[-2000:])
        out = {}
        with fitz.open(raw) as d:
            for p in range(min(6, len(d))):
                for link in d[p].get_links():
                    if link.get("nameddest") and link.get("page", -1) >= 0:
                        out.setdefault(link["nameddest"], link["page"] + 1)
        return out

    landed = print_once({})
    if toc:
        print_once(landed)      # the contents' page numbers, from where the first print's links landed
    doc = fitz.open(raw)
    print("%s: %d pages, html at %s" % (book["out"], len(doc), html_path))
    if not write:
        return
    cards = []
    for i, page in enumerate(doc):
        r = page.rect
        if i == 0:
            continue
        if abs(r.width - r.height) < 2:      # a social card: no foot
            cards.append(i)
            continue
        y = r.height - 20
        grey = (0.45, 0.45, 0.5)
        page.insert_text((34, y), "DAEMONS  ·  " + book["foot"], fontsize=6.5, fontname="helv", color=grey)
        num = str(i + 1)
        page.insert_text((r.width / 2 - fitz.get_text_length(num, "helv", 7.5) / 2, y), num, fontsize=7.5,
                         fontname="helv", color=(0.1, 0.1, 0.12))
        right = "design bible v%s" % bible_version()
        page.insert_text((r.width - 34 - fitz.get_text_length(right, "helv", 6.5), y), right, fontsize=6.5,
                         fontname="helv", color=grey)
    doc.set_metadata({"title": book["title"], "author": "the DAEMONS project",
                      "subject": "against design bible v%s" % bible_version(), "creator": "tools/reviewpdf.py",
                      "producer": "Chrome, PyMuPDF"})
    out = os.path.join(ROOT, book["out"])
    doc.save(out, garbage=3, deflate=True)
    print("wrote", book["out"])
    if book.get("cards") and cards:
        cdir = os.path.join(ROOT, book["cards"])
        os.makedirs(cdir, exist_ok=True)
        for f in glob.glob(os.path.join(cdir, "*.png")):
            os.remove(f)
        labels = [re.sub(r"^\d+\s*·\s*", "", k) for k in re.findall(r'<div class="k">([^<]*)</div>', md)]
        for n, i in enumerate(cards, 1):
            p = doc[i]
            title = labels[n - 1] if n - 1 < len(labels) else "card"
            slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:40] or "card"
            pix = p.get_pixmap(matrix=fitz.Matrix(1080 / p.rect.width, 1080 / p.rect.width))
            name = "%02d-%s.png" % (n, slug)
            pix.save(os.path.join(cdir, name))
            print("  card", name)
    doc.close()


def bible_version():
    m = re.search(r"\bv(\d+\.\d+)\b", open(os.path.join(ROOT, "docs/vision.md"), encoding="utf-8").read(3000))
    return m.group(1) if m else "?"


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] not in BOOKS:
        raise SystemExit(__doc__)
    build(args[0], "--write" in args)
