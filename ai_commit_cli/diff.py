import dataclasses
import functools
import pathlib
from collections.abc import Sequence
from typing import Optional

from ai_commit_cli.cmd import git


@dataclasses.dataclass(kw_only=True)
class Diff:
    raw: Optional[str] = None
    file: Optional[pathlib.Path] = None
    pathspec: Sequence[str] = dataclasses.field(default_factory=list)

    def __post_init__(self) -> None:
        self.pathspec = [*self.pathspec, ":(exclude)*-lock.*", ":(exclude)*.lock"]

    @functools.cached_property
    async def content(self) -> str:
        if self.raw is not None:
            return self.raw
        if self.file is not None:
            return self.file.read_text()
        await git.status(self.pathspec)
        return await git.diff(self.pathspec)
