#!/usr/bin/env python3
"""T-509: the tarot decks in both books, the GBA's half -- the words and the frames, from the companion's own.

    python3 tools/port_arcana.py                       # report: every face read, measured and checked; nothing written
    python3 tools/port_arcana.py --write               # engineGba/src/data/arcana_cards.h and graphics/book/cards/
    python3 tools/port_arcana.py --write --engine DIR  # the same, into another engine checkout (a worktree)

WHAT IT READS. The companion's server/data/arcana.json (THE SUBTLE LAYER session's, every word DRAFT): twenty-two
cards, each with four faces the game deals -- REASON and INSTINCT (THE SUBTLE LAYER), ABOVE and BELOW (THE HERMETIC
LAYER) -- and each face { keyword, phrase, prophecy, species }. The game takes the KEYWORD and the short PHRASE (the
user, 2026-11-01: the long prophecy is the app's alone) and the face's daemon, which species.json turns into the
engine's SPECIES_ constant. The old single SPELLCRAFT face is ignored. A word changed there needs only a re-run.

WHAT IT WRITES. src/data/arcana_cards.h: the cards' words in the game's charset (the band and the panel draw them in
the frames' own 3x5 letters, gfx/drafts/t509_cards/draw_cards.py's font kept here as bitmasks by the game's byte, a
small letter drawn as its capital; the reading page in the book's font), each face's SPECIES_ constant, the frames'
sixteen-colour palettes, the section's DRAFT interface words, and the INCBINs of graphics/book/cards/: the eight
approved frames, the back (gfx/drafts/t509_cards/, approved 2026-11-01) and the deck tile, the back at half size
stacked three deep. The pulse-blue frames are not copied: book_reader.c breathes index 14 itself.

WHAT IT CHECKS, and fails on: a daemon species.json does not know, or the engine does not; a character the game
cannot print; a keyword over twelve letters; a phrase that does not fit the card's panel (three lines of fifteen
3x5 letters) or the reading page's column; any interface word over its box, and never over 208px.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fontwidth

ROOT = os.path.dirname(HERE)
WRITE = "--write" in sys.argv
ENGINE = sys.argv[sys.argv.index("--engine") + 1] if "--engine" in sys.argv else os.path.join(ROOT, "engineGba")
#  The companion as setup.sh links it, or where it is cloned when this checkout has no link (a worktree, or
#  check_generators --writes' sandbox, which crashed here 2026-11-06). Only ever READ.
COMPANION = next((p for p in (os.path.join(ROOT, "companion", "server", "data"),
                              os.path.expanduser("~/Projects/daemons-companion/server/data"))
                  if os.path.isfile(os.path.join(p, "arcana.json"))), os.path.join(ROOT, "companion", "server", "data"))
ART = os.path.join(ROOT, "gfx", "drafts", "t509_cards")
OUT_H = "src/data/arcana_cards.h"
OUT_GFX = "graphics/book/cards"

SIDES = ("reason", "instinct", "above", "below")
FRAMES = [s + v for s in SIDES for v in ("", "_shiny")]
ALLOWED = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 .,:;!?'-")

# the card's geometry (draw_cards.py): a 72x104 frame, the keyword band rows 4-12 and the phrase panel 79-99, both
# x 5-66; the daemon's 64x64 window at (4,14). Letters 3x5 on a 4px advance.
PANEL_X0, PANEL_X1 = 5, 66
PANEL_CHARS = (PANEL_X1 - PANEL_X0 + 1 + 1) // 4      # 15
PANEL_LINES = 3
READ_W = 140                                          # the reading page's column (book_reader.c CR_TEXT_W)
READ_LINES = 4
MSG_W = 208

# ---------------------------------------------------------------- the 3x5 letters (the frames' own font, extended)
FONT = {
    "A": "010101111101101", "B": "110101110101110", "C": "011100100100011",
    "D": "110101101101110", "E": "111100110100111", "F": "111100110100100",
    "G": "011100101101011", "H": "101101111101101", "I": "111010010010111",
    "J": "001001001101010", "K": "101101110101101", "L": "100100100100111",
    "M": "101111111101101", "N": "110101101101101", "O": "010101101101010",
    "P": "110101110100100", "Q": "010101101110011", "R": "110101110101101",
    "S": "011100010001110", "T": "111010010010010", "U": "101101101101111",
    "V": "101101101101010", "W": "101101111111101", "X": "101101010101101",
    "Y": "101101010010010", "Z": "111001010100111", " ": "000000000000000",
    "/": "001001010100100", "-": "000000111000000", ".": "000000000000010",
    # T-509's additions, for the phrases (DRAFT, drawn to sit with the art's)
    ",": "000000000010100", "'": "010010000000000", ":": "000010000010000", ";": "000010000010100",
    "!": "010010010000010", "?": "110001010000010",
    "0": "111101101101111", "1": "010110010010111", "2": "110001010100111", "3": "110001010001110",
    "4": "101101111001001", "5": "111100110001110", "6": "011100111101111", "7": "111001010010010",
    "8": "111101111101111", "9": "111101111001110",
}

# ---------------------------------------------------------------- the section's interface words, every one DRAFT
#  (name, text, font, limit px). The selector's titles are struck twice (+1px a letter), so they are measured bold.
UI = [
    ("CardsTile",      "CARDS",                   "small", 44),
    ("CardOfDay",      "THE CARD OF THE DAY",     "small", 96),
    ("ModeSingle",     "A SINGLE DRAW",           "normal", 140),
    ("ModePast",       "PAST / PRESENT / FUTURE", "normal", 140),
    ("ModeMind",       "MIND / BODY / SPIRIT",    "normal", 140),
    ("Past",           "PAST",                    "small", 74),
    ("Present",        "PRESENT",                 "small", 74),
    ("Future",         "FUTURE",                  "small", 74),
    ("Mind",           "MIND",                    "small", 74),
    ("Body",           "BODY",                    "small", 74),
    ("Spirit",         "SPIRIT",                  "small", 74),
    ("TurnBack",       "A TURN    B BACK",        "small", MSG_W),
    ("Draw",           "A DRAW",                  "small", MSG_W),
    ("DeckReason",     "The Deck of Reason",      "bold", 133),
    ("DeckInstinct",   "The Deck of Instinct",    "bold", 133),
    ("DeckCombined",   "A Combined Deck",         "bold", 133),
    ("DeckAbove",      "The Deck Above",          "bold", 128),
    ("DeckBelow",      "The Deck Below",          "bold", 128),
    ("DeckWithin",     "The Deck Within",         "bold", 128),
    ("DeckWithout",    "The Deck Without",        "bold", 128),
    ("DeckBoth",       "Both as One",             "bold", 128),
    ("As",             "as",                      "normal", 40),
    ("So",             "so",                      "normal", 40),
    ("Or",             "or",                      "normal", 40),
    ("Comma",          ",",                       "normal", 8),
    ("SubtleTitle",    "THE SUBTLE LAYER",        "bold", MSG_W),
    ("HermeticTitle",  "THE HERMETIC LAYER",      "bold", MSG_W),
    ("SideReason",     "REASON",                  "small", 90),
    ("SideInstinct",   "INSTINCT",                "small", 90),
    ("SideAbove",      "ABOVE",                   "small", 90),
    ("SideBelow",      "BELOW",                   "small", 90),
    ("SideWithin",     "WITHIN",                  "small", 90),
    ("SideWithout",    "WITHOUT",                 "small", 90),
    ("Shiny",          "SHINY",                   "small", 40),
]


def fail(msg):
    raise SystemExit("  port_arcana: " + msg)


def widths():
    w, cm = fontwidth.font(ENGINE)
    small = fontwidth.glyph_widths("sFontSmallLatinGlyphWidths", ENGINE)
    return w, small, cm


def measure(s, kind, W):
    w, small, cm = W
    table = small if kind == "small" else w
    total = 0
    for ch in s:
        if ch not in cm:
            fail("the game cannot print %r (in %r)" % (ch, s))
        total += table[cm[ch]] + (1 if kind == "bold" else 0)
    return total


def wrap(text, width, fits):
    out, cur = [], ""
    for word in text.split(" "):
        t = (cur + " " + word) if cur else word
        if fits(t, width):
            cur = t
        else:
            if not cur:
                fail("a word wider than its line: %r" % word)
            out.append(cur)
            cur = word
    return out + [cur]


def species_constants():
    sp = json.load(open(os.path.join(COMPANION, "species.json")))
    by_name = {}
    for idx, s in sp.items():
        by_name.setdefault(s["name"], s.get("constant"))
    hdr = open(os.path.join(ENGINE, "include/constants/species.h")).read()
    known = set(re.findall(r"#define (SPECIES_\w+)", hdr))
    return by_name, known


def c_text(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


def png_palette(path):
    from PIL import Image
    im = Image.open(path)
    if im.mode != "P" or im.size not in ((72, 104),):
        fail("%s is not a 72x104 indexed frame" % path)
    p = im.getpalette()[:48]
    p += [0] * (48 - len(p))
    return [(p[i * 3] >> 3, p[i * 3 + 1] >> 3, p[i * 3 + 2] >> 3) for i in range(16)]


def deck_tile():
    """The cover's tile: the back at half size (box-filtered, then each pixel the nearest of the back's own colours),
    three of them squared up two pixels apart, in a 64x64 sprite on the back's palette."""
    import numpy as np
    from PIL import Image
    b = Image.open(os.path.join(ART, "back.png"))
    pal = np.array(b.getpalette()[:48]).reshape(16, 3).astype(float)
    a = np.array(b)
    rgb = Image.fromarray(np.array(b.convert("RGB")))
    alpha = Image.fromarray(((a != 0) * 255).astype(np.uint8))
    w, h = 36, 52
    sm = np.array(rgb.resize((w, h), Image.BOX)).astype(float)
    al = np.array(alpha.resize((w, h), Image.BOX))
    d = ((sm[:, :, None, :] - pal[None, None, 1:, :]) ** 2).sum(-1)
    idx = d.argmin(-1) + 1
    idx[al < 128] = 0
    tile = np.zeros((64, 64), np.uint8)
    for k in (2, 1, 0):                                 # the bottom card first, down and right
        x, y = 2 + 2 * k, 2 + 2 * (2 - k)
        m = idx > 0
        tile[y:y + h, x:x + w][m] = idx[m]
    im = Image.fromarray(tile, "P")
    im.putpalette(b.getpalette()[:48] + [0] * (768 - 48))
    return im


def build():
    W = widths()
    arcana = json.load(open(os.path.join(COMPANION, "arcana.json")))
    by_name, known = species_constants()
    cards = arcana["cards"]
    if len(cards) != 22 or [c["n"] for c in cards] != list(range(22)):
        fail("arcana.json does not hold the twenty-two cards in order")
    rows, problems, longest = [], [], (0, "")
    for c in cards:
        faces = []
        for side in SIDES:
            f = c.get(side)
            if f is None:
                fail("card %s has no %s face" % (c["roman"], side))
            kw, ph, name = f["keyword"], f["phrase"], f["species"]
            const = by_name.get(name)
            if const is None or "SPECIES_" + const not in known:
                problems.append("%s %s: no daemon %r" % (c["roman"], side, name))
                const = "NONE"
            for s in (kw, ph):
                bad = set(s) - ALLOWED
                if bad:
                    problems.append("%s %s: cannot print %s in %r" % (c["roman"], side, sorted(bad), s))
            if len(kw.replace(" ", "")) > 12 or len(kw) > 15:
                problems.append("%s %s: keyword %r over twelve letters" % (c["roman"], side, kw))
            card_lines = wrap(ph.upper(), PANEL_CHARS, lambda t, n: len(t) <= n)
            if len(card_lines) > PANEL_LINES:
                problems.append("%s %s: phrase %r is %d lines on the card (%d fit)"
                                % (c["roman"], side, ph, len(card_lines), PANEL_LINES))
            read_lines = wrap(ph, READ_W, lambda t, n: measure(t, "normal", W) <= n)
            if len(read_lines) > READ_LINES:
                problems.append("%s %s: phrase is %d lines on its page" % (c["roman"], side, len(read_lines)))
            if measure(kw, "bold", W) > READ_W:
                problems.append("%s %s: keyword %r wider than the page's column" % (c["roman"], side, kw))
            if len(ph) > longest[0]:
                longest = (len(ph), ph)
            faces.append(dict(kw=kw, ph=ph, const=const, name=name))
        rows.append((c["roman"], faces))
    ui = []
    for name, text, kind, limit in UI:
        px = measure(text, kind, W)
        if px > min(limit, MSG_W):
            problems.append("interface %s %r is %dpx (%d fit)" % (name, text, px, limit))
        ui.append((name, text, px, limit))
    return rows, ui, problems, longest


def header(rows, ui, pals, backpal):
    L = ["// Generated by DAEMONS tools/port_arcana.py from the companion's server/data/arcana.json and",
         "// gfx/drafts/t509_cards/ -- edit those, not this. T-509: the tarot decks in both books.",
         "// DRAFT WORDING, every string: the faces' words are THE SUBTLE LAYER session's, the interface's the game lane's.",
         "",
         "#define ARCANA_CARDS 22",
         "enum { CARD_REASON, CARD_INSTINCT, CARD_ABOVE, CARD_BELOW, CARD_SIDES };",
         "struct ArcanaFace { const u8 *keyword; const u8 *phrase; u16 species; };",
         "struct ArcanaCard { const u8 *roman; struct ArcanaFace face[CARD_SIDES]; };",
         ""]
    for i, (roman, faces) in enumerate(rows):
        L.append('static const u8 sArcanaRoman_%d[] = _("%s");' % (i, roman))
        for side, f in zip(SIDES, faces):
            L.append('static const u8 sArcanaKw_%d_%s[] = _("%s");' % (i, side, c_text(f["kw"])))
            L.append('static const u8 sArcanaPh_%d_%s[] = _("%s");' % (i, side, c_text(f["ph"])))
    L += ["", "static const struct ArcanaCard sArcana[ARCANA_CARDS] =", "{"]
    for i, (roman, faces) in enumerate(rows):
        L.append("    {   // %s" % roman)
        L.append("        sArcanaRoman_%d," % i)
        L.append("        {")
        for side, f in zip(SIDES, faces):
            L.append('            { sArcanaKw_%d_%s, sArcanaPh_%d_%s, SPECIES_%s },   // %s'
                     % (i, side, i, side, f["const"], f["name"]))
        L.append("        },")
        L.append("    },")
    L += ["};", ""]
    for fr in FRAMES:
        L.append('static const u32 sCardFrame_%s[] = INCBIN_U32("%s/frame_%s.4bpp");' % (fr, OUT_GFX, fr))
    L.append('static const u32 sCardBack[] = INCBIN_U32("%s/back.4bpp");' % OUT_GFX)
    L.append('static const u32 sCardDeckTile[] = INCBIN_U32("%s/deck_tile.4bpp");' % OUT_GFX)
    L += ["", "static const u32 *const sCardFrames[CARD_SIDES][2] =", "{"]
    for s in SIDES:
        L.append("    { sCardFrame_%s, sCardFrame_%s_shiny }," % (s, s))
    L += ["};", "", "static const u16 sCardPals[CARD_SIDES][2][16] =", "{"]
    for s in SIDES:
        L.append("    {")
        for v in ("", "_shiny"):
            L.append("        { " + ", ".join("RGB(%d, %d, %d)" % c for c in pals[s + v]) + " },")
        L.append("    },")
    L += ["};", "", "static const u16 sCardBackPal[16] = { " + ", ".join("RGB(%d, %d, %d)" % c for c in backpal) + " };", ""]
    L.append("// the 3x5 letters the frames carry, by the game's own byte (a small letter drawn as its capital): rows top")
    L.append("// to bottom, three bits a row, the left one high")
    L.append("static const u16 sCardGlyphs[256] =")
    L.append("{")
    cm = fontwidth.charmap(ENGINE)
    seen = set()
    for ch in sorted(set(FONT) | set(c.lower() for c in FONT if c.isalpha()), key=ord):
        bits = int(FONT[ch.upper()], 2)
        if bits == 0 or cm[ch] in seen:
            continue
        seen.add(cm[ch])
        L.append("    [0x%02X] = 0x%04X,   // %s" % (cm[ch], bits, ch))
    L += ["};", "","// the section's words (DRAFT): text, and its width as measured"]
    for name, text, px, limit in ui:
        L.append('static const u8 sCardsText_%s[] = _("%s");   // %dpx' % (name, c_text(text), px))
    L.append("")
    return "\n".join(L) + "\n"


def main():
    from PIL import Image
    rows, ui, problems, longest = build()
    pals = {fr: png_palette(os.path.join(ART, "frame_%s.png" % fr)) for fr in FRAMES}
    backpal = png_palette(os.path.join(ART, "back.png"))
    text = header(rows, ui, pals, backpal)
    print("  port_arcana: 22 cards x 4 faces read; the longest phrase %d characters: %r" % longest)
    for name, t, px, limit in ui:
        if px > limit * 0.9:
            print("    close: %s %r %d/%dpx" % (name, t, px, limit))
    if problems:
        for p in problems:
            print("  PROBLEM: " + p)
        return 1
    targets = {OUT_H: text.encode()}
    for fr in FRAMES:
        targets["%s/frame_%s.png" % (OUT_GFX, fr)] = open(os.path.join(ART, "frame_%s.png" % fr), "rb").read()
    targets["%s/back.png" % OUT_GFX] = open(os.path.join(ART, "back.png"), "rb").read()
    import io
    buf = io.BytesIO()
    deck_tile().save(buf, format="PNG", transparency=0)
    tile = buf.getvalue()
    tile_path = "%s/deck_tile.png" % OUT_GFX
    changed = []
    for rel, data in targets.items():
        path = os.path.join(ENGINE, rel)
        old = open(path, "rb").read() if os.path.exists(path) else None
        if old != data:
            changed.append(rel)
    # the tile is drawn here, so compare its pixels and palette, not its PNG bytes
    tpath = os.path.join(ENGINE, tile_path)
    new_tile = Image.open(io.BytesIO(tile))
    if not os.path.exists(tpath) or Image.open(tpath).tobytes() != new_tile.tobytes() \
            or Image.open(tpath).getpalette()[:48] != new_tile.getpalette()[:48]:
        changed.append(tile_path)
    if not WRITE:
        print("  %s" % ("would write: " + ", ".join(changed) if changed else "the engine is up to date"))
        return 0
    for rel in changed:
        path = os.path.join(ENGINE, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        data = tile if rel == tile_path else targets[rel]
        tmp = path + ".tmp"
        open(tmp, "wb").write(data)
        os.replace(tmp, path)
        print("  wrote " + rel)
    return 0


if __name__ == "__main__":
    sys.exit(main())
