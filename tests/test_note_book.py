import pytest

from personal_assistant.models.note import Note
from personal_assistant.models.note_book import NoteBook


@pytest.fixture
def notebook() -> NoteBook:
    return NoteBook()


@pytest.fixture
def sample_note() -> Note:
    return Note("Shopping", "Buy milk and eggs")


# --- add_note ---


def test_add_note_stores_in_notebook(notebook: NoteBook, sample_note: Note) -> None:
    notebook.add_note(sample_note)
    assert sample_note.id in notebook.data


def test_add_note_can_find_by_id(notebook: NoteBook, sample_note: Note) -> None:
    notebook.add_note(sample_note)
    assert notebook.find(sample_note.id) is sample_note


# --- find ---


def test_find_existing_note_returns_note(notebook: NoteBook, sample_note: Note) -> None:
    notebook.add_note(sample_note)
    result = notebook.find(sample_note.id)
    assert isinstance(result, Note)


def test_find_non_existing_returns_none(notebook: NoteBook) -> None:
    result = notebook.find("non-existing-id")
    assert result is None


# --- delete ---


def test_delete_existing_note_removes_it(notebook: NoteBook, sample_note: Note) -> None:
    notebook.add_note(sample_note)
    notebook.delete(sample_note.id)
    assert notebook.find(sample_note.id) is None


def test_delete_non_existing_does_not_raise(notebook: NoteBook) -> None:
    notebook.delete("non-existing-id")


# --- edit_note ---


def test_edit_note_changes_body(notebook: NoteBook, sample_note: Note) -> None:
    notebook.add_note(sample_note)
    notebook.edit_note(sample_note.id, "Buy bread and butter")
    assert notebook.find(sample_note.id).body == "Buy bread and butter"


def test_edit_note_preserves_title_and_tags(notebook: NoteBook, sample_note: Note) -> None:
    sample_note.add_tag("groceries")
    notebook.add_note(sample_note)
    notebook.edit_note(sample_note.id, "Updated body")
    note = notebook.find(sample_note.id)
    assert note.title == "Shopping"
    assert "groceries" in note.tags


def test_edit_non_existing_note_raises_key_error(notebook: NoteBook) -> None:
    with pytest.raises(KeyError):
        notebook.edit_note("non-existing-id", "New body")


# --- find_by_text ---


def test_find_by_text_matches_title_case_insensitive(notebook: NoteBook, sample_note: Note) -> None:
    notebook.add_note(sample_note)
    results = notebook.find_by_text("shopping")
    assert len(results) == 1


def test_find_by_text_matches_body_case_insensitive(notebook: NoteBook, sample_note: Note) -> None:
    notebook.add_note(sample_note)
    results = notebook.find_by_text("milk")
    assert len(results) == 1


def test_find_by_text_returns_empty_when_no_match(notebook: NoteBook, sample_note: Note) -> None:
    notebook.add_note(sample_note)
    results = notebook.find_by_text("nonexistent")
    assert results == []


def test_find_by_text_returns_multiple_matches(notebook: NoteBook) -> None:
    note1 = Note("Shopping list", "Buy milk")
    note2 = Note("Grocery plan", "Buy eggs and milk")
    note3 = Note("Workout", "Go to the gym")
    notebook.add_note(note1)
    notebook.add_note(note2)
    notebook.add_note(note3)
    results = notebook.find_by_text("buy")
    assert len(results) == 2


# --- find_by_tag ---


def test_find_by_tag_returns_matching_notes(notebook: NoteBook, sample_note: Note) -> None:
    sample_note.add_tag("groceries")
    notebook.add_note(sample_note)
    results = notebook.find_by_tag("groceries")
    assert len(results) == 1


def test_find_by_tag_returns_empty_when_no_match(notebook: NoteBook, sample_note: Note) -> None:
    sample_note.add_tag("groceries")
    notebook.add_note(sample_note)
    results = notebook.find_by_tag("fitness")
    assert results == []


def test_find_by_tag_returns_multiple_notes_with_same_tag(notebook: NoteBook) -> None:
    note1 = Note("Shopping", "Buy milk")
    note1.add_tag("urgent")
    note2 = Note("Work", "Finish report")
    note2.add_tag("urgent")
    notebook.add_note(note1)
    notebook.add_note(note2)
    results = notebook.find_by_tag("urgent")
    assert len(results) == 2


# --- sort_by_tags ---


def test_sort_by_tags_alphabetical_order(notebook: NoteBook) -> None:
    note_b = Note("B note", "Body B")
    note_b.add_tag("beta")
    note_a = Note("A note", "Body A")
    note_a.add_tag("alpha")
    notebook.add_note(note_b)
    notebook.add_note(note_a)
    sorted_notes = notebook.sort_by_tags()
    assert sorted_notes[0].tags[0] == "alpha"
    assert sorted_notes[1].tags[0] == "beta"


def test_sort_by_tags_notes_without_tags_go_last(notebook: NoteBook) -> None:
    note_no_tag = Note("No tag", "Body without tag")
    note_with_tag = Note("With tag", "Body with tag")
    note_with_tag.add_tag("alpha")
    notebook.add_note(note_no_tag)
    notebook.add_note(note_with_tag)
    sorted_notes = notebook.sort_by_tags()
    assert sorted_notes[0].tags[0] == "alpha"
    assert sorted_notes[-1].tags == []


def test_sort_by_tags_returns_all_notes(notebook: NoteBook) -> None:
    note1 = Note("Note 1", "Body 1")
    note1.add_tag("beta")
    note2 = Note("Note 2", "Body 2")
    note3 = Note("Note 3", "Body 3")
    note3.add_tag("alpha")
    notebook.add_note(note1)
    notebook.add_note(note2)
    notebook.add_note(note3)
    sorted_notes = notebook.sort_by_tags()
    assert len(sorted_notes) == 3
