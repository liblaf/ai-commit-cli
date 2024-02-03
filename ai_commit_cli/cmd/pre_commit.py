import asyncio
import subprocess
from asyncio import subprocess as asp
from collections.abc import Sequence

from loguru import logger


async def run() -> None:
    args: Sequence[str] = ["pre-commit"]
    logger.debug(args)
    proc: asp.Process = await asyncio.create_subprocess_exec(*args, stdin=asp.DEVNULL)
    returncode: int = await proc.wait()
    if returncode != 0:
        raise subprocess.CalledProcessError(
            returncode=returncode,
            cmd=args,
            output=await proc.stdout.read() if proc.stdout is not None else None,
            stderr=await proc.stderr.read() if proc.stderr is not None else None,
        )
