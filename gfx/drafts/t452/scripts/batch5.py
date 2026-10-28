"""T-452 batch 5 (2026-10-27): HEATSINK to COREFILE (86-105) and the PREMISE line (106, 107, 236, 237), the charm recipe, drafted into gfx/drafts/t452/h.

    batch.py charm|contact|charmback|charmlo --dir=h --seed=5300 --prefix=t452b5 NAME ...   the drafts (one job at a time)
    batch.py reduce --dir=h --seed=5300 --prefix=t452b5 NAME ...                            fronts and backs by reduce2
    batch5.py icons      every chosen icon by round2.icon_from_draft (card off, cleaned, icon3), into h/picks.json
    batch5.py sheets     in ROM | draft front/back/icon, 1x and 3x, with the draft's shiny (sheet_r2), five to a sheet,
                         and the one-page overview t452b5_combined.png (combined_r2's layout)

Seeds: t2i chibi fronts 5301/5302 (5303/5304 a second wording), i2i from today's front 0.8 = 5321, 0.85 = 5322
(0.72 = 5323, 0.76 = 5324 where charmlo ran), backs from today's back 0.66 = 5331, 0.75 = 5332, chibi icons
5341/5342, backs turned from the chosen new front 0.75 = 5351, 0.85 = 5352. Drafts only: nothing in gfx/daemons/
or the engine."""
import json, os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
R = "/Users/christopherhicks/Projects/DAEMONS"; T = os.environ.get("T452_ROOT", R + "/gfx/drafts/t452"); D = T + "/h"
PY = os.path.expanduser("~/.pyenv/versions/3.12.2/bin/python3")
SP = "/private/tmp/claude-502/-Users-christopherhicks-Projects-DAEMONS/d99297fc-c29c-48ac-bea7-477ee8d1422e/scratchpad/"
NAMES_ALL = ["heatsink", "archiver", "deadletter", "landfill", "capsule", "coldvault", "respawn", "hauntproc", "lull", "busywait", "acquire", "lockup", "fuse", "breaker", "bootstrap", "ensemble", "artefact", "corefile", "axiomkick", "rebuttal", "premise", "circular"]

NAMES = [a for a in sys.argv[2:]] or NAMES_ALL
def icons():
    os.chdir(R); sys.argv = [sys.argv[0], "gen"]
    import round2
    ch = json.load(open(D + "/choose.json")); P = json.load(open(D + "/picks.json"))
    for n in NAMES:
        if n not in P: continue
        if ch[n]["icon"] == "derived":   # icon3 from the clean new front (round two's rule for a lost bust)
            import icon3
            hf = f"{D}/hand/{n}_front.png"   # batch 5: from the hand-drawn front where hand_b5 drew one (the claw, the heads, the kick)
            P[n]["measured"]["icon3"] = icon3.make(n, P[n]["type"], hf if os.path.exists(hf) else f"{D}/clean/{n}_front.png", f"{D}/reduced/{n}_icon.png")
        else:
            P[n]["measured"]["icon3"] = round2.icon_from_draft("h", n, ch[n]["icon"], P[n]["type"])
        print(n, P[n]["measured"]["icon3"]["icon_palette"], P[n]["measured"]["icon3"]["size"], flush=True)
    json.dump(P, open(D + "/picks.json", "w"), indent=1)

def sheets():
    ch = json.load(open(D + "/choose.json"))
    done = [n for n in NAMES if os.path.exists(f"{D}/reduced/{n}_front.png")]
    for k in range(0, len(done), 5):
        grp = done[k:k + 5]
        args = [f"{n}:h:" + ("LOST KEY: " + ch[n]["failed"] + " -- " if ch[n].get("failed") else "") + ch[n].get("note", "")
                for n in grp]
        subprocess.run([PY, HERE + "/sheet_r2.py", SP + "t452b5_sheet%d.png" % (k // 5 + 1),
                        "T-452 batch 5 -- DRAFT, not in the ROM: in ROM | draft, front / back / icon, 1x and 3x, and the draft's shiny"]
                       + args, check=True)
    combined(done, ch)

def combined(done, ch):
    from sheet_r2 import show, on, readpal, BY, G, F, FS, PAPER, INK, GROUND, PARTY
    from PIL import Image, ImageDraw
    CW, RH, per = 3 * (64 * 2 + 70) + 32 * 2 + 40 + 40, 232, 3
    rows = (len(done) + per - 1) // per
    s = Image.new("RGB", (20 + per * (CW + 20), 50 + rows * RH), PAPER); d = ImageDraw.Draw(s)
    d.text((20, 14), "T-452 batch 5 (HEATSINK to CIRCULAR) -- DRAFT, not in the ROM: in ROM front | draft front, back, icon (1x and 2x)",
           fill=INK, font=F)
    for i, n in enumerate(done):
        v = BY[n]; rom = G + v["constant"].lower(); npal = readpal(rom + "/normal.pal")
        x = 20 + (i % per) * (CW + 20); y = 46 + (i // per) * RH
        f = ch[n].get("failed", ""); lab = ("LOST KEY" if f.startswith("front") else "FLAGGED") if f else "batch 5"
        d.text((x, y), "%d %s  (%s)" % (v["national"], v["name"], lab), fill=(170, 40, 40) if f else INK, font=FS)
        nd = f"{D}/reduced/{n}_"
        from PIL import Image as I
        p = I.open(nd + "front.png").getpalette()[:48]; fpal = [tuple(p[j:j + 3]) for j in range(0, 48, 3)]
        ims = [(show(rom + "/front.png", npal), GROUND), (show(nd + "front.png"), GROUND),
               (show(nd + "back.png", fpal), GROUND), (show(nd + "icon.png", None, 32), PARTY)]
        xx = x
        for j, (im, bg) in enumerate(ims):
            s.paste(on(im, bg, 1), (xx, y + 20)); s.paste(on(im, bg, 2), (xx, y + 20 + im.height + 4))
            xx += im.width * 2 + (30 if j == 0 else 8)
            if j == 0: d.line((xx - 16, y + 20, xx - 16, y + RH - 10), fill=INK, width=2)
    s.save(SP + "t452b5_combined.png"); print(SP + "t452b5_combined.png", s.size)

if __name__ == "__main__":
    {"icons": icons, "sheets": sheets}[sys.argv[1]]()
