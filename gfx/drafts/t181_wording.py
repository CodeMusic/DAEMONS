#!/usr/bin/env python3
"""T-181's fourteen: shorter WORDING for the move descriptions no wrap can fit (vision.md 9.4a).

    python3 gfx/drafts/t181_wording.py            # report: every line, measured against the pane
    python3 gfx/drafts/t181_wording.py --write     # write them into src/move_descriptions.c

WHY THIS FILE EXISTS. The summary screen prints a move's description into POKESUM_WIN_TRAINER_MEMO,
which on the moves page is fifteen tiles wide with the text inset seven pixels: a 113px pane, four
lines. Vanilla's widest line in that file is 108px, which is what `port_vocab`'s "demonstrated by
vanilla" ceiling was reading. T-138 wrote lines up to 170px. `port_vocab --write` reflowed 22 of
them, and seventeen lines in these fourteen moves stayed over, because no four-line wrap of that
WORDING fits -- confirmed on the screen, where GOTO reads "a CHECKPOINT alread" with the y cut off
at the window edge.

So the wrap was never the fault. These are shorter sentences saying the same thing, wrapped here at
the real pane rather than typed with line breaks by hand.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
C = os.path.join(ROOT, "engineGba/src/move_descriptions.c")
PANE, MAXLINES = 113, 4
WRITE = "--write" in sys.argv

#  port_vocab.py runs its report at import, so its font table is lifted by executing the file down to
#  the marker instead -- one glyph-width table in the repository, not two.
_src = open(os.path.join(ROOT, "tools/port_vocab.py"), encoding="utf-8").read()
_ns = {"__name__": "port_vocab_font", "__file__": os.path.join(ROOT, "tools/port_vocab.py")}
exec(compile(_src.split("# ------------------------------------------------------- names, derived")[0],
             "port_vocab.py", "exec"), _ns)
textwidth = _ns["textwidth"]

WORDING = {
    "Teleport":    "DETACHES from a wild DAEMON. Also warps to the last CHECKPOINT.",
    "Refresh":     "Clears a leak, an overheat or a throttle from the user.",
    #  FATIGUE landed at exactly 113 of 113 as "May lower their DEFENSE." -- legal and no margin at
    #  all. Making the stat the subject spends one word and buys eight pixels back.
    "IronTail":    "Load applied over and over until the armour gives. Their DEFENSE may drop.",
    "FireBlast":   "Hits them with an intense flame. It may leave them overheating.",
    "LovelyKiss":  "A forced kiss, with a face odd enough to induce suspension.",
    "Attract":     "Binds their attention to the user, which may leave them unable to act.",
    "Uproar":      "An uproar that blocks suspension for two to five turns.",
    #  THEM, not "the foe" (the user's call, and the better one). "the foe" is 40px and "them" is
    #  23px, so the pronoun pays for seventeen pixels a use -- and it is what this game already
    #  believes: a foe is a thing and a them is a someone. Three of these needed no shortening at
    #  all once it went in. FATIGUE and PAIR are T-138's own sentences, unchanged but for the
    #  pronoun; MISLEAD keeps "Tells them what they want to hear" whole and recasts only its tail,
    #  because the original tail kept the pronoun of a thing ("leaves IT") beside a they. The tail
    #  says THRASHING and not "they THRASH": 1.6 renamed the STATE to THRASHING, and the bare verb
    #  is a different thing entirely -- MOVE_THRASH is BUSY WAIT. check_lexicon caught it.
    "Flatter":     "Tells them what they want to hear. Their SP. ATK rises, then THRASHING.",
    "CosmicPower": "Widens the frame until little matters. Raises DEFENSE and SP. DEF.",
    "RapidSpin":   "Frees the user from LATCH, ENCLOSE, SEED and TRIPWIRE as it hits.",
    "Fly":         "Transfers control to a CHECKPOINT already reached. Attacks next turn.",
    "Dig":         "Goes under, and is up again next turn. Outside, it digs a cave.",
    "FocusEnergy": "Reads ahead, so what comes next lands better. Raises critical hits.",
    "FirePunch":   "Punches them with a fiery fist. It may leave them overheating.",
}


def wrap(s):
    out, cur = [], ""
    for w in s.split():
        trial = (cur + " " + w).strip()
        if cur and textwidth(trial) > PANE:
            out.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        out.append(cur)
    return out


def main():
    src = open(C, encoding="utf-8").read()
    over = 0
    for key, prose in WORDING.items():
        lines = wrap(prose)
        widest = max(textwidth(l) for l in lines)
        if widest > PANE or len(lines) > MAXLINES:
            over += 1
        print("  %-12s %3dpx %d lines  %s" % (key, widest, len(lines), " / ".join(lines)))
        pat = re.compile(r'(const u8 gMoveDescription_%s\[\] = _\()(.*?)(\);)' % key, re.S)
        if not pat.search(src):
            raise SystemExit("no description for %s" % key)
        src = pat.sub(lambda m: m.group(1) + '"' + "\\n".join(lines) + '"' + m.group(3), src, count=1)
    print("\n  %d of %d over the %dpx pane" % (over, len(WORDING), PANE))
    if WRITE:
        open(C, "w", encoding="utf-8").write(src)
        print("  written into src/move_descriptions.c")


if __name__ == "__main__":
    main()
