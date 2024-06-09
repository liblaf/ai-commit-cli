import pathlib
import tomllib

import pydantic
import typer


class Config(pydantic.BaseModel):
    api_key: str | None = None
    base_url: str | None = None
    model: str = "gpt-3.5-turbo"
    max_tokens: int = 500

    class Pricing(pydantic.BaseModel):
        prompt: float | None = None
        completion: float | None = None
        request: float | None = None
        image: float | None = None

    pricing: Pricing | None = None
    context_length: int | None = None


def load() -> Config:
    app_dir = pathlib.Path(typer.get_app_dir("aic"))
    config_file: pathlib.Path = app_dir / "config.toml"
    if config_file.exists():
        with config_file.open("rb") as fp:
            return Config(**tomllib.load(fp))
    return Config()
