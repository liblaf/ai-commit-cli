from typing import Annotated, Optional

import typer

from aic import config, log
from aic.cli import list_models as cli_list
from aic.cli import main as cli_main

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
    log.init()
    if list_models:
        cli_list.list_models()
        return
    if pathspec is None:
        pathspec = []
    pathspec += [":!*-lock.*", ":!*.lock*", ":!*cspell*"]
    cfg: config.Config = config.load()
    if api_key is not None:
        cfg.api_key = api_key
    if base_url is not None:
        cfg.base_url = base_url
    if model is not None:
        cfg.model = model
    if max_tokens is not None:
        cfg.max_tokens = max_tokens
    cli_main.main(*pathspec, cfg=cfg, verify=verify)
