from datetime import datetime

from personal_assistant.models.note import Note


# --- Constructor ---


def test_note_stores_title() -> None:
    note = Note("Shopping", "Buy milk")
    assert note.title == "Shopping"


def test_note_stores_body() -> None:
    note = Note("Shopping", "Buy milk")
    assert note.body == "Buy milk"


def test_note_tags_initially_empty_list() -> None:
    note = Note("Shopping", "Buy milk")
    assert note.tags == []


def test_note_created_at_is_datetime_instance() -> None:
    note = Note("Shopping", "Buy milk")
    assert isinstance(note.created_at, datetime)


def test_note_id_is_non_empty_string() -> None:
    note = Note("Shopping", "Buy milk")
    assert isinstance(note.id, str)
    assert len(note.id) > 0


def test_two_notes_have_different_ids() -> None:
    note1 = Note("Shopping", "Buy milk")
    note2 = Note("Workout", "Go to the gym")
    assert note1.id != note2.id


# --- add_tag ---


def test_add_tag_appends_to_tags_list() -> None:
    note = Note("Shopping", "Buy milk")
    note.add_tag("groceries")
    assert len(note.tags) == 1


def test_add_multiple_tags_stores_all() -> None:
    note = Note("Shopping", "Buy milk")
    note.add_tag("groceries")
    note.add_tag("urgent")
    note.add_tag("weekly")
    assert len(note.tags) == 3


def test_add_tag_stores_correct_value() -> None:
    note = Note("Shopping", "Buy milk")
    note.add_tag("groceries")
    assert note.tags[0] == "groceries"


# --- __str__ ---


def test_str_contains_title() -> None:
    note = Note("Shopping", "Buy milk")
    assert "Shopping" in str(note)


def test_str_contains_body() -> None:
    note = Note("Shopping", "Buy milk")
    assert "Buy milk" in str(note)
