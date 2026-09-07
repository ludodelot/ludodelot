"""
Hand-authored neofetch-style info card SVG: a title bar, then colored
key/value rows. Each line fades + slides in on a short stagger so the
panel looks like it's printing next to the ASCII portrait. Prints once,
then freezes (no looping).

STATIC=1 env var emits a frozen (already-fully-visible) frame, useful
for local previews / Quick Look.

Usage: python make_info_card.py
Output: ../info-card.svg
"""
import os

WIDTH = 640
LINE_H = 27
PAD_X = 26
TITLE_H = 44

# Blue palette shared with the rsb-* project READMEs.
NAVY = "#0B1F3F"
NAVY_LIGHT = "#132A52"
BORDER = "#1F3A66"
KEY_COLOR = "#5FA8E0"   # sky blue for labels
VAL_COLOR = "#E8EEF7"   # near-white for values
DIM_COLOR = "#7E93B8"   # muted blue-gray for punctuation/comments
ACCENT = "#39D353"      # small "online/active" green dot, GitHub-heatmap green

ROWS = [
    ("whoami", "Ludovic Delot"),
    ("role", "BI & Data Analyst · Content Producer"),
    ("now", "LVMH — Data & BI Intern (Luxury / Beauty)"),
    ("past", "Groupe SEB (CPFR) · El Puerto de Liverpool (Automation)"),
    ("stack", "Power BI · DAX · SQL · Python · R"),
    ("also_shoots", "Live Nation/OCESA · Tomorrowland Lab of Tomorrow"),
    ("founded", "Delot Media — 160+ clients since 2019"),
    ("education", "MSc Int'l Management & Finance — Rennes SB"),
    ("location", "Mexico City, MX  🇲🇽🇫🇷"),
    ("languages", "Spanish (native) · English · French"),
]

STATIC = os.environ.get("STATIC") == "1"


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_svg() -> str:
    height = TITLE_H + len(ROWS) * LINE_H + 22
    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {height}" '
        f'width="{WIDTH}" height="{height}" font-family="Menlo, Consolas, \'DejaVu Sans Mono\', monospace">'
    )

    # Card background + border, rounded like a terminal window.
    parts.append(
        f'<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{height - 1}" rx="10" '
        f'fill="{NAVY}" stroke="{BORDER}" stroke-width="1"/>'
    )

    # Title bar.
    parts.append(f'<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{TITLE_H}" rx="10" fill="{NAVY_LIGHT}"/>')
    parts.append(f'<rect x="0.5" y="{TITLE_H - 9.5}" width="{WIDTH - 1}" height="10" fill="{NAVY_LIGHT}"/>')
    parts.append(f'<line x1="0.5" y1="{TITLE_H}" x2="{WIDTH - 0.5}" y2="{TITLE_H}" stroke="{BORDER}" stroke-width="1"/>')
    # Traffic-light dots.
    for i, c in enumerate(["#FF5F57", "#FEBC2E", "#28C840"]):
        parts.append(f'<circle cx="{22 + i * 18}" cy="{TITLE_H / 2}" r="6" fill="{c}"/>')
    parts.append(
        f'<text x="{WIDTH / 2}" y="{TITLE_H / 2 + 4.5}" text-anchor="middle" '
        f'font-size="12.5" fill="{DIM_COLOR}">ludo@github: ~/whoami</text>'
    )
    # "active now" dot, top-right.
    parts.append(f'<circle cx="{WIDTH - 20}" cy="{TITLE_H / 2}" r="4" fill="{ACCENT}"/>')

    # Prompt line.
    prompt_y = TITLE_H + LINE_H
    parts.append(
        f'<text x="{PAD_X}" y="{prompt_y - 6}" font-size="13.5">'
        f'<tspan fill="{ACCENT}">ludo@github</tspan><tspan fill="{DIM_COLOR}">:</tspan>'
        f'<tspan fill="{KEY_COLOR}">~</tspan><tspan fill="{DIM_COLOR}">$ </tspan>'
        f'<tspan fill="{VAL_COLOR}">./whoami.sh</tspan></text>'
    )

    key_w = 118
    for i, (key, val) in enumerate(ROWS):
        y = prompt_y + LINE_H * (i + 1) - 6
        key_x = PAD_X
        val_x = PAD_X + key_w
        opacity_attrs = "" if STATIC else 'opacity="0"'
        text = (
            f'<text x="{val_x}" y="{y}" font-size="13.5" {opacity_attrs}>'
            f'<tspan x="{key_x}" fill="{KEY_COLOR}" font-weight="600">{esc(key)}</tspan>'
            f'<tspan fill="{DIM_COLOR}"> : </tspan>'
            f'<tspan fill="{VAL_COLOR}">{esc(val)}</tspan>'
        )
        if not STATIC:
            begin = 0.35 + i * 0.09
            text += (
                f'<animate attributeName="opacity" from="0" to="1" '
                f'begin="{begin:.2f}s" dur="0.35s" fill="freeze"/>'
            )
        text += "</text>"
        parts.append(text)

    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    svg = build_svg()
    out_path = "../info-card.svg"
    with open(out_path, "w") as f:
        f.write(svg)
    print(f"Saved: {out_path}")
