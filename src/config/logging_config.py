"""Logging configuration"""

import os
from loguru import logger
from src.config.settings import settings

# Remove default handler
logger.remove()

# Create logs directory if it doesn't exist
os.makedirs(os.path.dirname(settings.log_file) or ".", exist_ok=True)

# Add console handler
logger.add(
    lambda msg: print(msg, end=""),
    level=settings.log_level,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{line} - {message}",
)

# Add file handler
logger.add(
    settings.log_file,
    level=settings.log_level,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    rotation="10 MB",
    retention="7 days",
)

__all__ = ["logger"]
