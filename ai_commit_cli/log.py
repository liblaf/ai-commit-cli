import enum
import inspect
import logging
import os
import pathlib
import sys
from typing import Optional

import loguru


class Level(enum.StrEnum):
    """https://github.com/Delgan/loguru/blob/master/loguru/_defaults.py"""

    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        level: str | int
        try:
            level = loguru.logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        loguru.logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def init(
    level: Optional[int | str] = None, file: Optional[pathlib.Path] = None
) -> None:
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    if level is None:
        level = os.getenv("LOG_LEVEL")
    if level is not None:
        loguru.logger.remove()
        loguru.logger.add(sys.stderr, level=level)
    if file is None and (f := os.getenv("LOG_FILE")):
        file = pathlib.Path(f)
    if file is not None:
        loguru.logger.add(file)
