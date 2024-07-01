import requests
from src.logging_config import log
from src.config import config
from src.models import BranchPackages


class AltLinuxAPI:
    """Class to interact with ALT Linux API."""

    def __init__(self) -> None:
        self.base_url = config.base_url

    def get_branch_packages(self, branch: str) -> BranchPackages:
        """
        Retrieves the branch packages based on the provided branch name.
        Args:
            branch (str): The name of the branch to fetch packages from.
        Returns:
            BranchPackages: An instance of BranchPackages class containing the fetched packages.
        Raises:
            Exception: If the data retrieval for the specified branch fails.
        """
        url: str = f"{self.base_url}/export/branch_binary_packages/{branch}"
        log.debug(f"Fetching packages from URL: {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            log.error(f"Failed to fetch data for branch {branch}: {e}")
            raise Exception(f"Failed to fetch data for branch {branch}") from e
        packages: BranchPackages = BranchPackages(**response.json())
        log.success(f"Successfully fetched packages for branch {branch}")
        return packages
