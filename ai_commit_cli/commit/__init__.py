import re
from collections.abc import Sequence
from typing import Optional

PATTERN: re.Pattern[str] = re.compile(
    r"(?P<type>\w+)(?:\((?P<scope>[^\)]+)\))?(?P<breaking>!)?: (?P<description>.+)"
)


def check(message: str) -> bool:
    title_line: str = message.splitlines()[0]
    return title_line == sanitize_line(title_line)


def sanitize(message: str) -> str:
    message = message.replace("```", "")
    message = re.sub(r"\n\n\n+", "\n\n", message)
    message = message.strip()
    lines: Sequence[str] = [sanitize_line(line) for line in message.splitlines()]
    return "\n".join(lines)


def sanitize_line(line: str) -> str:
    matches: Optional[re.Match[str]] = PATTERN.fullmatch(line)
    if matches is None:
        return line
    type_: str = matches.group("type")
    scope: Optional[str] = matches.group("scope")
    breaking: Optional[str] = matches.group("breaking")
    description: str = matches.group("description")
    type_ = type_.strip()
    line = type_
    if scope is not None:
        scope = scope.strip().lower()
        line += f"({scope})"
    if breaking is not None:
        line += "!"
    description = description.strip()
    description = description[0].lower() + description[1:]
    line += f": {description}"
    return line
