from typing import Annotated, Optional

import typer

from aic import config as _config
from aic import log as _log
from aic.cli import list_models as _list_models
from aic.cli import main as _main

app = typer.Typer(name="aic")


@app.command()
def main(
    pathspec: Annotated[Optional[list[str]], typer.Argument()] = None,  # noqa: UP007
    *,
    list_models: Annotated[bool, typer.Option()] = False,
    api_key: Annotated[Optional[str], typer.Option(envvar="OPENAI_API_KEY")] = None,  # noqa: UP007
    base_url: Annotated[Optional[str], typer.Option(envvar="OPENAI_BASE_URL")] = None,  # noqa: UP007
    model: Annotated[Optional[str], typer.Option()] = None,  # noqa: UP007
    max_tokens: Annotated[Optional[int], typer.Option()] = None,  # noqa: UP007
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
    if api_key is not None:
        config.api_key = api_key
    if base_url is not None:
        config.base_url = base_url
    if model is not None:
        config.model = model
    if max_tokens is not None:
        config.max_tokens = max_tokens
    _main.main(
        *pathspec,
        config=config,
        verify=verify,
    )
