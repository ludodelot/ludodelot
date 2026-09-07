"""
Fetch a public GitHub contribution calendar with no token: GitHub serves
it as HTML at https://github.com/users/<user>/contributions -- the same
fragment the profile page itself embeds. Parse the day cells with
BeautifulSoup and write data/contributions.json (raw days + derived
stats: current streak, longest streak, best day, total).

Usage: python fetch_contributions.py [username]
Output: ../data/contributions.json
"""
import json
import sys
from datetime import date, datetime

import requests
from bs4 import BeautifulSoup

USERNAME = sys.argv[1] if len(sys.argv) > 1 else "ludodelot"
URL = f"https://github.com/users/{USERNAME}/contributions"


def fetch_days() -> list[dict]:
    resp = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    days = []
    # GitHub renders each day as a <td> (older markup) or <rect>/<table>
    # cell with data-date + data-level (or data-count via title).
    cells = soup.select("td.ContributionCalendar-day") or soup.select("[data-date]")
    for cell in cells:
        d = cell.get("data-date")
        if not d:
            continue
        level = cell.get("data-level")
        count = 0
        title_el = cell.find_next("tool-tip") if cell.has_attr("id") else None
        tooltip_id = cell.get("id")
        if tooltip_id:
            tip = soup.find("tool-tip", attrs={"for": tooltip_id})
            if tip and tip.text:
                text = tip.text.strip()
                first_word = text.split(" ")[0]
                if first_word.lower() == "no":
                    count = 0
                else:
                    try:
                        count = int(first_word.replace(",", ""))
                    except ValueError:
                        count = 0
        days.append({"date": d, "count": count, "level": int(level) if level else 0})

    days.sort(key=lambda x: x["date"])
    return days


def compute_stats(days: list[dict]) -> dict:
    total = sum(d["count"] for d in days)

    # Longest streak + current streak (consecutive days with count > 0).
    longest = current = 0
    running = 0
    today = date.today()
    last_active_date = None
    for d in days:
        if d["count"] > 0:
            running += 1
            longest = max(longest, running)
            last_active_date = datetime.strptime(d["date"], "%Y-%m-%d").date()
        else:
            running = 0

    # Current streak: walk backwards from the most recent day.
    running = 0
    for d in reversed(days):
        d_date = datetime.strptime(d["date"], "%Y-%m-%d").date()
        if (today - d_date).days > 1 and running == 0:
            # allow "today has no contribution yet" to not break the streak
            if d_date != today:
                continue
        if d["count"] > 0:
            running += 1
        else:
            if d_date == today:
                continue  # today might just not have activity YET
            break
    current = running

    best = max(days, key=lambda x: x["count"], default={"date": None, "count": 0})

    return {
        "total": total,
        "longest_streak": longest,
        "current_streak": current,
        "best_day": {"date": best["date"], "count": best["count"]},
        "last_active": last_active_date.isoformat() if last_active_date else None,
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }


def main() -> None:
    days = fetch_days()
    stats = compute_stats(days)
    out = {"username": USERNAME, "days": days, "stats": stats}
    with open("../data/contributions.json", "w") as f:
        json.dump(out, f, indent=2)
    print(f"Fetched {len(days)} days. Total: {stats['total']}. Longest streak: {stats['longest_streak']}.")


if __name__ == "__main__":
    main()
