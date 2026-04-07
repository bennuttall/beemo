from pathlib import Path
from typing import Annotated, Optional

import typer


app = typer.Typer(no_args_is_help=True)


def _get_config():
    try:
        from beemo.settings import get_config

        return get_config()
    except Exception:
        return None


def _require(value, name: str):
    if value is None:
        typer.echo(f"Error: {name} must be set in config or provided as an option", err=True)
        raise typer.Exit(1)
    return value


@app.command("build")
def do_build():
    """Build the site."""
    from .scribe import TheScribe

    TheScribe().build_site()


@app.command("logs")
def do_logs(
    input: Annotated[
        Optional[Path], typer.Argument(help="gz file or directory of gz files")
    ] = None,
    csv_dir: Annotated[Optional[Path], typer.Option(help="Output directory for CSV files")] = None,
    pattern: Annotated[
        Optional[str], typer.Option(help="Filename glob pattern when input is a directory")
    ] = None,
):
    """Process Apache log gz files into CSV."""
    from .logs.cli import run

    config = _get_config()
    logs = config.logs if config else None

    input = _require(input or (logs.logs_dir if logs else None), "logs.logs_dir")
    csv_dir = _require(csv_dir or (logs.csv_dir if logs else None), "logs.csv_dir")
    pattern = pattern or (logs.pattern if logs else "*.gz")

    run(input, csv_dir, pattern)


@app.command("report")
def do_report(
    csv_dir: Annotated[Optional[Path], typer.Option(help="Input CSV directory")] = None,
    templates_dir: Annotated[
        Optional[Path], typer.Option(help="Chameleon templates directory")
    ] = None,
    manifest: Annotated[Optional[Path], typer.Option(help="manifest.json from beemo build")] = None,
    output_dir: Annotated[Optional[Path], typer.Option(help="Output directory")] = None,
    base_url: Annotated[
        Optional[str], typer.Option(help="Site base URL e.g. https://bennuttall.com")
    ] = None,
    title: Annotated[Optional[str], typer.Option(help="Report title")] = None,
):
    """Generate HTML analytics report from log CSVs."""
    from .reports.cli import run

    config = _get_config()
    report_config = config.report if config else None
    build_config = config.build if config else None

    csv_dir = _require(
        csv_dir or (report_config.csv_dir if report_config else None), "report.csv_dir"
    )
    templates_dir = _require(
        templates_dir or (build_config.templates_dir if build_config else None),
        "build.templates_dir",
    )
    manifest = manifest or (build_config.output_dir / "manifest.json" if build_config else None)
    output_dir = _require(output_dir or (report_config.output_dir if report_config else None), "report.output_dir")
    base_url = base_url or (report_config.base_url if report_config else "")
    title = title or (report_config.title if report_config else "")

    run(csv_dir, templates_dir, manifest, output_dir, base_url, title)


def main():
    app()
