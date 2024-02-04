# ruff: noqa: E501

import dataclasses
import enum
from collections.abc import Mapping, Sequence
from typing import Any, Optional, Self

import questionary
from openai.types import chat

from ai_commit_cli import spec


class CommitType(enum.StrEnum):
    """https://github.com/commitizen/conventional-commit-types/blob/master/index.json"""

    FEAT = "feat"
    FIX = "fix"
    DOCS = "docs"
    STYLE = "style"
    REFACTOR = "refactor"
    PERF = "perf"
    TEST = "test"
    BUILD = "build"
    CI = "ci"
    CHORE = "chore"
    REVERT = "revert"

    @property
    def description(self) -> str:
        return DESCRIPTIONS[self]


DESCRIPTIONS: Mapping[CommitType, str] = {
    CommitType.FEAT: "A new feature",
    CommitType.FIX: "A bug fix",
    CommitType.DOCS: "Documentation only changes",
    CommitType.STYLE: "Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)",
    CommitType.REFACTOR: "A code change that neither fixes a bug nor adds a feature",
    CommitType.PERF: "A code change that improves performance",
    CommitType.TEST: "Adding missing tests or correcting existing tests",
    CommitType.BUILD: "Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)",
    CommitType.CI: "Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs)",
    CommitType.CHORE: "Other changes that don't modify src or test files",
    CommitType.REVERT: "Reverts a previous commit",
}


async def _ask_async(question: questionary.Question, patch_stdout: bool = False) -> Any:
    try:
        return await question.unsafe_ask_async(patch_stdout=patch_stdout)
    except KeyboardInterrupt:
        return None


@dataclasses.dataclass(kw_only=True)
class Prompt:
    spec: bool = True
    type_: Optional[CommitType] = None
    scope: Optional[str] = None
    breaking: Optional[bool] = None
    issue: Optional[str] = None

    async def ask(self) -> Self:
        if self.type_ is None:
            self.type_ = await _ask_async(
                questionary.select(
                    message="Select the type of change that you're committing",
                    choices=[
                        questionary.Choice(title=f"{t:<9} {t.description}", value=t)
                        for t in CommitType
                    ],
                ),
                patch_stdout=True,
            )
        if self.scope is None:
            self.scope = await _ask_async(
                questionary.text(
                    message="What is the scope of this change (e.g. component or file name)"
                ),
                patch_stdout=True,
            )
        if self.breaking is None:
            self.breaking = await _ask_async(
                questionary.confirm("Are there any breaking changes?"),
                patch_stdout=True,
            )
        if self.issue is None:
            self.issue = await _ask_async(
                questionary.text(
                    message='Add issue references (e.g. "fix #123", "re #123".)'
                ),
                patch_stdout=True,
            )
        return self

    def make(self, diff: str) -> Sequence[chat.ChatCompletionMessageParam]:
        system_content: str = ""
        if self.spec:
            system_content += spec.SPEC + "\n---\n\n"
        system_content += """You are to act as the author of a commit message in git. Your mission is to create clean and comprehensive commit messages as per the conventional commit convention and explain WHAT were the changes and mainly WHY the changes were done. I'll send you an output of `git diff --cached` command, and you are to convert it into a commit message. Add a short description of WHY the changes are done after the commit message. Don't start it with "This commit", just describe the changes. Use the present tense. Lines must not be longer than 100 characters. Use English for the commit message."""
        if self.type_ is None:
            system_content += " Determine the type of change based on the changes."
        else:
            system_content += f" The type of change is `{self.type_}`."
        if self.scope is None:
            system_content += " Determine the scope of change (e.g. component of file name) or omit the scope of change based on the changes."
        elif self.scope == "":
            system_content += " The scope of change is omitted."
        else:
            system_content += f" The scope of change is `{self.scope}`."
        if self.breaking is None:
            system_content += (
                " Determine if there are any breaking changes based on the changes."
            )
        elif self.breaking:
            system_content += " There are breaking changes."
        else:
            system_content += " There are no breaking changes."
        if self.issue is None:
            system_content += (
                " Determine if this change affect any open issues based on the changes."
            )
        elif self.issue == "":
            system_content += " This change does not affect any open issues."
        else:
            system_content += f" Add issue references: `{self.issue}`."
        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": diff},
        ]
