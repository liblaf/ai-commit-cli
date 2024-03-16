import asyncio
import subprocess
from asyncio import subprocess as asp
from collections.abc import Sequence

from loguru import logger


async def get_notes(id: str) -> str:
    args: Sequence[str] = ["bw", "--nointeraction", "get", "notes", id]
    logger.debug(args)
    proc: asp.Process = await asyncio.create_subprocess_exec(
        *args, stdin=asp.DEVNULL, stdout=asp.PIPE
    )
    assert proc.stdout is not None
    output: str = (await proc.stdout.read()).decode()
    returncode: int = await proc.wait()
    if returncode != 0:
        raise subprocess.CalledProcessError(
            returncode=returncode, cmd=args, output=output
        )
    return output
