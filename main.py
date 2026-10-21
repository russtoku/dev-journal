import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path

import typer

MAX_TITLE_LENGTH = 50
MAX_CONTENT_LENGTH = 1000

app = typer.Typer()


@dataclass
class JournalEntry:
    title: str
    content: str
    tags: list[str] = field(default_factory=list)
    date: str = field(default_factory=lambda: datetime.now().isoformat())

    def __post_init__(self):
        if not self.title or len(self.title) > MAX_TITLE_LENGTH:
            raise ValueError(
                f"Title must be non-empty and <= {MAX_TITLE_LENGTH} characters"
            )
        if not self.content or len(self.content) > MAX_CONTENT_LENGTH:
            raise ValueError(
                f"Content must be non-empty and <= {MAX_CONTENT_LENGTH} characters"
            )


def save_entries(entries: list[JournalEntry], db_path: Path) -> None:
    data = [asdict(entry) for entry in entries]
    with open(db_path, "w") as f:
        json.dump(data, f, indent=2)


def load_entries(db_path: Path) -> list[JournalEntry]:
    if not db_path.exists() or db_path.stat().st_size == 0:
        return []
    with open(db_path) as f:
        data = json.load(f)
    return [JournalEntry(**entry) for entry in data]


def add_entry(title: str, content: str, tags: list[str], db_path: Path) -> None:
    entries = load_entries(db_path)  # load exiting first
    entry = JournalEntry(title=title, content=content, tags=tags)
    entries.append(entry)  # append, don't overwrite
    save_entries(entries, db_path)


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

    try:
        add_entry(title, content, tag_list, db)
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
    entries = load_entries(db)  # list[JournalEntry]

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


def matches_query(entry: JournalEntry, query: str) -> bool:
    """returns True when the query (case-insensitive) is in the entry's title,
    content, or any of its tags.
    """
    q = query.lower()
    places = [entry.title, entry.content] + entry.tags
    return any(q in place.lower() for place in places)


@app.command()
def search(
    query: str = typer.Argument(..., help="Search term"),
    db: Path = typer.Option(Path("journal.json"), hidden=True),
) -> None:
    """Shows entries that match the query.
    When nothing matches, show a message containing "no".
    """
    entries = load_entries(db)  # list[JournalEntry]
    results = [entry for entry in entries if matches_query(entry, query)]
    if len(results) > 0:
        for entry in results:
            _display(entry)
    else:
        print("No entries match query")


def main():
    print("Hello from dev-journal!")


if __name__ == "__main__":
    app()
