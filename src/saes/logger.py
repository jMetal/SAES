"""Standardized logging configuration using Rich."""

from __future__ import annotations

import logging
import os

from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme

# Theme definitions for the level styles
custom_theme = Theme(
    {
        "logging.level.info": "white on blue",
        "logging.level.debug": "white on red",
    }
)

console = Console(theme=custom_theme)


def get_logger(name: str) -> logging.Logger:
    """Returns a configured logger instance using Rich.

    Args:
        name: The name of the logger, typically ``__name__``.

    Returns:
        A pre-configured :class:`logging.Logger` instance.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        # Default to INFO, but allow override via environment variable
        level_str = os.getenv("LOG_LEVEL", "INFO").upper()

        handler = RichHandler(
            console=console,
            rich_tracebacks=True,
            show_time=True,
            show_path=(level_str == "DEBUG"),
            markup=True,
        )

        handler.setFormatter(logging.Formatter("%(name)s | %(message)s"))

        logger.addHandler(handler)
        logger.propagate = False

        if hasattr(logging, level_str) and level_str in (
            "DEBUG",
            "INFO",
            "WARNING",
            "ERROR",
            "CRITICAL",
        ):
            logger.setLevel(getattr(logging, level_str))
        else:
            logger.setLevel(logging.INFO)

    return logger
