"""Logging configuration and utilities."""

import sys
from pathlib import Path
from typing import Optional
from loguru import logger


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    rotation: str = "10 MB",
    retention: str = "1 week"
) -> None:
    """
    Configure application-wide logging with loguru.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_file: Optional path to log file. If None, only logs to console.
        rotation: When to rotate log files (e.g., "10 MB", "1 day").
        retention: How long to keep old log files (e.g., "1 week", "30 days").
    """
    # Remove default handler
    logger.remove()

    # Add console handler with colors
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=log_level.upper(),
        colorize=True
    )

    # Add file handler if specified
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        logger.add(
            log_file,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level=log_level.upper(),
            rotation=rotation,
            retention=retention,
            compression="zip",
            enqueue=True  # Thread-safe logging
        )

    logger.info(f"Logging configured with level: {log_level.upper()}")
    if log_file:
        logger.info(f"Logging to file: {log_file}")


def get_logger(name: str):
    """
    Get a logger instance for a specific module.

    Args:
        name: Name of the module requesting the logger.

    Returns:
        Logger instance bound to the module name.
    """
    return logger.bind(name=name)


class LoggerContext:
    """Context manager for temporary log level changes."""

    def __init__(self, level: str):
        """
        Initialize context with desired log level.

        Args:
            level: Temporary log level to use.
        """
        self.level = level.upper()
        self.previous_level = None

    def __enter__(self):
        """Enter context and change log level."""
        # Store current handlers and their levels
        self.handler_id = logger.add(
            sys.stderr,
            level=self.level,
            format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>"
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context and restore previous log level."""
        logger.remove(self.handler_id)


def log_function_call(func):
    """
    Decorator to log function calls with parameters and results.

    Args:
        func: Function to decorate.

    Returns:
        Wrapped function with logging.
    """
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        logger.debug(f"Calling {func_name} with args={args}, kwargs={kwargs}")

        try:
            result = func(*args, **kwargs)
            logger.debug(f"{func_name} completed successfully")
            return result
        except Exception as e:
            logger.error(f"{func_name} failed with error: {str(e)}")
            raise

    return wrapper
