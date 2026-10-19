"""The helpers the tools had each been carrying a copy of -- one copy, imported (T-421).

    from daemonslib import read_pal, write_pal, upstream, preview

read_pal / write_pal   a 16-colour JASC-PAL, as the engine's .gitattributes keeps it (CRLF)
upstream               vanilla's copy of a file, `git show upstream/master:<rel>`, failing LOUDLY
preview                where a report-mode preview goes: /tmp/<name>, or $DAEMONS_PREVIEW_DIR/<name>

As tools/fontwidth.py: nothing here imports a tool, so importing it runs nothing. A tool whose own copy BEHAVED
differently kept it (a palette of any length, a write that pads to sixteen, a git with a timeout); T-421's row in
docs/TODO.md lists them.
"""
import os, subprocess, sys

# ---------------------------------------------------------------------------------------------------- palettes


def read_pal(path):
    """The sixteen colours of a JASC-PAL file, as (r, g, b) tuples (lines 4-19; CR or CRLF alike)."""
    return [tuple(map(int, l.split())) for l in open(path).read().replace("\r", "").split("\n")[3:19]]


def write_pal(path, colours):
    """A JASC-PAL file, CRLF, as .gitattributes has it: written LF, git rewrites every one on checkout."""
    lines = ["JASC-PAL", "0100", "16"] + ["%d %d %d" % c for c in colours]
    open(path, "wb").write(("\r\n".join(lines) + "\r\n").encode())


# ---------------------------------------------------------------------------------------------------- vanilla

#  The value `missing` takes when nothing was passed: a file vanilla never had stops the run like any other failure.
_EXIT = object()
#  What git says when the path is simply not in that tree -- the one failure that can mean "vanilla never had it".
_ABSENT = ("does not exist in", "exists on disk, but not in")


def upstream(repo, rel, missing=_EXIT, binary=False, ref="upstream/master"):
    """vanilla's copy of REL in REPO (an engine checkout with an `upstream` remote).

    Any failed git -- no upstream remote, a bad ref, a path vanilla never had -- stops the run with git's own error
    (T-421: about twelve tools read a failure as "", so a fork with no upstream remote made every name look new and
    every check pass). Pass `missing=` (a value: "", b"", None) only where a file vanilla never had is expected: then
    that one failure returns it, and every other still stops the run.

    Text is read as `subprocess.run(..., text=True)` reads it -- the locale's codec, universal newlines -- which is
    what each tool's own copy did; binary=True returns the bytes untouched.
    """
    r = subprocess.run(["git", "-C", repo, "show", "%s:%s" % (ref, rel)], capture_output=True, text=not binary)
    if r.returncode != 0:
        err = r.stderr if not binary else r.stderr.decode("utf-8", "replace")
        if missing is not _EXIT and any(s in err for s in _ABSENT):
            return missing
        sys.exit("  !! git show %s:%s failed: %s" % (ref, rel, err.strip()))
    return r.stdout


# ---------------------------------------------------------------------------------------------------- previews


def preview(name):
    """Where a report-mode preview is written: /tmp/NAME, as the tools always have, or under $DAEMONS_PREVIEW_DIR
    when it is set -- so two sessions, or check_generators, need not write over each other's /tmp/NAME."""
    d = os.environ.get("DAEMONS_PREVIEW_DIR")
    if not d:
        return os.path.join("/tmp", name)
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, name)
