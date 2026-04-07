import json
from pathlib import Path

from chameleon import PageTemplateLoader

from . import build_report, load_all_csvs
from .enrich import Manifest


DEFAULT_CSV_DIR = Path("csv")
DEFAULT_TEMPLATES_DIR = Path("templates")
DEFAULT_OUTPUT = Path("html/summary.html")


def _load_config_defaults():
    try:
        from beemo.settings import get_config
        config = get_config()
        return config
    except Exception:
        return None


def main():
    import argparse

    config = _load_config_defaults()
    report_config = config.report if config else None

    parser = argparse.ArgumentParser(description="Generate HTML analytics report from log CSVs")
    parser.add_argument(
        "--csv-dir", type=Path,
        default=report_config.csv_dir if report_config else DEFAULT_CSV_DIR,
    )
    parser.add_argument(
        "--templates-dir", type=Path,
        default=config.build.templates_dir if config and config.build else DEFAULT_TEMPLATES_DIR,
    )
    parser.add_argument(
        "--manifest", type=Path,
        default=config.build.output_dir / "manifest.json" if config and config.build else None,
        help="manifest.json from beemo build",
    )
    parser.add_argument(
        "--output", type=Path,
        default=report_config.output if report_config else DEFAULT_OUTPUT,
    )
    parser.add_argument(
        "--base-url",
        default=report_config.base_url if report_config else "",
        help="Site base URL e.g. https://bennuttall.com",
    )
    parser.add_argument(
        "--title",
        default=report_config.title if report_config else "",
        help="Report title (default: derived from base-url and date range)",
    )
    args = parser.parse_args()

    manifest = Manifest(args.manifest) if args.manifest and args.manifest.exists() else None
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
