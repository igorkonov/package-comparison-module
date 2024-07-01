from loguru import logger
import sys


def setup_logger() -> logger:
    """
    Set up logger configuration with various log levels and formats for console and file outputs.
    Returns:
        logger: The configured logger object.
    """
    logger.remove()

    logger.add(
        sys.stderr,
        level="DEBUG",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<blue>{message}</blue>",
        filter=lambda record: record["level"].name == "DEBUG",
    )
    logger.add(
        sys.stderr,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "{message}",
        filter=lambda record: record["level"].name == "INFO",
    )
    logger.add(
        sys.stderr,
        level="SUCCESS",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<green>{message}</green>",
        filter=lambda record: record["level"].name == "SUCCESS",
    )
    logger.add(
        sys.stderr,
        level="WARNING",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<yellow>{message}</yellow>",
        filter=lambda record: record["level"].name == "WARNING",
    )
    logger.add(
        sys.stdout,
        level="ERROR",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<red>{message}</red>",
        filter=lambda record: record["level"].name == "ERROR",
    )

    logger.add(
        "logs/debug.log",
        rotation="100 MB",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
        compression="zip",
    )
    logger.add(
        "logs/info.log",
        rotation="100 MB",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
        compression="zip",
    )
    logger.add(
        "logs/warning.log",
        rotation="100 MB",
        level="WARNING",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
        compression="zip",
    )
    logger.add(
        "logs/error.log",
        rotation="100 MB",
        level="ERROR",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
        compression="zip",
    )

    return logger


log = setup_logger()
