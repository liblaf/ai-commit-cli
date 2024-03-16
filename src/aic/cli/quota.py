import babel.numbers
from loguru import logger

from aic import provider as _provider


async def quota(provider: _provider.Provider) -> None:
    quota: tuple[float, str] | None = await provider.quota()
    if quota is not None:
        print(
            babel.numbers.format_currency(
                quota[0], quota[1], decimal_quantization=False
            )
        )
    else:
        logger.error("Quota not available")
