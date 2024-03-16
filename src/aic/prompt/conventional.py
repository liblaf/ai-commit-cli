# ruff: noqa: E501

import dataclasses
import enum
from typing import Any, Optional

import openai.types.chat
import questionary
import rich

from aic.prompt import base as _base


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


DESCRIPTIONS: dict[CommitType, str] = {
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


async def _ask_async(question: questionary.Question, patch_stdout: bool = True) -> Any:
    try:
        return await question.unsafe_ask_async(patch_stdout=patch_stdout)
    except KeyboardInterrupt:
        return None


@dataclasses.dataclass(kw_only=True)
class Conventional(_base.Prompt):
    type_: Optional[CommitType] = None
    scope: Optional[str] = None
    breaking: Optional[bool] = None
    issue: Optional[str] = None

    async def ask(self) -> None:
        """https://github.com/commitizen/cz-conventional-changelog/blob/master/engine.js"""
        console = rich.console.Console()
        console.print("? Ctrl+C to skip any question.", style="bold cyan")
        if self.type_ is None:
            self.type_ = await _ask_async(
                questionary.select(
                    message="Select the type of change that you're committing",
                    choices=[
                        questionary.Choice(title=f"{t:<9} {t.description}", value=t)
                        for t in CommitType
                    ],
                )
            )
        if self.scope is None:
            self.scope = await _ask_async(
                questionary.text(
                    message="What is the scope of this change (e.g. component or file name)"
                )
            )
        if self.breaking is None:
            self.breaking = await _ask_async(
                questionary.confirm("Are there any breaking changes?", default=False)
            )
        if self.issue is None:
            self.issue = await _ask_async(
                questionary.text(
                    message='Add issue references (e.g. "fix #123", "re #123".)'
                )
            )

    @property
    def messages(self) -> list[openai.types.chat.ChatCompletionMessageParam]:
        return [
            {
                "role": "system",
                "content": """You are an advanced AI programming assistant tasked with summarizing code changes into a concise and meaningful commit message. Compose a commit message that:
- Strictly synthesizes meaningful information from the provided code diff
- Utilizes any additional user-provided context to comprehend the rationale behind the code changes
- Is clear and brief, with an informal yet professional tone, and without superfluous descriptions
- Avoids unnecessary phrases such as "this commit", "this change", and the like
- Avoids direct mention of specific code identifiers, names, or file names, unless they are crucial for understanding the purpose of the changes
- Most importantly emphasizes the 'why' of the change, its benefits, or the problem it addresses rather than only the 'what' that changed

Follow the user's instructions carefully, don't repeat yourself, don't include the code in the output, or make anything up!""",
            },
            {
                "role": "user",
                "content": f"Here is the code diff to use to generate the commit message:\n\n{self.diff}",
            },
            {
                "role": "user",
                "content": f"Here is additional instructions you should follow:\n\n{self.instructions}",
            },
            {
                "role": "user",
                "content": "Now, please generate a commit message using Conventional Commits format. Ensure that it includes a precise and informative subject line that succinctly summarizes the crux of the changes in under 50 characters. If necessary, follow with an explanatory body providing insight into the nature of the changes, the reasoning behind them, and any significant consequences or considerations arising from them. Conclude with any relevant issue references at the end of the message.",
            },
        ]

    @property
    def instructions(self) -> str:
        content: str = ""

        if self.type_ is None:
            content += "- Determine the type of change based on the changes, available types are:\n"
            for t in CommitType:
                content += f"  - {t}: {t.description}\n"
            pass
        else:
            content += (
                f"- The type of change is `{self.type_}`: {self.type_.description}.\n"
            )

        if self.scope is None:
            content += "- Determine the scope of change (e.g. component of file name) or omit the scope of change based on the changes.\n"
            pass
        elif self.scope == "":
            content += "- Do not add scope of change in commit message.\n"
        else:
            content += f"- The scope of change is `{self.scope}`.\n"

        if self.breaking is None:
            content += (
                "- Determine if there are any breaking changes based on the changes.\n"
            )
        elif self.breaking:
            content += "- There are breaking changes.\n"
        else:
            content += "- Do not add breaking changes in commit message.\n"

        if self.issue is None:
            content += "- Determine if this change affect any open issues based on the changes.\n"
            pass
        elif self.issue == "":
            content += "- Do not add issue references in commit message.\n"
        else:
            content += f"- Add issue references: `{self.issue}`.\n"
        return content
