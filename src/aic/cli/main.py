import asyncio
import os
import pathlib
from collections.abc import Sequence
from typing import Annotated, Optional

import rich.console
import rich.live
import rich.markdown
import rich.text
import typer
from loguru import logger

from aic import log as _log
from aic import message as _message
from aic import prompt as _prompt
from aic import provider as _provider
from aic.cli import list_models as _list_models
from aic.cli import quota as _quota
from aic.proc import git as _git

app = typer.Typer(name="aic", add_completion=False)


async def _main(
    *,
    pathspec: Sequence[str] | None = None,
    diff_file: pathlib.Path | None = None,
    models: list[str] | None = None,
    provider: _provider.Provider,
    prompt: _prompt.Prompt,
    dry_run: bool = False,
    list_models: bool = False,
    quota: bool = False,
    stream: bool = True,
    truncate: bool = True,
    verify: bool = True,
) -> None:
    await provider.init(models)
    if list_models:
        await _list_models.list_models(provider)
        return
    if quota:
        await _quota.quota(provider)
        return
    await prompt.init(pathspec, diff_file=diff_file)
    await prompt.ask()
    message: str = ""
    if stream:
        with rich.live.Live() as live:
            async for response in provider.generate_stream(prompt, truncate=truncate):
                message = _message.sanitize(response.message)
                markdown = rich.markdown.Markdown(message)
                usage: list[str] = []
                if response.usage_predict is not None:
                    if (tokens := response.usage_predict.pretty_tokens()) is not None:
                        usage.append(f"Tokens (Predict): {tokens}")
                    if (cost := response.usage_predict.pretty_cost()) is not None:
                        usage.append(f"Cost (Predict): {cost}")
                if response.usage_actual is not None:
                    if (tokens := response.usage_actual.pretty_tokens()) is not None:
                        usage.append(f"Tokens (Actual): {tokens}")
                    if (cost := response.usage_actual.pretty_cost()) is not None:
                        usage.append(f"Cost (Actual): {cost}")
                group = rich.console.Group(
                    markdown, rich.text.Text("; ".join(usage), style="bold cyan")
                )
                live.update(group)
    else:
        response: _provider.Response = await provider.generate(
            prompt, truncate=truncate
        )
        message = _message.sanitize(response.message)
        if response.usage_predict is not None:
            if (tokens := response.usage_predict.pretty_tokens()) is not None:
                logger.info("Tokens (Predict): {}", tokens)
            if (cost := response.usage_predict.pretty_cost()) is not None:
                logger.info("Cost (Predict): {}", cost)
        if response.usage_actual is not None:
            if (tokens := response.usage_actual.pretty_tokens()) is not None:
                logger.info("Tokens (Actual): {}", tokens)
            if (cost := response.usage_actual.pretty_cost()) is not None:
                logger.info("Cost (Actual): {}", cost)
    if dry_run:
        print(message)
    else:
        await _git.commit(message, verify=verify)


@app.command()
def main(
    pathspec: Annotated[Optional[list[str]], typer.Argument()] = None,
    *,
    api_key: Annotated[Optional[str], typer.Option(envvar="OPENAI_API_KEY")] = None,
    base_url: Annotated[Optional[str], typer.Option(envvar="OPENAI_BASE_URL")] = None,
    diff: Annotated[
        Optional[pathlib.Path], typer.Option(exists=True, dir_okay=False)
    ] = None,
    models: Annotated[Optional[list[str]], typer.Option()] = None,
    provider: Annotated[
        _provider.ProviderEnum, typer.Option()
    ] = _provider.ProviderEnum.OPENAI,
    prompt: Annotated[
        _prompt.PromptEnum, typer.Option()
    ] = _prompt.PromptEnum.CONVENTIONAL,
    dry_run: Annotated[bool, typer.Option()] = False,
    list_models: Annotated[bool, typer.Option()] = False,
    quota: Annotated[bool, typer.Option()] = False,
    stream: Annotated[bool, typer.Option()] = True,
    truncate: Annotated[bool, typer.Option()] = True,
    verify: Annotated[bool, typer.Option()] = True,
) -> None:
    _log.init()
    if pathspec is None:
        pathspec = []
    if api_key is not None:
        os.environ["OPENAI_API_KEY"] = api_key
    if base_url is not None:
        os.environ["OPENAI_BASE_URL"] = base_url
    asyncio.run(
        _main(
            pathspec=pathspec,
            diff_file=diff,
            models=models,
            provider=provider.factory(),
            prompt=prompt.factory(),
            dry_run=dry_run,
            list_models=list_models,
            quota=quota,
            stream=stream,
            truncate=truncate,
            verify=verify,
        )
    )
