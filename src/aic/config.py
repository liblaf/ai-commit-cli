import pathlib
import tomllib

import pydantic
import typer


class Config(pydantic.BaseModel):
    api_key: str | None = None


def load() -> Config:
    app_dir = pathlib.Path(typer.get_app_dir("aic"))
    config_file: pathlib.Path = app_dir / "config.toml"
    if config_file.exists():
        with config_file.open("rb") as fp:
            return Config(**tomllib.load(fp))
    return Config()
