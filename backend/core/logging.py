import sys
from loguru import logger
from core.config import settings

def setup_logging():
    # Remove default handler
    logger.remove()

    # Determine log level
    log_level = "DEBUG" if settings.DEBUG else "INFO"

    # Standard Console Handler (Structured if production)
    if settings.ENVIRONMENT == "production":
        # In production, we might want JSON formatting for ELK/Cloudwatch
        # For now, keeping loguru's clean format but with higher level
        logger.add(
            sys.stdout,
            level=log_level,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
            serialize=True # This enables JSON output
        )
    else:
        logger.add(
            sys.stdout,
            level=log_level,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            colorize=True
        )

    # File Handler for persistence
    logger.add(
        "logs/backend.log",
        rotation="10 MB",
        retention="10 days",
        level="INFO",
        compression="zip",
        serialize=(settings.ENVIRONMENT == "production")
    )

    logger.info(f"Logging initialized with level: {log_level}")

setup_logging()
