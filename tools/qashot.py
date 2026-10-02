#!/usr/bin/env python3
"""File a QA screenshot in qa/screenshots/, where GitHub shows it (the user, 2026-10-02).

    python3 tools/qashot.py --ticket T-297 --caption "FOLDS' corner of paper, before and after" FILE [FILE ...]
    python3 tools/qashot.py --ticket T-335 --caption "the dated pages" --private FILE ...
    python3 tools/qashot.py --list            # what is filed, public and private

Every picture sent to the user is filed here too. Each is copied into qa/screenshots/<date>/ as
<ticket>_<name>.png, and that day's README.md gains the caption and the picture, so a day's folder reads as a gallery
on GitHub.

--private files into qa/screenshots/private/<date>/ instead, which is gitignored: anything that shows a NOTEBOOK
page, anything drawn from docs/private/, or any of the four things CLAUDE.md never puts in public writing. **When in
doubt, private** -- a picture can be moved to the public folder later, and never un-published. A public filing
whose file name or caption sounds private (PRIVATE_HINTS) is refused unless --public says it was looked at.

Filing the same picture twice does nothing; a different picture under a name already filed is refused.
"""
import argparse, datetime, filecmp, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOTS = os.path.join(ROOT, "qa", "screenshots")
PRIVATE = os.path.join(SHOTS, "private")
PRIVATE_HINTS = ("notebook", "page", "loose", "correspondence", "prospectus", "lab notes", "lab_notes", "run log",
                 "run_log", "the file", "peer review", "story", "secret", "private", "witness", "engraving", "t335",
                 "t-335", "t336", "t-336")


def slug(s):
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def file_one(src, ticket, caption, date, private):
    if not os.path.isfile(src):
        raise SystemExit("  refused: %s does not exist" % src)
    day = os.path.join(PRIVATE if private else SHOTS, date)
    os.makedirs(day, exist_ok=True)
    base, ext = os.path.splitext(os.path.basename(src))
    tag, stem = re.sub(r"[^a-z0-9]", "", ticket.lower()), slug(base)
    name = (stem if not tag or stem.startswith(tag) else tag + "_" + stem) + ext.lower()
    dest = os.path.join(day, name)
    if os.path.exists(dest):
        if filecmp.cmp(src, dest, shallow=False):
            print("  already filed: %s" % os.path.relpath(dest, ROOT))
            return None
        raise SystemExit("  refused: %s is filed already with different contents -- rename the source" %
                         os.path.relpath(dest, ROOT))
    shutil.copyfile(src, dest)
    print("  filed %s" % os.path.relpath(dest, ROOT))
    return name


def note(date, private, ticket, caption, names):
    readme = os.path.join(PRIVATE if private else SHOTS, date, "README.md")
    new = not os.path.exists(readme)
    with open(readme, "a") as f:
        if new:
            f.write("# QA screenshots, %s%s\n\nDecoded from the built ROM unless a caption says otherwise. "
                    "Every word in them is a DRAFT until approved.\n" % (date, " (private)" if private else ""))
        f.write("\n### %s%s\n\n" % (ticket + " -- " if ticket else "", caption))
        for n in names:
            f.write("![%s](%s)\n" % (caption.replace("]", ")").replace("[", "("), n.replace(" ", "%20")))


def listing():
    for label, top in (("public", SHOTS), ("private (gitignored)", PRIVATE)):
        days = sorted(d for d in os.listdir(top) if re.fullmatch(r"\d{4}-\d\d-\d\d", d)) if os.path.isdir(top) else []
        count = sum(len([f for f in os.listdir(os.path.join(top, d)) if f != "README.md"]) for d in days)
        print("  %s: %d pictures over %d days%s" % (label, count, len(days), (", latest " + days[-1]) if days else ""))


def main():
    ap = argparse.ArgumentParser(description="File QA screenshots in qa/screenshots/.")
    ap.add_argument("files", nargs="*")
    ap.add_argument("--ticket", default="", help="the TODO id the pictures are for, e.g. T-297")
    ap.add_argument("--caption", default="", help="one line, the same as the caption sent to the user")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--private", action="store_true", help="file in the gitignored private folder")
    ap.add_argument("--public", action="store_true", help="file publicly although the name or caption sounds private")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    if a.list or not a.files:
        listing()
        return
    if not a.caption:
        raise SystemExit("  refused: --caption is needed (the gallery shows it)")
    if not a.private and not a.public:
        said = " ".join([a.caption, a.ticket] + [os.path.basename(f) for f in a.files]).lower()
        hit = [h for h in PRIVATE_HINTS if h in said]
        if hit:
            raise SystemExit("  refused: this sounds private (%s). File it with --private, or with --public once "
                             "you have looked and it is not." % ", ".join(hit))
    names = [n for n in (file_one(f, a.ticket, a.caption, a.date, a.private) for f in a.files) if n]
    if names:
        note(a.date, a.private, a.ticket, a.caption, names)


if __name__ == "__main__":
    sys.exit(main())
