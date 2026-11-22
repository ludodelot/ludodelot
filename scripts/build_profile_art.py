"""Build every themed SVG used by the profile README.

Writes assets/dark/*.svg and assets/light/*.svg so the README can switch
images with <picture> and prefers-color-scheme. Text inside SVGs is sized for
GitHub's ~830 px README column; anything a recruiter or crawler must read
also lives as plain Markdown in README.md.

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
        "blue": "#62b0ef", "sky": "#8bd5ff", "deep": "#1d5f98", "green": "#39d353",
        "num0": "#f4f8fc", "num1": "#8bd5ff",
    },
    "light": {
        "bg0": "#ffffff", "bg1": "#f1f6fd", "bg2": "#dcebfb",
        "card": "#ffffff", "card2": "#f6f8fa", "border": "#d0d7de", "grid": "#c9dcf2",
        "text": "#1f2328", "muted": "#59636e", "dim": "#6e7781",
        "blue": "#0969da", "sky": "#218bff", "deep": "#80b8f5", "green": "#1a7f37",
        "num0": "#0b1f3f", "num1": "#0969da",
    },
}

REDUCED = "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(w, h, title, desc, body, style=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" '
        f'aria-labelledby="title desc" font-family="{SANS}">\n'
        f'<title id="title">{esc(title)}</title>\n<desc id="desc">{esc(desc)}</desc>\n'
        f"<style>{style}{REDUCED}</style>\n{body}\n</svg>\n"
    )


# --------------------------------------------------------------------------- banner
ROLES = ["Business Intelligence Analyst", "Power BI Developer", "Data Analyst", "AI Developer"]


def banner(t):
    cycle = 3.2 * len(ROLES)
    clips, roles = [], []
    for i, role in enumerate(ROLES):
        clips.append(
            f'<clipPath id="c{i}"><rect class="typer r{i}" x="98" y="150" width="{len(role) * 15.4 + 6:.0f}" height="40"/></clipPath>'
        )
        roles.append(
            f'<text clip-path="url(#c{i})" x="98" y="180" font-family="{MONO}" font-size="25.5" '
            f'font-weight="700" fill="{t["text"]}">{esc(role)}</text>'
        )
    delays = "".join(f".r{i}{{animation-delay:{i * 3.2}s}}" for i in range(len(ROLES)))
    style = f"""
.typer{{transform-box:fill-box;transform-origin:left center;transform:scaleX(0);animation:type {cycle}s infinite both}}
{delays}
@keyframes type{{0%{{transform:scaleX(0);animation-timing-function:steps(24,end)}}
8%{{transform:scaleX(1)}}19%{{transform:scaleX(1);animation-timing-function:steps(24,end)}}
24%,100%{{transform:scaleX(0)}}}}
@media (prefers-reduced-motion: reduce){{.r0{{transform:scaleX(1)}}}}
.bar{{transform-box:fill-box;transform-origin:bottom;animation:grow 1.1s cubic-bezier(.2,.8,.3,1) both}}
.b2{{animation-delay:.1s}}.b3{{animation-delay:.2s}}.b4{{animation-delay:.3s}}.b5{{animation-delay:.4s}}.b6{{animation-delay:.5s}}.b7{{animation-delay:.6s}}
.trend{{stroke-dasharray:420;animation:draw 1.6s .5s cubic-bezier(.2,.7,.3,1) both}}
.node{{transform-box:fill-box;transform-origin:center;animation:pulse 3s ease-in-out infinite}}
.n2{{animation-delay:.6s}}.n3{{animation-delay:1.2s}}.n4{{animation-delay:1.8s}}
.edge{{stroke-dasharray:4 6;animation:flow 1.2s linear infinite}}
.cursor{{animation:blink 1.1s steps(1,end) infinite}}
@keyframes grow{{from{{transform:scaleY(0)}}to{{transform:scaleY(1)}}}}
@keyframes draw{{from{{stroke-dashoffset:420}}to{{stroke-dashoffset:0}}}}
@keyframes pulse{{0%,100%{{opacity:.55;transform:scale(.85)}}50%{{opacity:1;transform:scale(1.12)}}}}
@keyframes flow{{to{{stroke-dashoffset:-20}}}}
@keyframes blink{{50%{{opacity:0}}}}
"""
    bars = [(4, 98, 36), (26, 84, 50), (48, 90, 44), (70, 70, 64), (92, 60, 74), (114, 46, 88), (136, 32, 102)]
    bar_svg = "".join(
        f'<rect class="bar{" b" + str(i + 1) if i else ""}" x="{x}" y="{y}" width="14" height="{h}" rx="2"/>'
        for i, (x, y, h) in enumerate(bars)
    )
    body = f"""<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t['bg0']}"/><stop offset=".55" stop-color="{t['bg1']}"/><stop offset="1" stop-color="{t['bg2']}"/></linearGradient>
<linearGradient id="accent" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t['green']}"/><stop offset="1" stop-color="{t['blue']}"/></linearGradient>
<linearGradient id="barg" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{t['deep']}"/><stop offset="1" stop-color="{t['sky']}"/></linearGradient>
<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="{t['grid']}" stroke-width=".7" opacity=".6"/></pattern>
<clipPath id="card"><rect width="960" height="300" rx="18"/></clipPath>
{''.join(clips)}
</defs>
<g clip-path="url(#card)"><rect width="960" height="300" fill="url(#bg)"/><rect x="600" width="360" height="300" fill="url(#grid)"/></g>
<rect x="0.5" y="0.5" width="959" height="299" rx="18" fill="none" stroke="{t['border']}"/>
<rect x="56" y="52" width="56" height="5" rx="2.5" fill="url(#accent)"/>
<text x="54" y="126" fill="{t['text']}" font-size="60" font-weight="800" letter-spacing="-1">Ludovic Delot</text>
<text x="58" y="180" font-family="{MONO}" font-size="25.5" font-weight="700" fill="{t['green']}">❯</text>
{''.join(roles)}
<text x="58" y="226" fill="{t['muted']}" font-size="17.5" font-weight="600">Power BI · DAX · SQL · Python · dbt · BigQuery · LLM agents</text>
<text x="58" y="258" fill="{t['dim']}" font-size="15" font-family="{MONO}">LVMH · Groupe SEB · Liverpool · Mexico City</text>
<g transform="translate(632 70)">
<rect x="-14" y="-14" width="182" height="176" rx="10" fill="{t['card2']}" stroke="{t['border']}"/>
<rect x="0" y="0" width="38" height="5" rx="2.5" fill="{t['blue']}" opacity=".85"/><rect x="0" y="11" width="22" height="4" rx="2" fill="{t['deep']}"/>
<g fill="url(#barg)">{bar_svg}</g>
<path class="trend" d="M11 88 L33 76 L55 80 L77 58 L99 48 L121 34 L143 20" fill="none" stroke="{t['green']}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="143" cy="20" r="4.5" fill="{t['green']}"/>
<text x="0" y="154" fill="{t['dim']}" font-size="11" font-family="{MONO}">sell-out · MTD · YoY</text>
</g>
<g transform="translate(834 70)">
<rect x="-14" y="-14" width="100" height="176" rx="10" fill="{t['card2']}" stroke="{t['border']}"/>
<g stroke="{t['blue']}" stroke-width="1.5" fill="none" opacity=".8">
<path class="edge" d="M36 18 L12 66"/><path class="edge" d="M36 18 L60 66"/><path class="edge" d="M12 66 L36 118"/><path class="edge" d="M60 66 L36 118"/><path class="edge" d="M12 66 L60 66"/></g>
<circle class="node" cx="36" cy="18" r="9" fill="{t['green']}"/><circle class="node n2" cx="12" cy="66" r="7" fill="{t['blue']}"/>
<circle class="node n3" cx="60" cy="66" r="7" fill="{t['blue']}"/><circle class="node n4" cx="36" cy="118" r="9" fill="{t['sky']}"/>
<text x="36" y="154" fill="{t['dim']}" font-size="11" text-anchor="middle" font-family="{MONO}">agents</text>
</g>"""
    return svg(960, 300, "Ludovic Delot",
               "Business Intelligence Analyst, Power BI Developer, Data Analyst and AI Developer. "
               "Power BI, DAX, SQL, Python, dbt, BigQuery and LLM agents.", body, style)


# --------------------------------------------------------------------------- impact
IMPACT = [
    ("20+", "Power BI dashboards", "scaled from 4 · shared KPIs"),
    ("25", "table semantic model", "sell-out → stock → quotas"),
    ("25K+", "SKU–store combinations", "CPFR across 300+ stores"),
    ("h→min", "reporting prep time", "Python ETL automation"),
]


def impact(t):
    style = """.tile{animation:rise .8s cubic-bezier(.2,.8,.3,1) both}.t1{animation-delay:.15s}.t2{animation-delay:.3s}.t3{animation-delay:.45s}
.glow{animation:glow 3.2s ease-in-out infinite}
@keyframes rise{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
@keyframes glow{0%,100%{opacity:.35}50%{opacity:1}}"""
    accents = [t["green"], t["blue"], t["sky"], t["green"]]
    tiles = []
    for i, (num, label, sub) in enumerate(IMPACT):
        x = i * 242
        tiles.append(f"""<g transform="translate({x} 0)"><g class="tile t{i}">
<rect x="1" y="1" width="234" height="168" rx="14" fill="{t['card']}" stroke="{t['border']}"/>
<rect class="glow" x="24" y="24" width="34" height="5" rx="2.5" fill="{accents[i]}"/>
<text x="22" y="94" font-size="{50 if len(num) < 5 else 44}" font-weight="800" fill="url(#num)" letter-spacing="-1">{esc(num)}</text>
<text x="24" y="126" font-size="17" font-weight="700" fill="{t['text']}">{esc(label)}</text>
<text x="24" y="150" font-size="14.5" fill="{t['muted']}">{esc(sub)}</text>
</g></g>""")
    body = (f'<defs><linearGradient id="num" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t["num0"]}"/>'
            f'<stop offset="1" stop-color="{t["num1"]}"/></linearGradient></defs>\n' + "\n".join(tiles))
    return svg(962, 170, "Selected impact",
               "20+ Power BI dashboards scaled from four; a 25-table semantic model; 25,000+ SKU-store "
               "combinations analyzed across 300+ stores; reporting prep cut from hours to minutes with Python ETL.",
               body, style)


# --------------------------------------------------------------------------- pipeline
STAGES = [
    ("01 · SOURCES", "Raw data", "GCP · SharePoint", "retailer files · APIs"),
    ("02 · TRANSFORM", "Python ETL", "pandas · SQL · dbt", "data-quality checks"),
    ("03 · MODEL", "Semantic model", "DAX · TMDL · star", "PBIP in Git"),
    ("04 · DECIDE", "Power BI", "governed KPIs", "self-service reports"),
    ("05 · AUTOMATE", "AI layer", "agents · skills · MCP", "docs · checks"),
]


def pipeline(t):
    style = """.stage{animation:rise .7s cubic-bezier(.2,.8,.3,1) both}.s1{animation-delay:.12s}.s2{animation-delay:.24s}.s3{animation-delay:.36s}.s4{animation-delay:.48s}
.wire{stroke-dasharray:3 7;animation:flow 1s linear infinite}
.packet{animation:travel 3.6s cubic-bezier(.45,0,.55,1) infinite}.p2{animation-delay:1.2s}.p3{animation-delay:2.4s}
@keyframes rise{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
@keyframes flow{to{stroke-dashoffset:-20}}
@keyframes travel{0%{transform:translateX(0);opacity:0}8%{opacity:1}92%{opacity:1}100%{transform:translateX(768px);opacity:0}}
@media (prefers-reduced-motion: reduce){.packet{opacity:0}}"""
    parts = [
        f'<path class="wire" d="M96 112 H864" stroke="{t["blue"]}" stroke-width="2" fill="none" opacity=".75"/>',
        f'<g fill="{t["green"]}"><circle class="packet" cx="96" cy="112" r="5"/>'
        f'<circle class="packet p2" cx="96" cy="112" r="5"/><circle class="packet p3" cx="96" cy="112" r="5"/></g>',
    ]
    for i, (kick, title, l1, l2) in enumerate(STAGES):
        stroke = t["blue"] if i == 2 else t["border"]
        parts.append(f"""<g transform="translate({i * 193} 0)"><g class="stage s{i}">
<rect x="1" y="20" width="182" height="188" rx="14" fill="{t['card']}" stroke="{stroke}" stroke-width="{1.6 if i == 2 else 1}"/>
<text x="18" y="52" font-size="12.5" font-weight="700" fill="{t['green']}" font-family="{MONO}">{esc(kick)}</text>
<text x="18" y="84" font-size="20" font-weight="800" fill="{t['text']}">{esc(title)}</text>
<text x="18" y="160" font-size="14.5" fill="{t['muted']}">{esc(l1)}</text>
<text x="18" y="182" font-size="14.5" fill="{t['muted']}">{esc(l2)}</text>
</g></g>""")
    return svg(960, 212, "How I build data products",
               "Five stages: raw sources; Python ETL with data-quality checks; a semantic model in DAX and TMDL "
               "versioned as PBIP in Git; Power BI with governed KPIs; and an AI layer of agents, skills and MCP.",
               "\n".join(parts), style)


# --------------------------------------------------------------------------- project thumbnails
def ill_list(t):  # ordered selector
    rows = []
    for i, (lab, w) in enumerate([("Region", 70), ("Brand", 58), ("Product", 74)]):
        y = 26 + i * 34
        rows.append(f'<rect x="0" y="{y}" width="150" height="26" rx="6" fill="{t["card"]}" stroke="{t["border"]}"/>'
                    f'<text x="12" y="{y + 18}" font-size="13" font-weight="700" fill="{t["blue"]}">{i + 1}</text>'
                    f'<text x="30" y="{y + 18}" font-size="13" fill="{t["text"]}">{lab}</text>'
                    f'<text x="132" y="{y + 18}" font-size="12" fill="{t["green"]}" text-anchor="middle">⇅</text>')
    return "".join(rows)


def ill_matrix(t):
    cells = "".join(
        f'<rect x="{c * 30}" y="{30 + r * 22}" width="26" height="18" rx="3" fill="{t["deep"] if (r + c) % 3 else t["blue"]}" opacity="{.45 + .15 * ((r + c) % 3)}"/>'
        for r in range(4) for c in range(4))
    return cells + f'<path d="M132 52 a24 24 0 1 1 -4 34" fill="none" stroke="{t["green"]}" stroke-width="2.5"/><path d="M122 84 l6 6 l6 -8" fill="none" stroke="{t["green"]}" stroke-width="2.5"/>'


def ill_doc(t):
    lines = "".join(f'<rect x="14" y="{40 + i * 14}" width="{[70, 54, 64, 40, 60][i]}" height="5" rx="2.5" fill="{t["muted"]}" opacity=".55"/>' for i in range(5))
    return (f'<rect x="0" y="22" width="100" height="112" rx="8" fill="{t["card"]}" stroke="{t["border"]}"/>{lines}'
            f'<g stroke="{t["blue"]}" stroke-width="1.6"><line x1="124" y1="44" x2="150" y2="78"/><line x1="124" y1="112" x2="150" y2="78"/></g>'
            f'<circle cx="124" cy="44" r="7" fill="{t["blue"]}"/><circle cx="124" cy="112" r="7" fill="{t["blue"]}"/><circle cx="150" cy="78" r="9" fill="{t["green"]}"/>')


def ill_pages(t):
    out = ""
    for i in range(3):
        x, y = i * 22, 22 + i * 16
        out += (f'<rect x="{x}" y="{y}" width="110" height="66" rx="6" fill="{t["card"]}" stroke="{t["border"]}"/>'
                f'<rect x="{x + 10}" y="{y + 10}" width="40" height="22" rx="3" fill="{t["blue"]}" opacity=".5"/>'
                f'<rect x="{x + 56}" y="{y + 10}" width="44" height="5" rx="2" fill="{t["muted"]}" opacity=".5"/>'
                f'<rect x="{x + 56}" y="{y + 21}" width="34" height="5" rx="2" fill="{t["muted"]}" opacity=".5"/>')
    return out + f'<text x="66" y="150" font-size="12" font-family="{MONO}" fill="{t["green"]}" text-anchor="middle">EN ES IT FR</text>'


def ill_star(t):
    dims = [(80, 22), (150, 78), (80, 134), (10, 78)]
    lines = "".join(f'<line x1="80" y1="78" x2="{x}" y2="{y}" stroke="{t["blue"]}" stroke-width="1.6"/>' for x, y in dims)
    boxes = "".join(f'<rect x="{x - 22}" y="{y - 12}" width="44" height="24" rx="5" fill="{t["card"]}" stroke="{t["border"]}"/>'
                    f'<text x="{x}" y="{y + 4}" font-size="10" text-anchor="middle" fill="{t["muted"]}" font-family="{MONO}">dim</text>' for x, y in dims)
    return (lines + boxes + f'<rect x="52" y="62" width="56" height="32" rx="6" fill="{t["blue"]}"/>'
            f'<text x="80" y="83" font-size="12" font-weight="700" text-anchor="middle" fill="#ffffff" font-family="{MONO}">fact</text>')


def ill_dag(t):
    layers = [("stg", 0), ("int", 58), ("mart", 116)]
    out = ""
    for name, x in layers:
        for j in range(2 if name != "mart" else 1):
            y = 40 + j * 52 if name != "mart" else 66
            out += (f'<rect x="{x}" y="{y}" width="46" height="26" rx="6" fill="{t["card"]}" stroke="{t["border"]}"/>'
                    f'<text x="{x + 23}" y="{y + 17}" font-size="10.5" text-anchor="middle" fill="{t["muted"]}" font-family="{MONO}">{name}</text>')
    out += "".join(f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}" stroke="{t["blue"]}" stroke-width="1.5"/>'
                   for a, b, c, d in [(46, 53, 58, 53), (46, 105, 58, 105), (104, 53, 116, 79), (104, 105, 116, 79)])
    return out


def ill_agents(t):
    pts = [(80, 24), (24, 72), (136, 72), (52, 128), (108, 128)]
    edges = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 4), (1, 2), (0, 3)]
    out = "".join(f'<line class="edge" x1="{pts[a][0]}" y1="{pts[a][1]}" x2="{pts[b][0]}" y2="{pts[b][1]}" stroke="{t["blue"]}" stroke-width="1.5"/>' for a, b in edges)
    cols = [t["green"], t["blue"], t["blue"], t["sky"], t["sky"]]
    return out + "".join(f'<circle class="node n{i}" cx="{x}" cy="{y}" r="{10 if i == 0 else 8}" fill="{cols[i]}"/>' for i, (x, y) in enumerate(pts))


def ill_gate(t):
    return (f'<rect x="0" y="40" width="64" height="20" rx="5" fill="{t["card"]}" stroke="{t["border"]}"/>'
            f'<rect x="0" y="70" width="64" height="20" rx="5" fill="{t["card"]}" stroke="{t["border"]}"/>'
            f'<rect x="0" y="100" width="64" height="20" rx="5" fill="{t["card"]}" stroke="#cf222e" stroke-opacity=".7"/>'
            f'<rect x="84" y="34" width="12" height="92" rx="4" fill="{t["blue"]}"/>'
            f'<text x="128" y="62" font-size="22" font-weight="800" fill="{t["green"]}" text-anchor="middle">✓</text>'
            f'<text x="128" y="92" font-size="22" font-weight="800" fill="{t["green"]}" text-anchor="middle">✓</text>'
            f'<text x="128" y="122" font-size="22" font-weight="800" fill="#cf222e" text-anchor="middle">✕</text>')


def ill_hub(t):
    sats = [(20, 40), (20, 116), (140, 40), (140, 116), (80, 140)]
    return ("".join(f'<line x1="80" y1="78" x2="{x}" y2="{y}" stroke="{t["blue"]}" stroke-width="1.5"/>' for x, y in sats)
            + "".join(f'<rect x="{x - 14}" y="{y - 10}" width="28" height="20" rx="4" fill="{t["card"]}" stroke="{t["border"]}"/>' for x, y in sats)
            + f'<circle class="node" cx="80" cy="78" r="18" fill="{t["green"]}"/>'
            f'<text x="80" y="83" font-size="11" font-weight="800" text-anchor="middle" fill="#ffffff" font-family="{MONO}">MOC</text>')


def ill_mcp(t):
    return (f'<rect x="0" y="50" width="62" height="56" rx="10" fill="{t["card"]}" stroke="{t["border"]}"/>'
            f'<text x="31" y="84" font-size="13" font-weight="800" text-anchor="middle" fill="{t["blue"]}" font-family="{MONO}">LLM</text>'
            f'<line class="edge" x1="62" y1="78" x2="96" y2="78" stroke="{t["green"]}" stroke-width="2"/>'
            f'<rect x="96" y="30" width="66" height="34" rx="7" fill="{t["card"]}" stroke="{t["border"]}"/>'
            f'<rect x="96" y="92" width="66" height="34" rx="7" fill="{t["card"]}" stroke="{t["border"]}"/>'
            f'<line x1="96" y1="78" x2="96" y2="47" stroke="{t["green"]}" stroke-width="2"/><line x1="96" y1="78" x2="96" y2="109" stroke="{t["green"]}" stroke-width="2"/>'
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
    style = """.edge{stroke-dasharray:4 6;animation:flow 1.2s linear infinite}
.node{transform-box:fill-box;transform-origin:center;animation:pulse 3s ease-in-out infinite}
.n1{animation-delay:.5s}.n2{animation-delay:1s}.n3{animation-delay:1.5s}.n4{animation-delay:2s}
@keyframes flow{to{stroke-dashoffset:-20}}
@keyframes pulse{0%,100%{opacity:.6;transform:scale(.88)}50%{opacity:1;transform:scale(1.1)}}"""
    body = (f'<rect x="0.5" y="0.5" width="479" height="179" rx="14" fill="{t["card2"]}" stroke="{t["border"]}"/>'
            f'<rect x="26" y="28" width="30" height="5" rx="2.5" fill="{t["green"]}"/>'
            f'<text x="26" y="62" font-size="13.5" font-weight="700" letter-spacing="1.2" fill="{t["blue"]}" font-family="{MONO}">{esc(kicker)}</text>'
            f'<text x="26" y="108" font-size="27" font-weight="800" fill="{t["text"]}" letter-spacing="-.4">{esc(lines[0])}</text>'
            f'<text x="26" y="142" font-size="27" font-weight="800" fill="{t["text"]}" letter-spacing="-.4">{esc(lines[1])}</text>'
            f'<g transform="translate(298 14)">{ill(t)}</g>')
    return svg(480, 180, f"{kicker}: {' '.join(lines)}", f"{kicker}. {' '.join(lines)}.", body, style)


# --------------------------------------------------------------------------- footer rule
def footer(t):
    body = (f'<defs><linearGradient id="rule" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t["blue"]}" stop-opacity="0"/>'
            f'<stop offset=".5" stop-color="{t["blue"]}"/><stop offset="1" stop-color="{t["blue"]}" stop-opacity="0"/></linearGradient></defs>'
            f'<path d="M48 24 H912" stroke="url(#rule)" stroke-width="2"/><circle cx="480" cy="24" r="6" fill="{t["green"]}"/>')
    return svg(960, 48, "Divider", "Decorative divider.", body)


def main():
    for name, t in THEMES.items():
        out = ROOT / "assets" / name
        (out / "cards").mkdir(parents=True, exist_ok=True)
        (out / "banner.svg").write_text(banner(t), encoding="utf-8")
        (out / "impact.svg").write_text(impact(t), encoding="utf-8")
        (out / "pipeline.svg").write_text(pipeline(t), encoding="utf-8")
        (out / "footer.svg").write_text(footer(t), encoding="utf-8")
        for slug, kicker, lines, ill in CARDS:
            (out / "cards" / f"{slug}.svg").write_text(card(t, kicker, lines, ill), encoding="utf-8")
    print("Built assets/dark and assets/light")


if __name__ == "__main__":
    main()
