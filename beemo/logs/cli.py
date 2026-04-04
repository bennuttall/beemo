import sys
from pathlib import Path

from . import is_processed, process_log_file


DEFAULT_CSV_DIR = Path("csv")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Process Apache log gz files into CSV")
    parser.add_argument("input", type=Path, help="gz file or directory of gz files")
    parser.add_argument(
        "--csv-dir", type=Path, default=DEFAULT_CSV_DIR, help="Output directory (default: csv/)"
    )
    args = parser.parse_args()

    gz_files = sorted(args.input.rglob("*.gz")) if args.input.is_dir() else [args.input]

    for f in gz_files:
        if not is_processed(f, args.csv_dir):
            print(f"Processing {f}")
            n = process_log_file(f, args.csv_dir)
            print(f"  {n} rows -> {args.csv_dir / (f.name + '.csv')}")
