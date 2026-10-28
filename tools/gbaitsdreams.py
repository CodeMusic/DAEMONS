#!/usr/bin/env python3
"""T-462 (C-200, the user by multiple choice, 2026-10-28): the NOTEBOOK's DREAM LOG -- ITS DREAMS.

    python3 tools/gbaitsdreams.py            # report: every line measured, and whether the header is current
    python3 tools/gbaitsdreams.py --write    # engineGba/src/data/its_dreams.h

The carried daemon's dreams. The companion (daemons-companion, C-200) judges a night and writes only a NUMBER into the
save at SYNC -- VAR_ITS_DREAM: the night's quality (1 broken, 2 quiet, 3 vivid; bit 2 tucked in) and above it the
image, one of the sixteen in `docs/its_dreams.json`. The words are the ROM's, every one DRAFT. notebook.c files the
image at the first dawn after it arrives (as YOUR DREAMS are), says it after the line naming the daemon carried, and
lists it under ITS DREAMS by its title; its page ends with the ending of the quality last received for it.

It holds the words to the design and refuses what would break it:
  - sixteen dreams, images 0..15 in order, each key and title its own;
  - a title is ALL CAPS, at most TITLE_W, and never a number (the lock's rule: nothing in a dream counts, numbers or
    paces anything) -- and no telling carries a digit or a counting word either;
  - every box is one or two lines, and no line is wider than the 208px message box ({STR_VAR_1}, a daemon's name,
    is measured as ten of the widest capital);
  - dreamt while SUSPENDED: no SLEEP, SLEPT, ASLEEP, WAKE or WOKE anywhere in its words (vision 2.7's status row:
    "Not gone, not scheduled, and it resumes");
  - the arrival line and any dream fit gStringVar4 (1000 bytes) together;
  - flags.h defines FLAG_ITS_DREAM_<KEY> for each, consecutive in image order (notebook.c files FIRST + image).
"""
import io, contextlib, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
SRC = os.path.join(ROOT, "docs", "its_dreams.json")
OUT = os.path.join(GBA, "src", "data", "its_dreams.h")
WRITE = "--write" in sys.argv
BOX = 208
TITLE_W = 130      # tools/gbadreamlog.py's: the NOTEBOOK's list keeps the width the other sections use
COUNT = 16         # the companion's image is four bits (C-200, dreams.ts dreamImage)
ENDINGS = ("broken", "quiet", "vivid")   # quality 1, 2, 3
NAME_LEN = 10      # POKEMON_NAME_LENGTH
NOT_SUSPENDED = re.compile(r"\b(SLEEP\w*|SLEPT|ASLEEP|WAKE\w*|WOKE\w*|AWAKE\w*)\b", re.I)
COUNTING = re.compile(r"\b(TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN|ELEVEN|TWELVE|HUNDRED|THOUSAND|"
                      r"COUNT\w*|NUMBER\w*|FIRST|SECOND|THIRD|TWICE|THRICE)\b", re.I)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
argv, sys.argv = sys.argv, [sys.argv[0]]
with contextlib.redirect_stdout(io.StringIO()):
    from genguide import width   # noqa: E402  (the game's font, read from the engine)
sys.argv = argv

WIDEST_CAP = max(width(c) for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ")


def measure(line):
    """A line's width; {STR_VAR_1} is a daemon's name, at its longest and widest."""
    return width(line.replace("{STR_VAR_1}", "")) + (NAME_LEN * WIDEST_CAP if "{STR_VAR_1}" in line else 0)


def c(s):
    return s.replace('"', '\\"')


def box_text(box):
    return "\\n".join(box)


def check_box(box, where, bad):
    if not isinstance(box, list) or not 1 <= len(box) <= 2:
        bad.append("%s: a box is one or two lines" % where)
        return
    for line in box:
        if measure(line) > BOX:
            bad.append("%s: %dpx > %d: %s" % (where, measure(line), BOX, line))


def main():
    doc = json.load(open(SRC, encoding="utf-8"))
    flags_h = open(os.path.join(GBA, "include/constants/flags.h"), encoding="utf-8").read()
    bad = []
    h = doc["heading"]
    if h != h.upper() or width(h) > TITLE_W or re.search(r"\d", h):
        bad.append("the heading %r must be capitals within %dpx, no number" % (h, TITLE_W))
    for k in ("line_named", "line_unnamed"):
        check_box(doc[k], k, bad)
    if not any("{STR_VAR_1}" in l for l in doc["line_named"]):
        bad.append("line_named does not name the daemon ({STR_VAR_1})")
    dreams = doc["dreams"]
    if [d.get("image") for d in dreams] != list(range(COUNT)):
        bad.append("the dreams must be images 0..%d, in order" % (COUNT - 1))
    keys, titles = set(), set()
    offsets = {}
    for d in dreams:
        key, t = d["key"], d["title"]
        if key in keys or t in titles:
            bad.append("image %d: its key or title is not its own (%s, %s)" % (d["image"], key, t))
        keys.add(key)
        titles.add(t)
        if t != t.upper() or width(t) > TITLE_W or re.search(r"\d", t) or COUNTING.search(t):
            bad.append("image %d: the title %r must be capitals within %dpx (it is %dpx), no number"
                       % (d["image"], t, TITLE_W, width(t)))
        for part in ("open",) + ENDINGS:
            check_box(d.get(part), "image %d %s" % (d["image"], part), bad)
        said = " ".join([t] + [l for part in ("open",) + ENDINGS for l in d.get(part, [])])
        if re.search(r"\d", said) or COUNTING.search(said):
            bad.append("image %d counts or numbers something -- a dream never does: %s"
                       % (d["image"], (COUNTING.search(said) or re.search(r"\d", said)).group(0)))
        if NOT_SUSPENDED.search(said):
            bad.append("image %d says %r -- it is SUSPENDED, never asleep, and it resumes"
                       % (d["image"], NOT_SUSPENDED.search(said).group(0)))
        line = max(len(box_text(doc["line_named"])) + NAME_LEN, len(box_text(doc["line_unnamed"])))
        for e in ENDINGS:
            if line + 2 + len(box_text(d["open"])) + 2 + len(box_text(d[e])) >= 1000:
                bad.append("image %d %s: does not fit gStringVar4 with the line" % (d["image"], e))
        m = re.search(r"^#define\s+FLAG_ITS_DREAM_%s\s+\(DAEMONS_FLAGS_START \+ (0x[0-9A-Fa-f]+)\)" % key, flags_h, re.M)
        if not m:
            bad.append("image %d: flags.h defines no FLAG_ITS_DREAM_%s" % (d["image"], key))
        else:
            offsets[d["image"]] = int(m.group(1), 16)
    for w in ("line_named", "line_unnamed"):
        if NOT_SUSPENDED.search(" ".join(doc[w])):
            bad.append("%s says %r" % (w, NOT_SUSPENDED.search(" ".join(doc[w])).group(0)))
    if len(offsets) == COUNT and any(offsets[i] != offsets[0] + i for i in range(COUNT)):
        bad.append("the FLAG_ITS_DREAM_ flags are not consecutive in image order (notebook.c files FIRST + image)")
    if bad:
        print("  refused:")
        for b in bad:
            print("   ", b)
        sys.exit(1)

    K = lambda d: d["key"].capitalize()
    out = ["// GENERATED by DAEMONS tools/gbaitsdreams.py from docs/its_dreams.json -- do not edit by hand.",
           "// T-462 (C-200, 2026-10-28): the DREAM LOG's ITS DREAMS -- the carried daemon's, dreamt while SUSPENDED and",
           "// written into the save by the companion as a number. Every word DRAFT. Included once, by notebook.c.",
           "#ifndef GUARD_DATA_ITS_DREAMS_H", "#define GUARD_DATA_ITS_DREAMS_H", "",
           "#define ITS_DREAM_COUNT %d" % COUNT, "",
           'static const u8 sDreamHeading_Its[] = _("%s");' % c(h),
           "//  Said before the dream as it is filed: {STR_VAR_1} the daemon carried, or none away.",
           'static const u8 sItsDreamLine_Named[] = _("%s");' % c(box_text(doc["line_named"])),
           'static const u8 sItsDreamLine_Unnamed[] = _("%s");' % c(box_text(doc["line_unnamed"])), ""]
    for d in dreams:
        out.append('static const u8 sItsDreamTitle_%s[] = _("%s");' % (K(d), c(d["title"])))
        out.append('static const u8 sItsDreamOpen_%s[] = _("%s");' % (K(d), c(box_text(d["open"]))))
        for e in ENDINGS:
            out.append('static const u8 sItsDreamEnd_%s_%s[] = _("%s");' % (K(d), e.capitalize(), c(box_text(d[e]))))
    out += ["", "//  ITS DREAMS' entries, in image order (notebook.c rule 2: the authored order, never the order dreamt); ARG",
            "//  is the image, for the ending of the quality last received for it (VAR_ITS_DREAM_KINDS).",
            "#define NB_ITS_DREAM_ENTRIES \\"]
    out += ["    { NB_DREAM_LOG, NB_KIND_ITS_DREAM, %d, FLAG_ITS_DREAM_%s, 0, sItsDreamTitle_%s, sItsDreamOpen_%s }, \\"
            % (d["image"], d["key"], K(d), K(d)) for d in dreams]
    out += ["", "", "//  Each image's endings: broken (quality 1), quiet (2), vivid (3).",
            "static const u8 *const sItsDreamEndings[ITS_DREAM_COUNT][3] =", "{"]
    out += ["    { sItsDreamEnd_%s_Broken, sItsDreamEnd_%s_Quiet, sItsDreamEnd_%s_Vivid },   // %d %s"
            % (K(d), K(d), K(d), d["image"], d["title"]) for d in dreams]
    out += ["};", "", "#endif // GUARD_DATA_ITS_DREAMS_H", ""]
    text = "\n".join(out)

    for d in dreams:
        print("  %2d %-24s %s" % (d["image"], "%s (%dpx)" % (d["title"], width(d["title"])),
                                  "  |  ".join("%s (%dpx)" % (l, measure(l)) for l in d["open"])))
        for e in ENDINGS:
            print("     %-24s %s" % ("  " + e, "  |  ".join("%s (%dpx)" % (l, measure(l)) for l in d[e])))
    print("  the line: %s  /  %s" % (" | ".join("%s (%dpx)" % (l, measure(l)) for l in doc["line_named"]),
                                     " | ".join("%s (%dpx)" % (l, measure(l)) for l in doc["line_unnamed"])))
    print("  %d dreams, three endings each; every line fits %dpx, every title %dpx; nothing counted, nothing slept"
          % (len(dreams), BOX, TITLE_W))
    old = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
    if old == text:
        print("  its_dreams.h is current")
    elif not WRITE:
        print("  its_dreams.h would change; pass --write")
    else:
        open(OUT, "w", encoding="utf-8").write(text)
        print("  written  src/data/its_dreams.h")


if __name__ == "__main__":
    main()
