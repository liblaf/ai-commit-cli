import re

PATTERN: re.Pattern[str] = re.compile(
    r"(?P<type>\w+)(?:\((?P<scope>[^\)]+)\))?(?P<breaking>!)?: (?P<description>.+)"
)


def sanitize(msg: str) -> str:
    while True:
        msg_old: str = msg
        msg = msg.removeprefix("```").removesuffix("```")
        msg = msg.removeprefix("<Answer>").removesuffix("</Answer>")
        msg = msg.strip()
        if msg == msg_old:
            break
    lines: list[str] = [sanitize_line(line) for line in msg.splitlines()]
    return "\n".join(lines)


def sanitize_line(line: str) -> str:
    matches: re.Match[str] | None = PATTERN.fullmatch(line)
    if matches is None:
        return line
    type_: str = matches.group("type")
    scope: str | None = matches.group("scope")
    breaking: str | None = matches.group("breaking")
    description: str = matches.group("description")
    type_ = type_.strip().lower()
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
