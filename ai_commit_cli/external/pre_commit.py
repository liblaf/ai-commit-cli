import subprocess
import sys


def run() -> None:
    subprocess.run(
        args=["pre-commit", "run", "--color=always"],
        stdin=subprocess.DEVNULL,
        stdout=sys.stdout,
        stderr=sys.stderr,
        check=True,
    )
