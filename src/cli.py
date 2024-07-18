import argparse
from argparse import ArgumentParser
from src.altlinux_api import AltLinuxAPI
from src.config import config
from src.utils import get_dump_json, log_packages
from src.comparison import compare_packages, filter_package_data
from src.logging_config import log


def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments.
    Returns:
        argparse.Namespace: The parsed command line arguments.
    """
    parser: ArgumentParser = ArgumentParser(
        prog="compare_packages",
        description="Compare binary packages between sisyphus and p10 branches.",
        usage="compare_packages [-a <arch>] [-o <output_file>]",
    )
    parser.add_argument(
        "-a",
        "--arch",
        dest="arch",
        help="Specify the architecture to compare (x86_64, ppc64le, i586, armh, aarch64).",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_file",
        help="Specify the output JSON file to save (only_in_p10, only_in_sisyphus, higher_in_sisyphus, all_packages).",
        default="all_packages",
    )
    return parser.parse_args()


def run_comparison(arch: str, output_file: str) -> bool:
    """
    Runs the package comparison for the specified architecture and saves the result to a JSON file.
    Args:
        arch (str): The architecture to compare.
        output_file (str): The name of the output JSON file.
    Returns:
        bool: True if the comparison and saving were successful, False otherwise.
    """
    api: AltLinuxAPI = AltLinuxAPI()

    log.info(f"Fetching packages for architecture: {arch}")

    packages: dict = {}
    try:
        for branch in config.branches:
            packages[branch] = api.fetch_packages(branch, arch)
    except Exception as e:
        log.error(f"Error fetching packages: {e}")
        return False

    log_packages(packages)

    try:
        comparison_result: dict = compare_packages(
            packages["sisyphus"], packages["p10"]
        )
    except Exception as e:
        log.error(f"Error comparing packages: {e}")
        return False

    try:
        comparison_result["only_in_p10"] = filter_package_data(
            comparison_result["only_in_p10"]
        )
        comparison_result["only_in_sisyphus"] = filter_package_data(
            comparison_result["only_in_sisyphus"]
        )
        comparison_result["higher_in_sisyphus"] = filter_package_data(
            comparison_result["higher_in_sisyphus"]
        )
    except Exception as e:
        log.error(f"Error processing packages: {e}")
        return False

    try:
        if output_file == "only_in_p10":
            data_to_save = {output_file: {arch: comparison_result["only_in_p10"]}}
        elif output_file == "only_in_sisyphus":
            data_to_save = {output_file: {arch: comparison_result["only_in_sisyphus"]}}
        elif output_file == "higher_in_sisyphus":
            data_to_save = {
                output_file: {arch: comparison_result["higher_in_sisyphus"]}
            }
        else:
            data_to_save: dict = {output_file: {arch: comparison_result}}

        get_dump_json(data_to_save, f"{output_file}.json")
        return True

    except Exception as e:
        log.error(f"Error saving {output_file}.json: {e}")
        return False
