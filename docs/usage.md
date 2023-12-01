# Command-Line Help for `ai-commit-cli`

This document contains the help content for the `ai-commit-cli` command-line program.

**Command Overview:**

- [`ai-commit-cli`↴](#ai-commit-cli)
- [`ai-commit-cli commit`↴](#ai-commit-cli-commit)
- [`ai-commit-cli complete`↴](#ai-commit-cli-complete)

## `ai-commit-cli`

**Usage:** `ai-commit-cli [OPTIONS] <COMMAND>`

###### **Subcommands:**

- `commit` —
- `complete` — Generate tab-completion scripts for your shell

###### **Options:**

- `-v`, `--verbose` — More output per occurrence
- `-q`, `--quiet` — Less output per occurrence

## `ai-commit-cli commit`

**Usage:** `ai-commit-cli commit [OPTIONS]`

###### **Options:**

- `-a`, `--api-key <API_KEY>` — If not provided, will use `bw get notes OPENAI_API_KEY`
- `-e`, `--exclude <EXCLUDE>`

  Default values: `*-lock.*`, `*.lock`

- `-i`, `--include <INCLUDE>`
- `--no-pre-commit`

  Default value: `false`

- `-p`, `--prompt <PROMPT>`
- `--prompt-file <PROMPT_FILE>`
- `--model <MODEL>` — ID of the model to use

  Default value: `gpt-3.5-turbo-16k`

- `--max-tokens <MAX_TOKENS>` — The maximum number of tokens to generate in the chat completion

  Default value: `500`

- `-n <N>` — How many chat completion choices to generate for each input message

  Default value: `1`

- `--temperature <TEMPERATURE>` — What sampling temperature to use, between 0 and 2

  Default value: `0`

- `--top-p <TOP_P>` — An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass

  Default value: `0.1`

## `ai-commit-cli complete`

Generate tab-completion scripts for your shell

```fish
$ ai-commit-cli complete fish >$HOME/.local/share/fish/vendor_completions.d
$ ai-commit-cli complete fish >/usr/local/share/fish/vendor_completions.d
```

**Usage:** `ai-commit-cli complete <SHELL>`

###### **Arguments:**

- `<SHELL>`

  Possible values: `markdown`, `bash`, `elvish`, `fish`, `powershell`, `zsh`

<hr/>

<small><i>
This document was generated automatically by
<a href="https://crates.io/crates/clap-markdown"><code>clap-markdown</code></a>.
</i></small>
