#!/usr/bin/env python3
"""tickets.py -- the TODO files as Redmine tickets, proof of concept (T-581).

The plan (the user, 2026-11-17, by multiple choice): Redmine on roverbyteseer holds the tickets of docs/TODO.md (T-)
and the companion's TODO.md (C-); the ids stay T-/C- for good, in a Ticket field; both TODO files become a mirror
generated from Redmine, so a fresh clone or a cloud session can still read them.

This first slice touches nothing on the network. It parses both files into the payload Redmine would be sent --
subject, description, status, custom fields -- and proves the cut-over loses nothing: the files are rebuilt from that
payload alone (plus the frame, the prose around the tables) and compared byte for byte with the originals.

    python3 tools/tickets.py migrate --dry-run              # counts, irregular rows, and the round trip (also: bare)
    python3 tools/tickets.py migrate --dry-run --json OUT   # also write the payload
    python3 tools/tickets.py mirror --from OUT [--write]    # rebuild the TODO files from a payload

Read-only by default, like every tool here; `mirror --write` is the only write, and it writes only the two TODO files.
Stdlib only.
"""
import argparse
import difflib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = {
    "daemons": ROOT / "docs/TODO.md",
    "companion": (ROOT / "companion").resolve() / "TODO.md",
}
PREFIX = {"daemons": "T", "companion": "C"}

ROW = re.compile(r"^\| (?P<id>(~~)?\*\*(?P<p>[TC])-(?P<n>\d+)(?P<sfx>[a-z]?)\*\*(~~)?) \| ")
SEP = re.compile(r"^\|(\s*-+\s*\|)+\s*$")
SHA = re.compile(r"(?<![0-9A-Za-z/#=-])([0-9a-f]{7,12})(?![0-9A-Za-z])")
REPO_WORD = re.compile(r"\b(engineGba|engine|companion|playground|engineAi)\b[^|()]{0,12}$")
PLACEHOLDER = "@@tickets {}@@"
TICKET_TABLES = ("what", "ticket")  # the first column a table of tickets is headed by

# a section heading -> the ticket's status in Redmine (struck through is Closed wherever it stands)
STATUS = [("Ready", "Ready"), ("Blocked", "Blocked"), ("Wants a decision", "Needs decision"),
          ("Deferred", "Deferred"), ("Closed", "Closed")]


def ticket_key(p, n, sfx):
    return f"{p}-{int(n)}{sfx}"


def canonical_id_cell(key, struck):
    return f"~~**{key}**~~" if struck else f"**{key}**"


def subject_of(cell, key):
    m = re.search(r"\*\*(.+?)\*\*", cell.replace("~~", ""))
    text = m.group(1) if m else cell
    text = re.sub(r"[*_`]", "", text).strip()
    text = re.sub(r"\s+", " ", text)
    s = f"{key} {text}"
    return s if len(s) <= 250 else s[:249] + "…"


def commits_of(cells):
    out = []
    for cell in cells:
        for m in SHA.finditer(cell):
            sha = m.group(1)
            if not re.search(r"\d", sha) or not re.search(r"[a-f]", sha):
                continue  # a word made of a-f, or a number
            rw = REPO_WORD.search(cell[: m.start()])
            out.append((rw.group(1) if rw else "") + "@" + sha)
    return sorted(set(out), key=out.index)


def parse(project, text):
    """-> (frame lines with placeholders, tickets, irregular notes)"""
    lines = text.split("\n")
    frame, tickets, notes = [], [], []
    section, columns, run, prev_was_row = "", [], 0, False
    order = 0
    for i, line in enumerate(lines):
        m = ROW.match(line)
        if m and not (len(columns) > 1 and columns[1].lower() in TICKET_TABLES):
            m = None  # a table that names tickets without holding them (TODO.md's own "it said / it was")
        if not m:
            if line.startswith("## "):
                section = line[3:].strip()
            if SEP.match(line) and i > 0:
                columns = [c.strip() for c in lines[i - 1].strip().strip("|").split("|")]
            frame.append(line)
            prev_was_row = False
            continue
        if not prev_was_row:
            run += 1
            frame.append(PLACEHOLDER.format(run))
        prev_was_row = True
        order += 1
        struck = m.group("id").startswith("~~")
        key = ticket_key(m.group("p"), m.group("n"), m.group("sfx"))
        if m.group("p") != PREFIX[project]:
            notes.append(f"{project}:{i+1} {key} carries the other project's prefix")
        rest = line[len("| ") + len(m.group("id")) + len(" | "):]
        if rest.endswith(" |"):
            cells, tail = rest[:-2].split(" | "), " |"
        else:
            cells, tail = [rest], ""
            notes.append(f"{project}:{i+1} {key} row does not end with ' |'")
        names = columns[1:] if columns else []
        if len(cells) != len(names):
            notes.append(f"{project}:{i+1} {key} has {len(cells)} cells, its table {len(names)} columns")
        status = next((s for h, s in STATUS if section.startswith(h)), "Ready")
        if struck:
            status = "Closed"
        elif re.search(r"\bWIP\b", cells[0]):
            status = "In progress"
        fields = {"Ticket": key, "Run": run, "Order": order}
        if m.group("id") != canonical_id_cell(key, struck):
            fields["Shown as"] = m.group("id")
        if tail != " |":
            fields["Row tail"] = tail
        for name, cell in zip(names[1:], cells[1:]):
            fields[col(name)] = cell
        if len(cells) > len(names):
            fields["Extra cells"] = cells[max(len(names), 1):]
        commits = commits_of(cells)
        if commits:
            fields["Commits"] = commits
        tickets.append({
            "project": project, "line": i + 1, "section": section, "columns": names,
            "struck": struck, "status": status,
            "subject": subject_of(cells[0], key), "description": cells[0], "fields": fields,
        })
    return frame, tickets, notes


def col(name):
    return name.capitalize() or "-"


def render_row(t):
    f = t["fields"]
    id_cell = f.get("Shown as") or canonical_id_cell(f["Ticket"], t["struck"])
    cells = [t["description"]] + [f[col(n)] for n in t["columns"][1:] if col(n) in f] + f.get("Extra cells", [])
    return "| " + id_cell + " | " + " | ".join(cells) + f.get("Row tail", " |")


def render(frame, tickets):
    by_run = {}
    for t in sorted(tickets, key=lambda t: t["fields"]["Order"]):
        by_run.setdefault(t["fields"]["Run"], []).append(render_row(t))
    out = []
    for line in frame:
        m = re.fullmatch(r"@@tickets (\d+)@@", line)
        out.extend(by_run.get(int(m.group(1)), []) if m else [line])
    return "\n".join(out)


def goals_versions(project, text):
    """Companion 'Today's goals' sections -> the Redmine versions they would become, with the tickets each names."""
    out = []
    for m in re.finditer(r"^## Today's goals -- (\d{4}-\d\d-\d\d), (.+)$", text, re.M):
        end = text.find("\n## ", m.end())
        body = text[m.end(): end if end != -1 else len(text)]
        body = body.split("\n| ", 1)[0]
        ids = sorted({ticket_key(p, n, s) for p, n, s in re.findall(r"\b([TC])-(\d+)([a-z]?)\b", body)},
                     key=lambda k: (k[0], int(re.sub(r"\D", "", k))))
        out.append({"name": f"{m.group(1)} {m.group(2)}", "tickets": ids})
    return out


def load_all():
    data = {}
    for project, path in FILES.items():
        text = path.read_text(encoding="utf-8")
        frame, tickets, notes = parse(project, text)
        data[project] = {"path": str(path), "frame": frame, "tickets": tickets, "notes": notes,
                         "versions": goals_versions(project, text) if project == "companion" else []}
    return data


def report(data):
    ok = True
    for project, d in data.items():
        ts = d["tickets"]
        keys = [t["fields"]["Ticket"] for t in ts]
        dupes = sorted({k for k in keys if keys.count(k) > 1})
        nums = sorted({int(re.sub(r"\D", "", k)) for k in keys if not k[-1].isalpha()})
        gaps = [n for n in range(1, nums[-1] + 1) if n not in set(nums)] if nums else []
        by_status = {}
        for t in ts:
            by_status[t["status"]] = by_status.get(t["status"], 0) + 1
        struck_no_commit = [t["fields"]["Ticket"] for t in ts if t["struck"] and "Commits" not in t["fields"]]
        shown = [t["fields"]["Ticket"] for t in ts if "Shown as" in t["fields"]]
        long_subj = sum(1 for t in ts if t["subject"].endswith("…"))
        print(f"\n{project}: {d['path']}")
        print(f"  {len(ts)} tickets in {max((t['fields']['Run'] for t in ts), default=0)} table run(s); "
              f"ids {PREFIX[project]}-1..{PREFIX[project]}-{nums[-1] if nums else 0}"
              f"{', lettered: ' + ' '.join(k for k in keys if k[-1].isalpha()) if any(k[-1].isalpha() for k in keys) else ''}")
        print("  status: " + ", ".join(f"{s} {n}" for s, n in sorted(by_status.items(), key=lambda x: -x[1])))
        print(f"  gaps: {' '.join(f'{PREFIX[project]}-{n}' for n in gaps) or 'none'}"
              f"   duplicates: {' '.join(dupes) or 'none'}")
        print(f"  struck with no commit named: {len(struck_no_commit)}"
              f"{' (e.g. ' + ' '.join(struck_no_commit[:6]) + ')' if struck_no_commit else ''}")
        print(f"  id written another way (kept as 'Shown as'): {len(shown)}"
              f"{' (e.g. ' + ' '.join(shown[:6]) + ')' if shown else ''}")
        print(f"  subjects cut at 250 characters: {long_subj}")
        if d["versions"]:
            print(f"  goal lists -> versions: {len(d['versions'])}: "
                  + "; ".join(f"{v['name']} ({len(v['tickets'])})" for v in d["versions"]))
        kinds = {}
        for n in d["notes"]:
            kinds.setdefault(re.sub(r"^\S+ \S+ ", "", re.sub(r"\d+", "n", n)), []).append(n.split()[1])
        for k, ids in kinds.items():
            print(f"  note  {len(ids)} x {k}: {' '.join(ids[:6])}{' ...' if len(ids) > 6 else ''}")
        if dupes:
            ok = False
    return ok


def round_trip(data):
    ok = True
    for project, d in data.items():
        original = Path(d["path"]).read_text(encoding="utf-8")
        payload = json.loads(json.dumps(d["tickets"]))  # only what would survive the trip to Redmine
        rebuilt = render(d["frame"], payload)
        if rebuilt == original:
            print(f"  round trip {project}: identical ({len(original.encode())} bytes, "
                  f"{len(payload)} tickets rebuilt from fields)")
        else:
            ok = False
            diff = list(difflib.unified_diff(original.split("\n"), rebuilt.split("\n"), "original", "rebuilt",
                                             lineterm="", n=0))
            print(f"  round trip {project}: DIFFERS, {len(diff)} diff lines; first:")
            for l in diff[:12]:
                print("    " + l[:160])
    return ok


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")
    mg = sub.add_parser("migrate")
    mg.add_argument("--dry-run", action="store_true", required=True,
                    help="the only mode so far: nothing is sent to Redmine")
    mg.add_argument("--json", help="write the payload here")
    mr = sub.add_parser("mirror")
    mr.add_argument("--from", dest="src", required=True, help="a payload written by migrate --json")
    mr.add_argument("--write", action="store_true")
    # check_generators.py runs every tool bare (and with --write in its sandbox): both are the dry run, which writes
    # nothing -- there is no Redmine write to make from here yet.
    argv = sys.argv[1:]
    if argv in ([], ["--write"]):
        argv = ["migrate", "--dry-run"]
    a = ap.parse_args(argv)

    if a.cmd == "migrate":
        data = load_all()
        ok = report(data)
        print()
        ok = round_trip(data) and ok
        if a.json:
            Path(a.json).write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"\npayload written to {a.json}")
        sys.exit(0 if ok else 1)

    data = json.loads(Path(a.src).read_text(encoding="utf-8"))
    for project, d in data.items():
        path = Path(d["path"])
        text = render(d["frame"], d["tickets"])
        same = path.exists() and path.read_text(encoding="utf-8") == text
        if same:
            print(f"{path}: current")
        elif a.write:
            tmp = path.with_suffix(".md.mirror-tmp")
            tmp.write_text(text, encoding="utf-8")
            tmp.replace(path)
            print(f"{path}: written")
        else:
            print(f"{path}: would change (run with --write)")


if __name__ == "__main__":
    main()
