import subprocess
import sys


def get_notes(id: str) -> str:
    completed: subprocess.CompletedProcess = subprocess.run(
        args=["bw", "--nointeraction", "get", "notes", id],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=sys.stderr,
        check=True,
        text=True,
    )
    return completed.stdout
