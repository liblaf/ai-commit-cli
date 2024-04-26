import inspect
import logging
import os
import sys

from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def init(level: str | int = logging.NOTSET) -> None:
    if level == logging.NOTSET:
        level = os.getenv("LOG_LEVEL", logging.NOTSET)
    if level == logging.NOTSET:
        level = logging.INFO
    logger.remove()
    logger.add(sys.stderr, level=level)
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
