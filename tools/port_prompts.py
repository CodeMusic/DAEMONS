#!/usr/bin/env python3
"""Teach the AI harness's prompts the vocabulary the game actually uses.

    python3 tools/port_prompts.py [--write]

WHY THIS IS NOT COSMETIC. The agent is briefed in 2,757 lines of prompt that
say POKEMON, trainer, gym, badge and faint. The ROM says DAEMON, USER,
BENCHMARK, MARK and HALTED. So the model is told to look for things the screen
never shows, and shown things its brief never mentions -- and it reads the
screen through that brief. A dashboard saying the wrong word is cosmetic; a
system prompt saying it is a comprehension bug.

IT REUSES port_vocab's TABLE rather than restating it. That module already
carries the 68 renames, learned or declared once; a second copy here would be
a second thing to keep in sync, and the first divergence would be silent.

WHAT IS DELIBERATELY LEFT ALONE, checked against the ROM rather than assumed:
POTION and HP are unchanged in this build, so the prompts' 9 potions and 16 HPs
are already correct. Renaming them would have been the confident error.
"""
import contextlib, io, importlib.util, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMPTS = os.path.join(ROOT, "engineAi", "server", "prompts")
WRITE = "--write" in sys.argv


def vocab():
    """port_vocab's table, loaded without running its report."""
    spec = importlib.util.spec_from_file_location(
        "port_vocab", os.path.join(ROOT, "tools", "port_vocab.py"))
    m = importlib.util.module_from_spec(spec)
    argv, sys.argv = sys.argv, ["port_vocab"]
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            try:
                spec.loader.exec_module(m)
            except SystemExit:
                pass
    finally:
        sys.argv = argv
    return dict(m.VOCAB)


#  Prompt prose is not game text, so a few things differ from port_vocab.
#  Longest first: "gym leader" before "gym", or the leader becomes a BENCHMARK
#  leader.
EXTRA = [
    ("gym leader", "BENCHMARK leader"), ("Gym Leader", "BENCHMARK leader"),
    ("gym leaders", "BENCHMARK leaders"),
    ("Poke Ball", "USERBOX"), ("Poké Ball", "USERBOX"),
    ("pokeball", "USERBOX"), ("Pokeball", "USERBOX"), ("poke ball", "USERBOX"),
    ("Pokemon", "DAEMON"), ("pokemon", "DAEMON"), ("POKEMON", "DAEMON"),
    ("Pokémon", "DAEMON"), ("pokémon", "DAEMON"), ("POKéMON", "DAEMON"),
    ("Pokedex", "INDEX"), ("pokedex", "INDEX"), ("POKEDEX", "INDEX"),
    ("gym", "BENCHMARK"), ("Gym", "BENCHMARK"), ("GYM", "BENCHMARK"),
    ("wild", "UNBOUND"), ("Wild", "UNBOUND"),
    ("FIGHT", "INVOKE"),
    #  Capitalised at a sentence start, which port_vocab's game-text table has
    #  no reason to carry -- prose does, and three survived the first pass.
    ("Trainer", "USER"), ("Trainers", "USERS"),
    ("Badge", "MARK"), ("Badges", "MARKS"),
    ("Fainted", "HALTED"), ("Faint", "HALT"), ("Fainting", "HALTING"),
    ("Catch", "Bind"), ("Caught", "Bound"), ("caught", "bound"),
    #  the states, from 1.6
    ("poisoned", "LEAKING"), ("asleep", "SUSPENDED"),
    ("paralyzed", "THROTTLED"), ("paralysed", "THROTTLED"),
    ("burned", "OVERHEATED"), ("frozen", "HUNG"), ("confused", "THRASHING"),
    #  2.6 settled that moves are ROUTINES
    ("moves", "ROUTINES"), ("move", "ROUTINE"),
]

#  Left alone on purpose, verified present and unrenamed in the ROM.
KEEP = ("POTION", "HP")

#  Words whose replacement would break the harness rather than help it: these
#  name the emulator's own controls and the bridge's JSON keys, not the world.
PROTECT = re.compile(
    r"\b(move_?to|moveTo|movement|moves?_?list|A|B|START|SELECT|UP|DOWN|LEFT|RIGHT)\b")


def port(text, table):
    #  Protect the API surface first: the prompts describe button names and
    #  JSON fields as well as the world, and "move" is in both.
    holds = {}
    def hold(m):
        k = "\x00%d\x00" % len(holds)
        holds[k] = m.group(0)
        return k
    text = PROTECT.sub(hold, text)
    n = 0
    for old, new in table:
        pat = re.compile(r"\b%s\b" % re.escape(old))
        text, k = pat.subn(new, text)
        n += k
    for k, v in holds.items():
        text = text.replace(k, v)
    return text, n


def main():
    if not os.path.isdir(PROMPTS):
        sys.exit("no prompts at %s -- run ./setup.sh" % PROMPTS)
    V = vocab()
    #  port_vocab entries that make sense in prose, then the prompt-specific
    #  ones. Longest key first so "gym leader" beats "gym".
    table = [(k, v) for k, v in V.items()
             if k.upper() in ("TRAINER", "TRAINERS", "BADGE", "BADGES",
                              "POKéDEX", "FAINT", "FAINTED", "CATCH",
                              "CATCHES", "CATCHING")]
    table += EXTRA
    table.sort(key=lambda kv: -len(kv[0]))

    total, out = 0, []
    for f in sorted(os.listdir(PROMPTS)):
        if not f.endswith(".txt"):
            continue
        p = os.path.join(PROMPTS, f)
        t = open(p, encoding="utf-8").read()
        new, n = port(t, table)
        print("  %-24s %4d substitutions" % (f, n))
        total += n
        if n:
            out.append((p, new))

    left = []
    for p, new in out:
        for m in re.finditer(r"(?i)\b(pok[eé]mon|trainer|gym|badge|faint\w*|pok[eé]dex)\b", new):
            left.append("%s: %s" % (os.path.basename(p), m.group(0)))
    if left:
        print("  !! %d vanilla term(s) survived: %s" % (len(left), ", ".join(sorted(set(left))[:6])))
    else:
        print("  no vanilla creature vocabulary left")
    print("  kept on purpose (unrenamed in the ROM): %s" % ", ".join(KEEP))

    if not WRITE:
        print("\n  (report only; pass --write)")
        return
    for p, new in out:
        open(p, "w", encoding="utf-8").write(new)
    print("\n  written %d file(s)" % len(out))


if __name__ == "__main__":
    main()
