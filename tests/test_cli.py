import pytest
from click.testing import CliRunner
from pytest_mock import MockType
from src.cli import main


@pytest.fixture
def cli_runner():
    """
    Fixture function to create an instance of CliRunner for testing purposes.
    """
    return CliRunner()


def test_cli_menu(cli_runner: CliRunner):
    """
    Test for CLI menu functionality.
    Args:
        cli_runner (CliRunner): An instance of CliRunner for testing purposes.
    """
    result = cli_runner.invoke(main, input="5\n")
    assert result.exit_code == 0
    assert "Welcome to the Package Comparison Tool!" in result.output
    assert "Exiting the program. Goodbye!" in result.output


@pytest.mark.parametrize("choice", [1, 2, 3, 4])
def test_cli_comparison_types(cli_runner: CliRunner, mocker: MockType, choice: int):
    """
    Test CLI comparison types with specified choices.
    Args:
        cli_runner (CliRunner): An instance of CliRunner for testing purposes.
        mocker (MockType): A mocker object for mocking purposes.
        choice (int): The choice for comparison testing.
    """
    mocker.patch(
        "src.cli.AltLinuxAPI.get_branch_packages",
        return_value=mocker.Mock(packages=[]),
    )
    result = cli_runner.invoke(main, input=f"{choice}\nn\n")
    assert result.exit_code == 0
    assert "Fetching packages for p10 and sisyphus..." in result.output
    assert "Comparing packages..." in result.output


def test_invalid_choice(cli_runner: CliRunner):
    """
    Test for invalid choice handling.
    Args:
        cli_runner (CliRunner): An instance of CliRunner for testing purposes.
    """
    result = cli_runner.invoke(main, input="6\n5\n")
    assert result.exit_code == 0
    assert "Invalid choice. Please try again." in result.output


def test_no_comparisons(cli_runner: CliRunner, mocker: MockType):
    """
    Test for no comparisons made.
    Args:
        cli_runner (CliRunner): An instance of CliRunner for testing purposes.
        mocker (MockType): A mocker object for mocking purposes.
    """
    mocker.patch(
        "src.cli.AltLinuxAPI.get_branch_packages",
        return_value=mocker.Mock(packages=[]),
    )
    result = cli_runner.invoke(main, input="1\nn\n")
    assert result.exit_code == 0
    assert "Exiting the program. Goodbye!" in result.output
