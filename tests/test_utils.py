import sys

from typing import List
from src.utils import display_packages
from src.models import Package
from io import StringIO


def test_display_packages():
    """
    Test function for displaying packages.
    """
    packages: List[Package] = [
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
            version="2.0",
            release="1",
            arch="x86_64",
            disttag="p10",
            buildtime=1234567890,
            source="src2",
        ),
    ]

    captured_output: StringIO = StringIO()
    sys.stdout = captured_output

    display_packages(packages, "Test Header")

    sys.stdout = sys.__stdout__

    output: str = captured_output.getvalue()

    assert "Test Header" in output
    assert "pkg1" in output
    assert "pkg2" in output
