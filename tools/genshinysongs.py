#!/usr/bin/env python3
"""T-602: SHINY SONGS -- a shiny's song, from its song and its shiny palette. DRAFT, nothing approved.

    python3 tools/genshinysongs.py                     # report: the census, and a few forms' notes before and after
    python3 tools/genshinysongs.py NAME...             # those forms in full: the pull, every note moved and why
    python3 tools/genshinysongs.py --previews [DIR]    # an .mp3 sampler: each pair as normal, then shiny
                                                       # (default audio/drafts/t602_shiny)
    python3 tools/genshinysongs.py --sheets [DIR]      # a sheet per pair: the normal song over the shiny one
    python3 tools/genshinysongs.py --write             # T-602 BUILT (the user, 2026-11-22: "Yes, build it"): the
                                                       # engine's table, engineGba src/data/daemon_song_shiny.h

THE USER'S WORDS (2026-11-18): "since the colour palette is modified of the daemon, so would the shiny version song --
so the shiny song would be derived from the original song and the shiny's new palette".

WHAT A SHINY IS (tools/genshiny.py, T-432): the same drawing, its body ramp turned to the type's one shiny anchor (still
nearer its own type than any other) and its accents turned the other way round the wheel. So a shiny's colours are its
own colours moved a little -- and a shiny's song is its own song moved a little.

THE RULE. SYNESTHESIA ties a colour to a pitch (C red ... B violet, gensongs.NOTE_COLOURS). Each coloured slot a form's
front sprite uses (the body ramp, 1-4, and the accents, 6-10; never the ink, the streaks or a grey) names the note of
its KEY whose colour is nearest its hue -- shared between the two nearest notes by how near, so a small turn of hue is a small shift -- weighted by
how many pixels it covers. Done for the normal palette and for the
shiny one, that gives each palette a SHARE of every note in the key; their difference is the PULL:
    a note the shiny palette has more of than the normal one     pulls (the shiny's new colour)
    a note it has less of                                          lets go
Then, over the form's part:
    the OPENING   kept, every note: it is the cry, and the summon (T-598) listens for it -- a shiny still answers.
    the CADENCE   kept: the last two notes still go home to the key's tonic.
    the WORDS     each note may step ONE note of the key up or down onto a note that pulls harder than its own, and
                  only if it keeps the CONTOUR -- what rose still rises and what fell still falls, against the notes
                  either side as they now stand; a step may become a hold of two, never of three, so a strong pull
                  colours the tune without flattening it into a drone. The strongest gains move first; how many
                  move grows with how far the palette moved (MOVE_MIN .. MOVE_MAX of the words).
    the rest      the rhythm, the bass, the tempo, the key and every note's learning point stay the song's own, so a
                  shiny learns its song as its kind does and its colours (T-597) come in with the same notes.
EVOLUTION: a shiny's earlier forms were shiny too, so each part of its song is that form's own part moved by that form's
own shiny palette -- a shiny final form's song still carries its earlier forms, as theirs were sung by a shiny.
A form whose shiny moves nothing (no pull a contour allows) is listed: its shiny sings its kind's song.
"""
import collections, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import gencolourbysong as gcs
import gensongs as gsg

OUT_DIR = os.path.join(ROOT, "audio", "drafts", "t602_shiny")
KEEP_END = 2                     # the cadence's last notes, kept
MOVE_MIN, MOVE_MAX = 0.20, 0.45  # of the words' notes, moved -- by how far the palette moved (its pull, 0..1)
PULL_EPS = 0.02                  # a gain smaller than this is no gain
SAMPLER = ["ROVERBYTE", "BROADCAST", "GRIEVANCE", "ELATION", "CONJECTURE", "MULTICAST"]   # whole lines, six keys


class Shiny:
    def __init__(self):
        self.w = gcs.World()
        self.sp, self.paths, self.parts = gsg.build(self.w.sp)
        self._counts = {}

    def pixel_counts(self, k):
        if k not in self._counts:
            from PIL import Image
            self._counts[k] = collections.Counter(Image.open(os.path.join(self.w.folder(k), "front.png")).getdata())
        return self._counts[k]

    def has_shiny(self, k):
        return self.w.has_art(k) and os.path.exists(os.path.join(self.w.folder(k), "shiny.pal"))

    def shares(self, k, which):
        """Each note of the form's key: the share of its coloured pixels whose hue is nearest that note's colour."""
        p = self.parts[k]
        scale = gcs.SCALE[p["minor"]]
        inkey = [pc for pc in range(12) if (pc - p["tonic"]) % 12 in scale]
        pal = gcs.read_pal(os.path.join(self.w.folder(k), which + ".pal"))
        cnt = self.pixel_counts(k)
        out = collections.Counter()
        for i, c in enumerate(pal):
            if not (i in gcs.BODY or i in gcs.ACCENTS) or not cnt.get(i):
                continue
            hu, s, _ = gcs.hsv(c)
            if s < gcs.NEUTRAL:
                continue                                    # a grey carries no hue, so no note
            a, b = sorted(inkey, key=lambda q: gcs.hue_gap(hu, gcs.PC_HUE[q]))[:2]
            ga, gb = gcs.hue_gap(hu, gcs.PC_HUE[a]), gcs.hue_gap(hu, gcs.PC_HUE[b])
            out[a] += cnt[i] * gb / (ga + gb or 1)          # shared between the two nearest notes by how near, so a
            out[b] += cnt[i] * ga / (ga + gb or 1)          # small turn of hue is a small shift of weight, not none
        total = sum(out.values()) or 1
        return {pc: out.get(pc, 0) / total for pc in inkey}

    def pull(self, k):
        a, b = self.shares(k, "normal"), self.shares(k, "shiny")
        return {pc: b[pc] - a[pc] for pc in a}

    def shiny_part(self, k):
        """(the shiny part, [(index, old midi, new midi, gain)]) -- the form's own part with its words moved."""
        p = self.parts[k]
        if not self.has_shiny(k):
            return p, []
        g = self.pull(k)
        strength = min(1.0, sum(abs(v) for v in g.values()) / 2 * 2)     # half the L1 distance, doubled, capped
        notes = [list(n) for n in p["notes"]]
        n_open = _opening_len(p)                            # as gensongs.engine_rows counts it (and the summons)
        words = range(n_open, len(notes) - KEEP_END)
        sign = lambda x: (x > 0) - (x < 0)
        reverses = lambda was, now: sign(was) * sign(now) < 0          # a move may not turn the tune back
        orig = [m for m, _, _ in notes]
        cand = []
        for j in words:
            m = orig[j]
            if (m - p["tonic"]) % 12 not in gcs.SCALE[p["minor"]]:
                continue                                    # a bent note (CORRUPT's) stays bent
            for k_ in (1, -1):
                q = gsg.key_step(m, k_, p["tonic"], p["minor"])
                gain = g.get(q % 12, 0) - g.get(m % 12, 0)
                if gain > PULL_EPS and gsg.LOW <= q <= gsg.HIGH:
                    cand.append((gain, j, q))
        cand.sort(key=lambda c: (-c[0], c[1]))
        budget = max(1, round(len(words) * (MOVE_MIN + (MOVE_MAX - MOVE_MIN) * strength))) if len(words) else 0
        moved, done = [], set()
        for gain, j, q in cand:
            if len(moved) >= budget:
                break
            if j in done:
                continue
            prev, nxt = notes[j - 1][0], notes[j + 1][0]
            run = 1 + _same(notes, j - 1, -1, q) + _same(notes, j + 1, 1, q)
            if run > max(2, _longest_run(orig, j)):
                continue                                    # no new drone: a hold of two, never three
            if reverses(orig[j] - orig[j - 1], q - prev) or reverses(orig[j + 1] - orig[j], nxt - q):
                continue                                    # the contour is the song's: what rose never falls, what fell
                                                            # never rises (against its neighbours as they now stand)
            moved.append((j, orig[j], q, round(gain, 3)))
            notes[j][0] = q
            done.add(j)
        out = dict(p, notes=notes, shiny=True)
        return out, sorted(moved)

    def line(self, k, shiny):
        return [self.shiny_part(f)[0] if shiny else self.parts[f] for f in self.paths[k]]


def _same(notes, j, step, q):
    """How many notes from j outward (step -1 or 1) are q, in a row."""
    n = 0
    while 0 <= j < len(notes) and notes[j][0] == q:
        n += 1
        j += step
    return n


def _longest_run(orig, j):
    """The run of equal notes the song itself has through j (its own drones are its own)."""
    a = b = j
    while a > 0 and orig[a - 1] == orig[j]:
        a -= 1
    while b < len(orig) - 1 and orig[b + 1] == orig[j]:
        b += 1
    return b - a + 1


def _opening_len(p):
    """The opening's notes: those learned by OPEN_MAX (gensongs.thresholds learns the cry first)."""
    n = 0
    for _, _, th in p["notes"]:
        if th > gsg.OPEN_MAX + 1e-9:
            break
        n += 1
    return n


def letter(m):
    return gcs.LETTER[m % 12] + str(m // 12 - 1)


def describe(S, k):
    p = S.parts[k]
    sh, moved = S.shiny_part(k)
    g = S.pull(k) if S.has_shiny(k) else {}
    out = ["%s  %s  %d notes, opening %d" % (p["name"], p["key"], len(p["notes"]), _opening_len(p))]
    if g:
        out.append("  pull: " + ", ".join("%s %+.2f" % (gcs.LETTER[pc], v) for pc, v in sorted(g.items(), key=lambda x: -x[1]) if abs(v) >= 0.005))
    out.append("  kind : " + " ".join(letter(m) for m, _, _ in p["notes"]))
    out.append("  shiny: " + " ".join((letter(m) + "*") if any(j == i for j, *_ in moved) else letter(m)
                                       for i, (m, _, _) in enumerate(sh["notes"])))
    out.append("  moved: %d -- %s" % (len(moved), ", ".join("%d %s->%s (%+.2f)" % (j, letter(a), letter(b), gn) for j, a, b, gn in moved) or "nothing"))
    return "\n".join(out)


def report(names=None):
    S = Shiny()
    if names:
        for n in names:
            print(describe(S, S.w.by_name[n.upper()]) if n.upper() in S.w.by_name else "%s: no such daemon" % n)
        return
    kinds = collections.Counter()
    unmoved = []
    total_moved = []
    for k in S.sp:
        if not S.has_shiny(k):
            kinds["no shiny art"] += 1
            continue
        _, moved = S.shiny_part(k)
        if moved:
            kinds["moved"] += 1
            total_moved.append(len(moved))
        else:
            kinds["unmoved"] += 1
            unmoved.append(S.sp[k]["name"])
    print("T-602 SHINY SONGS (DRAFT): %d forms" % len(S.sp))
    for a, b in kinds.items():
        print("  %-13s %d" % (a, b))
    if total_moved:
        print("  notes moved a form: %d to %d, %.1f on average" % (min(total_moved), max(total_moved), sum(total_moved) / len(total_moved)))
    print("  a shiny that sings its kind's song (nothing a contour allows): %s" % (", ".join(unmoved) or "none"))
    print()
    for n in ("ROVERCUB", "LABEL", "CLUSTER", "CRAWLER"):
        if n in S.w.by_name:
            print(describe(S, S.w.by_name[n]))
            print()


def previews(outdir):
    import numpy as np
    S = Shiny()
    reel, listing = [], []
    for n in SAMPLER:
        k = S.w.by_name.get(n)
        if not k or not S.has_shiny(k):
            continue
        for shiny in (False, True):
            y = gsg.render(S.line(k, shiny), [1.0] * len(S.paths[k]))
            title = "%s's whole song (%s), %s" % (n, " -> ".join(S.sp[f]["name"] for f in S.paths[k]), "SHINY" if shiny else "its kind")
            slug = re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")[:70]
            gsg.mp3(os.path.join(outdir, "songs", slug + ".mp3"), y)
            reel += [y, np.zeros(int((0.6 if not shiny else 1.6) * gsg.SR))]
            listing.append("%-78s %5.1f s" % (title, len(y) / gsg.SR))
    gsg.mp3(os.path.join(outdir, "sampler.mp3"), np.concatenate(reel))
    with open(os.path.join(outdir, "SAMPLER.txt"), "w") as f:
        f.write("T-602 SHINY SONGS, DRAFT: the sampler, in order -- each daemon's whole line as its kind sings it, "
                "then as a shiny does\n\n" + "\n".join(listing) + "\n")
    print("genshinysongs: %d clips and sampler.mp3 in %s" % (len(listing), os.path.relpath(outdir, ROOT)))


def sheets(outdir):
    from PIL import Image
    S = Shiny()
    os.makedirs(os.path.join(outdir, "sheets"), exist_ok=True)
    tmp = os.path.join(outdir, "sheets", ".tmp.png")
    lines = []
    for n in SAMPLER:
        k = S.w.by_name.get(n)
        if not k or not S.has_shiny(k):
            continue
        ims = []
        for shiny in (False, True):
            parts = {f: (S.shiny_part(f)[0] if shiny else S.parts[f]) for f in S.paths[k]}
            gsg.sheet(S.sp, S.paths, parts, k, tmp)
            ims.append(Image.open(tmp).convert("RGB"))
        w = max(i.width for i in ims)
        out = Image.new("RGB", (w + 150, sum(i.height for i in ims) + 8), (12, 13, 18))
        y = 0
        for i, im in enumerate(ims):
            out.paste(im, (150, y))
            # the palette the part is coloured from, beside it: the form's front sprite in it
            spr = _sprite(S, S.paths[k][-1], "shiny" if i else "normal")
            if spr:
                out.paste(spr, (11, y + (im.height - spr.height) // 2), spr)
            from PIL import ImageDraw, ImageFont
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 14)
            except OSError:
                font = ImageFont.load_default()
            ImageDraw.Draw(out).text((14, y + 12), "SHINY (moved *)" if i else "ITS KIND", fill=(230, 230, 240), font=font)
            y += im.height + 8
        out.save(os.path.join(outdir, "sheets", n.lower() + ".png"))
        lines.append(describe(S, k))
    os.remove(tmp)
    with open(os.path.join(outdir, "SHINY.txt"), "w") as f:
        f.write("T-602 SHINY SONGS, DRAFT (tools/genshinysongs.py) -- * marks a note the shiny palette moved\n\n"
                + "\n\n".join(lines) + "\n")
    print("genshinysongs: %d sheets and SHINY.txt in %s" % (len(lines), os.path.relpath(outdir, ROOT)))


def _sprite(S, k, which):
    from PIL import Image
    f = S.w.folder(k)
    if not os.path.exists(os.path.join(f, "front.png")):
        return None
    im = Image.open(os.path.join(f, "front.png"))
    pal = gcs.read_pal(os.path.join(f, which + ".pal"))
    flat = [x for c in pal for x in c] + [0] * (768 - 3 * len(pal))
    im = im.copy()
    im.putpalette(flat)
    rgba = im.convert("RGBA")
    px = rgba.load()
    src = im.load()
    for yy in range(im.height):
        for xx in range(im.width):
            if src[xx, yy] == 0:
                px[xx, yy] = (0, 0, 0, 0)
    return rgba.resize((128, 128), Image.NEAREST)


# ---------------------------------------------------------------------------------------------------------------------
# The engine (T-602 built): only the notes a shiny moves -- src/daemon_song.c sings its kind's part and, for a shiny,
# looks each note up here first. Its colours (T-597) stay its kind's: a shiny learns its colours as its kind does.
# ---------------------------------------------------------------------------------------------------------------------
ENGINE_H = os.path.join(ROOT, "engineGba", "src", "data", "daemon_song_shiny.h")


def engine_moves(S=None):
    S = S or Shiny()
    rows = []
    for k in sorted(S.sp, key=int):
        _, moved = S.shiny_part(k)
        for j, a, b, _ in moved:
            assert 0 <= j < 255 and 0 <= b <= 127, (S.sp[k]["name"], j, b)
            rows.append((int(k), j, b, S.sp[k]["name"], letter(a), letter(b)))
    return rows


def engine_header(rows=None):
    rows = rows if rows is not None else engine_moves()
    forms = len({r[0] for r in rows})
    out = ["// T-602: SHINY SONGS -- the notes a shiny sings that its kind does not: each one a note of its own part",
           "// stepped toward the notes its shiny palette's colours name (SYNESTHESIA), the contour, opening and cadence kept.",
           "// GENERATED by DAEMONS tools/genshinysongs.py --write -- never edit by hand. DRAFT, every note.",
           "// src/daemon_song.c (ShinyNote) looks a shiny's note up here, sorted by species then note.",
           "// %d notes moved, in %d forms." % (len(rows), forms),
           "",
           "struct DaemonShinyNote",
           "{",
           "    u16 species;",
           "    u8 index;        // the note of the form's own part (sSongParts[species].note + index)",
           "    u8 note;         // what a shiny sings there (MIDI)",
           "};",
           "",
           "static const struct DaemonShinyNote sShinyNotes[] = {"]
    for sp, j, b, name, a_, b_ in rows:
        out.append("    {%d, %d, %d},   // %s: %s -> %s" % (sp, j, b, name, a_, b_))
    out += ["};", ""]
    return "\n".join(out)


def engine_write(write):
    want = engine_header()
    have = open(ENGINE_H).read() if os.path.exists(ENGINE_H) else None
    rel = os.path.relpath(ENGINE_H, ROOT)
    if not write:
        state = "current" if have == want else ("missing" if have is None else "DRIFTS from a write")
        print("genshinysongs: the engine's table (%s) is %s" % (rel, state))
        return 0 if have == want else 1
    if have == want:
        print("genshinysongs: %s already current" % rel)
        return 0
    tmp = ENGINE_H + ".tmp"
    with open(tmp, "w") as f:
        f.write(want)
    os.replace(tmp, ENGINE_H)
    print("genshinysongs: wrote %s (%d notes, about %.1f KB of ROM)" % (rel, want.count("\n    {"), want.count("\n    {") * 4 / 1024))
    return 0


def main():
    a = sys.argv[1:]
    def after(flag, default):
        i = a.index(flag)
        return a[i + 1] if i + 1 < len(a) and not a[i + 1].startswith("--") else default
    if "--write" in a:
        sys.exit(engine_write(True))
    if "--previews" in a:
        previews(after("--previews", OUT_DIR))
    elif "--sheets" in a:
        sheets(after("--sheets", OUT_DIR))
    else:
        names = [x for x in a if not x.startswith("--")]
        report(names)
        if not names:
            sys.exit(engine_write(False))


if __name__ == "__main__":
    main()
