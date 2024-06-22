import requests
import json
import pandas as pd

from config import config
from utils import get_dump_json


def get_branch_packages(branch):

    url = f"{config.base_url}/export/branch_binary_packages/{branch}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['packages']
    else:
        raise Exception(f"Failed to fetch data for branch {branch}")


def main():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 200)
    pd.set_option('display.max_rows', 100)
    p10_packages = get_branch_packages('p10')
    get_dump_json(p10_packages)

    # print(json.dumps(p10_packages, indent=4, sort_keys=True))
    df = pd.DataFrame(p10_packages)
    print(df)


if __name__ == "__main__":
    main()
