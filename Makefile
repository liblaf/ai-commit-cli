NAME   := ai-commit-cli
TARGET != rustc --version --verbose | sed --quiet "s/host: //p"

ifeq ($(OS), Windows_NT)
  EXE := .exe
else
  EXE :=
endif

all: check docs

check:
	cargo check
	cargo clippy

clean:
	@ rm --force --recursive --verbose dist
	cargo clean

dist: dist/$(NAME)-$(TARGET)$(EXE)

docs: docs/usage.md

###############
# Auxiliaries #
###############

dist/$(NAME)-$(TARGET)$(EXE): target/release/$(NAME)$(EXE)
	@ install -D --no-target-directory --verbose $< $@

.PHONY: docs/usage.md
docs/usage.md:
	@ mkdir --parents --verbose $(@D)
	cargo run complete markdown >$@
	- prettier --write $@

.PHONY: target/release/$(NAME)$(EXE)
target/release/$(NAME)$(EXE):
	cargo build --release
