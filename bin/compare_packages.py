#!/usr/bin/env python3
from src.cli import run_comparison, parse_args
from src.logging_config import log


def main():
    args = parse_args()
    success = run_comparison(args.arch, args.output_file)
    if success:
        log.success("Comparison completed successfully.")
    else:
        log.error("Comparison failed.")
        exit(1)


if __name__ == "__main__":
    main()
