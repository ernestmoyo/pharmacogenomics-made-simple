"""
PGx Clinical Solutions - Logging Configuration
================================================
Centralized logging for all platform modules.

Console: INFO level, clean format for terminal output.
File:    DEBUG level, timestamped, writes to output/logs/.
"""

import logging
import os
from datetime import datetime
from pathlib import Path

# Platform version — single source of truth
PLATFORM_VERSION = "0.5.0"

# Log directory
LOG_DIR = Path(__file__).parent.parent.parent / "output" / "logs"

_initialized = False


def _init_logging():
    """Initialize root logger with console and file handlers."""
    global _initialized
    if _initialized:
        return
    _initialized = True

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    root = logging.getLogger("pgx")
    root.setLevel(logging.DEBUG)

    # Console handler — INFO, clean format
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter("  %(message)s"))
    root.addHandler(console)

    # File handler — DEBUG, timestamped
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = LOG_DIR / f"run_{timestamp}.log"
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(name)-30s | %(levelname)-7s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))
    root.addHandler(file_handler)

    root.debug(f"PGx Clinical Solutions Platform v{PLATFORM_VERSION}")
    root.debug(f"Log file: {log_file}")


def get_logger(name: str) -> logging.Logger:
    """Get a named logger under the pgx namespace.

    Usage:
        from src.utils.logger import get_logger
        logger = get_logger(__name__)
        logger.info("Loading knowledge base...")
    """
    _init_logging()
    return logging.getLogger(f"pgx.{name}")
