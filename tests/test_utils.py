from pytest_mock import MockerFixture
from src.utils import get_dump_json, log_packages


def test_get_dump_json_success(mocker: MockerFixture) -> None:
    """
    Test for successful dumping of data to a JSON file.
    """
    data = {"key": "value"}
    mock_open = mocker.patch("builtins.open", mocker.mock_open())
    mock_json_dump = mocker.patch("json.dump")
    mock_log = mocker.patch("src.utils.log")

    get_dump_json(data, "dummy_path")

    mock_open.assert_called_once_with("dummy_path", "w", encoding="utf-8")
    mock_json_dump.assert_called_once_with(
        data, mock_open(), indent=2, ensure_ascii=False
    )
    mock_log.success.assert_called_once_with("Data saved to dummy_path")


def test_get_dump_json_no_data(mocker: MockerFixture) -> None:
    """
    Test for logging an error when there is no data to dump.
    """
    mock_log = mocker.patch("src.utils.log")

    get_dump_json(None, "test.json")

    mock_log.error.assert_called_once_with("No data available. No output file created.")


def test_log_packages(mocker: MockerFixture) -> None:
    """
    Test for successful logging of packages.
    """
    mock_log = mocker.patch("src.utils.log")
    packages = {
        "sisyphus": [{"name": "pkg1", "version": "1.0", "release": "1"}],
        "p10": [{"name": "pkg2", "version": "2.0", "release": "1"}],
    }

    log_packages(packages)

    mock_log.info.assert_any_call("sisyphus: name: pkg1, release: 1, version: 1.0")
    mock_log.info.assert_any_call("p10: name: pkg2, release: 1, version: 2.0")


def test_log_packages_exception(mocker: MockerFixture) -> None:
    """
    Test for logging an exception when invalid data is provided to log_packages function.
    """
    mock_log = mocker.patch("src.utils.log")
    packages = {"invalid": "data"}

    log_packages(packages)

    mock_log.error.assert_called_once()
    assert "Error logging packages:" in mock_log.error.call_args[0][0]
