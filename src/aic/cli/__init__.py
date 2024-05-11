from typing import Annotated

import typer

from aic import config as _config
from aic import log as _log
from aic.cli import list_models as _list_models
from aic.cli import main as _main

app = typer.Typer(name="aic")


@app.command()
def main(
    pathspec: Annotated[list[str] | None, typer.Argument()] = None,
    *,
    list_models: Annotated[bool, typer.Option()] = False,
    api_key: Annotated[str | None, typer.Option(envvar="OPENAI_API_KEY")] = None,
    base_url: Annotated[str | None, typer.Option(envvar="OPENAI_BASE_URL")] = None,
    model: Annotated[str, typer.Option()] = "gpt-3.5-turbo",
    max_tokens: Annotated[int, typer.Option()] = 500,
    verify: Annotated[bool, typer.Option()] = True,
) -> None:
    _log.init()
    if list_models:
        _list_models.list_models()
        return
    if pathspec is None:
        pathspec = []
    pathspec += [":!*-lock.*", ":!*.lock*", ":!*cspell*"]
    config: _config.Config = _config.load()
    if api_key is None:
        api_key = config.api_key
    _main.main(
        *pathspec,
        api_key=api_key,
        base_url=base_url,
        model=model,
        max_tokens=max_tokens,
        verify=verify,
    )
