import asyncio
import pathlib
import subprocess
import sys
from asyncio import subprocess as asp
from collections.abc import Sequence
from typing import Optional

from loguru import logger


async def commit(msg: str) -> None:
    args: Sequence[str] = ["git", "commit", f"--message={msg}", "--edit"]
    logger.debug(args)
    proc: asp.Process = await asyncio.create_subprocess_exec(*args)
    returncode: int = await proc.wait()
    if returncode != 0:
        sys.exit(returncode)


async def diff(pathspec: Optional[Sequence[str]] = None) -> str:
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
            returncode=returncode,
            cmd=args,
            output=output,
            stderr=await proc.stderr.read() if proc.stderr is not None else None,
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
            returncode=returncode,
            cmd=args,
            output=output,
            stderr=await proc.stderr.read() if proc.stderr is not None else None,
        )
    return pathlib.Path(output.strip())


async def status(pathspec: Optional[Sequence[str]] = None) -> None:
    if pathspec is None:
        pathspec = []
    args: Sequence[str] = ["git", "status", "--short", *pathspec]
    logger.debug(args)
    proc: asp.Process = await asyncio.create_subprocess_exec(
        *args, stdin=subprocess.DEVNULL
    )
    returncode: int = await proc.wait()
    if returncode != 0:
        raise subprocess.CalledProcessError(
            returncode=returncode,
            cmd=args,
            output=await proc.stdout.read() if proc.stdout is not None else None,
            stderr=await proc.stderr.read() if proc.stderr is not None else None,
        )
