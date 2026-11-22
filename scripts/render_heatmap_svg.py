"""
Render data/contributions.json as a static 53-week x 7-day contribution
calendar with rounded cells, a Less-to-More legend, and a stats footer.

Usage: python render_heatmap_svg.py
Output: ../contrib-heatmap.svg
"""
import json
from datetime import datetime
from pathlib import Path

CELL = 11
GAP = 3
STEP = CELL + GAP
LEFT_PAD = 28
TOP_PAD = 20
BOTTOM_PAD = 34

THEMES = {
    "dark": {"cells": ["#161B22", "#0E4429", "#1F6FB2", "#2E86DE", "#4A90D9", "#39D353"],
             "label": "#7E93B8", "stats": "#5FA8E0", "out": "contrib-heatmap.svg"},
    "light": {"cells": ["#EBEFF5", "#B6E3C4", "#80B8F5", "#4A95E8", "#0969DA", "#1A7F37"],
              "label": "#6E7781", "stats": "#0969DA", "out": "contrib-heatmap-light.svg"},
}
PALETTE = THEMES["dark"]["cells"]
# level:    none      1          2          3          4          5(best-day highlight)

MONTHS = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]

ROOT = Path(__file__).resolve().parent.parent


def load_data():
    with (ROOT / "data" / "contributions.json").open(encoding="utf-8") as f:
        return json.load(f)


def build_weeks(days: list[dict]) -> list[list[dict | None]]:
    """Group days into GitHub-style weeks (columns), Sunday-first."""
    parsed = []
    for d in days:
        dt = datetime.strptime(d["date"], "%Y-%m-%d").date()
        parsed.append((dt, d))
    parsed.sort(key=lambda x: x[0])

    weeks: list[list[dict | None]] = []
    current_week: list[dict | None] = [None] * 7
    for dt, d in parsed:
        dow = (dt.weekday() + 1) % 7  # Python Mon=0 -> GitHub Sun=0
        if dow == 0 and any(current_week):
            weeks.append(current_week)
            current_week = [None] * 7
        current_week[dow] = {**d, "_dt": dt}
    if any(current_week):
        weeks.append(current_week)
    return weeks


def month_labels(weeks: list[list[dict | None]]) -> list[tuple[int, str]]:
    labels = []
    last_month = None
    for wi, week in enumerate(weeks):
        for day in week:
            if day is None:
                continue
            m = day["_dt"].month
            if m != last_month:
                labels.append((wi, MONTHS[m - 1]))
                last_month = m
            break
    return labels


def build_svg(data: dict, theme: str = "dark") -> str:
    palette = THEMES[theme]["cells"]
    label_c = THEMES[theme]["label"]
    stats_c = THEMES[theme]["stats"]
    days = data["days"]
    stats = data["stats"]
    weeks = build_weeks(days)
    n_weeks = len(weeks)

    width = LEFT_PAD + n_weeks * STEP + 10
    height = TOP_PAD + 7 * STEP + BOTTOM_PAD

    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'role="img" aria-labelledby="title desc" '
        f'font-family="Menlo, Consolas, \'DejaVu Sans Mono\', monospace">'
    )
    parts.append('<title id="title">GitHub contribution activity</title>')
    parts.append(
        f'<desc id="desc">Contribution calendar for {data["username"]}: '
        f'{stats.get("total", 0)} contributions in the last year.</desc>'
    )
    # Month labels.
    for wi, label in month_labels(weeks):
        x = LEFT_PAD + wi * STEP
        parts.append(
            f'<text x="{x}" y="{TOP_PAD - 6}" font-size="10" fill="{label_c}">{label}</text>'
        )

    # Day cells, staggered diagonally (col + row) so they slide in like a wave.
    best_date = stats.get("best_day", {}).get("date")
    for wi, week in enumerate(weeks):
        for di, day in enumerate(week):
            x = LEFT_PAD + wi * STEP
            y = TOP_PAD + di * STEP
            if day is None:
                continue
            level = min(day.get("level", 0), 4)
            color = palette[level]
            if best_date and day["date"] == best_date and level > 0:
                color = palette[5]
            title = f'{day["count"]} contribution{"s" if day["count"] != 1 else ""} on {day["date"]}'
            parts.append(
                f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" fill="{color}">'
                f'<title>{title}</title></rect>'
            )

    # Legend: Less -> More.
    legend_y = height - BOTTOM_PAD + 22
    parts.append(f'<text x="{LEFT_PAD}" y="{legend_y}" font-size="10" fill="{label_c}">Less</text>')
    lx = LEFT_PAD + 34
    for level, color in enumerate(palette[:5]):
        parts.append(f'<rect x="{lx}" y="{legend_y - 9}" width="{CELL}" height="{CELL}" rx="2.5" fill="{color}"/>')
        lx += STEP
    parts.append(f'<text x="{lx + 4}" y="{legend_y}" font-size="10" fill="{label_c}">More</text>')

    # Stats footer, right-aligned.
    total = stats.get("total", 0)
    streak = stats.get("longest_streak", 0)
    stats_text = f'{total} contributions in the last year  ·  longest streak {streak} day{"s" if streak != 1 else ""}'
    parts.append(
        f'<text x="{width - 10}" y="{legend_y}" font-size="10" fill="{stats_c}" text-anchor="end">{stats_text}</text>'
    )

    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    data = load_data()
    for theme, cfg in THEMES.items():
        out = ROOT / cfg["out"]
        out.write_text(build_svg(data, theme), encoding="utf-8")
        print(f"Saved: {out}")


if __name__ == "__main__":
    main()
