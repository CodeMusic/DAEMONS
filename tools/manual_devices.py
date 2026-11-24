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


def glasses(a, b=None):
    """THE GLASSES: a frame seen from the front, the prism before the right lens, the daemon in its square."""
    return _svg(f"""
<rect x="40" y="96" width="140" height="104" rx="42" fill="#eef3f6" fill-opacity=".25" stroke="#e9e4da" stroke-width="8"/>
<rect x="220" y="96" width="140" height="104" rx="42" fill="#eef3f6" fill-opacity=".25" stroke="#e9e4da" stroke-width="8"/>
<path d="M180 124 Q200 106 220 124" fill="none" stroke="#e9e4da" stroke-width="8"/>
<path d="M40 120 L8 112 M360 120 L392 112" stroke="#e9e4da" stroke-width="8" stroke-linecap="round"/>
<rect x="300" y="70" width="96" height="30" rx="8" fill="{INK}"/>
<rect x="244" y="104" width="92" height="92" rx="4" fill="#9fd3e6" fill-opacity=".45" stroke="#e9e4da" stroke-width="3"/>
<rect x="252" y="112" width="76" height="76" fill="{INK}"/>
{_sprite(a, 258, 118, 64)}
""")


def cardputer(a, b=None):
    """THE CARDPUTERS: a Cardputer held flat, the daemon on its small screen, four rows of keys under it, a cap with its
    antenna along the top (C-393)."""
    keys = "".join('<rect x="%d" y="%d" width="16" height="13" rx="2" fill="#3e3e46"/>' % (86 + c * 17.6, 160 + r * 16)
                   for r in range(4) for c in range(13))
    return _svg(f"""
<rect x="104" y="26" width="192" height="22" rx="5" fill="#2f6b4f" stroke="#e9e4da" stroke-width="3"/>
<rect x="262" y="0" width="9" height="30" rx="3" fill="#8a8170"/>
<rect x="72" y="44" width="256" height="196" rx="16" fill="#e9e4da"/>
<rect x="104" y="58" width="144" height="88" rx="6" fill="{INK}"/>
<rect x="112" y="64" width="128" height="76" rx="2" fill="{SCREEN}"/>
<path d="M112 120 Q176 104 240 120 L240 140 L112 140z" fill="#9cc58f"/>
{_sprite(a, 146, 66, 60)}
<circle cx="288" cy="86" r="11" fill="#e8b04a" stroke="{INK}" stroke-width="2"/>
<circle cx="288" cy="122" r="5" fill="#9cc58f"/>
{keys}
""")


def kodedot(a, b=None):
    """THE KODE DOT: a small slab held upright, nearly all screen, the daemon in its den with its cares under it, two
    buttons on its edge and its light glowing LODESTONE's colour (C-442). A drawing: where the Dot's own buttons sit is
    the device's."""
    cares = "".join('<rect x="%d" y="176" width="26" height="11" rx="5.5" fill="none" stroke="#5f7f86" stroke-width="2"/>'
                    % (145 + i * 29) for i in range(4))
    return _svg(f"""
<rect x="112" y="10" width="176" height="240" rx="34" fill="#e9e4da"/>
<rect x="118" y="16" width="164" height="228" rx="29" fill="{INK}"/>
<rect x="288" y="58" width="6" height="30" rx="3" fill="#8a8170"/><rect x="288" y="150" width="6" height="30" rx="3" fill="#8a8170"/>
<rect x="132" y="32" width="136" height="166" rx="12" fill="{SCREEN}"/>
<rect x="150" y="40" width="100" height="5" rx="2.5" fill="#9fb09a"/>
{_sprite(a, 158, 52, 84)}
<rect x="164" y="146" width="72" height="8" rx="4" fill="#7a8a74"/>
<rect x="178" y="159" width="44" height="5" rx="2.5" fill="#9fb09a"/>
{cares}
<circle cx="200" cy="222" r="6" fill="#d9944e"/><circle cx="200" cy="222" r="11" fill="#d9944e" opacity=".25"/>
""")


def body(a, b=None):
    """EMBODIED: a four-legged body seen from the side, a servo at each joint, and the daemon in the open panel of its
    chest -- the one cover whose device has no screen (T-617). A drawing of a kind of body, not of any one kit."""
    def leg(x, back=False):
        k = -1 if back else 1
        return (f'<path d="M{x} 150 L{x - 14 * k} 190 L{x + 4 * k} 232" fill="none" stroke="#e9e4da" stroke-width="13" '
                f'stroke-linecap="round" stroke-linejoin="round"/>'
                f'<circle cx="{x}" cy="150" r="11" fill="{INK}" stroke="#e9e4da" stroke-width="3"/>'
                f'<circle cx="{x - 14 * k}" cy="190" r="8" fill="{INK}" stroke="#e9e4da" stroke-width="3"/>'
                f'<rect x="{x + 4 * k - 12}" y="228" width="24" height="9" rx="4.5" fill="#8a8170"/>')
    return _svg(f"""
<path d="M92 118 Q58 96 66 62" fill="none" stroke="#e9e4da" stroke-width="9" stroke-linecap="round"/>
<circle cx="92" cy="118" r="8" fill="{INK}" stroke="#e9e4da" stroke-width="3"/>
{leg(126, True)}{leg(274)}
<rect x="92" y="92" width="216" height="70" rx="20" fill="#e9e4da"/>
<rect x="150" y="100" width="100" height="54" rx="8" fill="{INK}"/>
<rect x="156" y="105" width="88" height="44" rx="4" fill="{SCREEN}"/>
{_sprite(a, 178, 105, 44)}
{leg(108, True)}{leg(292)}
<path d="M296 100 L318 60" fill="none" stroke="#e9e4da" stroke-width="16" stroke-linecap="round"/>
<circle cx="298" cy="100" r="10" fill="{INK}" stroke="#e9e4da" stroke-width="3"/>
<rect x="296" y="26" width="76" height="50" rx="16" fill="#e9e4da"/>
<path d="M306 30 L300 6 L324 26z" fill="#e9e4da"/><path d="M340 26 L350 4 L362 28z" fill="#e9e4da"/>
<circle cx="346" cy="48" r="7" fill="{INK}"/><circle cx="348" cy="46" r="2.2" fill="#9cc58f"/>
<rect x="364" y="52" width="14" height="10" rx="5" fill="{INK}"/>
<g stroke="#9cc58f" stroke-width="3" stroke-linecap="round" fill="none"><path d="M384 34 q8 12 0 26"/><path d="M392 26 q14 20 0 42"/></g>
""")


KIND = {"gba": gba, "phone": phone, "watch": watch, "glasses": glasses, "link": link, "tiiny": tiiny, "scroll": scroll,
        "cardputer": cardputer, "kodedot": kodedot, "body": body}

#  the cover's own colour, and what draws its device, for every book tools/manual.py prints with the game's cover
#  and the daemon(s) on its screen
COVER = {"main": ("#3b2f66", "gba", ("CLUSTER",)), "quick": ("#6a4f22", "gba", ("LABEL",)),
         "micro": ("#5e2a40", "gba", ("PING",)), "companion": ("#5e2b24", "phone", ("ROVERBYTE",)),
         "watch": ("#174d4b", "watch", ("ROVERCUB",)), "glass": ("#2e2a52", "glasses", ("PING",)), "social": ("#22395c", "link", ("PENGUIN", "PENPHIN")),
         "tiiny": ("#21463a", "tiiny", ("INFERENCE",)), "etymology": ("#47431c", "scroll", ("GUARDIAN",)),
         "cardputer": ("#7a3a16", "cardputer", ("PUNCHCARD",)),   # C-393
         "kodedot": ("#3a3f47", "kodedot", ("ANODE",)),   # C-442: graphite, the one grey cover
         "embodied": ("#1f4a3a", "body", ("ROVERBYTE",))}   # T-617: GROWTH's green, the line that ends in a body

#  laid over each book's own manual.css: the cover in its colour, the device large, the small print still readable
CSS = """.cover[style*="--cbg"] { background: var(--cbg); }
.cdev { width: 118mm; height: auto; max-height: 82mm; }
.cbot { color: rgba(255, 255, 255, .72); }
.cstrip img { background: rgba(0, 0, 0, .28); }"""
