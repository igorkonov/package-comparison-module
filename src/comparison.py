from collections import defaultdict
from typing import List, Dict, Callable, Optional
from src.models import Package, ComparisonResult, PackageInfo
from packaging.version import Version, InvalidVersion


class PackageComparator:
    """
    A class to compare packages between P10 and Sisyphus sources.
    """

    def __init__(self) -> None:
        self.packages = {"p10": [], "sisyphus": []}

    @staticmethod
    def _group_packages(packages: List[Package]) -> Dict[tuple, Package]:
        """
        Group packages by architecture and name.
        Parameters:
            packages (List[Package]): List of packages to group.
        Returns:
            Dict[tuple, Package]: Dictionary with keys as (arch, name) tuple and values as Package objects.
        """
        return {(pkg.arch, pkg.name): pkg for pkg in packages}

    @staticmethod
    def _filter_package_fields(pkg: Package) -> Dict[str, str]:
        """
        Filter package fields to only include necessary ones.
        Parameters:
            pkg (Package): Package to filter fields from.
        Returns:
            Dict[str, str]: Dictionary with filtered package fields.
        """
        return {
            "name": pkg.name,
            "version": pkg.version,
            "release": pkg.release,
            "arch": pkg.arch,
        }

    def _compare_packages_generic(
        self, include_in_result: Callable[[Optional[Package], Optional[Package]], bool]
    ) -> Dict[str, PackageInfo]:
        """
        Generic method to compare packages using a provided comparison function.
        Parameters:
            include_in_result (Callable[[Optional[Package], Optional[Package]], bool]):
             Function to decide if a package should be included in the result.
        Returns:
            Dict[str, PackageInfo]: Dictionary containing the comparison results.
        """
        result = defaultdict(list)

        p10_pkgs = self._group_packages(self.packages["p10"])
        sisyphus_pkgs = self._group_packages(self.packages["sisyphus"])

        all_keys = set(p10_pkgs.keys()).union(sisyphus_pkgs.keys())

        for key in all_keys:
            p10_pkg = p10_pkgs.get(key)
            sisyphus_pkg = sisyphus_pkgs.get(key)

            if include_in_result(p10_pkg, sisyphus_pkg):
                if p10_pkg:
                    result[p10_pkg.arch].append(self._filter_package_fields(p10_pkg))
                if sisyphus_pkg:
                    result[sisyphus_pkg.arch].append(
                        self._filter_package_fields(sisyphus_pkg)
                    )

        return {
            arch: PackageInfo(count_arches=len(pkgs), packages=pkgs)
            for arch, pkgs in result.items()
        }

    def compare_packages(self) -> ComparisonResult:
        """
        Compares packages between P10 and Sisyphus sources and categorizes them into different groups.
        Returns:
            ComparisonResult: A named tuple containing the comparison results.
        """
        only_in_p10_result = self._compare_packages_generic(
            lambda p10, sisyphus: p10 is not None and sisyphus is None
        )
        only_in_sisyphus_result = self._compare_packages_generic(
            lambda p10, sisyphus: sisyphus is not None and p10 is None
        )
        higher_in_sisyphus_result = self._compare_packages_generic(
            lambda p10, sisyphus: p10 is not None
            and sisyphus is not None
            and self._is_version_higher(sisyphus, p10)
        )

        return ComparisonResult(
            only_in_p10={
                "count": sum(info.count_arches for info in only_in_p10_result.values()),
                **only_in_p10_result,
            },
            only_in_sisyphus={
                "count": sum(
                    info.count_arches for info in only_in_sisyphus_result.values()
                ),
                **only_in_sisyphus_result,
            },
            higher_in_sisyphus={
                "count": sum(
                    info.count_arches for info in higher_in_sisyphus_result.values()
                ),
                **higher_in_sisyphus_result,
            },
        )

    @staticmethod
    def _is_version_higher(pkg_1: Package, pkg_2: Package) -> bool:
        """
        Compares the versions of two packages and returns True if the first package version is higher than the second.
        Parameters:
            pkg_1 (Package): The first package to compare.
            pkg_2 (Package): The second package to compare.
        Returns:
            bool: True if pkg1 version is higher, False otherwise.
        """
        try:
            version1: Version = Version(pkg_1.version)
            version2: Version = Version(pkg_2.version)
            return version1 > version2
        except InvalidVersion:
            return False
