"""
Logging utilities for Iago Deluxe
"""

import logging
import sys


def setup_logger(
    name: str = "iago_deluxe", level: int = logging.INFO
) -> logging.Logger:
    """Setup and configure logger"""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(console_handler)

    return logger


def get_logger(name: str = "iago_deluxe") -> logging.Logger:
    """Get configured logger instance"""
    return logging.getLogger(name)


# Global logger instance
logger = setup_logger()
