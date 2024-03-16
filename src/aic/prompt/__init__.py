import enum

from aic.prompt.base import Prompt as Prompt
from aic.prompt.conventional import Conventional


class PromptEnum(enum.StrEnum):
    CONVENTIONAL = "conventional"

    @property
    def factory(self) -> type[Prompt]:
        return PROMPTS[self]


PROMPTS: dict[PromptEnum, type[Prompt]] = {
    PromptEnum.CONVENTIONAL: Conventional,
}
