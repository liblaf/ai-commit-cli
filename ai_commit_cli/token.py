import logging
from collections.abc import Sequence

import tiktoken
from openai.types import chat


# https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken
def num_tokens_from_string(string: str, model: str = "gpt-3.5-turbo") -> int:
    """Returns the number of tokens in a text string."""
    encoding: tiktoken.Encoding
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        logging.warning("model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens: int = len(encoding.encode(string))
    return num_tokens


# https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken
def num_tokens_from_messages(
    messages: Sequence[chat.ChatCompletionMessageParam], model: str = "gpt-3.5-turbo"
) -> int:
    """Return the number of tokens used by a list of messages."""
    encoding: tiktoken.Encoding
    tokens_per_message: int
    tokens_per_name: int
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        logging.warning("model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_message = 4
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        logging.warning(
            "gpt-3.5-turbo may update over time. "
            "Returning num tokens assuming gpt-3.5-turbo-0613."
        )
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        logging.warning(
            "gpt-4 may update over time. Returning num tokens assuming gpt-4-0613."
        )
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"num_tokens_from_messages() is not implemented for model {model}."
        )
    num_tokens: int = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


# https://openai.com/pricing
def pricing(model: str = "gpt-3.5-turbo") -> tuple[float, float]:
    if model.startswith("gpt-4-1106"):
        return 0.01 / 1e3, 0.03 / 1e3
    elif model.startswith("gpt-4-32k"):
        return 0.06 / 1e3, 0.12 / 1e3
    elif model.startswith("gpt-4"):
        return 0.03 / 1e3, 0.06 / 1e3
    elif model.startswith("gpt-3.5"):
        return 0.0010 / 1e3, 0.0020 / 1e3
    raise NotImplementedError(f"princing() is not implemented for model {model}.")
