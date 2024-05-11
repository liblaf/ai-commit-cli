import subprocess

import typer
from loguru import logger


def commit(message: str, *, verify: bool = True) -> None:
    args: list[str] = [
        "git",
        "commit",
        f"--message={message}",
        "--edit",
        "--verify" if verify else "--no-verify",
    ]
    logger.debug(args)
    proc: subprocess.CompletedProcess[bytes] = subprocess.run(args, check=False)
    if proc.returncode != 0:
        raise typer.Exit(proc.returncode)


def diff(*pathspec: str) -> str:
    args: list[str] = ["git", "diff", "--cached", "--no-ext-diff", *pathspec]
    logger.debug(args)
    proc: subprocess.CompletedProcess[str] = subprocess.run(
        args, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, check=True, text=True
    )
    return proc.stdout


def status(*pathspec: str) -> None:
    args: list[str] = ["git", "status", "--short", *pathspec]
    logger.debug(args)
    subprocess.run(args, stdin=subprocess.DEVNULL, check=True)
