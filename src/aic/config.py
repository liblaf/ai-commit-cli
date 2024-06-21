import pathlib
import tomllib

import pydantic
import typer

from aic.api import openrouter


class Config(pydantic.BaseModel):
    api_key: str | None = None
    base_url: str | None = None
    model: str = "gpt-3.5-turbo"
    max_tokens: int = 500
    pricing: openrouter.Pricing | None = None
    context_length: int | None = None


def load() -> Config:
    app_dir = pathlib.Path(typer.get_app_dir("aic"))
    config_file: pathlib.Path = app_dir / "config.toml"
    if config_file.exists():
        with config_file.open("rb") as fp:
            return Config(**tomllib.load(fp))
    return Config()
