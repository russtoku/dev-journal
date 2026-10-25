import json
from dataclasses import asdict
from pathlib import Path

from .models import JournalEntry


class JournalDatabase:
    def __init__(self, db_path: Path):
        self.db_path = db_path

    def load_entries(self) -> list[JournalEntry]:
        if not self.db_path.exists() or self.db_path.stat().st_size == 0:
            return []
        with open(self.db_path) as f:
            return [JournalEntry(**e) for e in json.load(f)]

    def save_entries(self, entries: list[JournalEntry]) -> None:
        with open(self.db_path, "w") as f:
            json.dump([asdict(e) for e in entries], f, indent=2)

    def add_entry(self, title: str, content: str, tags: list[str]) -> None:
        entries = self.load_entries()
        entries.append(JournalEntry(title, content, tags))
        self.save_entries(entries)

    @staticmethod
    def search_entries(
        entries: list[JournalEntry], query: str, titles_only: bool = False
    ) -> list[JournalEntry]:
        """Returns entries that match the query. When the query
        (case-insensitive) is in the entry's title, content, or any of its
        tags, it's a match. When titles_only is False, just the entry's
        title is checked.
        When nothing matches, an empty list is returned.
        """
        q = query.lower()
        # filter entries for q
        if titles_only:
            results = [entry for entry in entries if q in entry.title.lower()]
        else:
            results = [
                entry
                for entry in entries
                if any(
                    q in p.lower() for p in [entry.title, entry.content] + entry.tags
                )
            ]

        return results
