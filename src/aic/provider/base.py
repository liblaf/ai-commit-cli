import abc
import dataclasses
import datetime
from collections.abc import AsyncGenerator, Sequence

import babel.numbers
from loguru import logger

from aic import prompt as _prompt


@dataclasses.dataclass(kw_only=True)
class Pricing:
    currency: str
    input: float
    output: float


@dataclasses.dataclass(kw_only=True)
class Model:
    id: str
    created: datetime.datetime | None = None
    context_window: int | None = None
    pricing: Pricing | None = None


@dataclasses.dataclass(kw_only=True)
class Usage:
    completion_tokens: int | None = None
    prompt_tokens: int | None = None
    total_tokens: int | None = None

    cost: float | None = None
    currency: str | None = None

    def pretty_tokens(self) -> str | None:
        if (
            self.total_tokens is not None
            and self.prompt_tokens is not None
            and self.completion_tokens is not None
        ):
            return "{} = {} + {}".format(
                babel.numbers.format_number(self.total_tokens),
                babel.numbers.format_number(self.prompt_tokens),
                babel.numbers.format_number(self.completion_tokens),
            )
        return None

    def pretty_cost(self) -> str | None:
        if self.cost is not None and self.currency is not None:
            return babel.numbers.format_currency(
                self.cost, self.currency, decimal_quantization=False
            )
        return None


@dataclasses.dataclass(kw_only=True)
class Response:
    message: str
    usage_predict: Usage | None = None
    usage_actual: Usage | None = None


class Provider(abc.ABC):
    models: Sequence[str]
    max_tokens: int = 500
    temperature: float = 0.2

    async def init(self, models: Sequence[str] | None = None) -> None:
        if models is not None:
            self.models = models

    async def list_models(self) -> AsyncGenerator[Model, None]: ...

    async def quota(self) -> tuple[float, str] | None:
        return None

    def context_window(self, model: str) -> int | None:
        return None

    def pricing(self, model: str) -> Pricing | None:
        return None

    @abc.abstractmethod
    async def generate(
        self, prompt: _prompt.Prompt, *, truncate: bool = True
    ) -> Response: ...

    async def generate_stream(
        self, prompt: _prompt.Prompt, *, truncate: bool = True
    ) -> AsyncGenerator[Response, None]:
        yield await self.generate(prompt, truncate=truncate)

    def select_model(self, prompt: _prompt.Prompt) -> str:
        for model in self.models:
            context_window: int | None = self.context_window(model)
            if context_window is None:
                logger.success('using "{}"', model)
                return model
            tokens: int = self.count_tokens(model, prompt)
            if tokens + self.max_tokens <= context_window:
                logger.success(
                    'using "{}": {} + {} <= {} tokens',
                    model,
                    tokens,
                    self.max_tokens,
                    context_window,
                )
                return model
            logger.error(
                'skipping "{}": {} + {} > {} tokens',
                model,
                tokens,
                self.max_tokens,
                context_window,
            )
        logger.warning('fallback to "{}"', self.models[0])
        return self.models[0]

    @abc.abstractmethod
    def count_tokens(self, model: str, prompt: _prompt.Prompt) -> int: ...

    @abc.abstractmethod
    def truncate(self, model: str, prompt: _prompt.Prompt) -> _prompt.Prompt: ...
