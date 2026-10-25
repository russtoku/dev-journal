from rich.console import Console
from rich.table import Table

from .models import JournalEntry

console = Console()

table = Table(show_header=True, header_style="bold green")
table.add_column("Date")
table.add_column("Note")
table.add_column("Tags")


def list_entries(entries: list[JournalEntry]) -> None:
    if len(entries) > 0:
        for entry in entries:
            table.add_row(
                entry.date[:16],
                f"[bold]{entry.title}[/bold]\n{entry.content}",
                ", ".join(entry.tags),
            )
        console.print(table)
    else:
        print("No journal entries found")
