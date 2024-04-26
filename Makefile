NAME := aic

default: fmt

dist:
	rye build --clean

fmt: fmt-toml/pyproject.toml

fmt-toml/%:
	toml-sort --in-place --all "$*"
	taplo format "$*"
