# ruff: noqa: E501
import enum


class CommitType(enum.StrEnum):
    """https://github.com/commitizen/conventional-commit-types/blob/master/index.json."""

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
