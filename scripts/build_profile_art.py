"""Build every themed SVG used by the profile README.

Writes assets/{dark,light}/*.svg (banner, impact, pipeline, cards, closing)
and assets/icons/*.svg (theme-neutral section icons). The README switches
themed images with <picture> + prefers-color-scheme. Text inside SVGs is
sized for GitHub's ~830 px README column; anything a recruiter or crawler
must read also lives as plain Markdown in README.md.

Animations use CSS keyframes and SMIL, both of which play when GitHub
renders an SVG through <img>. Every file honours prefers-reduced-motion.

Usage: python scripts/build_profile_art.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'DejaVu Sans Mono', monospace"

THEMES = {
    "dark": {
        "bg0": "#050f22", "bg1": "#0a2348", "bg2": "#0e3a6b",
        "card": "#0b1f3f", "card2": "#071a36", "border": "#1f3a66", "grid": "#1a3d6b",
        "text": "#f2f6fb", "muted": "#9aaecc", "dim": "#7e93b8",
        "blue": "#62b0ef", "sky": "#8bd5ff", "deep": "#1d5f98", "green": "#39d353", "red": "#ff7b72",
        "num0": "#f4f8fc", "num1": "#8bd5ff", "glow": "#62b0ef",
    },
    "light": {
        "bg0": "#ffffff", "bg1": "#f1f6fd", "bg2": "#dcebfb",
        "card": "#ffffff", "card2": "#f6f8fa", "border": "#d0d7de", "grid": "#c9dcf2",
        "text": "#1f2328", "muted": "#59636e", "dim": "#6e7781",
        "blue": "#0969da", "sky": "#218bff", "deep": "#80b8f5", "green": "#1a7f37", "red": "#cf222e",
        "num0": "#0b1f3f", "num1": "#0969da", "glow": "#0969da",
    },
}

REDUCED = "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"

COMMON = """
.rise{animation:rise .8s cubic-bezier(.2,.8,.3,1) both}
.flow{stroke-dasharray:4 6;animation:flow 1.2s linear infinite}
.pulse{transform-box:fill-box;transform-origin:center;animation:pulse 2.6s ease-in-out infinite}
.blink{animation:blink 1.1s steps(1,end) infinite}
.spin{transform-box:fill-box;transform-origin:center;animation:spin 8s linear infinite}
.glow{animation:glow 3.2s ease-in-out infinite}
@keyframes rise{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
@keyframes flow{to{stroke-dashoffset:-20}}
@keyframes pulse{0%,100%{transform:scale(.85);opacity:.65}50%{transform:scale(1.15);opacity:1}}
@keyframes blink{50%{opacity:0}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes glow{0%,100%{opacity:.35}50%{opacity:1}}
"""


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(w, h, title, desc, body, style=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" '
        f'aria-labelledby="title desc" font-family="{SANS}">\n'
        f'<title id="title">{esc(title)}</title>\n<desc id="desc">{esc(desc)}</desc>\n'
        f"<style>{COMMON}{style}{REDUCED}</style>\n{body}\n</svg>\n"
    )


def packet(path, color, dur=2.4, begin=0.0, r=3.6):
    """A dot travelling along an SVG path forever (SMIL)."""
    return (f'<circle r="{r}" fill="{color}" opacity="0"><animateMotion dur="{dur}s" begin="{begin}s" '
            f'repeatCount="indefinite" path="{path}"/>'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.85;1" dur="{dur}s" '
            f'begin="{begin}s" repeatCount="indefinite"/></circle>')


def num_grad(t, gid="num"):
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t["num0"]}"/>'
            f'<stop offset="1" stop-color="{t["num1"]}"/></linearGradient>')


# =========================================================================== banner
ROLES = ["Business Intelligence Analyst", "Power BI Developer", "Data Analyst", "AI Developer"]


def banner(t):
    cycle = 3.2 * len(ROLES)
    clips, roles = [], []
    for i, role in enumerate(ROLES):
        clips.append(f'<clipPath id="c{i}"><rect class="typer r{i}" x="98" y="150" '
                     f'width="{len(role) * 15.4 + 6:.0f}" height="40"/></clipPath>')
        roles.append(f'<text clip-path="url(#c{i})" x="98" y="180" font-family="{MONO}" font-size="25.5" '
                     f'font-weight="700" fill="{t["text"]}">{esc(role)}</text>')
    delays = "".join(f".r{i}{{animation-delay:{i * 3.2}s}}" for i in range(len(ROLES)))
    style = f"""
.typer{{transform-box:fill-box;transform-origin:left center;transform:scaleX(0);animation:type {cycle}s infinite both}}
{delays}
@keyframes type{{0%{{transform:scaleX(0);animation-timing-function:steps(24,end)}}8%{{transform:scaleX(1)}}
19%{{transform:scaleX(1);animation-timing-function:steps(24,end)}}24%,100%{{transform:scaleX(0)}}}}
@media (prefers-reduced-motion: reduce){{.r0{{transform:scaleX(1)}}}}
.bar{{transform-box:fill-box;transform-origin:bottom;animation:breathe 4s ease-in-out infinite}}
.trend{{stroke-dasharray:300;animation:redraw 6s cubic-bezier(.3,.6,.3,1) infinite}}
.scan{{animation:scan 4.5s ease-in-out infinite}}
.float{{animation:float 7s ease-in-out infinite}}
@keyframes breathe{{0%,100%{{transform:scaleY(1)}}50%{{transform:scaleY(.82)}}}}
@keyframes redraw{{0%{{stroke-dashoffset:300;opacity:1}}45%,80%{{stroke-dashoffset:0;opacity:1}}95%,100%{{stroke-dashoffset:0;opacity:0}}}}
@keyframes scan{{0%,100%{{transform:translateX(0);opacity:0}}10%,90%{{opacity:.55}}50%{{transform:translateX(150px)}}}}
@keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-10px)}}}}
"""
    heights = [36, 50, 44, 64, 74, 88, 102]
    bars = "".join(
        f'<rect class="bar" style="animation-delay:{-i * .45:.2f}s" x="{4 + i * 22}" y="{134 - h}" width="14" height="{h}" rx="2"/>'
        for i, h in enumerate(heights))
    nodes = [(36, 18), (12, 66), (60, 66), (36, 118)]
    edges = [(0, 1), (0, 2), (1, 3), (2, 3), (1, 2)]
    epaths = [f"M{nodes[a][0]} {nodes[a][1]} L{nodes[b][0]} {nodes[b][1]}" for a, b in edges]
    agent_edges = "".join(f'<path class="flow" d="{p}"/>' for p in epaths)
    agent_packets = "".join(packet(p, t["green"], 1.8, i * .45, 3) for i, p in enumerate(epaths))
    particles = "".join(
        f'<circle class="float" style="animation-delay:{-i * 1.3:.1f}s" cx="{x}" cy="{y}" r="{r}" fill="{t["blue"]}" opacity=".35"/>'
        for i, (x, y, r) in enumerate([(560, 46, 2.5), (520, 250, 2), (600, 270, 3), (930, 30, 2), (590, 120, 1.8)]))
    body = f"""<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t['bg0']}"/><stop offset=".55" stop-color="{t['bg1']}"/><stop offset="1" stop-color="{t['bg2']}"/></linearGradient>
<linearGradient id="accent" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t['green']}"/><stop offset="1" stop-color="{t['blue']}"/></linearGradient>
<linearGradient id="name" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="{t['text']}"/><stop offset=".42" stop-color="{t['text']}"/><stop offset=".5" stop-color="{t['sky']}"/><stop offset=".58" stop-color="{t['text']}"/><stop offset="1" stop-color="{t['text']}"/>
<animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0;1 0" keyTimes="0;.35;1" dur="7s" repeatCount="indefinite"/></linearGradient>
<linearGradient id="barg" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{t['deep']}"/><stop offset="1" stop-color="{t['sky']}"/></linearGradient>
<linearGradient id="scanG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t['glow']}" stop-opacity="0"/><stop offset=".5" stop-color="{t['glow']}" stop-opacity=".35"/><stop offset="1" stop-color="{t['glow']}" stop-opacity="0"/></linearGradient>
<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="{t['grid']}" stroke-width=".7" opacity=".6"/></pattern>
<clipPath id="card"><rect width="960" height="300" rx="18"/></clipPath>
<clipPath id="dash"><rect x="-14" y="-14" width="182" height="176" rx="10"/></clipPath>
{''.join(clips)}
</defs>
<g clip-path="url(#card)"><rect width="960" height="300" fill="url(#bg)"/><rect x="600" width="360" height="300" fill="url(#grid)"/>{particles}</g>
<rect x="0.5" y="0.5" width="959" height="299" rx="18" fill="none" stroke="{t['border']}"/>
<rect x="56" y="52" width="56" height="5" rx="2.5" fill="url(#accent)"><animate attributeName="width" values="56;96;56" dur="5s" repeatCount="indefinite"/></rect>
<text x="54" y="126" fill="url(#name)" font-size="60" font-weight="800" letter-spacing="-1">Ludovic Delot</text>
<text x="58" y="180" font-family="{MONO}" font-size="25.5" font-weight="700" fill="{t['green']}">❯</text>
{''.join(roles)}
<text x="58" y="226" fill="{t['muted']}" font-size="17.5" font-weight="600">Power BI · DAX · SQL · Python · dbt · BigQuery · LLM agents</text>
<text x="58" y="258" fill="{t['dim']}" font-size="15" font-family="{MONO}">4.5+ years in data · LVMH · Groupe SEB · Mexico City</text>
<g transform="translate(632 70)">
<rect x="-14" y="-14" width="182" height="176" rx="10" fill="{t['card2']}" stroke="{t['border']}"/>
<g clip-path="url(#dash)"><rect class="scan" x="-60" y="-14" width="60" height="176" fill="url(#scanG)"/></g>
<rect x="0" y="0" width="38" height="5" rx="2.5" fill="{t['blue']}" opacity=".85"/><rect x="0" y="11" width="22" height="4" rx="2" fill="{t['deep']}"/>
<circle cx="146" cy="5" r="4" fill="{t['green']}"><animate attributeName="opacity" values="1;.2;1" dur="1.6s" repeatCount="indefinite"/></circle>
<g fill="url(#barg)">{bars}</g>
<path class="trend" d="M11 88 L33 76 L55 80 L77 58 L99 48 L121 34 L143 20" fill="none" stroke="{t['green']}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
<text x="0" y="154" fill="{t['dim']}" font-size="11" font-family="{MONO}">sell-out · MTD · YoY</text>
</g>
<g transform="translate(834 70)">
<rect x="-14" y="-14" width="100" height="176" rx="10" fill="{t['card2']}" stroke="{t['border']}"/>
<g stroke="{t['blue']}" stroke-width="1.5" fill="none" opacity=".8">{agent_edges}</g>
{agent_packets}
<circle class="pulse" cx="36" cy="18" r="9" fill="{t['green']}"/><circle class="pulse" style="animation-delay:.6s" cx="12" cy="66" r="7" fill="{t['blue']}"/>
<circle class="pulse" style="animation-delay:1.2s" cx="60" cy="66" r="7" fill="{t['blue']}"/><circle class="pulse" style="animation-delay:1.8s" cx="36" cy="118" r="9" fill="{t['sky']}"/>
<text x="36" y="154" fill="{t['dim']}" font-size="11" text-anchor="middle" font-family="{MONO}">agents</text>
</g>"""
    return svg(960, 300, "Ludovic Delot",
               "Business Intelligence Analyst, Power BI Developer, Data Analyst and AI Developer with 4.5+ years in "
               "data. Power BI, DAX, SQL, Python, dbt, BigQuery and LLM agents.", body, style)


# =========================================================================== impact (bento)
def ico_dash(t):
    bars = "".join(
        f'<rect x="{6 + i * 9}" y="{30 - h}" width="6" height="{h}" rx="1.5" fill="{t["blue"]}">'
        f'<animate attributeName="height" values="{h};{h * .45:.1f};{h}" dur="2.2s" begin="{-i * .35:.2f}s" repeatCount="indefinite"/>'
        f'<animate attributeName="y" values="{30 - h};{30 - h * .45:.1f};{30 - h}" dur="2.2s" begin="{-i * .35:.2f}s" repeatCount="indefinite"/></rect>'
        for i, h in enumerate([10, 16, 12, 20]))
    return f'<rect x="0" y="0" width="44" height="36" rx="7" fill="none" stroke="{t["border"]}" stroke-width="1.6"/>{bars}'


def ico_gear(t):
    return (f'<g transform="translate(18 18)"><g class="spin"><circle r="13" fill="none" stroke="{t["green"]}" stroke-width="6" stroke-dasharray="4.2 2.6"/>'
            f'<circle r="9" fill="{t["card"]}" stroke="{t["green"]}" stroke-width="2.4"/></g>'
            f'<circle r="3.5" fill="{t["green"]}"/></g>'
            f'<g transform="translate(34 30)"><g class="spin" style="animation-direction:reverse;animation-duration:5s">'
            f'<circle r="7" fill="none" stroke="{t["blue"]}" stroke-width="4" stroke-dasharray="2.6 2"/>'
            f'<circle r="4.5" fill="{t["card"]}" stroke="{t["blue"]}" stroke-width="1.6"/></g></g>')


def globe(t, r=58):
    mer = "".join(
        f'<ellipse cx="0" cy="0" rx="{r}" ry="{r}" fill="none" stroke="{t["blue"]}" stroke-width="1.2" opacity=".55">'
        f'<animate attributeName="rx" values="{r};0;{r}" dur="9s" begin="{-k * 2.25}s" repeatCount="indefinite"/></ellipse>'
        for k in range(4))
    lat = "".join(
        f'<ellipse cx="0" cy="{y}" rx="{(r * r - y * y) ** .5:.1f}" ry="{6 - abs(y) / 12:.1f}" fill="none" stroke="{t["blue"]}" stroke-width="1" opacity=".4"/>'
        for y in (-34, -12, 12, 34))
    pins = "".join(
        f'<g transform="translate({x} {y})"><circle r="9" fill="{c}" opacity=".25"><animate attributeName="r" values="3;12;3" dur="2.4s" begin="{b}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values=".45;0;.45" dur="2.4s" begin="{b}s" repeatCount="indefinite"/></circle><circle r="3.6" fill="{c}"/></g>'
        for x, y, c, b in [(-30, -18, t["green"], 0), (16, -30, t["sky"], .6), (28, 6, t["green"], 1.2), (-10, 24, t["sky"], 1.8), (-38, 14, t["blue"], .9)])
    arcs = (f'<path class="flow" d="M-30 -18 Q -8 -50 16 -30" fill="none" stroke="{t["green"]}" stroke-width="1.6"/>'
            f'<path class="flow" d="M16 -30 Q 40 -14 28 6" fill="none" stroke="{t["green"]}" stroke-width="1.6"/>'
            f'<path class="flow" d="M-38 14 Q -24 36 -10 24" fill="none" stroke="{t["green"]}" stroke-width="1.6"/>')
    return f'<circle r="{r}" fill="{t["card2"]}" stroke="{t["blue"]}" stroke-width="1.6"/>{lat}{mer}{arcs}{pins}'


def impact(t):
    style = """.d1{animation-delay:.1s}.d2{animation-delay:.2s}.d3{animation-delay:.3s}.d4{animation-delay:.4s}.d5{animation-delay:.5s}
.seg{transform-box:fill-box;transform-origin:left;animation:grow-x .9s cubic-bezier(.2,.8,.3,1) both}
.s1{animation-delay:.5s}.s2{animation-delay:.8s}.s3{animation-delay:1.1s}.s4{animation-delay:1.4s}
.cell{animation:twinkle 3s ease-in-out infinite}
@keyframes grow-x{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes twinkle{0%,100%{opacity:.25}50%{opacity:1}}"""

    def tile(x, y, w, h, cls, inner):
        return (f'<g transform="translate({x} {y})"><g class="rise {cls}">'
                f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="16" fill="{t["card"]}" stroke="{t["border"]}"/>'
                f'{inner}</g></g>')

    def kicker(x, y, s, color):
        return (f'<rect class="glow" x="{x}" y="{y - 13}" width="26" height="5" rx="2.5" fill="{color}"/>'
                f'<text x="{x + 36}" y="{y - 7}" font-size="12.5" font-weight="700" letter-spacing="1.3" '
                f'fill="{t["dim"]}" font-family="{MONO}">{esc(s)}</text>')

    def big(x, y, s, size=56):
        return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="800" letter-spacing="-1.5" fill="url(#num)">{esc(s)}</text>'

    def label(x, y, s, size=17, color=None, weight=700, anchor="start"):
        return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color or t["text"]}" '
                f'text-anchor="{anchor}">{esc(s)}</text>')

    W = 412
    segs = [(0.00, 0.39, t["deep"]), (0.39, 0.50, t["sky"]), (0.50, 0.61, t["blue"]), (0.61, 1.00, t["green"])]
    tl = "".join(f'<rect class="seg s{i + 1}" x="{28 + a * W:.1f}" y="150" width="{(b - a) * W - 3:.1f}" height="12" rx="6" fill="{c}"/>'
                 for i, (a, b, c) in enumerate(segs))
    tl += (label(28, 186, "BSc in BI", 13, t["muted"], 500)
           + label(int(28 + .39 * W), 186, "SEB", 13, t["muted"], 500)
           + label(int(28 + .50 * W), 186, "LIV·EGADE", 13, t["muted"], 500)
           + label(int(28 + .80 * W), 186, "LVMH", 13, t["text"], 700, "middle")
           + label(28 + W, 186, "now", 13, t["muted"], 500, "end")
           + f'<text x="{int(28 + .39 * W)}" y="140" font-size="12" fill="{t["dim"]}" font-family="{MONO}">2024</text>'
           + packet(f"M28 156 H{28 + W - 6}", t["text"], 3.2, 1.6, 3)
           + f'<circle class="pulse" cx="{28 + W - 4}" cy="156" r="7" fill="{t["green"]}"/>')
    a = tile(0, 0, 470, 214, "", kicker(28, 40, "YEARS IN DATA", t["green"]) + big(26, 104, "4.5+", 64)
             + label(176, 78, "years in data", 21) + label(176, 102, "BI degree + 4 data roles", 15, t["muted"], 500) + tl)

    b = tile(482, 0, 230, 214, "d1", kicker(24, 40, "DASHBOARDS", t["blue"])
             + f'<g transform="translate(164 18)">{ico_dash(t)}</g>'
             + big(22, 116, "90+", 60) + label(24, 146, "dashboards", 18) + label(24, 168, "developed", 18)
             + label(24, 192, "Power BI · Tableau", 13.5, t["muted"], 500))

    c = tile(724, 0, 236, 214, "d2", kicker(24, 40, "AUTOMATIONS", t["green"])
             + f'<g transform="translate(170 24)">{ico_gear(t)}</g>'
             + big(22, 116, "115+", 60) + label(24, 146, "automations", 18) + label(24, 168, "developed", 18)
             + label(24, 192, "Python ETL · RPA · AI", 13.5, t["muted"], 500))

    y2, h2 = 226, 176
    d = tile(0, y2, 470, h2, "d3", kicker(28, 40, "GLOBAL IMPACT", t["sky"])
             + big(26, 104, "30", 60) + label(104, 84, "countries", 21) + label(104, 104, "reached by my reporting", 14, t["muted"], 500)
             + label(28, 136, "Worldwide & EMEA models", 16)
             + label(28, 158, "Built from Mexico · France · Spain", 13.5, t["muted"], 500)
             + f'<g transform="translate(386 90)">{globe(t, 62)}</g>')

    cells = ""
    for r in range(4):
        for k in range(7):
            cells += (f'<rect class="cell" style="animation-delay:{-((r * 7 + k) * 37 % 30) / 10:.1f}s" x="{126 + k * 13}" y="{24 + r * 13}" '
                      f'width="10" height="10" rx="2" fill="{t["blue"] if (r + k) % 3 else t["green"]}"/>')
    e = tile(482, y2, 230, h2, "d4", kicker(24, 40, "CPFR", t["green"]) + cells
             + big(22, 120, "25K+", 50) + label(24, 146, "SKU–store combinations", 14.5)
             + label(24, 166, "across 300+ stores", 13.5, t["muted"], 500))

    rows = "".join(f'<rect x="150" y="{30 + i * 14}" width="{[44, 34, 52][i]}" height="9" rx="3" fill="{t["blue"]}" opacity=".7">'
                   f'<animate attributeName="width" values="{[44, 34, 52][i]};{[30, 52, 40][i]};{[44, 34, 52][i]}" dur="3s" begin="{i * .4}s" repeatCount="indefinite"/></rect>'
                   for i in range(3))
    f = tile(724, y2, 236, h2, "d5", kicker(24, 40, "SHIPPED", t["blue"])
             + f'<rect x="140" y="18" width="72" height="62" rx="8" fill="none" stroke="{t["border"]}" stroke-width="1.6"/>{rows}'
             + big(22, 120, "2", 50) + label(56, 112, "Power BI", 18) + label(24, 146, "custom visuals", 14.5)
             + label(24, 166, "public on GitHub", 13.5, t["muted"], 500))

    return svg(960, 402, "Impact at a glance",
               "4.5+ years in data; 90+ dashboards developed; 115+ automations developed; reporting that reaches 30 "
               "countries through worldwide and EMEA models, built from Mexico, France and Spain; 25,000+ SKU-store "
               "combinations analyzed across 300+ stores; two Power BI custom visuals published.",
               "\n".join([f"<defs>{num_grad(t)}</defs>", a, b, c, d, e, f]), style)


# =========================================================================== pipeline
STAGES = [
    ("01 · SOURCES", "Raw data", "GCP · SharePoint", "retailer files · APIs"),
    ("02 · TRANSFORM", "Python ETL", "pandas · SQL · dbt", "data-quality checks"),
    ("03 · MODEL", "Semantic model", "DAX · TMDL · star", "PBIP in Git"),
    ("04 · DECIDE", "Power BI", "governed KPIs", "self-service reports"),
    ("05 · AUTOMATE", "AI layer", "agents · skills · MCP", "docs · checks"),
]


def stage_icon(i, t):
    if i == 0:
        return (f'<ellipse cx="14" cy="6" rx="12" ry="5" fill="none" stroke="{t["blue"]}" stroke-width="2"/>'
                f'<path d="M2 6 V24 A12 5 0 0 0 26 24 V6" fill="none" stroke="{t["blue"]}" stroke-width="2"/>'
                f'<path d="M2 15 A12 5 0 0 0 26 15" fill="none" stroke="{t["blue"]}" stroke-width="2"/>'
                f'<circle cx="14" cy="6" r="2" fill="{t["green"]}"><animate attributeName="opacity" values="1;.2;1" dur="1.4s" repeatCount="indefinite"/></circle>')
    if i == 1:
        return (f'<path d="M1 3 H27 L17 15 V26 L11 22 V15 Z" fill="none" stroke="{t["blue"]}" stroke-width="2" stroke-linejoin="round"/>'
                f'<circle cx="14" cy="0" r="2.4" fill="{t["green"]}"><animate attributeName="cy" values="0;24" dur="1.4s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values="1;1;0" dur="1.4s" repeatCount="indefinite"/></circle>')
    if i == 2:
        return (f'<g stroke="{t["blue"]}" stroke-width="1.8"><line x1="14" y1="14" x2="14" y2="1"/><line x1="14" y1="14" x2="27" y2="14"/>'
                f'<line x1="14" y1="14" x2="14" y2="27"/><line x1="14" y1="14" x2="1" y2="14"/></g>'
                f'<rect class="pulse" x="8" y="8" width="12" height="12" rx="3" fill="{t["green"]}"/>'
                + "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="{t["blue"]}"/>' for x, y in [(14, 1), (27, 14), (14, 27), (1, 14)]))
    if i == 3:
        return "".join(f'<rect x="{2 + k * 7}" y="{26 - h}" width="5" height="{h}" rx="1" fill="{t["blue"]}">'
                       f'<animate attributeName="height" values="{h};{h * .5:.0f};{h}" dur="2s" begin="{-k * .3:.1f}s" repeatCount="indefinite"/>'
                       f'<animate attributeName="y" values="{26 - h};{26 - h * .5:.0f};{26 - h}" dur="2s" begin="{-k * .3:.1f}s" repeatCount="indefinite"/></rect>'
                       for k, h in enumerate([10, 18, 14, 24]))
    return (f'<path class="pulse" d="M14 2 l3.2 7.8 7.8 3.2 -7.8 3.2 -3.2 7.8 -3.2 -7.8 -7.8 -3.2 7.8 -3.2z" fill="{t["green"]}"/>'
            f'<circle class="pulse" style="animation-delay:1s" cx="25" cy="24" r="3" fill="{t["blue"]}"/>')


def pipeline(t):
    parts = [f'<path class="flow" d="M96 122 H864" stroke="{t["blue"]}" stroke-width="2" fill="none" opacity=".75"/>']
    for k in range(3):
        parts.append(packet("M96 122 H864", t["green"], 4.2, k * 1.4, 5))
    for i, (kick, title, l1, l2) in enumerate(STAGES):
        hl = i == 2
        parts.append(f"""<g transform="translate({i * 193} 0)"><g class="rise" style="animation-delay:{i * .12:.2f}s">
<rect x="1" y="20" width="182" height="200" rx="14" fill="{t['card']}" stroke="{t['blue'] if hl else t['border']}" stroke-width="{1.6 if hl else 1}"/>
<g transform="translate(140 36)">{stage_icon(i, t)}</g>
<text x="18" y="52" font-size="12.5" font-weight="700" fill="{t['green']}" font-family="{MONO}">{esc(kick)}</text>
<text x="18" y="86" font-size="20" font-weight="800" fill="{t['text']}">{esc(title)}</text>
<text x="18" y="172" font-size="14.5" fill="{t['muted']}">{esc(l1)}</text>
<text x="18" y="194" font-size="14.5" fill="{t['muted']}">{esc(l2)}</text>
</g></g>""")
    return svg(960, 224, "How I build data products",
               "Five stages: raw sources; Python ETL with data-quality checks; a semantic model in DAX and TMDL "
               "versioned as PBIP in Git; Power BI with governed KPIs; and an AI layer of agents, skills and MCP.",
               "\n".join(parts))


# =========================================================================== project card illustrations
def ill_list(t):
    out = ""
    for i in range(3):
        y = 26 + i * 34
        out += (f'<rect x="0" y="{y}" width="150" height="26" rx="6" fill="{t["card"]}" stroke="{t["border"]}"/>'
                f'<text x="12" y="{y + 18}" font-size="13" font-weight="700" fill="{t["blue"]}">{i + 1}</text>')
    for i, lab in enumerate(["Region", "Brand", "Product"]):
        y = 26 + i * 34
        move = ""
        if i < 2:
            d = 34 if i == 0 else -34
            move = (f'<animateTransform attributeName="transform" type="translate" values="0 0;0 0;0 {d};0 {d};0 0" '
                    f'keyTimes="0;.35;.45;.85;.95" dur="5s" repeatCount="indefinite"/>')
        out += (f'<g>{move}<text x="30" y="{y + 18}" font-size="13" fill="{t["text"]}">{lab}</text>'
                f'<text x="132" y="{y + 18}" font-size="12" fill="{t["green"]}" text-anchor="middle">⇅</text></g>')
    return out


def ill_matrix(t):
    cells = "".join(
        f'<rect x="{c * 26 - 52}" y="{r * 20 - 40}" width="22" height="16" rx="3" fill="{t["blue"] if r == 0 or c == 0 else t["deep"]}" '
        f'opacity="{1 if r == 0 or c == 0 else .5}"/>'
        for r in range(4) for c in range(4))
    return (f'<g transform="translate(68 80)"><g>{cells}<animateTransform attributeName="transform" type="rotate" '
            f'values="0;0;-90;-90;0" keyTimes="0;.3;.45;.8;.95" dur="5s" repeatCount="indefinite"/></g></g>'
            f'<g transform="translate(160 80)"><path class="spin" d="M-11 0 a11 11 0 1 1 3 7.7" fill="none" stroke="{t["green"]}" stroke-width="2.5"/></g>')


def ill_doc(t):
    widths = [70, 54, 64, 40, 60]
    lines = "".join(
        f'<rect x="14" y="{40 + i * 14}" width="{w}" height="5" rx="2.5" fill="{t["muted"]}" opacity=".6">'
        f'<animate attributeName="width" values="0;{w};{w};0" keyTimes="0;.25;.85;1" dur="4s" begin="{i * .3}s" repeatCount="indefinite"/></rect>'
        for i, w in enumerate(widths))
    return (f'<rect x="0" y="22" width="100" height="112" rx="8" fill="{t["card"]}" stroke="{t["border"]}"/>{lines}'
            f'<g stroke="{t["blue"]}" stroke-width="1.6"><path class="flow" d="M124 44 L150 78"/><path class="flow" d="M124 112 L150 78"/></g>'
            + packet("M124 44 L150 78", t["green"], 1.6, 0, 3) + packet("M124 112 L150 78", t["green"], 1.6, .8, 3)
            + f'<circle cx="124" cy="44" r="7" fill="{t["blue"]}"/><circle cx="124" cy="112" r="7" fill="{t["blue"]}"/>'
            f'<circle class="pulse" cx="150" cy="78" r="9" fill="{t["green"]}"/>')


def ill_pages(t):
    out = ""
    for i in range(3):
        x, y = i * 22, 22 + i * 16
        out += (f'<g><animateTransform attributeName="transform" type="translate" values="0 0;{i * 6} {-i * 4};0 0" '
                f'dur="3.6s" repeatCount="indefinite"/>'
                f'<rect x="{x}" y="{y}" width="110" height="66" rx="6" fill="{t["card"]}" stroke="{t["border"]}"/>'
                f'<rect x="{x + 10}" y="{y + 10}" width="40" height="22" rx="3" fill="{t["blue"]}" opacity=".55"/>'
                f'<rect x="{x + 56}" y="{y + 10}" width="44" height="5" rx="2" fill="{t["muted"]}" opacity=".5"/>'
                f'<rect x="{x + 56}" y="{y + 21}" width="34" height="5" rx="2" fill="{t["muted"]}" opacity=".5"/></g>')
    langs = "".join(f'<text x="{20 + k * 30}" y="150" font-size="12" font-family="{MONO}" fill="{t["green"]}" text-anchor="middle">{lang}'
                    f'<animate attributeName="opacity" values=".3;1;.3" dur="2.4s" begin="{k * .6}s" repeatCount="indefinite"/></text>'
                    for k, lang in enumerate(["EN", "ES", "IT", "FR"]))
    return out + langs


def ill_star(t):
    dims = [(80, 22), (150, 78), (80, 134), (10, 78)]
    lines = "".join(f'<path class="flow" d="M{x} {y} L80 78" stroke="{t["blue"]}" stroke-width="1.6"/>' for x, y in dims)
    pk = "".join(packet(f"M{x} {y} L80 78", t["green"], 1.8, i * .45, 3) for i, (x, y) in enumerate(dims))
    boxes = "".join(f'<rect x="{x - 22}" y="{y - 12}" width="44" height="24" rx="5" fill="{t["card"]}" stroke="{t["border"]}"/>'
                    f'<text x="{x}" y="{y + 4}" font-size="10" text-anchor="middle" fill="{t["muted"]}" font-family="{MONO}">dim</text>' for x, y in dims)
    return (lines + pk + boxes + f'<rect class="pulse" x="52" y="62" width="56" height="32" rx="6" fill="{t["blue"]}"/>'
            f'<text x="80" y="83" font-size="12" font-weight="700" text-anchor="middle" fill="#ffffff" font-family="{MONO}">fact</text>')


def ill_dag(t):
    boxes = [(0, 40, "stg"), (0, 92, "stg"), (58, 40, "int"), (58, 92, "int"), (116, 66, "mart")]
    paths = ["M46 53 L58 53", "M46 105 L58 105", "M104 53 L116 79", "M104 105 L116 79"]
    out = "".join(f'<path class="flow" d="{p}" stroke="{t["blue"]}" stroke-width="1.6"/>' for p in paths)
    out += "".join(packet(p, t["green"], 1.2, i * .3, 2.6) for i, p in enumerate(paths))
    for x, y, n in boxes:
        hl = n == "mart"
        out += (f'<rect x="{x}" y="{y}" width="46" height="26" rx="6" fill="{t["blue"] if hl else t["card"]}" stroke="{t["border"]}"/>'
                f'<text x="{x + 23}" y="{y + 17}" font-size="10.5" text-anchor="middle" fill="{"#ffffff" if hl else t["muted"]}" font-family="{MONO}">{n}</text>')
    return out + f'<text class="pulse" x="139" y="118" font-size="16" text-anchor="middle" fill="{t["green"]}">✓</text>'


def ill_agents(t):
    pts = [(80, 24), (24, 72), (136, 72), (52, 128), (108, 128)]
    edges = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 4), (1, 2), (0, 3)]
    paths = [f"M{pts[a][0]} {pts[a][1]} L{pts[b][0]} {pts[b][1]}" for a, b in edges]
    out = "".join(f'<path class="flow" d="{p}" stroke="{t["blue"]}" stroke-width="1.5"/>' for p in paths)
    out += "".join(packet(p, t["green"], 1.6, i * .35, 3) for i, p in enumerate(paths))
    cols = [t["green"], t["blue"], t["blue"], t["sky"], t["sky"]]
    return out + "".join(f'<circle class="pulse" style="animation-delay:{i * .5}s" cx="{x}" cy="{y}" r="{10 if i == 0 else 8}" fill="{cols[i]}"/>'
                         for i, (x, y) in enumerate(pts))


def ill_gate(t):
    out = ""
    for i, ok in enumerate([True, True, False]):
        y = 40 + i * 30
        stroke = t["border"] if ok else t["red"]
        out += (f'<g><animateTransform attributeName="transform" type="translate" values="-20 0;0 0;0 0" keyTimes="0;.2;1" dur="4.5s" '
                f'begin="{i * .5}s" repeatCount="indefinite"/>'
                f'<rect x="0" y="{y}" width="64" height="20" rx="5" fill="{t["card"]}" stroke="{stroke}"/>'
                f'<rect x="8" y="{y + 8}" width="{[40, 30, 46][i]}" height="4" rx="2" fill="{t["muted"]}" opacity=".5"/></g>'
                f'<text x="128" y="{y + 18}" font-size="22" font-weight="800" fill="{t["green"] if ok else t["red"]}" text-anchor="middle" opacity="0">{"✓" if ok else "✕"}'
                f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;.25;.32;.9;1" dur="4.5s" begin="{i * .5}s" repeatCount="indefinite"/></text>')
    return out + (f'<rect x="84" y="34" width="12" height="92" rx="4" fill="{t["blue"]}"/>'
                  f'<rect x="84" y="34" width="12" height="18" rx="4" fill="{t["sky"]}"><animate attributeName="y" values="34;108;34" dur="2.2s" repeatCount="indefinite"/></rect>')


def ill_hub(t):
    sats = [(20, 40), (20, 116), (140, 40), (140, 116), (80, 142)]
    out = "".join(f'<path class="flow" d="M80 78 L{x} {y}" stroke="{t["blue"]}" stroke-width="1.5"/>' for x, y in sats)
    out += "".join(packet(f"M80 78 L{x} {y}", t["green"], 1.5, i * .3, 2.8) for i, (x, y) in enumerate(sats))
    out += "".join(f'<rect x="{x - 14}" y="{y - 10}" width="28" height="20" rx="4" fill="{t["card"]}" stroke="{t["border"]}">'
                   f'<animate attributeName="stroke" values="{t["border"]};{t["green"]};{t["border"]}" dur="2.5s" begin="{i * .5}s" repeatCount="indefinite"/></rect>'
                   for i, (x, y) in enumerate(sats))
    return out + (f'<circle class="pulse" cx="80" cy="78" r="18" fill="{t["green"]}"/>'
                  f'<text x="80" y="83" font-size="11" font-weight="800" text-anchor="middle" fill="#ffffff" font-family="{MONO}">MOC</text>')


def ill_mcp(t):
    return (f'<rect x="0" y="50" width="62" height="56" rx="10" fill="{t["card"]}" stroke="{t["border"]}"/>'
            f'<text x="31" y="84" font-size="13" font-weight="800" text-anchor="middle" fill="{t["blue"]}" font-family="{MONO}">LLM</text>'
            f'<g stroke="{t["green"]}" stroke-width="2" fill="none"><path class="flow" d="M62 78 H96 V47"/><path class="flow" d="M62 78 H96 V109"/></g>'
            + packet("M62 78 H96 V47 H110", t["sky"], 1.8, 0, 3.2) + packet("M110 109 H96 V78 H62", t["green"], 1.8, .9, 3.2)
            + f'<rect x="96" y="30" width="66" height="34" rx="7" fill="{t["card"]}" stroke="{t["border"]}"/>'
            f'<rect x="96" y="92" width="66" height="34" rx="7" fill="{t["card"]}" stroke="{t["border"]}"/>'
            f'<text x="129" y="51" font-size="10" text-anchor="middle" fill="{t["muted"]}" font-family="{MONO}">search</text>'
            f'<text x="129" y="113" font-size="10" text-anchor="middle" fill="{t["muted"]}" font-family="{MONO}">get</text>')


CARDS = [
    ("fp-selector", "POWER BI CUSTOM VISUAL", ["Pick fields in", "the order you mean"], ill_list),
    ("transpose-matrix", "POWER BI CUSTOM VISUAL", ["Rows ⇄ columns", "in one click"], ill_matrix),
    ("pbip-doc", "CLAUDE CODE SKILL · PBIP", ["TMDL + PBIR", "→ living docs"], ill_doc),
    ("pbip-manual", "CLAUDE CODE SKILL · PBIP", ["Report → PDF", "user manual"], ill_pages),
    ("star-schema", "SQL · DIMENSIONAL MODEL", ["3.19× freight", "error, caught"], ill_star),
    ("ecom-dbt", "BIGQUERY + DBT · BUILDING", ["staging → marts", "tested KPIs"], ill_dag),
    ("agent-network", "MULTI-AGENT SYSTEM", ["Demand → deals", "→ purchase orders"], ill_agents),
    ("ats-tailor", "AGENT SKILL · VALIDATOR", ["No claim without", "evidence"], ill_gate),
    ("moc-memory", "AGENT SKILL · AI MEMORY", ["Vault → durable", "agent memory"], ill_hub),
    ("mcp-server", "MCP SERVER · TYPESCRIPT", ["Tools an LLM", "can call"], ill_mcp),
]


def card(t, kicker, lines, ill):
    body = (f'<rect x="0.5" y="0.5" width="479" height="179" rx="14" fill="{t["card2"]}" stroke="{t["border"]}"/>'
            f'<rect class="glow" x="26" y="28" width="30" height="5" rx="2.5" fill="{t["green"]}"/>'
            f'<text x="26" y="62" font-size="13.5" font-weight="700" letter-spacing="1.2" fill="{t["blue"]}" font-family="{MONO}">{esc(kicker)}</text>'
            f'<text x="26" y="108" font-size="27" font-weight="800" fill="{t["text"]}" letter-spacing="-.4">{esc(lines[0])}</text>'
            f'<text x="26" y="142" font-size="27" font-weight="800" fill="{t["text"]}" letter-spacing="-.4">{esc(lines[1])}</text>'
            f'<g transform="translate(298 14)">{ill(t)}</g>')
    return svg(480, 180, f"{kicker}: {' '.join(lines)}", f"{kicker}. {' '.join(lines)}.", body)


# =========================================================================== closing banner
def closing(t):
    spark = "M0 60 L40 52 L80 56 L120 36 L160 40 L200 22 L240 26 L280 8"
    body = f"""<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t['bg0']}"/><stop offset=".6" stop-color="{t['bg1']}"/><stop offset="1" stop-color="{t['bg2']}"/></linearGradient>
<linearGradient id="area" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t['green']}" stop-opacity=".35"/><stop offset="1" stop-color="{t['green']}" stop-opacity="0"/></linearGradient>
<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="{t['grid']}" stroke-width=".7" opacity=".55"/></pattern>
<clipPath id="card"><rect width="960" height="200" rx="18"/></clipPath>
</defs>
<g clip-path="url(#card)"><rect width="960" height="200" fill="url(#bg)"/><rect x="620" width="340" height="200" fill="url(#grid)" opacity=".8"/></g>
<rect x="0.5" y="0.5" width="959" height="199" rx="18" fill="none" stroke="{t['border']}"/>
<text x="56" y="84" font-size="38" font-weight="800" fill="{t['text']}" letter-spacing="-.8">Let's turn data into decisions.</text>
<text x="58" y="122" font-size="17" fill="{t['muted']}">Always happy to talk BI, analytics engineering and AI.</text>
<text x="58" y="158" font-size="15" font-family="{MONO}" fill="{t['green']}">❯ <tspan fill="{t['dim']}">linkedin.com/in/delot</tspan></text>
<rect class="blink" x="282" y="146" width="8" height="15" rx="1" fill="{t['green']}"/>
<g transform="translate(640 60)">
<path d="{spark} V90 H0 Z" fill="url(#area)"/>
<path d="{spark}" fill="none" stroke="{t['green']}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="320">
<animate attributeName="stroke-dashoffset" values="320;0;0" keyTimes="0;.5;1" dur="5s" repeatCount="indefinite"/></path>
{packet(spark, t['text'], 5, 0, 4)}
<circle class="pulse" cx="280" cy="8" r="6" fill="{t['green']}"/>
</g>"""
    return svg(960, 200, "Let's turn data into decisions", "Closing banner with a contact line and an animated trend line.", body)


# =========================================================================== section icons (theme-neutral)
ICON_BLUE, ICON_GREEN = "#2f81f7", "#2da44e"


def icon(name):
    b, g = ICON_BLUE, ICON_GREEN
    shapes = {
        "about": (f'<rect x="2" y="5" width="28" height="22" rx="5" fill="none" stroke="{b}" stroke-width="2.4"/>'
                  f'<path d="M8 12 l4 4 -4 4" fill="none" stroke="{g}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'
                  f'<rect class="blink" x="15" y="18" width="9" height="2.6" rx="1.3" fill="{g}"/>'),
        "impact": f'<path class="pulse" d="M18 2 L6 18 H15 L13 30 L26 13 H17 Z" fill="{g}" stroke="{g}" stroke-width="1.4" stroke-linejoin="round"/>',
        "work": "".join(f'<rect x="{2 + (k % 2) * 15}" y="{2 + (k // 2) * 15}" width="13" height="13" rx="3" fill="{b if k != 3 else g}">'
                        f'<animate attributeName="opacity" values=".35;1;.35" dur="2.4s" begin="{k * .6}s" repeatCount="indefinite"/></rect>' for k in range(4)),
        "stack": "".join(f'<path d="M16 {6 + k * 7} L29 {12 + k * 7} L16 {18 + k * 7} L3 {12 + k * 7} Z" fill="{[g, b, b][k]}" opacity="{[1, .75, .5][k]}">'
                         f'<animateTransform attributeName="transform" type="translate" values="0 0;0 {-2 + k};0 0" dur="2.6s" begin="{k * .3}s" repeatCount="indefinite"/></path>'
                         for k in (2, 1, 0)),
        "how": (f'<path class="flow" d="M5 16 H27" stroke="{b}" stroke-width="2.4"/>'
                f'<circle cx="5" cy="16" r="4" fill="{b}"/><circle cx="16" cy="16" r="4" fill="{b}"/><circle cx="27" cy="16" r="4" fill="{g}"/>'
                + packet("M5 16 H27", g, 1.6, 0, 2.6)),
        "experience": (f'<rect x="3" y="10" width="26" height="18" rx="4" fill="none" stroke="{b}" stroke-width="2.4"/>'
                       f'<path d="M11 10 V6 a2 2 0 0 1 2 -2 h6 a2 2 0 0 1 2 2 V10" fill="none" stroke="{b}" stroke-width="2.4"/>'
                       f'<rect class="pulse" x="13" y="16" width="6" height="5" rx="1.5" fill="{g}"/>'),
        "education": (f'<path d="M16 5 L30 12 L16 19 L2 12 Z" fill="{b}"/><path d="M8 15 V22 C8 26 24 26 24 22 V15" fill="none" stroke="{b}" stroke-width="2.4"/>'
                      f'<path d="M28 12 V21" stroke="{g}" stroke-width="2.4"/><circle class="pulse" cx="28" cy="23" r="2.6" fill="{g}"/>'),
        "activity": (f'<path d="M2 17 H8 L11 8 L16 26 L20 13 L23 17 H30" fill="none" stroke="{g}" stroke-width="2.6" stroke-linecap="round" '
                     f'stroke-linejoin="round" stroke-dasharray="60"><animate attributeName="stroke-dashoffset" values="60;0;0" keyTimes="0;.5;1" dur="2.4s" repeatCount="indefinite"/></path>'),
    }
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" role="img" aria-label="{name} icon">'
            f'<style>{COMMON}{REDUCED}</style>{shapes[name]}</svg>\n')


def main():
    for name, t in THEMES.items():
        out = ROOT / "assets" / name
        (out / "cards").mkdir(parents=True, exist_ok=True)
        (out / "banner.svg").write_text(banner(t), encoding="utf-8")
        (out / "impact.svg").write_text(impact(t), encoding="utf-8")
        (out / "pipeline.svg").write_text(pipeline(t), encoding="utf-8")
        (out / "closing.svg").write_text(closing(t), encoding="utf-8")
        for slug, kicker, lines, ill in CARDS:
            (out / "cards" / f"{slug}.svg").write_text(card(t, kicker, lines, ill), encoding="utf-8")
        old = out / "footer.svg"
        if old.exists():
            old.unlink()
    icons = ROOT / "assets" / "icons"
    icons.mkdir(parents=True, exist_ok=True)
    for n in ["about", "impact", "work", "stack", "how", "experience", "education", "activity"]:
        (icons / f"{n}.svg").write_text(icon(n), encoding="utf-8")
    print("Built assets/dark, assets/light and assets/icons")


if __name__ == "__main__":
    main()
