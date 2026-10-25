from pathlib import Path

import typer

from .db import JournalDatabase
from .models import JournalEntry

app = typer.Typer()


@app.command()
def add(
    title: str = typer.Option("", prompt="Title", show_default=False),
    content: str = typer.Option("", prompt="Content", show_default=False),
    tags: str = typer.Option("", prompt="Tags (comma separated)", show_default=False),
    db: Path = typer.Option(Path("journal.json"), hidden=True),
) -> None:
    # turn "python, cli" into ["python", "cli"], save the entry,
    # echo "Entry saved.", and handle a ValueError as shown above
    # tag_list = tags.split(",")
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []

    dbh = JournalDatabase(db)
    try:
        dbh.add_entry(title, content, tag_list)
    except ValueError as e:
        raise typer.BadParameter(str(e)) from e

    print("Entry saved")


def _display(entry: JournalEntry) -> None:
    """Print an entry."""
    print(
        f"Title: {entry.title}, Content: {entry.content}, Tags: {', '.join(entry.tags)}"
    )


@app.command("list")
def list_entries(
    tag: list[str] = typer.Option([], help="Filter by tag (repeatable)"),
    limit: int = typer.Option(0, help="Show last N entries (0 = all)"),
    db: Path = typer.Option(Path("journal.json"), hidden=True),
) -> None:
    """When the --tag flag is used, shows entries that have that tag value.
    Multiple tag values may be specified. When there are multiple tags, an
    entry is selected if at least one of its tags match at least one of the
    tags specified with the --tag flag. Tag match is an exact match; not
    partial.

    Shows the newest N entries when the --limit flag is used.

    The order matters: filter by tag first, then limit the number of entries
    shown.
    """

    # load the entries; if there are none, echo a message containing "no",
    # otherwise echo each entry's title, date, content, and tags
    dbh = JournalDatabase(db)
    entries = dbh.load_entries()

    if tag:
        # filter for tags
        wanted = [t.lower() for t in tag]
        entries = [e for e in entries if any(et.lower() in wanted for et in e.tags)]

    # limit entries
    if entries:
        for entry in entries[-limit:]:
            _display(entry)
    else:
        print("No entries.")


@app.command()
def search(
    query: str = typer.Argument(..., help="Search term"),
    db: Path = typer.Option(Path("journal.json"), hidden=True),
) -> None:
    """Shows entries that match the query.
    When nothing matches, show a message containing "no".
    """
    dbh = JournalDatabase(db)
    entries = dbh.load_entries()
    q = query.lower()
    results = [
        entry
        for entry in entries
        if any(q in p.lower() for p in [entry.title, entry.content] + entry.tags)
    ]
    if len(results) > 0:
        for entry in results:
            _display(entry)
    else:
        print("No entries match query")
