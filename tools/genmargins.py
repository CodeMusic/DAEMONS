#!/usr/bin/env python3
"""OPUS's margin lines, wrapped to the Index entry's own pane (T-197; vision.md 4.2).

    python3 tools/genmargins.py            # report every line, measured
    python3 tools/genmargins.py --write     # write src/data/opus_margins.h

WHAT A MARGIN LINE IS. The entry measures the daemon -- height, weight, type, stats, and the thin sentence
4.2 is about. The margin notices the PLAYER, and never says so. It is never a measurement, never advice,
never a hint, and it only makes sense read against the entry above it.

TWO LINES, because what OPUS noticed depends on what you did. A daemon you levelled gets one line; a daemon
you bound and put away gets another. The second is not a scold -- it is the same quiet noticing, aimed at the
thing you did not do.

NOT EVERY ENTRY HAS ONE, and that is the point: a reader annotates where they had a thought.

THE PANE is the entry's own, demonstrated rather than declared -- 234px and four lines, which is the widest
line and the most lines the 386 entries use.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA = os.path.join(ROOT, "engineGba")
OUT = os.path.join(GBA, "src/data/opus_margins.h")
PANE, MAXLINES = 234, 4
WRITE = "--write" in sys.argv

_src = open(os.path.join(ROOT, "tools/port_vocab.py"), encoding="utf-8").read()
_ns = {"__name__": "port_vocab_font", "__file__": os.path.join(ROOT, "tools/port_vocab.py")}
exec(compile(_src.split("# ------------------------------------------------------- names, derived")[0],
             "port_vocab.py", "exec"), _ns)
textwidth = _ns["textwidth"]

#  (species constant, our name, carried, neglected)
MARGINS = [
    ("SPECIES_BULBASAUR", "ROVERCUB",
     "It remembers the way back to the first town. You have not gone that way in some time.",
     "It is not being carried past anything."),
    ("SPECIES_CHARMANDER", "LABEL",
     "It has met you now. It has not changed the answer.",
     "It is still holding the one example. Nobody has shown it a second."),
    ("SPECIES_SQUIRTLE", "CLUSTER",
     "You have not checked the guess either.",
     "The guess has not changed. Nothing has been near it."),
    ("SPECIES_RATTATA", "NIBBLE",
     "You have met a great many. This is the one you kept.",
     "You kept this one. You have not filed it with anything."),
    ("SPECIES_PIDGEY", "PACKET",
     "It still does not ask. You have stopped noticing that.",
     "It has not been sent anywhere. It is still carrying it."),
    ("SPECIES_ABRA", "HUNCH",
     "You have started trusting it. There is still no working.",
     "Asleep. Nothing has needed an answer from it."),
    ("SPECIES_MAGNEMITE", "SENTINEL",
     "It has watched more of your fights than it has been in.",
     "It is still not looking away. There is nothing in there to watch."),
    ("SPECIES_DITTO", "MOCK",
     "You have seen it be other daemons. You have never seen it.",
     "It has nothing to look at. You do not know what it is like then."),
    ("SPECIES_PORYGON", "SUBSTRATE",
     "You carry it differently. You have not said why.",
     "Where it is has not changed in a long time."),
    ("SPECIES_GASTLY", "DANGLING",
     "It has been out in front of you more than most. It is still mostly not there.",
     "It does not have to be here either."),
    ("SPECIES_EEVEE", "MUSAI",
     "It has been shown something now.",
     "It is still waiting to be shown anything."),
    #  The best of these answer the entry's LAST SENTENCE, which is where an entry states the thing it is
    #  sure of. HEAP has never been asked to give one back; STUB says nobody came back for it. A margin that
    #  contradicts the entry above it is the strongest form of this: the record was right when it was written.
    ("SPECIES_GEODUDE", "HEAP",
     "It has been asked now. It gave one back.",
     "You put it down and left it. It is holding that too."),
    ("SPECIES_SPEAROW", "PING",
     "You have answered every time. It still asks.",
     "It is still asking. Nothing has answered in a long time."),
    ("SPECIES_ZUBAT", "ECHO",
     "It has built every room you have walked it through. You have not checked one.",
     "Nothing has come back. It has not stopped calling."),
    ("SPECIES_CATERPIE", "CRAWLER",
     "It has not finished. You have gone a long way with it.",
     "It stopped when you stopped. It had not finished."),
    ("SPECIES_WEEDLE", "SCRAPER",
     "Nobody has asked you for it back either.",
     "It took nothing. Nobody minded."),
    ("SPECIES_PIKACHU", "SPIKE",
     "You were counting.",
     "It has not fired. Nothing was counting anyway."),
    ("SPECIES_NIDORAN_F", "FORK",
     "You have one of them. You do not know which.",
     "It has not split. There is only the one, and it still cannot tell."),
    ("SPECIES_MANKEY", "PREEMPT",
     "It has gone first every time. You have stopped choosing.",
     "Nothing has been interrupted. It has not been first in a long time."),
    ("SPECIES_MACHOP", "PROOF",
     "It has not skipped one yet. You have.",
     "It is still on the first thing."),
    ("SPECIES_MAGIKARP", "STUB",
     "Somebody came back for it.",
     "You did not come back for it either."),
    ("SPECIES_PSYDUCK", "FAULT",
     "It has halted you a great many times. You waited every time.",
     "It is still waiting. So is whatever needed it."),
    ("SPECIES_ODDISH", "SPRAWL",
     "It has spread as far as you have walked.",
     "It has not spread. It is only buried."),
    ("SPECIES_BELLSPROUT", "SNARE",
     "It has closed on things for you. It is open again now.",
     "Still open. Nothing has entered."),
    ("SPECIES_JIGGLYPUFF", "SUSPEND",
     "You have used it to stop things. None of them ended.",
     "It has stopped, and nothing is happening to it."),
    ("SPECIES_MEOWTH", "COOKIE",
     "You set it down and picked it up again. It is the same one.",
     "Set down. Not picked up again."),
    ("SPECIES_DIGLETT", "TAPPOINT",
     "It has read everything you walked past. You did not.",
     "Nothing goes past in there."),
    #  The middle of the game. CANARY's is the one to read against 4.2: the daemon changes faster than
    #  anything measuring it, and the thing measuring it is the Index.
    ("SPECIES_EKANS", "WORM",
     "It has been in more places than you have looked.",
     "It has not stopped. You simply stopped looking."),
    ("SPECIES_SANDSHREW", "SECTOR",
     "You have got things back from it. You never checked what else was in there.",
     "Everything in it can still be got back. Nobody has asked."),
    ("SPECIES_VULPIX", "FLICKER",
     "Still neither. You have stopped checking which.",
     "Still not a fault. Still not looked at."),
    ("SPECIES_GROWLITHE", "SENTRY",
     "It has raised the alarm every time. You answered most of them.",
     "It is still watching. Nobody is listening for the alarm."),
    ("SPECIES_POLIWAG", "LOOP",
     "You have not told it when to stop either.",
     "Still going round. Nobody has come back to it."),
    ("SPECIES_TENTACOOL", "DRIFTNET",
     "It has caught a great deal. None of it was aimed at.",
     "There is no current in there."),
    ("SPECIES_SLOWPOKE", "LATENCY",
     "You have waited for it. It was right every time.",
     "The answer is ready. Nothing has asked the question."),
    ("SPECIES_GRIMER", "DEADLETTER",
     "You decided on somewhere. It is still keeping all of it.",
     "Kept. Somewhere nobody decided on."),
    ("SPECIES_SHELLDER", "CAPSULE",
     "You have stopped asking it to open.",
     "Still closed. Nobody has asked in a long time."),
    ("SPECIES_ONIX", "BACKBONE",
     "A great deal is built on it now.",
     "Nothing has been built on it."),
    ("SPECIES_KRABBY", "ACQUIRE",
     "It has led with that one every time.",
     "Nothing in there to lead with."),
    ("SPECIES_VOLTORB", "FUSE",
     "It has had its moment. You were there.",
     "Its moment has not come. It is still waiting to fail."),
    ("SPECIES_CUBONE", "ARTEFACT",
     "You have called it that name a great many times.",
     "Nobody has called it anything."),
    ("SPECIES_KOFFING", "EXHAUST",
     "It is still leaking. It is still up.",
     "Still leaking, into a box, and still up."),
    ("SPECIES_HORSEA", "BOTTLENECK",
     "Everything you sent through it came out slower.",
     "Nothing has passed through it."),
    ("SPECIES_GOLDEEN", "SPAWN",
     "It has started nothing yet. It is still swimming against it.",
     "Still against the current, in a box with no current."),
    ("SPECIES_STARYU", "BEACON",
     "It has not missed an interval. You have not counted one.",
     "Still emitting, at the same interval, to nobody."),
    ("SPECIES_SCYTHER", "REAPER",
     "You have seen the cut later, every time.",
     "Nothing it cut has shown up yet."),
    ("SPECIES_LAPRAS", "FERRY",
     "You asked. It has never mentioned that it could have gone alone.",
     "It is still waiting to be asked."),
    ("SPECIES_SNORLAX", "DEADLOCK",
     "Something outside came.",
     "You are outside. You did not come."),
    ("SPECIES_DRATINI", "CANARY",
     "It has changed a great deal. The Index says what it always said.",
     "Changing in there, faster than anything measuring it."),
    ("SPECIES_TOGEPI", "TRUST",
     "It came out facing you.",
     "It is still facing whoever was holding it."),
    ("SPECIES_MARILL", "MOOD",
     "It has been at every level you have been at.",
     "The water in there does not move."),
    ("SPECIES_WOOPER", "APATHY",
     "Things happened. It was told. It stayed.",
     "Nothing has been reported to it."),
    ("SPECIES_MURKROW", "OMEN",
     "It has arrived before a great many things. You stopped asking too.",
     "Nothing has arrived. Neither has it."),
    ("SPECIES_MISDREAVUS", "DREAD",
     "You expected it every time. It has eaten well.",
     "Nobody is expecting it. It is not eating."),
]


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
    over = 0
    body = ['//  Generated by tools/genmargins.py -- edit the tool, not this file (T-197).',
            '//',
            '//  OPUS writes one line under an entry. The entry measures the daemon; the margin notices the',
            '//  PLAYER, and never says so. Two lines per daemon, because what there was to notice depends on',
            '//  whether you carried it or bound it and put it away. Not every entry has one, and that is the',
            '//  point: a reader annotates where they had a thought.',
            '',
            'struct OpusMargin',
            '{',
            '    u16 species;',
            '    const u8 *carried;',
            '    const u8 *neglected;',
            '};',
            '']
    for sp, name, carried, neglected in MARGINS:
        for kind, text in (("Carried", carried), ("Neglected", neglected)):
            lines = wrap(text)
            widest = max(textwidth(l) for l in lines)
            bad = widest > PANE or len(lines) > MAXLINES
            over += bad
            print("  %-10s %-9s %3dpx %d lines%s  %s"
                  % (name, kind.lower(), widest, len(lines), " !!" if bad else "  ", " / ".join(lines)))
            body.append('static const u8 sOpusMargin_%s_%s[] = _("%s");' % (name.title(), kind, "\\n".join(lines)))
        body.append('')
    body.append('static const struct OpusMargin sOpusMargins[] = {')
    for sp, name, _c, _n in MARGINS:
        body.append('    { %-22s sOpusMargin_%s_Carried, sOpusMargin_%s_Neglected },'
                    % (sp + ",", name.title(), name.title()))
    body += ['};', '']
    print("\n  %d margin(s) for %d daemons; %d over the %dpx pane" % (2 * len(MARGINS), len(MARGINS), over, PANE))
    if WRITE:
        open(OUT, "w", encoding="utf-8").write("\n".join(body))
        print("  written %s" % os.path.relpath(OUT, ROOT))


if __name__ == "__main__":
    main()
