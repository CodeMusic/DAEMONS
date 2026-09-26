#!/usr/bin/env python3
"""Publish a ROM release to GitHub: its notes, and its four BPS patches as downloads -- never a ROM.

    python3 tools/ghrelease.py                 # report what the newest release would publish
    python3 tools/ghrelease.py --write         # create the GitHub release on CodeMusic/DAEMONS
    python3 tools/ghrelease.py v11.288.10      # a named release instead of the newest

`romrelease.py` files each release under `ROM RELEASE/` with its notes (committed) and its ROMs and patches (never
committed: the ROMs are Nintendo's engine with our work in it, and the patches are too large for git). This is the
step after it. It tags the commit that filed the notes, uses the notes as the page, puts the player's guide
(`ROM RELEASE/HOW_TO_PATCH.md`) at the top, and uploads the four `.bps` files. Nothing else in the folder is
uploaded, and it refuses outright if a `.gba` would be.

It refuses a release whose patches are missing (the folder of a sealed group keeps only its last ROMs), a tag that
already exists, and a dirty tree -- the tag must point at what is published.
"""
import glob, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REL = os.path.join(ROOT, "ROM RELEASE")
REPO = "CodeMusic/DAEMONS"
WRITE = "--write" in sys.argv


def run(*cmd, check=True):
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if check and r.returncode:
        raise SystemExit("  refused: %s failed\n%s" % (" ".join(cmd[:3]), r.stderr[-1200:]))
    return r


def newest():
    found = []
    for meta in glob.glob(os.path.join(REL, "v*.x", "v*", ".release.json")):
        folder = os.path.dirname(meta)
        found.append((os.path.getmtime(meta), os.path.basename(folder), folder))
    if not found:
        raise SystemExit("  refused: no release folders under ROM RELEASE/")
    return max(found)[1:]


def main():
    names = [a for a in sys.argv[1:] if a.startswith("v")]
    if names:
        hits = glob.glob(os.path.join(REL, "v*.x", names[0]))
        if not hits:
            raise SystemExit("  refused: no release called %s" % names[0])
        name, folder = names[0], hits[0]
    else:
        name, folder = newest()
    patches = sorted(glob.glob(os.path.join(folder, "PATCHES", "*.bps")))
    notes_path = os.path.join(folder, "RELEASE_NOTES.md")
    if len(patches) != 4 or not os.path.exists(notes_path):
        raise SystemExit("  refused: %s has %d patches and %s notes -- run romrelease.py --write first"
                         % (name, len(patches), "its" if os.path.exists(notes_path) else "no"))
    if any(p.lower().endswith(".gba") for p in patches):
        raise SystemExit("  refused: a ROM is in the upload list")

    rel = os.path.relpath(notes_path, ROOT)
    commit = run("git", "log", "-1", "--format=%H", "--", rel).stdout.strip()
    if not commit:
        raise SystemExit("  refused: %s is not committed -- commit what romrelease.py wrote first" % rel)
    dirty = run("git", "status", "--porcelain").stdout.strip()
    exists = run("gh", "release", "view", name, "-R", REPO, check=False).returncode == 0

    guide = open(os.path.join(REL, "HOW_TO_PATCH.md")).read()
    guide = guide.replace("](WHERES_THE_ROMS.md)", "](https://github.com/%s/blob/main/ROM%%20RELEASE/WHERES_THE_ROMS.md)" % REPO)
    guide = guide.replace("](../README.md)", "](https://github.com/%s/blob/main/README.md)" % REPO)
    notes = open(notes_path).read()
    body = ("**Play DAEMONS from your own cartridge.** Download the one `.bps` below that matches your ROM and apply "
            "it. The full guide follows the notes.\n\n" + notes + "\n---\n\n" + guide)

    print("  release    %s  (%s)" % (name, os.path.relpath(folder, ROOT)))
    print("  tag        %s at %s" % (name, commit[:8]))
    for p in patches:
        print("  upload     %s  (%d KB)" % (os.path.basename(p), os.path.getsize(p) // 1024))
    print("  page       %d characters: a line, the release notes, then HOW_TO_PATCH.md" % len(body))
    problem = ("%s is already published on GitHub" % name if exists else
               "the tree is dirty -- the tag must point at what is published" if dirty else None)
    if not WRITE:
        print("  report only; pass --write to publish%s" % ("  (it would refuse: %s)" % problem if problem else ""))
        return
    if problem:
        raise SystemExit("  refused: " + problem)
    body_path = os.path.join(folder, ".github_body.md")
    open(body_path, "w").write(body)
    try:
        run("gh", "release", "create", name, *patches, "-R", REPO, "--target", commit,
            "--title", "DAEMONS %s" % name, "--notes-file", body_path)
    finally:
        os.remove(body_path)
    url = run("gh", "release", "view", name, "-R", REPO, "--json", "url").stdout
    print("  published  %s" % json.loads(url)["url"])


if __name__ == "__main__":
    main()
