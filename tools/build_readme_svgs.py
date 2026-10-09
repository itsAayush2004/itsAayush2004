"""Generate the SVG cards used by the profile README.

Edit the content below, then run:  python3 tools/build_readme_svgs.py
Output goes to assets/readme/. GitHub renders README images without web
fonts, so every card uses system font stacks.
"""
from pathlib import Path
from textwrap import wrap
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets" / "readme"

INK = "#0E0E10"
CARD = "#16161A"
LINE = "#2A2A30"
TEXT = "#F4F2EE"
MUTED = "#B4B0A9"
DIM = "#86837D"
ACCENT = "#8C242F"
RED = "#E0262F"
GREEN = "#39D353"
BLUE = "#0EA5E9"

SANS = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

STYLE = f"""<style>
.s{{font-family:{SANS}}}
.m{{font-family:{MONO}}}
</style>"""


def svg(w, h, body, label):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">\n'
        f"<title>{escape(label)}</title>\n{STYLE}\n{body}\n</svg>\n"
    )


def write(name, content):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(content, encoding="utf-8")
    print("wrote", name)


def t(x, y, s, cls="s", size=14, fill=TEXT, weight=400, anchor="start", extra=""):
    return (
        f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" fill="{fill}" '
        f'font-weight="{weight}" text-anchor="{anchor}" {extra}>{escape(s)}</text>'
    )


def pill_w(s, size=13, mono=False):
    per = 0.62 if mono else 0.58
    return int(len(s) * size * per + 24)


# ---------------------------------------------------------------- hero
def hero():
    w, h = 880, 300
    roles = ["Developer", "AI Systems", "3D Tooling", "Games"]
    x = 40
    pills = []
    for r in roles:
        pw = pill_w(r, 12, mono=True)
        pills.append(
            f'<rect x="{x}" y="236" width="{pw}" height="28" rx="14" fill="#1E1E23"/>'
            + t(x + pw / 2, 254, r, "m", 12, "#E9E6E0", 500, "middle")
        )
        x += pw + 8
    body = f"""
<rect width="{w}" height="{h}" rx="20" fill="{INK}"/>
<circle cx="800" cy="40" r="170" fill="none" stroke="{LINE}"/>
<circle cx="760" cy="110" r="80" fill="none" stroke="{LINE}"/>
<rect x="40" y="36" width="96" height="28" rx="6" fill="none" stroke="#3A3A40"/>
{t(52, 55, "$", "m", 12, RED, 700)}{t(64, 55, " whoami", "m", 12, "#CFCBC4")}
<circle cx="156" cy="50" r="4" fill="{GREEN}"><animate attributeName="opacity" values="1;.25;1" dur="1.8s" repeatCount="indefinite"/></circle>
{t(167, 55, "shipping ARTHIS", "m", 12, "#9FD8A8")}
<text x="34" y="176" class="s" font-size="104" font-weight="900" fill="{TEXT}" letter-spacing="-4">Aayush<tspan fill="{RED}">.</tspan></text>
{t(40, 214, "Game developer & AI/backend engineer · Jaipur, India", "s", 17, "#CFCBC4", 500)}
{''.join(pills)}
{t(840, 52, "BUILD", "m", 11, DIM, 400, "end", 'letter-spacing="3"')}
{t(840, 70, "CREATE", "m", 11, DIM, 400, "end", 'letter-spacing="3"')}
{t(840, 88, "EXPLORE", "m", 11, DIM, 400, "end", 'letter-spacing="3"')}
<g transform="translate(690 120)" fill="none" stroke-width="16" stroke-linecap="square">
<path d="M45 15 L10 55 L45 95" stroke="{TEXT}"/>
<path d="M105 15 L140 55 L105 95" stroke="{TEXT}"/>
<path d="M88 8 L62 102" stroke="{RED}"/>
</g>
{t(840, 266, "NIT Jaipur · ECE", "m", 11, DIM, 400, "end")}
"""
    write("hero.svg", svg(w, h, body, "Aayush — game developer and AI/backend engineer"))


# ---------------------------------------------------------------- CTA + tiles
def cta():
    w, h = 880, 112
    body = f"""
<rect width="{w}" height="{h}" rx="16" fill="{ACCENT}"/>
{t(30, 36, "START HERE", "m", 11, "#F6D3D6", 500, "start", 'letter-spacing="2.5"')}
{t(30, 68, "Walk through my 3D portfolio", "s", 26, "#FFFFFF", 800)}
{t(30, 92, "Nine themed rooms you scroll through — doors and all.", "s", 14, "#F6D3D6")}
<g fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
<g><animateTransform attributeName="transform" type="translate" values="0 0;8 0;0 0" dur="1.4s" repeatCount="indefinite"/>
<path d="M800 56h40"/><path d="M826 42l14 14-14 14"/></g>
</g>
"""
    write("cta-portfolio.svg", svg(w, h, body, "Walk through my 3D portfolio"))


def tile(name, kicker, title, color):
    w, h = 214, 72
    body = f"""
<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="12" fill="{CARD}" stroke="{LINE}"/>
{t(16, 29, kicker, "m", 10, color, 700, "start", 'letter-spacing="1.5"')}
{t(16, 53, title, "s", 17, TEXT, 700)}
<path d="M186 30l8 8-8 8" fill="none" stroke="{DIM}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
"""
    write(name, svg(w, h, body, title))


# ---------------------------------------------------------------- tagline strip
def strip():
    w, h = 880, 46
    lines = [
        "Multiplayer mini-games · real-time worlds",
        "Interactive 3D on the web with Three.js",
        "Unity + Python relays + WebGL",
    ]
    n = len(lines)
    dur = n * 3
    parts = []
    for i, s in enumerate(lines):
        a, b = i / n, (i + 1) / n
        keys = f"0;{a:.3f};{a+0.02:.3f};{b-0.02:.3f};{b:.3f};1"
        vals = "0;0;1;1;0;0"
        if i == 0:
            keys, vals = f"0;0.02;{b-0.02:.3f};{b:.3f};0.98;1", "0;1;1;0;0;0"
        parts.append(
            f'<g opacity="0"><animate attributeName="opacity" values="{vals}" keyTimes="{keys}" '
            f'dur="{dur}s" repeatCount="indefinite"/>'
            + t(42, 28, s, "m", 14, "#E2DED7")
            + "</g>"
        )
    body = f"""
<rect width="{w}" height="{h}" rx="12" fill="{CARD}"/>
{t(22, 28, ">", "m", 14, RED, 700)}
{''.join(parts)}
<rect x="852" y="15" width="8" height="16" fill="{RED}"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect>
"""
    write("strip.svg", svg(w, h, body, "Multiplayer mini-games, real-time worlds, Three.js, Unity and WebGL"))


# ---------------------------------------------------------------- section headers
def header(name, num, title, note):
    w, h = 880, 54
    body = f"""
{t(0, 36, num, "m", 13, RED, 700)}
{t(34, 37, title, "s", 26, "#8C8A85", 800)}
{t(880, 36, note, "m", 12, "#8C8A85", 400, "end")}
<rect x="0" y="52" width="{w}" height="1" fill="#8C8A85" opacity=".35"/>
"""
    write(name, svg(w, h, body, title))


# ---------------------------------------------------------------- stats
def stats():
    w, h = 880, 236
    items = [
        ("154", "interactive builds"), ("141K", "lines of game code"), ("43", "Three.js 3D builds"),
        ("15", "P2P multiplayer games"), ("28", "Blender add-ons"), ("21.9K", "YouTube subscribers"),
    ]
    cw, ch = w / 3, h / 2
    parts = [f'<rect width="{w}" height="{h}" rx="16" fill="{CARD}"/>']
    parts.append(f'<path d="M{cw} 18V{h-18}M{2*cw} 18V{h-18}M18 {ch}H{w-18}" stroke="{LINE}"/>')
    for i, (num, lab) in enumerate(items):
        x = (i % 3) * cw + 28
        y = (i // 3) * ch
        color = RED if i == 5 else TEXT
        parts.append(t(x, y + 68, num, "s", 46, color, 900, "start", 'letter-spacing="-1"'))
        parts.append(t(x, y + 94, lab, "s", 14, MUTED))
    write("stats.svg", svg(w, h, "\n".join(parts), "By the numbers"))


# ---------------------------------------------------------------- project cards
PROJECTS = [
    ("card-portfolio.svg", "01", "THREE.JS · SINGLE FILE", "Portfolio — the house",
     "My CV as a scroll-driven 3D house. Nine themed rooms on a zig-zag plan; doors swing open as you approach and every room's work hangs on its walls.",
     "Walk through", RED),
    ("card-space.svg", "02", "SUPABASE · 10K DAU", "ARTHIS.space",
     "An endless, swipeable feed of single- and multiplayer mini-games — no installs. Backend scaled from 1 to 10,000 daily active users.",
     "Play now", RED),
    ("card-land.svg", "03", "UNITY · WEBGL", "ARTHIS.land — The Wall",
     "A handcrafted Unity vertical city — real-time multiplayer, playable in the browser. 40+ rooms live on the wall.",
     "Enter the wall", RED),
    ("card-relay.svg", "04", "PYTHON STDLIB · 0 DEPS", "arthisland-relay",
     "Real-time multiplayer relay — 2–4 players per room over TCP and WebSocket, written from scratch with zero dependencies. Containerised and cloud-ready.",
     "View source", TEXT),
    ("card-hexabed.svg", "05", "UNITY · C# · 3,705 LINES", "HexaBed",
     "Procedural hex-grid terrain engine — 160+ tiles into one world, a road generator that reads neighbouring heights, and a custom inspector so designers never open a script.",
     "14 scripts · 160+ tiles", DIM),
    ("card-atlas.svg", "06", "THREE.JS · GITHUB PAGES", "Travel Atlas",
     "A living 3D globe charting 30+ places I've been — and the ones I still dream of. Auto-deploys on every push.",
     "Spin the globe", BLUE),
]


def card(name, num, kicker, title, desc, action, color):
    w, h = 432, 236
    lines = wrap(desc, 54)[:4]
    desc_svg = "".join(t(24, 104 + i * 21, ln, "s", 14, MUTED) for i, ln in enumerate(lines))
    aw = pill_w(action + "  →", 13)
    body = f"""
<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="16" fill="{CARD}" stroke="{LINE}"/>
<circle cx="28" cy="34" r="4" fill="{color}"/>
{t(40, 38, kicker, "m", 11, DIM, 500, "start", 'letter-spacing="1.5"')}
{t(w-24, 38, num, "m", 11, DIM, 500, "end")}
{t(24, 74, title, "s", 22, TEXT, 800)}
{desc_svg}
<rect x="24" y="{h-50}" width="{aw}" height="30" rx="8" fill="none" stroke="#3A3A40"/>
{t(24 + aw/2, h-30, action + "  →", "s", 13, TEXT, 700, "middle")}
"""
    write(name, svg(w, h, body, f"{title} — {desc}"))


# ---------------------------------------------------------------- toolkit
STACK = [
    ("ENGINES", ["Unity", "Unreal Engine"]),
    ("LANGUAGES", ["C#", "Python", "JavaScript", "C++", "Java", "HTML/CSS"]),
    ("WEB 3D", ["Three.js", "WebGL", "Unity WebGL", "WebRTC"]),
    ("AI & BACKEND", ["FastAPI", "RAG pipelines", "Vector DBs", "LLM workflows", "ComfyUI", "n8n"]),
    ("DATA", ["Supabase", "PostgreSQL", "Docker"]),
    ("3D & TOOLING", ["Blender + Python API", "Unity editor tooling", "GLB/FBX pipelines"]),
]


def toolkit():
    w = 880
    row_h = 52
    h = row_h * len(STACK) + 16
    parts = [f'<rect width="{w}" height="{h}" rx="16" fill="{CARD}"/>']
    for i, (lab, items) in enumerate(STACK):
        y = 8 + i * row_h
        if i:
            parts.append(f'<rect x="24" y="{y}" width="{w-48}" height="1" fill="{LINE}"/>')
        parts.append(t(28, y + 31, lab, "m", 11, DIM, 500, "start", 'letter-spacing="1.5"'))
        x = 190
        for it in items:
            pw = pill_w(it, 13)
            parts.append(f'<rect x="{x}" y="{y+12}" width="{pw}" height="28" rx="14" fill="#222228"/>')
            parts.append(t(x + pw / 2, y + 31, it, "s", 13, "#E9E6E0", 600, "middle"))
            x += pw + 8
    write("toolkit.svg", svg(w, h, "\n".join(parts), "Toolkit"))


# ---------------------------------------------------------------- play button + footer
def play():
    w, h = 300, 52
    body = f"""
<rect width="{w}" height="{h}" rx="12" fill="{GREEN}"/>
<path d="M28 17l18 9-18 9z" fill="#04220E"/>
{t(60, 32, "PLAY COMMIT BREAKOUT", "s", 15, "#04220E", 800, "start", 'letter-spacing="0.6"')}
"""
    write("play-breakout.svg", svg(w, h, body, "Play Commit Breakout"))


def footer():
    w, h = 880, 170
    body = f"""
<rect width="{w}" height="{h}" rx="20" fill="{INK}"/>
<text x="40" y="70" class="s" font-size="30" font-weight="800" fill="{TEXT}">Handcrafted worlds,</text>
<text x="40" y="106" class="s" font-size="30" font-weight="800" fill="{TEXT}">real-time and on the web<tspan fill="{RED}">.</tspan></text>
{t(40, 136, "open to collabs, game jams and interesting problems", "m", 12, DIM)}
<rect x="686" y="62" width="154" height="48" rx="12" fill="{TEXT}"/>
<g fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<rect x="706" y="77" width="22" height="17" rx="2"/><path d="M706 80l11 7 11-7"/></g>
{t(740, 92, "Say hello", "s", 16, INK, 800)}
"""
    write("footer.svg", svg(w, h, body, "Handcrafted worlds, real-time and on the web — say hello"))


if __name__ == "__main__":
    hero()
    cta()
    tile("tile-space.svg", "MINI GAMES", "ARTHIS.space", RED)
    tile("tile-land.svg", "THE WALL", "ARTHIS.land", RED)
    tile("tile-atlas.svg", "LIVE DEMO", "Travel Atlas", BLUE)
    tile("tile-email.svg", "REACH OUT", "Email me", GREEN)
    strip()
    header("h-arcade.svg", "01", "Contribution arcade", "every green square is a brick")
    header("h-about.svg", "02", "About me", "Jaipur, India")
    header("h-numbers.svg", "03", "By the numbers", "and counting")
    header("h-projects.svg", "04", "Featured projects", "click a card")
    header("h-toolkit.svg", "05", "Toolkit", "what I build with")
    stats()
    for p in PROJECTS:
        card(*p)
    toolkit()
    play()
    footer()
