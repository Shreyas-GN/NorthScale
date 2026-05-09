import sys
from loguru import logger

def setup_logging():
    # Remove default handler
    logger.remove()
    
    # Add standard output handler with institutional format
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO"
    )
    
    # Add error file handler
    logger.add(
        "logs/error.log",
        rotation="10 MB",
        retention="10 days",
        level="ERROR",
        compression="zip"
    )

    return logger
