from pytest_mock import MockerFixture
from src.altlinux_api import AltLinuxAPI


def test_fetch_packages_success(mocker: MockerFixture) -> None:
    """
    Test for successful fetching of packages.
    """
    api = AltLinuxAPI()
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"packages": [{"name": "test_package"}]}
    mocker.patch("requests.get", return_value=mock_response)

    result = api.fetch_packages("sisyphus", "x86_64")

    assert result == [{"name": "test_package"}]


def test_fetch_packages_empty_response(mocker: MockerFixture) -> None:
    """
    Test for successful fetching of packages when the response is empty.
    """
    api = AltLinuxAPI()
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"packages": []}
    mocker.patch("requests.get", return_value=mock_response)

    result = api.fetch_packages("sisyphus", "x86_64")

    assert result == []


def test_fetch_packages_invalid_branch(mocker: MockerFixture) -> None:
    """
    Test for fetching packages for an invalid branch.
    """
    api = AltLinuxAPI()
    mock_log_error = mocker.patch("src.altlinux_api.log.error")

    api.fetch_packages("invalid_branch", "x86_64")

    assert mock_log_error.call_count == 2

    first_call_args = mock_log_error.call_args_list[0][0][0]
    assert "Invalid branch 'invalid_branch'" in first_call_args
    assert "Allowed branches:" in first_call_args
    assert "p10" in first_call_args
    assert "sisyphus" in first_call_args

    second_call_args = mock_log_error.call_args_list[1][0][0]
    assert "Failed to fetch data for branch invalid_branch:" in second_call_args
    assert "400 Client Error: Bad Request for url:" in second_call_args
    assert (
        "https://rdb.altlinux.org/api/export/branch_binary_packages/invalid_branch?arch=x86_64"
        in second_call_args
    )
