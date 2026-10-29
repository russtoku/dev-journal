# Dev Journal

A command-line journal for tracking what you learn. Add entries, tag them,
search, and list them in a formatted table.

From Bob Belderbos's [Ship Your First Python App: a Free Course on the Local Dev Workflow](https://belderbos.dev/blog/free-python-foundations-course-local-dev-workflow/) posted on September 19, 2026.
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
