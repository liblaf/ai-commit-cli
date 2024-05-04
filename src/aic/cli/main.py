import openai
from openai.types.chat import ChatCompletionChunk, ChatCompletionMessageParam
from rich.console import Group
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel

from aic import commit_lint as _lint
from aic import git as _git
from aic import pretty as _pretty
from aic import prompt as _prompt
from aic import token as _token
from aic.api import openrouter as _openrouter


def main(
    *pathspec: str,
    api_key: str | None,
    base_url: str | None,
    model: str,
    max_tokens: int,
    verify: bool,
) -> None:
    _git.status(*pathspec)
    diff: str = _git.diff(*pathspec)
    model_info: _openrouter.Model = _openrouter.get_model(f"openai/{model}")
    client = openai.OpenAI(api_key=api_key, base_url=base_url)
    prompt_builder = _prompt.Prompt()
    prompt_builder.ask()
    prompt: str = prompt_builder.build(diff, model_info, max_tokens)
    messages: list[ChatCompletionMessageParam] = [{"role": "user", "content": prompt}]
    prompt_tokens: int = _token.num_tokens_from_messages(messages, model)
    response: openai.Stream[ChatCompletionChunk] = client.chat.completions.create(
        messages=messages,
        model=model,
        max_tokens=max_tokens,
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
            completion_tokens: int = _token.num_tokens_from_string(completion, model)
            live.update(
                Group(
                    Panel(Markdown(_lint.sanitize(completion))),
                    Panel(
                        format_tokens(prompt_tokens, completion_tokens)
                        + "\n"
                        + format_cost(
                            prompt_tokens, completion_tokens, model_info.pricing
                        )
                    ),
                )
            )
    _git.commit(_lint.sanitize(completion), verify=verify)


def format_tokens(prompt_tokens: int, completion_tokens: int) -> str:
    total_tokens: int = prompt_tokens + completion_tokens
    return "Tokens: {} = {} (Prompt) + {} (Completion)".format(
        _pretty.format_int(total_tokens),
        _pretty.format_int(prompt_tokens),
        _pretty.format_int(completion_tokens),
    )


def format_cost(
    prompt_tokens: int, completion_tokens: int, pricing: _openrouter.Model.Pricing
) -> str:
    prompt_cost: float = prompt_tokens * pricing.prompt
    completion_cost: float = completion_tokens * pricing.completion
    total_cost: float = prompt_cost + completion_cost
    return "Cost: {} = {} (Prompt) + {} (Completion)".format(
        _pretty.format_currency(total_cost),
        _pretty.format_currency(prompt_cost),
        _pretty.format_currency(completion_cost),
    )
