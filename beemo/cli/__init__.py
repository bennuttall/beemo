from typer import Typer

from . import arguments, options
from .utils import get_config, require


app = Typer(no_args_is_help=True)


@app.command("build")
def do_build(
    pages_dir: options.pages_dir_opt = None,
    posts_dir: options.posts_dir_opt = None,
    static_dir: options.static_dir_opt = None,
    templates_dir: options.templates_dir_opt = None,
    output_dir: options.output_dir_opt = None,
    blog_root: options.blog_root_opt = None,
    base_url: options.base_url_opt = None,
):
    """
    Build the site.
    """
    from pathlib import Path

    from ..scribe import TheScribe
    from ..settings import BuildConfig

    config = get_config()
    build_config = config.build if config else None

    static_dir = require(
        static_dir or (build_config.static_dir if build_config else None), "build.static_dir"
    )
    templates_dir = require(
        templates_dir or (build_config.templates_dir if build_config else None),
        "build.templates_dir",
    )
    output_dir = require(
        output_dir or (build_config.output_dir if build_config else None), "build.output_dir"
    )
    pages_dir = pages_dir or (build_config.pages_dir if build_config else None)
    posts_dir = posts_dir or (build_config.posts_dir if build_config else None)
    blog_root = blog_root or (build_config.blog_root if build_config else Path())
    base_url = base_url or (build_config.base_url if build_config else None)

    TheScribe(
        BuildConfig(
            pages_dir=pages_dir,
            posts_dir=posts_dir,
            static_dir=static_dir,
            templates_dir=templates_dir,
            output_dir=output_dir,
            blog_root=blog_root,
            base_url=base_url,
        )
    ).build_site()


@app.command("logs")
def do_logs(
    input: arguments.gz_arg = None,
    csv_dir: options.logs_csv_dir_opt = None,
    pattern: options.pattern_opt = None,
):
    """
    Process Apache log gz files into CSV.
    """
    from ..logs.cli import run

    config = get_config()
    logs = config.logs if config else None

    input = require(input or (logs.logs_dir if logs else None), "logs.logs_dir")
    csv_dir = require(csv_dir or (logs.csv_dir if logs else None), "logs.csv_dir")
    pattern = pattern or (logs.pattern if logs else "*.gz")

    run(input, csv_dir, pattern)


@app.command("analytics")
def do_analytics(
    csv_dir: options.analytics_csv_dir_opt = None,
    templates_dir: options.templates_dir_opt = None,
    manifest: options.manifest_opt = None,
    output_dir: options.output_dir_opt = None,
    base_url: options.base_url_opt = None,
    title: options.title_opt = None,
):
    """
    Generate HTML analytics site from log CSVs.
    """
    from ..analytics.cli import run

    config = get_config()
    analytics_config = config.analytics if config else None

    csv_dir = require(
        csv_dir or (analytics_config.csv_dir if analytics_config else None), "analytics.csv_dir"
    )
    templates_dir = require(
        templates_dir or (analytics_config.templates_dir if analytics_config else None),
        "analytics.templates_dir",
    )
    output_dir = require(
        output_dir or (analytics_config.output_dir if analytics_config else None),
        "analytics.output_dir",
    )
    manifest_path = manifest or (analytics_config.manifest_path if analytics_config else None)
    base_url = base_url or (analytics_config.base_url if analytics_config else "")
    title = title or (analytics_config.title if analytics_config else "")

    run(csv_dir, templates_dir, manifest_path, output_dir, base_url, title)


def main():
    app()
