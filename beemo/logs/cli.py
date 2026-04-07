from pathlib import Path

from . import is_processed, process_log_file


DEFAULT_LOGS_DIR = Path("apache2")
DEFAULT_CSV_DIR = Path("csv")
DEFAULT_PATTERN = "*.gz"


def _load_config_defaults():
    try:
        from beemo.settings import get_config
        return get_config().logs
    except Exception:
        return None


def add_arguments(parser):
    logs_config = _load_config_defaults()
    parser.add_argument(
        "input", nargs="?", type=Path,
        default=logs_config.logs_dir if logs_config else DEFAULT_LOGS_DIR,
        help="gz file or directory of gz files (default: apache2/)",
    )
    parser.add_argument(
        "--csv-dir", type=Path,
        default=logs_config.csv_dir if logs_config else DEFAULT_CSV_DIR,
        help="Output directory (default: csv/)",
    )
    parser.add_argument(
        "--pattern",
        default=logs_config.pattern if logs_config else DEFAULT_PATTERN,
        help="Filename glob pattern when input is a directory (default: *.gz)",
    )


def run(args):
    gz_files = sorted(args.input.rglob(args.pattern)) if args.input.is_dir() else [args.input]
    for f in gz_files:
        if not is_processed(f, args.csv_dir):
            print(f"Processing {f}")
            n = process_log_file(f, args.csv_dir)
            print(f"  {n} rows -> {args.csv_dir / (f.name + '.csv')}")
