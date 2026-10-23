"""The helpers the tools had each been carrying a copy of -- one copy, imported (T-421).

    from daemonslib import read_pal, write_pal, upstream, preview

read_pal / write_pal   a 16-colour JASC-PAL, as the engine's .gitattributes keeps it (CRLF)
upstream               vanilla's copy of a file, `git show upstream/master:<rel>`, failing LOUDLY
preview                where a report-mode preview goes: /tmp/<name>, or $DAEMONS_PREVIEW_DIR/<name>
tileset_base           the tileset whose FOLDER a tileset draws from (a palette split has none of its own, T-438)

As tools/fontwidth.py: nothing here imports a tool, so importing it runs nothing. A tool whose own copy BEHAVED
differently kept it (a git with a timeout, a write in LF with its own count); T-421's row in docs/TODO.md lists
them. A palette of any length (sized=) and a write that pads to sixteen (pad=) were folded in later (T-421).
"""
import os, re, subprocess, sys

# ---------------------------------------------------------------------------------------------------- palettes


def read_pal(path, sized=False):
    """The sixteen colours of a JASC-PAL file, as (r, g, b) tuples (lines 4-19; CR or CRLF alike). sized=True reads
    as many as the file's own third line says, for the tools that take a palette of any length."""
    L = open(path).read().replace("\r", "").split("\n")
    return [tuple(map(int, l.split())) for l in L[3:3 + int(L[2]) if sized else 19]]


def write_pal(path, colours, pad=False):
    """A JASC-PAL file, CRLF, as .gitattributes has it: written LF, git rewrites every one on checkout. pad=True fills
    a short palette out to sixteen with black."""
    if pad:
        colours = list(colours) + [(0, 0, 0)] * (16 - len(colours))
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


# ---------------------------------------------------------------------------------------------------- tilesets
_HEADERS = {}


def tileset_base(gba, symbol):
    """The tileset whose folder `symbol` draws from. The tools find a tileset's folder by its name (gTileset_RockTunnel
    -> secondary/rock_tunnel), and a PALETTE SPLIT has no folder of its own (T-438 batch E): gTileset_OtherCave is a
    Tileset header that reuses gTileset_RockTunnel's tiles, metatiles and attributes with palettes of its own. So a
    symbol with no folder of its own answers the header that shares its metatiles and has one; any other symbol is
    returned as it is. Its palettes are the one thing that differs: tileset_palettes() reads those."""
    want = lambda sym: re.sub(r"[^a-z0-9]", "", sym.replace("gTileset_", "").lower())
    dirs = {re.sub(r"[^a-z0-9]", "", d.lower()) for k in ("primary", "secondary")
            for d in os.listdir(os.path.join(gba, "data/tilesets", k))}
    if not symbol or want(symbol) in dirs:
        return symbol
    if gba not in _HEADERS:
        _HEADERS[gba] = dict(re.findall(r"const struct Tileset (\w+) =\s*\{(.*?)\};",
                                        open(os.path.join(gba, "src/data/tilesets/headers.h")).read(), re.S))
    hdr = _HEADERS[gba]
    mt = re.search(r"\.metatiles = (\w+)", hdr.get(symbol, ""))
    for other, body in hdr.items():
        if mt and other != symbol and want(other) in dirs and re.search(r"\.metatiles = %s\b" % mt.group(1), body):
            return other
    return symbol


def tileset_palettes(gba, symbol):
    """the sixteen .pal files a tileset's header loads, by its .palettes table in graphics.h (None if not found)"""
    body = re.search(r"const struct Tileset %s =\s*\{(.*?)\};" % re.escape(symbol),
                     open(os.path.join(gba, "src/data/tilesets/headers.h")).read(), re.S)
    p = body and re.search(r"\.palettes = (\w+)", body.group(1))
    gfx = open(os.path.join(gba, "src/data/tilesets/graphics.h")).read()
    t = p and re.search(r"%s\[\]\[16\] =\s*\{(.*?)\};" % re.escape(p.group(1)), gfx, re.S)
    if not t:
        return None
    return [os.path.join(gba, f[:-len(".gbapal")] + ".pal") for f in re.findall(r'INCBIN_U16\("([^"]+)"\)', t.group(1))]
