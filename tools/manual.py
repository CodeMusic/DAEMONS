#!/usr/bin/env python3
"""The DAEMONS player's manual, as a PDF (the user, 2026-10-28: "a DAEMONs user manual pdf that goes thorugh
everything has images from the game and really communicates everthing includes the different ways to play").

    python3 tools/manual.py               # build the page and say whether docs/DAEMONS-manual.pdf is current
    python3 tools/manual.py --write       # print docs/DAEMONS-manual.pdf, if its sources changed since it was printed
    python3 tools/manual.py --write --force       # print it even if they did not
    python3 tools/manual.py --html OUT.html       # the page before printing, to look at in a browser
    python3 tools/manual.py --refresh     # copy docs/manual/frames/ again from the theatre's captures (and --write)
    python3 tools/manual.py --book social --write   # the second book: PLAYING TOGETHER, the social features (C-219..)
    python3 tools/manual.py --book quick --write    # QUICK START: what DAEMONS is and how to play, in large type
    python3 tools/manual.py --book micro --write    # MICRO-START: the same, in five pages at most
    python3 tools/manual.py --book etymology --write   # THE OLD WORD: how daimon branched, and why it is said DAY-mons
    python3 tools/manual.py --book textbook --write    # CALLOW SCHOOL's TEXTBOOK, as a university textbook
    python3 tools/manual.py --book companion --write   # THE COMPANION: the whole app, its pictures from the site (C-321)
    python3 tools/manual.py --book watch --write       # THE WATCH: the T-Watch Ultra and S3 on the wrist (C-326)

Rebuild it every release: the version, the patches and every daemon's picture and INDEX entry are read from the
build, so a release that changes them changes the manual.

WHAT IT READS
  docs/manual/manual.md       the words, in pandoc markdown; {{...}} marks what is drawn from the build (below)
  docs/manual/frames/*.png    game screens, 240x160, each captured in the theatre from a built ROM; frames.json says
                              which route, stop and frame, and when (.theatre/ is gitignored, so the frames are kept here)
  engineGba/                  the daemons' sprites, types and INDEX entries; the seventeen types, their 111 relations
                              and their hues (through tools/gbachart.py, the type chart's own reader)
  ROM RELEASE/                the newest release, and HOW_TO_PATCH.md's table of the four patches
  docs/vision.md              the design bible's version
  wiki/images/                the two books' covers, titled in a common typeface (wiki/covers.py) -- never the game's
  docs/holidays.json          the year's holidays by their in-world names, and each month's note and colour (T-416)
  tools/companion_export.py   the week: each day's note, word, virtue over its shadow and centre, as the companion has it

THE SHORTCODES, each alone on its line except the inline three
  {{screen NAME | caption}}           one game screen
  {{screens A B=Its_label C | caption}}   two to four in a row, each with an optional label (underscores are spaces)
  {{daemons NAME NAME ...}}           a card for each: front sprite, number, types, category, both editions' entries
  {{sprites NAME NAME ...}}           a row of front sprites and names
  {{typechart}}  {{typelist}}  {{patches}}  {{cover guide|subtle}}  {{week}}  {{holidays}}
  inline: {{release}}  {{bible}}  {{date}}

HOW IT PRINTS. pandoc turns the words into HTML; Google Chrome prints it (as docs/build-pdf.sh does) on A5. It prints
twice: the first print's contents links say which page each chapter and section landed on, the second prints those
numbers. PyMuPDF then stamps the running foot on every page but the cover, and keeps a hash of every source in the
PDF's keywords -- which is how this knows, without printing, whether the PDF on disk is current.

Every word quoted from the game is a DRAFT until approved, as the game's are; the manual says so on its second page.
It shows nothing from docs/private/, no NOTEBOOK page, and none of the four things CLAUDE.md keeps out of public
writing, and it says how things work, never where they are.
"""
import base64, datetime, glob, hashlib, html as H, json, os, re, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
SRC = os.path.join(ROOT, "docs/manual")
OUT = os.path.join(ROOT, "docs/DAEMONS-manual.pdf")   # the companion app reads it here, on main (C-233): never move it
#  The books this prints: the player's manual (the default, unchanged), and PLAYING TOGETHER -- trading, loans, gifts,
#  meetings and friends' homes (the user, 2026-10-31: "a separate manual ... about the social features of daemons
#  specifically, still with diagrams and artwork"). --book NAME chooses; each has its own folder and PDF.
BOOKS = {
    "main": {"src": "docs/manual", "out": "docs/DAEMONS-manual.pdf", "title": "DAEMONS: the player's manual",
             "tag": "PLAYER'S MANUAL", "sub": "Every way to play, and how it all works", "foot": "the player's manual",
             "subject": "How to play DAEMONS: CONTEXT / CONTENT, and every way to play it",
             "sprites": ("ROVERCUB", "LABEL", "CLUSTER"), "strip": None},
    "social": {"src": "docs/manual-social", "out": "docs/DAEMONS-social-manual.pdf", "title": "DAEMONS: playing together",
               "tag": "PLAYING TOGETHER", "sub": "Trading, lending, gifts, meetings and friends' homes", "foot": "playing together",
               "subject": "DAEMONS with other players: trading, loans, gifts, meetings and friends' homes",
               "sprites": ("PENGUIN", "PENPHIN", "DOLPHIN"),
               "strip": ("ROVERCUB", "LABEL", "CLUSTER", "INFERENCE", "HAUNTPROC", "LEMMA MIND", "THEOREM", "PING")},
    # the third: THE TIINY, setting up the house's bigger mind for the companion (the user, 2026-10-31: "a short pdf for
    # how to set up the tiiny to a computer and have it communicate with the hub ... a bit daemon gamified")
    "tiiny": {"src": "docs/manual-tiiny", "out": "docs/DAEMONS-tiiny-manual.pdf", "title": "DAEMONS: a bigger mind",
              "tag": "A BIGGER MIND", "sub": "The Tiiny, set up for the companion", "foot": "a bigger mind",
              "subject": "Setting up the Tiiny Pocket for the DAEMONS companion: the computer, the network and the hub",
              "sprites": ("ROVERBYTE", "INFERENCE", "MAINFRAME"),
              "strip": ("HUNCH", "CONJECTURE", "PROOF", "THEOREM", "LEMMA MIND", "HEATSINK", "DUALCORE", "ECHO")},
    # the fourth: QUICK START, short and in large type (the user, 2026-10-31: "much shorter started with the context of
    # what this is ... and then a how to play ... written such that my 77 year old Mom could understand it and play it")
    "quick": {"src": "docs/manual-quick", "out": "docs/DAEMONS-quickstart.pdf", "title": "DAEMONS: quick start",
              "tag": "QUICK-START", "sub": "What it is, and how to play", "foot": "quick start",
              "subject": "DAEMONS, quickly: what it is, and how to play it, step by step",
              "sprites": ("LABEL", "CLUSTER", "ROVERCUB"), "strip": None},
    # the fifth: MICRO-START, the quick start again in five pages at most, a little smaller (the user, 2026-10-31: "a
    # third potion, to represent an even quicker micro version, taht one is at max 5 pages, with a bit smaller text")
    "micro": {"src": "docs/manual-micro", "out": "docs/DAEMONS-microstart.pdf", "title": "DAEMONS: micro start",
              "tag": "MICRO-START", "sub": "Five pages, and you are playing", "foot": "micro start",
              "subject": "DAEMONS in five pages: what it is, and how to play it",
              "sprites": ("LABEL", "CLUSTER", "ROVERCUB"), "strip": None, "toc": False, "max_pages": 5},
    # the sixth: THE OLD WORD, the history of the word (the user, 2026-11-01: "maybe lets have a full etomoly book on how
    # daemons and demons branched?" -- a PDF like the manuals; the frightening word that forked from it never printed)
    "etymology": {"src": "docs/manual-etymology", "out": "docs/DAEMONS-etymology.pdf", "title": "DAEMONS: the old word",
                  "tag": "THE OLD WORD", "sub": "How daimon branched, and why it is said DAY-mons", "foot": "the old word",
                  "subject": "The history of the word daemon: the Greek daimon, Maxwell's sorting being, the computer's "
                             "background helpers, and the game",
                  "sprites": ("GUARDIAN", "LODESTAR", "CRON"),
                  "strip": ("PING", "ECHO", "HEARTBEAT", "SCHEDULER", "SENTINEL", "KEEPER", "LOOKOUT", "RELAY")},
    # the seventh: CALLOW SCHOOL's TEXTBOOK, its seven floors taught as a university textbook would (the user, 2026-11-03:
    # "the look and feel of a real school text book and properly teach the topics", each floor's board quoted to study
    # from). Its own cover and title pages (cover.html, front.html); every board quoted word for word from the build.
    "textbook": {"src": "docs/manual-textbook", "out": "docs/DAEMONS-textbook.pdf",
                 "title": "Principles of Mind: An Introduction in Seven Floors", "chapter": "CHAPTER",
                 "sub": "CALLOW SCHOOL's TEXTBOOK", "foot": "principles of mind",
                 "subject": "CALLOW SCHOOL's TEXTBOOK as a university textbook: language, attention, memory, categories, "
                            "learning, bias and error",
                 "sprites": ("LABEL", "CLUSTER", "ROVERCUB"), "strip": None},
    # the eighth: THE COMPANION, the whole app (C-321; the user, 2026-11-10: "a companion user manual pdf ... for the entire
    # companion functionality -- built in a way as we evolve the app the manual can easily be update and rebuilt"). Its
    # pictures are the site photographed by tools/companion_shots.py from docs/manual-companion/shots.json, so a rerun
    # retakes every one; pages.json says which chapter covers each of the app's pages, and a page it does not name is
    # said when the book is printed (app_pages).
    "companion": {"src": "docs/manual-companion", "out": "docs/DAEMONS-companion-manual.pdf", "title": "DAEMONS: the companion",
                  "tag": "THE COMPANION", "sub": "Your daemons AWAY: the app, the hub and the devices", "foot": "the companion",
                  "subject": "The DAEMONS companion: the app, the site, the hub, the house's mind and the devices",
                  "sprites": ("ROVERBYTE", "ROVERCUB", "PING"),
                  "strip": ("ECHO", "HEARTBEAT", "PACKET", "INFERENCE", "RELAY", "KEEPER", "LOOKOUT", "SENTINEL"),
                  "app_pages": True},
    # the ninth: THE WATCH, the T-Watch Ultra and the T-Watch S3 on the wrist (C-326; the user, 2026-11-11: "a manual
    # specific to the t-watch"), read from the companion's firmware (firmware/esp32/src) and its wiki's watch pages; no
    # screen of the watch is captured by any tool yet, so its pictures are drawings (diagrams/)
    "watch": {"src": "docs/manual-watch", "out": "docs/DAEMONS-watch-manual.pdf", "title": "DAEMONS: the watch",
              "tag": "THE WATCH", "sub": "Your daemon on your wrist: the T-Watch Ultra and the T-Watch S3",
              "foot": "the watch",
              "subject": "The DAEMONS companion on a watch: the T-Watch Ultra and the T-Watch S3",
              "sprites": ("ROVERCUB", "HEARTBEAT", "PING"),
              "strip": ("ECHO", "PACKET", "RELAY", "LOOKOUT", "SENTINEL", "KEEPER", "INFERENCE", "ROVERBYTE")},
}
BOOK = BOOKS["main"]
THEATRE = os.path.join(ROOT, ".theatre/routes")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SCREEN_SCALE, SPRITE_SCALE = 4, 8           # nearest-neighbour, so no PDF reader smooths a pixel
#  the cover: the three first daemons large, and a strip of the ones met on the first roads
COVER_STRIP = ("PING", "NIBBLE", "CRAWLER", "PACKET", "SPIKE", "FORK", "HUNCH", "LOOP")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gbachart                                  # noqa: E402  the seventeen types, their relations and hues
import companion_export                          # noqa: E402  the week, as the companion's TODAY shows it
import manual_devices                            # noqa: E402  each cover's colour and its device (C-326)
from PIL import Image                            # noqa: E402


# -- what the build says ---------------------------------------------------------------------------------------------

def bible_version():
    m = re.search(r"\bv(\d+\.\d+)\b", open(os.path.join(ROOT, "docs/vision.md"), encoding="utf-8").read(3000))
    return m.group(1) if m else "?"


def newest_release():
    """(name, date) of the newest folder under ROM RELEASE/v*.x/ that has its notes."""
    best = None
    for notes in glob.glob(os.path.join(ROOT, "ROM RELEASE", "v*.x", "v*", "RELEASE_NOTES.md")):
        name = os.path.basename(os.path.dirname(notes))
        key = tuple(int(x) for x in name[1:].split("."))
        if best is None or key > best[0]:
            best = (key, name, notes)
    if not best:
        return "unreleased", ""
    m = re.search(r"Released (\d{4}-\d\d-\d\d)", open(best[2], encoding="utf-8").read())
    return best[1], m.group(1) if m else ""


def patch_rows():
    """HOW_TO_PATCH.md's own table: your ROM, CRC32, SHA-1, patch."""
    text = open(os.path.join(ROOT, "ROM RELEASE/HOW_TO_PATCH.md"), encoding="utf-8").read()
    rows = re.findall(r"^\| (Pok[^|]+?) \| `([0-9A-F]{8})` \| `([0-9a-f]{40})` \| `([^`]+)` \|$", text, re.M)
    if len(rows) != 4:
        raise SystemExit("manual: HOW_TO_PATCH.md's table of four patches has changed shape (%d rows)" % len(rows))
    return rows


def gba_pal(path):
    d = open(path, "rb").read()
    return [((c & 31) * 255 // 31, ((c >> 5) & 31) * 255 // 31, ((c >> 10) & 31) * 255 // 31)
            for c in (int.from_bytes(d[2 * i:2 * i + 2], "little") for i in range(16))]


def gba_picture(path, pal):
    """A 64x64 4bpp front sprite as the GBA lays it out: 8x8 tiles, row-major, index 0 clear."""
    d = open(path, "rb").read()
    im = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    for t in range(64):
        for y in range(8):
            for x in range(8):
                b = d[t * 32 + y * 4 + x // 2]
                v = (b >> 4) if x & 1 else b & 15
                if v:
                    im.putpixel(((t % 8) * 8 + x, (t // 8) * 8 + y), pal[v] + (255,))
    return im


class Daemons:
    """Every daemon's name, number, types, category and both editions' entries, read from the engine's tables."""

    def __init__(self, type_names):
        rd = lambda p: open(os.path.join(GBA, p), encoding="utf-8").read()
        self.name = dict(re.findall(r'\[SPECIES_(\w+)\]\s*=\s*_\("([^"]*)"\)', rd("src/data/text/species_names.h")))
        self.slot = {v: k for k, v in self.name.items()}
        entries = rd("src/data/pokemon/pokedex_entries.h")
        self.cat = dict(re.findall(r'\[NATIONAL_DEX_(\w+)\]\s*=\s*\{\s*\.categoryName = _\("([^"]*)"\)', entries))
        # the text each INDEX row points at, read rather than guessed (OLD_UNOWN_B's is gMissingnoPokedexText, T-499)
        self.desc = dict(re.findall(r"\[NATIONAL_DEX_(\w+)\]\s*=\s*\{[^}]*?\.description\s*=\s*(g\w+)\s*,", entries))
        enum = re.search(r"enum\s*\{\s*NATIONAL_DEX_NONE,(.*?)\};", rd("include/constants/pokedex.h"), re.S).group(1)
        self.number = {n: i + 1 for i, n in enumerate(re.findall(r"NATIONAL_DEX_(\w+)", enum))}
        # An alias is the INDEX's key only when the INDEX has a row by that name: T-395's NEXUS residents do
        # (SPECIES_REFLECTION is OLD_UNOWN_C, numbered NATIONAL_DEX_REFLECTION), but T-234's are C nicknames for the
        # slot they took (SPECIES_DOLPHIN is WAILMER, still NATIONAL_DEX_WAILMER and gWailmerPokedexText, T-499).
        alias = {b: a for a, b in re.findall(r"#define SPECIES_(\w+)\s+SPECIES_(\w+)\b", rd("include/constants/species.h"))
                 if a in self.number}
        self.key = {slot: alias.get(slot, slot) for slot in self.name}
        info = rd("src/data/pokemon/species_info.h")
        self.types = {}
        for m in re.finditer(r"\[SPECIES_(\w+)\]\s*=", info):
            t = re.search(r"\.types\s*=\s*\{\s*TYPE_(\w+)\s*,\s*TYPE_(\w+)\s*\}", info[m.end():m.end() + 1500])
            if t:
                a, b = (type_names.get(x, x) for x in t.groups())
                self.types[m.group(1)] = [a] if a == b else [a, b]
        self.text = {ed: rd("src/data/pokemon/pokedex_text_%s.h" % ed) for ed in ("fr", "lg")}

    def entry(self, slot, ed):
        key = self.key[slot]
        sym = self.desc.get(key) or "g%sPokedexText" % key.replace("_", "")   # a stem matched without case (MR_MIME is Mrmime)
        m = re.search(r"%s\[\] = _\(\n(.*?)\);" % sym, self.text[ed], re.S | re.I)
        return "".join(re.findall(r'"([^"]*)"', m.group(1))).replace("\\n", " ").strip() if m else ""

    def sprite(self, name):
        slot = self.slot[name]
        base = os.path.join(GBA, "graphics/pokemon", slot.lower())
        if not os.path.isdir(base):                       # a NEXUS resident's own folder (T-395)
            base = os.path.join(GBA, "graphics/pokemon", "nexus_" + name.lower())
        return gba_picture(os.path.join(base, "front.4bpp"), gba_pal(os.path.join(base, "normal.gbapal")))


# -- the shortcodes --------------------------------------------------------------------------------------------------

class Build:
    def __init__(self, work):
        self.work, self.images = work, {}
        self.type_names, self.relations = gbachart.load_types()
        shipped, _ = gbachart.load_hues(self.type_names)
        self.hue = dict(gbachart.PROPOSED_HUE)
        self.hue.update(shipped)
        self.order = [t for t in gbachart.CHART_ORDER if t in self.type_names.values()]
        self.daemons = Daemons(self.type_names)
        listed = json.load(open(os.path.join(SRC, "frames.json"), encoding="utf-8"))
        self.frames, self.pictures = listed["frames"], listed.get("pictures", {})
        self.digest = hashlib.sha1()

    def image(self, key, im, scale):
        """Write an image into the work folder at a whole-number scale; return its file name."""
        if key not in self.images:
            im = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
            name = "img_%03d.png" % len(self.images)
            im.save(os.path.join(self.work, name))
            self.digest.update(key.encode() + im.tobytes())
            self.images[key] = name
        return self.images[key]

    def frame(self, name):
        if name not in self.frames:
            raise SystemExit("manual: no frame '%s' in docs/manual/frames.json" % name)
        return self.image("frame:" + name, Image.open(os.path.join(SRC, "frames", name + ".png")).convert("RGB"),
                          SCREEN_SCALE)

    def picture(self, name):
        """A picture filed in qa/screenshots/ (the companion's screens, which no theatre captures), cropped."""
        if name not in self.pictures:
            raise SystemExit("manual: no picture '%s' in docs/manual/frames.json" % name)
        p = self.pictures[name]
        im = Image.open(os.path.join(ROOT, p["from"])).convert("RGB")
        if p.get("crop"):
            im = im.crop(tuple(p["crop"]))
        if im.width > 1400:
            im = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
        return self.image("picture:" + name, im, 1)

    def chip(self, t):
        r, g, b = self.hue.get(t, (128, 128, 128))
        ink = "#16161a" if (0.299 * r + 0.587 * g + 0.114 * b) > 150 else "#fff"
        return '<span class="chip" style="background:rgb(%d,%d,%d);color:%s">%s</span>' % (r, g, b, ink, t)

    # each returns raw HTML
    def sc_screen(self, args, caption):
        return self.sc_screens(args, caption)

    def sc_screens(self, args, caption):
        cells = []
        for a in args:
            name, _, label = a.partition("=")
            lab = '<span class="lab">%s</span>' % H.escape(label.replace("_", " ")) if label else ""
            cells.append('<div class="scr"><img src="%s" alt="">%s</div>' % (self.frame(name), lab))
        cls = "screens n%d" % len(cells)
        cap = "<figcaption>%s</figcaption>" % caption if caption else ""
        return '<figure class="%s"><div class="row">%s</div>%s</figure>' % (cls, "".join(cells), cap)

    def sc_pictures(self, args, caption):
        cells = []
        for a in args:      # side by side at one height: each as wide as its shape asks
            src = self.picture(a)
            w, h = Image.open(os.path.join(self.work, src)).size
            cells.append('<div class="pic" style="flex:%.3f"><img src="%s" alt=""></div>' % (w / h, src))
        cells = "".join(cells)
        cap = "<figcaption>%s</figcaption>" % caption if caption else ""
        return '<figure class="pictures n%d"><div class="row">%s</div>%s</figure>' % (len(args), cells, cap)

    def sc_daemons(self, args, caption):
        out = []
        for name in args:
            d = self.daemons
            slot = d.slot[name]
            key = d.key[slot]
            img = self.image("sprite:" + name, d.sprite(name), SPRITE_SCALE)
            chips = "".join(self.chip(t) for t in d.types.get(slot, []))
            out.append(
                '<div class="dcard"><img class="spr" src="%s" alt=""><div class="dtext">'
                '<div class="dname">%s <span class="dno">No. %03d</span></div>'
                '<div class="dcat">%s DAEMON %s</div>'
                '<p><b>CONTENT</b> %s</p><p><b>CONTEXT</b> %s</p></div></div>'
                % (img, name, d.number.get(key, 0), H.escape(d.cat.get(key, "")), chips,
                   H.escape(d.entry(slot, "fr")), H.escape(d.entry(slot, "lg"))))
        cap = "<figcaption>%s</figcaption>" % caption if caption else ""
        return '<figure class="daemons">%s%s</figure>' % ("".join(out), cap)

    def sc_sprites(self, args, caption):
        cells = "".join('<div class="sp"><img src="%s" alt=""><span>%s</span></div>'
                        % (self.image("sprite:" + n, self.daemons.sprite(n), SPRITE_SCALE), n) for n in args)
        cap = "<figcaption>%s</figcaption>" % caption if caption else ""
        return '<figure class="sprites">%s%s</figure>' % (cells, cap)

    def sc_typelist(self, args, caption):
        rows = "".join("<tr><td>%s</td><td>%s</td></tr>" % (self.chip(t), H.escape(gbachart.CLAUSE.get(t, ("",))[0]))
                       for t in self.order)
        return '<table class="typelist"><tbody>%s</tbody></table>' % rows

    def sc_typechart(self, args, caption):
        sym = {2.0: "2", 0.5: "½", 0.0: "0"}
        head = "".join('<th class="v"><div style="background:rgb(%d,%d,%d)"></div><span>%s</span></th>'
                       % (self.hue.get(t, (128,) * 3) + (t,)) for t in self.order)
        body = []
        for a in self.order:
            cells = []
            for b in self.order:
                m = self.relations.get((a, b))
                cells.append('<td class="m%s">%s</td>' % (str(m).replace(".", "_") if m is not None else "",
                                                           sym.get(m, "")))
            body.append("<tr><th class=\"h\">%s</th>%s</tr>" % (self.chip(a), "".join(cells)))
        return ('<figure class="typechart"><table><thead><tr><th class="corner">attacking ↓ &nbsp; defending →</th>%s'
                '</tr></thead><tbody>%s</tbody></table><figcaption>%s</figcaption></figure>'
                % (head, "".join(body), caption or ""))

    def sc_patches(self, args, caption):
        rows = "".join("<tr><td>%s</td><td><code>%s</code></td><td><code>%s</code></td><td>%s</td></tr>"
                       % (H.escape(rom.replace("Pokémon ", "")), crc, sha[:12] + "…", H.escape(p))
                       for rom, crc, sha, p in patch_rows())
        return ('<table class="patches"><thead><tr><th>your ROM</th><th>CRC32</th><th>SHA-1 begins</th>'
                '<th>the patch</th></tr></thead><tbody>%s</tbody></table>' % rows)

    def sc_week(self, args, caption):
        """The seven days, Sunday first. No colour beside a centre (vision 4.38), and a virtue over its shadow (9.21)."""
        rows = "".join("<tr><td><b>%s</b></td><td>%s</td><td>%s</td><td><b>%s</b> over %s</td><td>%s</td></tr>"
                       % tuple(H.escape(d[k]) for k in ("day", "note", "theme", "virtue", "shadow", "chakra"))
                       for d in companion_export.week_table()["days"])
        return ('<table class="week"><thead><tr><th>day</th><th>note</th><th>its word</th><th>its virtue, over its '
                'shadow</th><th>its centre</th></tr></thead><tbody>%s</tbody></table>' % rows)

    def sc_holidays(self, args, caption):
        """The year, three a month, by the game's own names (real names are the companion's only, T-416)."""
        src = json.load(open(os.path.join(ROOT, "docs/holidays.json"), encoding="utf-8"))
        nth = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th"}
        wd = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

        def when(h):
            r = h["rule"]
            if r["kind"] == "fixed":
                w = "the %d%s" % (r["day"], {1: "st", 2: "nd", 3: "rd", 21: "st", 22: "nd", 23: "rd", 31: "st"}.get(r["day"], "th"))
            elif r["kind"] == "nth_weekday":
                w = "the %s %s" % (nth[r["n"]], wd[r["weekday"]])
            elif r["kind"] == "easter":
                w = "Easter Sunday" if not r["offset"] else "%d days %s Easter" % (abs(r["offset"]), "before" if r["offset"] < 0 else "after")
            elif r["kind"] == "season_start":
                w = "the first day of %s" % r["season"]
            else:
                w = "the harvest moon"
            if h["days"] > 1:
                w += ", %d days" % h["days"]
            return "<b>%s</b> <span class=\"when\">%s%s</span>" % (H.escape(h["name"]), w, ", quiet" if h.get("quiet") else "")

        rows = []
        for i, m in enumerate(src["months"], 1):
            cell = {e: "<br>".join(when(h) for h in src["holidays"] if h["month"] == i and h["edition"] == e)
                    for e in ("COMMON", "CONTENT", "CONTEXT")}
            r, g, b = (int(m["hex"][k:k + 2], 16) for k in (1, 3, 5))
            ink = "#16161a" if (0.299 * r + 0.587 * g + 0.114 * b) > 150 else "#fff"
            rows.append('<tr><td><span class="chip" style="background:%s;color:%s">%s · %s</span></td><td>%s</td>'
                        '<td>%s</td><td>%s</td></tr>' % (m["hex"], ink, m["month"], m["note"], cell["COMMON"],
                                                          cell["CONTENT"], cell["CONTEXT"]))
        return ('<table class="holidays"><thead><tr><th>the month</th><th>both</th><th>CONTENT, the north</th>'
                '<th>CONTEXT, the south</th></tr></thead><tbody>%s</tbody></table>' % "".join(rows))

    def school(self, floor):
        """CALLOW SCHOOL's floor as the build has it: the companion's export of the game's own boards (C-129)."""
        if not hasattr(self, "_school"):
            self._school = json.load(open(os.path.join(ROOT, "companion/server/data/school.json"), encoding="utf-8"))
        for f in self._school["floors"]:
            if f["floor"] == floor:
                return f
        raise SystemExit("manual: CALLOW SCHOOL has no floor %s" % floor)

    @staticmethod
    def chalk(text):
        """The game's lines, wrapped for a message box, as paragraphs: a blank line parts them, a newline is a space."""
        return "".join("<p>%s</p>" % H.escape(" ".join(p.split("\n")))
                       for p in text.split("\n\n") if p.strip())

    def sc_board(self, args, caption):
        """One board topic, word for word, as the TEXTBOOK quotes it to study from (T-520)."""
        floor, topic = args[0], " ".join(args[1:])
        f = self.school(floor)
        for b in f["board"]:
            if b["topic"] == topic:
                self.digest.update(b["text"].encode())
                return ('<blockquote class="board"><div class="blab">On the board &middot; %s %s &middot; <b>%s</b></div>'
                        '%s</blockquote>' % (floor, H.escape(f["subject"]), H.escape(topic), self.chalk(b["text"])))
        raise SystemExit("manual: %s's board has no topic %s" % (floor, topic))

    def sc_placard(self, args, caption):
        """A floor's placard by its stairs, word for word: what the floor is for."""
        f = self.school(args[0])
        self.digest.update(f["placard"].encode())
        text = f["placard"].split("\n\n", 1)[1] if "\n\n" in f["placard"] else f["placard"]
        return ('<blockquote class="placard"><div class="blab">The placard by the stairs &middot; %s</div>%s</blockquote>'
                % (H.escape(args[0]), self.chalk(text)))

    def sc_diagram(self, args, caption):
        """A drawing of how something works: an SVG from the book's diagrams/ folder, inline, so it prints sharp."""
        path = os.path.join(SRC, "diagrams", args[0] + ".svg")
        if not os.path.exists(path):
            raise SystemExit("manual: no diagram %s" % path)
        svg = open(path, encoding="utf-8").read()
        self.digest.update(svg.encode())
        svg = re.sub(r"<\?xml[^>]*>\s*", "", svg)
        cap = "<figcaption>%s</figcaption>" % caption if caption else ""
        return '<figure class="diagram">%s%s</figure>' % (svg, cap)

    def sc_cover(self, args, caption):
        path = os.path.join(ROOT, "wiki/images", {"guide": "guide_cover.png", "subtle": "subtle_cover.png"}[args[0]])
        im = Image.open(path).convert("RGB")
        return '<img class="bookcover" src="%s" alt="">' % self.image("cover:" + args[0], im, 1)

    def expand(self, text):
        rel, date = newest_release()
        text = (text.replace("{{release}}", rel).replace("{{bible}}", "v" + bible_version())
                .replace("{{date}}", date))

        def block(m):
            parts = m.group(1).split("|", 1)
            words = parts[0].split()
            fn = getattr(self, "sc_" + words[0], None)
            if fn is None:
                raise SystemExit("manual: no shortcode {{%s}}" % words[0])
            return "\n" + fn(words[1:], parts[1].strip() if len(parts) > 1 else "") + "\n"
        text = re.sub(r"^\{\{(.+?)\}\}\s*$", block, text, flags=re.M)
        if "{{" in text:
            raise SystemExit("manual: a shortcode was not expanded: " + text[text.index("{{"):][:60])
        return text


# -- the page --------------------------------------------------------------------------------------------------------

def pandoc(markdown):
    r = subprocess.run(["pandoc", "--from=markdown-smart+fenced_divs+bracketed_spans", "--to=html5",
                        "--section-divs", "--wrap=none"], input=markdown, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("manual: pandoc failed\n" + r.stderr)
    return r.stdout


#  pandoc --section-divs puts a heading's id on its section: <section id="ways" class="level1 ..."><h1 ...>
HEADS = re.compile(r'<section id="([^"]+)" class="level([12])[^"]*">\s*(?:<div class="chapnum">[^<]*</div>)?'
                   r'<h[12][^>]*>(.*?)</h[12]>', re.S)


def contents(body, pages=None):
    """The contents: every chapter (h1) and its sections (h2), each a link -- with its page once the first print says."""
    rows, n = [], 0
    for m in HEADS.finditer(body):
        ident, lvl, title = m.groups()
        title = re.sub(r"<[^>]+>", "", title)
        page = str(pages.get(ident, "")) if pages else "00"
        if lvl == "1":
            plain = "unnumbered" in m.group(0).split(">", 1)[0]     # a preface, a glossary: in the contents, no number
            n += 0 if plain else 1
            rows.append('<a class="toc1%s" href="#%s"><span class="tn">%s</span><span class="tt">%s</span>'
                        '<span class="tp">%s</span></a>' % (" plain" if plain else "", ident, "" if plain else n,
                                                            title, page))
        else:
            rows.append('<a class="toc2" href="#%s"><span class="tt">%s</span><span class="tp">%s</span></a>'
                        % (ident, title, page))
    return "\n".join(rows)


def chapters(body):
    """Number each chapter, and give its opening band the colour of the type it names (data-type)."""
    n = [0]

    def h1(m):
        attrs, title = m.group(1), m.group(2)
        if "unnumbered" in attrs:
            return '<h1%s>%s</h1>' % (attrs, title)
        n[0] += 1
        return '<div class="chapnum">%s %d</div><h1%s>%s</h1>' % (BOOK.get("chapter", "CHAPTER"), n[0], attrs, title)
    return re.sub(r"<h1([^>]*)>(.*?)</h1>", h1, body, flags=re.S)


def page_html(build, body, toc, css, rel, date):
    sprites = "".join('<img src="%s" alt="">' % build.image("sprite:" + n, build.daemons.sprite(n), SPRITE_SCALE)
                      for n in BOOK["sprites"])
    #  C-326: the book's own colour, and the device it is about in the middle, a daemon on its screen
    name = next(k for k, v in BOOKS.items() if v is BOOK)
    cover_style = ""
    if name in manual_devices.COVER:
        colour, kind, on = manual_devices.COVER[name]
        sprites = manual_devices.KIND[kind](*[build.image("dev:" + n, build.daemons.sprite(n), SPRITE_SCALE) for n in on],
                                            *([None] if len(on) == 1 else []))
        cover_style = ' style="--cbg:%s"' % colour
        build.digest.update((colour + kind + "".join(on) + sprites).encode())
    def band(t):
        r, g, b = build.hue.get(t, (128,) * 3)
        ink = "#16161a" if (0.299 * r + 0.587 * g + 0.114 * b) > 150 else "#fff"
        return ".t-%s{--tc:rgb(%d,%d,%d);--tink:%s}" % (t, r, g, b, ink)
    style = "\n".join(band(t) for t in build.order) + "\n" + manual_devices.CSS
    strip = "".join('<img src="%s" alt="">' % build.image("sprite:" + n, build.daemons.sprite(n), SPRITE_SCALE)
                    for n in (BOOK["strip"] or COVER_STRIP))
    tag = '<div class="ctag">%s</div>' % H.escape(BOOK["tag"]) if BOOK.get("tag") else ""   # QUICK-START, large
    contents_page = '<section class="toc"><h1 class="tochead">Contents</h1>%s</section>' % toc if BOOK.get("toc", True) else ""
    # a book may bring its own cover and the pages before its contents (cover.html, front.html beside its words): the
    # TEXTBOOK's is a university press's, not the game's (T-520). {release} and {date} are filled in.
    own = {}
    for part in ("cover", "front"):
        f = os.path.join(SRC, part + ".html")
        if os.path.exists(f):
            own[part] = open(f, encoding="utf-8").read().replace("{release}", H.escape(rel)).replace(
                "{date}", H.escape(date or ""))
    if "cover" in own:
        return """<!doctype html><html lang="en"><head><meta charset="utf-8"><title>%s</title>
<style>%s
%s</style></head><body>
%s
%s
%s
%s
</body></html>""" % (H.escape(BOOK["title"]), css, style, own["cover"], own.get("front", ""), contents_page, body)
    return """<!doctype html><html lang="en"><head><meta charset="utf-8"><title>%s</title>
<style>%s
%s</style></head><body>
<section class="cover"%s><div class="ctop"><div class="ced">CONTEXT / CONTENT</div><div class="ctitle">DAEMONS</div>
%s<div class="csub">%s</div></div>
<div class="cspr">%s</div><div class="cstrip">%s</div>
<div class="cbot"><div>For release <b>%s</b>%s &middot; every word quoted from the game is a DRAFT</div>
<div>A fan project for the Game Boy Advance. No ROM is in it, or anywhere in DAEMONS.</div></div></section>
%s
%s
</body></html>""" % (H.escape(BOOK["title"]), css, style, cover_style, tag, H.escape(BOOK["sub"]), sprites, strip, rel,
                        (", " + date) if date else "", contents_page, body)


def build_html(work):
    b = Build(work)
    md = open(os.path.join(SRC, "manual.md"), encoding="utf-8").read()
    body = chapters(pandoc(b.expand(md)))
    css = open(os.path.join(SRC, "manual.css"), encoding="utf-8").read()
    rel, date = newest_release()
    own = "".join(open(os.path.join(SRC, f), encoding="utf-8").read() for f in ("cover.html", "front.html")
                  if os.path.exists(os.path.join(SRC, f)))
    b.digest.update((md + css + own + rel).encode())
    return b, body, css, rel, date


def chrome(html_path, pdf_path):
    if not os.path.exists(CHROME):
        raise SystemExit("manual: Google Chrome is not at " + CHROME)
    r = subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer",
                        "--generate-pdf-document-outline", "--print-to-pdf=" + pdf_path, "file://" + html_path],
                       capture_output=True, text=True, timeout=300)
    if not os.path.exists(pdf_path):
        raise SystemExit("manual: Chrome printed nothing\n" + r.stderr[-2000:])


def landing_pages(pdf_path):
    """{id: page number} from the contents links of a first print."""
    import fitz
    out = {}
    with fitz.open(pdf_path) as doc:
        for p in range(min(12, len(doc))):     # a textbook's front pages push its contents later
            for link in doc[p].get_links():
                if link.get("nameddest") and link.get("page", -1) >= 0:
                    out.setdefault(link["nameddest"], link["page"] + 1)
    return out


def stamp(pdf_path, out_path, rel, digest):
    """The running foot on every page but the cover, and the sources' hash in the keywords."""
    import fitz
    doc = fitz.open(pdf_path)
    for i, page in enumerate(doc):
        if i == 0:
            continue
        r = page.rect
        y = r.height - 20
        page.insert_text((34, y), "DAEMONS  ·  " + BOOK["foot"], fontsize=6.5, fontname="helv", color=(0.45, 0.45, 0.5))
        num = str(i + 1)
        page.insert_text((r.width / 2 - fitz.get_text_length(num, "helv", 7.5) / 2, y), num, fontsize=7.5,
                         fontname="helv", color=(0.1, 0.1, 0.12))
        right = "DRAFT  ·  %s" % rel
        page.insert_text((r.width - 34 - fitz.get_text_length(right, "helv", 6.5), y), right, fontsize=6.5,
                         fontname="helv", color=(0.45, 0.45, 0.5))
    # the subject ends "(v<release>)": the companion's LIBRARY reads the release from it (C-233, app/manual.ts)
    doc.set_metadata({"title": BOOK["title"], "author": "the DAEMONS project",
                      "subject": "%s (%s)" % (BOOK["subject"], rel),
                      "keywords": "sources %s" % digest, "creator": "tools/manual.py", "producer": "Chrome, PyMuPDF"})
    doc.save(out_path, garbage=3, deflate=True)
    doc.close()


def printed_digest():
    if not os.path.exists(OUT):
        return None
    import fitz
    with fitz.open(OUT) as doc:
        m = re.search(r"sources (\w+)", doc.metadata.get("keywords") or "")
        return m.group(1) if m else None


def refresh_frames():
    """Copy every frame again from the theatre's captures, where this machine has them."""
    frames = json.load(open(os.path.join(SRC, "frames.json"), encoding="utf-8"))["frames"]
    got = 0
    for name, f in frames.items():
        src = os.path.join(THEATRE, f["from"] + ".png")
        if os.path.exists(src):
            shutil.copyfile(src, os.path.join(SRC, "frames", name + ".png"))
            got += 1
    print("  %d of %d frames copied from .theatre/routes/" % (got, len(frames)))


def app_pages():
    """C-321: every page of the companion app (its app/screens/**/*.tsx) that pages.json neither gives a chapter nor
    calls not for players -- so a page added to the app is named the next time the book is printed."""
    screens = os.path.join(ROOT, "companion", "app", "screens")
    listed = os.path.join(SRC, "pages.json")
    if not os.path.isdir(screens) or not os.path.exists(listed):
        return []
    known = json.load(open(listed, encoding="utf-8"))
    said = set(known.get("covered", {})) | set(known.get("not for players", []))
    found = sorted(os.path.relpath(os.path.join(d, f), os.path.dirname(screens))
                   for d, _, fs in os.walk(screens) for f in fs if f.endswith(".tsx"))
    return [f for f in found if f not in said]


def main():
    global BOOK, SRC, OUT
    args = sys.argv[1:]
    if "--book" in args:
        name = args[args.index("--book") + 1]
        if name not in BOOKS:
            raise SystemExit("manual: no book '%s' (%s)" % (name, ", ".join(BOOKS)))
        BOOK = BOOKS[name]
        SRC, OUT = os.path.join(ROOT, BOOK["src"]), os.path.join(ROOT, BOOK["out"])
    write, force = "--write" in args, "--force" in args
    if "--refresh" in args:
        refresh_frames()
        write = True
    with tempfile.TemporaryDirectory(prefix="daemons-manual-") as work:
        b, body, css, rel, date = build_html(work)
        digest = b.digest.hexdigest()[:16]
        html_path = os.path.join(work, "manual.html")
        if "--html" in args:
            dest = os.path.abspath(args[args.index("--html") + 1])
            open(html_path, "w", encoding="utf-8").write(page_html(b, body, contents(body), css, rel, date))
            shutil.copytree(work, os.path.dirname(dest), dirs_exist_ok=True)
            os.replace(os.path.join(os.path.dirname(dest), "manual.html"), dest)
            print("  wrote %s (and its %d pictures beside it)" % (dest, len(b.images)))
            return 0
        current = printed_digest() == digest
        if BOOK.get("app_pages"):
            new = app_pages()
            if new:
                print("  !! the app has %d page(s) the book does not cover: %s -- write of them, or list them in %s/pages.json"
                      % (len(new), ", ".join(new), BOOK["src"]))
        print("  release %s, design bible v%s; %d pictures (%d game screens); sources %s"
              % (rel, bible_version(), len(b.images), sum(k.startswith("frame:") for k in b.images), digest))
        if not write:
            print("  %s is %s" % (BOOK["out"], ("current" if current else
                  "missing" if not os.path.exists(OUT) else "out of date: --write prints it again")))
            return 0
        if current and not force:
            print("  %s is current; nothing to print (--force prints it anyway)" % BOOK["out"])
            return 0
        open(html_path, "w", encoding="utf-8").write(page_html(b, body, contents(body), css, rel, date))
        first = os.path.join(work, "first.pdf")
        chrome(html_path, first)
        second = first
        if BOOK.get("toc", True):        # a book with no contents page prints once: there are no numbers to place
            pages = landing_pages(first)
            missing = [i for i, _, _ in HEADS.findall(body) if i not in pages]
            if missing:
                raise SystemExit("manual: the first print did not place %s" % ", ".join(missing[:5]))
            open(html_path, "w", encoding="utf-8").write(page_html(b, body, contents(body, pages), css, rel, date))
            second = os.path.join(work, "second.pdf")
            chrome(html_path, second)
            if landing_pages(second) != pages:
                raise SystemExit("manual: the page numbers moved between the two prints")
        if BOOK.get("max_pages"):
            import fitz
            with fitz.open(second) as doc:
                if len(doc) > BOOK["max_pages"]:
                    raise SystemExit("manual: %s came to %d pages; it may have %d at most"
                                     % (BOOK["out"], len(doc), BOOK["max_pages"]))
        tmp = OUT + ".tmp"
        stamp(second, tmp, rel, digest)
        os.replace(tmp, OUT)
        import fitz
        with fitz.open(OUT) as doc:
            n = len(doc)
        print("  wrote %s: %d pages, %.1f MB" % (BOOK["out"], n, os.path.getsize(OUT) / 1e6))
        #  C-320: its cover on the companion's LIBRARY shelf, from the page just printed
        import shelfcovers
        shelfcovers.main(only={k for k, v in shelfcovers.PDFS.items() if v == os.path.basename(OUT)})
    return 0


if __name__ == "__main__":
    sys.exit(main())
