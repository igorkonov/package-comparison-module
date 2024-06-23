import requests
from config import config
from models import BranchPackages


class AltLinuxAPI:
    def __init__(self):
        self.base_url = config.base_url

    def get_branch_packages(self, branch: str) -> BranchPackages:
        url = f"{self.base_url}/export/branch_binary_packages/{branch}"
        response = requests.get(url)
        if response.status_code == 200:
            return BranchPackages(**response.json())
        else:
            raise Exception(f"Failed to fetch data for branch {branch}")
