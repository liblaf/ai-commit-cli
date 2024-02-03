import asyncio
import pathlib
import shutil
from collections.abc import Sequence
from typing import Annotated, Optional, cast

import openai
import typer
from loguru import logger
from openai import _streaming
from openai.types import chat
from rich import live, markdown

from ai_commit_cli import diff as _diff
from ai_commit_cli import gpt, log, msg
from ai_commit_cli import prompt as _prompt
from ai_commit_cli.cmd import bw, git
from ai_commit_cli.cmd import pre_commit as _pre_commit

app: typer.Typer = typer.Typer(name="aic")


async def main_async(
    *,
    pre_commit: bool,
    diff: _diff.Diff,
    prompt: _prompt.Prompt,
    params: gpt.Params,
    api_key: str,
) -> None:
    if pre_commit:
        await _pre_commit.run()
    prompt = await prompt.ask()
    completion_msg: Sequence[chat.ChatCompletionMessageParam] = prompt.make(
        diff=await diff.content
    )
    logger.debug(completion_msg)
    system_msg: chat.ChatCompletionSystemMessageParam = cast(
        chat.ChatCompletionSystemMessageParam, completion_msg[0]
    )
    user_msg: chat.ChatCompletionUserMessageParam = cast(
        chat.ChatCompletionUserMessageParam, completion_msg[1]
    )
    model: gpt.Model = params.select_model(msg=completion_msg)
    price_in: float
    price_out: float
    price_in, price_out = model.pricing
    logger.info(
        "Model: {}; ${} / 1K tokens (in), ${} / 1K tokens (out)",
        model.name,
        price_in,
        price_out,
    )
    input_tokens: int = model.num_tokens_from_messages(completion_msg)
    system_tokens: int = model.num_tokens_from_string(system_msg["content"])
    user_tokens: int = model.num_tokens_from_string(str(user_msg["content"]))
    logger.info(
        "Input Tokens: {:,} = {:,} (system) + {:,} (user) + {:,}",
        input_tokens,
        system_tokens,
        user_tokens,
        input_tokens - system_tokens - user_tokens,
    )
    client: openai.AsyncOpenAI = openai.AsyncOpenAI(api_key=api_key)
    response: _streaming.AsyncStream[
        chat.ChatCompletionChunk
    ] = await client.chat.completions.create(
        messages=list(completion_msg),
        model=model.name,
        stream=True,
        max_tokens=params.max_tokens,
        temperature=params.temperature,
    )
    commit_msg: str = ""
    with live.Live() as live_display:
        async for chunk in response:
            logger.debug(chunk.model_dump_json(indent=2))
            content: Optional[str] = chunk.choices[0].delta.content
            if content:
                commit_msg += content
            else:
                commit_msg += "\n"
            live_display.update(markdown.Markdown(msg.sanitize(commit_msg)))
    output_tokens: int = model.num_tokens_from_string(commit_msg)
    logger.info("Output Tokens: {}", f"{output_tokens:,}")
    price_in *= input_tokens / 1000
    price_out *= output_tokens / 1000
    logger.info(
        "Pricing: ${} = ${} (in) + ${} (out)",
        price_in + price_out,
        price_in,
        price_out,
    )
    sanitized: str = msg.sanitize(commit_msg)
    print(sanitized)
    await git.commit(msg=sanitized)


@app.command(name="aic")
def main(
    pathspec: Annotated[
        Optional[list[str]],
        typer.Argument(
            help="""When pathspec is given on the command line, commit the contents of \
the files that match the pathspec without recording the changes already added to the \
index. The contents of these files are also staged for the next commit on top of what \
have been staged before.

For more details, see the pathspec entry in gitglossary(7)."""
        ),
    ] = None,
    exclude: Annotated[Optional[list[str]], typer.Option("-e", "--exclude")] = None,
    *,
    # log
    log_level: Annotated[
        log.Level, typer.Option("--log", envvar="LOG_LEVEL", case_sensitive=False)
    ] = log.Level.INFO,
    log_file: Annotated[
        Optional[pathlib.Path], typer.Option(envvar="LOG_FILE", dir_okay=False)
    ] = None,
    # pre-commit
    pre_commit: Annotated[bool, typer.Option()] = True,
    # diff
    diff: Annotated[Optional[str], typer.Option()] = None,
    diff_file: Annotated[
        Optional[pathlib.Path], typer.Option(exists=True, dir_okay=False)
    ] = None,
    # prompt
    spec: Annotated[bool, typer.Option()] = True,
    # params
    models: Annotated[Optional[list[str]], typer.Option("-m", "--model")] = None,
    max_tokens: Annotated[int, typer.Option()] = 500,
    temperature: Annotated[float, typer.Option()] = 0.2,
    # API key
    api_key: Annotated[Optional[str], typer.Option(envvar="OPENAI_API_KEY")] = None,
) -> None:
    log.init(level=log_level, file=log_file)
    if pre_commit:
        if shutil.which("pre-commit"):
            root: pathlib.Path = asyncio.run(git.root())
            pre_commit = (root / ".pre-commit-config.yaml").exists()
        else:
            pre_commit = False
    if pathspec is None:
        pathspec = []
    if exclude is None:
        exclude = []
    pathspec += [f":(exclude){e}" for e in exclude]
    if not models:
        models = ["gpt-3.5-turbo-0125", "gpt-4-0125-preview"]
    if api_key is None:
        api_key = asyncio.run(bw.get_notes("OPENAI_API_KEY"))
    asyncio.run(
        main_async(
            pre_commit=pre_commit,
            diff=_diff.Diff(raw=diff, file=diff_file, pathspec=pathspec),
            prompt=_prompt.Prompt(spec=spec),
            params=gpt.Params(
                models=[gpt.Model(model) for model in models],
                max_tokens=max_tokens,
                temperature=temperature,
            ),
            api_key=api_key,
        )
    )
