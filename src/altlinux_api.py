import requests
import time
from typing import Optional, Dict, Any
from tqdm import tqdm
from src.config import config
from src.logging_config import log


class AltLinuxAPI:
    """Class to interact with ALT Linux API."""

    def __init__(self) -> None:
        self.base_url: str = config.base_url

    def fetch_packages(self, branch: str, arch: Optional[str] = None) -> Dict[str, Any]:
        """
        Fetches packages for a specific branch from the ALT Linux API.
        Args:
            branch (str): The branch for which packages are to be fetched.
            arch (Optional[str]): The architecture of the packages to fetch.
        Returns:
            Dict[str, Any]: A dictionary containing the fetched packages.
        Raises:
            requests.exceptions.RequestException: If there is an issue with the request.
        """
        if branch not in config.branches:
            log.error(f"Invalid branch '{branch}'. Allowed branches: {config.branches}")

        url: str = f"{self.base_url}/export/branch_binary_packages/{branch}"
        params: dict = {"arch": arch} if arch else {}
        log.debug(f"Fetching packages from URL: {url}")

        try:
            start_time: float = time.time()
            response: requests.Response = requests.get(url, params=params)
            response.raise_for_status()
            end_time: float = time.time()
            elapsed_time: float = end_time - start_time

            with tqdm(
                total=100, desc=f"Fetching data for {branch}", leave=True
            ) as pbar:

                for _ in range(100):
                    time.sleep(elapsed_time / 100)
                    pbar.update(1)

            log.success(f"Successfully fetched packages for branch {branch}")

            packages: Dict[str, Any] = response.json().get("packages")

            return packages

        except requests.exceptions.RequestException as e:
            log.error(f"Failed to fetch data for branch {branch}: {e}")
            return {}
