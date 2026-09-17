#!/usr/bin/env python3
"""A batch's contact sheet (T-131): per species, both drafts, then as the game will draw it.

    python3 tools/contactsheet.py DIR "RATTATA nibble 3" "PIDGEY packet 3" ...   (vanilla id, file stem, met level)

DIR holds <stem>_front.png / _back.png drafts and clean/<stem>_*.png. Columns: draft front, draft back, then the
cleaned front with the Index's blank streaks, the front and back with the four moves it knows at that level --
coloured by gbasprite.py's own place_rich and streaks.h's own table, so the sheet is the build, not a guess --
and the front at 2x. Writes DIR/sheet.png.
"""

import ast, re, sys, glob, os
sys.path.insert(0, "tools")
from PIL import Image, ImageDraw
tree = ast.parse(open("tools/gbasprite.py").read())
keep = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.Assign))]
ns = {"__file__": "tools/gbasprite.py"}; exec(compile(ast.Module(body=keep, type_ignores=[]), "gbasprite", "exec"), ns)
T = ns["TYPE_COLOR"]; E = "engineGba/src/data/"
NAMES = {"NORMAL":"CONTENT","FIGHTING":"LOGIC","FLYING":"VECTOR","POISON":"CORRUPT","GROUND":"STRATUM","ROCK":"LEGACY","BUG":"SWARM",
         "GHOST":"LATENT","STEEL":"HARDENED","FIRE":"ENTROPY","WATER":"FLOW","GRASS":"GROWTH","ELECTRIC":"SIGNAL","PSYCHIC":"CONTEXT",
         "ICE":"FROZEN","DRAGON":"EMERGENT","DARK":"OPAQUE"}
h = open(E + "pokemon/streaks.h").read()
table = {b: {m: tuple(int(v)*255//31 for v in c) for m, *c in re.findall(r"\[TYPE_(\w+)\] = RGB\((\d+), (\d+), (\d+)\)", row)}
         for b, row in re.findall(r"\[TYPE_(\w+)\] = \{(.*?)\},\n", h)}
info = open(E + "pokemon/species_info.h").read()
moves_h = open(E + "battle_moves.h").read()
learn = open(E + "pokemon/level_up_learnsets.h").read()
move_names = open(E + "text/move_names.h").read()
def types(sp):
    m = re.search(r"\[SPECIES_%s\] =.*?\.types = \{TYPE_(\w+), TYPE_(\w+)\}" % sp, info, re.S); return m.group(1), m.group(2)
def moves_at(sp, lvl):
    name = "".join(w.capitalize() for w in sp.split("_"))
    body = re.search(r"s%sLevelUpLearnset\[\] = \{(.*?)\};" % name, learn, re.S).group(1)
    got = []
    for l, mv in re.findall(r"LEVEL_UP_MOVE\(\s*(\d+), (MOVE_\w+)\)", body):
        if int(l) <= lvl and mv not in got: got.append(mv)
    return got[-4:]
def mtype(mv): return re.search(r"\[%s\] =.*?\.type = TYPE_(\w+)" % mv, moves_h, re.S).group(1)
def mname(mv): return re.search(r"\[%s\]\s*= _\(\"(.*?)\"\)" % mv, move_names).group(1)
R = sys.argv[1]; rows = [l.split() for l in sys.argv[2:]]
def render(gp, body, mts):
    grid, pal = gp; pal = list(pal)
    for k in range(4):
        pal[11+k] = ns["STREAK_BLANK"] if mts is None else (table[body][mts[k]] if k < len(mts) else pal[3])
    im = Image.new("RGB", (64, 64)); im.putdata([pal[i] for r in grid for i in r]); return im.resize((192, 192), Image.NEAREST)
W, H = 6*200+10, len(rows)*232+10
out = Image.new("RGB", (W, H), (36, 36, 42)); d = ImageDraw.Draw(out)
for i, (sp, ours, lvl) in enumerate(rows):
    y = 10 + i*232; t1, t2 = types(sp); mv = moves_at(sp, int(lvl)); mts = [mtype(m) for m in mv]
    front = ns["place_rich"](f"{R}/clean/{ours}_front.png", T[t1])
    back = ns["place_rich"](f"{R}/clean/{ours}_back.png", T[t1], shared=front[1])
    label = f"{ours.upper()}  {NAMES[t1]}" + ("" if t2 == t1 else "/" + NAMES[t2]) + f"   Lv{lvl}: " + ", ".join(f"{mname(m)} ({NAMES.get(t,t)})" for m, t in zip(mv, mts))
    d.text((12, y), label, fill=(236, 236, 236))
    for j, f in enumerate([f"{ours}_front.png", f"{ours}_back.png"]):
        out.paste(Image.open(f"{R}/{f}").convert("RGB").resize((192, 192)), (10 + j*200, y + 18))
    out.paste(render(front, t1, None), (10 + 2*200, y + 18))
    out.paste(render(front, t1, mts), (10 + 3*200, y + 18))
    out.paste(render(back, t1, mts), (10 + 4*200, y + 18))
    im = Image.new("RGB", (64, 64)); g, p = front
    im.putdata([p[k] if k < 11 else table[t1][mts[k-11]] if k-11 < len(mts) else p[3] for r in g for k in r])
    out.paste(im.resize((128,128), Image.NEAREST), (10 + 5*200, y + 18))
    d.text((10+5*200, y+150), "front, 2x", fill=(150,150,150))
out.save(f"{R}/sheet.png"); print("->", f"{R}/sheet.png")
