"""T-452 batch 8 (2026-10-27): DRUM to STEEPEST (140-160, less ARTSAI, a pilot), every line whole, the charm recipe, drafted into gfx/drafts/t452/k.

    batch.py charm8|contact|charmback|charmlo --dir=k --seed=5600 --prefix=t452b8 NAME ...   the drafts (one job at a time)
    batch.py reduce --dir=k --seed=5600 --prefix=t452b8 NAME ...                            fronts and backs by reduce2
    batch8.py icons      every chosen icon by round2.icon_from_draft (card off, cleaned, icon3), into k/picks.json
    batch8.py sheets     in ROM | draft front/back/icon, 1x and 3x, with the draft's shiny (sheet_r2), five to a sheet,
                         and the one-page overview t452b8_combined.png (combined_r2's layout)

Seeds: t2i chibi fronts 5601/5602 (5603/5604 a second wording), i2i from today's front 0.8 = 5621, 0.85 = 5622
(0.72 = 5623, 0.76 = 5624 where charmlo ran), one back from today's back 0.66 = 5631, one chibi icon 5641 (charm8:
the server shared by four batches), backs turned from the chosen new front 0.75 = 5651, 0.85 = 5652. Drafts only: nothing in gfx/daemons/
or the engine."""
import json, os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
R = "/Users/christopherhicks/Projects/DAEMONS"; T = os.environ.get("T452_ROOT", R + "/gfx/drafts/t452"); D = T + "/k"
PY = os.path.expanduser("~/.pyenv/versions/3.12.2/bin/python3")
SP = "/private/tmp/claude-502/-Users-christopherhicks-Projects-DAEMONS/d99297fc-c29c-48ac-bea7-477ee8d1422e/scratchpad/"
NAMES = ["drum", "punchcard", "fossilnet", "deadlock", "orpheus", "asclepius", "prometheus", "canary", "emergence", "singular", "starr", "primer", "syllabus", "curriculum", "tepid", "seethe", "heatdeath", "learnrate", "momentum", "steepest"]

def icons():
    os.chdir(R); sys.argv = [sys.argv[0], "gen"]
    import round2
    ch = json.load(open(D + "/choose.json")); P = json.load(open(D + "/picks.json"))
    for n in NAMES:
        if n not in P: continue
        if ch[n]["icon"] == "derived":   # icon3 from the clean new front (round two's rule for a lost bust)
            import icon3
            P[n]["measured"]["icon3"] = icon3.make(n, P[n]["type"], f"{D}/clean/{n}_front.png", f"{D}/reduced/{n}_icon.png")
        else:
            P[n]["measured"]["icon3"] = round2.icon_from_draft("k", n, ch[n]["icon"], P[n]["type"])
        print(n, P[n]["measured"]["icon3"]["icon_palette"], P[n]["measured"]["icon3"]["size"], flush=True)
    json.dump(P, open(D + "/picks.json", "w"), indent=1)

def sheets():
    ch = json.load(open(D + "/choose.json"))
    done = [n for n in NAMES if os.path.exists(f"{D}/reduced/{n}_front.png")]
    for k in range(0, len(done), 5):
        grp = done[k:k + 5]
        args = [f"{n}:k:" + ("LOST KEY: " + ch[n]["failed"] + " -- " if ch[n].get("failed") else "") + ch[n].get("note", "")
                for n in grp]
        subprocess.run([PY, HERE + "/sheet_r2.py", SP + "t452b8_work/sheets/t452b8_sheet%d.png" % (k // 5 + 1),
                        "T-452 batch 8 -- DRAFT, not in the ROM: in ROM | draft, front / back / icon, 1x and 3x, and the draft's shiny"]
                       + args, check=True)
    combined(done, ch)

def combined(done, ch):
    from sheet_r2 import show, on, readpal, BY, G, F, FS, PAPER, INK, GROUND, PARTY
    from PIL import Image, ImageDraw
    CW, RH, per = 3 * (64 * 2 + 70) + 32 * 2 + 40 + 40, 232, 3
    rows = (len(done) + per - 1) // per
    s = Image.new("RGB", (20 + per * (CW + 20), 50 + rows * RH), PAPER); d = ImageDraw.Draw(s)
    d.text((20, 14), "T-452 batch 8 (DRUM to STEEPEST) -- DRAFT, not in the ROM: in ROM front | draft front, back, icon (1x and 2x)",
           fill=INK, font=F)
    for i, n in enumerate(done):
        v = BY[n]; rom = G + v["constant"].lower(); npal = readpal(rom + "/normal.pal")
        x = 20 + (i % per) * (CW + 20); y = 46 + (i // per) * RH
        f = ch[n].get("failed", ""); lab = ("LOST KEY" if f.startswith("front") else "FLAGGED") if f else "batch 8"
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
    s.save(SP + "t452b8_work/sheets/t452b8_combined.png"); print(SP + "t452b8_work/sheets/t452b8_combined.png", s.size)

if __name__ == "__main__":
    {"icons": icons, "sheets": sheets}[sys.argv[1]]()
