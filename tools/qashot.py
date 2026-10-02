#!/usr/bin/env python3
"""File a QA screenshot in qa/screenshots/, where GitHub shows it (the user, 2026-10-02).

    python3 tools/qashot.py --ticket T-297 --name "FOLDS corner of paper" --caption "the painting, before and after" FILE
    python3 tools/qashot.py --ticket T-335 --caption "the dated pages" --private FILE ...
    python3 tools/qashot.py --list            # what is filed, public and private

Every picture sent to the user is filed here too. Each is copied into qa/screenshots/<YYYY-MM-DD>/ named the user's
way (2026-10-02): the day it was taken, the ticket if there is one, a short name for what it shows, and its number
that day -- "21Sept2026 - T121 - REVEALER Found in One Island - 1.png". The number counts the public and private
folders together, so a day's numbers never repeat. That day's README.md gains the caption and the picture, so the
folder reads as a gallery on GitHub.

--private files into qa/screenshots/private/<date>/ instead, which is gitignored: anything that shows a NOTEBOOK
page, anything drawn from docs/private/, or any of the four things CLAUDE.md never puts in public writing. **When in
doubt, private** -- a picture can be moved to the public folder later, and never un-published. A public filing
whose file name or caption sounds private (PRIVATE_HINTS) is refused unless --public says it was looked at.

Filing the same picture twice does nothing; a different picture under a name already filed is refused.
"""
import argparse, datetime, filecmp, os, re, shutil, sys, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOTS = os.path.join(ROOT, "qa", "screenshots")
PRIVATE = os.path.join(SHOTS, "private")
PRIVATE_HINTS = ("notebook", "page", "loose", "correspondence", "prospectus", "lab notes", "lab_notes", "run log",
                 "run_log", "the file", "peer review", "story", "secret", "private", "witness", "engraving", "t335",
                 "t-335", "t336", "t-336")


MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec")


def stamp(date):
    y, m, d = (int(v) for v in date.split("-"))
    return "%d%s%d" % (d, MONTHS[m - 1], y)


def clean(s):
    """A name safe in a file name on every system: no slashes, colons or quotes."""
    return re.sub(r"\s+", " ", re.sub(r"[^A-Za-z0-9 .,()&+=-]", "", s)).strip()


def next_index(date):
    n = 0
    for top in (SHOTS, PRIVATE):
        day = os.path.join(top, date)
        if os.path.isdir(day):
            for f in os.listdir(day):
                m = re.search(r" - (\d+)\.[a-z]+$", f)
                if m:
                    n = max(n, int(m.group(1)))
    return n + 1


def file_one(src, ticket, name, date, private):
    if not os.path.isfile(src):
        raise SystemExit("  refused: %s does not exist" % src)
    day = os.path.join(PRIVATE if private else SHOTS, date)
    os.makedirs(day, exist_ok=True)
    ext = os.path.splitext(src)[1].lower()
    for top in (SHOTS, PRIVATE):                               # the same picture filed that day already
        other = os.path.join(top, date)
        for f in (os.listdir(other) if os.path.isdir(other) else []):
            if f != "README.md" and filecmp.cmp(src, os.path.join(other, f), shallow=False):
                print("  already filed: %s" % os.path.relpath(os.path.join(other, f), ROOT))
                return None
    parts = [stamp(date)] + ([re.sub(r"[^A-Za-z0-9]", "", ticket).upper()] if ticket else []) + [clean(name)]
    name = " - ".join(parts + [str(next_index(date))]) + ext
    dest = os.path.join(day, name)
    shutil.copyfile(src, dest)
    print("  filed %s" % os.path.relpath(dest, ROOT))
    return name


def note(date, private, caption, names):
    readme = os.path.join(PRIVATE if private else SHOTS, date, "README.md")
    new = not os.path.exists(readme)
    with open(readme, "a") as f:
        if new:
            f.write("# QA screenshots, %s%s\n\nIn the order they were taken, each with the caption it was sent with. "
                    "Every word in them is a DRAFT until approved.\n" % (date, " (private)" if private else ""))
        for n in names:
            stem = os.path.splitext(n)[0]
            f.write("\n### %s\n\n%s\n\n![%s](%s)\n" % (stem, caption, stem, urllib.parse.quote(n)))


def listing():
    for label, top in (("public", SHOTS), ("private (gitignored)", PRIVATE)):
        days = sorted(d for d in os.listdir(top) if re.fullmatch(r"\d{4}-\d\d-\d\d", d)) if os.path.isdir(top) else []
        count = sum(len([f for f in os.listdir(os.path.join(top, d)) if f != "README.md"]) for d in days)
        print("  %s: %d pictures over %d days%s" % (label, count, len(days), (", latest " + days[-1]) if days else ""))


def main():
    ap = argparse.ArgumentParser(description="File QA screenshots in qa/screenshots/.")
    ap.add_argument("files", nargs="*")
    ap.add_argument("--ticket", default="", help="the TODO id the pictures are for, e.g. T-297")
    ap.add_argument("--name", default="", help="a few words for what it shows; the file is named with it")
    ap.add_argument("--caption", default="", help="one line, the same as the caption sent to the user")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--private", action="store_true", help="file in the gitignored private folder")
    ap.add_argument("--public", action="store_true", help="file publicly although the name or caption sounds private")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    if a.list or not a.files:
        listing()
        return
    if not a.caption or not a.name:
        raise SystemExit("  refused: --name and --caption are both needed (the file is named with one, the gallery "
                         "shows the other)")
    if not a.private and not a.public:
        said = " ".join([a.caption, a.name, a.ticket] + [os.path.basename(f) for f in a.files]).lower()
        hit = [h for h in PRIVATE_HINTS if h in said]
        if hit:
            raise SystemExit("  refused: this sounds private (%s). File it with --private, or with --public once "
                             "you have looked and it is not." % ", ".join(hit))
    names = [n for n in (file_one(f, a.ticket, a.name, a.date, a.private) for f in a.files) if n]
    if names:
        note(a.date, a.private, a.caption, names)


if __name__ == "__main__":
    sys.exit(main())
