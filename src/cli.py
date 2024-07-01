import click

from typing import List
from src.models import ComparisonResult
from src.altlinux_api import AltLinuxAPI
from src.comparison import PackageComparator
from src.config import config
from src.utils import get_dump_json, setup_pandas_display, log_summary, display_packages


def print_menu():
    """
    A function to print the menu options for the Package Comparison Tool.
    """
    click.echo(
        click.style("Welcome to the Package Comparison Tool!", fg="green", bold=True)
    )
    click.echo(click.style("Choose comparison type:", fg="yellow"))
    click.echo(click.style("1. Only in P10", fg="cyan"))
    click.echo(click.style("2. Only in Sisyphus", fg="cyan"))
    click.echo(click.style("3. Higher in Sisyphus", fg="cyan"))
    click.echo(click.style("4. All", fg="cyan"))
    click.echo(click.style("5. Exit", fg="red"))


@click.command()
def main():
    """
    Function to run the Package Comparison Tool.
    """
    setup_pandas_display()
    api = AltLinuxAPI()
    branch_p10: str = config.branch_p10
    branch_sisyphus: str = config.branch_sisyphus

    while True:
        print_menu()
        try:
            choice: int = click.prompt(
                click.style("Enter your choice (1-5)", fg="yellow"), type=int
            )
        except UnicodeDecodeError:
            click.echo(
                click.style("Invalid input. Please use UTF-8 characters.", fg="red")
            )
            continue

        if choice == 5:
            click.echo(click.style("Exiting the program. Goodbye!", fg="green"))
            return

        if choice < 1 or choice > 4:
            click.echo(click.style("Invalid choice. Please try again.", fg="red"))
            continue

        output_options: List[str] = [
            "only_in_p10",
            "only_in_sisyphus",
            "higher_in_sisyphus",
            "all",
        ]
        output_only: str = output_options[choice - 1]

        click.echo(
            click.style(
                f"Fetching packages for {branch_p10} and {branch_sisyphus}...",
                fg="yellow",
            )
        )
        p10_packages = api.get_branch_packages(branch_p10).packages
        sisyphus_packages = api.get_branch_packages(branch_sisyphus).packages

        if output_only == "only_in_p10":
            display_packages(p10_packages, "Packages only in P10:")
        elif output_only == "only_in_sisyphus":
            display_packages(sisyphus_packages, "Packages only in Sisyphus:")
        elif output_only == "higher_in_sisyphus":
            display_packages(sisyphus_packages, "Packages higher in Sisyphus:")
        elif output_only == "all":
            click.echo(click.style("All downloaded packages:", fg="cyan"))
            click.echo("Packages in P10:")
            display_packages(p10_packages, "Packages in P10:")
            click.echo("Packages in Sisyphus:")
            display_packages(sisyphus_packages, "Packages in Sisyphus:")

        comparator: PackageComparator = PackageComparator()
        comparator.packages["p10"] = p10_packages
        comparator.packages["sisyphus"] = sisyphus_packages

        click.echo(click.style("Comparing packages...", fg="yellow"))
        comparison_result: ComparisonResult = comparator.compare_packages()

        if comparison_result:
            log_summary(comparison_result, output_only)
            filename: str = f"comparison_{output_only}.json"
            if output_only == "all":
                get_dump_json(comparison_result, filename)
            else:
                get_dump_json(
                    {output_only: getattr(comparison_result, output_only)}, filename
                )
            click.echo(click.style(f"Results saved to {filename}", fg="green"))
        else:
            click.echo(
                click.style(
                    "No comparisons were successful. No output file created.", fg="red"
                )
            )

        try:
            if not click.confirm(
                click.style("Do you want to perform another comparison?", fg="yellow"),
                prompt_suffix=" ",
            ):
                click.echo(click.style("Exiting the program. Goodbye!", fg="green"))
                break
        except UnicodeDecodeError:
            click.echo(
                click.style(
                    "Error: Unable to process input. Please ensure your input is valid UTF-8.",
                    fg="red",
                )
            )


if __name__ == "__main__":
    main()
