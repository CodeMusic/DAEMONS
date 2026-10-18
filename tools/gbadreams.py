#!/usr/bin/env python3
"""The CHECKPOINT attendant's dreams, for a player who is stuck (T-347, the user, 2026-10-02).

    python3 tools/gbadreams.py            # report: every check, and whether the header is current
    python3 tools/gbadreams.py --write    # engineGba/src/data/attendant_dreams.h

After three heals with no main-path progress, the attendant offers a dream about the next step (src/daemons_dreams.c).
The STEPS are the AI playtester's own progress list -- engineAi/server/progress_steps.json -- so the attendant and the
playtester never disagree about what comes next; the WORDS are docs/attendant_dreams.json (DRAFT, two per step).

This tool holds the two together and refuses anything that would break the design:
  - every step in the harness's list has both dreams, or is in `_skip` with a reason (the GUIDE and the first
    UNDERSTANDING are: a hidden find and an arrived-at understanding are never pointed at);
  - every step's trigger maps to a flag the game sets (TRIGGERS below), so "done" means the same thing to both;
  - the FIRST dream names no place (every MAPSEC name and its first word is checked) -- it is pure image;
  - a box is one or two lines, and no line is wider than the 208px message box;
  - each dream fits gStringVar4 (1000 bytes), where the script shows it from.

T-412 (the user, 2026-10-18): her half of the NOTEBOOK's DREAM LOG. Each step also carries
  - LED: where it led, in her voice -- one box, checked as a dream's are -- written under her FIRST dream in the
    NOTEBOOK once the step is done, and said aloud once at the next heal (daemons_dreams.c, VAR_DREAM_LED);
  - TITLE (optional, the user's to choose, as YOUR DREAMS' were): her page's title under HER DREAMS -- capitals, at most
    TITLE_W, no number. Until a step has one, the title is the dream's first words after "I dreamt", as many whole
    words as fit TITLE_W, cut at a comma or full stop and not ending on a little word.
Each step is filed under FLAG_ATTENDANT_DREAM_<STEP> (flags.h) the first time she tells its FIRST dream; a step whose
flag flags.h does not define stops the run. The header's ATTENDANT_DREAMS_NOTEBOOK half is what notebook.c includes:
the pages' rows, and their titles and words by name.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
STEPS = os.path.join(ROOT, "engineAi", "server", "progress_steps.json")
WORDS = os.path.join(ROOT, "docs", "attendant_dreams.json")
OUT = os.path.join(GBA, "src", "data", "attendant_dreams.h")
WRITE = "--write" in sys.argv


def _font():
    """The message box's font: glyph widths from src/text.c, keyed through charmap.txt (as port_dialogue reads it --
    copied, not imported, because importing that tool runs it)."""
    body = re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\};',
                     open(os.path.join(GBA, "src/text.c"), encoding="utf-8").read(), re.S).group(1)
    widths = [int(x) for x in re.findall(r'\d+', body)]
    cm = {}
    for line in open(os.path.join(GBA, "charmap.txt"), encoding="utf-8"):
        line = line.split('@')[0].strip()
        if '=' not in line:
            continue
        k, v = (p.strip() for p in line.split('=', 1))
        if len(k) == 3 and k[0] == k[2] == "'":
            k = k[1]
        elif len(k) > 1 and k[0] == k[-1] == '"':
            k = k[1:-1]
        try:
            cm[k] = int(v, 16)
        except ValueError:
            pass
    return widths, cm


WIDTHS, CHARMAP = _font()


def textwidth(s):
    """A name token is measured as seven letters, the longest a player can type."""
    total = 0
    for tok in re.findall(r'\{[^}]*\}|.', s):
        if tok.startswith('{'):
            if tok in ("{PLAYER}", "{RIVAL}"):
                total += sum(WIDTHS[CHARMAP[c]] for c in "ABCDEFG")
            continue
        g = CHARMAP.get(tok)
        if g is not None and g < len(WIDTHS):
            total += WIDTHS[g]
    return total

#  The harness reads these off RAM (firered_bridge/player/snapshot.py); the game reads the same flags.
EVENTS = {
    "EVENT_GOT_STARTER": "FLAG_SYS_POKEMON_GET", "EVENT_GOT_POKEDEX": "FLAG_SYS_POKEDEX_GET",
    "EVENT_GOT_TEXTBOOK": "FLAG_SCHOOL_GOT_TEXTBOOK", "EVENT_GOT_DIPLOMA": "FLAG_GOT_DIPLOMA",
    "EVENT_SS_ANNE_LEFT": "FLAG_HIDE_SS_ANNE", "EVENT_GOT_REVEAL": "FLAG_GOT_REVEAL",
    "EVENT_BEAT_ROCKET_HIDEOUT_GIOVANNI": "FLAG_HIDE_HIDEOUT_GIOVANNI", "EVENT_GOT_POKE_FLUTE": "FLAG_GOT_POKE_FLUTE",
    "EVENT_GOT_HM03": "FLAG_GOT_HM03", "EVENT_BEAT_SILPH_CO_GIOVANNI": "FLAG_HIDE_SAFFRON_ROCKETS",
    "EVENT_GOT_GUIDE": "FLAG_GOT_GUIDE", "EVENT_UNDERSTANDING_FIRST": "FLAG_UNDERSTANDING_FIRST",
    "EVENT_BEAT_LANCE": "FLAG_DEFEATED_LANCE", "EVENT_BEAT_CHAMPION_RIVAL": "FLAG_DEFEATED_CHAMP",
}
BADGES = {"SLATE": 1, "SLOPE": 2, "SENSE": 3, "FIT": 4, "SKEW": 5, "FRAME": 6, "HEAT": 7, "TRUE": 8}
#  A map visit has no flag of its own in the harness; these are the flags the game sets on arriving (or, for the
#  MANSION's step, on taking the key the gym's door waits on).
VISITS = {"DOLDRUM_CITY": "FLAG_WORLD_MAP_CERULEAN_CITY", "HALFTONE_TOWN": "FLAG_WORLD_MAP_LAVENDER_TOWN",
          "QUICKSILVER_ISLAND_GYM": "FLAG_HIDE_POKEMON_MANSION_B1F_SECRET_KEY",
          "UMBRA_PLATEAU_CHECKPOINT_1_F": "FLAG_WORLD_MAP_INDIGO_PLATEAU_EXTERIOR"}
BOX_W, BUF = 208, 1000
TITLE_W = 130      # tools/gbadreamlog.py's: the NOTEBOOK's list keeps the width the other sections use
SMALL = {"A", "AN", "THE", "MY", "ITS", "INTO", "IN", "OF", "ON", "TO", "AND", "AT", "WITH", "WAS", "THAT", "HAD",
         "BEEN", "WHERE", "SO", "IT", "BEHIND", "UNDER", "LIKE", "FULL", "VERY"}
NUMBER_WORDS = {"ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE", "TEN"}   # a title never counts


def her_title(sid, d):
    """The step's own title (the user's, when chosen), or the FIRST dream's opening words after "I dreamt"."""
    t = d.get("title")
    if t:
        if t != t.upper() or textwidth(t) > TITLE_W or re.search(r"\d", t):
            sys.exit("gbadreams: %s's title %r must be capitals within %dpx, no number" % (sid, t, TITLE_W))
        return t
    #  (a number word is left out at the start and ends the title anywhere else: a title never counts)
    words = re.sub(r"^I dreamt (of )?", "", " ".join(l for b in d["first"] for l in b)).upper().split()
    taken = []
    for w in words:
        if w.rstrip(".,:;") in NUMBER_WORDS:
            if taken:
                break
            continue
        if textwidth(" ".join(taken + [w]).rstrip(".,:;")) > TITLE_W:
            break
        taken.append(w)
        if w[-1] in ".,:;":
            break
    taken[-1] = taken[-1].rstrip(".,:;")
    while len(taken) > 1 and taken[-1] in SMALL:
        taken.pop()
    return " ".join(taken)


def flag_for(step):
    t, trig = step["type"], step["trigger"]
    if t == "event":
        return EVENTS.get(trig)
    if t == "badge":
        return "FLAG_BADGE%02d_GET" % BADGES[trig] if trig in BADGES else None
    if t == "map_visit":
        return VISITS.get(trig)
    return None


def place_words():
    secs = json.load(open(os.path.join(GBA, "src/data/region_map/region_map_sections.json")))["map_sections"]
    words = set()
    for m in secs:
        n = (m.get("name") or "").strip()
        if not n or re.fullmatch(r"ROUTE \d+", n):
            continue
        words.add(n)
        first = n.split()[0]
        if len(first) > 3 and first not in ("THE", "ONE", "TWO", "SIX"):
            words.add(first)
    return words


def c_string(boxes):
    out = []
    for bi, box in enumerate(boxes):
        for li, line in enumerate(box):
            last = li == len(box) - 1
            out.append(line + (("\\p" if bi < len(boxes) - 1 else "") if last else "\\n"))
    return "".join(out)


def main():
    steps = json.load(open(STEPS))
    words = json.load(open(WORDS))
    skip, dreams = words.get("_skip", {}), words["steps"]
    flags_h = open(os.path.join(GBA, "include/constants/flags.h")).read()
    places = place_words()
    bad, rows = [], []
    for s in steps:
        sid = s["id"]
        if sid in skip:
            continue
        flag = flag_for(s)
        if not flag or not re.search(r"#define %s\b" % flag, flags_h):
            bad.append("%s: trigger %s maps to no flag the game defines (%s)" % (sid, s["trigger"], flag))
        d = dreams.get(sid)
        if not d or not d.get("first") or not d.get("second"):
            bad.append("%s: needs both dreams (or a reason in _skip)" % sid)
            continue
        for which in ("first", "second"):
            for box in d[which]:
                if not 1 <= len(box) <= 2:
                    bad.append("%s %s: a box of %d lines" % (sid, which, len(box)))
                for line in box:
                    if textwidth(line) > BOX_W:
                        bad.append("%s %s: %dpx > %d: %s" % (sid, which, textwidth(line), BOX_W, line))
            if len(c_string(d[which]).encode()) + 16 > BUF:
                bad.append("%s %s: too long for gStringVar4" % (sid, which))
        led = d.get("led")
        if not led or len(led) != 1 or not 1 <= len(led[0]) <= 2:
            bad.append("%s: needs LED, one box of one or two lines (T-412)" % sid)
        else:
            for line in led[0]:
                if textwidth(line) > BOX_W:
                    bad.append("%s led: %dpx > %d: %s" % (sid, textwidth(line), BOX_W, line))
        told = "FLAG_ATTENDANT_DREAM_" + sid.upper()
        if not re.search(r"#define %s\b" % told, flags_h):
            bad.append("%s: flags.h defines no %s (T-412: her dream, filed)" % (sid, told))
        said = " ".join(l for b in d["first"] for l in b)
        named = sorted(p for p in places if re.search(r"(?<![A-Z])%s(?![A-Z])" % re.escape(p), said))
        if named:
            bad.append("%s first: names a place (%s) -- the first dream is pure image" % (sid, ", ".join(named)))
        rows.append((sid, s["label"], flag, d, told, her_title(sid, d)))
    stray = sorted(set(dreams) - {s["id"] for s in steps})
    if stray:
        bad.append("dreams for steps the harness no longer has: %s" % ", ".join(stray))
    if bad:
        print("  refused:")
        for b in bad:
            print("   ", b)
        sys.exit(1)
    lines = ["//  GENERATED by tools/gbadreams.py from engineAi/server/progress_steps.json and docs/attendant_dreams.json.",
             "//  Do not edit; edit the JSON and run the tool. T-347 and T-412, DRAFT wording.", "",
             "#ifdef ATTENDANT_DREAMS_NOTEBOOK",
             "//  notebook.c's half (T-412): HER DREAMS' pages, in step order -- each filed the first time she tells its",
             "//  FIRST dream; ARG is its step, for where it led (DaemonsDream_Led).", ""]
    for sid, label, flag, d, told, title in rows:
        lines.append("extern const u8 gAttendantDreamTitle_%s[];" % sid)
        lines.append("extern const u8 gAttendantDreamFirst_%s[];" % sid)
    lines += ["", "#define NB_HER_DREAM_ENTRIES \\"]
    for i, (sid, label, flag, d, told, title) in enumerate(rows):
        lines.append("    { NB_DREAM_LOG, NB_KIND_HER_DREAM, %d, %s, 0, gAttendantDreamTitle_%s, gAttendantDreamFirst_%s }, \\"
                     % (i, told, sid, sid))
    lines += ["", "#else", "",
              "struct AttendantDream { u16 flag; u16 told; const u8 *first; const u8 *second; const u8 *led; };", ""]
    for sid, label, flag, d, told, title in rows:
        lines.append('const u8 gAttendantDreamTitle_%s[] = _("%s");' % (sid, title.replace('"', '\\"')))
        lines.append('const u8 gAttendantDreamFirst_%s[] = _("%s");' % (sid, c_string(d["first"])))
        lines.append('static const u8 sDream_%s_second[] = _("%s");' % (sid, c_string(d["second"])))
        lines.append('static const u8 sDream_%s_led[] = _("%s");' % (sid, c_string(d["led"])))
    lines += ["", "static const struct AttendantDream sAttendantDreams[] = {"]
    for sid, label, flag, d, told, title in rows:
        lines.append("    { %s, %s, gAttendantDreamFirst_%s, sDream_%s_second, sDream_%s_led },   // %s"
                     % (flag, told, sid, sid, sid, label))
    lines += ["};", "", "#endif // ATTENDANT_DREAMS_NOTEBOOK", ""]
    text = "\n".join(lines)
    for sid, label, flag, d, told, title in rows:
        print("  %-16s %-24s %s" % (sid, "%s (%dpx)" % (title, textwidth(title)),
                                    "  |  ".join("%s (%dpx)" % (l, textwidth(l)) for l in d["led"][0])))
    print("  %d steps dreamt, %d skipped (%s); every first dream names no place; every line fits %dpx"
          % (len(rows), len(skip), ", ".join(skip), BOX_W))
    if os.path.exists(OUT) and open(OUT).read() == text:
        print("  attendant_dreams.h is current")
        return
    if not WRITE:
        print("  report only; pass --write")
        return
    open(OUT, "w").write(text)
    print("  written %s" % os.path.relpath(OUT, ROOT))


if __name__ == "__main__":
    main()
