import dataclasses


@dataclasses.dataclass(kw_only=True)
class Example:
    diff: str
    message: str
