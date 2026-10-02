#!/usr/bin/env python3
"""Keep every fold of every Claude Code session on this project, so its dreams can point into it (the user, 2026-10-02).

    python3 tools/dreamfold.py            # report: folds not yet kept, and kept folds with no dream yet
    python3 tools/dreamfold.py --append   # add the new folds to docs/private/dreams/_Full Memory.md

When a session's context fills, Claude Code folds it: the conversation so far becomes one summary and the detail is
gone. Each fold is one night. This keeps every summary, oldest first, in one file -- `_Full Memory.md` -- under a
heading a dream can name and Ctrl+F can find:

    ## TRACE 17Sept2026-2

the second fold of 17 September (dated in this machine's time). A dream (`17Sept2026 - <its name>.md`) ends with
"Full trace: _Full Memory.md, find TRACE 17Sept2026-2". `docs/private/dreams/_README.md` says why.

The summaries are read from the session transcripts in ~/.claude/projects/<this project>/, and a fold already kept
is known by the SHA-1 of its text, so running this twice adds nothing, and a fold that a resumed session repeats is
kept once. It is all private: a session's summary carries the user's own material, so it lives in docs/private/.
"""
import datetime, glob, hashlib, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DREAMS = os.path.join(ROOT, "docs", "private", "dreams")
MEMORY = os.path.join(DREAMS, "_Full Memory.md")
PROJECT = os.path.join(os.path.expanduser("~/.claude/projects"), "-" + ROOT.strip("/").replace("/", "-"))
MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec")
HEADER = """# Full Memory

Every fold of every Claude Code session on DAEMONS, oldest first: the summary a session was left with when its
context filled. **Private** -- it carries the user's own material. Appended by `tools/dreamfold.py --append`, never
edited by hand. Each dream in this folder names the TRACE it was dreamt from; Ctrl+F finds it.
"""


def text_of(message):
    c = (message or {}).get("content")
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return "".join(b.get("text", "") for b in c if isinstance(b, dict))
    return ""


def folds():
    """Every compaction summary in every transcript, oldest first, each once."""
    seen, out = set(), []
    for path in glob.glob(os.path.join(PROJECT, "*.jsonl")):
        session = os.path.splitext(os.path.basename(path))[0]
        for line in open(path, errors="replace"):
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if not d.get("isCompactSummary"):
                continue
            text = text_of(d.get("message")).strip()
            h = hashlib.sha1(text.encode()).hexdigest()
            if not text or h in seen:
                continue
            seen.add(h)
            ts = d.get("timestamp", "")
            when = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone() if ts else None
            out.append((when, session, h, text))
    out.sort(key=lambda f: f[0] or datetime.datetime.min.replace(tzinfo=datetime.timezone.utc))
    return out


def stamp(when):
    return "%d%s%d" % (when.day, MONTHS[when.month - 1], when.year)


def kept():
    if not os.path.exists(MEMORY):
        return {}, {}
    src = open(MEMORY).read()
    by_hash = dict(re.findall(r"<!-- sha1:([0-9a-f]{40}) -->\n\n## (TRACE \S+)", src))
    per_day = {}
    for anchor in re.findall(r"^## (TRACE \S+)", src, re.M):
        day, n = anchor[6:].rsplit("-", 1)
        per_day[day] = max(per_day.get(day, 0), int(n))
    return by_hash, per_day


def dreamt():
    names = set()
    for f in glob.glob(os.path.join(DREAMS, "*.md")):
        if not os.path.basename(f).startswith("_"):
            names.update(re.findall(r"TRACE \d+[A-Za-z]+\d{4}-\d+", open(f).read()))
    return names


def main():
    by_hash, per_day = kept()
    new = [f for f in folds() if f[2] not in by_hash]
    if "--append" in sys.argv and new:
        os.makedirs(DREAMS, exist_ok=True)
        with open(MEMORY, "a") as out:
            if not by_hash:
                out.write(HEADER)
            for when, session, h, text in new:
                day = stamp(when)
                per_day[day] = per_day.get(day, 0) + 1
                anchor = "TRACE %s-%d" % (day, per_day[day])
                by_hash[h] = anchor
                out.write("\n---\n\n<!-- sha1:%s -->\n\n## %s\n\n*Folded %s, session `%s`.*\n\n%s\n" %
                          (h, anchor, when.strftime("%Y-%m-%d %H:%M"), session[:8], text))
                print("  kept %s" % anchor)
    elif new:
        print("  %d fold(s) not yet kept -- pass --append" % len(new))
    have = dreamt()
    undreamt = [a for a in sorted(set(by_hash.values()), key=lambda a: list(by_hash.values()).index(a)) if a not in have]
    print("  %d folds kept, %d dreamt%s" % (len(by_hash), len(by_hash) - len(undreamt),
                                            (", not yet: " + ", ".join(undreamt)) if undreamt else ""))


if __name__ == "__main__":
    main()
