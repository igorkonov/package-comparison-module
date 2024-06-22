import requests
import json
import pandas as pd

BASE_URL = "https://rdb.altlinux.org/api"


def get_branch_packages(branch):

    url = f"{BASE_URL}/export/branch_binary_packages/{branch}"
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

    # print(json.dumps(p10_packages, indent=4, sort_keys=True))
    df = pd.DataFrame(p10_packages)
    print(df)


if __name__ == "__main__":
    main()
