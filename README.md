# Dev Journal

A command-line journal for tracking what you learn. Add entries, tag them,
search, and list them in a formatted table.

## Install

```bash
git clone git@github.com:you/dev-journal.git
cd dev-journal
uv sync
```

## Usage

```bash
uv run journal add --title "Learned uv" --content "One tool for everything" --tags "python"
uv run journal list --tag python
uv run journal search pytest
```

## Develop

```bash
uv run ruff format .
uv run ruff check .
uv run pytest --cov=journal
```
