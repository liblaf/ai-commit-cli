import logging

from rich import logging as rich_logging


def init(level: int | str = logging.NOTSET) -> None:
    handler: rich_logging.RichHandler = rich_logging.RichHandler(level=level)
    logging.basicConfig(
        format="%(message)s", datefmt="[%X]", level=level, handlers=[handler]
    )
