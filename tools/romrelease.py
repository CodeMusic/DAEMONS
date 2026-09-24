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

THE FOLDER, at the repo root. Its NOTES are in git -- the release notes, a sealed group's PDF and the hidden
`.release.json` -- and its ROMS never are: they run Nintendo's engine, and this repo promises not to distribute it
(the user's, 2026-09-24: ROM RELEASE/WHERES_THE_ROMS.md says so to anyone who looks). So after a release or a seal,
commit what it wrote; the ROMs are ignored by pattern and will not follow.

    ROM RELEASE/
      v11.281.x/                      an OPEN group: one folder per release
        v11.281.1/
          daemonsContent.gba          CONTENT
          daemonsContext.gba          CONTEXT
          DEBUG/                      the two testing builds
          PATCHES/                    four BPS patches, one per retail ROM (below)
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

AND A PATCH FOR EACH RETAIL ROM. `PATCHES/` in every release holds four BPS patches (tools/bps.py) -- CONTENT for
FireRed 1.0 and Rev 1, CONTEXT for LeafGreen 1.0 and Rev 1 -- since a patch applies only to the exact ROM it was made
from and both revisions are common. The sources are pret's own builds of upstream, which are byte-identical to
retail (each checked against pret's .sha1), kept in ~/.cache/daemons and never in any repo. The patches are
gitignored for their size (2.5MB each, four a release); they are what gets published, not the ROMs.

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
CACHE = os.path.join(os.path.expanduser("~"), ".cache/daemons/pokefirered-upstream")
#  (our ROM, the patch's file, pret's build of the retail ROM, its .sha1 file, what the player owns)
PATCHES = [
    ("daemonsContent.gba", "DAEMONS CONTENT for FireRed 1.0.bps", "pokefirered.gba", "firered.sha1",
     "Pokemon FireRed (USA) 1.0"),
    ("daemonsContent.gba", "DAEMONS CONTENT for FireRed Rev 1.bps", "pokefirered_rev1.gba", "firered_rev1.sha1",
     "Pokemon FireRed (USA, Europe) Rev 1"),
    ("daemonsContext.gba", "DAEMONS CONTEXT for LeafGreen 1.0.bps", "pokeleafgreen.gba", "leafgreen.sha1",
     "Pokemon LeafGreen (USA) 1.0"),
    ("daemonsContext.gba", "DAEMONS CONTEXT for LeafGreen Rev 1.bps", "pokeleafgreen_rev1.gba", "leafgreen_rev1.sha1",
     "Pokemon LeafGreen (USA, Europe) Rev 1"),
]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bps


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


def retail_sources(build):
    """pret's upstream, built in a worktree in ~/.cache: byte-identical to the retail ROMs, checked by hash."""
    missing = [p for _, _, p, h, _ in PATCHES if not os.path.exists(os.path.join(CACHE, p))]
    if missing and not build:
        print("  !! no clean retail builds in %s yet -- --write makes them (pret upstream, a few minutes)" % CACHE)
        return False
    if missing:
        if not os.path.isdir(CACHE):
            subprocess.run(["git", "-C", GBA, "fetch", "-q", "upstream"], check=True)
            subprocess.run(["git", "-C", GBA, "worktree", "add", "-q", "--detach", CACHE, "upstream/master"], check=True)
            os.symlink(os.path.join(os.path.realpath(GBA), "tools/agbcc"), os.path.join(CACHE, "tools/agbcc"))
        for target in ("firered", "firered_rev1", "leafgreen", "leafgreen_rev1"):
            if subprocess.run(["make", "-C", CACHE, target, "-j8"], capture_output=True).returncode:
                raise SystemExit("  refused: pret's `make %s` failed in %s" % (target, CACHE))
    for _, _, rom, hashfile, _ in PATCHES:
        want = open(os.path.join(CACHE, hashfile)).read().split()[0]
        if sha1(os.path.join(CACHE, rom)) != want:
            raise SystemExit("  refused: %s is not the retail ROM (SHA-1 differs from pret's %s)" % (rom, hashfile))
    return True


def make_patches(dest):
    os.makedirs(os.path.join(dest, "PATCHES"), exist_ok=True)
    rows = []
    for ours, name, rom, hashfile, owned in PATCHES:
        src = open(os.path.join(CACHE, rom), "rb").read()
        tgt = open(os.path.join(dest, ours), "rb").read()
        patch = bps.create(src, tgt)
        if bps.apply(src, patch) != tgt:
            raise SystemExit("  refused: %s does not reproduce %s" % (name, ours))
        open(os.path.join(dest, "PATCHES", name), "wb").write(patch)
        rows.append((name, owned, open(os.path.join(CACHE, hashfile)).read().split()[0], len(patch)))
        print("  patched %s (%d KB, checked by applying it)" % (name, len(patch) // 1024))
    return rows


def patch_notes(rows):
    out = ["## Patches", "",
           "*Apply one to the ROM it names, in any BPS patcher (Rom Patcher JS works in a browser). Each checks the "
           "ROM's CRC and refuses the wrong one.*", "",
           "| patch | apply it to | that ROM's SHA-1 |", "|---|---|---|"]
    for name, owned, digest, size in rows:
        out.append("| `PATCHES/%s` | %s | `%s` |" % (name, owned, digest))
    return "\n".join(out) + "\n"


def release():
    bible = bible_version()
    group = "v%s.x" % bible
    existing = releases(group) if os.path.isdir(os.path.join(REL, group)) else []
    sealed = os.path.isdir(os.path.join(REL, group)) and not existing and os.path.exists(os.path.join(REL, group, ".release.json"))
    if sealed:
        raise SystemExit("  %s is sealed; bump the design bible before releasing again" % group)
    n = int(existing[-1].rsplit(".", 1)[1]) + 1 if existing else 1
    version = "%s.%d" % (bible, n)
    #  the release folder itself is not "dirty": a seal deletes tracked notes, and that is the tool's own work
    dirty = [name for name, repo in (("engine", GBA), ("docs", ROOT))
             if git(repo, "status", "--porcelain", "--untracked-files=no", "--", ".", ":!ROM RELEASE")]
    print("  design bible v%s: the next release is v%s, in %s/" % (bible, version, group))
    for g in groups():
        if g != group and releases(g):
            seal(g)
    if dirty:
        print("  !! uncommitted changes in the %s tree -- a release would not match its notes" % " and ".join(dirty))
    retail_sources(WRITE)
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
    rows = make_patches(dest)
    open(os.path.join(dest, "RELEASE_NOTES.md"), "w", encoding="utf-8").write(
        notes(version, bible, rec, engine, docs, roms) + "\n" + patch_notes(rows))
    json.dump({"version": version, "bible": bible, "engine": engine, "docs": docs,
               "made": datetime.datetime.now().isoformat(timespec="seconds")},
              open(os.path.join(dest, ".release.json"), "w"), indent=1)
    print("  released v%s -> %s  (commit its notes; the ROMs stay out of git)" % (version, os.path.relpath(dest, ROOT)))
    return 0


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "seal":
        seal(sys.argv[2])
        return 0
    if len(sys.argv) > 2 and sys.argv[1] == "patch":
        #  patches for a release filed before there were patches: `patch v11.281.2 --write`
        dest = os.path.join(REL, "v%s.x" % sys.argv[2][1:].rsplit(".", 1)[0], sys.argv[2])
        print("  patches for %s" % os.path.relpath(dest, ROOT))
        if WRITE and retail_sources(True):
            rows = make_patches(dest)
            with open(os.path.join(dest, "RELEASE_NOTES.md"), "a", encoding="utf-8") as f:
                f.write("\n" + patch_notes(rows))
        return 0
    return release()


if __name__ == "__main__":
    sys.exit(main())
