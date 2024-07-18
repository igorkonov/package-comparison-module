import argparse
import pytest
from pytest_mock import MockerFixture
from src.cli import run_comparison, parse_args


def test_parse_args(mocker: MockerFixture) -> None:
    """
    Test function for parsing command-line arguments.
    """
    mocker.patch(
        "sys.argv", ["script_name", "--arch", "x86_64", "--output", "test_output"]
    )
    args: argparse.Namespace = parse_args()
    assert args.arch == "x86_64"
    assert args.output_file == "test_output"

    mocker.patch("sys.argv", ["script_name"])
    args = parse_args()
    assert args.arch is None
    assert args.output_file == "all_packages"


@pytest.mark.parametrize(
    "output_file", ["only_in_p10", "only_in_sisyphus", "higher_in_sisyphus"]
)
def test_run_comparison_specific_output(
    mocker: MockerFixture, output_file: str
) -> None:
    """
    Test the run_comparison function for specific output files.
    """
    mocker.patch(
        "src.altlinux_api.AltLinuxAPI.fetch_packages",
        return_value=[{"name": "test", "version": "1.0", "release": "1"}],
    )
    mocker.patch(
        "src.comparison.compare_packages",
        return_value={
            "only_in_p10": [{"name": "test1"}],
            "only_in_sisyphus": [{"name": "test2"}],
            "higher_in_sisyphus": [{"name": "test3"}],
        },
    )
    mocker.patch("src.cli.filter_package_data", return_value=[{"name": "filtered"}])

    result = run_comparison("x86_64", output_file)
    assert result is True


def test_run_comparison_fetch_error(mocker: MockerFixture) -> None:
    """
    Test the run_comparison function when a fetch error occurs.
    """
    mocker.patch(
        "src.altlinux_api.AltLinuxAPI.fetch_packages",
        side_effect=Exception("Fetch error"),
    )
    result = run_comparison("x86_64", "test_output")
    assert result is False


def test_run_comparison_filter_error(mocker: MockerFixture) -> None:
    """
    Test the run_comparison function when a filter error occurs.
    """
    mocker.patch(
        "src.altlinux_api.AltLinuxAPI.fetch_packages",
        return_value=[{"name": "test", "version": "1.0", "release": "1"}],
    )
    mocker.patch(
        "src.comparison.compare_packages",
        return_value={
            "only_in_p10": [{"name": "test"}],
            "only_in_sisyphus": [{"name": "test"}],
            "higher_in_sisyphus": [{"name": "test"}],
        },
    )
    mocker.patch("src.cli.filter_package_data", side_effect=Exception("Filter error"))
    result = run_comparison("x86_64", "test_output")
    assert result is False


def test_run_comparison_compare_error(mocker: MockerFixture) -> None:
    """
    Test the run_comparison function when a comparison error occurs.
    """
    mocker.patch(
        "src.altlinux_api.AltLinuxAPI.fetch_packages",
        return_value=[{"name": "test", "version": "1.0", "release": "1"}],
    )
    mocker.patch(
        "src.comparison.compare_packages",
        side_effect=Exception("Comparison error"),
    )
    result = run_comparison("x86_64", "all_packages")
    assert result is True
