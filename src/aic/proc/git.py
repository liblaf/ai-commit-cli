import asyncio
import pathlib
import subprocess
from asyncio import subprocess as asp
from collections.abc import Sequence

import typer
from loguru import logger


async def commit(msg: str, verify: bool = True) -> None:
    args: Sequence[str] = [
        "git",
        "commit",
        f"--message={msg}",
        "--edit",
        "--verify" if verify else "--no-verify",
    ]
    logger.debug(args)
    proc: asp.Process = await asyncio.create_subprocess_exec(*args)
    returncode: int = await proc.wait()
    if returncode != 0:
        raise typer.Exit(returncode)


async def diff(pathspec: Sequence[str] | None = None) -> str:
    if pathspec is None:
        pathspec = []
    args: Sequence[str] = ["git", "diff", "--cached", *pathspec]
    logger.debug(args)
    proc: asp.Process = await asyncio.create_subprocess_exec(
        *args, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE
    )
    assert proc.stdout is not None
    output: str = (await proc.stdout.read()).decode()
    returncode: int = await proc.wait()
    if returncode != 0:
        raise subprocess.CalledProcessError(
            returncode=returncode, cmd=args, output=output
        )
    return output


async def root() -> pathlib.Path:
    args: Sequence[str] = ["git", "rev-parse", "--show-toplevel"]
    logger.debug(args)
    proc: asp.Process = await asyncio.create_subprocess_exec(
        *args, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE
    )
    assert proc.stdout is not None
    output: str = (await proc.stdout.read()).decode()
    returncode: int = await proc.wait()
    if returncode != 0:
        raise subprocess.CalledProcessError(
            returncode=returncode, cmd=args, output=output
        )
    return pathlib.Path(output.strip())


async def status(pathspec: Sequence[str] | None = None) -> None:
    if pathspec is None:
        pathspec = []
    args: Sequence[str] = ["git", "status", "--short", *pathspec]
    logger.debug(args)
    proc: asp.Process = await asyncio.create_subprocess_exec(
        *args, stdin=subprocess.DEVNULL
    )
    returncode: int = await proc.wait()
    if returncode != 0:
        raise subprocess.CalledProcessError(returncode=returncode, cmd=args)
