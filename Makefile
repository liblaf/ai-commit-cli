NAME   := ai-commit-cli
TARGET != rustc --version --verbose | sed --quiet "s/host: //p"

ifeq ($(OS), Windows_NT)
  EXE := .exe
else
  EXE :=
endif

all: check

check:
	cargo check
	cargo clippy

clean:
	@ $(RM) --recursive --verbose dist
	cargo clean

dist: dist/$(NAME)-$(TARGET)$(EXE)

###############
# Auxiliaries #
###############

dist/$(NAME)-$(TARGET)$(EXE): target/release/$(NAME)$(EXE)
	@ install -D --no-target-directory --verbose $< $@

.PHONY: target/release/$(NAME)$(EXE)
target/release/$(NAME)$(EXE):
	cargo build --release
