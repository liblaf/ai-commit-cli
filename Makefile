default: check format toml-sort

check:
	- ruff check

format:
	ruff format

toml-sort: toml-sort\:pyproject.toml
toml-sort: toml-sort\:ruff.toml

toml-sort\:%: %
	toml-sort --in-place --all "$<"
	taplo format "$<"
