#!/usr/bin/env python3
"""ROM releases: build the four ROMs, file them by version, and fold old versions away (the user's, 2026-09-24).

    python3 tools/romrelease.py                    # report: the version the next release would get, what would seal
    python3 tools/romrelease.py --write            # build all four ROMs and file a release (sealing older groups)
    python3 tools/romrelease.py --write --no-build # file the ROMs already built, without rebuilding
    python3 tools/romrelease.py seal v11.280.x --write   # seal one group by hand

THE VERSION IS THE DESIGN BIBLE'S, PLUS A RELEASE NUMBER. There was no ROM version before this, and the one version
the project has is `vision.md`'s (v11.281) -- the specification the ROM implements. So a release is
v<bible>.<n>: v11.281.1, v11.281.2, ... and every release made while the bible says v11.281 belongs to the GROUP
v11.281.x. A ROM therefore always says which design it was built against.

THE FOLDER, at the repo root, and never in git -- the ROMs carry Nintendo's code and this repo promises not to
distribute it (CLAUDE.md), so `ROM RELEASE/` is gitignored whole:

    ROM RELEASE/
      v11.281.x/                      an OPEN group: one folder per release
        v11.281.1/
          daemonsContent.gba          CONTENT
          daemonsContext.gba          CONTEXT
          DEBUG/                      the two testing builds
          RELEASE_NOTES.md            what changed since the release before it, and each ROM's SHA-1
        v11.281.2/ ...
      v11.280.x/                      a SEALED group: only its last release, flattened
        daemonsContent.gba
        daemonsContext.gba
        DEBUG/
        ReleaseNotes_v11.280.x.pdf    every release note the group had, newest first, in one document

SEALING happens when the bible moves on: the next release under a new version seals every older open group. The
latest release's ROMs move up into the group folder, the rest are deleted, and all the group's notes are read and
set as one PDF (pandoc and Chrome, docs/style.css, the same pipeline as docs/build-pdf.sh). A hidden
`.release.json` keeps the last release's commits, so the next release's notes can say what changed since.

A RELEASE IS REFUSED from a dirty engine or docs tree -- its notes list commits, and uncommitted work would be in
the ROM and not in the notes.
"""
import datetime, hashlib, json, os, re, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
REL = os.environ.get("ROM_RELEASE_DIR", os.path.join(ROOT, "ROM RELEASE"))   # overridable, for testing a seal
WRITE = "--write" in sys.argv
BUILD = "--no-build" not in sys.argv
TARGETS = [("firered", "daemonsContent.gba", False), ("leafgreen", "daemonsContext.gba", False),
           ("firered_debug", "daemonsContent_debug.gba", True), ("leafgreen_debug", "daemonsContext_debug.gba", True)]
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def git(repo, *args):
    return subprocess.run(["git", "-C", repo] + list(args), capture_output=True, text=True).stdout.strip()


def bible_version():
    if os.environ.get("ROM_RELEASE_BIBLE"):          # for testing a seal without bumping the bible
        return os.environ["ROM_RELEASE_BIBLE"]
    head = open(os.path.join(ROOT, "docs/vision.md"), encoding="utf-8").read(2000)
    return re.search(r"design bible, v(\d+\.\d+)", head).group(1)


def groups():
    if not os.path.isdir(REL):
        return []
    return sorted((g for g in os.listdir(REL) if re.fullmatch(r"v\d+\.\d+\.x", g)),
                  key=lambda g: tuple(int(n) for n in g[1:-2].split(".")))


def releases(group):
    d = os.path.join(REL, group)
    rs = [r for r in os.listdir(d) if re.fullmatch(re.escape(group[:-1]) + r"\d+", r)]
    return sorted(rs, key=lambda r: int(r.rsplit(".", 1)[1]))


def last_record():
    """The newest release anywhere, open or sealed: its commits are where the next notes start from."""
    for g in reversed(groups()):
        rs = releases(g)
        path = os.path.join(REL, g, rs[-1], ".release.json") if rs else os.path.join(REL, g, ".release.json")
        if os.path.exists(path):
            return json.load(open(path))
    return None


def sha1(path):
    return hashlib.sha1(open(path, "rb").read()).hexdigest()


def changelog_section(version):
    text = open(os.path.join(ROOT, "docs/CHANGELOG.md"), encoding="utf-8").read()
    m = re.search(r"^## v%s .*?(?=^## v|\Z)" % re.escape(version), text, re.S | re.M)
    return m.group(0).strip() if m else ""


def notes(version, bible, rec, engine, docs, roms):
    out = ["# DAEMONS v%s — release notes" % version, "",
           "*Released %s · built against the design bible v%s*" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), bible), "",
           "- **Engine**: CodeMusic/pokefirered-daemons `%s` (context-content)" % engine,
           "- **Design**: CodeMusic/DAEMONS `%s`" % docs, "",
           "| ROM | edition | SHA-1 |", "|---|---|---|"]
    for name, edition, digest in roms:
        out.append("| `%s` | %s | `%s` |" % (name, edition, digest))
    out.append("")
    if rec:
        out += ["## The engine since v%s" % rec["version"], ""]
        log = git(GBA, "log", "--format=- `%h` %s", "%s..%s" % (rec["engine"], engine))
        out += [log or "- *nothing: the same engine commit as the release before*", ""]
        out += ["## The design and tools since v%s" % rec["version"], ""]
        log = git(ROOT, "log", "--format=- `%h` %s", "%s..%s" % (rec["docs"], docs))
        out += [log or "- *nothing*", ""]
    else:
        out += ["*The first release: there is no earlier one to compare with.*", ""]
    if not rec or rec["bible"] != bible:
        section = changelog_section(bible)
        if section:
            out += ["## The design bible's own entry for v%s" % bible, "", re.sub(r"^## ", "### ", section, flags=re.M), ""]
    return "\n".join(out)


def render_pdf(md_text, out_pdf, title):
    with tempfile.TemporaryDirectory() as tmp:
        src, head, html = (os.path.join(tmp, n) for n in ("notes.md", "head.html", "notes.html"))
        open(src, "w", encoding="utf-8").write(md_text)
        open(head, "w", encoding="utf-8").write("<style>\n%s\n</style>\n" % open(os.path.join(ROOT, "docs/style.css")).read())
        subprocess.run(["pandoc", src, "--from=gfm", "--to=html5", "--standalone", "--metadata", "pagetitle=" + title,
                        "--include-in-header=" + head, "--output=" + html], check=True)
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer",
                        "--print-to-pdf-no-header", "--print-to-pdf=" + out_pdf, "file://" + html],
                       check=True, capture_output=True)


def seal(group):
    rs = releases(group)
    d = os.path.join(REL, group)
    if not rs:
        print("  %s is already sealed" % group)
        return
    latest = os.path.join(d, rs[-1])
    print("  seal %s: keep %s, fold %d release note(s) into ReleaseNotes_%s.pdf, delete %s"
          % (group, rs[-1], len(rs), group, ", ".join(rs[:-1]) or "nothing else"))
    if not WRITE:
        return
    body = ["# DAEMONS %s — release notes" % group, "",
            "*Every release made while the design bible was v%s, newest first. The ROMs beside this file are %s.*"
            % (group[1:-2], rs[-1]), ""]
    for r in reversed(rs):
        text = open(os.path.join(d, r, "RELEASE_NOTES.md"), encoding="utf-8").read()
        body += [re.sub(r"^(#+) ", r"#\1 ", text, flags=re.M), "", "---", ""]
    render_pdf("\n".join(body), os.path.join(d, "ReleaseNotes_%s.pdf" % group), "DAEMONS %s release notes" % group)
    for name in os.listdir(latest):
        if name != "RELEASE_NOTES.md":
            shutil.move(os.path.join(latest, name), os.path.join(d, name))
    for r in rs:
        shutil.rmtree(os.path.join(d, r))
    print("  sealed %s" % group)


def release():
    bible = bible_version()
    group = "v%s.x" % bible
    existing = releases(group) if os.path.isdir(os.path.join(REL, group)) else []
    sealed = os.path.isdir(os.path.join(REL, group)) and not existing and os.path.exists(os.path.join(REL, group, ".release.json"))
    if sealed:
        raise SystemExit("  %s is sealed; bump the design bible before releasing again" % group)
    n = int(existing[-1].rsplit(".", 1)[1]) + 1 if existing else 1
    version = "%s.%d" % (bible, n)
    dirty = [name for name, repo in (("engine", GBA), ("docs", ROOT)) if git(repo, "status", "--porcelain", "--untracked-files=no")]
    print("  design bible v%s: the next release is v%s, in %s/" % (bible, version, group))
    for g in groups():
        if g != group and releases(g):
            seal(g)
    if dirty:
        print("  !! uncommitted changes in the %s tree -- a release would not match its notes" % " and ".join(dirty))
    if not WRITE:
        return 0
    if dirty:
        raise SystemExit("  refused: commit first")
    if BUILD:
        for target, _, _ in TARGETS:
            r = subprocess.run(["make", "-C", GBA, target, "-j8"], capture_output=True, text=True)
            if r.returncode:
                raise SystemExit("  refused: `make %s` failed (exit %d)\n%s" % (target, r.returncode, r.stdout[-1500:] + r.stderr[-1500:]))
            print("  built %s" % target)
    rec = last_record()                  # before the new folder exists, or it finds itself
    dest = os.path.join(REL, group, "v" + version)
    os.makedirs(os.path.join(dest, "DEBUG"))
    roms = []
    for target, name, debug in TARGETS:
        src = os.path.join(GBA, name)
        shutil.copy2(src, os.path.join(dest, "DEBUG" if debug else "", name))
        roms.append(("DEBUG/" + name if debug else name,
                     ("CONTENT" if "Content" in name else "CONTEXT") + (" (testing build)" if debug else ""), sha1(src)))
    engine, docs = git(GBA, "rev-parse", "--short=9", "HEAD"), git(ROOT, "rev-parse", "--short=8", "HEAD")
    open(os.path.join(dest, "RELEASE_NOTES.md"), "w", encoding="utf-8").write(notes(version, bible, rec, engine, docs, roms))
    json.dump({"version": version, "bible": bible, "engine": engine, "docs": docs,
               "made": datetime.datetime.now().isoformat(timespec="seconds")},
              open(os.path.join(dest, ".release.json"), "w"), indent=1)
    print("  released v%s -> %s" % (version, os.path.relpath(dest, ROOT)))
    return 0


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "seal":
        seal(sys.argv[2])
        return 0
    return release()


if __name__ == "__main__":
    sys.exit(main())
