#!/usr/bin/env python3
"""Keep the documentation current at every release, read from WHAT'S NEW (T-544; the user, 2026-11-11: "during releases
we look back between now and the previous what's new -- and with that context, ensure git readme's, wiki's, manuals,
docs, etc automatically get updated and rebuilt").

    python3 tools/releasedocs.py                     # DAEMONS: what came since the last ROM release, and every stale surface
    python3 tools/releasedocs.py --companion         # the companion: since the WHAT'S NEW build before the newest
    python3 tools/releasedocs.py --since v11.340.1   # DAEMONS from a named release instead
    python3 tools/releasedocs.py --companion --since-build 960   # the companion from a named TestFlight build
    python3 tools/releasedocs.py --online            # also compare each of the five wikis with what GitHub shows
    python3 tools/releasedocs.py --kind              # print major, minor or patch and nothing else (for scripts)
    python3 tools/releasedocs.py --audio-gate        # the push routine's book-audio check, by release kind (below)
    python3 tools/releasedocs.py --json              # everything above as JSON

It only reports. What it finds is fixed by the release session in the same push (README and wiki words, a manual
reprinted with `tools/manual.py --book X --write`, a wiki published with its `wiki/publish.sh`), or filed as a TODO row.

WHAT CAME SINCE. DAEMONS: the engine's and this repository's commits since the newest ROM release (`ROM RELEASE/
.../.release.json` keeps both commits), grouped by the ticket each names, titled from docs/TODO.md. The companion: its
commits since the WHAT'S NEW build before the newest (server/data/whatsnew.json, C-318: at a TestFlight release
`whatsnew.py --write --build N` has already written the new build's entry, so "the previous what's new" is the one
before it), grouped the same way and joined to each WHAT'S NEW section -- its lines, and its SET UP (C-339) when it has
one. Each item gets its NAMES: the ticket, the capitalised names in its title (THE EASEL, SLEEP SOUNDS) and its SET UP's
title.

WHICH SURFACE SHOULD SAY IT. Each item is routed by the files its commits touched (ROUTES) and by its SET UP's `wiki`
and `book`, and every surface it is routed to is searched for its names. A surface that names none of them is a
CANDIDATE: a judgement for the release session, not a failure -- many tickets need no public word. The five READMEs,
the five wikis, the manuals' sources and each repository's docs/ are searched for every item, so the report also says
where each one is already told.

WHAT IS STALE, mechanically -- these are the gaps that count:
  * a README or wiki Home whose "newest release" line names an older release than ROM RELEASE/ holds
  * a manual PDF whose sources (docs/manual*/) were committed after it was printed, or changed and not committed
  * the design bible's PDF missing for the version vision.md carries
  * (--online) a wiki whose published pages differ from its wiki/ folder at HEAD
  * a SET UP entry whose wiki page or HOW TO PLAY book does not name what it sets up
  * a book recording out of date -- regenerated only on a MAJOR or MINOR release, never on a build or a fix (below)

MAJOR, MINOR, PATCH. A DAEMONS release is v<bible>.<n> (romrelease.py), and the bible's version is <major>.<minor>:
  major  the bible's first number moved since the last release (v11 -> v12)
  minor  the bible's second number moved (v11.348.x -> v11.349.1): the first release of a new group, the one that seals
  patch  another release in the same group (v11.349.1 -> v11.349.2)
The companion's TestFlight builds (930, 931, ...) are patches; its marketing version (app.json expo.version, 1.0.0)
is <major>.<minor>.<patch> and only a move in its first two numbers is a major or minor release.

BOOK AUDIO (tools/bookaudio.py). `--audio-gate` fails on a book with no voice, always (T-543), and on a recording out
of date only on a major or minor DAEMONS release; on a patch it names what is behind and defers it. On a minor or
major release it prints the commands that regenerate exactly the books that are behind. Recordings are long and
run on the Tiiny or roverbyteseer: report the plan to the user before running any.
"""
import ast, glob, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = os.path.expanduser("~/Projects")
PY = os.path.expanduser("~/.pyenv/shims/python3")      # bookaudio needs numpy and soundfile (memory: tools-need-pyenv)
REL = os.path.join(ROOT, "ROM RELEASE")
ARGS = sys.argv[1:]


def repo(link, name):
    """A sibling repository: through this checkout's symlink when it has one (a worktree may not), else ~/Projects."""
    p = os.path.join(ROOT, link)
    return os.path.realpath(p) if os.path.isdir(p) else os.path.join(HOME, name)


REPOS = {"DAEMONS": ROOT, "engine": repo("engineGba", "pokefirered-daemons"),
         "companion": repo("companion", "daemons-companion"), "playground": repo("playground", "daemons-playground"),
         "engineAi": repo("engineAi", "gpt-play-pokemon-firered-daemons")}

#  (repository, path prefix a commit touched) -> the surfaces that should then name it
ROUTES = [
    ("companion", "firmware/", ["companion:wiki/Boards.md", "companion:docs/HARDWARE.md"]),
    ("companion", "hub/", ["companion:docs/HUB.md", "companion:wiki/The-hub-and-its-AI.md"]),
    ("companion", "app/", ["DAEMONS:docs/manual-companion/manual.md"]),
    ("engine", "", ["DAEMONS:docs/manual/manual.md"]),
    ("DAEMONS", "ai/litellm/", ["companion:wiki/The-hub-and-its-AI.md"]),
    ("engineAi", "", ["engineAi:wiki/Home.md"]),
    ("playground", "", ["playground:README.md"]),
]
#  a HOW TO PLAY book as a SET UP entry names it -> manual.py's book
SETUP_BOOK = {"player": "main", "micro": "micro", "quick": "quick", "companion": "companion", "watch": "watch",
              "tiiny": "tiiny", "social": "social"}
NOT_NAMES = {"DAEMONS", "DAEMON", "DRAFT", "THE", "AI", "OK", "A", "AND", "OF", "IN", "TO", "ON", "BUILT", "DEBUG",
             "CONTENT", "CONTEXT", "DRAFTED", "DONE", "FIXED", "TODO", "WIP", "ROM", "RELEASE", "GBA", "INDEX", "HP", "LED", "USB", "PDF", "API", "QR", "SD", "TV", "NPC"}
TICKET = re.compile(r"\b([TC]-\d+)\b")


def git(where, *a, check=False):
    r = subprocess.run(["git", "-C", where, *a], capture_output=True, text=True)
    if check and r.returncode:
        raise SystemExit("releasedocs: git %s failed in %s\n%s" % (" ".join(a[:2]), where, r.stderr[-600:]))
    return r.stdout


def vtuple(v):
    return tuple(int(x) for x in re.findall(r"\d+", v))


def opt(flag):
    return ARGS[ARGS.index(flag) + 1] if flag in ARGS and ARGS.index(flag) + 1 < len(ARGS) else None


# ---------------------------------------------------------------- versions and releases

def bible_version():
    m = re.search(r"\bv(\d+\.\d+)\b", open(os.path.join(ROOT, "docs/vision.md"), encoding="utf-8").read(3000))
    return m.group(1) if m else "0.0"


def releases():
    """Every DAEMONS release with a record, oldest first: (version, record)."""
    out = []
    for meta in glob.glob(os.path.join(REL, "v*.x", "v*", ".release.json")) + glob.glob(os.path.join(REL, "v*.x", ".release.json")):
        rec = json.load(open(meta))
        out.append((rec["version"], rec))
    return sorted(out, key=lambda r: vtuple(r[0]))


def kind_between(old, new):
    """major, minor or patch, from two <major>.<minor>[...] versions."""
    o, n = vtuple(old), vtuple(new)
    if not o:
        return "major"
    return "major" if n[0] != o[0] else "minor" if n[1] != o[1] else "patch"


def daemons_kind():
    rs = releases()
    return kind_between(rs[-1][1]["bible"], bible_version()) if rs else "major"


def companion_marketing(commit=None):
    c = REPOS["companion"]
    text = git(c, "show", "%s:app/app.json" % commit) if commit else open(os.path.join(c, "app/app.json")).read()
    try:
        return json.loads(text)["expo"]["version"]
    except (ValueError, KeyError):
        return "0.0.0"


# ---------------------------------------------------------------- what came since

def titles(todo_path):
    t = {}
    if os.path.exists(todo_path):
        for m in re.finditer(r"^\|\s*(?:~~)?\*\*([TC]-\d+)\*\*(?:~~)?\s*\|?\s*(?:~~)?\*{2,3}(.+?)\*{2,3}", open(todo_path, encoding="utf-8").read(), re.M):
            t.setdefault(m.group(1), re.sub(r"\s+", " ", m.group(2)).strip())
    return t


def commits(where, since, label):
    """(repo label, sha, subject, files) for each commit since `since`, newest first."""
    out, cur = [], None
    for line in git(where, "log", "--name-only", "--format=\x1e%h\x1f%s", "%s..HEAD" % since).split("\n"):   # not splitlines: it splits on \x1e too
        if line.startswith("\x1e"):
            sha, subject = line[1:].split("\x1f", 1)
            cur = (label, sha, subject, [])
            out.append(cur)
        elif line.strip() and cur:
            cur[3].append(line.strip())
    return out


def names_in(text):
    """The capitalised names in a title: runs of two or more capital words, or one long one (THE EASEL, SLEEP SOUNDS)."""
    found = []
    for m in re.finditer(r"\b[A-Z][A-Z0-9'’\-]+(?:\s+[A-Z][A-Z0-9'’\-]+)*\b", text or ""):
        words = [w for w in m.group(0).split() if w not in NOT_NAMES]
        phrase = m.group(0).strip(" '’-")
        if not words:
            continue
        if len(phrase.split()) >= 2 or len(phrase) >= 4:
            found.append(phrase)
    return list(dict.fromkeys(found))


def group(cs, title_of, sections=None):
    """Commits grouped by the first ticket each names; a commit naming none is listed under '(no ticket)'."""
    items = {}
    for label, sha, subject, files in cs:
        m = TICKET.search(subject)
        key = m.group(1) if m else "(no ticket)"
        it = items.setdefault(key, {"ticket": key, "title": title_of.get(key, ""), "commits": [], "files": set(),
                                    "repos": set(), "lines": [], "setup": None, "subjects": []})
        it["commits"].append("%s %s %s" % (label, sha, subject[:110]))
        it["subjects"].append(subject)
        it["files"].update((label, f) for f in files)
        it["repos"].add(label)
    for s in sections or []:
        it = items.setdefault(s.get("ticket") or "(no ticket)", {"ticket": s.get("ticket"), "title": s.get("title", ""),
                                                                 "commits": [], "files": set(), "repos": {"companion"},
                                                                 "lines": [], "setup": None, "subjects": []})
        it["title"] = it["title"] or s.get("title", "")
        it["lines"] += s.get("lines", [])
        it["setup"] = it["setup"] or s.get("setup")
    for it in items.values():
        names = names_in(it["title"]) + (names_in(it["setup"]["title"]) if it["setup"] else [])
        if not names:      # a sentence-case title: the names its commits and WHAT'S NEW lines use most
            seen = {}
            for n in (x for line in it["subjects"] + it["lines"] for x in names_in(line)):
                seen[n] = seen.get(n, 0) + 1
            names = [n for n, k in sorted(seen.items(), key=lambda kv: -kv[1])[:3]]
        it["apis"] = sorted(set(a.rstrip("/.,;)") for t in it["subjects"] + it["lines"]
                                for a in re.findall(r"/api/[a-z][a-z0-9_/-]*", t)))
        it["names"] = list(dict.fromkeys(([it["ticket"]] if TICKET.match(it["ticket"] or "") else []) + names))
    return items


def daemons_since():
    rs = releases()
    if not rs:
        raise SystemExit("releasedocs: no ROM release on record")
    want = opt("--since")
    rec = next((r for v, r in rs if "v" + v == want or v == want), None) if want else rs[-1][1]
    if want and not rec:
        raise SystemExit("releasedocs: no release called %s" % want)
    cs = commits(REPOS["engine"], rec["engine"], "engine") + commits(ROOT, rec["docs"], "DAEMONS")
    tt = titles(os.path.join(ROOT, "docs/TODO.md"))
    tt.update({k: v for k, v in titles(os.path.join(REPOS["companion"], "TODO.md")).items() if k not in tt})
    return "v" + rec["version"], group(cs, tt)


def companion_since():
    c = REPOS["companion"]
    wn = json.load(open(os.path.join(c, "server/data/whatsnew.json"), encoding="utf-8"))
    builds = sorted(wn["builds"], key=lambda b: b["build"], reverse=True)
    want = opt("--since-build")
    if want:
        base = next((b for b in builds if str(b["build"]) == want), None)
        if not base:
            raise SystemExit("releasedocs: WHAT'S NEW has no build %s" % want)
    else:
        base = builds[1] if len(builds) > 1 else builds[0]
    newer = [b for b in builds if b["build"] > base["build"]]
    sections = [s for b in newer for s in b.get("sections", [])]
    cs = commits(c, base["commit"], "companion")
    tt = titles(os.path.join(c, "TODO.md"))
    tt.update({k: v for k, v in titles(os.path.join(ROOT, "docs/TODO.md")).items() if k not in tt})
    return "build %s" % base["build"], group(cs, tt, sections), base


# ---------------------------------------------------------------- the surfaces

def manual_books():
    tree = ast.parse(open(os.path.join(ROOT, "tools/manual.py"), encoding="utf-8").read())
    return next(ast.literal_eval(n.value) for n in tree.body
                if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) == "BOOKS")


def surfaces():
    """Every public surface: label -> absolute path."""
    out = {}
    for name, where in REPOS.items():
        for p in ["README.md"] + sorted(os.path.relpath(f, where) for f in glob.glob(os.path.join(where, "wiki", "*.md"))):
            if os.path.exists(os.path.join(where, p)):
                out["%s:%s" % (name, p)] = os.path.join(where, p)
    for b in manual_books().values():
        out["DAEMONS:%s/manual.md" % b["src"]] = os.path.join(ROOT, b["src"], "manual.md")
    for f in sorted(glob.glob(os.path.join(REPOS["companion"], "docs", "*.md"))):
        out["companion:docs/%s" % os.path.basename(f)] = f
    for f in ("docs/README.md", "docs/guide.md"):
        if os.path.exists(os.path.join(ROOT, f)):
            out["DAEMONS:" + f] = os.path.join(ROOT, f)
    return out


def mentions(text, names):
    """The names a text holds: a ticket as a word, a name in any case (SLEEP SOUNDS is told as "sleep sounds" too)."""
    low = text.lower()
    return [n for n in names if (n.lower() in low if not TICKET.match(n) else re.search(r"\b%s\b" % re.escape(n), text))]


def routed(it):
    want = set()
    for repo_label, prefix, targets in ROUTES:
        if any(l == repo_label and f.startswith(prefix) for l, f in it["files"]):
            want.update(targets)
    s = it.get("setup") or {}
    if s.get("wiki"):
        want.add("companion:wiki/%s.md" % s["wiki"].split("#")[0])
    if s.get("book") in SETUP_BOOK:
        want.add("DAEMONS:%s/manual.md" % manual_books()[SETUP_BOOK[s["book"]]]["src"])
    return want


def candidates(items, surf):
    texts = {k: open(p, encoding="utf-8", errors="replace").read() for k, p in surf.items()}
    rows = []
    for key, it in sorted(items.items()):
        named = [n for n in it["names"] if not TICKET.match(n)]
        told = sorted(k for k, t in texts.items() if mentions(t, it["names"]))
        want = sorted(routed(it))
        missing = [] if key == "(no ticket)" else [w for w in want if w in texts and not mentions(texts[w], named or it["names"])]
        api_doc = texts.get("companion:wiki/Server-API.md", "")
        apis = [a for a in it["apis"] if a not in api_doc]
        rows.append({"apis_untold": apis, "ticket": key, "title": it["title"], "names": it["names"], "commits": len(it["commits"]),
                     "told_in": told, "should_tell": want, "candidates": missing if named else [],
                     "unnamed": not named, "setup": bool(it.get("setup"))})
    return rows


# ---------------------------------------------------------------- what is stale

def newest_release():
    rs = releases()
    return "v" + rs[-1][0] if rs else None


def release_lines():
    """Each README or wiki Home that names 'the newest release' -- and whether it names the newest there is."""
    newest, out = newest_release(), []
    pat = re.compile(r"(?:newest release is|newest is|latest:)\s*\*\*(v\d+\.\d+\.\d+)\*\*", re.I)
    for label, path in surfaces().items():
        if not (label.endswith("README.md") or label.endswith("wiki/Home.md")):
            continue
        for m in pat.finditer(re.sub(r"\s+", " ", open(path, encoding="utf-8").read())):
            if newest and vtuple(m.group(1)) < vtuple(newest):
                out.append({"surface": label, "says": m.group(1), "newest": newest})
    return out


def last_commit_time(where, path):
    t = git(where, "log", "-1", "--format=%ct", "--", path).strip()
    return int(t) if t else 0


def manuals():
    out = []
    for name, b in manual_books().items():
        src, pdf = b["src"], b["out"]
        dirty = git(ROOT, "status", "--porcelain", "--", src).strip()
        s, p = last_commit_time(ROOT, src), last_commit_time(ROOT, pdf)
        if not os.path.exists(os.path.join(ROOT, pdf)):
            state = "missing"
        elif dirty:
            state = "sources changed, not committed"
        elif s > p:
            state = "sources committed after it was printed"
        else:
            continue
        out.append({"book": name, "pdf": pdf, "state": state,
                    "fix": "python3 tools/manual.py%s --write" % ("" if name == "main" else " --book " + name)})
    return out


def bible_pdf():
    v = bible_version()
    return [] if os.path.exists(os.path.join(ROOT, "docs/CONTEXT-CONTENT-design-bible-v%s.pdf" % v)) else \
        [{"pdf": "docs/CONTEXT-CONTENT-design-bible-v%s.pdf" % v, "fix": "./docs/build-pdf.sh %s" % v}]


def setup_pages():
    """Each SET UP entry's wiki page and HOW TO PLAY book should name what it sets up."""
    c, out = REPOS["companion"], []
    path = os.path.join(c, "server/data/whatsnew_setup.json")
    if not os.path.exists(path):
        return out
    books = manual_books()
    for ticket, s in json.load(open(path, encoding="utf-8")).items():
        if not isinstance(s, dict) or "steps" not in s:
            continue
        names = names_in(s.get("title", "")) or [s.get("title", "")]
        where = []
        if s.get("wiki"):
            where.append(("companion:wiki/%s.md" % s["wiki"].split("#")[0], os.path.join(c, "wiki", s["wiki"].split("#")[0] + ".md")))
        if s.get("book") in SETUP_BOOK:
            src = books[SETUP_BOOK[s["book"]]]["src"]
            where.append(("DAEMONS:%s/manual.md" % src, os.path.join(ROOT, src, "manual.md")))
        for label, p in where:
            text = open(p, encoding="utf-8").read() if os.path.exists(p) else ""
            if not any(n.lower() in text.lower() for n in names):
                out.append({"ticket": ticket, "title": s.get("title"), "surface": label})
    return out


def wikis_online():
    """Each wiki/ at HEAD against what GitHub's wiki shows (a shallow clone; nothing is written)."""
    import tempfile
    out = []
    for name, where in REPOS.items():
        pub = os.path.join(where, "wiki", "publish.sh")
        if not os.path.exists(pub):
            continue
        m = re.search(r"https://github\.com/\S+?\.wiki\.git", open(pub).read())
        if not m:
            continue
        with tempfile.TemporaryDirectory(prefix="daemons-wiki-") as tmp:
            r = subprocess.run(["git", "clone", "--quiet", "--depth", "1", m.group(0), tmp + "/w"], capture_output=True, text=True)
            if r.returncode:
                out.append({"wiki": name, "state": "could not clone %s" % m.group(0)})
                continue
            differ = []
            for f in git(where, "ls-tree", "--name-only", "HEAD", "wiki/").split():
                if not f.endswith(".md"):
                    continue
                live = os.path.join(tmp, "w", os.path.basename(f))
                head = git(where, "show", "HEAD:" + f)
                if not os.path.exists(live) or open(live, encoding="utf-8", errors="replace").read() != head:
                    differ.append(os.path.basename(f))
            if differ:
                out.append({"wiki": name, "state": "%d page(s) not published: %s" % (len(differ), ", ".join(differ[:8])),
                            "fix": "commit the pages, then %s/wiki/publish.sh (from HEAD if others have wiki/ edits)" % name})
    return out


def book_audio():
    """bookaudio.py --check, read: each book current, out of date or missing, and any book with no voice."""
    env = dict(os.environ, BOOK_DATA=os.path.join(REPOS["companion"], "server/data"))
    r = subprocess.run([PY if os.path.exists(PY) else sys.executable, os.path.join(ROOT, "tools/bookaudio.py"),
                        "--check", os.path.join(ROOT, "docs/books/audio")], cwd=ROOT, capture_output=True, text=True, env=env)
    behind, voiceless = [], []
    for line in r.stdout.splitlines():
        m = re.match(r"\s+(\w+): (\w+), sources \w+; (\S+) is (out of date|missing)", line)
        if m:
            behind.append({"book": m.group(1), "voice": m.group(2), "file": m.group(3), "state": m.group(4)})
        m = re.match(r"\s+(\w+): NO VOICE", line)
        if m:
            voiceless.append(m.group(1))
    if r.returncode not in (0, 1):
        return None, None, (r.stderr or r.stdout)[-600:]
    return behind, voiceless, None


# ---------------------------------------------------------------- report

def audio_plan(kind, behind, voiceless):
    lines = []
    for b in voiceless:
        lines.append("  !! %s has no voice -- choose one with the user from samples (T-543); this fails every release" % b)
    if not behind:
        lines.append("  every recording is current")
    elif kind in ("major", "minor"):
        lines.append("  a %s release: regenerate the %d recording(s) behind -- REPORT THIS PLAN TO THE USER FIRST "
                     "(long; run on the Tiiny or roverbyteseer):" % (kind, len(behind)))
        for b in behind:
            lines.append("    python3 tools/bookaudio.py %s docs/books/audio      # %s, %s" % (b["book"], b["file"], b["state"]))
    else:
        lines.append("  a patch release: %d recording(s) behind, deferred to the next minor release: %s"
                     % (len(behind), ", ".join(b["book"] for b in behind)))
    return lines


def main():
    side = "companion" if "--companion" in ARGS else "DAEMONS"
    if side == "companion":
        c_items = companion_since()
        base = c_items[2]
        old, new = companion_marketing(base["commit"]), companion_marketing()
        kind = kind_between(old, new)
    else:
        kind = daemons_kind()
    if "--kind" in ARGS:
        print(kind)
        return 0

    behind, voiceless, err = book_audio()
    if "--audio-gate" in ARGS:
        if err:
            print("  bookaudio --check failed:\n" + err)
            return 1
        print("  release kind: %s (bible v%s, last release %s)" % (kind, bible_version(), newest_release()))
        print("\n".join(audio_plan(kind, behind, voiceless)))
        return 1 if voiceless or (behind and kind in ("major", "minor")) else 0

    since, items = (c_items[0], c_items[1]) if side == "companion" else daemons_since()
    surf = surfaces()
    rows = candidates(items, surf)
    stale = {"release_lines": release_lines(), "manuals": manuals(), "bible_pdf": bible_pdf(),
             "setup_pages": setup_pages(), "wikis": wikis_online() if "--online" in ARGS else None,
             "audio_behind": behind, "audio_voiceless": voiceless}
    if "--json" in ARGS:
        print(json.dumps({"side": side, "since": since, "kind": kind, "items": rows, "stale": stale}, indent=1, default=list))
        return 0

    print("%s since %s -- a %s release; %d item(s) across %d surface(s)" % (side, since, kind, len(rows), len(surf)))
    print("\nWHAT CAME, and where it is told")
    for r in rows:
        print("  %-11s %s  (%d commit%s%s)" % (r["ticket"], (r["title"] or "")[:78], r["commits"], "" if r["commits"] == 1 else "s",
                                             ", SET UP" if r["setup"] else ""))
        if r["told_in"]:
            print("              told in: %s" % ", ".join(r["told_in"][:6]) + (" +%d" % (len(r["told_in"]) - 6) if len(r["told_in"]) > 6 else ""))
        if r["candidates"]:
            print("              CANDIDATE -- should it be told in: %s  (names: %s)"
                  % (", ".join(r["candidates"]), ", ".join(n for n in r["names"] if not TICKET.match(n))))
        if r["apis_untold"]:
            print("              API not in companion:wiki/Server-API.md: %s" % ", ".join(r["apis_untold"]))
        if r["unnamed"] and r["should_tell"]:
            print("              no name to search for; by its files, check: %s" % ", ".join(r["should_tell"]))
    print("\nSTALE")
    n = 0
    for s in stale["release_lines"]:
        print("  release line  %s says %s; the newest is %s" % (s["surface"], s["says"], s["newest"])); n += 1
    for s in stale["manuals"]:
        print("  manual        %s: %s -> %s" % (s["pdf"], s["state"], s["fix"])); n += 1
    for s in stale["bible_pdf"]:
        print("  bible PDF     %s missing -> %s" % (s["pdf"], s["fix"])); n += 1
    for s in stale["setup_pages"]:
        print("  SET UP        %s %s is not named in %s" % (s["ticket"], s["title"], s["surface"])); n += 1
    for s in stale["wikis"] or []:
        print("  wiki          %s: %s%s" % (s["wiki"], s["state"], " -> " + s["fix"] if s.get("fix") else "")); n += 1
    if stale["wikis"] is None:
        print("  (wikis not compared with GitHub: pass --online)")
    print("\nBOOK AUDIO")
    print("\n".join(audio_plan(kind, behind or [], voiceless or [])) if not err else "  bookaudio --check failed: " + err)
    n += len(voiceless or []) + (len(behind or []) if kind in ("major", "minor") else 0)
    print("\n%d stale; %d candidate(s) to judge" % (n, sum(bool(r["candidates"]) for r in rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
