"""The device a printed manual is about, drawn for its cover with a daemon on its screen (tools/manual.py).

The user, 2026-11-11, on the LIBRARY's shelf of manuals ("we should be able to differentiate guides for different
devices more easily ... I prefer the approach that looks the best"), picked D of four mockups: every manual its own
colour, and in the middle the device it is about, a daemon on its screen. Each function returns an inline SVG; a and b
are the daemons' sprite files in the print's work folder (64x64, drawn pixel for pixel).
"""

SCREEN = "#dfe9d6"      # a lit screen, the same on every device
INK = "#16161a"


def _sprite(href, x, y, s):
    return ('<image href="%s" x="%g" y="%g" width="%g" height="%g" preserveAspectRatio="xMidYMid meet" '
            'style="image-rendering:pixelated"/>' % (href, x, y, s, s))


def _svg(body):
    # one line: pandoc would split an SVG at a blank line or a comment, but this goes straight into the page's HTML
    return '<svg class="cdev" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 260">%s</svg>' % "".join(
        line.strip() for line in body.splitlines())


def gba(a, b=None, body="#a99fd0", edge="#5b5288"):
    """The Game Boy Advance: landscape, the screen between the D-pad and the buttons."""
    return _svg(f"""
<rect x="20" y="40" width="360" height="190" rx="92" fill="{edge}"/>
<rect x="26" y="34" width="348" height="186" rx="88" fill="{body}"/>
<rect x="112" y="58" width="176" height="132" rx="10" fill="#2c2944"/>
<rect x="128" y="72" width="144" height="104" rx="3" fill="{SCREEN}"/>
<path d="M128 150 Q200 128 272 150 L272 176 L128 176z" fill="#9cc58f"/>
{_sprite(a, 162, 82, 76)}
<circle cx="138" cy="200" r="3" fill="#c94a5e"/>
<g fill="#2c2944"><rect x="54" y="106" width="44" height="14" rx="3"/><rect x="69" y="91" width="14" height="44" rx="3"/></g>
<circle cx="322" cy="104" r="15" fill="#c94a5e"/><circle cx="350" cy="128" r="15" fill="#c94a5e"/>
<g fill="#2c2944"><rect x="168" y="200" width="22" height="7" rx="3.5"/><rect x="210" y="200" width="22" height="7" rx="3.5"/></g>
<g stroke="{edge}" stroke-width="3" stroke-linecap="round"><path d="M318 176l22 -14M326 186l22 -14M334 196l22 -14"/></g>
""")


def phone(a, b=None):
    """THE COMPANION: a phone, the daemon on its screen, a word from it above."""
    return _svg(f"""
<rect x="134" y="8" width="132" height="244" rx="24" fill="{INK}" stroke="#e9e4da" stroke-width="4"/>
<rect x="146" y="30" width="108" height="200" rx="6" fill="{SCREEN}"/>
<rect x="180" y="16" width="40" height="8" rx="4" fill="#3a3a44"/>
<rect x="146" y="30" width="108" height="16" fill="#c9d8c0"/>
<g fill="#7a8a74"><rect x="152" y="36" width="20" height="4" rx="2"/><rect x="178" y="36" width="16" height="4" rx="2"/><rect x="200" y="36" width="20" height="4" rx="2"/><rect x="226" y="36" width="20" height="4" rx="2"/></g>
<rect x="160" y="58" width="80" height="26" rx="13" fill="#fff"/><path d="M190 84l8 9 4-9z" fill="#fff"/>
<g fill="{INK}"><circle cx="186" cy="71" r="3.5"/><circle cx="200" cy="71" r="3.5"/><circle cx="214" cy="71" r="3.5"/></g>
{_sprite(a, 160, 98, 80)}
<rect x="158" y="190" width="84" height="24" rx="12" fill="#a65a4f"/>
<rect x="176" y="199" width="48" height="6" rx="3" fill="#fff"/>
""")


def watch(a, b=None):
    """THE WATCH: on its strap, the crown at its side, the daemon on its hill, the time above."""
    return _svg(f"""
<rect x="160" y="0" width="80" height="260" rx="14" fill="#e9e4da"/>
<g stroke="#c9c2b4" stroke-width="2"><path d="M168 18h64M168 30h64M168 230h64M168 242h64"/></g>
<rect x="128" y="40" width="144" height="180" rx="40" fill="{INK}"/>
<rect x="140" y="52" width="120" height="156" rx="30" fill="{SCREEN}"/>
<rect x="272" y="104" width="14" height="44" rx="4" fill="#9a8f7c" stroke="{INK}" stroke-width="2"/>
<text x="200" y="88" text-anchor="middle" font-family="Avenir Next, Helvetica, sans-serif" font-weight="800" font-size="26" fill="{INK}">9:41</text>
<path d="M140 172 Q200 148 260 172 L260 208 L140 208z" fill="#9cc58f"/>
{_sprite(a, 168, 100, 64)}
""")


def link(a, b):
    """PLAYING TOGETHER: two handhelds, a daemon on each, the cable between."""
    def small(x, s, col, edge):
        return f"""<rect x="{x}" y="64" width="140" height="160" rx="20" fill="{edge}"/>
<rect x="{x + 4}" y="60" width="132" height="156" rx="18" fill="{col}"/>
<rect x="{x + 16}" y="74" width="108" height="84" rx="6" fill="#2c2944"/>
<rect x="{x + 24}" y="80" width="92" height="72" rx="2" fill="{SCREEN}"/>
{_sprite(s, x + 38, 84, 64)}
<g fill="#2c2944"><rect x="{x + 18}" y="180" width="30" height="10" rx="2"/><rect x="{x + 28}" y="170" width="10" height="30" rx="2"/></g>
<circle cx="{x + 100}" cy="178" r="9" fill="#c94a5e"/><circle cx="{x + 118}" cy="192" r="9" fill="#c94a5e"/>"""
    return _svg(f"""
<path d="M110 60 C110 6 290 6 290 60" fill="none" stroke="#e9e4da" stroke-width="7" stroke-linecap="round"/>
<rect x="100" y="52" width="20" height="14" rx="3" fill="#e9e4da"/><rect x="280" y="52" width="20" height="14" rx="3" fill="#e9e4da"/>
{small(40, a, "#a9bcd9", "#5a6f94")}
{small(220, b, "#d9b1c4", "#946279")}
""")


def tiiny(a, b=None):
    """A BIGGER MIND: the Tiiny Pocket, a small box with its light on, and the daemon sitting on it, thinking."""
    return _svg(f"""
<rect x="96" y="132" width="208" height="112" rx="16" fill="#1f2a25" stroke="#e9e4da" stroke-width="4"/>
<g stroke="#4f8a6e" stroke-width="5" stroke-linecap="round"><path d="M122 160h112M122 176h112M122 192h112M122 208h112M122 224h112"/></g>
<circle cx="270" cy="188" r="10" fill="#9df29d"/><circle cx="270" cy="188" r="18" fill="none" stroke="#9df29d" stroke-opacity=".35" stroke-width="4"/>
{_sprite(a, 136, 4, 136)}
<g fill="#e9e4da"><circle cx="282" cy="78" r="6"/><circle cx="302" cy="56" r="9"/><circle cx="330" cy="32" r="13"/></g>
""")


def scroll(a, b=None):
    """THE OLD WORD: an unrolled scroll with the word in Greek on it, and a daemon beside it."""
    return _svg(f"""
<rect x="40" y="56" width="216" height="150" fill="#efe2bf"/>
<rect x="28" y="44" width="24" height="174" rx="12" fill="#b79257" stroke="#6e5326" stroke-width="3"/>
<rect x="244" y="44" width="24" height="174" rx="12" fill="#b79257" stroke="#6e5326" stroke-width="3"/>
<text x="148" y="140" text-anchor="middle" font-family="Iowan Old Style, Palatino, Georgia, serif" font-size="44" fill="#4d3a26">δαίμων</text>
<g stroke="#c8b48a" stroke-width="3" stroke-linecap="round"><path d="M74 168h148M90 184h116"/></g>
{_sprite(a, 268, 70, 128)}
""")


KIND = {"gba": gba, "phone": phone, "watch": watch, "link": link, "tiiny": tiiny, "scroll": scroll}

#  the cover's own colour, and what draws its device, for every book tools/manual.py prints with the game's cover
#  and the daemon(s) on its screen
COVER = {"main": ("#3b2f66", "gba", ("CLUSTER",)), "quick": ("#6a4f22", "gba", ("LABEL",)),
         "micro": ("#5e2a40", "gba", ("PING",)), "companion": ("#5e2b24", "phone", ("ROVERBYTE",)),
         "watch": ("#174d4b", "watch", ("ROVERCUB",)), "social": ("#22395c", "link", ("PENGUIN", "PENPHIN")),
         "tiiny": ("#21463a", "tiiny", ("INFERENCE",)), "etymology": ("#47431c", "scroll", ("GUARDIAN",))}

#  laid over each book's own manual.css: the cover in its colour, the device large, the small print still readable
CSS = """.cover[style*="--cbg"] { background: var(--cbg); }
.cdev { width: 118mm; height: auto; max-height: 82mm; }
.cbot { color: rgba(255, 255, 255, .72); }
.cstrip img { background: rgba(0, 0, 0, .28); }"""
