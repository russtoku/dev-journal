import pytest

from journal.models import MAX_CONTENT_LENGTH, MAX_TITLE_LENGTH, JournalEntry


def test_valid_journal_entry():
    entry = JournalEntry(title="Test", content="Content")
    assert entry.title == "Test"
    assert entry.tags == []
    assert entry.date is not None


def test_title_too_long():
    with pytest.raises(ValueError):
        JournalEntry(title="T" * (MAX_TITLE_LENGTH + 1), content="Valid")


def test_content_too_long():
    with pytest.raises(ValueError):
        JournalEntry(title="Valid", content="C" * (MAX_CONTENT_LENGTH + 1))


def test_empty_title():
    with pytest.raises(ValueError):
        JournalEntry(title="", content="Valid")


def test_empty_content():
    with pytest.raises(ValueError):
        JournalEntry(title="Valid", content="")


def test_each_entry_gets_own_tag_list():
    a = JournalEntry(title="A", content="C")
    b = JournalEntry(title="B", content="C")
    a.tags.append("python")
    assert b.tags == []
