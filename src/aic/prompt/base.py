import abc
import dataclasses
import functools
import pathlib
from collections.abc import Sequence

import openai.types.chat

from aic import example as _example
from aic.proc import git as _git


@dataclasses.dataclass(kw_only=True)
class Prompt(abc.ABC):
    _diff: str = ""

    async def init(
        self,
        pathspec: Sequence[str] | None = None,
        diff_file: pathlib.Path | None = None,
    ) -> None:
        if diff_file is not None:
            self._diff = diff_file.read_text()
        else:
            if pathspec is None:
                pathspec = []
            pathspec = [*pathspec, ":!.cspell.json", ":!*-lock.*", ":!*.lock"]
            self._diff = await _git.diff(pathspec)

    async def ask(self) -> None: ...

    @property
    @abc.abstractmethod
    def messages(self) -> list[openai.types.chat.ChatCompletionMessageParam]:
        messages: list[openai.types.chat.ChatCompletionMessageParam] = [
            {"role": "system", "content": self.prompt}
        ]
        for example in self.examples:
            messages.append({"role": "user", "content": example.diff})
            messages.append({"role": "assistant", "content": example.message})
        messages.append({"role": "user", "content": self.diff})
        return messages

    @property
    def prompt(self) -> str:
        return ""

    @functools.cached_property
    def diff(self) -> str:
        return self._diff

    @property
    def examples(self) -> list[_example.Example]:
        return []
