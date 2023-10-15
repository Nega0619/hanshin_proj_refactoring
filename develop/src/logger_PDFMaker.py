from loguru import logger
logger.add(
    "PDFMaker.log",
    rotation="500 MB",
    backtrace=True,
    format="{time}, {level}, {message}"
)