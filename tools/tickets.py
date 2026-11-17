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
    python3 tools/tickets.py sync [--write]                 # files -> Redmine until the cut-over (never deletes)
    python3 tools/tickets.py mirror --from-redmine [--write] # Redmine -> files; refuses if any ticket would be lost
    python3 tools/tickets.py export [--out FILE]            # every ticket with its history, for git (docs/tickets/)
    python3 tools/tickets.py show T-581 [--lane game]       # one ticket
    python3 tools/tickets.py mine --lane game               # a lane's open tickets
    python3 tools/tickets.py assign T-581 --to ops          # give a ticket to a lane
    python3 tools/tickets.py claim T-581 --lane ops --branch main      # after the cut-over only
    python3 tools/tickets.py close T-581 --lane ops --commit DAEMONS@6ff940f9   # after the cut-over only

Redmine's address and key come from ~/.redmine.env (0600, outside every repo); the key is never printed. The Redmine
side is set up by tools/redmine_setup_tickets.rb (statuses, trackers, priorities, fields, projects, membership).

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


# ---- Redmine ---------------------------------------------------------------------------------------------------
# The key is read from ~/.redmine.env (0600, outside every repo) and sent only as a header; it is never printed, and an
# error message has it removed before it is shown.
import urllib.request
import urllib.error

ENV = Path.home() / ".redmine.env"
EMPTY = "(empty)"  # a cell that is there and empty; Redmine cannot tell "" from no value (C-242's rows)
NO_TAIL = "(none)"  # a row with no closing " |"
FIELD_NAMES = ["Ticket", "Run", "Order", "Shown as", "Commits", "Branch", "Where", "From", "Blocked on", "Why not yet",
               "Closed by", "State", "See", "Extra cells", "Row tail"]


class Redmine:
    def __init__(self, lane=None):
        env = dict(l.split("=", 1) for l in ENV.read_text().split("\n") if "=" in l and not l.startswith("#"))
        name = f"REDMINE_KEY_{lane.upper().replace('-', '_')}" if lane else "REDMINE_API_KEY"
        if name not in env:
            raise SystemExit(f"no key for lane {lane!r} in {ENV} (lanes: "
                             + ", ".join(k[12:].lower().replace("_", "-") for k in env if k.startswith("REDMINE_KEY_"))
                             + ")")
        self.url, self._key, self.lane = env["REDMINE_URL"].rstrip("/"), env[name].strip(), lane

    def call(self, method, path, body=None):
        req = urllib.request.Request(self.url + path, method=method,
                                     data=json.dumps(body).encode() if body is not None else None,
                                     headers={"X-Redmine-API-Key": self._key, "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                raw = r.read()
                return json.loads(raw) if raw.strip() else {}
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace").replace(self._key, "<key>")
            raise SystemExit(f"Redmine {method} {path}: {e.code} {msg[:300]}")

    def project(self, ident):
        p = self.call("GET", f"/projects/{ident}.json?include=trackers,issue_custom_fields")["project"]
        p["fields"] = {f["name"]: f["id"] for f in p["issue_custom_fields"]}
        missing = [n for n in FIELD_NAMES if n not in p["fields"]]
        if missing:
            raise SystemExit(f"Redmine project {ident} lacks fields {missing}: run tools/redmine_setup_tickets.rb")
        return p

    def statuses(self):
        return {s["name"]: s["id"] for s in self.call("GET", "/issue_statuses.json")["issue_statuses"]}

    def issues(self, ident):
        out, offset = [], 0
        while True:
            page = self.call("GET", f"/issues.json?project_id={ident}&subproject_id=!*&status_id=*"
                                    f"&sort=id&limit=100&offset={offset}")
            out += page["issues"]
            offset += 100
            if offset >= page["total_count"]:
                return out

    def versions(self, ident):
        return {v["name"]: v["id"] for v in self.call("GET", f"/projects/{ident}/versions.json")["versions"]}


def cf(issue):
    return {c["name"]: c.get("value") for c in issue.get("custom_fields", [])}


def redmine_payload(t, p, statuses, version_id=None):
    """A parsed ticket -> the issue Redmine is sent. The id cell is kept only when it is not the plain form for its
    status (struck through when Closed), so a status change in Redmine moves the strike in the mirror."""
    f = t["fields"]
    key = f["Ticket"]
    closed = t["status"] in ("Closed", "Superseded")
    shown = f.get("Shown as") or canonical_id_cell(key, t["struck"])
    vals = {"Ticket": key, "Run": str(f["Run"]), "Order": str(f["Order"]),
            "Shown as": shown if shown != canonical_id_cell(key, closed) else "",
            "Commits": "\n".join(f.get("Commits", [])),
            "Extra cells": json.dumps(f["Extra cells"], ensure_ascii=False) if "Extra cells" in f else "",
            "Row tail": (f["Row tail"] or NO_TAIL) if "Row tail" in f else ""}
    for n in t["columns"][1:]:
        vals[col(n)] = (f[col(n)] or EMPTY) if col(n) in f else ""
    issue = {"project_id": p["id"], "tracker_id": next(x["id"] for x in p["trackers"] if x["name"] == "Job"),
             "status_id": statuses[t["status"]], "subject": t["subject"], "description": t["description"],
             "custom_fields": [{"id": p["fields"][n], "value": v} for n, v in vals.items() if n in p["fields"]]}
    if version_id:
        issue["fixed_version_id"] = version_id
    return issue


def same_issue(have, want, statuses):
    if have["subject"] != want["subject"] or (have.get("description") or "") != want["description"]:
        return False
    if have["status"]["id"] != want["status_id"]:
        return False
    if want.get("fixed_version_id") and (have.get("fixed_version") or {}).get("id") != want["fixed_version_id"]:
        return False
    hv = {c["id"]: (c.get("value") or "") for c in have.get("custom_fields", [])}
    return all(hv.get(c["id"], "") == c["value"] for c in want["custom_fields"])


def sync(write):
    """Files -> Redmine, until the cut-over: creates what is missing, updates what differs, deletes nothing."""
    rm, data = Redmine(), load_all()
    statuses = rm.statuses()
    for project, d in data.items():
        p = rm.project(project)
        versions = rm.versions(project)
        want_versions = {}
        for v in d["versions"]:  # newest goal list first in the file: a ticket goes to the newest that names it
            if v["name"] not in versions and write:
                versions[v["name"]] = rm.call("POST", f"/projects/{project}/versions.json",
                                              {"version": {"name": v["name"]}})["version"]["id"]
            for k in v["tickets"]:
                want_versions.setdefault(k, v["name"])
        have = {}
        for i in rm.issues(project):
            have.setdefault(cf(i).get("Ticket"), i)
        created = updated = same = 0
        for n, t in enumerate(d["tickets"], 1):
            key = t["fields"]["Ticket"]
            want = redmine_payload(t, p, statuses, versions.get(want_versions.get(key)))
            if key not in have:
                created += 1
                if write:
                    rm.call("POST", "/issues.json", {"issue": want})
            elif not same_issue(have[key], want, statuses):
                updated += 1
                if write:
                    rm.call("PUT", f"/issues/{have[key]['id']}.json", {"issue": want})
            else:
                same += 1
            if write and n % 100 == 0:
                print(f"  {project}: {n}/{len(d['tickets'])}", flush=True)
        extra = sorted(k for k in have if k not in {t["fields"]["Ticket"] for t in d["tickets"]})
        verb = "" if write else "would be "
        print(f"{project}: {created} {verb}created, {updated} {verb}updated, {same} the same"
              f"{'; only in Redmine: ' + ' '.join(extra) if extra else ''}")


def from_redmine(rm, project, d, statuses_by_id):
    """Redmine's issues -> tickets in the shape render() takes, using the file's frame for each table's columns."""
    runs = {}
    for t in d["tickets"]:
        runs.setdefault(t["fields"]["Run"], t["columns"])
    out = []
    for i in rm.issues(project):
        c = cf(i)
        if not c.get("Ticket"):
            continue
        run = int(c["Run"])
        closed = statuses_by_id[i["status"]["id"]] in ("Closed", "Superseded")
        f = {"Ticket": c["Ticket"], "Run": run, "Order": int(c["Order"])}
        if c.get("Shown as"):
            f["Shown as"] = c["Shown as"]
        if c.get("Row tail"):
            f["Row tail"] = "" if c["Row tail"] == NO_TAIL else c["Row tail"]
        if c.get("Extra cells"):
            f["Extra cells"] = json.loads(c["Extra cells"])
        for n in runs.get(run, [])[1:]:
            if c.get(col(n)):
                f[col(n)] = "" if c[col(n)] == EMPTY else c[col(n)]
        out.append({"struck": closed, "columns": runs.get(run, []), "description": i.get("description") or "",
                    "fields": f})
    return out


def mirror_from_redmine(write):
    """Redmine -> both TODO files. Refuses (exit 1) if any ticket in a file is missing from Redmine: an emptied or
    re-created Redmine must never be mirrored over the files and pushed."""
    rm, data = Redmine(), load_all()
    by_id = {v: k for k, v in rm.statuses().items()}
    ok = True
    for project, d in data.items():
        tickets = from_redmine(rm, project, d, by_id)
        have = {t["fields"]["Ticket"] for t in tickets}
        lost = [t["fields"]["Ticket"] for t in d["tickets"] if t["fields"]["Ticket"] not in have]
        path = Path(d["path"])
        if lost:
            ok = False
            print(f"{path}: REFUSED -- {len(lost)} ticket(s) in the file are not in Redmine "
                  f"({' '.join(lost[:8])}{' ...' if len(lost) > 8 else ''}); nothing written")
            continue
        text = render(d["frame"], tickets)
        original = path.read_text(encoding="utf-8")
        if text == original:
            print(f"{path}: current ({len(tickets)} tickets, identical to Redmine)")
            continue
        diff = list(difflib.unified_diff(original.split("\n"), text.split("\n"), "file", "redmine", lineterm="", n=0))
        print(f"{path}: differs from Redmine, {len([l for l in diff if l[:1] in '+-'])} changed line(s)")
        for l in diff[:10]:
            print("    " + l[:160])
        if write:
            tmp = path.with_suffix(".md.mirror-tmp")
            tmp.write_text(text, encoding="utf-8")
            tmp.replace(path)
            print(f"{path}: written")
    return ok


def export(out):
    """Every ticket with its history (journals), relations, attachments' names and watchers, and each project's
    versions -- what a rebuilt Redmine would need beyond the TODO rows. No address, key, email or password: it is
    committed to a public repository. Sorted and stable, so a quiet night changes nothing."""
    rm = Redmine()
    doc = {"what": "T-581: the tickets as Redmine held them; rebuild with tools/tickets.py", "projects": {}}
    for project in FILES:
        issues = []
        for i in rm.issues(project):
            x = rm.call("GET", f"/issues/{i['id']}.json?include=journals,relations,attachments,watchers")["issue"]
            for a in x.get("attachments", []):
                a.pop("content_url", None)
                a.pop("thumbnail_url", None)
            issues.append(x)
        issues.sort(key=lambda x: x["id"])
        versions = sorted(rm.call("GET", f"/projects/{project}/versions.json")["versions"], key=lambda v: v["id"])
        doc["projects"][project] = {"versions": versions, "issues": issues}
    text = json.dumps(doc, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    if rm.url in text:
        raise SystemExit("export: Redmine's address is in the export; refusing to write it")
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    tmp = Path(str(out) + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(out)
    print(f"export: {sum(len(p['issues']) for p in doc['projects'].values())} tickets -> {out}")


# ---- lanes: a session works as its lane (the user, 2026-11-17: tickets assigned to lanes, sessions pick them up) ----
TRUTH = Path.home() / ".local/share/daemons-tickets/truth"
PROJECT_OF = {"T": "daemons", "C": "companion"}


def truth():
    try:
        return TRUTH.read_text().strip() or "files"
    except OSError:
        return "files"


def norm_key(k):
    m = re.fullmatch(r"\s*([TCtc])-0*(\d+)([a-z]?)\s*", k)
    if not m:
        raise SystemExit(f"not a ticket id: {k!r} (T-581, C-397)")
    return f"{m.group(1).upper()}-{int(m.group(2))}{m.group(3)}"


def find(rm, key):
    project = PROJECT_OF[key[0]]
    p = rm.project(project)
    hits = rm.call("GET", f"/issues.json?project_id={project}&status_id=*&cf_{p['fields']['Ticket']}={key}")["issues"]
    hits = [i for i in hits if cf(i).get("Ticket") == key]
    if len(hits) != 1:
        raise SystemExit(f"{key}: {len(hits)} tickets in Redmine carry this id")
    return p, rm.call("GET", f"/issues/{hits[0]['id']}.json?include=journals")["issue"]


def lane_ids(rm):
    out = {}
    for project in PROJECT_OF.values():
        for m in rm.call("GET", f"/projects/{project}/memberships.json?limit=100")["memberships"]:
            u = m.get("user")
            if u and u["name"].startswith("Lane "):
                out[u["name"][5:]] = u["id"]
    return out


def show(rm, key):
    p, i = find(rm, key)
    c = cf(i)
    print(f"{key}  #{i['id']}  {i['status']['name']}"
          f"{'  -> ' + i['assigned_to']['name'] if i.get('assigned_to') else ''}"
          f"{'  [' + i['fixed_version']['name'] + ']' if i.get('fixed_version') else ''}")
    print(i["subject"])
    for n in ("Branch", "Commits", "Where", "From", "Blocked on"):
        if c.get(n):
            print(f"  {n}: {c[n][:200]}")
    print("  " + (i.get("description") or "")[:600])
    for j in [j for j in i.get("journals", []) if j.get("notes")][-3:]:
        print(f"  -- {j['user']['name']}, {j['created_on'][:10]}: {j['notes'][:200]}")
    print(f"  {rm.url}/issues/{i['id']}")


def mine(rm, project=None):
    me = rm.call("GET", "/users/current.json")["user"]
    for proj in ([project] if project else PROJECT_OF.values()):
        issues = rm.call("GET", f"/issues.json?project_id={proj}&assigned_to_id=me&status_id=open"
                                f"&sort=priority:desc,id&limit=100")["issues"]
        print(f"{proj}: {len(issues)} open for {me['login']}")
        for i in issues:
            print(f"  {i['subject'][:110]}  ({i['status']['name']}, {i['priority']['name']})")


def needs_cutover(what):
    if truth() != "redmine":
        raise SystemExit(f"{what} waits for the cut-over: until then the TODO files are the truth and the nightly sync "
                         f"would undo it. Claim and close in TODO.md as before ({TRUTH} says {truth()!r}).")


def update(rm, key, issue, note):
    p, i = find(rm, key)
    issue = dict(issue)
    if note:
        issue["notes"] = note
    rm.call("PUT", f"/issues/{i['id']}.json", {"issue": issue})
    return p, i


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")
    mg = sub.add_parser("migrate")
    mg.add_argument("--dry-run", action="store_true", required=True,
                    help="the only mode so far: nothing is sent to Redmine")
    mg.add_argument("--json", help="write the payload here")
    mr = sub.add_parser("mirror")
    mr.add_argument("--from", dest="src", help="a payload written by migrate --json")
    mr.add_argument("--from-redmine", action="store_true", help="rebuild the files from Redmine (refuses a loss)")
    mr.add_argument("--write", action="store_true")
    sy = sub.add_parser("sync", help="files -> Redmine until the cut-over; creates and updates, never deletes")
    sy.add_argument("--write", action="store_true")
    ex = sub.add_parser("export", help="Redmine -> one JSON file with every ticket's history (for git)")
    ex.add_argument("--out", default=str(ROOT / "docs/tickets/redmine-export.json"))
    for name, hlp in (("show", "one ticket, its fields and its last notes"), ("mine", "the open tickets of a lane"),
                      ("assign", "give a ticket to a lane"), ("claim", "take a ticket: In progress, yours, a branch"),
                      ("close", "close a ticket with the commit that closed it")):
        x = sub.add_parser(name, help=hlp)
        x.add_argument("--lane", help="work as this lane (its key in ~/.redmine.env): game, story, audio, art, app, "
                                      "hub, esp32, pi-zero, playground, docs, ops")
        if name != "mine":
            x.add_argument("ticket")
        else:
            x.add_argument("--project", choices=list(PROJECT_OF.values()))
        if name == "assign":
            x.add_argument("--to", required=True, help="the lane to give it to")
        if name == "claim":
            x.add_argument("--branch", required=True)
        if name == "close":
            x.add_argument("--commit", required=True, action="append", help="repo@sha; more than once for several")
        if name in ("assign", "claim", "close"):
            x.add_argument("--note", default="")
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

    if a.cmd in ("show", "mine", "assign", "claim", "close"):
        if a.cmd in ("mine", "claim", "close") and not a.lane:
            ap.error(f"{a.cmd} needs --lane (whose tickets, who is working)")
        rm = Redmine(a.lane)
        if a.cmd == "mine":
            return mine(rm, a.project)
        key = norm_key(a.ticket)
        if a.cmd == "show":
            return show(rm, key)
        statuses = rm.statuses()
        if a.cmd == "assign":
            ids = lane_ids(rm)
            if a.to not in ids:
                raise SystemExit(f"no lane {a.to!r}; lanes: {', '.join(sorted(ids))}")
            update(rm, key, {"assigned_to_id": ids[a.to]}, a.note)
            print(f"{key}: assigned to lane {a.to}")
            return
        needs_cutover(a.cmd)
        me = rm.call("GET", "/users/current.json")["user"]
        if a.cmd == "claim":
            p, i = find(rm, key)
            if i["status"]["name"] == "In progress" and (i.get("assigned_to") or {}).get("id") != me["id"]:
                raise SystemExit(f"{key} is already In progress for {i['assigned_to']['name']}")
            update(rm, key, {"status_id": statuses["In progress"], "assigned_to_id": me["id"],
                             "custom_fields": [{"id": p["fields"]["Branch"], "value": a.branch}]},
                   a.note or f"Claimed by {me['login']} on {a.branch}.")
            print(f"{key}: In progress, {me['login']}, {a.branch}")
            return
        p, i = find(rm, key)
        old = [x for x in (cf(i).get("Commits") or "").split("\n") if x]
        commits = old + [c for c in a.commit if c not in old]
        update(rm, key, {"status_id": statuses["Closed"],
                         "custom_fields": [{"id": p["fields"]["Commits"], "value": "\n".join(commits)},
                                           {"id": p["fields"]["Branch"], "value": ""}]},
               a.note or f"Closed by {me['login']}: {', '.join(a.commit)}.")
        print(f"{key}: Closed ({', '.join(a.commit)})")
        return
    if a.cmd == "export":
        export(a.out)
        return
    if a.cmd == "sync":
        sync(a.write)
        return
    if a.from_redmine:
        sys.exit(0 if mirror_from_redmine(a.write) else 1)
    if not a.src:
        ap.error("mirror needs --from FILE or --from-redmine")
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
