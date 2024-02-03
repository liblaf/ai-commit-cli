import dataclasses
import datetime
import functools
from collections.abc import Mapping, Sequence

import tiktoken
from loguru import logger
from openai.types import chat


class Model:
    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    def num_tokens_from_string(self, text: str) -> int:
        """Returns the number of tokens in a text string."""
        tokens: Sequence[int] = self.encoding.encode(text)
        return len(tokens)

    def num_tokens_from_messages(
        self, messages: Sequence[chat.ChatCompletionMessageParam]
    ) -> int:
        """Return the number of tokens used by a list of messages."""
        try:
            encoding: tiktoken.Encoding = self.encoding
        except KeyError:
            logger.warning("model not found. Using cl100k_base encoding.")
            encoding = tiktoken.get_encoding("cl100k_base")
        num_tokens: int = 0
        tokens_per_message: int
        tokens_per_name: int
        tokens_per_message, tokens_per_name = self.tokens_per
        for msg in messages:
            num_tokens += tokens_per_message
            for key, value in msg.items():
                num_tokens += len(encoding.encode(str(value)))
                if key == "name":
                    num_tokens += tokens_per_name
        num_tokens += 3
        return num_tokens

    @property
    def encoding(self) -> tiktoken.Encoding:
        """Returns the encoding used by a model.

        Raises a KeyError if the model name is not recognised.
        """
        return tiktoken.encoding_for_model(self.name)

    @property
    def encoding_name(self) -> str:
        """Returns the name of the encoding used by a model.

        Raises a KeyError if the model name is not recognised.
        """
        return tiktoken.encoding_name_for_model(self.name)

    @functools.cached_property
    def tokens_per(self) -> tuple[int, int]:
        if self.name in {
            "gpt-3.5-turbo-0613",
            "gpt-3.5-turbo-16k-0613",
            "gpt-4-0314",
            "gpt-4-32k-0314",
            "gpt-4-0613",
            "gpt-4-32k-0613",
        }:
            return 3, 1
        elif self.name == "gpt-3.5-turbo-0301":
            return (
                4,  # every message follows <|start|>{role/name}\n{content}<|end|>\n
                -1,  # if there's a name, the role is omitted
            )
        elif "gpt-3.5-turbo" in self.name:
            logger.warning(
                "gpt-3.5-turbo may update over time. "
                "Returning num tokens assuming gpt-3.5-turbo-0613."
            )
            return Model("gpt-3.5-turbo-0613").tokens_per
        elif "gpt-4" in self.name:
            logger.warning(
                "gpt-4 may update over time. "
                "Returning num tokens assuming gpt-4-0613."
            )
            return Model("gpt-4-0613").tokens_per
        else:
            raise NotImplementedError(
                f"""tokens_per_message() is not implemented for model {self}. \
See https://github.com/openai/openai-python/blob/main/chatml.md for information on how \
messages are converted to tokens."""
            )

    @property
    def context(self) -> int:
        return CONTEXT[self.name]

    @property
    def pricing(self) -> tuple[float, float]:
        return PRICING[self.name]

    @property
    def point_to(self) -> "Model":
        return Model(TO.get(self.name, self.name))


CONTEXT: Mapping[str, int] = {
    # GPT-4 and GPT-4 Turbo
    "gpt-4-0125-preview": 128000,
    "gpt-4-turbo-preview": 128000,
    "gpt-4-1106-preview": 128000,
    "gpt-4-vision-preview": 128000,
    "gpt-4": 8192,
    "gpt-4-0613": 8192,
    "gpt-4-32k": 32768,
    "gpt-4-32k-0613": 32768,
    # GPT-3.5 Turbo
    "gpt-3.5-turbo-0125": 16385,
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-1106": 16385,
    "gpt-3.5-turbo-instruct": 4096,
    "gpt-3.5-turbo-16k": 16385,
    "gpt-3.5-turbo-0613": 4096,
    "gpt-3.5-turbo-16k-0613": 16385,
}

PRICING: Mapping[str, tuple[float, float]] = {
    # GPT-4 Turbo
    "gpt-4-0125-preview": (0.01, 0.01),
    "gpt-4-1106-preview": (0.01, 0.01),
    "gpt-4-1106-vision-preview": (0.01, 0.01),
    # GPT-4
    "gpt-4": (0.03, 0.06),
    "gpt-4-32k": (0.06, 0.12),
    # GPT-3.5 Turbo
    "gpt-3.5-turbo-0125": (0.0005, 0.0015),
    "gpt-3.5-turbo-instruct": (0.0015, 0.0020),
    # Older models
    "gpt-3.5-turbo-1106": (0.0010, 0.0020),
    "gpt-3.5-turbo-0613": (0.0015, 0.0020),
    "gpt-3.5-turbo-16k-0613": (0.0030, 0.0040),
    "gpt-3.5-turbo-0301": (0.0015, 0.0020),
}


TO: Mapping[str, str] = {
    # GPT-4 and GPT-4 Turbo
    "gpt-4-turbo-preview": "gpt-4-0125-preview",
    "gpt-4": "gpt-4-0613",
    "gpt-4-32k": "gpt-4-32k-0613",
    # GPT-3.5 Turbo
    "gpt-3.5-turbo": "gpt-3.5-turbo-0125"
    if datetime.date.today() >= datetime.date(year=2024, month=2, day=16)
    else "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-16k": "gpt-3.5-turbo-16k-0613",
}


@dataclasses.dataclass(kw_only=True)
class Params:
    models: Sequence[Model]
    max_tokens: int = 500
    temperature: float = 0.2

    def select_model(self, msg: Sequence[chat.ChatCompletionMessageParam]) -> Model:
        for model in self.models:
            num_tokens: int = model.num_tokens_from_messages(msg)
            if num_tokens + self.max_tokens <= model.context:
                return model
        return self.models[0]
