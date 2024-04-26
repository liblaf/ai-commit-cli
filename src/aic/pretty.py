import babel.numbers


def format_int(value: int) -> str:
    return babel.numbers.format_number(value)


def format_currency(value: float) -> str:
    return babel.numbers.format_currency(
        round(value, 8), "USD", decimal_quantization=False
    )
