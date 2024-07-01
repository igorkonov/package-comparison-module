import json
import click
import pandas as pd

from typing import List, Any
from tqdm import tqdm
from src.models import Package, ComparisonResult
from src.logging_config import log


def display_packages(packages: List[Package], header: str) -> None:
    """
    A function to display packages with specific information.

    Parameters:
        packages: The list of packages to display.
        header: The header text to display before the packages.
    """
    click.echo(click.style(header, fg="cyan"))
    package_lines = [
        (
            f"{package.name}, {package.version}, {package.release},"
            f" {package.arch}, {package.disttag}, {package.buildtime}, {package.source}"
        )
        for package in packages
    ]

    with tqdm(
        total=len(package_lines),
        desc="Downloading",
        bar_format="{l_bar}{bar}",
        position=0,
        leave=True,
    ) as pbar:
        for line in package_lines:
            pbar.update(1)
            click.echo(line)


def setup_pandas_display():
    """
    Set display options for pandas to customize the way data is shown.
    """
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    pd.set_option("display.max_colwidth", 200)
    pd.set_option("display.max_rows", 100)


def log_summary(comparison_result: ComparisonResult, output_only: str) -> None:
    """
    Log the summary of package counts based on the comparison result and the output type.

    Parameters:
        comparison_result: The result of the comparison between P10 and Sisyphus sources.
        output_only: The type of summary to log, either 'all' for all summary or a specific category.
    """
    summary = {
        "only_in_p10": [
            comparison_result.only_in_p10["count"],
            [arch for arch in comparison_result.only_in_p10.keys() if arch != "count"],
        ],
        "only_in_sisyphus": [
            comparison_result.only_in_sisyphus["count"],
            [
                arch
                for arch in comparison_result.only_in_sisyphus.keys()
                if arch != "count"
            ],
        ],
        "higher_in_sisyphus": [
            comparison_result.higher_in_sisyphus["count"],
            [
                arch
                for arch in comparison_result.higher_in_sisyphus.keys()
                if arch != "count"
            ],
        ],
    }

    if output_only == "all":
        df_summary = pd.DataFrame.from_dict(
            summary, orient="index", columns=["count_arches", "arch"]
        )
        log.warning(
            "\n"
            + "Summary of package counts by category:"
            + "\n"
            + "=================================="
            + "\n"
            + df_summary.to_string()
            + "\n"
            + "=================================="
        )
    else:
        detailed_summary = {output_only: summary[output_only]}
        df_detailed = pd.DataFrame(detailed_summary, index=["count_arches", "arch"])
        log.warning(
            "\n"
            + f"Detailed summary for {output_only}:"
            + "\n"
            + "=================================="
            + "\n"
            + df_detailed.transpose().to_string()
            + "\n"
            + "=================================="
        )


def get_dump_json(data: Any, filename: str) -> None:
    """
    A function to dump JSON data to a file.
    Parameters:
        data: The JSON data to be dumped.
        filename: The name of the file to dump the JSON data into.
    """
    if data:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=2,
                ensure_ascii=False,
                default=lambda o: o.model_dump(),
            )

        log.success(f"Data saved to {filename}")
    else:
        log.error("No data available. No output file created.")
