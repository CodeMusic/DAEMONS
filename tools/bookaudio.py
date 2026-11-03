"""Render a DAEMONS book (companion server/data/<book>.json) to an MP3 audiobook with chapter markers, in its own voice.

Usage: python3 tools/bookaudio.py <guide|subtle|hermetic|textbook> <out_dir> [--voice NAME]
       python3 tools/bookaudio.py --check <out_dir>        # which books on disk are current
Needs kokoro-onnx, soundfile and ffmpeg (with rubberband), plus kokoro-v1.0.onnx and voices-v1.0.bin in KOKORO_DIR
(default ~/.cache/daemons/kokoro, from github.com/thewh1teagle/kokoro-onnx's releases).
Writes <out_dir>/<file>.mp3 and <file>.chapters.json. A SEALED book goes into a zip the way tools/bookpdf.py seals the
vault, and nothing of it is left open. Each paragraph is cached under BOOKAUDIO_CACHE (default ~/.cache/daemons/bookaudio)
by its words and its voice, so a changed word or voice is rendered again and nothing else is.

Each book has its own voice (T-518, the user 2026-11-01: "each voice for eachbook should be different -- reflecting the
books essence"), picked by multiple choice from samples: a Kokoro voice or a blend of their style vectors, and a speed.
The third book is one voice in two halves, each leaned toward what it says by blend, pitch, tone and pause.
"""
import hashlib, json, os, re, subprocess, sys, tempfile, zipfile
import numpy as np, soundfile as sf

DATA = os.environ.get("BOOK_DATA", "../daemons-companion/server/data")
KOKORO = os.environ.get("KOKORO_DIR", os.path.expanduser("~/.cache/daemons/kokoro"))
CACHE = os.environ.get("BOOKAUDIO_CACHE", os.path.expanduser("~/.cache/daemons/bookaudio"))
SR = 24000
GAP = {"para": 0.45, "entry": 1.2, "section": 2.2}
VOICES = {  # picked with the user from samples, 2026-11-01
    "reason": {"blend": {"am_michael": 0.6, "bm_george": 0.4}, "speed": 0.97},   # the GUIDE: even, unhurried
    "instinct": {"blend": {"af_bella": 1.0}, "speed": 0.96},                      # THE SUBTLE LAYER: warm and full
    # the third book's two halves: one voice (bf_isabella), each half leaned toward what it says
    "night": {"blend": {"bf_isabella": 0.7, "af_nicole": 0.3}, "speed": 0.9, "pitch": -1.5,
              "tone": "bass=g=3:f=140,lowpass=f=6500"},                            # low, close, drawn down
    "dawn": {"blend": {"bf_isabella": 0.75, "bf_alice": 0.25}, "speed": 0.86, "pitch": 0.8, "sentence": 0.9,
             "clause": 0.3, "pause": 1.5, "tone": "highpass=f=110,treble=g=2:f=5000"},  # lighter, slower, leaves room
    "professor": {"blend": {"bm_fable": 0.5, "bm_lewis": 0.5}, "speed": 0.94,     # the TEXTBOOK (2026-11-03): grave, warm
                  "tone": "alimiter=limit=0.89:level=disabled"},             # its loudest syllables touched 0 dB
}
BOOK_VOICE = {"guide": "reason", "subtle": "instinct", "hermetic": "night", "textbook": "professor"}   # its counterbalance takes "dawn"
FILE = {"guide": "guide", "subtle": "the-subtle-layer", "hermetic": "the-vault-audio", "textbook": "principles-of-mind"}
RATE = {"textbook": "48k"}       # a long book a little lighter, under GitHub's 50 MB; the rest 64k
SEALED = {"hermetic"}             # and its counterbalance, until that is decided otherwise
SEAL_INSIDE = "sealed"            # the names a closed zip shows (sealed.mp3, sealed.chapters.json): they say nothing
DRAFT = "DRAFT · every word, until it is approved"                              # as the PDFs' covers say it
ROMAN = {"I": "one", "II": "two", "III": "three", "IV": "four", "V": "five", "VI": "six", "VII": "seven",
         "VIII": "eight", "IX": "nine", "X": "ten", "XI": "eleven", "XII": "twelve", "XIII": "thirteen"}
KEEP_CAPS = {"AI", "OK", "TV", "DNA", "NPC", "HP"}


def speakable(t: str) -> str:
    def fix(m):
        w = m.group(0)
        if w in ROMAN: return ROMAN[w]
        if w in KEEP_CAPS: return w
        return w.capitalize() if w.isupper() and len(w) > 1 else w
    t = re.sub(r"\b[A-Z][A-Z']+\b", fix, t)
    t = re.sub(r"([Dd])aemon", r"\1aymon", t)  # said DAY-mons, as the hub's voices say it (companion C-270); eudaemon too
    return re.sub(r"\s+", " ", t.replace("—", ", ").replace("–", ", ")).strip()


def titled(t):
    return " ".join(w.capitalize() for w in t.split())


def chunks(t: str, limit=380):
    out, cur = [], ""
    for s in re.findall(r"[^.!?]+[.!?\"”']*\s*", t) or [t]:
        if len(cur) + len(s) > limit and cur:
            out.append(cur.strip()); cur = ""
        cur += s
    if cur.strip(): out.append(cur.strip())
    return out


TEXTBOOK = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs/manual-textbook/manual.md")
FLOOR = {f"{n}F": f"the {w} floor" for n, w in enumerate(
    ("first", "second", "third", "fourth", "fifth", "sixth", "seventh"), 1)}
SKIP = {"references", "reading"}  # what a reader skips aloud: the References, and each chapter's Further Reading


def plain(t: str) -> str:
    """A line of the TEXTBOOK's markdown as it is said: no marks, no links, no (1.3) pointing at a section."""
    t = re.sub(r"\[([^\]]*)\]\{[^}]*\}", r"\1", t)                    # [Research Spotlight · ...]{.bh}
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)                    # a link says its words
    t = re.sub(r"\s*\((?:intro|Ch\. \d+|\d+\.\d+)(?:, (?:intro|Ch\. \d+|\d+\.\d+))*\)", "", t)
    t = re.sub(r"(?<!\w)-(\w)", r"\1", t)                             # the -s of daemons: the s
    t = re.sub(r"(\w)-(?=[*\s,.)]|$)", r"\1", t)                      # un- and -able: un, able
    t = t.replace("**", "").replace("*", "").replace(" · ", ". ").replace("&middot;", ". ")
    return re.sub(r"<[^>]+>", "", t).strip()


def chalk(text):
    """The game's lines as the TEXTBOOK quotes them: a blank line parts them, a newline is a space."""
    return [" ".join(p.split("\n")) for p in text.split("\n\n") if p.strip()]


def textbook_script():
    """CALLOW SCHOOL's TEXTBOOK (T-520), read from its markdown: each floor's placard and boards from the build's
    export, as tools/manual.py quotes them; every figure by its caption; no References, no Further Reading."""
    school = {f["floor"]: f for f in json.load(open(f"{DATA}/school.json"))["floors"]}
    lines = [("section", "Principles of Mind", "Principles of Mind. An Introduction in Seven Floors. By the Faculty of "
              "Callow School. Every passage quoted from the game is a draft, every word, until it is approved.")]
    divs, chapter, skip_h1, para = [], 0, False, []

    def flush():
        if para and not skip_h1 and not SKIP & set(divs):
            text = " ".join(para)
            text = plain(text.replace(" · ", ", ") if "terms" in divs else text)   # Key Terms, as a list
            if text: lines.append(("para", None, text))
        para.clear()
    for raw in open(TEXTBOOK, encoding="utf-8"):
        line = raw.rstrip("\n")
        h = re.match(r"^(#{1,3}) (.+?)\s*(\{[^}]*\})?\s*$", line)
        if h:
            flush()
            title, attrs = plain(h.group(2)), h.group(3) or ""
            if len(h.group(1)) == 1:
                skip_h1 = bool(SKIP & set(re.findall(r"#([\w-]+)", attrs)))
                if skip_h1: continue
                if ".unnumbered" not in attrs:
                    chapter += 1; title = f"Chapter {chapter}: {title}"
                lines.append(("section", title, title.replace(":", ".", 1) + "."))
            elif not skip_h1 and title != "Further Reading":
                lines.append(("entry", title, re.sub(r"^(\d+\.\d+) ", r"\1, ", title) + "."))
            continue
        if skip_h1: continue
        d = re.match(r"^(:{3,})\s*(.*)$", line)
        if d:
            flush()
            if d.group(2): divs.append(" ".join(re.findall(r"[\w-]+", d.group(2))).split()[-1])
            elif divs: divs.pop()
            continue
        sc = re.match(r"^\{\{(\w+) ([^|}]*)(?:\|(.*))?\}\}\s*$", line)
        if sc:
            flush()
            kind, args = sc.group(1), sc.group(2).split()
            if kind == "placard":
                f = school[args[0]]
                text = f["placard"].split("\n\n", 1)[1] if "\n\n" in f["placard"] else f["placard"]
                lines.append(("para", None, f"The placard by the stairs, on {FLOOR[args[0]]}."))
                lines += [("para", None, p) for p in chalk(text)]
            elif kind == "board":
                f = school[args[0]]
                b = next(b for b in f["board"] if b["topic"] == " ".join(args[1:]))
                lines.append(("para", None, f"On the board, {FLOOR[args[0]]}, {titled(f['subject'])}: {titled(b['topic'])}."))
                lines += [("para", None, p) for p in chalk(b["text"])]
            elif kind == "diagram" and sc.group(3):
                lines.append(("para", None, re.sub(r"^(Figure \d+\.\d+) ", r"\1. ", plain(sc.group(3)))))
            continue
        if not line.strip():
            flush(); continue
        bh = re.match(r"^\[(.+)\]\{\.bh\}\s*$", line)
        if bh:                                                         # a box's own heading, said on its own
            flush()
            if not SKIP & set(divs): lines.append(("para", None, plain(bh.group(1)) + "."))
            continue
        if re.match(r"^\s*(?:- |\d+\. )", line) or (divs and divs[-1] == "glossary" and line.startswith("**")):
            flush()
            line = re.sub(r"^\s*- ", "", line)
            if divs and divs[-1] == "glossary":
                line = re.sub(r"^\*\*(.+?)\*\*\s+", lambda m: m.group(1)[:1].upper() + m.group(1)[1:] + ". ", line)
        para.append(line.strip())
    flush()
    return lines


def script(book: str):
    """[(kind, chapter_title_or_None, text)] in reading order."""
    if book == "textbook":
        return textbook_script()
    d = json.load(open(f"{DATA}/{book}.json"))
    lines = []
    head = d["title"] + (f". {d['subtitle']}" if d.get("subtitle") else "") + (f". By {d['author']}" if d.get("author") else "") + "."
    if d.get("draft"): head += " A draft, every word, until it is approved."
    lines.append(("section", titled(d["title"]), head))
    for s in d["sections"]:
        label = s.get("heading") or s.get("label")
        names = [x for x in (s.get("label"), s.get("heading")) if x]
        if len(names) == 2 and names[0].lower() == names[1].lower(): names = names[1:]
        lines.append(("section", label, ". ".join(names) + "."))
        for e in s["entries"]:
            lines.append(("entry", e["title"], e["title"] + "."))
            for p in e["paragraphs"]:
                lines.append(("para", None, p["text"] if isinstance(p, dict) else p))
    return lines


def sources(book, voice):
    """What the recording is made of -- every word as spoken and the whole voice -- as a short hash."""
    said = [(kind, title, speakable(text)) for kind, title, text in script(book)]
    return hashlib.sha256(json.dumps([said, VOICES[voice]], sort_keys=True).encode()).hexdigest()[:16]


def recorded(book, out_dir):
    """The sources hash a recording on disk was made from: None if there is none, "" if it carries no hash."""
    path = f"{out_dir}/{FILE.get(book, book)}" + (".zip" if book in SEALED else ".chapters.json")
    if not os.path.exists(path):
        return None
    if book in SEALED:
        with zipfile.ZipFile(path) as z:
            m = re.search(r"sources (\w+)", z.comment.decode("utf-8", "replace"))
        return m.group(1) if m else ""
    return json.load(open(path)).get("sources", "")


def silence(s): return np.zeros(int(s * SR), np.float32)


def ffescape(t): return re.sub(r"([=;#\\\n])", r"\\\1", t)


def seal(paths, zip_path, digest):
    """As tools/bookpdf.py seals the vault: its key (the author's name as the book's warning gives it), names that
    say nothing, ZipCrypto, the hash in the comment. The key is never printed."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import bookpdf
    key = bookpdf.author_of_hermetic(bookpdf.layer_book("hermetic"))
    with tempfile.TemporaryDirectory(prefix="daemons-vault-") as work:
        tmp = os.path.join(work, "vault.zip")
        # -0: kept, not deflated (an MP3 does not shrink), so the companion opens it with ZipCrypto alone (C-277)
        r = subprocess.run(["zip", "-q", "-0", "-j", "-X", "-P", key, tmp, *paths], capture_output=True, text=True)
        if r.returncode:
            raise SystemExit("bookaudio: zip failed\n" + r.stderr)
        subprocess.run(["zip", "-q", "-z", tmp], input="sources %s\n" % digest, text=True, check=True)
        with zipfile.ZipFile(tmp) as z:                 # it opens with the key, and with nothing else
            z.setpassword(key.encode())
            if z.read(f"{SEAL_INSIDE}.mp3")[:3] != b"ID3":
                raise SystemExit("bookaudio: the vault does not open with its key")
        os.replace(tmp, zip_path)


def main(book, out_dir, voice):
    from kokoro_onnx import Kokoro
    v = VOICES[voice]
    k = Kokoro(f"{KOKORO}/kokoro-v1.0.onnx", f"{KOKORO}/voices-v1.0.bin")
    tot = sum(v["blend"].values())
    style = sum(k.get_voice_style(n) * (w / tot) for n, w in v["blend"].items()).astype(np.float32)
    clips = f"{CACHE}/{book}"; os.makedirs(clips, exist_ok=True)
    pause = v.get("pause", 1.0)
    parts, chapters, t = [], [], 0.0
    lines = script(book)
    for i, (kind, title, text) in enumerate(lines):
        if kind in ("section", "entry") and title and i:
            parts.append(silence(GAP[kind] * pause)); t += GAP[kind] * pause
        if title:
            chapters.append({"kind": kind, "title": title, "start": round(t, 2)})
        said = speakable(text)
        made = [said] + [v.get(x) for x in ("blend", "speed", "sentence", "clause")]
        wav = f"{clips}/{hashlib.sha1(json.dumps(made, sort_keys=True).encode()).hexdigest()[:20]}.wav"
        if not os.path.exists(wav):
            got = []
            for c in chunks(said):
                if got: got.append(silence(v.get("sentence", 0.25)))
                got.append(k.create(c, voice=style, speed=v.get("speed", 1.0), lang="en-us",
                                    sentence_pause=v.get("sentence", 0.25), clause_pause=v.get("clause", 0.1))[0])
            sf.write(wav, np.concatenate(got), SR)
        a, _ = sf.read(wav, dtype="float32")
        parts.append(a); t += len(a) / SR
        parts.append(silence(GAP["para"] * pause)); t += GAP["para"] * pause
        print(f"{book} {i + 1}/{len(lines)} {t / 60:.1f} min", flush=True)
    total = t
    for j, c in enumerate(chapters):
        c["end"] = chapters[j + 1]["start"] if j + 1 < len(chapters) else round(total, 2)
    digest = sources(book, voice)
    name = SEAL_INSIDE if book in SEALED else FILE.get(book, book)
    title = lines[0][1]
    with tempfile.TemporaryDirectory(prefix="daemons-audio-") as work:
        full = f"{work}/{book}.wav"; sf.write(full, np.concatenate(parts), SR)
        files = [f"{work}/{name}.chapters.json", f"{work}/{name}.mp3"]
        json.dump({"book": book, "voice": voice, **v, "draft": DRAFT, "sources": digest, "duration": round(total, 2),
                   "chapters": chapters}, open(f"{work}/{name}.chapters.json", "w"), indent=1)
        meta = f"{work}/{book}.ffmeta"
        with open(meta, "w") as m:
            m.write(";FFMETADATA1\n")
            for c in chapters:
                if c["kind"] == "entry":
                    m.write(f"[CHAPTER]\nTIMEBASE=1/1000\nSTART={int(c['start'] * 1000)}\nEND={int(c['end'] * 1000)}\ntitle={ffescape(c['title'])}\n")
        shape = ([f"rubberband=pitch={2 ** (v['pitch'] / 12):.4f}:formant=preserved"] if v.get("pitch") else []) + \
                ([v["tone"]] if v.get("tone") else [])
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", full, "-i", meta, "-map_metadata", "1", "-map_chapters", "1",
                        *(["-af", ",".join(shape)] if shape else []),
                        "-metadata", f"title={title} (DRAFT)", "-metadata", "artist=Christopher Art Hicks",
                        "-metadata", "album=DAEMONS books", "-metadata", f"comment={DRAFT}",
                        "-ac", "1", "-c:a", "libmp3lame", "-b:a", RATE.get(book, "64k"), f"{work}/{name}.mp3"], check=True)
        os.makedirs(out_dir, exist_ok=True)
        if book in SEALED:
            seal(files, f"{out_dir}/{FILE.get(book, book)}.zip", digest)
        else:
            for p in files:
                os.replace(p, f"{out_dir}/{os.path.basename(p)}")
    print(f"DONE {book} in {voice}, {total / 60:.1f} min, sources {digest}", flush=True)


def check(out_dir):
    for book, voice in BOOK_VOICE.items():
        have, want = recorded(book, out_dir), sources(book, voice)
        print(f"  {book}: {voice}, sources {want}; {FILE.get(book, book)} is " +
              ("missing" if have is None else "current" if have == want else "out of date"))


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--check":
        check(args[1] if len(args) > 1 else "docs/books/audio")
    else:
        voice = args[args.index("--voice") + 1] if "--voice" in args else BOOK_VOICE.get(args[0])
        if voice not in VOICES:
            raise SystemExit(f"bookaudio: {args[0]} has no voice; name one with --voice ({', '.join(VOICES)})")
        main(args[0], args[1], voice)
