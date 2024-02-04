# AI-Commit

A CLI that writes your git commit messages for you with AI

## Demo

![Demo](https://github.com/liblaf/ai-commit-cli/raw/assets/demo.gif)

## Usage

```help
 Usage: aic [OPTIONS] [PATHSPEC]...

╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────╮
│   pathspec      [PATHSPEC]...  When pathspec is given on the command line, commit the contents of    │
│                                the files that match the pathspec without recording the changes       │
│                                already added to the index. The contents of these files are also      │
│                                staged for the next commit on top of what have been staged before.    │
│                                For more details, see the pathspec entry in gitglossary(7).           │
│                                [default: None]                                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────╮
│ --exclude             -e                     TEXT                        [default: None]             │
│ --log                                        [TRACE|DEBUG|INFO|SUCCESS|  [env var: LOG_LEVEL]        │
│                                              WARNING|ERROR|CRITICAL]     [default: INFO]             │
│ --log-file                                   FILE                        [env var: LOG_FILE]         │
│                                                                          [default: None]             │
│ --pre-commit              --no-pre-commit                                [default: pre-commit]       │
│ --diff                                       TEXT                        [default: None]             │
│ --diff-file                                  FILE                        [default: None]             │
│ --spec                    --no-spec                                      [default: spec]             │
│ --model               -m                     TEXT                        [default: None]             │
│ --max-tokens                                 INTEGER                     [default: 500]              │
│ --temperature                                FLOAT                       [default: 0.2]              │
│ --api-key                                    TEXT                        [env var: OPENAI_API_KEY]   │
│                                                                          [default: None]             │
│ --install-completion                         [bash|zsh|fish|powershell|  Install completion for the  │
│                                              pwsh]                       specified shell.            │
│                                                                          [default: None]             │
│ --show-completion                            [bash|zsh|fish|powershell|  Show completion for the     │
│                                              pwsh]                       specified shell, to copy it │
│                                                                          or customize the            │
│                                                                          installation.               │
│                                                                          [default: None]             │
│ --help                                                                   Show this message and exit. │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
