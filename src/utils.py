import json
from typing import Any, Dict
from src.logging_config import log


def log_packages(packages: Dict[str, Any]) -> None:
    """
    Log packages information.
    Args:
        packages (Dict[str, Any]): A dictionary containing package information.
    """
    try:
        for branch, branch_packages in packages.items():
            for package in branch_packages:
                package_str: str = ", ".join(
                    f"{key}: {value}" for key, value in sorted(package.items())
                )
                log.info(f"{branch}: {package_str}")
    except Exception as e:
        log.error(f"Error logging packages: {e}")


def get_dump_json(data: Any, filename: str) -> None:
    """
    A function to dump JSON data to a file.
    Args:
        data: The JSON data to be dumped.
        filename: The name of the file to dump the JSON data into.
    """
    if data:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=2,
                ensure_ascii=False,
            )

        log.success(f"Data saved to {filename}")
    else:
        log.error("No data available. No output file created.")
