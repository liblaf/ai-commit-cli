from typing import TYPE_CHECKING

import openai
from rich.console import Group
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel

from aic import commit_lint as lint
from aic import config, git, pretty, prompt, token
from aic.api import openrouter

if TYPE_CHECKING:
    from openai.types import chat


def main(*pathspec: str, cfg: config.Config, verify: bool) -> None:
    git.status(*pathspec)
    diff: str = git.diff(*pathspec)
    model_info: openrouter.Model = openrouter.get_model(cfg.model)
    client = openai.OpenAI(api_key=cfg.api_key, base_url=cfg.base_url)
    prompt_builder = prompt.Prompt()
    prompt_builder.ask()
    prompt_str: str = prompt_builder.build(diff, model_info, cfg.max_tokens)
    messages: list[chat.ChatCompletionMessageParam] = [
        {"role": "user", "content": prompt_str}
    ]
    prompt_tokens: int = token.num_tokens_from_messages(messages, cfg.model)
    response: openai.Stream[chat.ChatCompletionChunk] = client.chat.completions.create(
        messages=messages,
        model=cfg.model,
        max_tokens=cfg.max_tokens,
        stream=True,
        temperature=0.2,
    )
    completion: str = ""
    with Live() as live:
        for chunk in response:
            content: str | None = chunk.choices[0].delta.content
            if content is None:
                completion += "\n"
            else:
                completion += content
            completion_tokens: int = token.num_tokens_from_string(completion, cfg.model)
            live.update(
                Group(
                    Panel(Markdown(lint.sanitize(completion))),
                    Panel(
                        format_tokens(prompt_tokens, completion_tokens)
                        + "\n"
                        + format_cost(
                            prompt_tokens, completion_tokens, model_info.pricing
                        )
                    ),
                )
            )
    git.commit(lint.sanitize(completion), verify=verify)


def format_tokens(prompt_tokens: int, completion_tokens: int) -> str:
    total_tokens: int = prompt_tokens + completion_tokens
    total: str = pretty.format_int(total_tokens)
    prompt: str = pretty.format_int(prompt_tokens)
    completion: str = pretty.format_int(completion_tokens)
    return f"Tokens: {total} = {prompt} (Prompt) + {completion} (Completion)"


def format_cost(
    prompt_tokens: int, completion_tokens: int, pricing: openrouter.Model.Pricing
) -> str:
    prompt_cost: float = prompt_tokens * pricing.prompt
    completion_cost: float = completion_tokens * pricing.completion
    total_cost: float = prompt_cost + completion_cost
    total: str = pretty.format_currency(total_cost)
    prompt: str = pretty.format_currency(prompt_cost)
    completion: str = pretty.format_currency(completion_cost)
    return f"Cost: {total} = {prompt} (Prompt) + {completion} (Completion)"
