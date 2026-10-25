from rich.console import Console
from rich.table import Table

console = Console()

table = Table(show_header=True, header_style="bold magenta")
table.add_column("Language")
table.add_column("Notes", style="italic yellow")
table.add_row("[bold]Python[/bold]\nReadable", "batteries included")
table.add_row("[bold]Rust[/bold]\nFast", "no garbage collector")
console.print(table)
