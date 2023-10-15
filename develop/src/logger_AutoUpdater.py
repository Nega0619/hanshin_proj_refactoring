from loguru import logger
logger.add(
    "AutoUpdater.log",
    rotation="500 MB",
    backtrace=True,
    format="{time}, {level}, {message}"
)