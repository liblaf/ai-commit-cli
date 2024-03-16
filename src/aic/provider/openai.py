import datetime
import os
from collections.abc import AsyncGenerator, Iterable, Sequence

import openai
import openai.types.chat
import tiktoken
from loguru import logger

from aic import prompt as _prompt
from aic.proc import bw as _bw
from aic.provider import base as _base

CONTEXT_WINDOW: dict[str, int] = {
    # GPT-4 and GPT-4 Turbo
    "gpt-4-0125-preview": 128_000,
    "gpt-4-turbo-preview": 128_000,  # gpt-4-0125-preview
    "gpt-4": 8_192,  # gpt-4-0613
    "gpt-4-0613": 8_192,
    "gpt-4-32k": 32_768,  # gpt-4-32k-0613
    "gpt-4-32k-0613": 32_768,
    # GPT-3.5 Turbo
    "gpt-3.5-turbo-0125": 16_385,
    "gpt-3.5-turbo": 16_385,
}


PRICING: dict[str, tuple[float, float]] = {
    # GPT-4 Turbo
    "gpt-4-0125-preview": (10.00, 10.00),
    "gpt-4-turbo-preview": (10.00, 10.00),  # gpt-4-0125-preview
    # GPT-4
    "gpt-4": (30.00, 60.00),
    "gpt-4-0613": (30.00, 60.00),
    "gpt-4-32k": (60.00, 120.00),
    "gpt-4-32k-0613": (60.00, 120.00),
    # GPT-3.5 Turbo
    "gpt-3.5-turbo-0125": (0.50, 1.50),
    "gpt-3.5-turbo": (0.50, 1.50),
}


class OpenAI(_base.Provider):
    client: openai.AsyncOpenAI

    async def init(self, models: Sequence[str] | None = None) -> None:
        self.models = models or ["gpt-3.5-turbo-0125"]
        api_key: str | None = os.getenv("OPENAI_API_KEY")
        if not api_key:
            api_key = await _bw.get_notes("OPENAI_API_KEY")
        self.client = openai.AsyncOpenAI(api_key=api_key)

    async def list_models(self) -> AsyncGenerator[_base.Model, None]:
        async for model in self.client.models.list():
            if model.id in CONTEXT_WINDOW:
                yield _base.Model(
                    id=model.id,
                    created=datetime.datetime.fromtimestamp(model.created),
                    context_window=self.context_window(model.id),
                    pricing=self.pricing(model.id),
                )

    def context_window(self, model: str) -> int | None:
        if (window := CONTEXT_WINDOW.get(model)) is not None:
            return window
        return None

    def pricing(self, model: str) -> _base.Pricing | None:
        if (pricing := PRICING.get(model)) is not None:
            return _base.Pricing(
                currency="USD", input=pricing[0] / 1e6, output=pricing[1] / 1e6
            )
        return None

    async def generate(
        self, prompt: _prompt.Prompt, *, truncate: bool = True
    ) -> _base.Response:
        model: str = self.select_model(prompt)
        if truncate:
            prompt = self.truncate(model, prompt)
        response: openai.types.chat.ChatCompletion = (
            await self.client.chat.completions.create(
                messages=prompt.messages,
                model=model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
        )
        logger.debug(response)
        assert response.choices[0].message.content
        message: str = response.choices[0].message.content
        assert response.usage
        usage_actual = _base.Usage(**response.usage.model_dump())
        assert usage_actual.prompt_tokens is not None
        assert usage_actual.completion_tokens is not None
        if (pricing := self.pricing(response.model)) is not None:
            usage_actual.currency = pricing.currency
            usage_actual.cost = (
                pricing.input * usage_actual.prompt_tokens
                + pricing.output * usage_actual.completion_tokens
            )
        return _base.Response(
            message=message,
            usage_predict=self.predict_usage(model, prompt, message),
            usage_actual=usage_actual,
        )

    async def generate_stream(
        self, prompt: _prompt.Prompt, *, truncate: bool = True
    ) -> AsyncGenerator[_base.Response, None]:
        model: str = self.select_model(prompt)
        if truncate:
            prompt = self.truncate(model, prompt)
        response: openai.AsyncStream[
            openai.types.chat.ChatCompletionChunk
        ] = await self.client.chat.completions.create(
            messages=prompt.messages,
            model=model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            stream=True,
        )
        message: str = ""
        async for chunk in response:
            logger.debug(response)
            if (content := chunk.choices[0].delta.content) is not None:
                message += content
            else:
                message += "\n"
            yield _base.Response(
                message=message,
                usage_predict=self.predict_usage(model, prompt, message),
            )

    def count_tokens(self, model: str, prompt: _prompt.Prompt) -> int:
        return num_tokens_from_messages(prompt.messages, model) + 3

    def predict_usage(
        self, model: str, prompt: _prompt.Prompt, message: str
    ) -> _base.Usage:
        prompt_tokens: int = self.count_tokens(model, prompt)
        completion_tokens: int = len(tiktoken.encoding_for_model(model).encode(message))
        usage = _base.Usage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        )
        assert usage.prompt_tokens is not None
        assert usage.completion_tokens is not None
        if (pricing := self.pricing(model)) is not None:
            usage.currency = pricing.currency
            usage.cost = (
                pricing.input * usage.prompt_tokens
                + pricing.output * usage.completion_tokens
            )
        return usage

    def truncate(self, model: str, prompt: _prompt.Prompt) -> _prompt.Prompt:
        context_window: int | None = self.context_window(model)
        if context_window is None:
            logger.warning('Context Window not available for "{}"', model)
            return prompt
        num_tokens: int = self.count_tokens(model, prompt) + self.max_tokens
        if num_tokens <= context_window:
            return prompt
        encoding: tiktoken.Encoding
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            logger.warning("model not found. Using cl100k_base encoding.")
            encoding = tiktoken.get_encoding("cl100k_base")
        tokens: list[int] = encoding.encode(prompt.diff)
        tokens_truncated: list[int] = tokens[: num_tokens - context_window]
        prompt.diff = encoding.decode(tokens_truncated)
        logger.warning(
            "Truncated diff from {} to {} tokens", len(tokens), len(tokens_truncated)
        )
        return prompt


def num_tokens_from_string(string: str, model: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding: tiktoken.Encoding
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        logger.warning("model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens: int = len(encoding.encode(string))
    return num_tokens


def num_tokens_from_messages(
    messages: Iterable[openai.types.chat.ChatCompletionMessageParam], model: str
) -> int:
    """Return the number of tokens used by a list of messages.

    https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken"""
    encoding: tiktoken.Encoding
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        logger.warning("model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    tokens_per_message: int = 3
    tokens_per_name: int = 1
    num_tokens: int = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(str(value)))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens
