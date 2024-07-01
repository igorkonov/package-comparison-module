import pytest
from src.comparison import PackageComparator
from src.models import Package, ComparisonResult


@pytest.fixture
def package_comparator():
    """
    Fixture function to create an instance of PackageComparator for testing purposes.
    """
    return PackageComparator()


def test_compare_packages(package_comparator: PackageComparator):
    """
    Test function to compare packages using the provided PackageComparator instance.
    Args:
        package_comparator (PackageComparator): An instance of PackageComparator for testing.
    """
    package_comparator.packages = {
        "p10": [
            Package(
                name="pkg1",
                epoch=0,
                version="1.0",
                release="1",
                arch="x86_64",
                disttag="p10",
                buildtime=1234567890,
                source="src1",
            ),
            Package(
                name="pkg2",
                epoch=0,
                version="1.0",
                release="1",
                arch="x86_64",
                disttag="p10",
                buildtime=1234567890,
                source="src2",
            ),
        ],
        "sisyphus": [
            Package(
                name="pkg2",
                epoch=0,
                version="2.0",
                release="1",
                arch="x86_64",
                disttag="sisyphus",
                buildtime=1234567890,
                source="src2",
            ),
            Package(
                name="pkg3",
                epoch=0,
                version="1.0",
                release="1",
                arch="x86_64",
                disttag="sisyphus",
                buildtime=1234567890,
                source="src3",
            ),
        ],
    }

    result = package_comparator.compare_packages()

    assert isinstance(result, ComparisonResult)
    assert result.only_in_p10["count"] == 1
    assert result.only_in_sisyphus["count"] == 1
    assert result.higher_in_sisyphus["count"] == 2


def test_is_version_higher(package_comparator: PackageComparator):
    """
    Test if the version of pkg2 is higher than pkg1 using the provided PackageComparator instance.
    Args:
        package_comparator (PackageComparator): An instance of PackageComparator for testing.
    """
    pkg1: Package = Package(
        name="pkg",
        epoch=0,
        version="1.0",
        release="1",
        arch="x86_64",
        disttag="p10",
        buildtime=1234567890,
        source="src",
    )
    pkg2: Package = Package(
        name="pkg",
        epoch=0,
        version="2.0",
        release="1",
        arch="x86_64",
        disttag="sisyphus",
        buildtime=1234567890,
        source="src",
    )

    assert package_comparator._is_version_higher(pkg2, pkg1)
    assert not package_comparator._is_version_higher(pkg1, pkg2)
