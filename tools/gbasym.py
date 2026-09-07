#!/usr/bin/env python3
"""Emit a pokefirered.sym for the AI harness, from OUR build rather than retail.

    python3 tools/gbasym.py [--write] [--out <path>]

WHY THIS EXISTS. Clad3815/gpt-play-pokemon-firered drives mGBA over a Lua
socket and reads the game out of RAM -- no screenshots anywhere, which is what
makes a small local model viable for it at all. It finds the game state by
NAME, through a pokefirered.sym shipped for the retail ROM, and its loader
honours FIRERED_SYM_PATH. So pointing it at our build is a file, not a fork.

AND OURS IS THE ONE THAT WILL BE RIGHT. Their .sym describes a ROM we did not
build. Ours is regenerated from the ELF every time, so it cannot drift: rename
a symbol, move a struct, add a move, and the table follows on the next build.

WHAT DID NOT SHIFT, CHECKED. CONSENSUS is APPENDED after MOVE_PSYCHO_BOOST
rather than inserted, and PERSPECTIVE is a renamed string on MOVE_TRANSFORM
rather than a new constant -- so move IDs are vanilla and the structure layouts
the harness reads are unchanged. What differs between the two ROMs is text,
which a RAM-reading agent barely touches.

THE FORMAT is what their loader parses: four whitespace-separated columns,

    ADDR TYPE SIZE NAME        02020000 g 00000002 gTrainerId

hex address, `g` or `l` for global or local, hex size, name. nm reports type as
a letter whose CASE carries the binding -- B is a global in .bss, b a local one
-- so the case is the only part of that letter this needs.
"""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GBA  = os.path.join(ROOT, "engineGba")
ELF  = os.path.join(GBA, "pokefirered.elf")
NM   = "arm-none-eabi-nm"
OUT  = os.path.join(ROOT, "ai", "pokefirered.sym")

#  A few the harness cannot work without. Emitting the table is cheap; proving
#  these are IN it is the part worth failing loudly on, because a missing
#  symbol shows up as an agent that reads zeroes and says nothing is wrong.
REQUIRED = ["gPlayerParty", "gSaveBlock1Ptr", "gSaveBlock2Ptr", "gMain",
            "gBattleMons", "gEnemyParty", "gObjectEvents", "gBattleTypeFlags"]


def symbols():
    if not os.path.isfile(ELF):
        sys.exit("no ELF at %s -- build first: make -C engineGba firered" % ELF)
    try:
        raw = subprocess.run([NM, "-S", "--defined-only", ELF],
                             capture_output=True, text=True, check=True).stdout
    except FileNotFoundError:
        sys.exit("%s not found. brew install arm-none-eabi-binutils" % NM)
    out = []
    for line in raw.splitlines():
        p = line.split()
        #  "addr size type name" when nm knows a size, "addr type name" when not
        if len(p) == 4:
            addr, size, kind, name = p
        elif len(p) == 3:
            addr, kind, name = p; size = "00000000"
        else:
            continue
        addr_i = int(addr, 16)
        #  ABSOLUTE SYMBOLS ARE NOT ADDRESSES. nm reports every `.equ` constant
        #  as type a/A at its literal value, so BLDCNT_EFFECT_NONE arrives as
        #  "address 0" -- 150k of them, outnumbering the real table three to
        #  one and able to shadow a real name on lookup. The harness resolves
        #  by name, so a constant called the same thing as a variable is a
        #  silently wrong read.
        if not name or name.startswith(".") or kind in "aA":
            continue
        if addr_i < 0x02000000:          # below EWRAM is not a mapped address
            continue
        out.append((int(addr, 16), "g" if kind.isupper() else "l",
                    int(size, 16), name))
    return out


def main():
    dst = OUT
    if "--out" in sys.argv:
        dst = os.path.abspath(sys.argv[sys.argv.index("--out") + 1])
    syms = symbols()
    names = {s[3] for s in syms}
    print("  %-28s %d symbols" % (os.path.basename(ELF), len(syms)))
    missing = [r for r in REQUIRED if r not in names]
    for r in REQUIRED:
        hit = next((s for s in syms if s[3] == r), None)
        print("    %-18s %s" % (r, ("%08x" % hit[0]) if hit else "MISSING"))
    if missing:
        sys.exit("  !! %d required symbol(s) missing -- the agent would read "
                 "zeroes and report nothing wrong" % len(missing))
    if "--write" not in sys.argv:
        print("\n  would write %s\n  (report only; pass --write)" % dst)
        return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "w") as f:
        for addr, kind, size, name in sorted(syms):
            f.write("%08x %s %08x %s\n" % (addr, kind, size, name))
    print("\n  written %s" % dst)


if __name__ == "__main__":
    main()
