import json
from pathlib import Path

from chameleon import PageTemplateLoader

from . import build_report, load_all_csvs
from .enrich import Manifest


DEFAULT_CSV_DIR = Path("csv")
DEFAULT_TEMPLATES_DIR = Path("templates")
DEFAULT_OUTPUT = Path("html/summary.html")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate HTML analytics report from log CSVs")
    parser.add_argument("--csv-dir", type=Path, default=DEFAULT_CSV_DIR)
    parser.add_argument("--templates-dir", type=Path, default=DEFAULT_TEMPLATES_DIR)
    parser.add_argument("--manifest", type=Path, help="manifest.json from beemo build")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--base-url", default="", help="Site base URL e.g. https://bennuttall.com")
    parser.add_argument(
        "--title", default="", help="Report title (default: derived from base-url and date range)"
    )
    args = parser.parse_args()

    manifest = Manifest(args.manifest) if args.manifest else None
    rows = load_all_csvs(args.csv_dir)
    report = build_report(rows, manifest, base_url=args.base_url)

    date_range = (
        report["date_from"]
        if report["date_from"] == report["date_to"]
        else f"{report['date_from']} to {report['date_to']}"
    )
    site = args.base_url.replace("https://", "").replace("http://", "").rstrip("/") or "Analytics"
    title = args.title or f"{site} — {date_range}"

    templates = PageTemplateLoader(search_path=[str(args.templates_dir)], default_extension=".pt")
    html = templates["report"](report=report, title=title, json=json)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(html)
    print(args.output)
