import functools
from collections.abc import Iterable

import tiktoken
from loguru import logger
from openai.types.chat import ChatCompletionMessageParam


@functools.lru_cache
def encoding_for_model(model: str) -> tiktoken.Encoding:
    try:
        return tiktoken.encoding_for_model(model)
    except KeyError as e:
        logger.error(e)
        return tiktoken.encoding_for_model("gpt-3.5-turbo")


@functools.lru_cache
def num_tokens_from_string(string: str, model: str) -> int:
    """Returns the number of tokens in a text string.

    https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken
    """
    encoding: tiktoken.Encoding = encoding_for_model(model)
    num_tokens: int = len(encoding.encode(string))
    return num_tokens


def num_tokens_from_messages(
    messages: Iterable[ChatCompletionMessageParam], model: str
) -> int:
    """Return the number of tokens used by a list of messages."""
    encoding: tiktoken.Encoding = encoding_for_model(model)
    tokens_per_message: int = 3
    tokens_per_name: int = 1
    num_tokens: int = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            assert isinstance(value, str)
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens
