from src.comparison import compare_packages, compare_versions, filter_package_data


def test_compare_packages() -> None:
    """
    Test function for comparing packages between Sisyphus and p10 branches.
    """
    sisyphus_packages = [
        {"name": "pkg1", "version": "1.0", "release": "1"},
        {"name": "pkg2", "version": "2.0", "release": "1"},
        {"name": "pkg4", "version": "2.0", "release": "2"},
    ]
    p10_packages = [
        {"name": "pkg1", "version": "1.0", "release": "1"},
        {"name": "pkg3", "version": "3.0", "release": "1"},
        {"name": "pkg4", "version": "2.0", "release": "1"},
    ]

    result = compare_packages(sisyphus_packages, p10_packages)
    assert "only_in_p10" in result
    assert "only_in_sisyphus" in result
    assert "higher_in_sisyphus" in result

    assert result["only_in_p10"] == [{"name": "pkg3", "version": "3.0", "release": "1"}]
    assert result["only_in_sisyphus"] == [
        {"name": "pkg2", "version": "2.0", "release": "1"}
    ]
    assert result["higher_in_sisyphus"] == [
        {"name": "pkg4", "version": "2.0", "release": "2"}
    ]


def test_compare_packages_empty() -> None:
    """
    Test function for comparing empty packages between Sisyphus and p10 branches.
    """
    result = compare_packages([], [])
    assert result == {
        "only_in_sisyphus": [],
        "only_in_p10": [],
        "higher_in_sisyphus": [],
    }


def test_compare_versions() -> None:
    """
    Test function for comparing versions of RPM packages.
    """
    assert compare_versions("1.0", "1", "1.0", "1") == 0
    assert compare_versions("1.0", "1", "1.0", "2") < 0
    assert compare_versions("1.1", "1", "1.0", "1") > 0


def test_filter_package_data() -> None:
    """
    Test function for filtering package data.
    """
    packages = [
        {
            "name": "pkg1",
            "version": "1.0",
            "release": "1",
            "epoch": "0",
            "disttag": "alt",
            "arch": "x86_64",
            "buildtime": "123456",
        },
        {"name": "pkg2", "version": "2.0", "release": "1", "extra": "data"},
    ]
    filtered = filter_package_data(packages)
    assert filtered == [
        {"name": "pkg1", "version": "1.0", "release": "1"},
        {"name": "pkg2", "version": "2.0", "release": "1", "extra": "data"},
    ]


def test_filter_package_data_empty() -> None:
    """
    Test function for filtering empty package data.
    """
    assert filter_package_data([]) == []
