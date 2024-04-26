import babel.numbers
import rich
from rich.table import Table

from aic import pretty as _pretty
from aic.api import openrouter as _openrouter


def list_models() -> None:
    models: list[_openrouter.Model] = _openrouter.get_models()
    table = Table(title="Models")
    table.add_column("ID", style="bright_cyan")
    table.add_column("Context", style="bright_magenta", justify="right")
    table.add_column("Prompt", style="bright_green", justify="left")
    table.add_column("Completion", style="bright_green", justify="left")
    for model in models:
        if not model.id.startswith("openai/"):
            continue
        table.add_row(
            model.id.removeprefix("openai/"),
            babel.numbers.format_number(model.context_length),
            _pretty.format_currency(model.pricing.prompt * 1000),
            _pretty.format_currency(model.pricing.completion * 1000),
        )
    rich.print(table)
