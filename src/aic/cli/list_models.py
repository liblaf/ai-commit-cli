import babel.numbers
from rich import live as rich_live
from rich import table as rich_table

from aic import provider as _provider


def _pretty_int(value: int | None) -> str | None:
    return f"{value:,}" if value else None


def _pretty_pricing(pricing: _provider.Pricing | None) -> str | None:
    if pricing is None:
        return None

    def format_currency(number: float) -> str:
        return babel.numbers.format_currency(
            round(number * 1e3, 8), pricing.currency, decimal_quantization=False
        )

    return (
        f"{format_currency(pricing.input):<7s} / {format_currency(pricing.output):<7s}"
    )


async def list_models(provider: _provider.Provider) -> None:
    table = rich_table.Table()
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Created", style="magenta", no_wrap=True)
    table.add_column("Context Window", style="green", justify="right", no_wrap=True)
    table.add_column("Pricing / 1k tokens", style="yellow", no_wrap=True)
    with rich_live.Live() as live:
        async for model in provider.list_models():
            table.add_row(
                model.id,
                str(model.created),
                _pretty_int(model.context_window),
                _pretty_pricing(model.pricing),
            )
            live.update(table)
