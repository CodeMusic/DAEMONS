"""Render a DAEMONS book (companion server/data/<book>.json) to an MP3 audiobook with chapter markers.

Usage: python3 tools/bookaudio.py <subtle|guide|hermetic> <out_dir>
Needs kokoro-onnx, soundfile and ffmpeg, plus kokoro-v1.0.onnx and voices-v1.0.bin beside this file (or in KOKORO_DIR).
Writes <out_dir>/<book>.mp3, <book>.chapters.json and caches each paragraph under <out_dir>/clips/<book>/.
"""
import json, os, re, subprocess, sys
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

DATA = os.environ.get("BOOK_DATA", "../daemons-companion/server/data")
HERE = os.environ.get("KOKORO_DIR", os.path.dirname(os.path.abspath(__file__)))
VOICE, SR = "af_heart", 24000
GAP = {"para": 0.45, "entry": 1.2, "section": 2.2}
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
    t = re.sub(r"\b([Dd])aemon", r"\1aymon", t)  # said DAY-mons, as the hub's voices say it (companion C-270)
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


def script(book: str):
    """[(kind, chapter_title_or_None, text)] in reading order."""
    d = json.load(open(f"{DATA}/{book}.json"))
    lines = []
    head = d["title"] + (f". {d['subtitle']}" if d.get("subtitle") else "") + (f". By {d['author']}" if d.get("author") else "") + "."
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


def main(book, out_dir):
    clips = f"{out_dir}/clips/{book}"; os.makedirs(clips, exist_ok=True)
    k = Kokoro(f"{HERE}/kokoro-v1.0.onnx", f"{HERE}/voices-v1.0.bin")
    parts, chapters, t = [], [], 0.0
    lines = script(book)
    for i, (kind, title, text) in enumerate(lines):
        if kind in ("section", "entry") and title and i:
            parts.append(np.zeros(int(GAP[kind] * SR), np.float32)); t += GAP[kind]
        if title:
            chapters.append({"kind": kind, "title": title, "start": round(t, 2)})
        wav = f"{clips}/{i:04d}.wav"
        if not os.path.exists(wav):
            audio = np.concatenate([k.create(c, voice=VOICE, speed=1.0, lang="en-us")[0] for c in chunks(speakable(text))])
            sf.write(wav, audio, SR)
        a, _ = sf.read(wav, dtype="float32")
        parts.append(a); t += len(a) / SR
        parts.append(np.zeros(int(GAP["para"] * SR), np.float32)); t += GAP["para"]
        print(f"{book} {i + 1}/{len(lines)} {t / 60:.1f} min", flush=True)
    full = f"{out_dir}/{book}.wav"; sf.write(full, np.concatenate(parts), SR)
    total = t
    for j, c in enumerate(chapters):
        c["end"] = chapters[j + 1]["start"] if j + 1 < len(chapters) else round(total, 2)
    json.dump({"book": book, "voice": VOICE, "duration": round(total, 2), "chapters": chapters},
              open(f"{out_dir}/{book}.chapters.json", "w"), indent=1)
    meta = f"{out_dir}/{book}.ffmeta"
    with open(meta, "w") as m:
        m.write(";FFMETADATA1\n")
        for c in chapters:
            if c["kind"] == "entry":
                m.write(f"[CHAPTER]\nTIMEBASE=1/1000\nSTART={int(c['start'] * 1000)}\nEND={int(c['end'] * 1000)}\ntitle={c['title']}\n")
    title = titled(json.load(open(f"{DATA}/{book}.json"))["title"])
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", full, "-i", meta, "-map_metadata", "1", "-map_chapters", "1",
                    "-metadata", f"title={title}", "-metadata", "artist=Christopher Art Hicks", "-metadata", "album=DAEMONS books",
                    "-ac", "1", "-c:a", "libmp3lame", "-b:a", "64k", f"{out_dir}/{book}.mp3"], check=True)
    os.remove(full)
    print(f"DONE {book} {total / 60:.1f} min", flush=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
