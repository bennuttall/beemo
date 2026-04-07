import argparse

from .logs.cli import add_arguments as add_logs_arguments, run as run_logs
from .reports.cli import add_arguments as add_report_arguments, run as run_report


def main():
    parser = argparse.ArgumentParser(prog="beemo")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("build", help="Build the site")

    logs_parser = subparsers.add_parser("logs", help="Process Apache log gz files into CSV")
    add_logs_arguments(logs_parser)

    report_parser = subparsers.add_parser("report", help="Generate HTML analytics report")
    add_report_arguments(report_parser)

    args = parser.parse_args()

    if args.command == "build":
        from .scribe import TheScribe
        TheScribe().build_site()
    elif args.command == "logs":
        run_logs(args)
    elif args.command == "report":
        run_report(args)
