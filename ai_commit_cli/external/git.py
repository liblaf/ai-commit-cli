import subprocess
import sys
from collections.abc import Sequence


def commit(message: str) -> None:
    subprocess.run(
        args=["git", "commit", "--file=-"],
        stdout=sys.stdout,
        stderr=sys.stderr,
        check=True,
        input=message,
        text=True,
    )


def diff(exclude: Sequence[str], include: Sequence[str]) -> str:
    completed: subprocess.CompletedProcess = subprocess.run(
        args=[
            "git",
            "diff",
            "--cached",
            *[":(exclude)" + p for p in exclude],
            *include,
        ],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=sys.stderr,
        check=True,
        text=True,
    )
    return completed.stdout


def status(exclude: Sequence[str], include: Sequence[str]) -> str:
    completed: subprocess.CompletedProcess = subprocess.run(
        args=[
            "git",
            *(["-c", "color.status=always"] if sys.stdout.isatty() else []),
            "status",
            *[":(exclude)" + p for p in exclude],
            *include,
        ],
        stdin=subprocess.DEVNULL,
        stdout=sys.stdout,
        stderr=sys.stderr,
        check=True,
        text=True,
    )
    return completed.stdout
