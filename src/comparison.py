from typing import List, Dict
from version_utils import rpm


def compare_versions(version1: str, release1: str, version2: str, release2: str) -> int:
    """
    Compare two RPM version-release pairs.
    Args:
        version1 (str): The first version.
        release1 (str): The first release.
        version2 (str): The second version.
        release2 (str): The second release.
    Returns:
        int: The result of the comparison.
            1 if version1-release1 is greater than version2-release2,
            -1 if version1-release1 is less than version2-release2,
            0 if they are equal.
    """
    return rpm.compare_versions(f"{version1}-{release1}", f"{version2}-{release2}")


def compare_packages(packages_sisyphus: list[dict], packages_p10: list[dict]) -> dict:
    """
    Compares packages between sisyphus and p10 branches.
    Args:
        packages_sisyphus (list[dict]): List of packages from the sisyphus branch.
        packages_p10 (list[dict]): List of packages from the p10 branch.
    Returns:
        dict: Dictionary containing comparison results:
            - 'only_in_p10': List of packages only in p10.
            - 'only_in_sisyphus': List of packages only in sisyphus.
            - 'higher_in_sisyphus': List of packages with higher version-release in sisyphus.
    """
    packages_sisyphus_dict: dict = {pkg["name"]: pkg for pkg in packages_sisyphus}
    packages_p10_dict: dict = {pkg["name"]: pkg for pkg in packages_p10}

    only_in_p10: list = []
    only_in_sisyphus: list = []
    higher_in_sisyphus: list = []

    for name, pkg_p10 in packages_p10_dict.items():
        if name not in packages_sisyphus_dict:
            only_in_p10.append(pkg_p10)
        else:
            pkg_sisyphus = packages_sisyphus_dict[name]
            if (
                compare_versions(
                    pkg_sisyphus["version"],
                    pkg_sisyphus["release"],
                    pkg_p10["version"],
                    pkg_p10["release"],
                )
                > 0
            ):
                higher_in_sisyphus.append(pkg_sisyphus)

    for name, pkg_sisyphus in packages_sisyphus_dict.items():
        if name not in packages_p10_dict:
            only_in_sisyphus.append(pkg_sisyphus)

    return {
        "only_in_p10": only_in_p10,
        "only_in_sisyphus": only_in_sisyphus,
        "higher_in_sisyphus": higher_in_sisyphus,
    }


def filter_package_data(packages: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Filters out specific keys from a list of package dictionaries.
    Args:
        packages (List[Dict[str, str]]): List of package dictionaries.
    Returns:
        List[Dict[str, str]]: Filtered list of package dictionaries without keys 'epoch', 'disttag', 'arch', 'buildtime'.
    """
    return [
        {
            key: value
            for key, value in pkg.items()
            if key not in {"epoch", "disttag", "arch", "buildtime"}
        }
        for pkg in packages
    ]
