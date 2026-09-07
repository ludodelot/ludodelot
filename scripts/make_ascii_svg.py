"""
Convert the prepped grayscale photo into a self-typing, monochrome
ASCII-art SVG.

The image is downsampled to a character grid; each cell's average
brightness picks a glyph from a density ramp (sparse -> dense).
Each row wipes in left-to-right via an SVG clip-path animation,
staggered top to bottom. Prints once, then freezes (no looping).

Usage: python make_ascii_svg.py source-photo-prepped.png
Output: ../avi-ascii.svg  (well, ludo-ascii.svg)
"""
import sys
import numpy as np
from PIL import Image

# Bright (sparse) -> dark (dense). Leading space clears the background.
RAMP = " .`:-=+*cs#%@"

COLS = 100
ROWS = 55
CHAR_W = 6.4
CHAR_H = 12.0
FONT_SIZE = 12
FILL = "#8fa8c9"  # light steel-blue, monochrome accent matching the repo palette


def image_to_ascii_rows(path: str) -> list[str]:
    img = Image.open(path).convert("L")
    img = img.resize((COLS, ROWS), Image.LANCZOS)
    arr = np.asarray(img, dtype=np.float32) / 255.0  # 0=black, 1=white

    # Stretch levels so the darkest/lightest pixels hit 0/1, then apply a
    # gentle gamma to brighten midtones -- keeps the ramp from over-using
    # the dense glyphs on skin/hair and reserves them for real shadow.
    lo, hi = arr.min(), arr.max()
    if hi > lo:
        arr = (arr - lo) / (hi - lo)
    arr = arr ** 0.72

    rows = []
    n = len(RAMP)
    for y in range(ROWS):
        chars = []
        for x in range(COLS):
            brightness = arr[y, x]
            idx = int((1.0 - brightness) * (n - 1))
            idx = max(0, min(n - 1, idx))
            chars.append(RAMP[idx])
        rows.append("".join(chars))
    return rows


def escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def build_svg(rows: list[str]) -> str:
    width = COLS * CHAR_W
    height = ROWS * CHAR_H
    row_duration = 0.55
    row_stagger = 0.028  # seconds between each row starting

    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width:.1f} {height:.1f}" '
        f'width="{width:.0f}" height="{height:.0f}" font-family="Menlo, Consolas, \'DejaVu Sans Mono\', monospace">'
    )
    parts.append(f'<rect width="100%" height="100%" fill="none"/>')
    parts.append("<defs>")

    for i, row in enumerate(rows):
        clip_id = f"clip{i}"
        y = (i + 0.85) * CHAR_H
        parts.append(f'<clipPath id="{clip_id}">')
        parts.append(f'  <rect x="0" y="{i * CHAR_H:.1f}" width="0" height="{CHAR_H:.1f}">')
        begin = i * row_stagger
        parts.append(
            f'    <animate attributeName="width" from="0" to="{width:.1f}" '
            f'begin="{begin:.3f}s" dur="{row_duration}s" fill="freeze" '
            f'calcMode="spline" keySplines="0.25 0.1 0.25 1"/>'
        )
        parts.append("  </rect>")
        parts.append("</clipPath>")

    parts.append("</defs>")

    for i, row in enumerate(rows):
        clip_id = f"clip{i}"
        y = (i + 0.85) * CHAR_H
        text = escape(row)
        parts.append(
            f'<text x="0" y="{y:.1f}" font-size="{FONT_SIZE}" '
            f'fill="{FILL}" clip-path="url(#{clip_id})" '
            f'style="white-space:pre" xml:space="preserve">{text}</text>'
        )

    parts.append("</svg>")
    return "\n".join(parts)


def main(src_path: str, out_path: str) -> None:
    rows = image_to_ascii_rows(src_path)
    svg = build_svg(rows)
    with open(out_path, "w") as f:
        f.write(svg)
    print(f"Saved: {out_path} ({COLS}x{ROWS} chars)")


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "source-photo-prepped.png"
    out = sys.argv[2] if len(sys.argv) > 2 else "../ludo-ascii.svg"
    main(src, out)
