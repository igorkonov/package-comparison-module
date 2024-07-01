import pytest
from src.altlinux_api import AltLinuxAPI
from src.models import BranchPackages
from pytest_mock import MockType


@pytest.fixture
def alt_linux_api():
    """
    Fixture function to create an instance of AltLinuxAPI for testing purposes.
    """
    return AltLinuxAPI()


def test_get_branch_packages_success(alt_linux_api: AltLinuxAPI, mocker: MockType):
    """
    Test function to validate successful retrieval of branch packages.
    Args:
        alt_linux_api (AltLinuxAPI): An instance of AltLinuxAPI for testing purposes.
        mocker (MockType): A mocker object for mocking requests.
    """
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        "request_args": {},
        "length": 1,
        "packages": [
            {
                "name": "test_package",
                "epoch": 0,
                "version": "1.0",
                "release": "1",
                "arch": "x86_64",
                "disttag": "p10",
                "buildtime": 1234567890,
                "source": "test_source",
            }
        ],
    }
    mock_response.raise_for_status.return_value = None
    mocker.patch("requests.get", return_value=mock_response)

    result = alt_linux_api.get_branch_packages("p10")
    assert isinstance(result, BranchPackages)
    assert len(result.packages) == 1
    assert result.packages[0].name == "test_package"


def test_get_branch_packages_failure(alt_linux_api: AltLinuxAPI, mocker: MockType):
    """
    Test function to validate failure in retrieving branch packages.
    Args:
        alt_linux_api (AltLinuxAPI): An instance of AltLinuxAPI for testing purposes.
        mocker (MockType): A mocker object for mocking requests.
    """
    mocker.patch("requests.get", side_effect=Exception("API error"))

    with pytest.raises(Exception):
        alt_linux_api.get_branch_packages("p10")


def test_get_branch_packages_no_packages(alt_linux_api: AltLinuxAPI, mocker: MockType):
    """
    Test function to validate retrieval of branch packages with no packages.
    Args:
        alt_linux_api (AltLinuxAPI): An instance of AltLinuxAPI for testing.
        mocker (MockType): A mocker object for mocking requests.
    """
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"request_args": {}, "length": 0, "packages": []}
    mock_response.raise_for_status.return_value = None
    mocker.patch("requests.get", return_value=mock_response)

    result = alt_linux_api.get_branch_packages("p10")
    assert isinstance(result, BranchPackages)
    assert len(result.packages) == 0
