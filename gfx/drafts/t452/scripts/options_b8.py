"""T-452 batch 8: the three open questions, each option side by side (drafts at 512 shown at 192; reduced at 3x)."""
import numpy as np, os
from PIL import Image, ImageDraw, ImageFont
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); K = W + "/k"
F = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 11)
def red(f, palf=None):
    im = Image.open(f)
    if palf: im.putpalette(Image.open(palf).getpalette())
    a = np.array(im.convert("RGBA")); a[np.array(im) == 0, 3] = 0; im = Image.fromarray(a)
    b = Image.new("RGBA", im.size, (205, 205, 172, 255)); b.alpha_composite(im); return b.convert("RGB").resize((192, 192), Image.NEAREST)
def red2(f):
    im = Image.open(f).convert("RGBA"); b = Image.new("RGBA", im.size, (205, 205, 172, 255)); b.alpha_composite(im); return b.convert("RGB").resize((192, 192), Image.NEAREST)
def dr(f): return Image.open(f).convert("RGB").resize((192, 192))
rows = [("PROMETHEUS's flame", [
          ("A as picked: crest greyed by the cap", red(K + "/reduced/prometheus_front.png")),
          ("B crest hand-painted red/yellow", red(K + "/opt/prometheus_front_flameA.png")),
          ("(draft it came from)", dr(K + "/prometheus_front_i2i_5621.png")),
          ("C t2i 5601: flame crest+tail", dr(K + "/prometheus_front_5601.png"))]),
        ("DEADLOCK one or two", [
          ("A one, as picked", red(K + "/reduced/deadlock_front.png")),
          ("B two side by side, one lock each (mock)", red2(K + "/opt/deadlock_front_twoB.png")),
          ("C the same, mirrored (mock)", red2(K + "/opt/deadlock_front_twoC.png")),
          ("today's (one)", red("/Users/christopherhicks/Projects/DAEMONS/engineGba/graphics/pokemon/snorlax/front.png", None) if False else dr(K + "/src/deadlock_front_512.png") if os.path.exists(K + "/src/deadlock_front_512.png") else Image.new("RGB",(192,192),(200,200,200)))]),
        ("STARR among the deer", [
          ("A as picked (pink stag)", red(K + "/reduced/starr_front.png")),
          ("CURRICULUM beside it", red(K + "/reduced/curriculum_front.png")),
          ("B a small star in the antlers (mock)", red2(K + "/opt/starr_front_starB.png")),
          ("(t2i ring+star 5671: no star drawn)", dr(K + "/starr_front_star_5671.png"))])]
s = Image.new("RGB", (4 * 260 + 200, len(rows) * 240 + 10), (236, 234, 226)); d = ImageDraw.Draw(s)
for i, (t, cs) in enumerate(rows):
    y = 10 + i * 240; d.text((10, y + 90), t, fill=(0, 0, 0), font=F)
    for j, (lab, im) in enumerate(cs):
        x = 200 + j * 260; s.paste(im, (x, y + 22)); d.text((x, y), lab, fill=(150, 30, 30), font=F)
s.save(W + "/sheets/t452b8_questions.png"); print(W + "/sheets/t452b8_questions.png")
