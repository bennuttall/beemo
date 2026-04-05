import csv
from collections import Counter
from datetime import datetime
from pathlib import Path

from .enrich import Manifest


def load_csv(csv_path: Path) -> list[dict]:
    with open(csv_path) as f:
        return list(csv.DictReader(f))


def load_all_csvs(csv_dir: Path) -> list[dict]:
    rows = []
    for f in sorted(csv_dir.rglob("*.csv")):
        rows.extend(load_csv(f))
    return rows


def build_report(rows: list[dict], manifest: Manifest | None = None, base_url: str = "") -> dict:
    times = [datetime.fromisoformat(r["time"]) for r in rows]
    dates = sorted(set(t.date() for t in times))
    hits_by_day = [sum(1 for t in times if t.date() == d) for d in dates]

    month_counts = Counter(t.strftime("%Y-%m") for t in times)
    months = sorted(month_counts)
    hits_by_month = [month_counts[m] for m in months]

    human_rows = [r for r in rows if r.get("is_bot", "False") not in ("True", True)]
    bot_rows = [r for r in rows if r.get("is_bot", "False") in ("True", True)]

    path_counts = Counter(r["path"] for r in rows)
    ua_counts = Counter(r["ua"] for r in rows).most_common(15)
    unique_ips = len(set(r["remote_host"] for r in rows))

    base_domain = (
        base_url.replace("https://", "").replace("http://", "").rstrip("/") if base_url else ""
    )
    referer_counts = Counter(
        r["referer"] for r in rows if r.get("referer") and r["referer"] != base_domain
    ).most_common(20)

    sections = {"page": [], "post": [], "other": []}
    for path, n in path_counts.most_common():
        if path == "/404/":
            continue
        info = manifest.get(path) if manifest else None
        if not info:
            continue
        entry = {"path": path, "title": info["title"], "type": info["type"], "hits": n}
        if info["type"] == "page":
            sections["page"].append(entry)
        elif info["type"] == "post":
            sections["post"].append(entry)
        else:
            sections["other"].append(entry)

    return {
        "date_from": str(dates[0]) if dates else "",
        "date_to": str(dates[-1]) if dates else "",
        "total_hits": len(rows),
        "human_hits": len(human_rows),
        "bot_hits": len(bot_rows),
        "unique_ips": unique_ips,
        "dates": [str(d) for d in dates],
        "hits_by_day": hits_by_day,
        "months": months,
        "hits_by_month": hits_by_month,
        "sections": sections,
        "ua_counts": ua_counts,
        "referer_counts": referer_counts,
        "base_url": base_url,
    }
