import json
from pathlib import Path

from chameleon import PageTemplateLoader

from . import build_report, load_all_csvs
from .enrich import Manifest


def run(csv_dir: Path, templates_dir: Path, manifest: Path | None, output: Path, base_url: str, title: str):
    manifest_obj = Manifest(manifest) if manifest and manifest.exists() else None
    rows = load_all_csvs(csv_dir)
    report = build_report(rows, manifest_obj, base_url=base_url)

    date_range = (
        report["date_from"]
        if report["date_from"] == report["date_to"]
        else f"{report['date_from']} to {report['date_to']}"
    )
    site = base_url.replace("https://", "").replace("http://", "").rstrip("/") or "Analytics"
    title = title or f"{site} — {date_range}"

    templates = PageTemplateLoader(search_path=[str(templates_dir)], default_extension=".pt")
    html = templates["report"](report=report, title=title, json=json)

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html)
    print(output)
