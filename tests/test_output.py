from journal.models import JournalEntry
from journal.output import list_entries


def test_list_entries_renders_content(capsys):
    entries = [
        JournalEntry(title="Test Entry", content="Content", tags=["python"]),
        JournalEntry(title="Another Entry", content="More content", tags=["rust"]),
    ]
    list_entries(entries)
    out = capsys.readouterr().out
    assert "Test Entry" in out
    assert "Another Entry" in out
    assert "python" in out


def test_list_entries_empty(capsys):
    list_entries([])
    out = capsys.readouterr().out
    assert "No journal entries found" in out
