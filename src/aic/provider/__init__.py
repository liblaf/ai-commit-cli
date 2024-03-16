import enum

from aic.provider.base import Pricing as Pricing
from aic.provider.base import Provider as Provider
from aic.provider.base import Response as Response
from aic.provider.openai import OpenAI


class ProviderEnum(enum.StrEnum):
    OPENAI = "openai"

    @property
    def factory(self) -> type[Provider]:
        return PROVIDERS[self]


PROVIDERS: dict[str, type[Provider]] = {
    ProviderEnum.OPENAI: OpenAI,
}
