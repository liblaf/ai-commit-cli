import string
from typing import Any

import questionary
import tiktoken
from loguru import logger

from aic import token as _token
from aic.api import openrouter as _openrouter
from aic.prompt import _type
from aic.prompt import template as _template

TEMPLATE: string.Template = string.Template(_template.TEMPLATE)


def _ask(question: questionary.Question) -> Any:
    try:
        return question.unsafe_ask()
    except KeyboardInterrupt:
        return None


class Prompt:
    type_: str | None = None
    scope: str | None = None
    breaking_change: str | None = None

    def ask(self) -> None:
        self.ask_type()
        self.ask_scope()
        self.ask_breaking_change()

    def ask_type(self) -> str | None:
        self.type_ = _ask(
            questionary.select(
                message="Select the type of change that you're committing",
                choices=[
                    questionary.Choice(title=f"{t:<9} {t.description}", value=t)
                    for t in _type.CommitType
                ],
            )
        )
        return self.type_

    def ask_scope(self) -> str | None:
        self.scope = _ask(
            questionary.text(
                "What is the scope of this change (e.g. component or file name)"
            )
        )
        return self.scope

    def ask_breaking_change(self) -> str | None:
        try:
            has_breaking_change: bool = questionary.confirm(
                "Are there any breaking changes?", default=False
            ).unsafe_ask()
            if not has_breaking_change:
                self.breaking_change = ""
                return self.breaking_change
            self.breaking_change = questionary.text(
                "Describe the breaking changes:"
            ).unsafe_ask()
        except KeyboardInterrupt:
            self.breaking_change = None
        return self.breaking_change

    def build(self, diff: str, model: _openrouter.Model, max_tokens: int) -> str:
        _: Any
        prompt: str = TEMPLATE.substitute(
            {
                "GIT_DIFF": diff,
                "TYPE": self.type_,
                "SCOPE": self.scope,
                "BREAKING_CHANGE": self.breaking_change,
            }
        )
        model_id: str
        _, _, model_id = model.id.partition("/")
        num_tokens: int = (
            _token.num_tokens_from_messages(
                [{"role": "user", "content": prompt}], model_id
            )
            + max_tokens
        )
        if num_tokens > model.context_length:
            encoding: tiktoken.Encoding = tiktoken.encoding_for_model(model_id)
            tokens: list[int] = encoding.encode(diff)
            origin_tokens: int = len(tokens)
            tokens_truncated: list[int] = tokens[: model.context_length - num_tokens]
            diff_truncated: str = encoding.decode(tokens_truncated)
            logger.warning(
                "Truncated diff from {} to {} tokens",
                origin_tokens,
                len(tokens_truncated),
            )
            prompt = TEMPLATE.substitute(
                {
                    "GIT_DIFF": diff_truncated,
                    "TYPE": self.type_,
                    "SCOPE": self.scope,
                    "BREAKING_CHANGE": self.breaking_change,
                }
            )
        logger.debug(prompt)
        return prompt
