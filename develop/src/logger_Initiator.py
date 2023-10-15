from loguru import logger
logger.add(
    "Initiator.log",
    rotation="500 MB",
    backtrace=True,
    format="{time}, {level}, {message}"
)