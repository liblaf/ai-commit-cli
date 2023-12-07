import os

import typer

from ai_commit_cli import logging as my_logging
from ai_commit_cli.cmd import commit

my_logging.init(level=os.getenv("LOG_LEVEL", "INFO"))
app: typer.Typer = typer.Typer()
app.command(name="commit")(commit.main)

if __name__ == "__main__":
    app()
