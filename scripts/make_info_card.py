"""Generate the static, terminal-inspired profile summary SVG."""

from pathlib import Path

WIDTH = 640
LINE_H = 27
PAD_X = 26
TITLE_H = 54

NAVY = "#0B1F3F"
BORDER = "#1F3A66"
KEY_COLOR = "#79BFF0"
VAL_COLOR = "#F2F6FB"
DIM_COLOR = "#9AAECC"
ACCENT = "#39D353"

ROWS = [
    ("whoami", "Ludovic Delot"),
    ("role", "BI & Data Analyst · Content Producer"),
    ("now", "LVMH — Data & BI Intern (Luxury / Beauty)"),
    ("past", "Groupe SEB (CPFR) · Liverpool (Automation)"),
    ("stack", "Power BI · DAX · SQL · Python · R"),
    ("also_shoots", "Live Nation/OCESA · Tomorrowland"),
    ("founded", "Delot Media — 160+ clients since 2019"),
    ("education", "MSc Management & Finance — Rennes SB"),
    ("location", "Mexico City, MX · Mexican / French"),
    ("languages", "Spanish · English · French"),
]

ROOT = Path(__file__).resolve().parent.parent


def esc(value: str) -> str:
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_svg() -> str:
    height = TITLE_H + len(ROWS) * LINE_H + 22
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {height}" '
        'role="img" aria-labelledby="title desc" '
        'font-family="Menlo, Consolas, \'DejaVu Sans Mono\', monospace">',
        '<title id="title">Profile facts for Ludovic Delot</title>',
        '<desc id="desc">Role, experience, tools, education, location, and languages.</desc>',
        '<style>.cursor{animation:blink 1.1s steps(1,end) infinite}'
        '@keyframes blink{50%{opacity:.2}}'
        '@media(prefers-reduced-motion:reduce){.cursor{animation:none}}</style>',
        f'<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{height - 1}" rx="10" '
        f'fill="{NAVY}" stroke="{BORDER}"/>',
        f'<text x="{PAD_X}" y="34" font-size="13.5" fill="{VAL_COLOR}" font-weight="600">'
        f'<tspan fill="{ACCENT}">&gt;</tspan> profile.json</text>',
        f'<rect class="cursor" x="151" y="21" width="8" height="15" rx="1" fill="{ACCENT}"/>',
        f'<line x1="{PAD_X}" y1="{TITLE_H}" x2="{WIDTH - PAD_X}" y2="{TITLE_H}" '
        f'stroke="{BORDER}"/>',
    ]

    key_width = 118
    for index, (key, value) in enumerate(ROWS):
        y = TITLE_H + LINE_H * (index + 1)
        parts.append(
            f'<text x="{PAD_X + key_width}" y="{y}" font-size="13.5">'
            f'<tspan x="{PAD_X}" fill="{KEY_COLOR}" font-weight="600">{esc(key)}</tspan>'
            f'<tspan fill="{DIM_COLOR}"> : </tspan>'
            f'<tspan fill="{VAL_COLOR}">{esc(value)}</tspan></text>'
        )

    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    output = ROOT / "info-card.svg"
    output.write_text(build_svg(), encoding="utf-8")
    print(f"Saved: {output}")
