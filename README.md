# AI-Commit

A CLI that writes your git commit messages for you with AI

## Usage

```help
Usage: aic [OPTIONS] [PATHSPEC]...

Arguments:
  [PATHSPEC]...

Options:
  --api-key TEXT                  [env var: OPENAI_API_KEY]
  --base-url TEXT                 [env var: OPENAI_BASE_URL]
  --diff FILE
  --models TEXT
  --provider [openai]             [default: openai]
  --prompt [conventional]         [default: conventional]
  --dry-run / --no-dry-run        [default: no-dry-run]
  --list-models / --no-list-models
                                  [default: no-list-models]
  --quota / --no-quota            [default: no-quota]
  --stream / --no-stream          [default: stream]
  --verify / --no-verify          [default: verify]
  --help                          Show this message and exit.
```
