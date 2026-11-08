"""T-532 concept drafts (2026-11-08): the MUSAI branch's four seasons -- 6 daemons x 4 seasons = 24 fronts. DRAFT.

    seasons.py gen     [NAME ...]   draw on the sprite server through tools/spriteforge.py (arm C: klein4b + pixel LoRA)
    seasons.py reduce               cleandraft -> fold -> the type ramp (gbasprite.place_rich) -> 64x64, 16 colours
    seasons.py sheet                the concept sheet: 6 rows of daemons x 4 columns of seasons (sheets/)

The arm C recipe (gfx/drafts/t452/scripts/armc.py): spriteforge.run, model klein4b, the Limbicnation pixel-art LoRA at
1.0, 512x512, each draft's JSON recording the model, LoRA, reference, seed and prompt. Every draw takes the daemon's
APPROVED front from the ROM (8x on white) as its reference, so each season is the same creature, changed. Two seeds a
concept (5321/5322). Nothing here writes into the game; backs and icons wait for the user's pick.

THE FABLE RULE (docs/musai-seasons-draft.md): the vehicles are part of the body, never ridden -- runners and a
windscreen crest; knobby wheels and a roll-bar frame; pontoon floats and a canopy; model-plane wings and a propeller.
A daemon's HOME season (MASKMUSAI winter, SEEKMUSAI autumn, CAREMUSAI summer, LENSMUSAI spring) is its fullest form;
the other three carry a smaller piece of the same body. MUSAI wears the season itself; CODEMUSAI, the dialect, wears
a small piece of each sibling's body in that sibling's season.
"""
import json, os, sys, subprocess, time
import numpy as np
from PIL import Image, ImageDraw, ImageFont
R = "/Users/christopherhicks/Projects/DAEMONS"
sys.path.insert(0, R + "/tools"); sys.path.insert(0, R + "/gfx/drafts/t452/scripts")
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = R + "/engineGba/graphics/pokemon/"
PY = os.path.expanduser("~/.pyenv/versions/3.12.2/bin/python3")
LORA = [["klein4b_pixelart_limbicnation.safetensors", 1.0]]
SEEDS = (5321, 5322)
SEASONS = ("winter", "spring", "summer", "autumn")

#  name: (ROM slot, type constant, type word, home season or None, identity kept from the ROM front)
DAEMONS = {
    "musai":     ("eevee",    "NORMAL",   "CONTENT", None,
                  "a little white astronaut robot, a big round white helmet with a dark visor face, two glowing eyes, two thin antennae"),
    "codemusai": ("flareon",  "FIGHTING", "LOGIC",   None,
                  "a little grey round robot, a big round helmet with one narrow dark visor slit straight across it, two red-tipped antennae"),
    "seekmusai": ("jolteon",  "FLYING",   "VECTOR",  "autumn",
                  "a little white astronaut robot, a round helmet with a dark visor and two glowing eyes, two wide flat fins sticking out sideways from its helmet"),
    "caremusai": ("vaporeon", "PSYCHIC",  "CONTEXT", "summer",
                  "a little white astronaut robot, big round padded headphones over its helmet, a dark visor with two soft eyes, one curly antenna"),
    "lensmusai": ("espeon",   "PSYCHIC",  "CONTEXT", "spring",
                  "a little white robot whose whole face is one big round dark camera lens, one small antenna on the side of its head"),
    "maskmusai": ("umbreon",  "DARK",     "OPAQUE",  "winter",
                  "a lanky little grey robot, a smooth light grey mask plate over its face with two narrow dark eye slits, round headphones, its outline closed all round"),
}

#  the season, woven into each body (no rider, no vehicle beside it: the machine IS the daemon)
MOTIF = {
    "musai": {
        "winter": "a little cap of snow on its helmet, a short knitted scarf, frost on its antennae",
        "spring": "a small green sprout growing from the top of its helmet, tiny pink blossoms on its antennae",
        "summer": "a small sun-visor brim on its helmet, a tiny yellow sun charm on one antenna, a warm glow",
        "autumn": "a few orange fallen leaves stuck to its helmet, a little acorn on one antenna",
    },
    "codemusai": {   # the dialect: a small piece of each sibling's body, in that sibling's season, and its glyph lights
        "winter": "two small ski runners for feet and a little clear windscreen crest on its helmet, frost on its antennae, a row of small square glyph lights on its chest",
        "spring": "two small model-aeroplane wings on its back and a tiny propeller on one antenna, a row of small square glyph lights on its chest",
        "summer": "two small boat floats for feet and a little striped canopy over its helmet, a row of small square glyph lights on its chest",
        "autumn": "two small knobby wheels at its sides and a little roll-bar frame arching over its helmet, a row of small square glyph lights on its chest",
    },
    "seekmusai": {   # autumn: the side-by-side, ranging all around
        "autumn": "its body built as a rugged little off-road buggy, four big knobby tyres for legs, a roll-bar cage frame arching over its helmet, two round headlight eyes, mud splashes, golden yellow autumn leaves caught in its fins",
        "winter": "two chunky knobby wheels wrapped in snow chains, a small roll-bar frame over its helmet with snow on top",
        "spring": "two muddy knobby wheels, a small roll-bar frame over its helmet with a green sprout tucked in it",
        "summer": "two dusty knobby wheels, a small roll-bar frame over its helmet with a little sunshade on top",
    },
    "caremusai": {   # summer: the pontoon boat
        "summer": "its lower body two long silver pontoon floats side by side, a striped canopy top over its helmet like a boat's sunshade, a little railing round its middle, water splashing at the floats, warm sun",
        "winter": "its two pontoon floats frozen into a small block of ice, its canopy folded down flat, snow on its headphones",
        "spring": "two short pontoon floats under it, a small canopy over its helmet, a few rain drops",
        "autumn": "two short pontoon floats under it with fallen leaves on them, a faded canopy over its helmet",
    },
    "lensmusai": {   # spring: the model planes
        "spring": "its body built as a little model aeroplane, two long balsa-wood wings spread from its back, a propeller on its chest below the lens, a tail fin, pale yellow blossoms drifting",
        "summer": "two small model-aeroplane wings on its back, a little propeller on its chest, a bright sun glint on its lens",
        "autumn": "two small model-aeroplane wings on its back with orange leaves caught on them, a little propeller on its chest",
        "winter": "two small model-aeroplane wings on its back, little skis under its feet, frost on its propeller",
    },
    "maskmusai": {   # winter: the snowmobile
        "winter": "its body built as a little snowmobile, two long ski runners for feet, a track tread under its body, a tall clear windscreen crest rising over its mask, snow spraying, frost",
        "spring": "two short ski runners for feet with mud on them, a small windscreen crest over its mask, melting snow dripping",
        "summer": "two short ski runners for feet lifted up, a small dark tinted windscreen crest over its mask like sunglasses",
        "autumn": "two short ski runners for feet in fallen leaves, a small windscreen crest over its mask with the first frost",
    },
}
VEHICLE = {"musai": "the season itself", "codemusai": "the dialect: a piece of each",
           "seekmusai": "side-by-side (UTV)", "caremusai": "pontoon boat", "lensmusai": "model plane", "maskmusai": "snowmobile"}

TAIL = ("full body, chibi proportions, big round head, soft shading, mostly greyscale, medium grey body with light grey "
        "highlights and dark grey shading, only small touches of colour, clean black outline, isolated on white, centered, "
        "large in the frame, the whole body inside the picture with white space on every side, no rider, no person, "
        "no shadow, no text, game asset")


def prompt(n, s):
    home = DAEMONS[n][3]
    lead = "its fullest, most complete seasonal form" if home == s else "its %s form" % s
    return ("pixel art sprite, chibi, the same creature as in the image redrawn as %s: %s, keeping its face and "
            "its shape; %s, facing left three-quarter view, %s" % (lead, DAEMONS[n][4], MOTIF[n][s], TAIL))


def readpal(f):
    l = open(f).read().splitlines()[3:19]; return [tuple(int(v) for v in x.split()) for x in l]


def rom_ref(n):
    p = "%s/src/%s_romfront_512.png" % (HERE, n)
    if not os.path.exists(p):
        os.makedirs(HERE + "/src", exist_ok=True)
        d = G + DAEMONS[n][0]
        idx = np.array(Image.open(d + "/front.png"))[:64, :64]; pal = readpal(d + "/normal.pal")
        a = np.array([pal[i] if i else (255, 255, 255) for i in idx.flat], np.uint8).reshape(64, 64, 3)
        Image.fromarray(a).resize((512, 512), Image.NEAREST).save(p)
    return p


def draw(out, text, seed, refs):
    import spriteforge as SF
    if os.path.exists(out + ".png"): return
    p = dict(mode="t2i", out=out, prompt=text, negative="", seed=seed, steps=None, cfg=None, sampler=None, scheduler=None,
             denoise=1.0, stop_at=None, size=(512, 512), model="klein4b", loras=LORA, references=list(refs))
    for k in range(3):
        try: SF.run(p); return
        except SystemExit as e: print("  retry", out, e, flush=True); time.sleep(10)
        except Exception as e: print("  retry", out, repr(e), flush=True); time.sleep(10)


def gen(names):
    os.makedirs(HERE + "/raw", exist_ok=True)
    for n in DAEMONS:
        if names and n not in names: continue
        for s in SEASONS:
            for seed in SEEDS:
                print(n, s, seed, flush=True)
                draw("%s/raw/%s_%s_%d" % (HERE, n, s, seed), prompt(n, s), seed, [rom_ref(n)])


def reduce_all():
    import gbs, armc
    for d in ("clean", "reduced"): os.makedirs(HERE + "/" + d, exist_ok=True)
    M = {}
    for n, (slot, t, word, home, _) in DAEMONS.items():
        for s in SEASONS:
            for seed in SEEDS:
                key = "%s_%s_%d" % (n, s, seed); src = "%s/raw/%s.png" % (HERE, key)
                if not os.path.exists(src): continue
                cl = "%s/clean/%s.png" % (HERE, key)
                ok, err = armc.clean(src, cl)
                m = dict(daemon=n, season=s, seed=seed, type=word)
                if not ok: m["error"] = err; M[key] = m; continue
                m["folded"] = armc.fold(cl, t)
                #  shift_off moves an accent within 40 degrees of the type's hue to the far side of the wheel (a red eye
                #  on a VECTOR daemon is no eye). On the near-grey types (armc.ACHRO) the body has no hue to protect, and
                #  the rule turned MUSAI's orange autumn leaves navy -- so on those it is skipped; elsewhere it stands, and
                #  the prompts keep each season's accent off the type's hue (SEEKMUSAI's leaves gold, LENSMUSAI's blossom
                #  pale yellow).
                keep = gbs.shift_off
                if t in armc.ACHRO: gbs.place_rich.__globals__["shift_off"] = lambda acc, typ: acc
                try: grid, pal = gbs.place_rich(cl, gbs.TYPE_COLOR[t])
                except Exception as e: m["error"] = repr(e)[:300]; M[key] = m; continue
                finally: gbs.place_rich.__globals__["shift_off"] = keep
                gbs.write_png4("%s/reduced/%s.png" % (HERE, key), grid, pal)
                g = np.array(grid); m["px"] = int((g > 0).sum()); m["colours"] = len(set(g.flat) - {0})
                edge = int((g[0] > 0).sum() + (g[-1] > 0).sum() + (g[:, 0] > 0).sum() + (g[:, -1] > 0).sum())
                m["edge"] = edge
                M[key] = m; print(key, m, flush=True)
    json.dump(M, open(HERE + "/metrics.json", "w"), indent=1)
    P = json.load(open(HERE + "/picks.json")) if os.path.exists(HERE + "/picks.json") else {}
    for n in DAEMONS:
        for s in SEASONS:
            k = "%s_%s" % (n, s)
            if P.get(k, {}).get("by") == "eye": continue
            c = [M.get("%s_%d" % (k, seed)) for seed in SEEDS]; c = [m for m in c if m and "px" in m]
            if c:   # fewer pixels on the frame's edge, then the fuller body
                b = min(c, key=lambda m: (m["edge"] > 0, m["edge"], -m["px"])); P[k] = dict(seed=b["seed"], by="score")
    json.dump(P, open(HERE + "/picks.json", "w"), indent=1)


F = lambda z: ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", z)
PAPER = (236, 234, 226); INK = (30, 30, 34); GROUND = (205, 205, 172); RED = (170, 40, 40)
SEASON_TINT = {"winter": (214, 226, 236), "spring": (220, 234, 212), "summer": (244, 232, 198), "autumn": (236, 214, 192)}


def sprite(png):
    im = Image.open(png); idx = np.array(im); a = np.array(im.convert("RGBA")); a[idx == 0, 3] = 0
    return Image.fromarray(a)


def sheet(out=None, scale=3):
    import gbs
    P = json.load(open(HERE + "/picks.json"))
    CW, RH, LW = 64 * scale + 36, 64 * scale + 58, 250
    W = LW + 4 * CW + 16 + 64 * 2 + 24; H = 96 + 6 * RH + 40
    sh = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(sh)
    d.text((16, 12), "T-532  THE MUSAI BRANCH'S SEASONS -- concept fronts, DRAFT (not in the ROM)", fill=INK, font=F(20))
    d.text((16, 42), "arm C (FLUX.2 klein 4B + pixel-art LoRA) from each ROM front, reduced to 64x64 / 16 colours in its type ramp. "
           "* = home season (the fullest form).", fill=INK, font=F(13))
    d.text((16, 60), "CONTENT keeps the northern year, CONTEXT the southern: the same daemon wears opposite seasons in the two editions.",
           fill=INK, font=F(13))
    for j, s in enumerate(SEASONS):
        x = LW + j * CW
        d.rectangle((x, 82, x + CW - 8, 82 + 6 * RH), fill=SEASON_TINT[s])
        d.text((x + 8, 86), s.upper(), fill=INK, font=F(15))
    x0 = LW + 4 * CW + 8
    d.text((x0, 86), "ROM now", fill=INK, font=F(13))
    for i, (n, (slot, t, word, home, _)) in enumerate(DAEMONS.items()):
        y = 108 + i * RH
        d.text((16, y + 10), n.upper(), fill=INK, font=F(17))
        sw = gbs.TYPE_COLOR[t]
        d.rectangle((16, y + 38, 34, y + 56), fill=sw, outline=INK)
        d.text((42, y + 38), word, fill=INK, font=F(14))
        d.text((16, y + 64), VEHICLE[n], fill=INK, font=F(12))
        if home: d.text((16, y + 82), "home: " + home, fill=RED, font=F(12))
        for j, s in enumerate(SEASONS):
            k = "%s_%s" % (n, s); x = LW + j * CW + 10
            if k not in P: d.text((x, y + 40), "(none)", fill=RED, font=F(12)); continue
            im = sprite("%s/reduced/%s_%d.png" % (HERE, k, P[k]["seed"]))
            sh.paste(im.resize((64 * scale, 64 * scale), Image.NEAREST), (x, y), im.resize((64 * scale, 64 * scale), Image.NEAREST))
            lab = s + (" *" if home == s else "")
            d.text((x, y + 64 * scale + 2), "%s  seed %d" % (lab, P[k]["seed"]), fill=RED if home == s else INK, font=F(11))
        rp = G + slot + "/front.png"; pal = readpal(G + slot + "/normal.pal")
        im = Image.open(rp); idx = np.array(im)[:64, :64]
        a = np.zeros((64, 64, 4), np.uint8)
        for yy in range(64):
            for xx in range(64):
                if idx[yy, xx]: a[yy, xx] = pal[idx[yy, xx]] + (255,)
        r = Image.fromarray(a).resize((128, 128), Image.NEAREST); sh.paste(r, (x0, y + 20), r)
    d.text((16, H - 28), "Under the fable rule the vehicles are part of each body, never ridden. Backs, icons and followers come after the pick.",
           fill=INK, font=F(12))
    out = out or HERE + "/sheets/t532_musai_seasons_concepts.png"
    os.makedirs(os.path.dirname(out), exist_ok=True); sh.save(out); print(out, sh.size)
    return out


def realsize(out=None):
    """every pick at 1x and 2x on the battle ground, the way the screen shows them"""
    P = json.load(open(HERE + "/picks.json"))
    W = 16 + 4 * 220; H = 40 + 6 * 150
    sh = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(sh)
    d.text((16, 10), "T-532 concepts at real size (1x, 2x) on the battle ground -- DRAFT", fill=INK, font=F(14))
    for i, n in enumerate(DAEMONS):
        for j, s in enumerate(SEASONS):
            k = "%s_%s" % (n, s); x = 16 + j * 220; y = 40 + i * 150
            if k not in P: continue
            im = sprite("%s/reduced/%s_%d.png" % (HERE, k, P[k]["seed"]))
            b = Image.new("RGBA", (64, 64), GROUND + (255,)); b.alpha_composite(im)
            sh.paste(b.convert("RGB"), (x, y + 16)); sh.paste(b.convert("RGB").resize((128, 128), Image.NEAREST), (x + 72, y + 16))
            d.text((x, y), "%s %s" % (n.upper(), s), fill=INK, font=F(11))
    out = out or HERE + "/sheets/t532_musai_seasons_realsize.png"; sh.save(out); print(out, sh.size); return out


SUMMARY = [
    ("THE IDEA", "Each of the six MUSAI has four seasonal forms (24 looks) and wears the one DaemonsSeason() gives it: CONTENT "
     "on the northern year, CONTEXT on the southern. OVERLOADED's idea, moved from the weather to the year; separate from "
     "evolution; the type never changes. The vehicles are part of each body, never ridden. A home season is the fullest form."),
    ("THE BRANCH", "MUSAI wears the season itself. CODEMUSAI is the shared tongue: a small piece of each sibling's body in "
     "that sibling's season, and glyph lights. MASKMUSAI winter (runners, windscreen crest); LENSMUSAI spring (model-plane "
     "wings, propeller); CAREMUSAI summer (pontoon floats, canopy); SEEKMUSAI autumn (knobby wheels, roll-bar frame)."),
    ("HOW (RECOMMENDED)", "A seasonal display id, the way the INDEX's Unown letters work: one function, called where pictures, "
     "palettes and icons are chosen, so battle, party, PC, follower, summary and INDEX all follow. The species never changes: "
     "no save change. About 85 KB of ROM (of 4.9 MB free), 0 bytes of EWRAM and IWRAM. A battle keeps the season it began in."),
    ("CRYPTOPHASIA", "CODEMUSAI's own routine, learned at 30. LOGIC, special, 100% accurate, 10 PP. Power 40, +20 for each "
     "other MUSAI-branch daemon in the party still able to fight (40 to 140). Move 383; 12 letters, the limit. DRAFT text: "
     "'Words only its own / family can follow. / It hits harder for / each of them near.'"),
    ("FOR THE USER", "How forms are built; whether today's art becomes summer; look only or a battle edge; whether the change "
     "is noticed; INDEX entries per form; CRYPTOPHASIA's power rule and level; the seed for each concept. "
     "All in docs/musai-seasons-draft.md, section F."),
]


def wrap(d, text, font, width):
    out, line = [], ""
    for w in text.split():
        t = (line + " " + w).strip()
        if d.textlength(t, font=font) <= width: line = t
        else: out.append(line); line = w
    return out + [line]


def pdf(out=None):
    """one page (A4 at 200 dpi): the concept sheet and the design summary"""
    W, H = 1654, 2339; M = 90
    pg = Image.new("RGB", (W, H), (250, 249, 245)); d = ImageDraw.Draw(pg)
    d.text((M, 70), "The MUSAI branch keeps the seasons", fill=INK, font=F(46))
    d.text((M, 132), "T-532 -- design and concept drafts, 2026-11-08. DRAFT: nothing here is in the game until the user picks.",
           fill=RED, font=F(20))
    y = 186
    for head, text in SUMMARY:
        d.text((M, y), head, fill=INK, font=F(20)); y += 28
        for l in wrap(d, text, F(18), W - 2 * M):
            d.text((M + 16, y), l, fill=INK, font=F(18)); y += 24
        y += 12
    sh = Image.open(HERE + "/sheets/t532_musai_seasons_concepts.png")
    room = H - y - 70; sc = min((W - 2 * M) / sh.width, room / sh.height)
    sh = sh.resize((int(sh.width * sc), int(sh.height * sc)), Image.LANCZOS)
    pg.paste(sh, ((W - sh.width) // 2, y + 6))
    d.text((M, H - 54), "docs/musai-seasons-draft.md  |  gfx/drafts/t532_musai_seasons/  |  the vision bible's 9.34 when approved",
           fill=INK, font=F(16))
    out = out or HERE + "/t532_musai_seasons.pdf"
    pg.save(out, "PDF", resolution=200.0); print(out); return out


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "gen": gen(a[1:])
    elif a[0] == "reduce": reduce_all()
    elif a[0] == "sheet": sheet(); realsize()
    elif a[0] == "pdf": pdf()
    elif a[0] == "prompts":
        for n in DAEMONS:
            for s in SEASONS: print(n, s, "::", prompt(n, s))
